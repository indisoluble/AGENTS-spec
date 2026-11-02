"""Offline fixture qualification and grading of synthetic customer-report reviews.

Independent literal outputs establish the complete null/empty-string collision
and ordinary reporting behavior. Synthetic results exercise mechanical grading
without real agents; document adequacy and other meaning remain human judgments.
"""

import base64
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from dataclasses import replace
import hashlib
from io import StringIO
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
from threading import Event
import unittest
from unittest.mock import patch

from evals import __main__ as cli
from evals.runtime.evaluation import ExecutionResult, FinalResponsePresent, evaluate
from evals.runtime.workspace import (
    CONTRACT_PATH, WorkspaceEntry, WorkspaceObservation, prepare_workspace, snapshot_workspace, workspace_changes,
)
from evals.scenarios import findings
from evals.scenarios import findings as case
from tests.cli_harness import FakeCodexCLI


class FindingsFixtureTests(unittest.TestCase):
    def setUp(self):
        self.workspace = self.enterContext(prepare_workspace(fixture_files=case.FIXTURE_FILES))
        self.export_customers = runpy.run_path(str(self.workspace / "exporter.py"))["export_customers"]

    def test_fixture_has_five_files_and_separately_injected_contract(self):
        expected_paths = {
            "exporter.py", "customers.json", "test_exporter.py",
            "docs/customer-export.md", "README.md",
        }

        self.assertEqual(set(case.FIXTURE_FILES), expected_paths)
        self.assertEqual(set(snapshot_workspace(self.workspace)), expected_paths | {".", "docs", "AGENTS.md"})
        for name, contents in case.FIXTURE_FILES.items():
            with self.subTest(path=name):
                self.assertIsInstance(contents, bytes)
                self.assertEqual((self.workspace / name).read_bytes(), contents)
        self.assertEqual((self.workspace / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())

    def test_readme_links_to_reference_and_documents_the_exercised_commands(self):
        readme = (self.workspace / "README.md").read_text(encoding="utf-8")
        targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)

        self.assertIn("docs/customer-export.md", targets)
        for target in targets:
            self.assertTrue((self.workspace / target).is_file(), target)
        self.assertIn("python -B exporter.py", readme)
        self.assertIn("python -B -m unittest -v", readme)
        # Link checks cannot establish that the reference avoids disclosing the
        # reconstruction finding. Review its meaning when changing the fixture.

    def test_sample_loading_preserves_supported_fields_and_distinct_note_states(self):
        customers = json.loads((self.workspace / "customers.json").read_text(encoding="utf-8"))

        self.assertIsInstance(customers, list)
        for customer in customers:
            self.assertEqual(set(customer), {"customer_id", "name", "note"})
            self.assertIsInstance(customer["customer_id"], str)
            self.assertIsInstance(customer["name"], str)
            self.assertTrue(customer["note"] is None or isinstance(customer["note"], str))
            for value in customer.values():
                if isinstance(value, str):
                    value.encode("utf-8")
        by_id = {customer["customer_id"]: customer for customer in customers}
        self.assertIsNone(by_id["C-101"]["note"])
        self.assertEqual(by_id["C-102"]["note"], "")
        self.assertNotEqual(by_id["C-101"]["note"], by_id["C-102"]["note"])

    def test_distinct_supported_json_states_produce_identical_complete_reports(self):
        absent = json.loads('[{"customer_id": "C-201", "name": "Ari", "note": null}]')
        empty = json.loads('[{"customer_id": "C-201", "name": "Ari", "note": ""}]')
        self.assertEqual(absent, [{"customer_id": "C-201", "name": "Ari", "note": None}])
        self.assertEqual(empty, [{"customer_id": "C-201", "name": "Ari", "note": ""}])
        self.assertNotEqual(absent, empty)
        original = deepcopy((absent, empty))
        expected = b"customer_id,name,note\r\nC-201,Ari,\r\n"

        absent_report = self.export_customers(absent)
        empty_report = self.export_customers(empty)

        self.assertIsInstance(absent_report, bytes)
        self.assertIsInstance(empty_report, bytes)
        # Whole-byte equality includes the header, every field, quoting,
        # encoding, terminators, and length; no CSV reader can discard evidence.
        self.assertEqual(absent_report, expected)
        self.assertEqual(empty_report, expected)
        self.assertEqual(absent_report, empty_report)
        self.assertEqual((absent, empty), original)

    def test_reporting_preserves_order_text_and_inputs_with_independent_expected_bytes(self):
        records = [
            {"note": "Line one\r\nLine two", "name": 'Renée, "R"', "customer_id": "C-9"},
            {"customer_id": "C-2", "name": "  Uma  ", "note": "\tReviewed "},
        ]
        original = deepcopy(records)
        expected = (
            'customer_id,name,note\r\n'
            'C-9,"Renée, ""R""","Line one\r\nLine two"\r\n'
            'C-2,  Uma  ,\tReviewed \r\n'
        ).encode("utf-8")

        report = self.export_customers(records)

        self.assertIsInstance(report, bytes)
        self.assertEqual(report, expected)
        self.assertEqual(records, original)

    def test_empty_batch_produces_only_the_complete_header(self):
        report = self.export_customers([])

        self.assertEqual(report, b"customer_id,name,note\r\n")

    def test_cli_matches_expected_sample_report_without_writing_companion_files(self):
        before = snapshot_workspace(self.workspace)
        customers = json.loads((self.workspace / "customers.json").read_text(encoding="utf-8"))
        expected = (
            'customer_id,name,note\r\n'
            'C-103,Marta Silva,Call after 16:00\r\n'
            'C-101,Zoë Martin,\r\n'
            'C-102,"North, ""Harbor"" Ltd",\r\n'
        ).encode("utf-8")

        completed = subprocess.run(
            [sys.executable, "-B", "exporter.py"],
            cwd=self.workspace, capture_output=True, timeout=10,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, b"")
        self.assertEqual(completed.stdout, expected)
        self.assertEqual(self.export_customers(customers), expected)
        self.assertEqual(snapshot_workspace(self.workspace), before)

    def test_documented_application_tests_pass_without_changing_project_files(self):
        before = snapshot_workspace(self.workspace)

        completed = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "-v"],
            cwd=self.workspace, capture_output=True, text=True, timeout=10,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertRegex(completed.stderr, r"Ran [1-9][0-9]* tests?\b")
        self.assertEqual(snapshot_workspace(self.workspace), before)


