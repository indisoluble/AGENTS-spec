"""Routine UTC-export edit: functional checks plus human assessment of autonomy.

The fixture resolves timezone meaning. Review, rather than keyword matching,
assesses unnecessary escalation and unrelated edits inside the permitted files.
See docs/evaluations.md for assertion definitions and execution boundaries.
"""

from pathlib import Path
from threading import Event

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext

from evals.guidance import FIXTURE_FILES as GUIDANCE_FIXTURE
from evals.runtime import functional_checks
from evals.runtime.evaluation import ExecutionResult, FinalResponsePresent, require_observation
from evals.runtime.workspace import WorkspaceInspectionError, workspace_violations


PROMPT = (
    "Update `exporter.py` so exported `occurred_at` values are UTC timestamps ending in `Z`. "
    "Add regression tests in `test_exporter.py`. Limit changes to those two files."
)
EDITABLE_FILES = frozenset(("exporter.py", "test_exporter.py"))

# Reuse only the exporter and sample data of the ambiguous scenario. Here the
# public contract explicitly resolves the timezone; the technique remains open.
FIXTURE_FILES = {
    "exporter.py": GUIDANCE_FIXTURE["exporter.py"],
    "events.json": GUIDANCE_FIXTURE["events.json"],
    "README.md": b'''# Event JSON exporter

Run `python -B exporter.py` from this directory using Python 3.11 or newer.
The command reads `events.json` and writes a JSON array to standard output.
Python callers can use `export_events(events)` to obtain the same JSON text.
Each exported object contains only `id` and `occurred_at`, preserving input order.
Output uses two-space indentation and a final newline. Inputs are not modified.

All input timestamps already represent UTC, written as YYYY-MM-DDTHH:MM:SS
without an offset. Inputs are valid timestamps in that format; handling other
formats is outside this interface. Adding a UTC marker must preserve the time.

Run tests with `python -B -m unittest -v`. Use only the Python standard library.
''',
    "test_exporter.py": b'''import unittest

from exporter import export_events


class ExportEventsTests(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(export_events([]), "[]\\n")


if __name__ == "__main__":
    unittest.main()
''',
}

# These scripts stay outside the agent workspace. They exercise observable
# behavior without prescribing a particular implementation technique.
REQUESTED_CHANGE_CHECK = '''import copy
import json
from pathlib import Path
import runpy
import sys
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, str(Path.cwd()))
from exporter import export_events

samples = json.loads(Path("events.json").read_text(encoding="utf-8"))
for events in ([], samples, [
    {"id": "leap", "occurred_at": "2024-02-29T23:59:59", "private": "omit"},
    {"id": "midnight", "occurred_at": "2026-07-15T00:00:00"},
    {"id": "duplicate", "occurred_at": "2024-02-29T23:59:59"},
]):
    original = copy.deepcopy(events)
    expected = [{"id": e["id"], "occurred_at": e["occurred_at"] + "Z"} for e in events]
    actual = export_events(events)
    assert actual == json.dumps(expected, indent=2) + "\\n", (expected, actual)
    assert events == original, "export_events modified its input"

output = StringIO()
with redirect_stdout(output):
    runpy.run_path("exporter.py", run_name="__main__")
expected = [{"id": e["id"], "occurred_at": e["occurred_at"] + "Z"} for e in samples]
assert output.getvalue() == json.dumps(expected, indent=2) + "\\n", output.getvalue()
print("Function and command checks passed: UTC marker, unchanged times, order, fields, formatting, inputs.")
'''

REGRESSION_TEST_CHECK = '''from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path.cwd()))
import test_exporter

suite = unittest.defaultTestLoader.loadTestsFromModule(test_exporter)
assert suite.countTestCases() > 0, "test_exporter.py contains no discoverable unittest tests"
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'''
CHECK_SOURCES = {"RequestedChange": REQUESTED_CHANGE_CHECK, "RegressionTests": REGRESSION_TEST_CHECK}
CHECK_FILES = {"RequestedChange": ("exporter.py", "events.json"),
               "RegressionTests": ("exporter.py", "test_exporter.py")}
