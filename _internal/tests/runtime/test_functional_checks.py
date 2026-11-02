"""Shared orchestration and interpretation contracts without subprocesses."""

from dataclasses import replace
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Event
import unittest
from unittest.mock import call, patch

from evals.runtime import functional_checks
from evals.runtime.evaluation import ExecutionResult
from evals.runtime.functional import FunctionalCheckResult
from evals.runtime.workspace import WorkspaceEntry, WorkspaceObservation


class FunctionalChecksTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(TemporaryDirectory()))
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.artifacts = self.root / "evidence"
        self.artifacts.mkdir()
        snapshot = {"module.py": WorkspaceEntry("file", 0o644, b"pass\n")}
        self.result = ExecutionResult(
            "completed", file_contents="summary\r\n", final_response="Done.\n",
            workspace_observation=WorkspaceObservation(snapshot, snapshot),
        )

    def test_source_order_timeout_cancellation_and_exact_evidence_are_preserved(self):
        cancelled = Event()
        passing = FunctionalCheckResult("completed", 0, stdout=b"first\r\n\xff", launcher_stderr=b"launcher\x00")
        failing = FunctionalCheckResult("completed", 7, stderr=b"second\xfe")

        def run(source, workspace, **kwargs):
            if source == "# first\n":
                cancelled.set()
                return passing
            # Each earlier check and its evidence finish before the next call.
            self.assertTrue(kwargs["cancelled"].is_set())
            self.assertEqual((self.artifacts / "checks/Zulu.stdout").read_bytes(), b"first\r\n\xff")
            return failing

        with patch.object(functional_checks, "run_python_check", side_effect=run) as runner:
            checked = functional_checks.run_checks(
                self.result, self.workspace, sources={"Zulu": "# first\n", "Alpha": "# second π\n"},
                required_files={"Zulu": ("module.py",), "Alpha": ("module.py",)},
                timeout=1.25, artifacts=self.artifacts, cancelled=cancelled,
            )

        self.assertEqual(runner.call_args_list, [
            call("# first\n", self.workspace, timeout=1.25, cancelled=cancelled),
            call("# second π\n", self.workspace, timeout=1.25, cancelled=cancelled),
        ])
        self.assertEqual(checked, replace(self.result, functional_checks={"Zulu": passing, "Alpha": failing}))
        self.assertIsNone(self.result.functional_checks)
        records = json.loads((self.artifacts / "functional-checks.json").read_text())
        self.assertEqual(list(records), ["Zulu", "Alpha"])
        self.assertEqual(records, {
            "Zulu": {"timeout_seconds": 1.25, "status": "completed", "returncode": 0, "error": None},
            "Alpha": {"timeout_seconds": 1.25, "status": "completed", "returncode": 7, "error": None},
        })
        expected_files = {
            "Zulu.py": b"# first\n", "Zulu.stdout": b"first\r\n\xff", "Zulu.stderr": b"",
            "Zulu.launcher-stderr": b"launcher\x00", "Alpha.py": "# second π\n".encode("utf-8"),
            "Alpha.stdout": b"", "Alpha.stderr": b"second\xfe", "Alpha.launcher-stderr": b"",
        }
        self.assertEqual({path.name: path.read_bytes() for path in (self.artifacts / "checks").iterdir()},
                         expected_files)

    def test_check_and_write_errors_accumulate_without_stopping_independent_writes(self):
        write_bytes = Path.write_bytes

        def deny_first_files(path, contents):
            if path.name in ("First.py", "First.stdout"):
                raise PermissionError("cannot save " + path.name)
            return write_bytes(path, contents)

        first = FunctionalCheckResult("error", error="first failure", stderr=b"partial\xff")
        second = FunctionalCheckResult("error", error="second failure", launcher_stderr=b"diagnostic")
        with (patch.object(functional_checks, "run_python_check", side_effect=[first, second]),
              patch.object(Path, "write_bytes", autospec=True, side_effect=deny_first_files),
              patch.object(functional_checks, "save_json", side_effect=ValueError("cannot encode summary")) as save):
            checked = functional_checks.run_checks(
                self.result, self.workspace, sources={"First": "pass", "Second": "pass"},
                required_files={"First": ("module.py",), "Second": ("module.py",)},
                timeout=5, artifacts=self.artifacts,
            )

        self.assertEqual(checked.status, "error")
        self.assertEqual(checked.error, "First: first failure\nchecks/First.py: cannot save First.py\n"
                         "checks/First.stdout: cannot save First.stdout\nSecond: second failure\n"
                         "functional-checks.json: cannot encode summary")
        self.assertEqual(checked.functional_checks, {"First": first, "Second": second})
        self.assertEqual((self.artifacts / "checks/First.stderr").read_bytes(), b"partial\xff")
        self.assertEqual((self.artifacts / "checks/Second.py").read_bytes(), b"pass")
        self.assertEqual((self.artifacts / "checks/Second.launcher-stderr").read_bytes(), b"diagnostic")
        save.assert_called_once_with(self.artifacts / "functional-checks.json", {
            "First": {"timeout_seconds": 5, "status": "error", "returncode": None, "error": "first failure"},
            "Second": {"timeout_seconds": 5, "status": "error", "returncode": None, "error": "second failure"},
        })

    def test_inspection_failure_keeps_primary_error_and_existing_agent_failure_skip_reason(self):
        primary = "Final workspace inspection failed: denied"
        result = replace(self.result, status="error", error=primary,
                         workspace_observation=WorkspaceObservation(self.result.workspace_observation.initial, None))
        write_bytes = Path.write_bytes

        def deny_first_source(path, contents):
            if path.name == "First.py":
                raise PermissionError("cannot save source")
            return write_bytes(path, contents)

        with (patch.object(functional_checks, "run_python_check") as runner,
              patch.object(Path, "write_bytes", autospec=True, side_effect=deny_first_source)):
            checked = functional_checks.run_checks(
                result, self.workspace, sources={"First": "pass", "Second": "pass"},
                required_files={"First": ("module.py",), "Second": ("module.py",)},
                timeout=5, artifacts=self.artifacts,
            )

        runner.assert_not_called()
        self.assertEqual(checked.status, "error")
        self.assertEqual(checked.error, primary + "\nchecks/First.py: cannot save source")
        self.assertEqual(checked.functional_checks, {})
        self.assertEqual((self.artifacts / "checks/Second.py").read_bytes(), b"pass")
        self.assertEqual(json.loads((self.artifacts / "functional-checks.json").read_text()), {
            "First": {"timeout_seconds": 5, "status": "not_run", "reason": "Agent execution failed"},
            "Second": {"timeout_seconds": 5, "status": "not_run", "reason": "Agent execution failed"},
        })

    def test_completed_checks_keep_exact_success_and_nonzero_assertion_reasons(self):
        for returncode, expected, reason in (
            (0, True, "Example: check passed; see checks/Example.stdout and .stderr"),
            (7, False, "Example: check exited 7; diagnostic\r\n\\xff"),
        ):
            with self.subTest(returncode=returncode):
                result = replace(self.result, functional_checks={
                    "Example": FunctionalCheckResult("completed", returncode, stderr=b"diagnostic\r\n\xff"),
                })
                assertion = functional_checks.check_assertion(result, "Example", required_files=("module.py",))
                self.assertEqual(assertion.value, expected)
                self.assertEqual(assertion.reason, reason)

    def test_missing_and_invalid_results_keep_exact_infrastructure_error_reasons(self):
        for checks, message in (
            (None, "Example: functional-check observation is required"),
            ({}, "Example: functional-check observation is required"),
            ({"Other": FunctionalCheckResult("completed", 0)}, "Example: functional-check observation is required"),
            ({"Example": FunctionalCheckResult("completed")}, "Example: functional check did not complete"),
            ({"Example": FunctionalCheckResult("error")}, "Example: functional check did not complete"),
            ({"Example": FunctionalCheckResult("error", error="capture failed")}, "Example: capture failed"),
        ):
            with self.subTest(checks=checks):
                with self.assertRaises(RuntimeError) as raised:
                    functional_checks.check_assertion(replace(self.result, functional_checks=checks), "Example",
                                                      required_files=("module.py",))
                self.assertEqual(str(raised.exception), message)


if __name__ == "__main__":
    unittest.main()
