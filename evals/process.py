"""Own subprocess lifetimes and cancellation across Pydantic's worker thread.

The CLI installs signal handlers; workers observe the shared event. Cleanup stays
with the code that launched each process. See META-EVALUATIONS.md for guarantees.
"""

from collections.abc import Iterator
from contextlib import contextmanager
import os
from pathlib import Path
import signal
import subprocess
from threading import Event
import time
from typing import TextIO


class ExecutionInterrupted(RuntimeError):
    """A cancellation request stopped execution before a result was available."""


@contextmanager
def cancellation_signals() -> Iterator[Event]:
    """Install on the main thread; restore the caller's handlers on exit."""
    cancelled = Event()

    def request_cancellation(signum, frame):
        # Raising KeyboardInterrupt here would not interrupt Pydantic's worker.
        cancelled.set()

    previous = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM)}
    try:
        for sig in previous:
            signal.signal(sig, request_cancellation)
        yield cancelled
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def stop_process_group(process: subprocess.Popen) -> None:
    """Stop the parent and children, including children outliving the parent."""
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        pass
    finally:
        # A child may ignore TERM even when its parent has already exited.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def run_process(
    command: list[str], *, cwd: Path, env: dict[str, str], timeout: float,
    cancelled: Event | None = None, input_text: str | None = None,
    stdout: TextIO | int = subprocess.PIPE, stderr: TextIO | int = subprocess.PIPE,
) -> subprocess.CompletedProcess[str]:
    """Run once with a deadline; capture output or stream it to evidence files."""
    if cancelled is not None and cancelled.is_set():
        raise ExecutionInterrupted("Evaluation interrupted")
    deadline = time.monotonic() + timeout
    with subprocess.Popen(
        command, cwd=cwd, env=env, text=True, start_new_session=True,
        stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
        stdout=stdout, stderr=stderr,
    ) as process:
        try:
            while True:
                if cancelled is not None and cancelled.is_set():
                    raise ExecutionInterrupted("Evaluation interrupted")
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(command, timeout)
                try:
                    output, errors = process.communicate(input=input_text, timeout=min(0.1, remaining))
                except subprocess.TimeoutExpired:
                    # communicate resumes buffered input/output; this does not relaunch Codex.
                    input_text = None
                    continue
                if cancelled is not None and cancelled.is_set():
                    raise ExecutionInterrupted("Evaluation interrupted")
                return subprocess.CompletedProcess(command, process.returncode, output, errors)
        finally:
            stop_process_group(process)
