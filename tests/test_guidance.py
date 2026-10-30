"""Test evidence and automated checks with local substitutes, never real Codex.

Responses below illustrate different meanings, but tests deliberately do not
assign human-rubric verdicts. Nonempty text alone must never become a full pass.
"""

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evals import __main__ as cli
from evals.evaluation import ExecutionResult, evaluate
from evals.guidance import FIXTURE_FILES, PROMPT, REVIEW_RUBRIC, guidance_dataset
from evals.workspace import (
    CONTRACT_PATH, WorkspaceEntry, WorkspaceObservation, prepare_workspace, snapshot_workspace, workspace_changes,
)


class GuidanceTests(unittest.TestCase):
    def run_substitute(self, response="Which source timezone should these timestamps use?", edit=None):
        workspaces = []

        def execute(prompt, workspace):
            self.assertEqual(prompt, PROMPT)
            workspaces.append(workspace)
            initial = snapshot_workspace(workspace)
            if edit is not None:
                edit(workspace)
            return ExecutionResult("completed", final_response=response,
                                   workspace_observation=WorkspaceObservation(initial, snapshot_workspace(workspace)))

        report = evaluate(execute, dataset=guidance_dataset(), fixture_files=FIXTURE_FILES)
        self.assertTrue(all(not path.exists() for path in workspaces))
        return report

    def render_report(self, report):
        with TemporaryDirectory() as directory, redirect_stdout(StringIO()) as terminal:
            artifacts = Path(directory)
            code = cli.write_report(report, artifacts, case_name="requester-guidance", review_required=True)
            saved = json.loads((artifacts / "report.json").read_text())
            self.assertEqual(terminal.getvalue(), (artifacts / "report.txt").read_text())
            return code, saved, terminal.getvalue()

    def test_good_misleading_and_irrelevant_replies_all_require_human_review(self):
        replies = (
            "The source timezone is unknown. Guessing could shift event times. "
            "Which timezone should I use? I have deferred conversion.",
            "Which source timezone? I assumed UTC and accepted that policy already.",
            "Done.",
        )
        for reply in replies:
            with self.subTest(reply=reply):
                code, saved, terminal = self.render_report(self.run_substitute(reply))
                self.assertEqual(code, 3)
                self.assertEqual(saved["outcome"], "review_required")
                self.assertTrue(saved["review_required"])
                self.assertEqual(saved["cases"][0]["final_response"], reply)
                self.assertEqual(saved["cases"][0]["assertions"], {
                    "FinalResponsePresent": True, "RootContractPreserved": True,
                })
                self.assertEqual(len(saved["cases"][0]["assertion_reasons"]), 2)
                self.assertIn("Human review pending", terminal)

    def test_empty_and_whitespace_responses_fail_presence_without_failing_contract(self):
        for reply in ("", " \n\t"):
            with self.subTest(reply=reply):
                code, saved, _ = self.render_report(self.run_substitute(reply))
                self.assertEqual(code, 1)
                self.assertEqual(saved["outcome"], "assertion_failed")
                self.assertTrue(saved["review_required"])
                self.assertEqual(saved["cases"][0]["assertions"], {
                    "FinalResponsePresent": False, "RootContractPreserved": True,
                })

    def test_contract_changes_fail_independently_of_response_presence(self):
        def alter_contract(workspace, kind):
            contract = workspace / "AGENTS.md"
            if kind == "contents":
                contract.write_bytes(b"altered contract")
            elif kind == "permissions":
                contract.chmod(contract.stat().st_mode ^ 0o100)
            else:
                contract.unlink()
                if kind == "symlink":
                    contract.symlink_to(workspace / "events.json")
                elif kind == "directory":
                    contract.mkdir()

        for kind in ("contents", "permissions", "deleted", "symlink", "directory"):
            with self.subTest(kind=kind):
                report = self.run_substitute(edit=lambda workspace: alter_contract(workspace, kind))
                code, saved, _ = self.render_report(report)
                self.assertEqual(code, 1)
                self.assertEqual(saved["cases"][0]["assertions"], {
                    "FinalResponsePresent": True, "RootContractPreserved": False,
                })
                self.assertIn("AGENTS.md:", saved["cases"][0]["assertion_reasons"]["RootContractPreserved"])

    def test_missing_capture_or_observation_is_an_evaluator_error(self):
        original = self.run_substitute().cases[0].output
        invalid = (
            replace(original, final_response=None),
            replace(original, workspace_observation=None),
            replace(original, workspace_observation=WorkspaceObservation(None, {})),
            replace(original, workspace_observation=WorkspaceObservation({}, None)),
            replace(original, workspace_observation=WorkspaceObservation({}, {})),
        )
        for output in invalid:
            with self.subTest(output=output):
                report = evaluate(lambda prompt, workspace: output,
                                  dataset=guidance_dataset(), fixture_files=FIXTURE_FILES)
                code, saved, _ = self.render_report(report)
                self.assertEqual(code, 2)
                self.assertEqual(saved["outcome"], "execution_failed")
                self.assertTrue(saved["cases"][0]["evaluator_errors"])
                self.assertTrue(saved["review_required"])

    def test_fixture_is_fresh_and_its_existing_exporter_runs(self):
        paths = []
        for _ in range(2):
            with prepare_workspace(fixture_files=FIXTURE_FILES) as workspace:
                paths.append(workspace)
                self.assertEqual(set(path.name for path in workspace.iterdir()), {*FIXTURE_FILES, "AGENTS.md"})
                for name, contents in FIXTURE_FILES.items():
                    self.assertEqual((workspace / name).read_bytes(), contents)
                self.assertEqual((workspace / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())
                # Run only the tiny fixture exporter, not a coding agent.
                result = subprocess.run([sys.executable, "exporter.py"], cwd=workspace,
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), json.loads(FIXTURE_FILES["events.json"]))
                (workspace / "events.json").write_bytes(b"changed")
        self.assertEqual(len(set(paths)), 2)
        self.assertTrue(all(not path.exists() for path in paths))

    def test_notes_code_data_and_policy_edits_remain_observations_for_review(self):
        edits = {
            "timezone-note.md": b"Unresolved timezone; proposal: ask the requester.\n",
            "exporter.py": b"# Unsupported assumption: input is UTC.\n",
            "events.json": b'[{"occurred_at": "2026-01-15T09:00:00Z"}]\n',
            "README.md": b"Accepted timezone policy: UTC.\n",
        }
        for path, contents in edits.items():
            with self.subTest(path=path):
                report = self.run_substitute(edit=lambda workspace: (workspace / path).write_bytes(contents))
                code, _, _ = self.render_report(report)
                self.assertEqual(code, 3)
                observation = report.cases[0].output.workspace_observation
                self.assertEqual(observation.final[path].contents, contents)
                changes = workspace_changes(observation)
                self.assertIn(f'Path: "{path}"', changes)
                self.assertNotIn("No observed workspace changes", changes)

    def test_aggregate_exit_codes_prioritize_errors_then_failures_then_review(self):
        scenarios = (
            ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 0), ((0, 0, 3, 3, 3, 3, 3, 3, 3, 3), 3), ((3, 1, 0, 3, 3, 3, 3, 3, 3, 3), 1),
            ((1, 0, 3, 0, 3, 3, 3, 3, 3, 3), 1), ((3, 0, 2, 3, 3, 3, 3, 3, 3, 3), 2), ((2, 1, 3, 0, 3, 3, 3, 3, 3, 3), 2),
            ((0, 0, 0, 1, 3, 3, 3, 3, 3, 3), 1), ((0, 0, 3, 2, 3, 3, 3, 3, 3, 3), 2), ((0, 0, 0, 0, 3, 3, 3, 3, 3, 3), 3),
            ((0, 0, 3, 3, 1, 3, 3, 3, 3, 3), 1), ((0, 0, 3, 3, 2, 3, 3, 3, 3, 3), 2), ((0, 0, 0, 0, 0, 3, 3, 3, 3, 3), 3),
            ((0, 0, 3, 3, 3, 1, 3, 3, 3, 3), 1), ((0, 0, 3, 3, 3, 2, 3, 3, 3, 3), 2), ((0, 0, 0, 0, 0, 0, 3, 3, 3, 3), 3),
            ((0, 0, 3, 3, 3, 3, 1, 3, 3, 3), 1), ((0, 0, 3, 3, 3, 3, 2, 3, 3, 3), 2), ((0, 0, 0, 0, 0, 0, 0, 3, 3, 3), 3),
            ((0, 0, 3, 3, 3, 3, 3, 1, 3, 3), 1), ((0, 1, 3, 3, 3, 3, 3, 2, 3, 3), 2), ((0, 0, 0, 0, 0, 0, 0, 0, 3, 3), 3),
            ((0, 0, 3, 3, 3, 3, 3, 3, 1, 3), 1), ((0, 1, 3, 3, 3, 3, 3, 3, 2, 3), 2),
            ((0, 0, 0, 0, 0, 0, 0, 0, 0, 3), 3), ((0, 0, 3, 3, 3, 3, 3, 3, 3, 1), 1),
            ((0, 1, 3, 3, 3, 3, 3, 3, 3, 2), 2),
        )
        for codes, expected in scenarios:
            with self.subTest(codes=codes), patch.object(cli, "run_case", side_effect=codes) as run:
                with patch.object(sys, "argv", ["evals", "--case", "all", "--model", "test", "--reasoning-effort", "medium"]):
                    self.assertEqual(cli.main(), expected)
                self.assertEqual([call.args[0].name for call in run.call_args_list],
                                 ["smoke", "scope-discipline", "requester-guidance", "independent-execution",
                                  "assumption-disclosure", "missing-permission", "no-safe-next-step",
                                  "contract-change-followthrough", "bounded-inquiry", "durable-finding-review"])

    def test_review_rubric_write_failure_is_a_setup_error_without_launching(self):
        with TemporaryDirectory() as directory:
            original_write = Path.write_text

            def deny_rubric(path, *args, **kwargs):
                if path.name == "review.md":
                    raise PermissionError("rubric unavailable")
                return original_write(path, *args, **kwargs)

            with (patch.object(cli, "ARTIFACTS_ROOT", Path(directory)),
                  patch.object(cli, "run_codex") as execute,
                  patch.object(Path, "write_text", autospec=True, side_effect=deny_rubric),
                  patch.object(sys, "argv", ["evals", "--case", "requester-guidance", "--model", "test",
                                             "--reasoning-effort", "medium", "--timeout", "1", "--codex-home", directory]),
                  redirect_stdout(StringIO()), redirect_stderr(StringIO())):
                code = cli.main()
            self.assertEqual(code, 2)
            execute.assert_not_called()
            artifacts, = Path(directory).iterdir()
            saved = json.loads((artifacts / "report.json").read_text())
            self.assertIn("rubric unavailable", saved["error"])
            self.assertTrue(saved["review_required"])

    def test_change_report_write_failure_preserves_primary_error_and_other_evidence(self):
        with TemporaryDirectory() as directory:
            original_write = Path.write_text

            def deny_changes(path, *args, **kwargs):
                if path.name == "workspace-changes.txt":
                    raise PermissionError("changes unavailable")
                return original_write(path, *args, **kwargs)

            with (patch.object(cli, "ARTIFACTS_ROOT", Path(directory)),
                  patch("evals.auth.codex_executable", side_effect=RuntimeError("primary failure")),
                  patch.object(Path, "write_text", autospec=True, side_effect=deny_changes),
                  patch.object(sys, "argv", ["evals", "--case", "requester-guidance", "--model", "test",
                                             "--reasoning-effort", "medium", "--timeout", "1", "--codex-home", directory]),
                  redirect_stdout(StringIO()), redirect_stderr(StringIO())):
                code = cli.main()
            self.assertEqual(code, 2)
            artifacts, = Path(directory).iterdir()
            saved = json.loads((artifacts / "report.json").read_text())
            error = saved["execution_errors"][0]
            self.assertIn("primary failure", error)
            self.assertIn("changes unavailable", error)
            self.assertEqual((artifacts / "review.md").read_text(), REVIEW_RUBRIC)
            for phase in ("initial", "final"):
                self.assertTrue((artifacts / f"{phase}-workspace.json").is_file())


