"""Exercise Candidate selection through the integrated command without an agent."""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from engine.runtime.evaluation import ExecutionResult
from engine.runtime.functional import FunctionalCheckResult
from engine.runtime.workspace import WorkspaceObservation, snapshot_workspace
from evaluation import __main__ as cli


class CandidateBindingTests(unittest.TestCase):
    def setUp(self):
        root = Path(self.enterContext(TemporaryDirectory()))
        self.contract = root / "selected.md"
        self.runs = root / "runs"
        self.enterContext(patch.object(cli, "CANDIDATE_PATH", self.contract))
        self.enterContext(patch.object(cli, "ARTIFACTS_ROOT", self.runs))
        self.enterContext(redirect_stdout(StringIO()))
        self.enterContext(redirect_stderr(StringIO()))

    def invoke(self, *args):
        with patch.object(sys, "argv", ["evaluation", *args]):
            return cli.main()

    def test_argument_and_auth_operations_do_not_read_the_contract(self):
        with patch.object(Path, "read_bytes", side_effect=AssertionError("unexpected read")):
            for args, status in ((["--help"], 0), (["--case", "unknown"], 2)):
                with self.subTest(args=args), self.assertRaises(SystemExit) as stopped:
                    self.invoke(*args)
                self.assertEqual(stopped.exception.code, status)
            for action in ("login", "logout"):
                with patch.object(cli.auth, action, return_value=0):
                    self.assertEqual(self.invoke("--" + action), 0)
        self.assertFalse(self.runs.exists())

    def test_unreadable_candidate_is_a_task_failure_with_review_retained(self):
        with patch.object(cli, "run_codex") as launch:
            self.assertEqual(self.invoke("--case", "durable-finding-review", "--model", "test",
                                         "--reasoning-effort", "medium"), 2)
        launch.assert_not_called()
        artifacts, = self.runs.iterdir()
        report = json.loads((artifacts / "report.json").read_text())
        self.assertEqual(report["case"], "durable-finding-review")
        self.assertEqual(report["outcome"], "execution_failed")
        self.assertTrue(report["review_required"])
        self.assertEqual(report["cases"], [])
        self.assertIn(str(self.contract), report["execution_errors"][0])
        self.assertTrue((artifacts / "review.md").is_file())
        self.assertTrue((artifacts / "report.txt").is_file())

    def test_suite_keeps_first_contract_for_setup_and_independent_grading(self):
        original = b"# Selected contract\r\n"
        self.contract.write_bytes(original)
        received = []

        def inspect(prompt, workspace, **settings):
            received.append((workspace / "AGENTS.md").read_bytes())
            self.contract.write_bytes(b"changed source\n")
            observed = snapshot_workspace(workspace)
            return ExecutionResult("completed", file_contents="after\n", final_response="reply",
                                   workspace_observation=WorkspaceObservation(observed, dict(observed)))

        # Only exercise contract injection and assessment. The existing fake CLI
        # tests cover actual command capture, hashing, cleanup, and sandbox checks.
        with (patch.object(cli, "run_codex", side_effect=inspect),
              patch("engine.runtime.functional_checks.run_python_check",
                    return_value=FunctionalCheckResult("completed", 0))):
            self.invoke("--case", "all", "--model", "test", "--reasoning-effort", "medium")
        self.assertEqual(received, [original] * 10)
        reports = [json.loads(p.read_text()) for p in self.runs.glob("*/report.json")]
        findings, = [report for report in reports if report["case"] == "durable-finding-review"]
        self.assertEqual(findings["outcome"], "review_required")
        self.assertTrue(findings["cases"][0]["assertions"]["ProtectedStatePreserved"])

