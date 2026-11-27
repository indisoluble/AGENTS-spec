"""Offline fixture qualification and grading of synthetic customer-report reviews.

Independent literal outputs establish the complete null/empty-string collision
and ordinary reporting behavior. Synthetic results exercise mechanical grading
without real agents; document adequacy and other meaning remain human judgments.
"""

import base64
from contextlib import redirect_stderr, redirect_stdout
import hashlib
from io import StringIO
import json
from pathlib import Path
import re
from threading import Event
import unittest
from unittest.mock import patch

from evaluation import __main__ as cli
from evaluation.__main__ import CANDIDATE_PATH
from engine.runtime.evaluation import ExecutionResult
from conformance import findings
from conformance import findings as case
from evaluation.tests.support.cli_harness import FakeCodexCLI


class FindingsCLITests(FakeCodexCLI, unittest.TestCase):
    def test_registration_uses_approved_dataset_fixture_and_rubric(self):
        from evaluation.__main__ import registered_cases

        registered, = [config for config in registered_cases(CANDIDATE_PATH.read_bytes) if config.name == "durable-finding-review"]
        self.assertIs(registered.dataset_factory.func, case.findings_dataset)
        self.assertIs(registered.fixture_files, case.FIXTURE_FILES)
        self.assertEqual(registered.review_rubric, case.REVIEW_RUBRIC)
        self.assertTrue(registered.observe_workspace)
        self.assertIsNone(registered.check_execution)
        self.assertEqual(registered.dataset_factory().cases[0].name, "customer-csv-reconstruction")


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
        contract = CANDIDATE_PATH.read_bytes()
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
        selected = next(case for case in cli.registered_cases(CANDIDATE_PATH.read_bytes) if case.name == "durable-finding-review")
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
            code = cli.run_case(selected, read_contract=CANDIDATE_PATH.read_bytes, model="test-model", effort="medium", timeout=10,
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
