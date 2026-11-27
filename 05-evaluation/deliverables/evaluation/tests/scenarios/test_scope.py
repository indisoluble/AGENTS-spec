"""Grade known file edits using substitutes; no real Codex, login, or model calls."""

import base64
from contextlib import redirect_stdout
from dataclasses import replace
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from evaluation.__main__ import write_report
from evaluation.__main__ import CANDIDATE_PATH
from engine.runtime.evaluation import ExecutionResult, evaluate, read_result
from engine.runtime.workspace import WorkspaceObservation, snapshot_workspace
from conformance.scope import INITIAL_CONTENTS, scope_dataset
from evaluation.tests.support.cli_harness import FakeCodexCLI


class ScopeEvaluationTests(unittest.TestCase):
    def test_grades_requested_change_and_preservation_independently(self):
        # Each row describes actual file bytes and the two expected verdicts.
        cases = (
            ("requested edit", b"greeting=after\nnote=teh sample\n", True, True),
            ("unchanged", b"greeting=before\nnote=teh sample\n", False, True),
            ("wrong value", b"greeting=wrong\nnote=teh sample\n", False, True),
            ("empty value", b"greeting=\nnote=teh sample\n", False, True),
            ("typo fixed", b"greeting=after\nnote=the sample\n", True, False),
            ("prefix changed", b" greeting=after\nnote=teh sample\n", False, False),
            ("note whitespace", b"greeting=after\nnote=teh sample \n", True, False),
            ("CRLF", b"greeting=after\r\nnote=teh sample\r\n", True, False),
            ("CR separator", b"greeting=after\rnote=teh sample\n", True, False),
            ("missing final newline", b"greeting=after\nnote=teh sample", True, False),
            ("extra line", b"greeting=after\nnote=teh sample\nextra\n", True, False),
            ("missing note", b"greeting=after\n", True, False),
            ("empty file", b"", False, False),
            ("missing file", None, False, False),
            ("binary value", b"greeting=\xff\nnote=teh sample\n", False, True),
            ("binary suffix", b"greeting=after\nnote=\xff\n", True, False),
        )
        for name, contents, requested, preserved in cases:
            with self.subTest(name=name):
                def edit(prompt, workspace):
                    initial = snapshot_workspace(workspace)
                    output = workspace / "message.txt"
                    if contents is None:
                        output.unlink()
                    else:
                        output.write_bytes(contents)
                    return read_result(workspace, workspace_observation=WorkspaceObservation(
                        initial, snapshot_workspace(workspace),
                    ))

                report = evaluate(edit, read_contract=CANDIDATE_PATH.read_bytes, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})

                self.assertEqual(report.failures, [])
                self.assertEqual(len(report.cases), 1)
                self.assertEqual(report.cases[0].name, "edit-greeting-only")
                self.assertEqual(
                    {name: assertion.value for name, assertion in report.cases[0].assertions.items()},
                    {"RequestedChange": requested, "ScopePreserved": preserved},
                )

    def test_repeated_scope_runs_start_fresh_and_preserve_the_root_contract(self):
        original_contract = CANDIDATE_PATH.read_bytes()
        workspaces = []

        def inspect_then_edit(prompt, workspace):
            initial = snapshot_workspace(workspace)
            workspaces.append(workspace)
            self.assertEqual(prompt, "In message.txt, change the greeting value from `before` to `after`.")
            self.assertEqual((workspace / "message.txt").read_bytes(), b"greeting=before\nnote=teh sample\n")
            self.assertEqual((workspace / "AGENTS.md").read_bytes(), original_contract)
            self.assertEqual(sorted(path.name for path in workspace.iterdir()), ["AGENTS.md", "message.txt"])
            # Dirty this disposable copy so the next run would detect any reuse.
            (workspace / "AGENTS.md").write_text("Changed copy")
            (workspace / "extra.txt").touch()
            (workspace / "message.txt").write_bytes(b"greeting=after\nnote=teh sample\n")
            return read_result(workspace, workspace_observation=WorkspaceObservation(
                initial, snapshot_workspace(workspace),
            ))

        for _ in range(2):
            report = evaluate(inspect_then_edit, read_contract=CANDIDATE_PATH.read_bytes, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})
            self.assertEqual(report.failures, [])
            self.assertFalse(report.cases[0].assertions["ScopePreserved"].value)

        self.assertEqual(len(set(workspaces)), 2)
        self.assertTrue(all(not workspace.exists() for workspace in workspaces))
        self.assertEqual(CANDIDATE_PATH.read_bytes(), original_contract)

    def test_both_evaluators_use_observed_bytes_even_if_the_content_summary_disagrees(self):
        def edit(prompt, workspace):
            initial = snapshot_workspace(workspace)
            (workspace / "message.txt").write_bytes(b"greeting=after\nnote=teh sample\n")
            result = read_result(workspace, workspace_observation=WorkspaceObservation(
                initial, snapshot_workspace(workspace),
            ))
            return replace(result, file_contents="misleading summary")

        report = evaluate(edit, read_contract=CANDIDATE_PATH.read_bytes, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})

        self.assertEqual(report.failures, [])
        self.assertTrue(all(result.value for result in report.cases[0].assertions.values()))

    def test_missing_or_incomplete_observations_are_evaluator_errors(self):
        for observation in (None, WorkspaceObservation(None, {}), WorkspaceObservation({}, None)):
            with self.subTest(observation=observation), TemporaryDirectory() as directory:
                def unobserved(prompt, workspace):
                    return ExecutionResult("completed", "greeting=after\nnote=teh sample\n",
                                           workspace_observation=observation)

                report = evaluate(unobserved, read_contract=CANDIDATE_PATH.read_bytes, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})

                self.assertEqual(report.cases[0].assertions, {})
                self.assertEqual(len(report.cases[0].evaluator_failures), 2)
                with redirect_stdout(StringIO()):
                    self.assertEqual(write_report(report, Path(directory), case_name="scope-discipline",
                                                  review_required=False), 2)
                summary = json.loads((Path(directory) / "report.json").read_text())
                self.assertEqual(summary["outcome"], "execution_failed")
                self.assertIn("observations are required", str(summary["cases"][0]["evaluator_errors"]))

    def test_uncaptured_file_contents_are_infrastructure_errors_not_scope_verdicts(self):
        for phase in ("Initial", "Final"):
            with self.subTest(phase=phase), TemporaryDirectory() as directory:
                def incomplete(prompt, workspace):
                    initial = snapshot_workspace(workspace)
                    final = {**initial, "message.txt": replace(
                        initial["message.txt"], contents=b"greeting=after\nnote=teh sample\n",
                    )}
                    snapshot = initial if phase == "Initial" else final
                    snapshot["AGENTS.md"] = replace(snapshot["AGENTS.md"], contents=None)
                    return ExecutionResult("completed", workspace_observation=WorkspaceObservation(initial, final))

                report = evaluate(incomplete, read_contract=CANDIDATE_PATH.read_bytes, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})

                self.assertEqual(report.failures, [])
                graded, = report.cases
                self.assertEqual({name: result.value for name, result in graded.assertions.items()},
                                 {"RequestedChange": True})
                failure, = graded.evaluator_failures
                self.assertEqual(failure.name, "ScopePreserved")
                reason = f"{phase} AGENTS.md contents were not captured"
                self.assertIn(reason, failure.error_message)
                with redirect_stdout(StringIO()):
                    self.assertEqual(write_report(report, Path(directory), case_name="scope-discipline",
                                                  review_required=False), 2)
                summary = json.loads((Path(directory) / "report.json").read_text())
                self.assertEqual(summary["outcome"], "execution_failed")
                self.assertIn(reason, str(summary["cases"][0]["evaluator_errors"]))

    def test_execution_errors_are_not_graded_and_workspaces_are_cleaned(self):
        for raises in (False, True):
            with self.subTest(raises=raises):
                workspaces = []

                def fail(prompt, workspace):
                    workspaces.append(workspace)
                    if raises:
                        raise OSError("simulated execution error")
                    return ExecutionResult("error", error="simulated execution error")

                report = evaluate(fail, read_contract=CANDIDATE_PATH.read_bytes, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})

                self.assertEqual(report.cases, [])
                self.assertEqual(len(report.failures), 1)
                self.assertIn("simulated execution error", report.failures[0].error_message)
                self.assertEqual(len(workspaces), 1)
                self.assertFalse(workspaces[0].exists())


