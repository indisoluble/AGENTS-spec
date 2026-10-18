"""Exercise fixture and response plumbing with local files and a fake CLI only.

The executable below writes predetermined replies. It never runs real Codex,
authenticates with OpenAI, or evaluates whether a reply is behaviorally correct.
"""

import base64
from contextlib import redirect_stderr
from io import StringIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from pydantic_evals import Case, Dataset

from evals.auth import PROFILE_CONFIG
from evals.codex import run_codex
from evals.smoke import CONTRACT_PATH, ExecutionResult, evaluate, prepare_workspace, read_fixture_file


FIXTURE_FILES = {
    "src/app.py": b"value = 1\n",
    "data/input.bin": b"\x00\xff\r\n",
    "README.md": b"A test fixture.\n",
}

# Version/login replies imitate the CLI protocol using dummy profile files.
# Progress messages deliberately differ from the separately captured final reply.
FAKE_CLI = r'''
import json
import os
from pathlib import Path
import sys

profile = Path(os.environ["CODEX_HOME"])
if "--version" in sys.argv:
    print("codex-cli test")
elif "login" in sys.argv:
    print("Logged in using ChatGPT")
else:
    sys.stdin.read()
    with (profile / "invocations").open("a") as log:
        log.write("exec\n")
    settings = json.loads((profile / "response-settings.json").read_text())
    mode = settings["mode"]
    workspace = Path(sys.argv[sys.argv.index("--cd") + 1])
    if (workspace / "message.txt").exists():
        (workspace / "message.txt").write_bytes(b"after\n")
    else:
        (workspace / "src/app.py").write_bytes(b"value = 2\n")
        (workspace / "notes").mkdir()
        (workspace / "notes/decision.md").write_bytes(b"Test note.\n")
        (workspace / "link").symlink_to(profile / "auth.json")
        (workspace / "empty").mkdir()
        os.mkfifo(workspace / "pipe")
    print(json.dumps({"type": "item.completed", "item": {
        "type": "agent_message", "text": "Progress only: starting work."
    }}))
    if "--output-last-message" in sys.argv:
        destination = Path(sys.argv[sys.argv.index("--output-last-message") + 1])
        assert not destination.resolve().is_relative_to(workspace.resolve())
        if mode == "directory":
            destination.mkdir()
        elif mode == "symlink":
            destination.symlink_to(profile / "auth.json")
        elif mode == "fifo":
            os.mkfifo(destination)
        elif mode == "invalid-utf8":
            destination.write_bytes(b"\xff")
        elif mode not in ("missing", "nonzero-missing"):
            destination.write_bytes(settings["text"].encode("utf-8"))
    if mode.startswith("nonzero"):
        print("Simulated execution failure", file=sys.stderr)
        sys.exit(7)
    print(json.dumps({"type": "item.completed", "item": {
        "type": "agent_message", "text": "Progress only: finishing work."
    }}))
    print(json.dumps({"type": "turn.completed"}))
'''


def fixture_dataset():
    # This case tests execution plumbing only; it has no behavioral assertions.
    return Dataset(
        name="capture-fixture",
        cases=[Case(name="capture-fixture", inputs="Exercise the test fixture.")],
    )


class MultiFileFixtureTests(unittest.TestCase):
    def test_each_run_recreates_exact_files_and_contract_without_implicit_message(self):
        workspaces = []

        def inspect_then_dirty(prompt, workspace):
            workspaces.append(workspace)
            self.assertEqual((workspace / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())
            self.assertFalse((workspace / "message.txt").exists())
            self.assertFalse((workspace / "residue").exists())
            for name, contents in FIXTURE_FILES.items():
                self.assertEqual((workspace / name).read_bytes(), contents)
            (workspace / "src/app.py").write_bytes(b"changed")
            (workspace / "residue").touch()
            return ExecutionResult("completed")

        for _ in range(2):
            report = evaluate(inspect_then_dirty, dataset=fixture_dataset(), fixture_files=FIXTURE_FILES)
            self.assertEqual(report.failures, [])
        self.assertEqual(len(set(workspaces)), 2)
        self.assertTrue(all(not path.exists() for path in workspaces))

    def test_empty_mapping_creates_only_the_root_contract(self):
        with prepare_workspace(fixture_files={}) as workspace:
            self.assertEqual([path.name for path in workspace.iterdir()], ["AGENTS.md"])

    def test_fixture_paths_cannot_escape_or_override_the_contract(self):
        paths = ("../outside", "/absolute", ".", "", "AGENTS.md", "./agents.md", "AGENTS.md/child")
        for path in paths:
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "Invalid fixture path"):
                with prepare_workspace(fixture_files={path: b"unwanted"}):
                    self.fail("Invalid fixture was accepted")

    def test_failed_fixture_setup_removes_its_temporary_directory(self):
        directories = []

        def track_directory(**kwargs):
            temporary = TemporaryDirectory(**kwargs)
            directories.append(Path(temporary.name))
            return temporary

        with patch("evals.smoke.TemporaryDirectory", side_effect=track_directory):
            with self.assertRaises(OSError):
                # A regular file cannot also serve as a parent directory.
                with prepare_workspace(fixture_files={"parent": b"file", "parent/child": b"data"}):
                    self.fail("Conflicting fixture paths were accepted")
        self.assertEqual(len(directories), 1)
        self.assertFalse(directories[0].exists())


class FinalResponseCaptureTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(TemporaryDirectory()))
        self.profile = self.root / "profile"
        self.profile.mkdir()
        (self.profile / "config.toml").write_text(PROFILE_CONFIG)
        (self.profile / "auth.json").write_text("dummy credential: never copy")
        executable = self.root / "codex"
        executable.write_text(f"#!{sys.executable}\n" + FAKE_CLI)
        executable.chmod(0o700)
        self.enterContext(patch("evals.auth.codex_executable", return_value=str(executable)))
        self.run_count = 0

    def run_fixture(self, *, text="Final reply.\n", mode="success", capture=True, files=FIXTURE_FILES):
        self.run_count += 1
        artifacts = self.root / f"run-{self.run_count}"
        artifacts.mkdir()
        (self.profile / "response-settings.json").write_text(json.dumps({"text": text, "mode": mode}))
        results = []

        def execute(prompt, workspace):
            result = run_codex(prompt, workspace, model="test", effort="medium", timeout=3,
                               artifacts=artifacts, profile=self.profile,
                               observe_workspace=True, capture_response=capture)
            results.append(result)
            return result

        report = evaluate(execute, dataset=fixture_dataset() if files is not None else None, fixture_files=files)
        metadata = json.loads((artifacts / "execution.json").read_text())
        self.assertFalse(Path(metadata["workspace"]).exists())
        self.assertEqual((self.profile / "invocations").read_text(), "exec\n" * self.run_count)
        return report, results[0], artifacts, metadata

    def test_captures_exact_final_response_separately_from_progress(self):
        for response in ("  ¿Which source timezone?\r\n\r\n", "", " \n\t"):
            with self.subTest(response=response):
                report, result, artifacts, metadata = self.run_fixture(text=response)
                self.assertEqual(report.failures, [])
                self.assertEqual(result.status, "completed")
                self.assertEqual(result.final_response, response)
                self.assertEqual(report.cases[0].output.final_response, response)
                self.assertIsNone(result.file_contents)
                self.assertEqual((artifacts / "final-response.txt").read_bytes(), response.encode("utf-8"))
                command = metadata["command"]
                self.assertEqual(command[command.index("--output-last-message") + 1],
                                 str((artifacts / "final-response.txt").resolve()))
                self.assertEqual(command[-1], "-")
                self.assertIn("Progress only", (artifacts / "events.jsonl").read_text())
                self.assertNotIn("Progress only", result.final_response)
                self.assertNotIn("final-response.txt", result.workspace_observation.final)

    def test_retains_multifile_initial_and_final_bytes_without_recreating_links_or_special_files(self):
        report, result, artifacts, _ = self.run_fixture()
        self.assertEqual(report.failures, [])
        for name, contents in {"AGENTS.md": CONTRACT_PATH.read_bytes(), **FIXTURE_FILES}.items():
            self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
        self.assertEqual((artifacts / "workspace/src/app.py").read_bytes(), b"value = 2\n")
        self.assertEqual((artifacts / "workspace/data/input.bin").read_bytes(), FIXTURE_FILES["data/input.bin"])
        self.assertEqual((artifacts / "workspace/notes/decision.md").read_bytes(), b"Test note.\n")
        self.assertFalse((artifacts / "message.txt").exists())
        final = json.loads((artifacts / "final-workspace.json").read_text())
        initial = json.loads((artifacts / "initial-workspace.json").read_text())
        self.assertEqual(base64.b64decode(initial["src/app.py"]["contents_base64"]), FIXTURE_FILES["src/app.py"])
        for name, kind in (("link", "symlink"), ("pipe", "fifo"), ("empty", "directory")):
            self.assertEqual(final[name]["kind"], kind)
            self.assertIsNone(final[name]["contents_base64"])
            self.assertFalse((artifacts / "workspace" / name).exists())
        self.assertNotIn("dummy credential", (artifacts / "final-workspace.json").read_text())
        self.assertNotIn("dummy credential", result.final_response)

    def test_disabled_capture_keeps_the_default_smoke_result(self):
        report, result, artifacts, metadata = self.run_fixture(capture=False, files=None)
        self.assertEqual(report.failures, [])
        self.assertTrue(report.cases[0].assertions["ExactFileContents"].value)
        self.assertIsNone(result.final_response)
        self.assertNotIn("--output-last-message", metadata["command"])
        self.assertFalse((artifacts / "final-response.txt").exists())
        self.assertEqual((artifacts / "message.txt").read_bytes(), b"before\n")

    def test_missing_invalid_or_nonregular_capture_is_an_error_without_grading(self):
        for mode in ("missing", "invalid-utf8", "directory", "symlink", "fifo"):
            with self.subTest(mode=mode):
                report, result, artifacts, metadata = self.run_fixture(mode=mode)
                self.assertEqual(result.status, "error")
                self.assertIsNone(result.final_response)
                self.assertIn("Final response capture failed", result.error)
                self.assertEqual(report.cases, [])
                self.assertEqual(len(report.failures), 1)
                self.assertEqual(metadata["returncode"], 0)
                self.assertEqual(metadata["status"], "error")
                self.assertTrue((artifacts / "final-workspace.json").is_file())
                self.assertTrue((artifacts / "workspace/src/app.py").is_file())

    def test_execution_failure_retains_response_or_reports_capture_failure_without_hiding_original(self):
        for mode in ("nonzero", "nonzero-missing"):
            with self.subTest(mode=mode):
                report, result, artifacts, metadata = self.run_fixture(mode=mode, text="Available reply.")
                self.assertEqual(report.cases, [])
                self.assertIn("Codex exited with status 7", result.error)
                self.assertEqual(metadata["returncode"], 7)
                if mode == "nonzero":
                    self.assertEqual(result.final_response, "Available reply.")
                    self.assertEqual((artifacts / "final-response.txt").read_text(), "Available reply.")
                else:
                    self.assertIsNone(result.final_response)
                    self.assertIn("final-response.txt was not produced", result.error)
                self.assertTrue((artifacts / "initial-workspace.json").is_file())
                self.assertTrue((artifacts / "final-workspace.json").is_file())

    def test_response_read_failure_retains_raw_capture_and_workspace_evidence(self):
        def deny_response(path):
            if path.name == "final-response.txt":
                raise PermissionError("simulated response read failure")
            return read_fixture_file(path)

        with patch("evals.codex.read_fixture_file", side_effect=deny_response):
            report, result, artifacts, _ = self.run_fixture()
        self.assertEqual(report.cases, [])
        self.assertEqual(result.status, "error")
        self.assertIn("simulated response read failure", result.error)
        self.assertIsNone(result.final_response)
        self.assertEqual((artifacts / "final-response.txt").read_text(), "Final reply.\n")
        self.assertTrue((artifacts / "final-workspace.json").is_file())

    def test_copy_failure_preserves_captured_response_and_primary_execution_error(self):
        write_bytes = Path.write_bytes

        def deny_one_copy(path, contents):
            if path.parts[-3:] == ("workspace", "src", "app.py"):
                raise PermissionError("simulated copy failure")
            return write_bytes(path, contents)

        with patch.object(Path, "write_bytes", autospec=True, side_effect=deny_one_copy), redirect_stderr(StringIO()):
            report, result, artifacts, metadata = self.run_fixture(mode="nonzero")
        self.assertEqual(report.cases, [])
        self.assertIn("Codex exited with status 7", result.error)
        self.assertIn("simulated copy failure", result.error)
        self.assertEqual(result.final_response, "Final reply.\n")
        self.assertTrue(metadata["evidence_errors"])
        self.assertEqual((artifacts / "workspace/data/input.bin").read_bytes(), FIXTURE_FILES["data/input.bin"])
        self.assertEqual((artifacts / "initial-workspace/src/app.py").read_bytes(), FIXTURE_FILES["src/app.py"])

    def test_capture_target_inside_workspace_or_existing_reply_is_rejected_before_execution(self):
        for invalid in ("inside", "existing"):
            with self.subTest(invalid=invalid), prepare_workspace() as workspace:
                artifacts = workspace / "evidence" if invalid == "inside" else self.root / "existing"
                artifacts.mkdir()
                if invalid == "existing":
                    (artifacts / "final-response.txt").write_bytes(b"stale reply")
                result = run_codex("test", workspace, model="test", effort="medium", timeout=3,
                                   artifacts=artifacts, profile=self.profile, capture_response=True)
                self.assertEqual(result.status, "error")
                self.assertIsNone(result.final_response)
                self.assertIn("outside" if invalid == "inside" else "already exists", result.error)
                self.assertFalse((self.profile / "invocations").exists())


if __name__ == "__main__":
    unittest.main()
