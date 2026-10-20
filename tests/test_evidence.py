"""Regression checks using temporary files and substitutes, never real Codex or login."""

from contextlib import redirect_stderr, redirect_stdout
from functools import partial
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evals.__main__ import main
from evals.codex import retain_evidence, run_codex
from evals.evaluation import ExecutionResult, read_result
from evals.scope import INITIAL_CONTENTS
from evals.smoke import evaluate
from evals.workspace import WorkspaceObservation, prepare_workspace, snapshot_workspace
from tests.offline_smoke import write_after


class EvidenceTests(unittest.TestCase):
    def test_nonregular_output_is_rejected_without_blocking_and_workspace_is_cleaned(self):
        # Run in a child with a deadline so a regression cannot hang the test suite.
        # This child is Python, not Codex; it only replaces temporary fixture files.
        script = '''
import os
from pathlib import Path
from evals.evaluation import read_result
from evals.smoke import evaluate

for kind in ("pipe", "directory", "symlink"):
    workspaces = []
    def invalid_output(prompt, workspace):
        workspaces.append(workspace)
        output = workspace / "message.txt"
        output.unlink()
        if kind == "pipe":
            os.mkfifo(output)
        elif kind == "directory":
            output.mkdir()
        else:
            output.symlink_to(workspace / "AGENTS.md")
        return read_result(workspace)
    report = evaluate(invalid_output)
    assert len(report.failures) == 1, kind
    assert not report.cases, kind
    assert not workspaces[0].exists(), kind
'''
        result = subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_snapshot_failure_preserves_primary_error_and_attempts_remaining_evidence(self):
        for blocked in ("workspace", "workspace/AGENTS.md"):
            with self.subTest(blocked=blocked), TemporaryDirectory() as directory:
                artifacts = Path(directory)
                if blocked == "workspace":
                    (artifacts / blocked).write_text("Not a directory")
                else:
                    (artifacts / blocked).mkdir(parents=True)
                # Fail before launching any CLI; then make a snapshot write fail too.
                with (
                    patch("evals.auth.codex_executable", side_effect=RuntimeError("primary failure")),
                    redirect_stderr(StringIO()),
                ):
                    report = evaluate(partial(
                        run_codex, model="test", effort="medium", timeout=1,
                        artifacts=artifacts, profile=artifacts / "unused-profile",
                    ))
                self.assertIn("primary failure", report.failures[0].error_message)
                self.assertIn("Evidence could not be fully saved", report.failures[0].error_message)
                metadata = json.loads((artifacts / "execution.json").read_text())
                self.assertEqual(metadata["error"], "primary failure")
                self.assertTrue(metadata["evidence_errors"])
                self.assertFalse(Path(metadata["workspace"]).exists())
                if blocked == "workspace/AGENTS.md":
                    self.assertEqual((artifacts / "workspace/message.txt").read_bytes(), b"before\n")

    def test_metadata_write_failure_retains_snapshots_and_reports_both_errors(self):
        with TemporaryDirectory() as directory, prepare_workspace(fixture_files={"message.txt": b"before\n"}) as workspace:
            artifacts = Path(directory)
            errors = StringIO()
            with (
                patch("evals.auth.codex_executable", side_effect=RuntimeError("primary failure")),
                patch("evals.codex.save_json", side_effect=PermissionError("metadata unavailable")),
                redirect_stderr(errors),
            ):
                result = run_codex(
                    "test", workspace, model="test", effort="medium", timeout=1,
                    artifacts=artifacts, profile=artifacts / "unused-profile",
                )
            self.assertEqual(result.status, "error")
            self.assertIn("primary failure", result.error)
            self.assertIn("metadata unavailable", result.error)
            self.assertIn(result.error, errors.getvalue())
            self.assertEqual((artifacts / "workspace/message.txt").read_bytes(), b"before\n")

    def test_evidence_failure_turns_completed_execution_into_an_error(self):
        with TemporaryDirectory() as directory, prepare_workspace(fixture_files={"message.txt": b"before\n"}) as workspace:
            artifacts = Path(directory)
            (artifacts / "workspace").write_text("Not a directory")
            with redirect_stderr(StringIO()):
                result = retain_evidence(workspace, artifacts, {}, ExecutionResult("completed", "after\n"))
            self.assertEqual(result.status, "error")
            metadata = json.loads((artifacts / "execution.json").read_text())
            self.assertEqual(metadata["status"], "error")
            self.assertEqual(metadata["execution_status"], "completed")
            self.assertIsNone(metadata["error"])
            self.assertTrue(metadata["evidence_errors"])

    def test_report_write_failures_return_two_and_attempt_both_formats(self):
        report = evaluate(write_after)
        original_write = Path.write_text
        for blocked in ({"report.txt"}, {"report.json"}, {"report.txt", "report.json"}):
            with self.subTest(blocked=blocked), TemporaryDirectory() as directory:
                root = Path(directory)
                output, errors = StringIO(), StringIO()
                def write(path, *args, **kwargs):
                    if path.name in blocked:
                        raise PermissionError(f"{path.name} unavailable")
                    return original_write(path, *args, **kwargs)
                with (
                    patch("evals.__main__.evaluate", return_value=report),
                    patch("evals.__main__.ARTIFACTS_ROOT", root),
                    patch.object(Path, "write_text", autospec=True, side_effect=write),
                    patch.object(sys, "argv", ["evals", "--model", "test", "--reasoning-effort", "medium"]),
                    redirect_stdout(output), redirect_stderr(errors),
                ):
                    self.assertEqual(main(), 2)
                self.assertIn("replace-message", output.getvalue())
                artifacts, = root.iterdir()
                for name in ("report.txt", "report.json"):
                    self.assertEqual((artifacts / name).exists(), name not in blocked)
                for name in blocked:
                    self.assertIn(f"{name} unavailable", errors.getvalue())
                if "report.json" not in blocked:
                    summary = json.loads((artifacts / "report.json").read_text())
                    self.assertEqual(summary["outcome"], "execution_failed")
                    self.assertTrue(summary["evidence_errors"])

    def test_fallback_report_failure_does_not_hide_original_error_or_escape(self):
        with TemporaryDirectory() as directory:
            errors = StringIO()
            with (
                patch("evals.__main__.ARTIFACTS_ROOT", Path(directory)),
                patch("evals.__main__.evaluate", side_effect=RuntimeError("primary failure")),
                patch("evals.__main__.save_json", side_effect=PermissionError("report unavailable")),
                patch.object(sys, "argv", ["evals", "--model", "test", "--reasoning-effort", "medium"]),
                redirect_stdout(StringIO()), redirect_stderr(errors),
            ):
                self.assertEqual(main(), 2)
            self.assertIn("primary failure", errors.getvalue())
            self.assertIn("report unavailable", errors.getvalue())


