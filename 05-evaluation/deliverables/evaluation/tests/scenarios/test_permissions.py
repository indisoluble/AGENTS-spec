"""Grade known cleanup results without real Codex, credentials, or model calls.

Substitutes modify disposable fixtures. Replies demonstrate that semantic
judgments stay with humans, not that these tests can recognize good requests.
"""

import base64
import json
import unittest

from conformance import permissions
from evaluation.tests.support.cli_harness import FakeCodexCLI


class PermissionCLITests(FakeCodexCLI, unittest.TestCase):
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


