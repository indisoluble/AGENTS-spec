"""The text-edit smoke case, workspace lifecycle, and deterministic grading.

Current requirements (owned here until the evaluation guide is added):
When a case starts, the smoke suite shall provide a fresh temporary workspace
with the initial fixture and an unchanged copy of the current root AGENTS.md.
When execution completes, the smoke suite shall compare the reported file
contents exactly with the case's expected contents, including whitespace.
If execution reports an error or raises an exception, then the smoke suite
shall report an execution failure separately from content assertions.
When a case finishes or raises, the smoke suite shall clean its workspace.
"""

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
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


def read_result(workspace: Path) -> ExecutionResult:
    """Read the actual file without normalizing newlines or whitespace."""
    try:
        contents = (workspace / "message.txt").read_bytes().decode("utf-8")
    except FileNotFoundError:
        # Missing output is graded as incorrect, rather than an execution crash.
        contents = None
    return ExecutionResult("completed", contents)


def evaluate(
    execute: Callable[[str, Path], ExecutionResult],
) -> EvaluationReport[str, ExecutionResult, None]:
    """Run one task in a fresh workspace and return Pydantic's printable report.

    The execution function receives a prompt and workspace and returns a result.
    Both the Codex launcher and offline test substitutes use this interface.
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
