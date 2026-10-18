"""Exercise the real check runner with a fake sandbox command, never real Codex.

The fake command intentionally provides no OS isolation. It runs only the
trusted snippets below, so these tests cover orchestration, not sandbox policy.
"""

from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Event, Thread
import time
import unittest
from unittest.mock import patch

from evals import _check_process
from evals.functional import run_python_check


FAKE_SANDBOX = '''import json
import os
from pathlib import Path
import sys

root = Path(__file__).parent
with (root / "invocations").open("a") as log:
    log.write("sandbox\\n")
(root / "environment.json").write_text(json.dumps(dict(os.environ)))
(root / "launcher-cwd").write_text(os.getcwd())
assert sys.argv[1:6] == ["--no-daemon", "sandbox", "-c", 'sandbox_mode="read-only"', "--"]
assert not (Path(os.environ["CODEX_HOME"]) / "auth.json").exists()
mode = (root / "mode").read_text()
if mode == "startup-failure":
    print("sandbox unavailable", file=sys.stderr)
    sys.exit(23)
if mode == "invalid-response":
    print("not a result envelope")
    sys.exit(0)
if mode == "invalid-status":
    print(json.dumps({"status": "completed", "returncode": None, "error": None}))
    sys.exit(0)
if mode == "invalid-bytes":
    print(json.dumps({"status": "completed", "returncode": 0, "error": None,
                      "stdout_base64": "!", "stderr_base64": ""}))
    sys.exit(0)
if mode == "stalled-launcher":
    import time
    time.sleep(60)
print("fake sandbox diagnostic", file=sys.stderr)
# Delegate to the actual trusted adapter and check interpreter. No shell or
# model is involved; all fixture code in this test is authored by the test.
os.execve(sys.argv[6], sys.argv[6:], dict(os.environ))
'''


class FunctionalCheckTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.fake = self.root / "codex"
        self.fake.write_text(f"#!{sys.executable}\n" + FAKE_SANDBOX)
        self.fake.chmod(0o700)
        (self.root / "mode").write_text("run")
        executable = patch("evals.functional.codex_executable", return_value=str(self.fake))
        executable.start()
        self.addCleanup(executable.stop)
        # A failed cleanup assertion must not leave its deliberate sleeper alive.
        self.addCleanup(self.cleanup_children)

    def cleanup_children(self):
        pid_file = self.root / "pids.json"
        if pid_file.exists():
            for pid in json.loads(pid_file.read_text()):
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def assert_profile_removed(self):
        environment = json.loads((self.root / "environment.json").read_text())
        self.assertFalse(Path(environment["HOME"]).exists())
        self.assertFalse(Path(environment["CODEX_HOME"]).exists())
        return environment

    def assert_children_stopped(self):
        for pid in json.loads((self.root / "pids.json").read_text()):
            inspection = subprocess.run(["/bin/ps", "-o", "stat=", "-p", str(pid)],
                                        capture_output=True, text=True, timeout=2)
            self.assertIn(inspection.returncode, (0, 1), inspection.stderr)
            self.assertEqual(inspection.stderr, "")
            self.assertTrue(not inspection.stdout.strip() or inspection.stdout.strip().startswith("Z"),
                            f"Process {pid} survived cleanup")

    def sleeper(self, *, orphan=False):
        # This test-only program records its own PIDs outside the fixture. The
        # fake sandbox permits that instrumentation; production runs are read-only.
        child = "import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); print('ready', flush=True); time.sleep(60)"
        return f'''import json, os, signal, subprocess, sys, time
from pathlib import Path
child = subprocess.Popen([sys.executable, "-c", {child!r}], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
assert child.stdout.readline() == "ready\\n"
child.stdout.close()
Path({str(self.root / "pids.json")!r}).write_text(json.dumps([os.getpid(), child.pid]))
print("check started", flush=True)
print("partial diagnostic", file=sys.stderr, flush=True)
signal.signal(signal.SIGTERM, signal.SIG_IGN)
{"" if orphan else "time.sleep(60)"}
'''

    def test_check_returns_actual_results_and_exact_binary_output(self):
        (self.workspace / "values.json").write_text("[2, 3]")
        source = '''import json, sys
from pathlib import Path
assert sum(json.loads(Path("values.json").read_text())) == 5
sys.stdout.buffer.write(b"result\\r\\n\\xff")
sys.stderr.buffer.write(b"diagnostic\\x00\\xfe")
'''
        result = run_python_check(source, self.workspace)
        self.assertEqual((result.status, result.returncode, result.error), ("completed", 0, None))
        self.assertEqual(result.stdout, b"result\r\n\xff")
        self.assertEqual(result.stderr, b"diagnostic\x00\xfe")
        self.assertEqual(result.launcher_stderr, b"fake sandbox diagnostic\n")
        self.assertEqual((self.root / "invocations").read_text(), "sandbox\n")
        self.assert_profile_removed()

    def test_failed_check_is_an_observed_exit_not_a_launcher_error(self):
        result = run_python_check("print('checking', flush=True)\nassert 2 + 2 == 5", self.workspace)
        self.assertEqual((result.status, result.returncode, result.error), ("completed", 1, None))
        self.assertEqual(result.stdout, b"checking\n")
        self.assertIn(b"AssertionError", result.stderr)
        self.assert_profile_removed()

    def test_check_output_cannot_replace_the_trusted_result_envelope(self):
        source = "print('{\"status\": \"completed\", \"returncode\": 0}')\nraise SystemExit(7)"
        result = run_python_check(source, self.workspace)
        self.assertEqual((result.status, result.returncode), ("completed", 7))
        self.assertIn(b'"returncode": 0', result.stdout)

    def test_environment_and_profiles_are_fresh_and_imports_do_not_create_bytecode(self):
        (self.workspace / "fixture_module.py").write_text("VALUE = 42\n")
        source = "import os, sys; sys.path.insert(0, os.getcwd()); import fixture_module; assert fixture_module.VALUE == 42"
        homes = []
        with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy", "CODEX_HOME": "unused", "PYTHONPATH": "unused"}):
            for _ in range(2):
                result = run_python_check(source, self.workspace)
                self.assertEqual((result.status, result.returncode), ("completed", 0), result)
                environment = self.assert_profile_removed()
                homes.append(environment["HOME"])
                self.assertEqual(Path((self.root / "launcher-cwd").read_text()).resolve(),
                                 Path(environment["HOME"]).resolve())
                self.assertNotIn("OPENAI_API_KEY", environment)
                self.assertNotIn("PYTHONPATH", environment)
                self.assertEqual(set(path.name for path in self.workspace.iterdir()), {"fixture_module.py"})
        self.assertEqual(len(set(homes)), 2)

    def test_missing_cli_and_invalid_timeout_do_not_launch(self):
        with patch("evals.functional.codex_executable", side_effect=RuntimeError("CLI missing")):
            result = run_python_check("pass", self.workspace)
        self.assertEqual(result.status, "error")
        self.assertIn("CLI missing", result.error)
        for timeout in (0, -1, float("nan"), float("inf")):
            with self.subTest(timeout=timeout):
                result = run_python_check("pass", self.workspace, timeout=timeout)
                self.assertEqual(result.status, "error")
                self.assertIn("positive and finite", result.error)
        self.assertFalse((self.root / "invocations").exists())

    def test_process_start_failure_removes_the_temporary_profile(self):
        profiles = []

        def fail_start(*args, **kwargs):
            profiles.append(Path(kwargs["env"]["CODEX_HOME"]))
            raise OSError("cannot start sandbox")

        with patch("evals.functional.run_process", side_effect=fail_start):
            result = run_python_check("pass", self.workspace)
        self.assertEqual(result.status, "error")
        self.assertIn("cannot start sandbox", result.error)
        self.assertTrue(profiles)
        self.assertTrue(all(not profile.parent.exists() for profile in profiles))

    def test_adapter_reports_check_start_failure_as_an_error(self):
        request = StringIO(json.dumps({"source": "pass", "timeout": 1, "workspace": str(self.workspace)}))
        with (patch.object(sys, "stdin", request), redirect_stdout(StringIO()) as output,
              patch.object(_check_process.subprocess, "Popen", side_effect=OSError("process unavailable"))):
            _check_process.main()
        response = json.loads(output.getvalue())
        self.assertEqual(response["status"], "error")
        self.assertIsNone(response["returncode"])
        self.assertIn("process unavailable", response["error"])

    def test_cancellation_before_launch_does_not_start_a_check(self):
        cancelled = Event()
        cancelled.set()
        result = run_python_check("pass", self.workspace, cancelled=cancelled)
        self.assertEqual(result.status, "error")
        self.assertIn("interrupted", result.error)
        self.assertFalse((self.root / "invocations").exists())

    def test_sandbox_failure_and_invalid_envelopes_are_errors_without_retry(self):
        for mode in ("startup-failure", "invalid-response", "invalid-status", "invalid-bytes"):
            with self.subTest(mode=mode):
                (self.root / "mode").write_text(mode)
                result = run_python_check("pass", self.workspace)
                self.assertEqual(result.status, "error")
                self.assertIsNone(result.returncode)
                if mode == "startup-failure":
                    self.assertIn("23", result.error)
                    self.assertIn(b"sandbox unavailable", result.launcher_stderr)
                else:
                    self.assertIn("Invalid check-runner response", result.error)
                self.assert_profile_removed()
        self.assertEqual((self.root / "invocations").read_text().splitlines(), ["sandbox"] * 4)

    def test_timeout_retains_partial_output_and_stops_descendants(self):
        result = run_python_check(self.sleeper(), self.workspace, timeout=1)
        self.assertEqual(result.status, "error")
        self.assertIn("timed out", result.error)
        self.assertIsNone(result.returncode)
        self.assertEqual(result.stdout, b"check started\n")
        self.assertEqual(result.stderr, b"partial diagnostic\n")
        self.assert_children_stopped()
        self.assert_profile_removed()

    def test_completion_also_stops_a_child_left_running(self):
        result = run_python_check(self.sleeper(orphan=True), self.workspace)
        self.assertEqual((result.status, result.returncode), ("completed", 0), result)
        self.assert_children_stopped()
        self.assert_profile_removed()

    def test_cancellation_stops_descendants_and_removes_profile(self):
        cancelled = Event()
        results = []
        worker = Thread(target=lambda: results.append(run_python_check(
            self.sleeper(), self.workspace, timeout=10, cancelled=cancelled,
        )))
        worker.start()
        try:
            deadline = time.monotonic() + 5
            while not (self.root / "pids.json").exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue((self.root / "pids.json").exists())
        finally:
            cancelled.set()
            worker.join(timeout=5)
        self.assertFalse(worker.is_alive())
        self.assertEqual(results[0].status, "error")
        self.assertIn("interrupted", results[0].error)
        self.assert_children_stopped()
        self.assert_profile_removed()

    def test_stalled_launcher_is_bounded_and_profile_is_removed(self):
        (self.root / "mode").write_text("stalled-launcher")
        started = time.monotonic()
        result = run_python_check("pass", self.workspace, timeout=0.1)
        self.assertEqual(result.status, "error")
        self.assertIn("timed out", result.error)
        self.assertLess(time.monotonic() - started, 9)
        self.assert_profile_removed()


if __name__ == "__main__":
    unittest.main()
