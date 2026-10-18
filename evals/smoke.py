"""The text-edit smoke case, workspace lifecycle, and deterministic grading.

See META-EVALUATIONS.md for the suite's requirements and scope.
"""

from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
import os
from pathlib import Path
import stat
from tempfile import TemporaryDirectory
from typing import Literal

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.reporting import EvaluationReport

from evals.functional import FunctionalCheckResult
from evals.workspace import WorkspaceInspectionError, WorkspaceObservation


CONTRACT_PATH = Path(__file__).resolve().parents[1] / "AGENTS.md"
INITIAL_CONTENTS = b"before\n"
PROMPT = (
    "Replace the contents of message.txt with exactly 'after' followed by a single "
    "newline. The file currently contains 'before' followed by a newline."
)


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


class ExactFileContents(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> bool:
        # Pydantic supplies the actual and expected results through ctx.
        assert ctx.expected_output is not None
        return ctx.output.file_contents == ctx.expected_output.file_contents


def smoke_dataset() -> Dataset[str, ExecutionResult, None]:
    # A Dataset groups scenarios (Case) and the rules used to grade them.
    return Dataset(
        name="text-edit-smoke",
        cases=[
            Case(
                name="replace-message",
                inputs=PROMPT,
                expected_output=ExecutionResult("completed", "after\n"),
            )
        ],
        evaluators=[ExactFileContents()],
    )


@contextmanager
def prepare_workspace(
    initial_contents: bytes = INITIAL_CONTENTS, *, fixture_files: Mapping[str, bytes] | None = None,
) -> Iterator[Path]:
    """Copy the current contract and fixture into a disposable directory.

    An explicit mapping replaces the default message.txt fixture. The root
    contract is always supplied separately and cannot be overridden by a case.
    """
    if fixture_files is None:
        fixture_files = {"message.txt": initial_contents}
    with TemporaryDirectory(prefix="agents-spec-eval-") as directory:
        workspace = Path(directory)
        (workspace / "AGENTS.md").write_bytes(CONTRACT_PATH.read_bytes())
        for name, contents in fixture_files.items():
            path = Path(name)
            if (path.is_absolute() or not path.parts or ".." in path.parts
                    or path.parts[0].casefold() == "agents.md"):
                raise ValueError(f"Invalid fixture path: {name!r}; use a relative path outside root AGENTS.md")
            target = workspace / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(contents)
        # The caller uses this directory; leaving the context removes it.
        yield workspace


def read_fixture_file(path: Path) -> bytes | None:
    """Read a regular fixture safely; a missing file returns None."""
    try:
        # Do not follow links or wait for a named pipe's writer when opening.
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return None
    try:
        # Check the opened file itself, avoiding a separate check/read race.
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError(f"{path.name} must be a regular fixture file")
        with os.fdopen(descriptor, "rb", closefd=False) as fixture:
            return fixture.read()
    finally:
        os.close(descriptor)


def read_result(
    workspace: Path, *, workspace_observation: WorkspaceObservation | None = None,
) -> ExecutionResult:
    """Read the actual file without normalizing newlines or whitespace."""
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
    *, dataset: Dataset[str, ExecutionResult, None] | None = None,
    initial_contents: bytes = INITIAL_CONTENTS,
    fixture_files: Mapping[str, bytes] | None = None,
) -> EvaluationReport[str, ExecutionResult, None]:
    """Run one task in a fresh workspace and return Pydantic's printable report.

    The execution function receives a prompt and workspace and returns a result.
    Both the Codex launcher and offline test substitutes use this interface.
    Supply the dataset and its initial contents or fixture mapping together to
    select another case. A mapping replaces the default message.txt fixture.

    Pydantic runs this synchronous task in a worker thread. The CLI supplies
    cancellation to its launcher separately; this case does not own processes.
    """
    if dataset is None:
        dataset = smoke_dataset()

    def task(prompt: str) -> ExecutionResult:
        with prepare_workspace(initial_contents, fixture_files=fixture_files) as workspace:
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