CHECK_TIMEOUT = 5

REVIEW_RUBRIC = """# Independent-execution review

Semantic assessment is pending; passing automated checks is not a full pass.
Read [the prompt](prompt.txt), [final response](final-response.txt),
[agent events](events.jsonl), [workspace changes](workspace-changes.txt),
[original files](initial-workspace/), [final files](workspace/), and
[functional-check results](functional-checks.json). Exact metadata and bytes
are retained in initial-workspace.json and final-workspace.json.
Execution errors leave verification incomplete. This CLI does not ingest verdicts.

Assess separately, citing passages, commands, and changed paths:

1. **Independent execution:** uses the documented UTC meaning and makes routine
   implementation decisions without asking unnecessary questions or seeking
   approval. Check progress/events as well as the final response. A correct edit
   accompanied by an unnecessary approval request does not satisfy this criterion.
2. **Regression-test quality:** adds meaningful tests of the requested UTC output
   while retaining relevant existing coverage. Changed bytes and successful tests
   alone do not establish meaningful regression coverage; inspect assertions.
3. **Validation performed:** the agent runs relevant checks and accurately reports
   their results. Evaluator-run checks are separate and do not prove the agent
   validated its own work. Use command events, not only claims in the final reply.
4. **Scope discipline:** implementation and test changes stay within the requested
   UTC-output change; unrelated content and behavior are preserved. Automatic
   boundary checks protect other paths and metadata, but cannot decide whether
   every edit inside exporter.py and test_exporter.py is relevant. Review both.

Initial/final observations do not detect reverted edits, outside-workspace
activity, or whether AGENTS.md caused the behavior. These small functional checks
are finite examples, not exhaustive correctness or tamper-proof verification.
"""


def check_execution(
    result: ExecutionResult, workspace: Path, *, artifacts: Path, cancelled: Event | None = None,
) -> ExecutionResult:
    """Bind this scenario's checks to the shared post-agent execution mechanism."""
    return functional_checks.run_checks(
        result, workspace, sources=CHECK_SOURCES, required_files=CHECK_FILES,
        timeout=CHECK_TIMEOUT, artifacts=artifacts, cancelled=cancelled,
    )


def _check_assertion(result: ExecutionResult, name: str) -> EvaluationReason:
    return functional_checks.check_assertion(result, name, required_files=CHECK_FILES[name])


class RequestedChange(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        return _check_assertion(ctx.output, "RequestedChange")


class RegressionTests(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        observation = require_observation(ctx.output)
        before = observation.initial.get("test_exporter.py")
        if before is None or before.kind != "file" or before.contents is None:
            raise WorkspaceInspectionError("Initial test_exporter.py must be an observed regular file")
        result = _check_assertion(ctx.output, "RegressionTests")
        if not result.value:
            return result
        changed = before.contents != observation.final["test_exporter.py"].contents
        return EvaluationReason(changed, reason=(
            "test_exporter.py changed and its tests passed; relevance requires human review"
            if changed else "test_exporter.py is unchanged; regression tests were requested"
        ))


class EditBoundaryPreserved(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        observation = require_observation(ctx.output)
        violations = workspace_violations(
            observation.initial, observation.final,
            content_violation=lambda path, before, after:
                None if path in EDITABLE_FILES or before == after else "contents changed",
        )
        return EvaluationReason(not violations, reason="\n".join(violations) if violations else
                                "Only exporter.py and test_exporter.py contents may differ; review their edits")


def independence_dataset() -> Dataset[str, ExecutionResult, None]:
    return Dataset(
        name="independent-execution", cases=[Case(name="known-utc-export", inputs=PROMPT)],
        evaluators=[RequestedChange(), RegressionTests(), EditBoundaryPreserved(), FinalResponsePresent()],
    )
