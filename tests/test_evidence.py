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
from evals.smoke import ExecutionResult, evaluate, prepare_workspace
from tests.offline_smoke import write_after


class EvidenceTests(unittest.TestCase):
    def test_nonregular_output_is_rejected_without_blocking_and_workspace_is_cleaned(self):
        # Run in a child with a deadline so a regression cannot hang the test suite.
        # This child is Python, not Codex; it only replaces temporary fixture files.
        script = '''
import os
from pathlib import Path
from evals.smoke import evaluate, read_result

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
        with TemporaryDirectory() as directory, prepare_workspace() as workspace:
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
        with TemporaryDirectory() as directory, prepare_workspace() as workspace:
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


if __name__ == "__main__":
    unittest.main()
