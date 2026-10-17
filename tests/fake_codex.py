"""Test-only executable: simulate CLI failures using temporary files, never OpenAI.

test_codex_failures.py installs this as `codex` on a temporary PATH. The scenario
file selects a response; no real credentials, network, or model calls are used.
"""

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def wait_with_child(profile: Path, *, exit_parent: bool = False) -> None:
    """Leave a TERM-resistant child so tests can verify whole-group cleanup."""
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    child = subprocess.Popen(
        [sys.executable, __file__, "--fake-child"],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    deadline = time.monotonic() + 5
    while not (profile / "child-ready").exists():
        if child.poll() is not None or time.monotonic() >= deadline:
            raise RuntimeError("Fake child did not start")
        time.sleep(0.01)
    (profile / "pids.json").write_text(json.dumps([os.getpid(), child.pid]))
    if not exit_parent:
        time.sleep(60)


def main() -> int:
    profile = Path(os.environ["CODEX_HOME"])
    if "--fake-child" in sys.argv:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        (profile / "child-ready").touch()
        time.sleep(60)
        return 0

    scenario = (profile / "scenario").read_text()
    if "--version" in sys.argv:
        if scenario == "sleep-version":
            wait_with_child(profile)
        print("codex-cli test")
        return 0
    if "login" in sys.argv:
        if scenario == "sleep-auth":
            wait_with_child(profile)
        if not (profile / "auth.json").exists():
            print("Not logged in", file=sys.stderr)
            return 1
        print("Logged in using an API key" if scenario == "api-auth" else "Logged in using ChatGPT")
        return 0

    # Record each invocation to detect retries. Check the real fixture and input.
    with (profile / "invocations").open("a") as log:
        log.write("exec\n")
    workspace = Path(sys.argv[sys.argv.index("--cd") + 1])
    assert (workspace / "message.txt").read_bytes() == b"before\n"
    assert "Replace the contents" in sys.stdin.read()
    print(json.dumps({"type": "turn.started"}), flush=True)
    print("fake CLI diagnostic", file=sys.stderr, flush=True)
    if scenario == "nonzero":
        return 7
    if scenario == "sleep":
        wait_with_child(profile)
    if scenario != "unchanged":
        (workspace / "message.txt").write_bytes(b"after\n")
    if scenario == "orphan":
        wait_with_child(profile, exit_parent=True)
    print(json.dumps({"type": "turn.completed"}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
