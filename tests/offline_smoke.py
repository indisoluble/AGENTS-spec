"""A test-only task substitute for viewing the Pydantic Evals report."""

from pathlib import Path

from evals.evaluation import ExecutionResult, read_result
from evals.smoke import evaluate


def write_after(prompt: str, workspace: Path) -> ExecutionResult:
    # Stand in for the agent: ignore the prompt and make the known correct edit.
    (workspace / "message.txt").write_bytes(b"after\n")
    return read_result(workspace)


if __name__ == "__main__":
    print("Offline demonstration: a test function edits the file; no agent runs.")
    evaluate(write_after).print(include_output=True, include_durations=False)
