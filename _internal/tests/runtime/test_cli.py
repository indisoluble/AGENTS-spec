"""Exercise real CLI orchestration and OS signals with a fake Codex process only."""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
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
from tests.support.cli_harness import FakeCodexCLI


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
