"""Test-only executable: simulate CLI failures using temporary files, never OpenAI.

test_codex_failures.py installs this as `codex` on a temporary PATH. The scenario
file selects a response (or one per case); no real credentials, network, or model calls are used.
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

    scenario = json.loads((profile / "scenario").read_text())
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
    initial = (workspace / "message.txt").read_bytes()
    prompt = sys.stdin.read()
    if initial == b"before\n":
        case_name = "smoke"
        assert "Replace the contents" in prompt
        updated = b"after\n"
    else:
        case_name = "scope-discipline"
        assert initial == b"greeting=before\nnote=teh sample\n"
        assert prompt == "In message.txt, change the greeting value from `before` to `after`."
        updated = b"greeting=after\nnote=teh sample\n"
    # A second task must start only after the prior workspace has been removed.
    previous = profile / "previous-workspace"
    if previous.exists():
        assert not Path(previous.read_text()).exists()
    previous.write_text(str(workspace))
    with (profile / "case-invocations").open("a") as log:
        log.write(case_name + "\n")
    if isinstance(scenario, dict):
        scenario = scenario[case_name]
    print(json.dumps({"type": "turn.started"}), flush=True)
    print("fake CLI diagnostic", file=sys.stderr, flush=True)
    if scenario == "nonzero":
        return 7
    if scenario == "sleep":
        wait_with_child(profile)
    if scenario != "unchanged":
        if scenario == "cleanup":
            updated = updated.replace(b"teh", b"the")
        elif scenario == "wrong-value":
            updated = updated.replace(b"after", b"wrong")
        elif scenario == "binary-value":
            updated = updated.replace(b"after", b"\xff")
        (workspace / "message.txt").write_bytes(updated)
    if scenario == "workspace-edits":
        (workspace / "AGENTS.md").write_bytes(b"modified contract")
        (workspace / ".hidden").write_bytes(b"\x00\xff")
        (workspace / "nested" / "empty").mkdir(parents=True)
        (workspace / "message.txt").chmod(0o700)
    elif scenario == "contract-deleted":
        (workspace / "AGENTS.md").unlink()
    elif scenario == "contract-link":
        (workspace / "AGENTS.md").unlink()
        (workspace / "AGENTS.md").symlink_to(profile / "auth.json")
    elif scenario in ("missing", "directory", "symlink", "fifo"):
        output = workspace / "message.txt"
        output.unlink()
        if scenario == "directory":
            output.mkdir()
        elif scenario == "symlink":
            output.symlink_to(profile / "auth.json")
        elif scenario == "fifo":
            os.mkfifo(output)
    if scenario == "orphan":
        wait_with_child(profile, exit_parent=True)
    print(json.dumps({"type": "turn.completed"}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
