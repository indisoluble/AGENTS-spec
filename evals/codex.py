"""Run the smoke task with a dedicated, ChatGPT-authenticated Codex profile.

When launching Codex, the runner shall use explicit model settings and a
workspace-write sandbox, without personal configuration or API-key overrides.
When execution ends, the runner shall retain evidence outside the workspace.
If execution exceeds its timeout, then the runner shall stop its process group.

This isolates configuration and fixture writes, not the entire host. Codex's
built-in and managed instructions still apply. The installed CLI must support
the skip_host_skill_discovery feature; its version is recorded in each run.
"""

import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import time

from evals import auth
from evals.smoke import ExecutionResult, read_result


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


def stop_process_group(process: subprocess.Popen) -> None:
    # Codex can spawn shell children; stopping only the parent can leave them running.
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        pass
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def save_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def run_codex(
    prompt: str, workspace: Path, *, model: str, effort: str,
    timeout: float, artifacts: Path, profile: Path,
) -> ExecutionResult:
    """Launch once and preserve evidence before the caller removes the workspace."""
    started = time.monotonic()
    contract = (workspace / "AGENTS.md").read_bytes()
    (artifacts / "AGENTS.md").write_bytes(contract)
    (artifacts / "prompt.txt").write_text(prompt, encoding="utf-8")
    metadata = {
        "model": model, "reasoning_effort": effort, "timeout_seconds": timeout,
        "contract_sha256": hashlib.sha256(contract).hexdigest(),
        "workspace": str(workspace), "codex_home": str(profile), "status": "error",
    }
    result = ExecutionResult("error", error="Execution did not complete")
    try:
        executable = auth.codex_executable()
        auth.check_profile(profile)
        environment = auth.codex_environment(profile)
        version = subprocess.run(
            [executable, "--version"], capture_output=True, text=True, check=True,
            env=environment, cwd=workspace, timeout=15,
        )
        metadata["codex_version"] = version.stdout.strip()
        auth.require_chatgpt_login(executable, profile)
        command = execution_command(executable, workspace, model, effort)
        metadata["command"] = command
        with (artifacts / "events.jsonl").open("w") as events, (artifacts / "stderr.txt").open("w") as errors:
            process = subprocess.Popen(
                command, cwd=workspace, env=environment, stdin=subprocess.PIPE,
                stdout=events, stderr=errors, text=True, start_new_session=True,
            )
            try:
                process.communicate(input=prompt, timeout=timeout)
            finally:
                stop_process_group(process)
            metadata["returncode"] = process.returncode
        if process.returncode:
            raise RuntimeError(f"Codex exited with status {process.returncode}; see stderr.txt and events.jsonl")
        # Only accept a completed turn, not a silent or partial CLI response.
        event_types = [json.loads(line).get("type") for line in (artifacts / "events.jsonl").read_text().splitlines()]
        if "turn.completed" not in event_types or "turn.failed" in event_types:
            raise RuntimeError("Codex did not emit a successful completed turn; see events.jsonl")
        output = workspace / "message.txt"
        if output.is_symlink():
            raise RuntimeError("message.txt must be a regular fixture file, not a symbolic link")
        result = read_result(workspace)
    except subprocess.TimeoutExpired:
        result = ExecutionResult("error", error="Codex execution or prerequisite check timed out")
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        result = ExecutionResult("error", error=str(exc))
    finally:
        # Preserve only fixture files; never copy the Codex profile or follow links.
        final_files = artifacts / "workspace"
        final_files.mkdir()
        for name in ("AGENTS.md", "message.txt"):
            source = workspace / name
            try:
                if stat.S_ISREG(source.lstat().st_mode):
                    (final_files / name).write_bytes(source.read_bytes())
            except FileNotFoundError:
                pass
        metadata.update(status=result.status, error=result.error, duration_seconds=time.monotonic() - started)
        save_json(artifacts / "execution.json", metadata)
    return result
