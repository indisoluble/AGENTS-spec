"""Run a selected task with a dedicated, ChatGPT-authenticated Codex profile.

See META-EVALUATIONS.md for requirements, evidence, and execution boundaries.
"""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from threading import Event
import time

from evals import auth
from evals.process import run_process
from evals.smoke import ExecutionResult, read_fixture_file, read_result


def execution_command(executable: str, workspace: Path, model: str, effort: str) -> list[str]:
    command = [
        executable, "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules",
        "--ephemeral", "--json", "--color", "never", "--skip-git-repo-check",
        "--sandbox", "workspace-write", "--cd", str(workspace), "--model", model,
        "--enable", "skip_host_skill_discovery",
    ]
    # Keep personal extensions and prior-session context out of the evaluation.
    for feature in ("apps", "plugins", "remote_plugin", "hooks", "memories", "multi_agent",
                    "skill_search", "shell_snapshot", "daemon_auto_start"):
        command.extend(["--disable", feature])
    settings = {
        "model_reasoning_effort": effort,
        "model_provider": "openai",
        **auth.AUTH_SETTINGS,
        "approval_policy": "never",
        "web_search": "disabled",
        "sandbox_workspace_write.network_access": False,
        "shell_environment_policy.inherit": "none",
        "analytics.enabled": False,
    }
    for key, value in settings.items():
        command.extend(["--config", f"{key}={json.dumps(value)}"])
    return [*command, "-"]  # Feed the prompt through stdin.


def save_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def retain_evidence(
    workspace: Path, artifacts: Path, metadata: dict, result: ExecutionResult,
) -> ExecutionResult:
    """Save what is available without replacing the primary execution failure."""
    errors = []
    final_files = artifacts / "workspace"
    for name in ("AGENTS.md", "message.txt"):
        try:
            # Each copy is independent, so one failure does not skip the other.
            final_files.mkdir(exist_ok=True)
            contents = read_fixture_file(workspace / name)
            if contents is not None:
                (final_files / name).write_bytes(contents)
        except (OSError, ValueError) as exc:
            errors.append(f"workspace/{name}: {exc}")

    # Keep the execution outcome separate from errors in saving its evidence.
    metadata.update(
        status="error" if errors else result.status,
        execution_status=result.status, error=result.error, evidence_errors=errors,
    )
    try:
        save_json(artifacts / "execution.json", metadata)
    except (OSError, ValueError) as exc:
        errors.append(f"execution.json: {exc}")
    if errors:
        message = "Evidence could not be fully saved: " + "; ".join(errors)
        if result.error:
            message = f"{result.error}\n{message}"
        print(message, file=sys.stderr)
        return ExecutionResult("error", result.file_contents, message)
    return result


def run_codex(
    prompt: str, workspace: Path, *, model: str, effort: str,
    timeout: float, artifacts: Path, profile: Path, cancelled: Event | None = None,
) -> ExecutionResult:
    """Launch once and preserve evidence before the caller removes the workspace."""
    started = time.monotonic()
    metadata = {
        "model": model, "reasoning_effort": effort, "timeout_seconds": timeout,
        "workspace": str(workspace), "codex_home": str(profile), "status": "error",
    }
    result = ExecutionResult("error", error="Execution did not complete")
    try:
        contract = (workspace / "AGENTS.md").read_bytes()
        metadata["contract_sha256"] = hashlib.sha256(contract).hexdigest()
        (artifacts / "AGENTS.md").write_bytes(contract)
        (artifacts / "message.txt").write_bytes((workspace / "message.txt").read_bytes())
        (artifacts / "prompt.txt").write_text(prompt, encoding="utf-8")
        executable = auth.codex_executable()
        auth.check_profile(profile)
        environment = auth.codex_environment(profile)
        version = run_process(
            [executable, "--version"], env=environment, cwd=workspace,
            timeout=15, cancelled=cancelled,
        )
        version.check_returncode()
        metadata["codex_version"] = version.stdout.strip()
        auth.require_chatgpt_login(executable, profile, cancelled)
        command = execution_command(executable, workspace, model, effort)
        metadata["command"] = command
        with (artifacts / "events.jsonl").open("w") as events, (artifacts / "stderr.txt").open("w") as errors:
            completed = run_process(
                command, cwd=workspace, env=environment, input_text=prompt,
                stdout=events, stderr=errors, timeout=timeout, cancelled=cancelled,
            )
            metadata["returncode"] = completed.returncode
        if completed.returncode:
            raise RuntimeError(f"Codex exited with status {completed.returncode}; see stderr.txt and events.jsonl")
        # Only accept a completed turn, not a silent or partial CLI response.
        event_types = [json.loads(line).get("type") for line in (artifacts / "events.jsonl").read_text().splitlines()]
        if "turn.completed" not in event_types or "turn.failed" in event_types:
            raise RuntimeError("Codex did not emit a successful completed turn; see events.jsonl")
        result = read_result(workspace)
    except subprocess.TimeoutExpired:
        result = ExecutionResult("error", error="Codex execution or prerequisite check timed out")
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        result = ExecutionResult("error", error=str(exc))
    finally:
        metadata["duration_seconds"] = time.monotonic() - started
        result = retain_evidence(workspace, artifacts, metadata, result)
    return result
