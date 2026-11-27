"""Grade predetermined scheduling edits without Codex, credentials, or models.

Only the original, test-owned inspector runs here to verify scenario feasibility.
Agent-edited code is never executed by this case's evaluators.
"""

import base64
import json
import unittest

from conformance import scheduling
from evaluation.tests.support.cli_harness import FakeCodexCLI


class SchedulingCLITests(FakeCodexCLI, unittest.TestCase):
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


