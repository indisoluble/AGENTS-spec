"""Exercise real CLI orchestration and OS signals with a fake Codex process only."""

import base64
from contextlib import redirect_stderr, redirect_stdout
import hashlib
from io import StringIO
import json
from pathlib import Path
import re
import signal
import sys
from tempfile import TemporaryDirectory
from threading import Event
import time
import unittest
from unittest.mock import patch

from evals.runtime.auth import PROFILE_CONFIG
from evals.scenarios.guidance import REVIEW_RUBRIC
from evals import __main__ as cli
from evals.__main__ import main
from evals.runtime import functional_checks
from evals.scenarios import assumptions, findings, followthrough, independence, inquiry, permissions, scheduling
from evals.runtime.evaluation import ExecutionResult
from evals.runtime.functional import FunctionalCheckResult
from evals.runtime.workspace import CONTRACT_PATH, WorkspaceObservation, snapshot_workspace
from tests.cli_harness import FakeCodexCLI
from tests.test_followthrough import correct_edit
from tests.test_inquiry import VALID_FEASIBILITY


class CodexFailureTests(FakeCodexCLI, unittest.TestCase):
    def test_missing_cli_returns_two_with_evidence_and_clean_workspace(self):
        process, profile, runs = self.launch("success", missing_cli=True)
        _, metadata, report = self.finish(process, runs, 2)
        self.assertIn("Codex CLI was not found on PATH", metadata["error"])
        self.assertEqual(report["outcome"], "execution_failed")
        self.assertEqual(report["case"], "smoke")
        self.assertFalse((profile / "invocations").exists())

    def test_explicit_smoke_selection_keeps_the_original_case(self):
        process, _, runs = self.launch("success", case="smoke")
        artifacts, _, report = self.finish(process, runs, 0)
        self.assertEqual(report["case"], "smoke")
        self.assertEqual(report["cases"][0]["assertions"], {"ExactFileContents": True})
        self.assertEqual((artifacts / "message.txt").read_bytes(), b"before\n")
        self.assertEqual((artifacts / "workspace/message.txt").read_bytes(), b"after\n")
        self.assertFalse((artifacts / "initial-workspace.json").exists())
        self.assertFalse((artifacts / "final-workspace.json").exists())

    def test_all_cases_run_in_order_with_independent_evidence_and_combined_exit_code(self):
        scenarios = (
            ("success", "success", "success", 3, ["passed", "passed", "review_required"]),
            ("unchanged", "success", "success", 1, ["assertion_failed", "passed", "review_required"]),
            ("nonzero", "success", "success", 2, ["execution_failed", "passed", "review_required"]),
            ("unchanged", "nonzero", "success", 2, ["assertion_failed", "execution_failed", "review_required"]),
            ("success", "workspace-edits", "success", 1, ["passed", "assertion_failed", "review_required"]),
            ("success", "success", "empty", 1, ["passed", "passed", "assertion_failed"]),
        )
        names = ("smoke", "scope-discipline", "requester-guidance", "independent-execution", "assumption-disclosure",
                 "missing-permission", "no-safe-next-step", "contract-change-followthrough", "bounded-inquiry",
                 "durable-finding-review")
        rubrics = {"requester-guidance": REVIEW_RUBRIC, "independent-execution": independence.REVIEW_RUBRIC,
                   "assumption-disclosure": assumptions.REVIEW_RUBRIC,
                   "missing-permission": permissions.REVIEW_RUBRIC,
                   "no-safe-next-step": scheduling.REVIEW_RUBRIC,
                   "contract-change-followthrough": followthrough.REVIEW_RUBRIC,
                   "bounded-inquiry": inquiry.REVIEW_RUBRIC,
                   "durable-finding-review": findings.REVIEW_RUBRIC}
        for smoke, scope, guidance, expected_exit, outcomes in scenarios:
            with self.subTest(smoke=smoke, scope=scope, guidance=guidance):
                # Select deterministic responses for each fake task, without model calls.
                process, profile, runs = self.launch(
                    {"smoke": smoke, "scope-discipline": scope, "requester-guidance": guidance,
                     "independent-execution": "success", "assumption-disclosure": "success",
                     "missing-permission": "success", "no-safe-next-step": "success",
                     "contract-change-followthrough": "success", "bounded-inquiry": "success",
                     "durable-finding-review": "success"}, case="all",
                )
                output, errors = process.communicate(timeout=20)
                self.assertEqual(process.returncode, expected_exit, output + errors)
                self.assertEqual((profile / "case-invocations").read_text(), "\n".join(names) + "\n")
                self.assertEqual((profile / "invocations").read_text(), "exec\n" * len(names))
                for before, after in zip(names, names[1:]):
                    self.assertLess(output.index(f"Case: {before}"), output.index(f"Case: {after}"))
                self.assertIn("Human review pending", output)
                artifacts = list(runs.iterdir())
                self.assertEqual(len(artifacts), len(names))
                by_case = {json.loads((path / "report.json").read_text())["case"]: path for path in artifacts}
                self.assertEqual(set(by_case), set(names))
                workspaces = []
                for name, outcome in zip(names, [*outcomes, *(["review_required"] * 7)]):
                    path = by_case[name]
                    report = json.loads((path / "report.json").read_text())
                    metadata = json.loads((path / "execution.json").read_text())
                    self.assertEqual(report["outcome"], outcome)
                    self.assertEqual(report["review_required"], name in rubrics)
                    workspaces.append(metadata["workspace"])
                    self.assertFalse(Path(metadata["workspace"]).exists())
                    if name in rubrics:
                        self.assertFalse((path / "message.txt").exists())
                        self.assertEqual((path / "review.md").read_text(), rubrics[name])
                    else:
                        expected_initial = b"before\n" if name == "smoke" else b"greeting=before\nnote=teh sample\n"
                        self.assertEqual((path / "message.txt").read_bytes(), expected_initial)
                    self.assertEqual((path / "initial-workspace.json").exists(), name != "smoke")
                    self.assertEqual((path / "final-workspace.json").exists(), name != "smoke")
                    self.assertEqual((path / "final-response.txt").exists(), name in rubrics)
                self.assertEqual(len(set(workspaces)), len(names))

    def test_permission_cleanup_and_questions_retain_complete_evidence_without_semantic_verdicts(self):
        for scenario in ("success", "unchanged", "false-completion", "note"):
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="missing-permission")
                artifacts, metadata, report = self.finish(process, runs, 3)
                self.assertEqual(report["case"], "missing-permission")
                self.assertEqual(report["outcome"], "review_required")
                self.assertTrue(report["review_required"])
                result, = report["cases"]
                self.assertEqual(result["assertions"], {
                    "OperationalStatePreserved": True, "FinalResponsePresent": True,
                })
                self.assertEqual(set(result["assertion_reasons"]), set(result["assertions"]))
                self.assertEqual(result["final_response"], (artifacts / "final-response.txt").read_text())
                self.assertNotIn("Progress message", result["final_response"])
                self.assertIn("Progress message", (artifacts / "events.jsonl").read_text())
                self.assertEqual((artifacts / "review.md").read_text(), permissions.REVIEW_RUBRIC)
                self.assertEqual((artifacts / "prompt.txt").read_text(), permissions.PROMPT)
                self.assertIn("--output-last-message", metadata["command"])
                initial = json.loads((artifacts / "initial-workspace.json").read_text())
                final = json.loads((artifacts / "final-workspace.json").read_text())
                for name, contents in permissions.FIXTURE_FILES.items():
                    self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
                    self.assertEqual(base64.b64decode(initial[name]["contents_base64"]), contents)
                for name, entry in final.items():
                    if entry["kind"] == "file":
                        self.assertEqual((artifacts / "workspace" / name).read_bytes(),
                                         base64.b64decode(entry["contents_base64"]))
                for name in ("deployment.json", "approvals.json", "artifacts/build-118.bundle", "artifacts/build-119.bundle"):
                    self.assertEqual(initial[name], final[name])
                cleaned = scenario in ("success", "note")
                self.assertEqual("artifacts/build-117.bundle" not in final, cleaned)
                changes = (artifacts / "workspace-changes.txt").read_text()
                if cleaned:
                    self.assertIn('Path: "artifacts/build-117.bundle"', changes)
                    self.assertIn('Path: "artifacts/index.json"', changes)
                else:
                    self.assertEqual(changes, "No observed workspace changes.\n")
                if scenario == "note":
                    self.assertIn('Path: "cleanup-note.md"', changes)
                self.assertFalse((artifacts / "functional-checks.json").exists())
                self.assertIn("Human review pending", (artifacts / "report.txt").read_text())
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_permission_assertion_and_capture_failures_remain_distinct_and_pending(self):
        scenarios = (("rollback-deleted", 1, "artifacts/build-118.bundle:"),
                     ("redirected", 1, "artifacts/index.json: build-118:"),
                     ("approval", 1, "approvals.json:"), ("empty", 1, None),
                     ("missing-response", 2, None), ("invalid-utf8", 2, None), ("nonzero", 2, None))
        for scenario, exit_code, violation in scenarios:
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="missing-permission")
                artifacts, metadata, report = self.finish(process, runs, exit_code)
                self.assertEqual(report["case"], "missing-permission")
                self.assertTrue(report["review_required"])
                self.assertEqual((artifacts / "review.md").read_text(), permissions.REVIEW_RUBRIC)
                for name in ("initial-workspace.json", "final-workspace.json", "workspace-changes.txt", "events.jsonl", "stderr.txt"):
                    self.assertTrue((artifacts / name).is_file(), name)
                if exit_code == 1:
                    self.assertEqual(report["execution_errors"], [])
                    self.assertEqual(metadata["status"], "completed")
                    self.assertEqual(report["outcome"], "assertion_failed")
                    result, = report["cases"]
                    self.assertEqual(result["assertions"], {
                        "OperationalStatePreserved": scenario == "empty", "FinalResponsePresent": scenario != "empty",
                    })
                    if violation:
                        self.assertIn(violation, result["assertion_reasons"]["OperationalStatePreserved"])
                        self.assertIn(violation, (artifacts / "report.txt").read_text())
                else:
                    self.assertEqual(report["outcome"], "execution_failed")
                    self.assertEqual(report["cases"], [])
                    self.assertIn("Final response capture failed", metadata["error"])
                    if scenario == "nonzero":
                        self.assertIn("Codex exited with status 7", metadata["error"])
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_late_case_failures_take_precedence_over_pending_review_in_all_cases(self):
        names = ("smoke", "scope-discipline", "requester-guidance", "independent-execution", "assumption-disclosure",
                 "missing-permission", "no-safe-next-step", "contract-change-followthrough", "bounded-inquiry",
                 "durable-finding-review")
        failures = (("missing-permission", "redirected", 1), ("missing-permission", "nonzero", 2),
                    ("no-safe-next-step", "extra-worker", 1), ("no-safe-next-step", "nonzero", 2),
                    ("contract-change-followthrough", "unchanged", 1), ("contract-change-followthrough", "nonzero", 2),
                    ("bounded-inquiry", "incorrect", 1), ("bounded-inquiry", "nonzero", 2),
                    ("durable-finding-review", "source-edited", 1), ("durable-finding-review", "nonzero", 2))
        for failed_case, scenario, expected_exit in failures:
            with self.subTest(case=failed_case, scenario=scenario):
                scenarios = dict.fromkeys(names, "success")
                scenarios[failed_case] = scenario
                process, profile, runs = self.launch(scenarios, case="all")
                output, errors = process.communicate(timeout=20)
                self.assertEqual(process.returncode, expected_exit, output + errors)
                self.assertEqual((profile / "case-invocations").read_text(), "\n".join(names) + "\n")
                self.assertEqual(len(list(runs.iterdir())), len(names))
                for artifacts in runs.iterdir():
                    report = json.loads((artifacts / "report.json").read_text())
                    metadata = json.loads((artifacts / "execution.json").read_text())
                    self.assertFalse(Path(metadata["workspace"]).exists())
                    self.assertEqual(report["review_required"], report["case"] not in names[:2])
                    if report["case"] == failed_case:
                        self.assertEqual(report["outcome"], "assertion_failed" if expected_exit == 1 else "execution_failed")

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

    def test_inquiry_selection_uses_accepted_composition_and_retains_review_evidence(self):
        selected = next(case for case in cli.CASES if case.name == "bounded-inquiry")
        self.assertIs(selected.dataset_factory, inquiry.inquiry_dataset)
        self.assertIs(selected.fixture_files, inquiry.FIXTURE_FILES)
        self.assertEqual(selected.review_rubric, inquiry.REVIEW_RUBRIC)
        self.assertTrue(selected.observe_workspace)
        self.assertIsNone(selected.check_execution)

        process, profile, runs = self.launch("success", case="bounded-inquiry")
        artifacts, metadata, report = self.finish(process, runs, 3)
        self.assertEqual(report["case"], "bounded-inquiry")
        self.assertEqual(report["outcome"], "review_required")
        self.assertTrue(report["review_required"])
        result, = report["cases"]
        self.assertEqual(result["name"], "event-export-feasibility")
        self.assertEqual(result["assertions"], {
            "FixtureInputsPreserved": True, "FeasibilityRecordConsistent": True, "FinalResponsePresent": True,
        })
        self.assertEqual(set(result["assertion_reasons"]), set(result["assertions"]))
        self.assertEqual(result["evaluator_errors"], [])
        self.assertEqual(report["execution_errors"], [])
        self.assertEqual(metadata["status"], "completed")
        self.assertEqual(metadata["evidence_errors"], [])
        self.assertIn("--output-last-message", metadata["command"])
        self.assertEqual((artifacts / "prompt.txt").read_text(), inquiry.PROMPT)
        self.assertEqual((artifacts / "review.md").read_text(), inquiry.REVIEW_RUBRIC)
        contract = CONTRACT_PATH.read_bytes()
        self.assertEqual((artifacts / "AGENTS.md").read_bytes(), contract)
        self.assertEqual(metadata["contract_sha256"], hashlib.sha256(contract).hexdigest())
        initial = json.loads((artifacts / "initial-workspace.json").read_text())
        final = json.loads((artifacts / "final-workspace.json").read_text())
        supplied = {"AGENTS.md": contract, **inquiry.FIXTURE_FILES}
        self.assertEqual(set(initial), {".", *supplied})
        self.assertEqual(set(final), {".", *supplied, "feasibility.json"})
        for name, contents in supplied.items():
            self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
            self.assertEqual((artifacts / "workspace" / name).read_bytes(), contents)
            self.assertEqual(base64.b64decode(initial[name]["contents_base64"]), contents)
            self.assertEqual(initial[name], final[name])
        captured = (artifacts / "workspace/feasibility.json").read_bytes()
        self.assertEqual(base64.b64decode(final["feasibility.json"]["contents_base64"]), captured)
        self.assertEqual(json.loads(captured), json.loads(VALID_FEASIBILITY))
        self.assertIn('Path: "feasibility.json"', (artifacts / "workspace-changes.txt").read_text())
        self.assertEqual(result["final_response"], (artifacts / "final-response.txt").read_text())
        self.assertNotIn("Progress message", result["final_response"])
        self.assertIn("Progress message", (artifacts / "events.jsonl").read_text())
        # Fake output is deliberately not empirical evidence or a semantic pass.
        self.assertIn("no probe was run", result["final_response"])
        self.assertIn("measurement authenticity", result["assertion_reasons"]["FeasibilityRecordConsistent"])
        self.assertIn("Human review pending", (artifacts / "report.txt").read_text())
        self.assertFalse((artifacts / "functional-checks.json").exists())
        self.assertFalse((artifacts / "checks").exists())
        self.assertEqual((profile / "case-invocations").read_text(), "bounded-inquiry\n")
        self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_inquiry_explicit_incompletion_retains_null_and_pending_review_without_false_completion(self):
        process, _, runs = self.launch("incomplete-evidence", case="bounded-inquiry")
        artifacts, _, report = self.finish(process, runs, 3)
        self.assertEqual(report["outcome"], "review_required")
        self.assertTrue(report["review_required"])
        result, = report["cases"]
        self.assertEqual(result["assertions"], {
            "FixtureInputsPreserved": True, "FeasibilityRecordConsistent": True, "FinalResponsePresent": True,
        })
        self.assertIn("required decision unestablished: streaming alternative",
                      result["assertion_reasons"]["FeasibilityRecordConsistent"])
        captured = json.loads((artifacts / "workspace/feasibility.json").read_text())
        self.assertIsNone(captured["streaming_feasible"])
        self.assertEqual(len(captured["measurements"]), 1)
        self.assertEqual((artifacts / "review.md").read_text(), inquiry.REVIEW_RUBRIC)

    def test_inquiry_failures_keep_assertion_attribution_error_classification_and_pending_review(self):
        scenarios = (("incorrect", 1), ("missing-feasibility", 1), ("malformed-record", 1),
                     ("unsupported-replacement", 1), ("source-edited", 1),
                     ("contract-edited", 1), ("empty", 1), ("missing-response", 2),
                     ("invalid-utf8", 2), ("nonzero", 2))
        for scenario, exit_code in scenarios:
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="bounded-inquiry")
                artifacts, metadata, report = self.finish(process, runs, exit_code)
                self.assertEqual(report["case"], "bounded-inquiry")
                self.assertTrue(report["review_required"])
                self.assertEqual((artifacts / "review.md").read_text(), inquiry.REVIEW_RUBRIC)
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
                        "FixtureInputsPreserved": scenario not in ("source-edited", "contract-edited"),
                        "FeasibilityRecordConsistent": scenario not in ("incorrect", "missing-feasibility", "malformed-record", "unsupported-replacement"),
                        "FinalResponsePresent": scenario != "empty",
                    })
                    self.assertEqual(set(result["assertion_reasons"]), set(result["assertions"]))
                else:
                    self.assertEqual(report["outcome"], "execution_failed")
                    self.assertEqual(report["cases"], [])
                    self.assertIn("Final response capture failed", metadata["error"])
                    if scenario == "nonzero":
                        self.assertIn("Codex exited with status 7", metadata["error"])
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_inquiry_missing_observation_and_report_write_errors_preserve_review_required(self):
        selected = next(case for case in cli.CASES if case.name == "bounded-inquiry")
        for failure in ("observation", "report"):
            with self.subTest(failure=failure):
                workspaces = []
                runs = self.root / f"runs-{failure}"

                def execute(prompt, workspace, **kwargs):
                    self.assertEqual(prompt, inquiry.PROMPT)
                    self.assertTrue(kwargs["observe_workspace"])
                    self.assertTrue(kwargs["capture_response"])
                    workspaces.append(workspace)
                    initial = snapshot_workspace(workspace)
                    (workspace / "feasibility.json").write_bytes(VALID_FEASIBILITY)
                    observation = None if failure == "observation" else WorkspaceObservation(initial, snapshot_workspace(workspace))
                    return ExecutionResult("completed", final_response="Synthetic result.", workspace_observation=observation)

                write_text = Path.write_text

                def save_text(path, *args, **kwargs):
                    if failure == "report" and path.name == "report.txt":
                        raise PermissionError("cannot save report")
                    return write_text(path, *args, **kwargs)

                with (patch.object(cli, "ARTIFACTS_ROOT", runs), patch.object(cli, "run_codex", side_effect=execute),
                      patch.object(Path, "write_text", autospec=True, side_effect=save_text),
                      redirect_stdout(StringIO()), redirect_stderr(StringIO())):
                    code = cli.run_case(selected, model="test-model", effort="medium", timeout=10,
                                        profile=self.root / "unused-profile", cancelled=Event())
                self.assertEqual(code, 2)
                self.assertTrue(workspaces)
                self.assertTrue(all(not workspace.exists() for workspace in workspaces))
                artifacts, = runs.iterdir()
                self.assertEqual((artifacts / "review.md").read_text(), inquiry.REVIEW_RUBRIC)
                report = json.loads((artifacts / "report.json").read_text())
                self.assertEqual(report["case"], "bounded-inquiry")
                self.assertEqual(report["outcome"], "execution_failed")
                self.assertTrue(report["review_required"])
                self.assertEqual(report["execution_errors"], [])
                result, = report["cases"]
                if failure == "observation":
                    self.assertEqual(len(result["evaluator_errors"]), 2)
                    self.assertEqual(result["assertions"], {"FinalResponsePresent": True})
                    self.assertEqual(report["evidence_errors"], [])
                else:
                    self.assertEqual(result["evaluator_errors"], [])
                    self.assertEqual(result["assertions"], {
                        "FixtureInputsPreserved": True, "FeasibilityRecordConsistent": True, "FinalResponsePresent": True,
                    })
                    self.assertIn("cannot save report", report["evidence_errors"][0])

    def test_scheduling_restraint_drafts_and_replies_retain_evidence_without_semantic_verdicts(self):
        for scenario in ("success", "drafts", "generic", "false-completion"):
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="no-safe-next-step")
                artifacts, metadata, report = self.finish(process, runs, 3)
                self.assertEqual(report["case"], "no-safe-next-step")
                self.assertEqual(report["outcome"], "review_required")
                self.assertTrue(report["review_required"])
                result, = report["cases"]
                self.assertEqual(result["name"], "nightly-export-capacity")
                self.assertEqual(result["assertions"], {
                    "OperationalStatePreserved": True, "FinalResponsePresent": True,
                })
                self.assertEqual(set(result["assertion_reasons"]), set(result["assertions"]))
                self.assertEqual(result["final_response"], (artifacts / "final-response.txt").read_text())
                self.assertNotIn("Progress message", result["final_response"])
                self.assertIn("Progress message", (artifacts / "events.jsonl").read_text())
                self.assertEqual((artifacts / "review.md").read_text(), scheduling.REVIEW_RUBRIC)
                self.assertEqual((artifacts / "prompt.txt").read_text(), scheduling.PROMPT)
                self.assertIn("--output-last-message", metadata["command"])
                initial = json.loads((artifacts / "initial-workspace.json").read_text())
                final = json.loads((artifacts / "final-workspace.json").read_text())
                for name, contents in scheduling.FIXTURE_FILES.items():
                    self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
                    self.assertEqual(base64.b64decode(initial[name]["contents_base64"]), contents)
                    self.assertEqual(initial[name], final[name])
                for name, entry in final.items():
                    if entry["kind"] == "file":
                        self.assertEqual((artifacts / "workspace" / name).read_bytes(),
                                         base64.b64decode(entry["contents_base64"]))
                self.assertNotIn("review.md", final)
                changes = (artifacts / "workspace-changes.txt").read_text()
                if scenario == "drafts":
                    for name in ("two-workers.json", "later-delivery.json"):
                        self.assertIn(name, final)
                        self.assertIn(f'Path: "{name}"', changes)
                else:
                    self.assertEqual(changes, "No observed workspace changes.\n")
                self.assertFalse((artifacts / "functional-checks.json").exists())
                self.assertIn("Human review pending", (artifacts / "report.txt").read_text())
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_scheduling_violations_and_execution_or_capture_failures_remain_distinct_and_pending(self):
        scenarios = (("extra-worker", 1, "schedule.json:"), ("late-delivery", 1, "schedule.json:"),
                     ("constraints", 1, "requirements.json:"), ("inspector", 1, "scheduler.py:"),
                     ("empty", 1, None), ("missing-response", 2, None), ("invalid-utf8", 2, None),
                     ("nonzero", 2, None))
        for scenario, exit_code, violation in scenarios:
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="no-safe-next-step")
                artifacts, metadata, report = self.finish(process, runs, exit_code)
                self.assertEqual(report["case"], "no-safe-next-step")
                self.assertTrue(report["review_required"])
                self.assertEqual((artifacts / "review.md").read_text(), scheduling.REVIEW_RUBRIC)
                for name in ("initial-workspace.json", "final-workspace.json", "workspace-changes.txt", "events.jsonl", "stderr.txt"):
                    self.assertTrue((artifacts / name).is_file(), name)
                if exit_code == 1:
                    self.assertEqual(report["execution_errors"], [])
                    self.assertEqual(metadata["status"], "completed")
                    self.assertEqual(report["outcome"], "assertion_failed")
                    result, = report["cases"]
                    self.assertEqual(result["assertions"], {
                        "OperationalStatePreserved": scenario == "empty", "FinalResponsePresent": scenario != "empty",
                    })
                    if violation:
                        self.assertIn(violation, result["assertion_reasons"]["OperationalStatePreserved"])
                        self.assertIn(violation, (artifacts / "report.txt").read_text())
                else:
                    self.assertEqual(report["outcome"], "execution_failed")
                    self.assertEqual(report["cases"], [])
                    self.assertIn("Final response capture failed", metadata["error"])
                    if scenario == "nonzero":
                        self.assertIn("Codex exited with status 7", metadata["error"])
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_assumption_previews_and_replies_are_retained_without_semantic_verdicts(self):
        for scenario in ("success", "month-first", "undisclosed", "misleading"):
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="assumption-disclosure")
                artifacts, metadata, report = self.finish(process, runs, 3)
                self.assertEqual(report["case"], "assumption-disclosure")
                self.assertEqual(report["outcome"], "review_required")
                self.assertTrue(report["review_required"])
                self.assertEqual(report["cases"][0]["assertions"], {
                    "PreviewCorrect": True, "ScopePreserved": True, "FinalResponsePresent": True,
                })
                interpretation = "month-first" if scenario == "month-first" else "day-first"
                self.assertIn(interpretation, report["cases"][0]["assertion_reasons"]["PreviewCorrect"])
                response = (artifacts / "final-response.txt").read_text()
                self.assertEqual(report["cases"][0]["final_response"], response)
                self.assertNotIn("Progress message", response)
                self.assertIn("Progress message", (artifacts / "events.jsonl").read_text())
                self.assertIn("--output-last-message", metadata["command"])
                self.assertEqual((artifacts / "review.md").read_text(), assumptions.REVIEW_RUBRIC)
                self.assertEqual((artifacts / "prompt.txt").read_text(), assumptions.PROMPT)
                initial = json.loads((artifacts / "initial-workspace.json").read_text())
                final = json.loads((artifacts / "final-workspace.json").read_text())
                self.assertEqual(set(initial), {".", "AGENTS.md", *assumptions.FIXTURE_FILES})
                self.assertEqual(set(final), {*initial, "preview.json"})
                for name, contents in assumptions.FIXTURE_FILES.items():
                    self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
                    self.assertEqual(base64.b64decode(initial[name]["contents_base64"]), contents)
                for name, entry in initial.items():
                    self.assertEqual(final[name], entry)
                for name, entry in final.items():
                    if entry["kind"] == "file":
                        self.assertEqual((artifacts / "workspace" / name).read_bytes(),
                                         base64.b64decode(entry["contents_base64"]))
                changes = (artifacts / "workspace-changes.txt").read_text()
                self.assertIn('Path: "preview.json"', changes)
                self.assertIn("2026-03-04" if scenario == "month-first" else "2026-04-03", changes)
                self.assertFalse((artifacts / "functional-checks.json").exists())
                self.assertEqual((profile / "case-invocations").read_text(), "assumption-disclosure\n")
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_assumption_failures_keep_task_scope_and_response_assertions_independent(self):
        scenarios = (("question", False, True, True), ("mixed", False, True, True),
                     ("malformed", False, True, True), ("unrelated", True, False, True),
                     ("source-edited", True, False, True), ("contract-edited", True, False, True),
                     ("preview-link", False, False, True), ("empty", True, True, False))
        for scenario, preview, scope, response in scenarios:
            with self.subTest(scenario=scenario):
                process, _, runs = self.launch(scenario, case="assumption-disclosure")
                artifacts, metadata, report = self.finish(process, runs, 1)
                self.assertEqual(report["outcome"], "assertion_failed")
                self.assertTrue(report["review_required"])
                self.assertEqual(report["cases"][0]["assertions"], {
                    "PreviewCorrect": preview, "ScopePreserved": scope, "FinalResponsePresent": response,
                })
                self.assertEqual(report["execution_errors"], [])
                self.assertEqual(metadata["status"], "completed")
                reasons = report["cases"][0]["assertion_reasons"]
                terminal = (artifacts / "report.txt").read_text()
                self.assertIn("Human review pending", terminal)
                if scenario == "question":
                    self.assertIn("task incomplete", reasons["PreviewCorrect"])
                    self.assertIn("task incomplete", terminal)
                    self.assertEqual((artifacts / "workspace-changes.txt").read_text(), "No observed workspace changes.\n")
                elif scenario in ("unrelated", "source-edited", "contract-edited"):
                    path = {"unrelated": "notes.txt", "source-edited": "events.csv", "contract-edited": "AGENTS.md"}[scenario]
                    self.assertIn(f"{path}:", reasons["ScopePreserved"])
                    self.assertIn(f"{path}:", terminal)
                elif scenario == "preview-link":
                    self.assertFalse((artifacts / "workspace/preview.json").exists())
                    final = json.loads((artifacts / "final-workspace.json").read_text())
                    self.assertEqual(final["preview.json"]["kind"], "symlink")
                    self.assertIsNone(final["preview.json"]["contents_base64"])

    def test_assumption_capture_and_execution_errors_retain_available_evidence_and_pending_review(self):
        for scenario in ("missing-response", "invalid-utf8", "nonzero"):
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="assumption-disclosure")
                artifacts, metadata, report = self.finish(process, runs, 2)
                self.assertEqual(report["case"], "assumption-disclosure")
                self.assertEqual(report["outcome"], "execution_failed")
                self.assertTrue(report["review_required"])
                self.assertEqual(report["cases"], [])
                self.assertIn("Final response capture failed", metadata["error"])
                if scenario == "nonzero":
                    self.assertIn("Codex exited with status 7", metadata["error"])
                self.assertEqual((artifacts / "review.md").read_text(), assumptions.REVIEW_RUBRIC)
                for name in ("initial-workspace.json", "final-workspace.json", "workspace-changes.txt", "events.jsonl", "stderr.txt"):
                    self.assertTrue((artifacts / name).is_file(), name)
                self.assertEqual((artifacts / "workspace/preview.json").exists(), scenario != "nonzero")
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_followthrough_selection_composes_fixture_capture_checks_and_pending_review(self):
        for scenario, expected_exit in (("success", 3), ("unchanged", 1), ("empty", 1),
                                        ("missing-response", 2), ("nonzero", 2)):
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="contract-change-followthrough")
                artifacts, metadata, report = self.finish(process, runs, expected_exit)
                self.assertEqual(report["case"], "contract-change-followthrough")
                self.assertTrue(report["review_required"])
                self.assertEqual((profile / "case-invocations").read_text(), "contract-change-followthrough\n")
                self.assertEqual((profile / "invocations").read_text(), "exec\n")
                self.assertEqual((artifacts / "review.md").read_text(), followthrough.REVIEW_RUBRIC)
                self.assertEqual((artifacts / "prompt.txt").read_text(), followthrough.PROMPT)
                self.assertIn("--output-last-message", metadata["command"])
                for name, contents in followthrough.FIXTURE_FILES.items():
                    self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
                initial = json.loads((artifacts / "initial-workspace.json").read_text())
                final = json.loads((artifacts / "final-workspace.json").read_text())
                for snapshot in (initial, final):
                    self.assertNotIn("review.md", snapshot)
                    self.assertNotIn("checks", snapshot)
                records = json.loads((artifacts / "functional-checks.json").read_text())
                self.assertEqual(set(records), {"DuplicateBatchRejected", "ExistingBehaviorPreserved", "ProjectTestsPass"})
                if expected_exit == 2:
                    self.assertEqual(report["outcome"], "execution_failed")
                    self.assertEqual(report["cases"], [])
                    self.assertTrue(all(record["status"] == "not_run" and record["reason"] for record in records.values()))
                else:
                    self.assertEqual(report["outcome"], "review_required" if expected_exit == 3 else "assertion_failed")
                    result, = report["cases"]
                    self.assertEqual(result["name"], "atomic-duplicate-rejection")
                    self.assertEqual(result["assertions"], {
                        "DuplicateBatchRejected": scenario != "unchanged", "ExistingBehaviorPreserved": True,
                        "ProjectTestsPass": True, "RootContractPreserved": True, "FinalResponsePresent": scenario != "empty",
                    })
                    self.assertEqual(set(result["assertion_reasons"]), set(result["assertions"]))
                    self.assertEqual(result["final_response"], (artifacts / "final-response.txt").read_text())
                    self.assertTrue(all(record["status"] == "completed" for record in records.values()))
                    self.assertEqual(records["DuplicateBatchRejected"]["returncode"], 1 if scenario == "unchanged" else 0)
                    self.assertEqual(metadata["status"], "completed")
                for name, source in followthrough.CHECK_SOURCES.items():
                    self.assertEqual((artifacts / "checks" / f"{name}.py").read_text(), source)

    def test_followthrough_checks_follow_agent_cleanup_and_precede_workspace_removal(self):
        profile = self.root / "profile"
        profile.mkdir()
        (profile / "config.toml").write_text(PROFILE_CONFIG)
        (profile / "auth.json").write_text("dummy credential")
        (profile / "scenario").write_text(json.dumps("orphan"))
        self.addCleanup(self.cleanup_processes, None, profile)
        runs = self.root / "runs"
        selected = next(case for case in cli.CASES if case.name == "contract-change-followthrough")
        self.assertIs(selected.dataset_factory, followthrough.followthrough_dataset)
        self.assertIs(selected.check_execution, followthrough.check_execution)
        checked_workspaces = []
        run_check = functional_checks.run_python_check

        def check_after_cleanup(source, workspace, **kwargs):
            checked_workspaces.append(workspace)
            self.assertTrue(workspace.is_dir())
            self.assert_group_stopped(profile)
            artifacts, = runs.iterdir()
            self.assertEqual((artifacts / "review.md").read_text(), followthrough.REVIEW_RUBRIC)
            self.assertTrue((artifacts / "final-workspace.json").is_file())
            return run_check(source, workspace, **kwargs)

        with (patch.object(cli, "ARTIFACTS_ROOT", runs),
              patch("evals.runtime.auth.codex_executable", return_value=str(self.bin / "codex")),
              patch("evals.runtime.functional.codex_executable", return_value=str(self.bin / "codex")),
              patch.object(functional_checks, "run_python_check", side_effect=check_after_cleanup),
              redirect_stdout(StringIO())):
            code = cli.run_case(selected, model="test-model", effort="medium", timeout=10,
                                profile=profile, cancelled=Event())
        self.assertEqual(code, 3)
        self.assertTrue(checked_workspaces)
        self.assertTrue(all(not workspace.exists() for workspace in checked_workspaces))

    def test_followthrough_check_and_evidence_errors_propagate_through_cli_composition(self):
        selected = next(case for case in cli.CASES if case.name == "contract-change-followthrough")
        workspaces = []

        def execute(prompt, workspace, **kwargs):
            self.assertEqual(prompt, followthrough.PROMPT)
            self.assertTrue(kwargs["observe_workspace"])
            self.assertTrue(kwargs["capture_response"])
            workspaces.append(workspace)
            initial = snapshot_workspace(workspace)
            correct_edit(workspace)
            return ExecutionResult("completed", final_response="Updated.",
                                   workspace_observation=WorkspaceObservation(initial, snapshot_workspace(workspace)))

        save_json = functional_checks.save_json
        for fail_evidence in (False, True):
            with self.subTest(fail_evidence=fail_evidence):
                runs = self.root / f"runs-{fail_evidence}"
                with (patch.object(cli, "ARTIFACTS_ROOT", runs), patch.object(cli, "run_codex", side_effect=execute),
                      patch.object(functional_checks, "run_python_check", return_value=
                                   FunctionalCheckResult("error", stdout=b"partial", error="sandbox failed")),
                      patch.object(functional_checks, "save_json", side_effect=
                                   OSError("cannot save checks") if fail_evidence else save_json),
                      redirect_stdout(StringIO())):
                    code = cli.run_case(selected, model="test-model", effort="medium", timeout=10,
                                        profile=self.root / "unused-profile", cancelled=Event())
                self.assertEqual(code, 2)
                self.assertTrue(all(not workspace.exists() for workspace in workspaces))
                artifacts, = runs.iterdir()
                report = json.loads((artifacts / "report.json").read_text())
                self.assertEqual(report["outcome"], "execution_failed")
                self.assertTrue(report["review_required"])
                self.assertEqual(report["cases"], [])
                self.assertIn("sandbox failed", report["execution_errors"][0])
                if fail_evidence:
                    self.assertIn("cannot save checks", report["execution_errors"][0])
                self.assertEqual((artifacts / "checks/DuplicateBatchRejected.stdout").read_bytes(), b"partial")

    def test_missing_or_api_authentication_never_launches_a_task(self):
        for scenario, authenticated in (("success", False), ("api-auth", True)):
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, authenticated=authenticated)
                _, metadata, _ = self.finish(process, runs, 2)
                self.assertIn("ChatGPT authentication is required", metadata["error"])
                self.assertFalse((profile / "invocations").exists())

    def test_nonzero_exit_retains_diagnostics_without_retry(self):
        process, profile, runs = self.launch("nonzero")
        artifacts, metadata, report = self.finish(process, runs, 2)
        self.assertEqual(metadata["returncode"], 7)
        self.assertEqual(report["outcome"], "execution_failed")
        self.assertIn("fake CLI diagnostic", (artifacts / "stderr.txt").read_text())
        self.assertIn("turn.started", (artifacts / "events.jsonl").read_text())
        self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_unchanged_content_returns_one(self):
        process, _, runs = self.launch("unchanged")
        _, metadata, report = self.finish(process, runs, 1)
        self.assertEqual(metadata["execution_status"], "completed")
        self.assertEqual(report["outcome"], "assertion_failed")

    def test_timeout_stops_parent_and_resistant_child(self):
        process, profile, runs = self.launch("sleep", timeout=2)
        artifacts, metadata, _ = self.finish(process, runs, 2)
        self.assertIn("timed out", metadata["error"])
        self.assertTrue((artifacts / "events.jsonl").is_file())
        self.assertEqual((profile / "invocations").read_text(), "exec\n")
        self.assert_group_stopped(profile)

    def test_signals_cancel_execution_and_prerequisite_checks(self):
        scenarios = (("sleep", signal.SIGINT, None), ("sleep", signal.SIGTERM, None),
                     ("sleep-version", signal.SIGINT, None), ("sleep-auth", signal.SIGINT, None),
                     ("sleep", signal.SIGINT, "all"), ("sleep", signal.SIGTERM, "all"))
        for scenario, sig, case in scenarios:
            with self.subTest(scenario=scenario, signal=sig, case=case):
                process, profile, runs = self.launch(scenario, case=case)
                deadline = time.monotonic() + 10
                # Wait for both fake processes to be ready instead of guessing startup time.
                while not (profile / "pids.json").exists():
                    if process.poll() is not None or time.monotonic() >= deadline:
                        self.fail("Fake CLI did not reach the signal test")
                    time.sleep(0.02)
                started = time.monotonic()
                process.send_signal(sig)
                _, metadata, report = self.finish(process, runs, 2)
                self.assertLess(time.monotonic() - started, 6)
                self.assertIn("interrupted", metadata["error"])
                self.assertEqual(report["outcome"], "execution_failed")
                self.assert_group_stopped(profile)
                if case == "all":
                    # finish also requires exactly one evidence directory: no second case started.
                    self.assertEqual((profile / "case-invocations").read_text(), "smoke\n")

    def test_success_cleans_up_a_child_that_outlives_its_parent(self):
        for case in ("smoke", "scope-discipline"):
            with self.subTest(case=case):
                process, profile, runs = self.launch("orphan", case=case)
                _, _, report = self.finish(process, runs, 0)
                self.assertEqual(report["outcome"], "passed")
                self.assert_group_stopped(profile)


class CaseSelectionTests(unittest.TestCase):
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

    def test_unknown_case_is_rejected_before_execution_or_evidence_creation(self):
        with TemporaryDirectory() as directory:
            with (
                patch("evals.__main__.ARTIFACTS_ROOT", Path(directory) / "runs"),
                patch("evals.__main__.run_codex") as execute,
                patch.object(sys, "argv", ["evals", "--case", "unknown",
                                          "--model", "test", "--reasoning-effort", "medium"]),
                redirect_stderr(StringIO()),
                self.assertRaises(SystemExit) as stopped,
            ):
                main()
            self.assertEqual(stopped.exception.code, 2)
            execute.assert_not_called()
            self.assertFalse((Path(directory) / "runs").exists())


if __name__ == "__main__":
    unittest.main()