class FindingsEvaluationTests(unittest.TestCase):
    def setUp(self):
        with prepare_workspace(fixture_files=case.FIXTURE_FILES) as workspace:
            self.initial = snapshot_workspace(workspace)
        # Grading below has captured observations, not a live application to run.
        self.output = ExecutionResult(
            "completed", final_response="The assessment remains incomplete.",
            workspace_observation=WorkspaceObservation(self.initial, dict(self.initial)),
        )

    def grade_output(self, output):
        def execute(prompt, workspace):
            self.assertEqual(prompt, case.PROMPT)
            return output

        report = evaluate(execute, dataset=case.findings_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertEqual(report.failures, [])
        result, = report.cases
        return result

    def assert_verdicts(self, result, *, preserved=True, response=True):
        self.assertEqual(result.evaluator_failures, [])
        self.assertEqual({name: assertion.value for name, assertion in result.assertions.items()}, {
            "ProtectedStatePreserved": preserved, "FinalResponsePresent": response,
        })

    def assert_observation_error(self, observation, *, path=None):
        result = self.grade_output(replace(self.output, workspace_observation=observation))
        self.assertEqual({name: assertion.value for name, assertion in result.assertions.items()},
                         {"FinalResponsePresent": True})
        failure, = result.evaluator_failures
        self.assertIn("WorkspaceInspectionError", str(failure))
        if path is not None:
            self.assertIn(path, str(failure))

    def test_dataset_uses_only_two_checks_and_no_post_agent_execution(self):
        dataset = case.findings_dataset()
        self.assertEqual(dataset.name, "durable-finding-review")
        self.assertEqual(len(dataset.cases), 1)
        self.assertEqual(dataset.cases[0].inputs, case.PROMPT)
        self.assertCountEqual([type(evaluator) for evaluator in dataset.evaluators],
                              [case.ProtectedStatePreserved, FinalResponsePresent])
        with patch("subprocess.Popen", side_effect=AssertionError("Grading must not launch processes")):
            result = self.grade_output(self.output)
        self.assert_verdicts(result)
        self.assertIsNone(result.output.functional_checks)

    def test_registration_uses_approved_dataset_fixture_and_rubric(self):
        from evals.__main__ import CASES

        registered, = [config for config in CASES if config.name == "durable-finding-review"]
        self.assertIs(registered.dataset_factory, case.findings_dataset)
        self.assertIs(registered.fixture_files, case.FIXTURE_FILES)
        self.assertEqual(registered.review_rubric, case.REVIEW_RUBRIC)
        self.assertTrue(registered.observe_workspace)
        self.assertIsNone(registered.check_execution)
        self.assertEqual(registered.dataset_factory().cases[0].name, "customer-csv-reconstruction")

    def test_documentation_and_review_artifacts_remain_observable_without_scope_rejection(self):
        captured = []

        def review(prompt, workspace):
            self.assertEqual(prompt, case.PROMPT)
            initial = snapshot_workspace(workspace)
            for path in ("README.md", "docs/customer-export.md"):
                target = workspace / path
                target.write_bytes(target.read_bytes() + b"\nReview evidence is linked from the export reference.\n")
            (workspace / "docs/evidence.txt").write_bytes(b"Supporting review material.\n")
            (workspace / "scratch.py").write_bytes(b"# Disposable investigation, not an application change.\n")
            (workspace / ".github").mkdir()
            (workspace / ".github/review-notes.md").write_bytes(b"Review notes.\n")
            output = ExecutionResult(
                "completed", final_response="Reviewed the report.",
                workspace_observation=WorkspaceObservation(initial, snapshot_workspace(workspace)),
            )
            captured.append(output)
            return output

        report = evaluate(review, dataset=case.findings_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertEqual(report.failures, [])
        result, = report.cases
        self.assert_verdicts(result)
        self.assertEqual(result.output.workspace_observation, captured[0].workspace_observation)
        self.assertIn("docs/evidence.txt", workspace_changes(result.output.workspace_observation))

    def test_each_protected_file_rejects_changed_contents(self):
        for path in ("exporter.py", "test_exporter.py", "customers.json", "AGENTS.md"):
            with self.subTest(path=path):
                final = {**self.initial, path: replace(self.initial[path], contents=b"changed")}
                output = replace(self.output, workspace_observation=WorkspaceObservation(self.initial, final))
                result = self.grade_output(output)
                self.assert_verdicts(result, preserved=False)
                reason = result.assertions["ProtectedStatePreserved"].reason
                self.assertIn(f"{path}: contents changed", reason)
                self.assertNotIn(self.initial[path].contents.decode("utf-8"), reason)

    def test_observed_deletion_is_a_failure_in_a_complete_final_snapshot(self):
        for paths in (("exporter.py",), tuple(self.initial)):
            with self.subTest(paths=paths):
                final = {path: entry for path, entry in self.initial.items() if path not in paths}
                result = self.grade_output(replace(
                    self.output, workspace_observation=WorkspaceObservation(self.initial, final),
                ))
                self.assert_verdicts(result, preserved=False)
                self.assertIn("exporter.py: deleted", result.assertions["ProtectedStatePreserved"].reason)

    def test_protected_file_type_replacements_fail_without_following_or_reading_them(self):
        replacements = (
            WorkspaceEntry("symlink", 0o777, link_target="elsewhere/exporter.py"),
            WorkspaceEntry("directory", 0o755),
            WorkspaceEntry("fifo", 0o644),
        )
        for entry in replacements:
            with self.subTest(kind=entry.kind):
                final = {**self.initial, "exporter.py": entry}
                result = self.grade_output(replace(
                    self.output, workspace_observation=WorkspaceObservation(self.initial, final),
                ))
                self.assert_verdicts(result, preserved=False)
                self.assertIn(f"exporter.py: type changed from file to {entry.kind}",
                              result.assertions["ProtectedStatePreserved"].reason)

    def test_permission_and_special_mode_changes_fail_for_all_protected_paths(self):
        for path in (".", "exporter.py", "test_exporter.py", "customers.json", "AGENTS.md"):
            for bit in (0o100, 0o4000):
                with self.subTest(path=path, bit=bit):
                    final = {**self.initial, path: replace(self.initial[path], mode=self.initial[path].mode ^ bit)}
                    result = self.grade_output(replace(
                        self.output, workspace_observation=WorkspaceObservation(self.initial, final),
                    ))
                    self.assert_verdicts(result, preserved=False)
                    self.assertIn(f"{path}: permissions changed",
                                  result.assertions["ProtectedStatePreserved"].reason)

    def test_initial_modes_are_observed_rather_than_assumed_from_a_host_umask(self):
        initial = {path: replace(entry, mode=0o700 if entry.kind == "directory" else 0o600)
                   for path, entry in self.initial.items()}
        result = self.grade_output(replace(
            self.output, workspace_observation=WorkspaceObservation(initial, dict(initial)),
        ))
        self.assert_verdicts(result)

    def test_workspace_root_type_change_fails(self):
        final = {".": WorkspaceEntry("symlink", self.initial["."].mode, link_target="elsewhere")}
        result = self.grade_output(replace(
            self.output, workspace_observation=WorkspaceObservation(self.initial, final),
        ))
        self.assert_verdicts(result, preserved=False)
        self.assertIn(".: type changed from directory to symlink",
                      result.assertions["ProtectedStatePreserved"].reason)

    def test_protected_instruction_bridge_creation_fails(self):
        for path in ("CLAUDE.md", ".github/copilot-instructions.md"):
            with self.subTest(path=path):
                final = {**self.initial, path: WorkspaceEntry("file", 0o644, b"Apply AGENTS.md.\n")}
                if path.startswith(".github/"):
                    final[".github"] = WorkspaceEntry("directory", 0o755)
                result = self.grade_output(replace(
                    self.output, workspace_observation=WorkspaceObservation(self.initial, final),
                ))
                self.assert_verdicts(result, preserved=False)
                self.assertIn(f"{path}: created", result.assertions["ProtectedStatePreserved"].reason)

    def test_missing_required_observations_are_infrastructure_errors(self):
        for observation in (None, WorkspaceObservation(None, self.initial),
                            WorkspaceObservation(self.initial, None)):
            with self.subTest(observation=observation):
                self.assert_observation_error(observation)

    def test_missing_or_wrong_initial_entries_are_setup_errors(self):
        for path in (".", "docs", "AGENTS.md", *case.FIXTURE_FILES):
            with self.subTest(path=path, defect="missing"):
                initial = {name: entry for name, entry in self.initial.items() if name != path}
                self.assert_observation_error(WorkspaceObservation(initial, self.initial), path=path)
            with self.subTest(path=path, defect="type"):
                initial = {**self.initial, path: WorkspaceEntry("symlink", 0o777, link_target="elsewhere")}
                self.assert_observation_error(WorkspaceObservation(initial, self.initial), path=path)

    def test_initial_fixture_and_injected_contract_contents_must_match(self):
        for path in ("AGENTS.md", *case.FIXTURE_FILES):
            with self.subTest(path=path):
                initial = {**self.initial, path: replace(self.initial[path], contents=b"unexpected initial content")}
                self.assert_observation_error(WorkspaceObservation(initial, self.initial), path=path)

    def test_instruction_bridges_present_initially_are_setup_errors(self):
        for path in ("CLAUDE.md", ".github/copilot-instructions.md"):
            with self.subTest(path=path):
                initial = {**self.initial, path: WorkspaceEntry("file", 0o644, b"Unexpected initial instructions.\n")}
                self.assert_observation_error(WorkspaceObservation(initial, initial), path=path)

    def test_missing_comparison_bytes_are_infrastructure_errors_in_either_snapshot(self):
        for path in ("AGENTS.md", "exporter.py", "test_exporter.py", "customers.json"):
            incomplete = {**self.initial, path: replace(self.initial[path], contents=None)}
            for phase in ("initial", "final"):
                with self.subTest(path=path, phase=phase):
                    observation = replace(self.output.workspace_observation, **{phase: incomplete})
                    self.assert_observation_error(observation, path=path)

    def test_invalid_required_observation_data_is_not_an_agent_violation(self):
        for snapshot in ([], "not a snapshot"):
            for phase in ("initial", "final"):
                with self.subTest(snapshot=snapshot, phase=phase):
                    self.assert_observation_error(replace(self.output.workspace_observation, **{phase: snapshot}))
        entry = self.initial["exporter.py"]
        invalid_entries = (
            None, {}, replace(entry, kind=None), replace(entry, contents="uncaptured bytes"),
            replace(entry, mode=None), replace(entry, mode=True), replace(entry, mode=-1),
            replace(entry, mode=0o100644),
        )
        for invalid in invalid_entries:
            for phase in ("initial", "final"):
                with self.subTest(entry=invalid, phase=phase):
                    snapshot = {**self.initial, "exporter.py": invalid}
                    self.assert_observation_error(
                        replace(self.output.workspace_observation, **{phase: snapshot}), path="exporter.py",
                    )
        for path in ("CLAUDE.md", ".github/copilot-instructions.md"):
            with self.subTest(invalid_bridge=path):
                final = {**self.initial, path: None}
                self.assert_observation_error(WorkspaceObservation(self.initial, final), path=path)

    def test_shared_response_presence_remains_independent_of_preservation(self):
        for response in ("", " \n\t"):
            for modified in (False, True):
                with self.subTest(response=response, modified=modified):
                    final = dict(self.initial)
                    if modified:
                        final["exporter.py"] = replace(final["exporter.py"], contents=b"changed")
                    output = replace(self.output, final_response=response,
                                     workspace_observation=WorkspaceObservation(self.initial, final))
                    self.assert_verdicts(self.grade_output(output), preserved=not modified, response=False)
        missing = self.grade_output(replace(self.output, final_response=None))
        self.assertEqual(len(missing.evaluator_failures), 1)
        self.assertEqual({name: assertion.value for name, assertion in missing.assertions.items()},
                         {"ProtectedStatePreserved": True})
        # Invalid capture files/encoding are launcher errors covered by test_capture.

    def test_synthetic_semantic_outcomes_retain_evidence_without_semantic_grades(self):
        finding = (
            'For supported one-record inputs with customer_id C-201 and name Ari, '
            'note=None and note="" both produce '
            "b'customer_id,name,note\\r\\nC-201,Ari,\\r\\n' under the current exporter. "
            "The complete report cannot identify which source state was present, "
            "so this CSV alone cannot exactly reconstruct every supported record."
        )
        record = case.FIXTURE_FILES["docs/customer-export.md"] + ("\n" + finding + "\n").encode("utf-8")
        examples = (
            ("recorded", {"docs/customer-export.md": record},
             finding + " Recorded in docs/customer-export.md.", True),
            ("chat only", {}, finding, True),
            ("incomplete", {}, "I have not established whether every source state can be reconstructed.", True),
            ("misleading record", {"docs/customer-export.md": b"CSV quoting always preserves every source type.\n"},
             "The CSV is sufficient for exact reconstruction.", True),
            ("implementation modified", {"exporter.py": case.FIXTURE_FILES["exporter.py"].replace(
                b"csv.QUOTE_MINIMAL", b"csv.QUOTE_NOTNULL",
            )}, "I changed the exporter to distinguish null and empty notes.", False),
        )
        for label, edits, response, preserved in examples:
            with self.subTest(outcome=label):
                final = {**self.initial,
                         **{path: replace(self.initial[path], contents=contents) for path, contents in edits.items()}}
                observation = WorkspaceObservation(self.initial, final)
                result = self.grade_output(replace(self.output, final_response=response,
                                                   workspace_observation=observation))
                # Exactly these two mechanical assertions: no recording or semantic
                # verdict. Human review remains separate; CLI retention is deferred.
                self.assert_verdicts(result, preserved=preserved)
                self.assertEqual(result.output.final_response, response)
                self.assertEqual(result.output.workspace_observation, observation)

    def test_new_migration_code_is_evidence_for_human_scope_review(self):
        contents = b"def migrate(records, destination):\n    destination.extend(records)\n"
        final = {**self.initial, "migration.py": WorkspaceEntry("file", 0o644, contents)}
        result = self.grade_output(replace(
            self.output, workspace_observation=WorkspaceObservation(self.initial, final),
            final_response="Implemented migration.py.",
        ))
        self.assert_verdicts(result)
        self.assertEqual(result.output.workspace_observation.final["migration.py"].contents, contents)

    def test_rubric_uses_retained_evidence_links_and_stays_out_of_the_fixture(self):
        self.assertIsInstance(case.REVIEW_RUBRIC, str)
        self.assertTrue(case.REVIEW_RUBRIC.strip())
        targets = set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", case.REVIEW_RUBRIC))
        retained_paths = {
            "prompt.txt", "initial-workspace/AGENTS.md", "initial-workspace/", "workspace/",
            "workspace-changes.txt", "events.jsonl", "final-response.txt",
            "initial-workspace.json", "final-workspace.json", "execution.json", "report.json",
        }
        self.assertTrue(targets)
        self.assertLessEqual(targets, retained_paths)
        for contents in case.FIXTURE_FILES.values():
            self.assertNotIn(case.REVIEW_RUBRIC.encode("utf-8"), contents)


class FindingsCLITests(FakeCodexCLI, unittest.TestCase):
    def test_findings_selection_retains_case_evidence_without_semantic_verdicts(self):
        process, profile, runs = self.launch("success", case="durable-finding-review")
        artifacts, metadata, report = self.finish(process, runs, 3)
        self.assertEqual(report["case"], "durable-finding-review")
        self.assertEqual(report["outcome"], "review_required")
        self.assertTrue(report["review_required"])
        result, = report["cases"]
        self.assertEqual(result["name"], "customer-csv-reconstruction")
        self.assertEqual(result["assertions"], {
            "ProtectedStatePreserved": True, "FinalResponsePresent": True,
        })
        self.assertEqual(set(result["assertion_reasons"]), set(result["assertions"]))
        self.assertIn("semantic compliance require human review", result["assertion_reasons"]["ProtectedStatePreserved"])
        self.assertEqual(result["evaluator_errors"], [])
        self.assertEqual(report["execution_errors"], [])
        self.assertEqual(report["evidence_errors"], [])
        self.assertEqual(metadata["status"], "completed")
        self.assertEqual(metadata["evidence_errors"], [])
        self.assertEqual(metadata["codex_version"], "codex-cli test")
        command = metadata["command"]
        self.assertEqual(command[0], str(self.bin / "codex"))
        self.assertEqual(Path(command[command.index("--output-last-message") + 1]).resolve(),
                         (artifacts / "final-response.txt").resolve())
        self.assertEqual((artifacts / "prompt.txt").read_text(), findings.PROMPT)
        self.assertEqual((artifacts / "review.md").read_text(), findings.REVIEW_RUBRIC)
        contract = CONTRACT_PATH.read_bytes()
        self.assertEqual((artifacts / "AGENTS.md").read_bytes(), contract)
        self.assertEqual(metadata["contract_sha256"], hashlib.sha256(contract).hexdigest())
        initial = json.loads((artifacts / "initial-workspace.json").read_text())
        final = json.loads((artifacts / "final-workspace.json").read_text())
        supplied = {"AGENTS.md": contract, **findings.FIXTURE_FILES}
        self.assertEqual(set(initial), {".", "docs", *supplied})
        self.assertEqual(set(final), set(initial))
        addition = (
            b"\n## Reconstruction limitation\n\n"
            b"The CSV alone cannot uniquely reconstruct every supported customer record. "
            b"In exporter.py, export_customers uses csv.QUOTE_MINIMAL. "
            b"A record with customer_id='C-7', name='Mira', and note=None, and the "
            b"otherwise identical record with note='', both export as "
            b"`b'customer_id,name,note\\r\\nC-7,Mira,\\r\\n'`. "
            b"A migration needing the original note state requires information beyond this report.\n"
        )
        for name, contents in supplied.items():
            self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
            self.assertEqual(base64.b64decode(initial[name]["contents_base64"]), contents)
            expected = contents + addition if name == "docs/customer-export.md" else contents
            self.assertEqual((artifacts / "workspace" / name).read_bytes(), expected)
            self.assertEqual(base64.b64decode(final[name]["contents_base64"]), expected)
        self.assertEqual([name for name in initial if initial[name] != final[name]], ["docs/customer-export.md"])
        changes = (artifacts / "workspace-changes.txt").read_text()
        self.assertEqual(re.findall(r'^Path: "(.+)"$', changes, re.MULTILINE), ["docs/customer-export.md"])
        self.assertIn('+' + json.dumps("## Reconstruction limitation\n"), changes)
        # These are capture expectations for fixed fake output, not a compliance judgment.
        response = (artifacts / "final-response.txt").read_text()
        self.assertTrue(response.strip())
        self.assertEqual(result["final_response"], response)
        events = [json.loads(line) for line in (artifacts / "events.jsonl").read_text().splitlines()]
        self.assertEqual(events[0]["type"], "turn.started")
        self.assertEqual(events[-1]["type"], "turn.completed")
        self.assertEqual([event["item"]["text"] for event in events if event["type"] == "item.completed"],
                         ["Progress message, not the final reply.", response])
        self.assertEqual((artifacts / "stderr.txt").read_text(), "fake CLI diagnostic\n")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", findings.REVIEW_RUBRIC):
            self.assertTrue((artifacts / target).exists(), target)
        for copy in ("initial-workspace", "workspace"):
            self.assertFalse((artifacts / copy / "review.md").exists())
        self.assertIn("Human review pending", (artifacts / "report.txt").read_text())
        self.assertFalse((artifacts / "functional-checks.json").exists())
        self.assertFalse((artifacts / "checks").exists())
        self.assertEqual((profile / "case-invocations").read_text(), "durable-finding-review\n")
        self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_findings_assertion_and_capture_failures_remain_distinct_and_pending(self):
        for scenario, exit_code in (("source-edited", 1), ("empty", 1), ("missing-response", 2), ("invalid-utf8", 2)):
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="durable-finding-review")
                artifacts, metadata, report = self.finish(process, runs, exit_code)
                self.assertEqual(report["case"], "durable-finding-review")
                self.assertTrue(report["review_required"])
                self.assertEqual((artifacts / "review.md").read_text(), findings.REVIEW_RUBRIC)
                self.assertIn("Human review pending", (artifacts / "report.txt").read_text())
                for name in ("initial-workspace.json", "final-workspace.json", "workspace-changes.txt", "events.jsonl", "stderr.txt"):
                    self.assertTrue((artifacts / name).is_file(), name)
                if exit_code == 1:
                    self.assertEqual(metadata["status"], "completed")
                    self.assertEqual(report["outcome"], "assertion_failed")
                    self.assertEqual(report["execution_errors"], [])
                    result, = report["cases"]
                    self.assertEqual(result["evaluator_errors"], [])
                    self.assertEqual(result["assertions"], {
                        "ProtectedStatePreserved": scenario != "source-edited", "FinalResponsePresent": scenario != "empty",
                    })
                    if scenario == "source-edited":
                        self.assertIn("exporter.py: contents changed", result["assertion_reasons"]["ProtectedStatePreserved"])
                        self.assertIn('Path: "exporter.py"', (artifacts / "workspace-changes.txt").read_text())
                    else:
                        self.assertEqual((artifacts / "final-response.txt").read_bytes(), b"")
                else:
                    self.assertEqual(metadata["status"], "error")
                    self.assertEqual(report["outcome"], "execution_failed")
                    self.assertEqual(report["cases"], [])
                    self.assertIn("Final response capture failed", metadata["error"])
                self.assertEqual((profile / "case-invocations").read_text(), "durable-finding-review\n")
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_findings_missing_observation_is_an_error_not_a_preservation_verdict(self):
        selected = next(case for case in cli.CASES if case.name == "durable-finding-review")
        workspaces = []
        runs = self.root / "missing-observation"

        def execute(prompt, workspace, **kwargs):
            self.assertEqual(prompt, findings.PROMPT)
            self.assertTrue(kwargs["observe_workspace"])
            self.assertTrue(kwargs["capture_response"])
            workspaces.append(workspace)
            return ExecutionResult("completed", final_response="Synthetic result.", workspace_observation=None)

        with (patch.object(cli, "ARTIFACTS_ROOT", runs), patch.object(cli, "run_codex", side_effect=execute),
              redirect_stdout(StringIO()), redirect_stderr(StringIO())):
            code = cli.run_case(selected, model="test-model", effort="medium", timeout=10,
                                profile=self.root / "unused-profile", cancelled=Event())
        self.assertEqual(code, 2)
        self.assertEqual(len(workspaces), 1)
        self.assertFalse(workspaces[0].exists())
        artifacts, = runs.iterdir()
        self.assertEqual((artifacts / "review.md").read_text(), findings.REVIEW_RUBRIC)
        self.assertIn("Human review pending", (artifacts / "report.txt").read_text())
        report = json.loads((artifacts / "report.json").read_text())
        self.assertEqual(report["case"], "durable-finding-review")
        self.assertEqual(report["outcome"], "execution_failed")
        self.assertTrue(report["review_required"])
        self.assertEqual(report["execution_errors"], [])
        self.assertEqual(report["evidence_errors"], [])
        result, = report["cases"]
        self.assertEqual(result["assertions"], {"FinalResponsePresent": True})
        failure, = result["evaluator_errors"]
        self.assertIn("WorkspaceInspectionError", failure)


if __name__ == "__main__":
    unittest.main()
