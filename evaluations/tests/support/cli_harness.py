"""Run the real CLI against fake_codex.py in a child process; never real Codex or OpenAI.

Mix FakeCodexCLI into a unittest.TestCase. It defines no tests, so it adds none to discovery.
"""

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
from tempfile import TemporaryDirectory

from evaluations.runtime.auth import PROFILE_CONFIG


class FakeCodexCLI:
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
            "from pathlib import Path; import sys; import evaluations.__main__ as cli; "
            "cli.ARTIFACTS_ROOT = Path(sys.argv.pop(1)); raise SystemExit(cli.main())"
        )
        # Fix report width so long assertion names do not wrap across table cells.
        env = dict(os.environ, PATH=str(self.root / "missing" if missing_cli else self.bin), COLUMNS="160")
        case_arguments = [] if case is None else ["--case", case]
        process = subprocess.Popen(
            [sys.executable, "-c", bootstrap, str(runs), "--codex-home", str(profile),
             "--model", "test-model", "--reasoning-effort", "medium", "--timeout", str(timeout),
             *case_arguments],
            cwd=Path(__file__).resolve().parents[3], env=env,
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
