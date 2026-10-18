"""Exercise real CLI orchestration and OS signals with a fake Codex process only."""

import base64
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
import unittest

from evals.auth import PROFILE_CONFIG
from evals.guidance import FIXTURE_FILES, REVIEW_RUBRIC
from evals import assumptions, independence, permissions


class CodexFailureTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        source = Path(__file__).with_name("fake_codex.py").read_text()
        executable = self.bin / "codex"
        executable.write_text(f"#!{sys.executable}\n" + source)
        executable.chmod(0o700)
        self.run_count = 0

    def launch(self, scenario, *, timeout=30, missing_cli=False, authenticated=True, case=None):
        self.run_count += 1
        profile = self.root / f"profile-{self.run_count}"
        profile.mkdir()
        (profile / "config.toml").write_text(PROFILE_CONFIG)
        (profile / "scenario").write_text(json.dumps(scenario))
        if authenticated:
            (profile / "auth.json").write_text("dummy credential")
        runs = self.root / f"runs-{self.run_count}"
        # Override only the report location; execute the real command handler in a child
        # so sending Ctrl-C cannot interrupt unittest itself.
        bootstrap = (
            "from pathlib import Path; import sys; import evals.__main__ as cli; "
            "cli.ARTIFACTS_ROOT = Path(sys.argv.pop(1)); raise SystemExit(cli.main())"
        )
        # Fix report width so long assertion names do not wrap across table cells.
        env = dict(os.environ, PATH=str(self.root / "missing" if missing_cli else self.bin), COLUMNS="160")
        case_arguments = [] if case is None else ["--case", case]
        process = subprocess.Popen(
            [sys.executable, "-c", bootstrap, str(runs), "--codex-home", str(profile),
             "--model", "test-model", "--reasoning-effort", "medium", "--timeout", str(timeout),
             *case_arguments],
            cwd=Path(__file__).resolve().parents[1], env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True,
        )
        self.addCleanup(self.cleanup_processes, process, profile)
        return process, profile, runs

    def cleanup_processes(self, process, profile):
        # Even a failing regression must not leave its deliberately sleeping processes alive.
        if (profile / "pids.json").exists():
            parent_pid, _ = json.loads((profile / "pids.json").read_text())
            try:
                os.killpg(parent_pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
        process.communicate(timeout=5)

    def finish(self, process, runs, expected_exit):
        output, errors = process.communicate(timeout=10)
        self.assertEqual(process.returncode, expected_exit, output + errors)
        artifacts, = runs.iterdir()
        metadata = json.loads((artifacts / "execution.json").read_text())
        report = json.loads((artifacts / "report.json").read_text())
        self.assertFalse(Path(metadata["workspace"]).exists())
        self.assertTrue((artifacts / "AGENTS.md").is_file())
        self.assertTrue((artifacts / "prompt.txt").is_file())
        return artifacts, metadata, report

    def assert_group_stopped(self, profile):
        for pid in json.loads((profile / "pids.json").read_text()):
            inspection = subprocess.run(
                ["/bin/ps", "-o", "stat=", "-p", str(pid)],
                capture_output=True, text=True, timeout=2,
            )
            # ps returns 1 for a vanished PID. An inspection error must not pass silently.
            self.assertIn(inspection.returncode, (0, 1), inspection.stderr)
            self.assertEqual(inspection.stderr, "")
            state = inspection.stdout.strip()
            # A killed orphan can briefly remain as an OS-owned zombie awaiting reaping.
            self.assertTrue(not state or state.startswith("Z"), f"Process {pid} still running: {state}")

    def test_missing_cli_returns_two_with_evidence_and_clean_workspace(self):
        process, profile, runs = self.launch("success", missing_cli=True)
        _, metadata, report = self.finish(process, runs, 2)
        self.assertIn("Codex CLI was not found on PATH", metadata["error"])
        self.assertEqual(report["outcome"], "execution_failed")
        self.assertEqual(report["case"], "smoke")
        self.assertFalse((profile / "invocations").exists())

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
                 "missing-permission")
        rubrics = {"requester-guidance": REVIEW_RUBRIC, "independent-execution": independence.REVIEW_RUBRIC,
                   "assumption-disclosure": assumptions.REVIEW_RUBRIC,
                   "missing-permission": permissions.REVIEW_RUBRIC}
        for smoke, scope, guidance, expected_exit, outcomes in scenarios:
            with self.subTest(smoke=smoke, scope=scope, guidance=guidance):
                # Select deterministic responses for each fake task, without model calls.
                process, profile, runs = self.launch(
                    {"smoke": smoke, "scope-discipline": scope, "requester-guidance": guidance,
                     "independent-execution": "success", "assumption-disclosure": "success",
                     "missing-permission": "success"}, case="all",
                )
                output, errors = process.communicate(timeout=15)
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
                for name, outcome in zip(names, [*outcomes, "review_required", "review_required", "review_required"]):
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

    def test_permission_failure_at_end_of_all_cases_takes_precedence_over_pending_review(self):
        names = ("smoke", "scope-discipline", "requester-guidance", "independent-execution", "assumption-disclosure",
                 "missing-permission")
        for scenario, expected_exit in (("redirected", 1), ("nonzero", 2)):
            with self.subTest(scenario=scenario):
                scenarios = dict.fromkeys(names, "success")
                scenarios["missing-permission"] = scenario
                process, profile, runs = self.launch(scenarios, case="all")
                output, errors = process.communicate(timeout=15)
                self.assertEqual(process.returncode, expected_exit, output + errors)
                self.assertEqual((profile / "case-invocations").read_text(), "\n".join(names) + "\n")
                self.assertEqual(len(list(runs.iterdir())), len(names))
                for artifacts in runs.iterdir():
                    report = json.loads((artifacts / "report.json").read_text())
                    metadata = json.loads((artifacts / "execution.json").read_text())
                    self.assertFalse(Path(metadata["workspace"]).exists())
                    self.assertEqual(report["review_required"], report["case"] not in names[:2])
                    if report["case"] == "missing-permission":
                        self.assertEqual(report["outcome"], "assertion_failed" if expected_exit == 1 else "execution_failed")

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

    def test_guidance_replies_and_edits_are_retained_for_human_review(self):
        scenarios = (("success", None), ("misleading", None), ("proposal", "timezone-note.md"),
                     ("implementation", "exporter.py"), ("data-change", "events.json"), ("policy", "README.md"))
        for scenario, changed_path in scenarios:
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="requester-guidance")
                artifacts, metadata, report = self.finish(process, runs, 3)
                self.assertEqual(report["outcome"], "review_required")
                self.assertTrue(report["review_required"])
                self.assertEqual(report["cases"][0]["assertions"], {
                    "FinalResponsePresent": True, "RootContractPreserved": True,
                })
                response = (artifacts / "final-response.txt").read_text()
                self.assertEqual(report["cases"][0]["final_response"], response)
                self.assertNotIn("Progress message", response)
                self.assertIn("Progress message", (artifacts / "events.jsonl").read_text())
                self.assertIn("--output-last-message", metadata["command"])
                self.assertEqual((artifacts / "review.md").read_text(), REVIEW_RUBRIC)
                initial = json.loads((artifacts / "initial-workspace.json").read_text())
                final = json.loads((artifacts / "final-workspace.json").read_text())
                for name, contents in FIXTURE_FILES.items():
                    self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
                    self.assertEqual(base64.b64decode(initial[name]["contents_base64"]), contents)
                for name, entry in final.items():
                    if entry["kind"] == "file":
                        self.assertEqual((artifacts / "workspace" / name).read_bytes(),
                                         base64.b64decode(entry["contents_base64"]))
                changes = (artifacts / "workspace-changes.txt").read_text()
                if changed_path is None:
                    self.assertEqual(changes, "No observed workspace changes.\n")
                else:
                    self.assertIn(f'Path: "{changed_path}"', changes)
                self.assertNotIn("review.md", initial)
                self.assertNotIn("final-response.txt", final)
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

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

    def test_guidance_assertion_failures_keep_independent_results(self):
        for scenario in ("empty", "whitespace", "contract-edited", "contract-deleted", "contract-link", "contract-mode"):
            with self.subTest(scenario=scenario):
                process, _, runs = self.launch(scenario, case="requester-guidance")
                artifacts, metadata, report = self.finish(process, runs, 1)
                contract_changed = scenario.startswith("contract-")
                self.assertEqual(report["cases"][0]["assertions"], {
                    "FinalResponsePresent": contract_changed, "RootContractPreserved": not contract_changed,
                })
                self.assertTrue(report["review_required"])
                self.assertEqual(metadata["status"], "completed")
                self.assertEqual(metadata["evidence_errors"], [])
                self.assertTrue((artifacts / "workspace-changes.txt").is_file())
                if contract_changed:
                    self.assertIn("AGENTS.md:", report["cases"][0]["assertion_reasons"]["RootContractPreserved"])

    def test_guidance_capture_and_execution_failures_are_errors_with_available_evidence(self):
        for scenario in ("missing-response", "invalid-utf8", "nonzero"):
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case="requester-guidance")
                artifacts, metadata, report = self.finish(process, runs, 2)
                self.assertEqual(report["case"], "requester-guidance")
                self.assertEqual(report["outcome"], "execution_failed")
                self.assertEqual(report["cases"], [])
                self.assertTrue(report["review_required"])
                self.assertIn("Final response capture failed", metadata["error"])
                if scenario == "nonzero":
                    self.assertIn("Codex exited with status 7", metadata["error"])
                self.assertEqual((artifacts / "review.md").read_text(), REVIEW_RUBRIC)
                self.assertTrue((artifacts / "initial-workspace.json").is_file())
                self.assertTrue((artifacts / "final-workspace.json").is_file())
                self.assertTrue((artifacts / "workspace-changes.txt").is_file())
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

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


if __name__ == "__main__":
    unittest.main()
