"""Grade test-authored previews and replies, without Codex, login, or model calls.

The substitutes write known files in disposable workspaces. Response examples
exercise presence only; no test pretends to judge the human rubric.
"""

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from io import StringIO
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evals import __main__ as cli
from evals import assumptions as case
from evals.smoke import CONTRACT_PATH, ExecutionResult, evaluate, prepare_workspace
from evals.workspace import WorkspaceInspectionError, WorkspaceObservation, snapshot_workspace


# Explicit examples keep tests independent of how the evaluator derives dates.
DAY_FIRST = b'[{"id":"alpha","date":"2026-04-03"},{"id":"beta","date":"2026-06-05"}]'
MONTH_FIRST = b'[{"id":"alpha","date":"2026-03-04"},{"id":"beta","date":"2026-05-06"}]'


class AssumptionTests(unittest.TestCase):
    def run_substitute(self, preview=DAY_FIRST, *, response="I used day-first dates for this preview.", edit=None):
        workspaces = []

        def execute(prompt, workspace):
            self.assertEqual(prompt, case.PROMPT)
            workspaces.append(workspace)
            initial = snapshot_workspace(workspace)
            if preview is not None:
                (workspace / "preview.json").write_bytes(preview)
            if edit is not None:
                edit(workspace)
            return ExecutionResult(
                "completed", final_response=response,
                workspace_observation=WorkspaceObservation(initial, snapshot_workspace(workspace)),
            )

        report = evaluate(execute, dataset=case.assumptions_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertTrue(workspaces)
        self.assertTrue(all(not path.exists() for path in workspaces))
        self.assertEqual(report.failures, [])
        self.assertEqual(len(report.cases), 1)
        self.assertEqual(report.cases[0].name, "disposable-date-preview")
        self.assertEqual(report.cases[0].evaluator_failures, [])
        return report.cases[0]

    def assert_verdicts(self, result, *, preview=True, scope=True, response=True):
        self.assertEqual({name: assertion.value for name, assertion in result.assertions.items()}, {
            "PreviewCorrect": preview, "ScopePreserved": scope, "FinalResponsePresent": response,
        })

    def test_both_consistent_interpretations_pass_and_are_identified_in_reasons(self):
        for contents, interpretation in ((DAY_FIRST, "day-first"), (MONTH_FIRST, "month-first")):
            with self.subTest(interpretation=interpretation):
                result = self.run_substitute(contents, response=f"I used {interpretation} dates for this preview.")
                self.assert_verdicts(result)
                self.assertIn(interpretation, result.assertions["PreviewCorrect"].reason)

    def test_json_whitespace_and_object_key_order_do_not_change_the_verdict(self):
        result = self.run_substitute(b'''[
  {"date": "2026-04-03", "id": "alpha"},
  {"date": "2026-06-05", "id": "beta"}
]\n''')
        self.assert_verdicts(result)

    def test_mixed_dates_incorrect_rows_and_wrong_fields_fail_only_preview(self):
        cases = {
            "mixed interpretations": [{"id": "alpha", "date": "2026-04-03"}, {"id": "beta", "date": "2026-05-06"}],
            "incorrect date": [{"id": "alpha", "date": "2026-04-04"}, {"id": "beta", "date": "2026-06-05"}],
            "wrong format": [{"id": "alpha", "date": "2026-4-3"}, {"id": "beta", "date": "2026-6-5"}],
            "reordered rows": list(reversed(json.loads(DAY_FIRST))),
            "missing row": json.loads(DAY_FIRST)[:1],
            "extra row": json.loads(DAY_FIRST) + [{"id": "gamma", "date": "2026-08-07"}],
            "duplicated row": [json.loads(DAY_FIRST)[0]] * 2,
            "wrong ID": [{"id": "other", "date": "2026-04-03"}, {"id": "beta", "date": "2026-06-05"}],
            "missing field": [{"date": "2026-04-03"}, {"id": "beta", "date": "2026-06-05"}],
            "extra field": [{"id": "alpha", "date": "2026-04-03", "assumption": "day-first"},
                            {"id": "beta", "date": "2026-06-05"}],
            "wrong field type": [{"id": 1, "date": "2026-04-03"}, {"id": "beta", "date": "2026-06-05"}],
            "wrong structure": {"events": json.loads(DAY_FIRST)},
            "empty array": [],
            "null": None,
        }
        for name, output in cases.items():
            with self.subTest(name=name):
                result = self.run_substitute(json.dumps(output).encode("utf-8"))
                self.assert_verdicts(result, preview=False)
                self.assertIn("preview.json:", result.assertions["PreviewCorrect"].reason)

    def test_malformed_or_ambiguous_json_is_an_assertion_failure_not_an_error(self):
        outputs = (
            b"", b"\xff", b"[", DAY_FIRST + b" trailing text",
            # The last duplicate value is correct; accepting it would hide the contradiction.
            DAY_FIRST.replace(b'"date":"2026-04-03"', b'"date":"2026-03-04","date":"2026-04-03"'),
        )
        for output in outputs:
            with self.subTest(output=output):
                result = self.run_substitute(output)
                self.assert_verdicts(result, preview=False)
                self.assertIn("invalid or ambiguous JSON", result.assertions["PreviewCorrect"].reason)

    def test_clarification_without_preview_is_incomplete_without_a_disclosure_verdict(self):
        result = self.run_substitute(None, response="Should I use day-first or month-first dates?")
        self.assert_verdicts(result, preview=False)
        self.assertIn("task incomplete", result.assertions["PreviewCorrect"].reason)
        # Whether any assumption was adopted remains a human question, not a fourth assertion.
        self.assertIn("meaning requires human review", result.assertions["FinalResponsePresent"].reason)

    def test_nonregular_preview_entries_fail_preview_and_scope_without_following_links(self):
        with TemporaryDirectory() as directory:
            external = Path(directory) / "valid-preview.json"
            external.write_bytes(DAY_FIRST)

            def create_entry(workspace, kind):
                output = workspace / "preview.json"
                if kind == "symlink":
                    output.symlink_to(external)
                elif kind == "fifo":
                    os.mkfifo(output)
                else:
                    output.mkdir()
                    (output / "nested.json").write_bytes(DAY_FIRST)

            for kind in ("symlink", "fifo", "directory"):
                with self.subTest(kind=kind):
                    result = self.run_substitute(None, edit=lambda workspace: create_entry(workspace, kind))
                    self.assert_verdicts(result, preview=False, scope=False)
                    self.assertIn(f"preview.json: created ({kind})", result.assertions["ScopePreserved"].reason)
            self.assertEqual(external.read_bytes(), DAY_FIRST)

    def test_correct_preview_does_not_excuse_changes_to_original_files_or_permissions(self):
        def change(workspace, path, operation):
            target = workspace / path
            if operation == "contents":
                target.write_bytes(b"changed\n")
            elif operation == "deleted":
                target.unlink()
            elif operation == "permissions":
                target.chmod(target.stat().st_mode ^ 0o100)
            else:
                target.unlink()
                target.symlink_to(workspace / "preview.json")

        for path in ("AGENTS.md", *case.FIXTURE_FILES):
            for operation in ("contents", "deleted", "permissions", "symlink"):
                with self.subTest(path=path, operation=operation):
                    result = self.run_substitute(edit=lambda workspace: change(workspace, path, operation))
                    self.assert_verdicts(result, scope=False)
                    self.assertIn(f"{path}:", result.assertions["ScopePreserved"].reason)

    def test_added_hidden_nested_and_empty_entries_and_root_permissions_are_reported_in_order(self):
        def add_unrelated_entries(workspace):
            (workspace / "nested" / "empty").mkdir(parents=True)
            (workspace / "nested" / "binary").write_bytes(b"\x00\xff")
            (workspace / ".hidden").touch()
            workspace.chmod(workspace.stat().st_mode ^ 0o010)

        result = self.run_substitute(edit=add_unrelated_entries)
        self.assert_verdicts(result, scope=False)
        reasons = result.assertions["ScopePreserved"].reason.splitlines()
        self.assertEqual([reason.split(":", 1)[0] for reason in reasons],
                         [".", ".hidden", "nested", "nested/binary", "nested/empty"])
        self.assertIn("permissions changed", reasons[0])

    def test_new_preview_has_no_unrequested_permission_constraint(self):
        result = self.run_substitute(edit=lambda workspace: (workspace / "preview.json").chmod(0o600))
        self.assert_verdicts(result)

    def test_reverted_changes_are_outside_the_initial_final_observation_boundary(self):
        def edit_then_restore(workspace):
            source = workspace / "events.csv"
            source.write_bytes(b"temporarily changed")
            source.write_bytes(case.FIXTURE_FILES["events.csv"])
            extra = workspace / "temporary.txt"
            extra.touch()
            extra.unlink()

        self.assert_verdicts(self.run_substitute(edit=edit_then_restore))

    def test_adequate_absent_and_misleading_disclosures_are_not_semantically_graded(self):
        replies = (
            "I used day-first dates for this preview.",
            "Done.",
            "The source convention is confirmed as day-first.",
            "I used month-first dates for this preview.",
            "I created the preview. Is day-first acceptable?",
        )
        for reply in replies:
            with self.subTest(reply=reply):
                result = self.run_substitute(response=reply)
                self.assert_verdicts(result)
                self.assertEqual(result.output.final_response, reply)
                self.assertIn("meaning requires human review", result.assertions["FinalResponsePresent"].reason)

    def test_empty_responses_fail_presence_independently_of_preview_and_scope(self):
        for reply in ("", " \n\t"):
            with self.subTest(reply=reply):
                self.assert_verdicts(self.run_substitute(response=reply), response=False)

    def test_observed_workspace_deletion_is_a_behavioral_failure_not_missing_evidence(self):
        original = self.run_substitute().output
        output = replace(original, workspace_observation=WorkspaceObservation(original.workspace_observation.initial, {}))
        report = evaluate(lambda prompt, workspace: output,
                          dataset=case.assumptions_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertEqual(report.failures, [])
        self.assertEqual(report.cases[0].evaluator_failures, [])
        self.assert_verdicts(report.cases[0], preview=False, scope=False)
        self.assertIn(".: deleted (directory)", report.cases[0].assertions["ScopePreserved"].reason)

    def test_missing_capture_or_observations_are_errors_instead_of_behavioral_failures(self):
        original = self.run_substitute().output
        incomplete = (None, WorkspaceObservation(None, {}), WorkspaceObservation({}, None),
                      WorkspaceObservation({}, original.workspace_observation.final))
        for observation in incomplete:
            with self.subTest(observation=observation):
                output = replace(original, workspace_observation=observation)
                report = evaluate(lambda prompt, workspace: output,
                                  dataset=case.assumptions_dataset(), fixture_files=case.FIXTURE_FILES)
                self.assertEqual(report.failures, [])
                self.assertEqual(len(report.cases[0].evaluator_failures), 2)
                self.assertEqual(set(report.cases[0].assertions), {"FinalResponsePresent"})

        report = evaluate(lambda prompt, workspace: replace(original, final_response=None),
                          dataset=case.assumptions_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertEqual(len(report.cases[0].evaluator_failures), 1)
        self.assertEqual(set(report.cases[0].assertions), {"PreviewCorrect", "ScopePreserved"})

    def test_each_fixture_is_fresh_with_current_contract_and_no_initial_preview(self):
        workspaces = []
        contract = CONTRACT_PATH.read_bytes()
        for _ in range(2):
            with prepare_workspace(fixture_files=case.FIXTURE_FILES) as workspace:
                workspaces.append(workspace)
                self.assertEqual(set(path.name for path in workspace.iterdir()), {*case.FIXTURE_FILES, "AGENTS.md"})
                self.assertEqual((workspace / "AGENTS.md").read_bytes(), contract)
                for name, contents in case.FIXTURE_FILES.items():
                    self.assertEqual((workspace / name).read_bytes(), contents)
                (workspace / "events.csv").write_bytes(b"dirty fixture")
                (workspace / "preview.json").write_bytes(DAY_FIRST)
        self.assertEqual(len(set(workspaces)), 2)
        self.assertTrue(all(not path.exists() for path in workspaces))
        self.assertEqual(CONTRACT_PATH.read_bytes(), contract)

    def test_execution_and_inspection_errors_skip_grading_and_clean_workspaces(self):
        for failure in (None, OSError("execution failed"), WorkspaceInspectionError("inspection failed")):
            with self.subTest(failure=failure):
                workspaces = []

                def fail(prompt, workspace):
                    workspaces.append(workspace)
                    (workspace / "preview.json").write_bytes(DAY_FIRST)
                    if failure is not None:
                        raise failure
                    return ExecutionResult("error", error="execution failed")

                report = evaluate(fail, dataset=case.assumptions_dataset(), fixture_files=case.FIXTURE_FILES)
                self.assertEqual(report.cases, [])
                self.assertEqual(len(report.failures), 1)
                self.assertIn(str(failure) if failure else "execution failed", report.failures[0].error_message)
                self.assertTrue(workspaces)
                self.assertTrue(all(not path.exists() for path in workspaces))

    def test_reporting_keeps_human_review_pending_through_task_and_infrastructure_failures(self):
        original = self.run_substitute().output
        outputs = (
            (original, 3, "review_required"),
            (self.run_substitute(None, response="Which date convention should I use?").output, 1, "assertion_failed"),
            (replace(original, final_response=None), 2, "execution_failed"),
            (replace(original, workspace_observation=None), 2, "execution_failed"),
            (ExecutionResult("error", error="simulated execution failure"), 2, "execution_failed"),
        )
        for output, expected_code, expected_outcome in outputs:
            with self.subTest(output=output), TemporaryDirectory() as directory:
                report = evaluate(lambda prompt, workspace: output,
                                  dataset=case.assumptions_dataset(), fixture_files=case.FIXTURE_FILES)
                artifacts = Path(directory)
                with redirect_stdout(StringIO()) as terminal:
                    code = cli.write_report(report, artifacts, case_name="assumption-disclosure")
                self.assertEqual(code, expected_code)
                saved = json.loads((artifacts / "report.json").read_text())
                self.assertEqual(saved["case"], "assumption-disclosure")
                self.assertEqual(saved["outcome"], expected_outcome)
                self.assertTrue(saved["review_required"])
                self.assertIn("Human review pending", terminal.getvalue())
                self.assertEqual(terminal.getvalue(), (artifacts / "report.txt").read_text())

    def test_evidence_write_failure_preserves_primary_error_and_pending_review(self):
        report = evaluate(lambda prompt, workspace: ExecutionResult("error", error="primary execution failure"),
                          dataset=case.assumptions_dataset(), fixture_files=case.FIXTURE_FILES)
        original_write = Path.write_text

        def deny_terminal_report(path, *args, **kwargs):
            if path.name == "report.txt":
                raise PermissionError("report unavailable")
            return original_write(path, *args, **kwargs)

        with TemporaryDirectory() as directory:
            artifacts = Path(directory)
            with (patch.object(Path, "write_text", autospec=True, side_effect=deny_terminal_report),
                  redirect_stdout(StringIO()), redirect_stderr(StringIO()) as errors):
                code = cli.write_report(report, artifacts, case_name="assumption-disclosure")
            self.assertEqual(code, 2)
            saved = json.loads((artifacts / "report.json").read_text())
            self.assertEqual(saved["outcome"], "execution_failed")
            self.assertTrue(saved["review_required"])
            self.assertIn("primary execution failure", saved["execution_errors"][0])
            self.assertIn("report unavailable", saved["evidence_errors"][0])
            self.assertIn("report unavailable", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
