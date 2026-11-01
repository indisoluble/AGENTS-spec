"""Orchestrate functional checks, retain evidence, and interpret generic results.

Scenarios supply ordered check sources, required files, and timeouts, and keep
additional acceptance criteria local. See docs/evaluations.md for evidence and
error semantics; functional.py owns the sandboxed execution of each individual check.
"""

from collections.abc import Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from threading import Event

from pydantic_evals.evaluators import EvaluationReason

from evals.codex import save_json
from evals.evaluation import ExecutionResult
from evals.functional import run_python_check
from evals.workspace import WorkspaceInspectionError, WorkspaceObservation


def require_observation(result: ExecutionResult) -> WorkspaceObservation:
    """Require both snapshots without confusing an observed empty tree with absence."""
    observation = result.workspace_observation
    if observation is None or observation.initial is None or observation.final is None:
        raise WorkspaceInspectionError("Complete initial and final workspace observations are required")
    return observation


def _invalid_files(result: ExecutionResult, required_files: Sequence[str]) -> list[str]:
    final = require_observation(result).final
    invalid = []
    for path in required_files:
        entry = final.get(path)
        if entry is None or entry.kind != "file":
            invalid.append(f"{path}: missing or not a regular file")
        elif entry.contents is None:
            raise WorkspaceInspectionError(f"{path}: file contents were not observed")
    return invalid


def run_checks(
    result: ExecutionResult, workspace: Path, *, sources: Mapping[str, str],
    required_files: Mapping[str, Sequence[str]], timeout: float, artifacts: Path,
    cancelled: Event | None = None,
) -> ExecutionResult:
    """Run checks in source mapping order and retain each result.

    Call after agent cleanup and before fixture removal.

    Never execute links or special files in place of required fixture files.
    A successfully observed invalid fixture fails grading, rather than inventing
    a process exit status. Launcher failures remain infrastructure errors.
    """
    checks = {}
    evidence = {}
    errors = [result.error or "Agent execution failed"] if result.status == "error" else []
    for name, source in sources.items():
        skipped = "Agent execution failed" if result.status == "error" else None
        if skipped is None:
            try:
                invalid = _invalid_files(result, required_files[name])
                skipped = "; ".join(invalid) if invalid else None
            except WorkspaceInspectionError as exc:
                skipped = str(exc)
                errors.append(skipped)
        record = {"timeout_seconds": timeout, "status": "not_run", "reason": skipped}
        if skipped is None:
            check = run_python_check(source, workspace, timeout=timeout, cancelled=cancelled)
            checks[name] = check
            record = {"timeout_seconds": timeout, "status": check.status,
                      "returncode": check.returncode, "error": check.error}
            if check.status == "error":
                errors.append(f"{name}: {check.error}")
        evidence[name] = record
        # Independent writes preserve available diagnostics even if one fails.
        files = {f"{name}.py": source.encode("utf-8")}
        if name in checks:
            check = checks[name]
            files.update({f"{name}.stdout": check.stdout, f"{name}.stderr": check.stderr,
                          f"{name}.launcher-stderr": check.launcher_stderr})
        for filename, contents in files.items():
            try:
                folder = artifacts / "checks"
                folder.mkdir(exist_ok=True)
                (folder / filename).write_bytes(contents)
            except OSError as exc:
                errors.append(f"checks/{filename}: {exc}")
    try:
        save_json(artifacts / "functional-checks.json", evidence)
    except (OSError, ValueError) as exc:
        errors.append(f"functional-checks.json: {exc}")
    return replace(result, functional_checks=checks,
                   status="error" if errors else result.status,
                   error="\n".join(errors) if errors else result.error)


def check_assertion(
    result: ExecutionResult, name: str, *, required_files: Sequence[str],
) -> EvaluationReason:
    """Interpret observed files and a check result before scenario-specific grading."""
    invalid = _invalid_files(result, required_files)
    if invalid:
        return EvaluationReason(False, reason="; ".join(invalid))
    if result.functional_checks is None or name not in result.functional_checks:
        raise RuntimeError(f"{name}: functional-check observation is required")
    check = result.functional_checks[name]
    if check.status != "completed" or check.returncode is None:
        raise RuntimeError(f"{name}: {check.error or 'functional check did not complete'}")
    passed = check.returncode == 0
    return EvaluationReason(passed, reason=(
        f"{name}: check passed; see checks/{name}.stdout and .stderr"
        if passed else f"{name}: check exited {check.returncode}; "
        + check.stderr.decode("utf-8", errors="backslashreplace")
    ))
