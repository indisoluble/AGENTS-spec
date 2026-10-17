"""The text-edit smoke case, workspace lifecycle, and deterministic grading.

See META-EVALUATIONS.md for the suite's requirements and scope.
"""

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
import os
from pathlib import Path
import stat
from tempfile import TemporaryDirectory
from typing import Literal

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.reporting import EvaluationReport


CONTRACT_PATH = Path(__file__).resolve().parents[1] / "AGENTS.md"
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
def prepare_workspace() -> Iterator[Path]:
    """Copy the current contract and fixture into a disposable directory."""
    with TemporaryDirectory(prefix="agents-spec-eval-") as directory:
        workspace = Path(directory)
        (workspace / "AGENTS.md").write_bytes(CONTRACT_PATH.read_bytes())
        (workspace / "message.txt").write_bytes(b"before\n")
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


def read_result(workspace: Path) -> ExecutionResult:
    """Read the actual file without normalizing newlines or whitespace."""
    data = read_fixture_file(workspace / "message.txt")
    # Missing output is graded as incorrect, rather than an execution crash.
    contents = None if data is None else data.decode("utf-8")
    return ExecutionResult("completed", contents)


def evaluate(
    execute: Callable[[str, Path], ExecutionResult],
) -> EvaluationReport[str, ExecutionResult, None]:
    """Run one task in a fresh workspace and return Pydantic's printable report.

    The execution function receives a prompt and workspace and returns a result.
    Both the Codex launcher and offline test substitutes use this interface.

    Pydantic runs this synchronous task in a worker thread. The CLI supplies
    cancellation to its launcher separately; this case does not own processes.
    """

    def task(prompt: str) -> ExecutionResult:
        with prepare_workspace() as workspace:
            # The supplied function performs the work inside the fresh fixture.
            result = execute(prompt, workspace)
            if result.status == "error":
                # Pydantic records raised errors in report.failures, without grading.
                raise ExecutionError(result.error or "Task execution failed")
            return result

    # Run the case, grade its result, and return the report before continuing.
    return smoke_dataset().evaluate_sync(
        task,
        name="text-edit-smoke",
        max_concurrency=1,
        progress=False,
    )
