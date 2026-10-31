"""The text-edit smoke case, exact-content grading, and default execution helper.

See EVALUATIONS.md for the suite's requirements and scope.
"""

from collections.abc import Callable, Mapping
from pathlib import Path

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.reporting import EvaluationReport

from evals.evaluation import ExecutionResult, evaluate as evaluate_dataset


INITIAL_CONTENTS = b"before\n"
PROMPT = (
    "Replace the contents of message.txt with exactly 'after' followed by a single "
    "newline. The file currently contains 'before' followed by a newline."
)


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


def evaluate(
    execute: Callable[[str, Path], ExecutionResult],
    *, dataset: Dataset[str, ExecutionResult, None] | None = None,
    initial_contents: bytes = INITIAL_CONTENTS,
    fixture_files: Mapping[str, bytes] | None = None,
) -> EvaluationReport[str, ExecutionResult, None]:
    """Run with the smoke defaults and return Pydantic's printable report.

    Keep the existing convenience arguments: a supplied dataset replaces smoke,
    initial_contents sets message.txt, and an explicit mapping replaces that file.
    An empty mapping creates only the root contract.
    """
    if dataset is None:
        dataset = smoke_dataset()
    if fixture_files is None:
        fixture_files = {"message.txt": initial_contents}
    return evaluate_dataset(execute, dataset=dataset, fixture_files=fixture_files)
