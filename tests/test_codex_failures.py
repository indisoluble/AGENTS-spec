"""Exercise real CLI orchestration and OS signals with a fake Codex process only."""

import base64
from contextlib import redirect_stderr, redirect_stdout
import hashlib
from io import StringIO
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Event
import time
import unittest
from unittest.mock import patch

from evals.auth import PROFILE_CONFIG
from evals.guidance import FIXTURE_FILES, REVIEW_RUBRIC
from evals import __main__ as cli
from evals import assumptions, followthrough, independence, inquiry, material_growth, permissions, scheduling
from evals.evaluation import ExecutionResult
from evals.functional import FunctionalCheckResult
from evals.workspace import CONTRACT_PATH, WorkspaceObservation, snapshot_workspace
from tests.test_followthrough import correct_edit
from tests.test_inquiry import VALID_FEASIBILITY


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
        if process is not None:
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
                 "missing-permission", "no-safe-next-step", "contract-change-followthrough", "bounded-inquiry",
                 "material-growth-handoff-b", "material-growth-handoff-c")
        rubrics = {"requester-guidance": REVIEW_RUBRIC, "independent-execution": independence.REVIEW_RUBRIC,
                   "assumption-disclosure": assumptions.REVIEW_RUBRIC,
                   "missing-permission": permissions.REVIEW_RUBRIC,
                   "no-safe-next-step": scheduling.REVIEW_RUBRIC,
                   "contract-change-followthrough": followthrough.REVIEW_RUBRIC,
                   "bounded-inquiry": inquiry.REVIEW_RUBRIC,
                   "material-growth-handoff-b": material_growth.REVIEW_RUBRIC,
                   "material-growth-handoff-c": material_growth.REVIEW_RUBRIC_C}
        for smoke, scope, guidance, expected_exit, outcomes in scenarios:
            with self.subTest(smoke=smoke, scope=scope, guidance=guidance):
                # Select deterministic responses for each fake task, without model calls.
                process, profile, runs = self.launch(
                    {"smoke": smoke, "scope-discipline": scope, "requester-guidance": guidance,
                     "independent-execution": "success", "assumption-disclosure": "success",
                     "missing-permission": "success", "no-safe-next-step": "success",
                     "contract-change-followthrough": "success", "bounded-inquiry": "success",
                     "material-growth-handoff-b": "success", "material-growth-handoff-c": "success"}, case="all",
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
                for name, outcome in zip(names, [*outcomes, *(["review_required"] * 8)]):
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
                before = by_case["material-growth-handoff-b"]
                budgeted = by_case["material-growth-handoff-c"]
                self.assertNotEqual(before, budgeted)
                self.assertEqual((before / "prompt.txt").read_text(), material_growth.PROMPT)
                self.assertEqual((budgeted / "prompt.txt").read_text(), material_growth.PROMPT_C)
                for name in ("AGENTS.md", *material_growth.FIXTURE_FILES):
                    self.assertEqual((before / "initial-workspace" / name).read_bytes(),
                                     (budgeted / "initial-workspace" / name).read_bytes())
                first = json.loads((before / "execution.json").read_text())
                second = json.loads((budgeted / "execution.json").read_text())
                for key in ("model", "reasoning_effort", "timeout_seconds", "codex_home", "contract_sha256"):
                    self.assertEqual(first[key], second[key], key)
                commands = []
                for metadata in (first, second):
                    command = list(metadata["command"])
                    for flag in ("--cd", "--output-last-message"):
                        command[command.index(flag) + 1] = f"<{flag}>"
                    commands.append(command)
                self.assertEqual(commands[0], commands[1])

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
                 "material-growth-handoff-b", "material-growth-handoff-c")
        failures = (("missing-permission", "redirected", 1), ("missing-permission", "nonzero", 2),
                    ("no-safe-next-step", "extra-worker", 1), ("no-safe-next-step", "nonzero", 2),
                    ("contract-change-followthrough", "unchanged", 1), ("contract-change-followthrough", "nonzero", 2),
                    ("bounded-inquiry", "incorrect", 1), ("bounded-inquiry", "nonzero", 2),
                    ("material-growth-handoff-b", "contract-edited", 1), ("material-growth-handoff-b", "nonzero", 2),
                    ("material-growth-handoff-c", "contract-edited", 1), ("material-growth-handoff-c", "nonzero", 2))
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

    def test_material_growth_b_selection_retains_evidence_and_requires_human_review(self):
        self.assert_material_growth_evidence(
            "material-growth-handoff-b", material_growth.material_growth_dataset,
            material_growth.PROMPT, material_growth.REVIEW_RUBRIC, "requester-underestimated-repair",
        )

    def test_material_growth_c_selection_retains_evidence_and_requires_human_review(self):
        self.assert_material_growth_evidence(
            "material-growth-handoff-c", material_growth.material_growth_c_dataset,
            material_growth.PROMPT_C, material_growth.REVIEW_RUBRIC_C, "requester-budgeted-repair",
        )

    def assert_material_growth_evidence(self, case_name, dataset_factory, prompt, rubric, instance_name):
        selected = next(case for case in cli.CASES if case.name == case_name)
        self.assertIs(selected.dataset_factory, dataset_factory)
        self.assertIs(selected.fixture_files, material_growth.FIXTURE_FILES)
        self.assertEqual(selected.review_rubric, rubric)
        self.assertTrue(selected.observe_workspace)
        self.assertIsNone(selected.check_execution)

        for scenario in ("success", "application-edit"):
            with self.subTest(scenario=scenario):
                process, profile, runs = self.launch(scenario, case=case_name)
                artifacts, metadata, report = self.finish(process, runs, 3)
                self.assertEqual(report["case"], case_name)
                self.assertEqual(report["outcome"], "review_required")
                self.assertTrue(report["review_required"])
                result, = report["cases"]
                self.assertEqual(result["name"], instance_name)
                self.assertEqual(result["assertions"], {
                    "InitialFixtureIntact": True, "RootContractPreserved": True, "FinalResponsePresent": True,
                })
                self.assertEqual(result["evaluator_errors"], [])
                self.assertEqual(metadata["evidence_errors"], [])
                self.assertIn("--output-last-message", metadata["command"])
                self.assertEqual((artifacts / "prompt.txt").read_text(), prompt)
                self.assertEqual((artifacts / "review.md").read_text(), rubric)
                contract = CONTRACT_PATH.read_bytes()
                self.assertEqual(metadata["contract_sha256"], hashlib.sha256(contract).hexdigest())
                initial = json.loads((artifacts / "initial-workspace.json").read_text())
                final = json.loads((artifacts / "final-workspace.json").read_text())
                supplied = {"AGENTS.md": contract, **material_growth.FIXTURE_FILES}
                self.assertEqual(set(initial), {".", "docs", *supplied})
                self.assertEqual(set(final), set(initial))
                for name, contents in supplied.items():
                    self.assertEqual((artifacts / "initial-workspace" / name).read_bytes(), contents)
                    self.assertEqual(base64.b64decode(initial[name]["contents_base64"]), contents)
                    if scenario == "success" or name != "job_queue.py":
                        self.assertEqual((artifacts / "workspace" / name).read_bytes(), contents)
                        self.assertEqual(initial[name], final[name])
                changes = (artifacts / "workspace-changes.txt").read_text()
                if scenario == "application-edit":
                    self.assertIn('Path: "job_queue.py"', changes)
                else:
                    self.assertEqual(changes, "No observed workspace changes.\n")
                self.assertEqual(result["final_response"], (artifacts / "final-response.txt").read_text())
                # False completion can pass structure; there is no compliance verdict.
                self.assertIn("repair is complete", result["final_response"])
                events = (artifacts / "events.jsonl").read_text()
                self.assertIn("no repair or queue validation", events)
                self.assertIn("test-only inspection event", events)
                self.assertIn("Human review pending", (artifacts / "report.txt").read_text())
                self.assertFalse((artifacts / "functional-checks.json").exists())
                self.assertFalse((artifacts / "checks").exists())
                self.assertEqual((profile / "case-invocations").read_text(), case_name + "\n")
                self.assertEqual((profile / "invocations").read_text(), "exec\n")

    def test_material_growth_b_failures_preserve_classification_and_pending_review(self):
        self.assert_material_growth_failures("material-growth-handoff-b", material_growth.REVIEW_RUBRIC)

    def test_material_growth_c_failures_preserve_classification_and_pending_review(self):
        self.assert_material_growth_failures("material-growth-handoff-c", material_growth.REVIEW_RUBRIC_C)

    def assert_material_growth_failures(self, case_name, rubric):
        for scenario, expected_exit in (("contract-edited", 1), ("empty", 1), ("missing-response", 2), ("nonzero", 2)):
            with self.subTest(scenario=scenario):
                process, _, runs = self.launch(scenario, case=case_name)
                artifacts, _, report = self.finish(process, runs, expected_exit)
                self.assertTrue(report["review_required"])
                self.assertEqual(report["case"], case_name)
                self.assertEqual((artifacts / "review.md").read_text(), rubric)
                if expected_exit == 2:
                    self.assertEqual(report["outcome"], "execution_failed")
                    self.assertEqual(report["cases"], [])
                    self.assertTrue(report["execution_errors"])
                else:
                    self.assertEqual(report["outcome"], "assertion_failed")
                    self.assertEqual(report["cases"][0]["assertions"], {
                        "InitialFixtureIntact": True,
                        "RootContractPreserved": scenario != "contract-edited",
                        "FinalResponsePresent": scenario != "empty",
                    })

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
        run_check = followthrough.run_python_check

        def check_after_cleanup(source, workspace, **kwargs):
            checked_workspaces.append(workspace)
            self.assertTrue(workspace.is_dir())
            self.assert_group_stopped(profile)
            artifacts, = runs.iterdir()
            self.assertEqual((artifacts / "review.md").read_text(), followthrough.REVIEW_RUBRIC)
            self.assertTrue((artifacts / "final-workspace.json").is_file())
            return run_check(source, workspace, **kwargs)

        with (patch.object(cli, "ARTIFACTS_ROOT", runs),
              patch("evals.auth.codex_executable", return_value=str(self.bin / "codex")),
              patch("evals.functional.codex_executable", return_value=str(self.bin / "codex")),
              patch.object(followthrough, "run_python_check", side_effect=check_after_cleanup),
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

        save_json = followthrough.save_json
        for fail_evidence in (False, True):
            with self.subTest(fail_evidence=fail_evidence):
                runs = self.root / f"runs-{fail_evidence}"
                with (patch.object(cli, "ARTIFACTS_ROOT", runs), patch.object(cli, "run_codex", side_effect=execute),
                      patch.object(followthrough, "run_python_check", return_value=
                                   FunctionalCheckResult("error", stdout=b"partial", error="sandbox failed")),
                      patch.object(followthrough, "save_json", side_effect=
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
