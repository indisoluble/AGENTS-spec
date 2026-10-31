"""Shared execution results, evaluation orchestration, and response presence.

Callers supply the dataset, fixture, and execution function; scenario policy
stays with the scenario. See EVALUATIONS.md for requirements and scope.
"""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from pydantic_evals import Dataset
from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext
from pydantic_evals.reporting import EvaluationReport

from evals.functional import FunctionalCheckResult
from evals.workspace import WorkspaceInspectionError, WorkspaceObservation, prepare_workspace, read_fixture_file


@dataclass(frozen=True)
class ExecutionResult:
    # "completed" means execution finished; the evaluator decides if it passed.
    status: Literal["completed", "error"]
    file_contents: str | None = None
    error: str | None = None
    # Keep potentially large snapshots out of the terminal's output column.
    workspace_observation: WorkspaceObservation | None = field(default=None, repr=False)
    final_response: str | None = field(default=None, repr=False)
    functional_checks: dict[str, FunctionalCheckResult] | None = field(default=None, repr=False)


class ExecutionError(RuntimeError):
    """The task could not execute; this is not a failed content assertion."""


class FinalResponsePresent(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        response = ctx.output.final_response
        if response is None:
            raise RuntimeError("Final response capture is required")
        present = bool(response.strip())
        return EvaluationReason(present, reason=(
            "Final response contains non-whitespace text; meaning requires human review"
            if present else "Final response is empty or whitespace only"
        ))


def read_result(
    workspace: Path, *, workspace_observation: WorkspaceObservation | None = None,
) -> ExecutionResult:
    """Assemble the existing message.txt summary without normalizing its contents."""
    if workspace_observation is not None:
        if workspace_observation.final is None:
            raise WorkspaceInspectionError("Final workspace observation is missing")
        entry = workspace_observation.final.get("message.txt")
        # Scope grading uses captured bytes only. Links and special files have no
        # regular-file output; invalid UTF-8 remains observable rather than crashing.
        data = entry.contents if entry is not None and entry.kind == "file" else None
        contents = None if data is None else data.decode("utf-8", errors="surrogateescape")
        return ExecutionResult("completed", contents, workspace_observation=workspace_observation)
    data = read_fixture_file(workspace / "message.txt")
    # Missing output is graded as incorrect, rather than an execution crash.
    contents = None if data is None else data.decode("utf-8")
    return ExecutionResult("completed", contents)


def evaluate(
    execute: Callable[[str, Path], ExecutionResult],
    *, dataset: Dataset[str, ExecutionResult, None],
    fixture_files: Mapping[str, bytes],
) -> EvaluationReport[str, ExecutionResult, None]:
    """Run a supplied dataset in fresh workspaces and return Pydantic's report.

    The execution function receives a prompt and workspace and returns a result.
    Both the Codex launcher and offline test substitutes use this interface.
    The fixture mapping supplies exact bytes; workspace preparation injects the
    current root contract separately.

    Pydantic runs this synchronous task in a worker thread. The CLI supplies
    cancellation to its launcher separately; this function does not own processes.
    """
    def task(prompt: str) -> ExecutionResult:
        with prepare_workspace(fixture_files=fixture_files) as workspace:
            # The supplied function performs the work inside the fresh fixture.
            result = execute(prompt, workspace)
            if result.status == "error":
                # Pydantic records raised errors in report.failures, without grading.
                raise ExecutionError(result.error or "Task execution failed")
            return result

    # Run the case, grade its result, and return the report before continuing.
    return dataset.evaluate_sync(
        task,
        name=dataset.name,
        max_concurrency=1,
        progress=False,
    )
