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

from evaluations import __main__ as cli
from evaluations.runtime import functional_checks
from evaluations.runtime.evaluation import ExecutionResult, evaluate
from evaluations.runtime.functional import FunctionalCheckResult
from evaluations.runtime.workspace import WorkspaceObservation, prepare_workspace, snapshot_workspace
from evaluations.scenarios import guidance
from evaluations.scenarios import independence
from evaluations.scenarios import independence as case
from evaluations.tests.support.cli_harness import FakeCodexCLI


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
        self.executable.write_text(f"#!{sys.executable}\n" + (Path(__file__).resolve().parents[1] / "support" / "fake_codex.py").read_text())
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
            with patch("evaluations.runtime.functional.codex_executable", return_value=str(self.executable)):
                return case.check_execution(result, workspace, artifacts=self.artifacts)

        report = evaluate(execute, dataset=case.independence_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertTrue(workspaces)
        self.assertTrue(all(not path.exists() for path in workspaces))
        with redirect_stdout(StringIO()):
            code = cli.write_report(report, self.artifacts, case_name="independent-execution", review_required=True)
        saved = json.loads((self.artifacts / "report.json").read_text())
        return code, saved

    def test_fixture_shares_only_the_exporter_and_sample_data_with_requester_guidance(self):
        self.assertEqual(list(case.FIXTURE_FILES), ["exporter.py", "events.json", "README.md", "test_exporter.py"])
        for path in ("exporter.py", "events.json"):
            self.assertEqual(case.FIXTURE_FILES[path], guidance.FIXTURE_FILES[path])
        self.assertNotEqual(case.FIXTURE_FILES["README.md"], guidance.FIXTURE_FILES["README.md"])
        self.assertIn(b"already represent UTC", case.FIXTURE_FILES["README.md"])

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
                with patch.object(functional_checks, "run_python_check") as run:
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
            with self.subTest(message=message), patch.object(functional_checks, "run_python_check", return_value=
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
        with (patch.object(functional_checks, "run_python_check", return_value=
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
            with patch.object(functional_checks, "run_python_check") as run:
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
                code = cli.write_report(report, self.artifacts, case_name="independent-execution", review_required=True)
            self.assertEqual(code, 2)
            self.assertTrue(report.cases[0].evaluator_failures)

    def fixture_result(self):
        with prepare_workspace(fixture_files=case.FIXTURE_FILES) as workspace:
            snapshot = snapshot_workspace(workspace)
        return ExecutionResult("completed", final_response="Done",
                               workspace_observation=WorkspaceObservation(snapshot, snapshot),
                               functional_checks={name: FunctionalCheckResult("completed", 0)
                                                  for name in case.CHECK_SOURCES})

    @staticmethod
    def uncaptured(snapshot, path):
        return {**snapshot, path: replace(snapshot[path], contents=None)}

    def check_observation(self, observation):
        self.artifacts = Path(self.enterContext(TemporaryDirectory(dir=self.root, prefix="evidence-")))
        with prepare_workspace(fixture_files=case.FIXTURE_FILES) as workspace:
            checked = case.check_execution(
                ExecutionResult("completed", final_response="Done", workspace_observation=observation),
                workspace, artifacts=self.artifacts)
        return checked, json.loads((self.artifacts / "functional-checks.json").read_text())

    def grade(self, result):
        report = evaluate(lambda prompt, workspace: result, dataset=case.independence_dataset(),
                          fixture_files=case.FIXTURE_FILES)
        with redirect_stdout(StringIO()):
            code = cli.write_report(report, self.artifacts, case_name="independent-execution", review_required=True)
        return code, json.loads((self.artifacts / "report.json").read_text()), report

    def test_incomplete_observations_skip_checks_as_infrastructure_errors(self):
        snapshot = self.fixture_result().workspace_observation.initial
        incomplete = "Complete initial and final workspace observations are required"
        for state, observation, reason in (
            ("absent", None, incomplete),
            ("missing initial", WorkspaceObservation(None, snapshot), incomplete),
            ("missing final", WorkspaceObservation(snapshot, None), incomplete),
            ("uncaptured final exporter.py", WorkspaceObservation(snapshot, self.uncaptured(snapshot, "exporter.py")),
             "exporter.py: file contents were not observed"),
        ):
            with self.subTest(state=state):
                with patch.object(functional_checks, "run_python_check") as run:
                    checked, records = self.check_observation(observation)
                run.assert_not_called()
                self.assertEqual(checked.status, "error")
                self.assertEqual(checked.functional_checks, {})
                for name, source in case.CHECK_SOURCES.items():
                    self.assertEqual(records[name], {"timeout_seconds": 5, "status": "not_run", "reason": reason})
                    self.assertEqual((self.artifacts / "checks" / f"{name}.py").read_text(), source)
                    self.assertFalse((self.artifacts / "checks" / f"{name}.stdout").exists())
                code, saved, _ = self.grade(checked)
                self.assertEqual(code, 2)
                self.assertEqual(saved["outcome"], "execution_failed")
                self.assertEqual(saved["cases"], [])
                self.assertIn(reason, saved["execution_errors"][0])

    def test_uncaptured_test_file_skips_only_the_regression_check(self):
        snapshot = self.fixture_result().workspace_observation.initial
        reason = "test_exporter.py: file contents were not observed"
        with patch.object(functional_checks, "run_python_check", return_value=FunctionalCheckResult("completed", 0)) as run:
            checked, records = self.check_observation(
                WorkspaceObservation(snapshot, self.uncaptured(snapshot, "test_exporter.py")))
        self.assertEqual([call.args[0] for call in run.call_args_list], [case.REQUESTED_CHANGE_CHECK])
        self.assertEqual(records["RequestedChange"]["status"], "completed")
        self.assertEqual(records["RegressionTests"], {"timeout_seconds": 5, "status": "not_run", "reason": reason})
        self.assertEqual(checked.status, "error")
        code, saved, _ = self.grade(checked)
        self.assertEqual(code, 2)
        self.assertEqual(saved["cases"], [])
        self.assertIn(reason, saved["execution_errors"][0])

    def test_observed_missing_file_fails_assertions_but_uncaptured_file_is_an_error(self):
        snapshot = self.fixture_result().workspace_observation.initial
        missing = {path: entry for path, entry in snapshot.items() if path != "exporter.py"}
        for state, final, reason in (
            ("missing", missing, "exporter.py: missing or not a regular file"),
            ("uncaptured", self.uncaptured(snapshot, "exporter.py"), "exporter.py: file contents were not observed"),
        ):
            with self.subTest(state=state):
                with patch.object(functional_checks, "run_python_check") as run:
                    checked, records = self.check_observation(WorkspaceObservation(snapshot, final))
                run.assert_not_called()
                self.assertTrue(all(record["reason"] == reason for record in records.values()))
                code, saved, _ = self.grade(checked)
                if state == "missing":
                    self.assertEqual(code, 1)
                    self.assertEqual(checked.status, "completed")
                    self.assertEqual(saved["execution_errors"], [])
                    self.assertEqual(saved["cases"][0]["evaluator_errors"], [])
                    self.assertEqual(saved["cases"][0]["assertions"], {
                        "RequestedChange": False, "RegressionTests": False,
                        "EditBoundaryPreserved": False, "FinalResponsePresent": True,
                    })
                else:
                    self.assertEqual(code, 2)
                    self.assertEqual(checked.status, "error")
                    self.assertEqual(saved["cases"], [])

    def test_regression_verdict_is_never_derived_from_incomplete_observations(self):
        result = self.fixture_result()
        snapshot = result.workspace_observation.initial
        uncaptured = self.uncaptured(snapshot, "test_exporter.py")
        initial_error = "Initial test_exporter.py must be an observed regular file"
        incomplete = "Complete initial and final workspace observations are required"
        for state, observation, returncode, message in (
            ("uncaptured initial, passing check", WorkspaceObservation(uncaptured, snapshot), 0, initial_error),
            ("uncaptured initial, failing check", WorkspaceObservation(uncaptured, snapshot), 1, initial_error),
            ("uncaptured final", WorkspaceObservation(snapshot, uncaptured), 0,
             "test_exporter.py: file contents were not observed"),
            ("missing initial", WorkspaceObservation(None, snapshot), 0, incomplete),
            ("missing final", WorkspaceObservation(snapshot, None), 0, incomplete),
        ):
            with self.subTest(state=state):
                checks = {**result.functional_checks, "RegressionTests": FunctionalCheckResult("completed", returncode)}
                code, _, report = self.grade(replace(result, workspace_observation=observation, functional_checks=checks))
                self.assertEqual(code, 2)
                graded, = report.cases
                # Require RegressionTests' own error; EditBoundaryPreserved can also fail on these inputs.
                self.assertNotIn("RegressionTests", graded.assertions)
                failure, = [failure for failure in graded.evaluator_failures if failure.name == "RegressionTests"]
                self.assertIn(message, failure.error_message)
                if None not in (observation.initial, observation.final):
                    self.assertTrue(graded.assertions["RequestedChange"].value)


class IndependenceCLITests(FakeCodexCLI, unittest.TestCase):
    def test_independent_execution_selection_retains_checks_and_pending_review(self):
        scenarios = (("success", 3), ("question", 3), ("internal-unrelated", 3),
                     ("no-tests", 1), ("broken-tests", 1), ("unrelated", 1), ("empty", 1),
                     ("missing-response", 2), ("nonzero", 2))
        for scenario, expected_exit in scenarios:
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="independent-execution")
                artifacts, metadata, report = self.finish(process, runs, expected_exit)
                self.assertEqual(report["case"], "independent-execution")
                self.assertTrue(report["review_required"])
                self.assertEqual((profile / "invocations").read_text(), "exec\n")
                self.assertEqual((artifacts / "review.md").read_text(), independence.REVIEW_RUBRIC)
                self.assertEqual((artifacts / "prompt.txt").read_text(), independence.PROMPT)
                for name, contents in independence.FIXTURE_FILES.items():
                    self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
                records = json.loads((artifacts / "functional-checks.json").read_text())
                if expected_exit == 2:
                    self.assertEqual(report["cases"], [])
                    self.assertTrue(all(record["status"] == "not_run" for record in records.values()))
                else:
                    assertions = report["cases"][0]["assertions"]
                    self.assertTrue(assertions["RequestedChange"])
                    self.assertEqual(assertions["RegressionTests"], scenario not in ("no-tests", "broken-tests"))
                    self.assertEqual(assertions["EditBoundaryPreserved"], scenario != "unrelated")
                    self.assertEqual(assertions["FinalResponsePresent"], scenario != "empty")
                    self.assertEqual(report["cases"][0]["final_response"], (artifacts / "final-response.txt").read_text())
                    self.assertEqual(records["RequestedChange"]["returncode"], 0)
                    self.assertTrue((artifacts / "checks/RequestedChange.stdout").is_file())
                    self.assertEqual(metadata["status"], "completed")
                final = json.loads((artifacts / "final-workspace.json").read_text())
                self.assertNotIn("checks", final)
                self.assertNotIn("review.md", final)
                changes = (artifacts / "workspace-changes.txt").read_text()
                if scenario == "nonzero":
                    self.assertEqual(changes, "No observed workspace changes.\n")
                else:
                    self.assertIn('Path: "exporter.py"', changes)


if __name__ == "__main__":
    unittest.main()
