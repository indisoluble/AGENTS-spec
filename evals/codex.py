"""Run a selected task with a dedicated, ChatGPT-authenticated Codex profile.

See META-EVALUATIONS.md for requirements, evidence, and execution boundaries.
"""

import base64
from dataclasses import replace
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
from evals.workspace import WorkspaceObservation, WorkspaceSnapshot, snapshot_workspace, workspace_changes


def execution_command(
    executable: str, workspace: Path, model: str, effort: str, *, final_response_path: Path | None = None,
) -> list[str]:
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
    if final_response_path is not None:
        command.extend(["--output-last-message", str(final_response_path)])
    return [*command, "-"]  # Feed the prompt through stdin.


def save_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def snapshot_manifest(snapshot: WorkspaceSnapshot) -> dict:
    """Encode exact bytes for JSON; links and special files remain descriptions."""
    return {path: {
        "kind": entry.kind,
        "mode": entry.mode,
        "contents_base64": None if entry.contents is None else base64.b64encode(entry.contents).decode("ascii"),
        "link_target": entry.link_target,
    } for path, entry in sorted(snapshot.items())}


def retain_snapshot(snapshot: WorkspaceSnapshot, artifacts: Path, phase: str) -> list[str]:
    """Attempt the manifest and each regular-file copy independently."""
    errors = []
    try:
        save_json(artifacts / f"{phase}-workspace.json", snapshot_manifest(snapshot))
    except (OSError, ValueError) as exc:
        errors.append(f"{phase}-workspace.json: {exc}")
    folder = "initial-workspace" if phase == "initial" else "workspace"
    for name, entry in sorted(snapshot.items()):
        # The manifest describes directories, links, special files, and the root.
        # Recreate only regular children, using captured bytes rather than paths.
        if name == "." or entry.kind != "file":
            continue
        assert entry.contents is not None
        target = artifacts / folder / name
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(entry.contents)
        except (OSError, ValueError) as exc:
            errors.append(f"{folder}/{name}: {exc}")
    return errors


def retain_evidence(
    workspace: Path, artifacts: Path, metadata: dict, result: ExecutionResult,
) -> ExecutionResult:
    """Save what is available without replacing the primary execution failure."""
    errors = []
    observation = result.workspace_observation
    if observation is not None:
        for name, snapshot in (("initial", observation.initial), ("final", observation.final)):
            if snapshot is not None:
                errors.extend(retain_snapshot(snapshot, artifacts, name))
        try:
            (artifacts / "workspace-changes.txt").write_text(workspace_changes(observation), encoding="utf-8")
        except (OSError, ValueError) as exc:
            errors.append(f"workspace-changes.txt: {exc}")
    else:
        # Preserve smoke's safe reads and its rejection of non-regular fixtures.
        final_files = artifacts / "workspace"
        for name in ("AGENTS.md", "message.txt"):
            try:
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
        return replace(result, status="error", error=message)
    return result


def run_codex(
    prompt: str, workspace: Path, *, model: str, effort: str,
    timeout: float, artifacts: Path, profile: Path, cancelled: Event | None = None,
    observe_workspace: bool = False,
    capture_response: bool = False,
) -> ExecutionResult:
    """Launch once and preserve evidence before the caller removes the workspace."""
    started = time.monotonic()
    metadata = {
        "model": model, "reasoning_effort": effort, "timeout_seconds": timeout,
        "workspace": str(workspace), "codex_home": str(profile), "status": "error",
    }
    result = ExecutionResult("error", error="Execution did not complete")
    initial = None
    response_path = None
    try:
        if observe_workspace:
            initial = snapshot_workspace(workspace)
        contract = (workspace / "AGENTS.md").read_bytes()
        metadata["contract_sha256"] = hashlib.sha256(contract).hexdigest()
        (artifacts / "AGENTS.md").write_bytes(contract)
        message = read_fixture_file(workspace / "message.txt")
        if message is not None:
            (artifacts / "message.txt").write_bytes(message)
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
        if capture_response:
            destination = artifacts.resolve() / "final-response.txt"
            if destination.is_relative_to(workspace.resolve()):
                raise ValueError("Final response evidence must be outside the agent workspace")
            # A pre-existing reply could otherwise turn failed capture into success.
            if destination.exists() or destination.is_symlink():
                raise ValueError("Final response evidence already exists; use a fresh evidence directory")
            response_path = destination
        command = execution_command(executable, workspace, model, effort, final_response_path=response_path)
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
        result = ExecutionResult("completed") if observe_workspace else read_result(workspace)
    except subprocess.TimeoutExpired:
        result = ExecutionResult("error", error="Codex execution or prerequisite check timed out")
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        result = ExecutionResult("error", error=str(exc))
    finally:
        if response_path is not None:
            try:
                response = read_fixture_file(response_path)
                if response is None:
                    raise ValueError("final-response.txt was not produced")
                # Preserve whitespace and line endings, including an empty reply.
                result = replace(result, final_response=response.decode("utf-8"))
            except (OSError, ValueError) as exc:
                message = f"Final response capture failed: {exc}"
                result = replace(result, status="error", error=f"{result.error}\n{message}" if result.error else message)
        if observe_workspace:
            # run_process has stopped its process group before we reach this point,
            # including on timeout or interruption. Keep any successful observation.
            final = None
            try:
                final = snapshot_workspace(workspace)
            except OSError as exc:
                message = f"Final workspace inspection failed: {exc}"
                result = replace(result, status="error", error=f"{result.error}\n{message}" if result.error else message)
            observation = WorkspaceObservation(initial, final)
            contents = None if final is None else read_result(workspace, workspace_observation=observation).file_contents
            result = replace(result, file_contents=contents, workspace_observation=observation)
        metadata["duration_seconds"] = time.monotonic() - started
        result = retain_evidence(workspace, artifacts, metadata, result)
    return result
