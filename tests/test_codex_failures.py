"""Exercise real CLI orchestration and OS signals with a fake Codex process only."""

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

    def launch(self, scenario, *, timeout=30, missing_cli=False, authenticated=True):
        self.run_count += 1
        profile = self.root / f"profile-{self.run_count}"
        profile.mkdir()
        (profile / "config.toml").write_text(PROFILE_CONFIG)
        (profile / "scenario").write_text(scenario)
        if authenticated:
            (profile / "auth.json").write_text("dummy credential")
        runs = self.root / f"runs-{self.run_count}"
        # Override only the report location; execute the real command handler in a child
        # so sending Ctrl-C cannot interrupt unittest itself.
        bootstrap = (
            "from pathlib import Path; import sys; import evals.__main__ as cli; "
            "cli.ARTIFACTS_ROOT = Path(sys.argv.pop(1)); raise SystemExit(cli.main())"
        )
        env = dict(os.environ, PATH=str(self.root / "missing" if missing_cli else self.bin))
        process = subprocess.Popen(
            [sys.executable, "-c", bootstrap, str(runs), "--codex-home", str(profile),
             "--model", "test-model", "--reasoning-effort", "medium", "--timeout", str(timeout)],
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
        self.assertFalse((profile / "invocations").exists())

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
        scenarios = (("sleep", signal.SIGINT), ("sleep", signal.SIGTERM),
                     ("sleep-version", signal.SIGINT), ("sleep-auth", signal.SIGINT))
        for scenario, sig in scenarios:
            with self.subTest(scenario=scenario, signal=sig):
                process, profile, runs = self.launch(scenario)
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

    def test_success_cleans_up_a_child_that_outlives_its_parent(self):
        process, profile, runs = self.launch("orphan")
        _, _, report = self.finish(process, runs, 0)
        self.assertEqual(report["outcome"], "passed")
        self.assert_group_stopped(profile)


if __name__ == "__main__":
    unittest.main()
