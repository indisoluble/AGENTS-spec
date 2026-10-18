"""Run evaluator-owned Python checks without a model call or saved credentials.

Used by the independent-execution case. See META-EVALUATIONS.md#functional-check-execution
for its result contract, sandbox boundary, and timeout behavior.
"""

import base64
from dataclasses import dataclass
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Event
from typing import Literal

from evals.auth import codex_executable
from evals.process import run_process


@dataclass(frozen=True)
class FunctionalCheckResult:
    # Completed means the check ran, including when it returned a nonzero status.
    # The case, not this process owner, interprets its output as assertions.
    status: Literal["completed", "error"]
    returncode: int | None = None
    stdout: bytes = b""
    stderr: bytes = b""
    error: str | None = None
    launcher_stderr: bytes = b""


def _decode_result(completed: subprocess.CompletedProcess[str]) -> FunctionalCheckResult:
    """Separate sandbox startup failure from a check that actually ran."""
    diagnostics = completed.stderr.encode("utf-8")
    if completed.returncode:
        return FunctionalCheckResult(
            "error", error=f"Sandbox launcher exited with status {completed.returncode}; response: {completed.stdout!r}",
            launcher_stderr=diagnostics,
        )
    try:
        payload = json.loads(completed.stdout)
        status, returncode, error = payload["status"], payload["returncode"], payload["error"]
        if status == "completed":
            valid = type(returncode) is int and error is None
        else:
            valid = status == "error" and returncode is None and isinstance(error, str) and bool(error)
        if not valid:
            raise ValueError("inconsistent check status")
        result = FunctionalCheckResult(
            status, returncode,
            base64.b64decode(payload["stdout_base64"], validate=True),
            base64.b64decode(payload["stderr_base64"], validate=True),
            error, diagnostics,
        )
    except (KeyError, TypeError, ValueError) as exc:
        return FunctionalCheckResult(
            "error", error=f"Invalid check-runner response: {exc}; response: {completed.stdout!r}",
            launcher_stderr=diagnostics,
        )
    return result


def run_python_check(
    source: str, workspace: Path, *, timeout: float = 5, cancelled: Event | None = None,
) -> FunctionalCheckResult:
    """Execute one trusted check script in a read-only, network-disabled sandbox.

    Source comes from the evaluator, never the agent's response. It can import
    the resulting fixture explicitly; isolated Python does not add cwd to its
    import path. No shell, retry, login, or model session is involved.
    """
    try:
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("Check timeout must be positive and finite")
        executable = codex_executable()
        with TemporaryDirectory(prefix="agents-spec-check-") as directory:
            profile = Path(directory) / "profile"
            profile.mkdir()
            # Neither the normal profile nor the evaluation login is used here.
            environment = {
                "HOME": directory, "CODEX_HOME": str(profile),
                "PATH": os.pathsep.join((str(Path(sys.executable).parent), "/usr/bin", "/bin")),
            }
            command = [
                executable, "--no-daemon", "sandbox", "-c", 'sandbox_mode="read-only"', "--",
                sys.executable, "-I", "-B", "-S", "-X", "utf8",
                str(Path(__file__).with_name("_check_process.py").resolve()),
            ]
            # The small trusted runner emits a result envelope. Check output is
            # encoded inside it, so arbitrary output cannot masquerade as status.
            completed = run_process(
                # Resolve Codex configuration in evaluator-owned space; only
                # the check subprocess enters the potentially modified fixture.
                command, cwd=Path(directory), env=environment,
                input_text=json.dumps({
                    "source": source, "timeout": timeout, "workspace": str(workspace.resolve()),
                }),
                timeout=timeout + 5, cancelled=cancelled,
            )
            return _decode_result(completed)
    except subprocess.TimeoutExpired:
        return FunctionalCheckResult("error", error="Sandbox launcher or check runner timed out")
    except (OSError, RuntimeError, ValueError) as exc:
        return FunctionalCheckResult("error", error=str(exc))