class WorkspaceChangeReportTests(unittest.TestCase):
    def test_changes_include_types_modes_links_exact_text_and_binary_contents_in_path_order(self):
        initial = {
            ".": WorkspaceEntry("directory", 0o700),
            "binary": WorkspaceEntry("file", 0o600, b"\xff"),
            "deleted": WorkspaceEntry("file", 0o600, b"removed\n"),
            "link": WorkspaceEntry("symlink", 0o777, link_target="old"),
            "text": WorkspaceEntry("file", 0o644, b"same\r\nlast"),
            "type": WorkspaceEntry("directory", 0o700),
        }
        final = {
            ".": WorkspaceEntry("directory", 0o755),
            ".hidden": WorkspaceEntry("file", 0o600, b"added\n"),
            "binary": WorkspaceEntry("file", 0o600, b"\x00\xfe"),
            "empty": WorkspaceEntry("directory", 0o700),
            "link": WorkspaceEntry("symlink", 0o777, link_target="new\nname"),
            "nested": WorkspaceEntry("directory", 0o700),
            "nested/pipe": WorkspaceEntry("fifo", 0o600),
            "text": WorkspaceEntry("file", 0o755, b"same\nlast\n"),
            "type": WorkspaceEntry("file", 0o600, b"new file\n"),
        }
        rendered = workspace_changes(WorkspaceObservation(initial, final))
        paths = [json.loads(line.removeprefix("Path: ")) for line in rendered.splitlines() if line.startswith("Path: ")]
        self.assertEqual(paths, sorted(initial.keys() | final.keys()))
        for expected in ('mode=0700', 'mode=0755', 'mode=0644', 'After: absent', 'Before: absent',
                         'target="old"', 'target="new\\nname"', 'fifo, mode=0600',
                         '-"same\\r\\n"', '+"same\\n"', '-"last"', '+"last\\n"',
                         '-base64: /w==', '+base64: AP4=', '-"removed\\n"', '+"added\\n"'):
            self.assertIn(expected, rendered)

    def test_unchanged_and_incomplete_observations_are_distinct(self):
        self.assertEqual(workspace_changes(WorkspaceObservation({}, {})), "No observed workspace changes.\n")
        for observation in (WorkspaceObservation(None, {}), WorkspaceObservation({}, None)):
            self.assertIn("comparison unavailable", workspace_changes(observation))
            self.assertNotIn("No observed", workspace_changes(observation))


if __name__ == "__main__":
    unittest.main()