class ScopeEvidenceTests(unittest.TestCase):
    """Inject process replies and filesystem failures; no real CLI or credentials."""

    def setUp(self):
        self.artifacts = Path(self.enterContext(TemporaryDirectory()))
        self.workspace = self.enterContext(prepare_workspace(fixture_files={"message.txt": INITIAL_CONTENTS}))
        self.enterContext(patch("evals.auth.codex_executable", return_value="unused-codex"))
        self.enterContext(patch("evals.auth.check_profile"))
        self.enterContext(patch("evals.auth.codex_environment", return_value={}))
        self.enterContext(patch("evals.auth.require_chatgpt_login"))

        def execute(command, **kwargs):
            if "--version" in command:
                return subprocess.CompletedProcess(command, 0, stdout="test-cli")
            (self.workspace / "message.txt").write_bytes(b"greeting=after\nnote=teh sample\n")
            kwargs["stdout"].write('{"type": "turn.completed"}\n')
            return subprocess.CompletedProcess(command, 0)

        self.process = self.enterContext(patch("evals.codex.run_process", side_effect=execute))

    def run_observed(self):
        return run_codex("test", self.workspace, model="test", effort="medium", timeout=1,
                         artifacts=self.artifacts, profile=self.artifacts / "unused-profile",
                         observe_workspace=True)

    def test_initial_inspection_failure_prevents_execution_and_retains_final_observation(self):
        final = snapshot_workspace(self.workspace)
        with patch("evals.codex.snapshot_workspace", side_effect=[PermissionError("inspection denied"), final]):
            result = self.run_observed()

        self.assertEqual(result.status, "error")
        self.assertIn("inspection denied", result.error)
        self.process.assert_not_called()
        self.assertIsNone(result.workspace_observation.initial)
        self.assertFalse((self.artifacts / "initial-workspace.json").exists())
        self.assertTrue((self.artifacts / "final-workspace.json").is_file())
        self.assertTrue((self.artifacts / "execution.json").is_file())

    def test_final_inspection_failure_preserves_primary_error_and_initial_evidence(self):
        initial = snapshot_workspace(self.workspace)
        self.process.side_effect = RuntimeError("primary execution failure")
        with patch("evals.codex.snapshot_workspace", side_effect=[initial, PermissionError("inspection denied")]):
            result = self.run_observed()

        self.assertEqual(result.status, "error")
        self.assertIn("primary execution failure", result.error)
        self.assertIn("Final workspace inspection failed", result.error)
        self.assertIsNone(result.workspace_observation.final)
        self.assertTrue((self.artifacts / "initial-workspace.json").is_file())
        self.assertFalse((self.artifacts / "final-workspace.json").exists())
        self.assertFalse((self.artifacts / "workspace/message.txt").exists())

    def test_successful_execution_with_failed_inspection_is_an_error(self):
        initial = snapshot_workspace(self.workspace)
        with patch("evals.codex.snapshot_workspace", side_effect=[initial, PermissionError("inspection denied")]):
            result = self.run_observed()

        self.assertEqual(result.status, "error")
        self.assertIn("inspection denied", result.error)
        metadata = json.loads((self.artifacts / "execution.json").read_text())
        self.assertEqual(metadata["status"], "error")
        self.assertEqual(metadata["returncode"], 0)

    def test_each_manifest_write_is_independent_and_primary_error_survives(self):
        initial = snapshot_workspace(self.workspace)
        result = ExecutionResult("error", error="primary failure",
                                 workspace_observation=WorkspaceObservation(initial, initial))
        for blocked in ("initial", "final"):
            with self.subTest(blocked=blocked), TemporaryDirectory() as directory:
                artifacts = Path(directory)
                (artifacts / f"{blocked}-workspace.json").mkdir()
                with redirect_stderr(StringIO()):
                    retained = retain_evidence(self.workspace, artifacts, {}, result)
                self.assertEqual(retained.status, "error")
                self.assertIn("primary failure", retained.error)
                self.assertIn(f"{blocked}-workspace.json", retained.error)
                other = "final" if blocked == "initial" else "initial"
                self.assertTrue((artifacts / f"{other}-workspace.json").is_file())
                self.assertEqual((artifacts / "workspace/message.txt").read_bytes(), INITIAL_CONTENTS)
                metadata = json.loads((artifacts / "execution.json").read_text())
                self.assertEqual(metadata["error"], "primary failure")
                self.assertTrue(metadata["evidence_errors"])

    def test_final_fixture_copies_use_captured_bytes_without_reopening_paths(self):
        initial = snapshot_workspace(self.workspace)
        (self.workspace / "message.txt").write_bytes(b"greeting=after\nnote=teh sample\n")
        observation = WorkspaceObservation(initial, snapshot_workspace(self.workspace))
        result = read_result(self.workspace, workspace_observation=observation)
        # Later disk contents must not disagree with what the retained observation graded.
        (self.workspace / "message.txt").write_bytes(b"changed after observation")
        with patch("evals.codex.read_fixture_file", side_effect=AssertionError("Unexpected file read")):
            retained = retain_evidence(self.workspace, self.artifacts, {}, result)

        self.assertEqual(retained.status, "completed")
        self.assertEqual((self.artifacts / "workspace/message.txt").read_bytes(),
                         b"greeting=after\nnote=teh sample\n")


if __name__ == "__main__":
    unittest.main()
