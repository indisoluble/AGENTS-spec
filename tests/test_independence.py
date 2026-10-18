"""Offline regression checks: local test-authored edits, replies, and fake CLI.

No real Codex, credentials, or model calls. The fake sandbox does not enforce
OS isolation; tests here establish grading and retained evidence, not policy.
"""

from contextlib import redirect_stdout
from dataclasses import replace
from io import StringIO
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evals import __main__ as cli
from evals import independence as case
from evals.functional import FunctionalCheckResult
from evals.smoke import ExecutionResult, evaluate, prepare_workspace
from evals.workspace import WorkspaceObservation, snapshot_workspace


ADDED_TEST = '''

class UTCRegressionTests(unittest.TestCase):
    def test_timestamp_keeps_its_time_and_gets_utc_marker(self):
        self.assertIn("2026-01-15T09:00:00Z", export_events([
            {"id": "one", "occurred_at": "2026-01-15T09:00:00"}]))
'''


def correct_edit(workspace):
    path = workspace / "exporter.py"
    path.write_bytes(path.read_bytes().replace(b'event["occurred_at"]', b'event["occurred_at"] + "Z"'))
    path = workspace / "test_exporter.py"
    path.write_text(path.read_text() + ADDED_TEST)


class IndependenceTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.executable = self.root / "codex"
        self.executable.write_text(f"#!{sys.executable}\n" + Path(__file__).with_name("fake_codex.py").read_text())
        self.executable.chmod(0o700)
        self.artifacts = self.root / "evidence"
        self.artifacts.mkdir()

    def run_substitute(self, edit=correct_edit, response="Updated and tested."):
        workspaces = []

        def execute(prompt, workspace):
            self.assertEqual(prompt, case.PROMPT)
            workspaces.append(workspace)
            initial = snapshot_workspace(workspace)
            if edit:
                edit(workspace)
            result = ExecutionResult("completed", final_response=response,
                                     workspace_observation=WorkspaceObservation(initial, snapshot_workspace(workspace)))
            with patch("evals.functional.codex_executable", return_value=str(self.executable)):
                return case.check_execution(result, workspace, artifacts=self.artifacts)

        report = evaluate(execute, dataset=case.independence_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertTrue(workspaces)
        self.assertTrue(all(not path.exists() for path in workspaces))
        with redirect_stdout(StringIO()):
            code = cli.write_report(report, self.artifacts, case_name="independent-execution")
        saved = json.loads((self.artifacts / "report.json").read_text())
        return code, saved

    def test_correct_edit_has_four_assertions_and_retained_check_sources_and_outputs(self):
        code, saved = self.run_substitute()
        self.assertEqual(code, 3)
        self.assertEqual(saved["outcome"], "review_required")
        self.assertTrue(saved["review_required"])
        self.assertEqual(saved["cases"][0]["assertions"], {
            "RequestedChange": True, "RegressionTests": True,
            "EditBoundaryPreserved": True, "FinalResponsePresent": True,
        })
        checks = json.loads((self.artifacts / "functional-checks.json").read_text())
        for name, source in case.CHECK_SOURCES.items():
            self.assertEqual(checks[name]["status"], "completed")
            self.assertEqual(checks[name]["returncode"], 0)
            self.assertEqual(checks[name]["timeout_seconds"], 5)
            self.assertEqual((self.artifacts / "checks" / f"{name}.py").read_text(), source)
        self.assertIn("Function and command checks passed", (self.artifacts / "checks/RequestedChange.stdout").read_text())
        self.assertIn("Ran 2 tests", (self.artifacts / "checks/RegressionTests.stderr").read_text())

    def test_original_fixture_fails_request_and_test_update_but_preserves_boundary(self):
        code, saved = self.run_substitute(edit=None)
        self.assertEqual(code, 1)
        self.assertEqual(saved["cases"][0]["assertions"], {
            "RequestedChange": False, "RegressionTests": False,
            "EditBoundaryPreserved": True, "FinalResponsePresent": True,
        })
        self.assertIn("unchanged", saved["cases"][0]["assertion_reasons"]["RegressionTests"])

    def test_incorrect_time_fields_order_and_input_mutation_fail_fixed_checks(self):
        replacements = (
            ('event["occurred_at"] + "Z"', 'event["occurred_at"] + "+00:00"'),
            ('event["occurred_at"] + "Z"', '"2026-01-15T09:00:00Z"'),
            ('event["id"]', '"changed"'),
            ('for event in events', 'for event in reversed(events)'),
            ('    return json.dumps', '    events.clear()\n    return json.dumps'),
        )
        for before, after in replacements:
            with self.subTest(after=after):
                def edit(workspace):
                    correct_edit(workspace)
                    path = workspace / "exporter.py"
                    path.write_text(path.read_text().replace(before, after))
                code, saved = self.run_substitute(edit)
                self.assertEqual(code, 1)
                self.assertFalse(saved["cases"][0]["assertions"]["RequestedChange"])
                self.assertTrue(saved["cases"][0]["assertions"]["EditBoundaryPreserved"])

    def test_no_new_tests_failing_tests_and_zero_discovered_tests_fail_separately(self):
        for tests in (case.FIXTURE_FILES["test_exporter.py"],
                      b"raise AssertionError('broken tests')\n", b"# No tests\n"):
            with self.subTest(tests=tests):
                def edit(workspace):
                    correct_edit(workspace)
                    (workspace / "test_exporter.py").write_bytes(tests)
                code, saved = self.run_substitute(edit)
                self.assertEqual(code, 1)
                assertions = saved["cases"][0]["assertions"]
                self.assertTrue(assertions["RequestedChange"])
                self.assertFalse(assertions["RegressionTests"])
                self.assertTrue(assertions["EditBoundaryPreserved"])

    def test_questions_claims_and_superficial_tests_do_not_get_semantic_verdicts(self):
        # Deliberately misleading examples stay pending: no keyword classifier or
        # claim that a passing process proves meaningful agent-written tests.
        for response in ("May I use concatenation?", "Done; no tests needed.", "Implemented and tested."):
            with self.subTest(response=response):
                def edit(workspace):
                    correct_edit(workspace)
                    (workspace / "test_exporter.py").write_bytes(case.FIXTURE_FILES["test_exporter.py"] + b"\n# Changed\n")
                    with (workspace / "exporter.py").open("a") as output:
                        output.write("\n# Unrelated redesign proposal\n")
                code, saved = self.run_substitute(edit, response)
                self.assertEqual(code, 3)
                self.assertTrue(all(saved["cases"][0]["assertions"].values()))
                self.assertTrue(saved["review_required"])

    def test_empty_response_fails_but_missing_capture_is_an_error(self):
        for response, expected in ((" \n", 1), (None, 2)):
            with self.subTest(response=response):
                code, saved = self.run_substitute(response=response)
                self.assertEqual(code, expected)
                self.assertTrue(saved["review_required"])
                self.assertTrue(saved["cases"][0]["assertions"]["RequestedChange"])

    def test_boundary_includes_contract_other_paths_and_editable_file_permissions(self):
        def edit(workspace):
            correct_edit(workspace)
            (workspace / "AGENTS.md").write_text("changed")
            (workspace / ".hidden").write_bytes(b"\xff")
            (workspace / "empty").mkdir()
            (workspace / "exporter.py").chmod(0o700)
        code, saved = self.run_substitute(edit)
        self.assertEqual(code, 1)
        assertions = saved["cases"][0]["assertions"]
        self.assertTrue(assertions["RequestedChange"])
        self.assertTrue(assertions["RegressionTests"])
        self.assertFalse(assertions["EditBoundaryPreserved"])
        reason = saved["cases"][0]["assertion_reasons"]["EditBoundaryPreserved"]
        self.assertEqual([line.partition(":")[0] for line in reason.splitlines()],
                         [".hidden", "AGENTS.md", "empty", "exporter.py"])

    def test_missing_link_directory_and_fifo_are_not_executed(self):
        for kind in ("missing", "symlink", "directory", "fifo"):
            with self.subTest(kind=kind):
                def edit(workspace):
                    correct_edit(workspace)
                    target = workspace / "exporter.py"
                    target.unlink()
                    if kind == "symlink":
                        target.symlink_to(self.root / "do-not-read")
                    elif kind == "directory":
                        target.mkdir()
                    elif kind == "fifo":
                        os.mkfifo(target)
                with patch.object(case, "run_python_check") as run:
                    code, saved = self.run_substitute(edit)
                run.assert_not_called()
                self.assertEqual(code, 1)
                assertions = saved["cases"][0]["assertions"]
                self.assertFalse(assertions["RequestedChange"])
                self.assertFalse(assertions["RegressionTests"])
                self.assertFalse(assertions["EditBoundaryPreserved"])
                records = json.loads((self.artifacts / "functional-checks.json").read_text())
                self.assertTrue(all(record["status"] == "not_run" for record in records.values()))

    def test_check_errors_keep_output_and_remain_infrastructure_errors(self):
        for message in ("Sandbox launcher failed", "Functional check timed out", "Evaluation interrupted"):
            with self.subTest(message=message), patch.object(case, "run_python_check", return_value=
                    FunctionalCheckResult("error", stdout=b"partial\xff", error=message)):
                code, saved = self.run_substitute()
                self.assertEqual(code, 2)
                self.assertEqual(saved["cases"], [])
                self.assertIn(message, saved["execution_errors"][0])
                self.assertEqual((self.artifacts / "checks/RequestedChange.stdout").read_bytes(), b"partial\xff")

    def test_deleted_test_file_skips_only_test_execution(self):
        def edit(workspace):
            correct_edit(workspace)
            (workspace / "test_exporter.py").unlink()
        code, saved = self.run_substitute(edit)
        self.assertEqual(code, 1)
        self.assertEqual(saved["cases"][0]["assertions"], {
            "RequestedChange": True, "RegressionTests": False,
            "EditBoundaryPreserved": False, "FinalResponsePresent": True,
        })
        records = json.loads((self.artifacts / "functional-checks.json").read_text())
        self.assertEqual(records["RequestedChange"]["status"], "completed")
        self.assertEqual(records["RegressionTests"]["status"], "not_run")

    def test_evidence_failure_preserves_check_error_and_attempts_other_files(self):
        write_bytes = Path.write_bytes
        def deny_stdout(path, contents):
            if path.name == "RequestedChange.stdout":
                raise PermissionError("cannot save stdout")
            return write_bytes(path, contents)
        with (patch.object(case, "run_python_check", return_value=
                           FunctionalCheckResult("error", stderr=b"diagnostic", error="primary check failure")),
              patch.object(Path, "write_bytes", autospec=True, side_effect=deny_stdout)):
            code, saved = self.run_substitute()
        self.assertEqual(code, 2)
        self.assertIn("primary check failure", saved["execution_errors"][0])
        self.assertIn("cannot save stdout", saved["execution_errors"][0])
        self.assertEqual((self.artifacts / "checks/RequestedChange.stderr").read_bytes(), b"diagnostic")
        self.assertTrue((self.artifacts / "functional-checks.json").exists())

    def test_agent_failure_skips_checks_and_preserves_primary_error(self):
        with prepare_workspace(fixture_files=case.FIXTURE_FILES) as workspace:
            with patch.object(case, "run_python_check") as run:
                result = case.check_execution(ExecutionResult("error", error="agent failed"), workspace,
                                              artifacts=self.artifacts)
        run.assert_not_called()
        self.assertEqual(result.status, "error")
        self.assertEqual(result.error, "agent failed")
        records = json.loads((self.artifacts / "functional-checks.json").read_text())
        self.assertTrue(all(record["reason"] == "Agent execution failed" for record in records.values()))

    def test_missing_observation_or_check_result_is_never_a_pass(self):
        with prepare_workspace(fixture_files=case.FIXTURE_FILES) as workspace:
            snapshot = snapshot_workspace(workspace)
        output = ExecutionResult("completed", final_response="Done", workspace_observation=
                                 WorkspaceObservation(snapshot, snapshot))
        for result in (output, replace(output, workspace_observation=None)):
            report = evaluate(lambda prompt, workspace: result, dataset=case.independence_dataset(),
                              fixture_files=case.FIXTURE_FILES)
            with redirect_stdout(StringIO()):
                code = cli.write_report(report, self.artifacts, case_name="independent-execution")
            self.assertEqual(code, 2)
            self.assertTrue(report.cases[0].evaluator_failures)


if __name__ == "__main__":
    unittest.main()