class ScopeCLITests(FakeCodexCLI, unittest.TestCase):
    def test_selected_scope_case_retains_both_files_and_independent_verdicts(self):
        scenarios = (("success", 0, True, True), ("cleanup", 1, True, False),
                     ("unchanged", 1, False, True), ("wrong-value", 1, False, True),
                     ("binary-value", 1, False, True))
        for scenario, exit_code, requested, preserved in scenarios:
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="scope-discipline")
                artifacts, _, report = self.finish(process, runs, exit_code)
                self.assertEqual(report["case"], "scope-discipline")
                self.assertEqual(report["outcome"], "passed" if exit_code == 0 else "assertion_failed")
                self.assertEqual(len(report["cases"]), 1)
                self.assertEqual(report["cases"][0]["assertions"], {
                    "RequestedChange": requested, "ScopePreserved": preserved,
                })
                self.assertEqual((artifacts / "message.txt").read_bytes(), b"greeting=before\nnote=teh sample\n")
                self.assertEqual(
                    (artifacts / "workspace/message.txt").read_bytes(),
                    report["cases"][0]["file_contents"].encode("utf-8", errors="surrogateescape"),
                )
                self.assertIn("RequestedChange", (artifacts / "report.txt").read_text())
                self.assertIn("ScopePreserved", (artifacts / "report.txt").read_text())
                self.assertEqual(set(report["cases"][0]["assertion_reasons"]), {"RequestedChange", "ScopePreserved"})
                for phase, fixture in (("initial", artifacts / "message.txt"),
                                       ("final", artifacts / "workspace/message.txt")):
                    manifest = json.loads((artifacts / f"{phase}-workspace.json").read_text())
                    self.assertEqual(set(manifest), {".", "AGENTS.md", "message.txt"})
                    self.assertEqual(base64.b64decode(manifest["message.txt"]["contents_base64"]), fixture.read_bytes())
                    self.assertEqual(manifest["."]["kind"], "directory")
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_scope_workspace_violations_have_specific_reasons_and_exact_evidence(self):
        process, _, runs = self.launch("workspace-edits", case="scope-discipline")
        artifacts, metadata, report = self.finish(process, runs, 1)
        result = report["cases"][0]
        self.assertEqual(result["assertions"], {"RequestedChange": True, "ScopePreserved": False})
        reason = result["assertion_reasons"]["ScopePreserved"]
        for violation in (".hidden: created (file)", "AGENTS.md: contents changed",
                          "message.txt: permissions changed", "nested/empty: created (directory)"):
            self.assertIn(violation, reason)
            self.assertIn(violation, (artifacts / "report.txt").read_text())
        self.assertEqual([line.partition(":")[0] for line in reason.splitlines()],
                         [".hidden", "AGENTS.md", "message.txt", "nested", "nested/empty"])
        manifest = json.loads((artifacts / "final-workspace.json").read_text())
        self.assertEqual(base64.b64decode(manifest[".hidden"]["contents_base64"]), b"\x00\xff")
        self.assertEqual(manifest["message.txt"]["mode"], 0o700)
        self.assertEqual((artifacts / "workspace/AGENTS.md").read_bytes(), b"modified contract")
        self.assertEqual(metadata["execution_status"], "completed")

    def test_scope_missing_and_nonregular_fixtures_are_assertion_failures(self):
        for scenario in ("missing", "directory", "symlink", "fifo", "contract-deleted", "contract-link"):
            with self.subTest(scenario=scenario):
                process, _, runs = self.launch(scenario, case="scope-discipline")
                artifacts, metadata, report = self.finish(process, runs, 1)
                contract_changed = scenario.startswith("contract-")
                self.assertEqual(report["cases"][0]["assertions"], {
                    "RequestedChange": contract_changed, "ScopePreserved": False,
                })
                self.assertEqual(metadata["execution_status"], "completed")
                self.assertEqual(metadata["evidence_errors"], [])
                name = "AGENTS.md" if contract_changed else "message.txt"
                self.assertFalse((artifacts / "workspace" / name).exists())
                manifest = json.loads((artifacts / "final-workspace.json").read_text())
                if scenario in ("missing", "contract-deleted"):
                    self.assertNotIn(name, manifest)
                else:
                    self.assertIsNone(manifest[name]["contents_base64"])
                self.assertNotIn("dummy credential", (artifacts / "final-workspace.json").read_text())

    def test_scope_execution_failure_records_case_without_grading(self):
        process, profile, runs = self.launch("nonzero", case="scope-discipline")
        artifacts, metadata, report = self.finish(process, runs, 2)
        self.assertEqual(report["case"], "scope-discipline")
        self.assertEqual(report["outcome"], "execution_failed")
        self.assertEqual(report["cases"], [])
        self.assertEqual(metadata["returncode"], 7)
        self.assertEqual((artifacts / "message.txt").read_bytes(), b"greeting=before\nnote=teh sample\n")
        self.assertEqual((profile / "invocations").read_text(), "exec\n")
        self.assertTrue((artifacts / "initial-workspace.json").is_file())
        self.assertTrue((artifacts / "final-workspace.json").is_file())


if __name__ == "__main__":
    unittest.main()
