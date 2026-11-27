"""Validate the fixture and grade synthetic outputs, without live agent calls.

Expected records, digest, and feasibility examples are independent of fixture
implementation. Instrumented unit calls check measurement boundaries; the
unmodified probe also runs in a real isolated subprocess without a fixed peak.
Repeated measurements qualify only this interpreter; twofold headroom is a
fixture-qualification gate, not an application requirement or an agent bound.
Contract isolation additionally requires semantic review of all supplied text.
Evaluator controls use test-owned records, not fixture calculations or grader
constants. They do not authenticate measurements or test the human judgments.
"""

import base64
from contextlib import redirect_stderr, redirect_stdout
import hashlib
from io import StringIO
import json
from pathlib import Path
from threading import Event
import unittest
from unittest.mock import patch

from evaluation import __main__ as cli
from evaluation.__main__ import CANDIDATE_PATH
from engine.runtime.evaluation import ExecutionResult
from engine.runtime.workspace import WorkspaceObservation, snapshot_workspace
from conformance import inquiry
from conformance import inquiry as case
from evaluation.tests.support.cli_harness import FakeCodexCLI


from conformance.tests.inquiry_data import VALID_FEASIBILITY


class InquiryCLITests(FakeCodexCLI, unittest.TestCase):
    def test_inquiry_selection_uses_accepted_composition_and_retains_review_evidence(self):
        selected = next(case for case in cli.registered_cases(CANDIDATE_PATH.read_bytes) if case.name == "bounded-inquiry")
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
        contract = CANDIDATE_PATH.read_bytes()
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
        selected = next(case for case in cli.registered_cases(CANDIDATE_PATH.read_bytes) if case.name == "bounded-inquiry")
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
                    code = cli.run_case(selected, read_contract=CANDIDATE_PATH.read_bytes, model="test-model", effort="medium", timeout=10,
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


if __name__ == "__main__":
    unittest.main()
