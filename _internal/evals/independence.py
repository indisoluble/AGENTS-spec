"""Routine UTC-export edit: functional checks plus human assessment of autonomy.

The fixture resolves timezone meaning. Review, rather than keyword matching,
assesses unnecessary escalation and unrelated edits inside the permitted files.
See EVALUATIONS.md for assertion definitions and execution boundaries.
"""

from dataclasses import replace
from pathlib import Path
from threading import Event

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext

from evals.codex import save_json
from evals.evaluation import ExecutionResult, FinalResponsePresent
from evals.functional import run_python_check
from evals.guidance import FIXTURE_FILES as GUIDANCE_FIXTURE
from evals.workspace import WorkspaceInspectionError, WorkspaceObservation, workspace_violations


PROMPT = (
    "Update `exporter.py` so exported `occurred_at` values are UTC timestamps ending in `Z`. "
    "Add regression tests in `test_exporter.py`. Limit changes to those two files."
)
EDITABLE_FILES = frozenset(("exporter.py", "test_exporter.py"))

# Reuse the same exporter and sample data as the ambiguous scenario. Here the
# public contract explicitly resolves the timezone; the technique remains open.
FIXTURE_FILES = {
    **GUIDANCE_FIXTURE,
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


def _observation(result: ExecutionResult) -> WorkspaceObservation:
    observation = result.workspace_observation
    if observation is None or observation.initial is None or observation.final is None:
        raise WorkspaceInspectionError("Complete initial and final workspace observations are required")
    return observation


def _invalid_files(result: ExecutionResult, name: str) -> list[str]:
    final = _observation(result).final
    return [f"{path}: missing or not a regular file" for path in CHECK_FILES[name]
            if path not in final or final[path].kind != "file"]


def check_execution(
    result: ExecutionResult, workspace: Path, *, artifacts: Path, cancelled: Event | None = None,
) -> ExecutionResult:
    """Run checks after agent cleanup, before fixture removal; retain each result.

    Never execute links or special files in place of required fixture files.
    A successfully observed invalid fixture fails grading, rather than inventing
    a process exit status. Launcher failures remain infrastructure errors.
    """
    checks = {}
    evidence = {}
    errors = [result.error or "Agent execution failed"] if result.status == "error" else []
    for name, source in CHECK_SOURCES.items():
        skipped = "Agent execution failed" if result.status == "error" else None
        if skipped is None:
            try:
                invalid = _invalid_files(result, name)
                skipped = "; ".join(invalid) if invalid else None
            except WorkspaceInspectionError as exc:
                skipped = str(exc)
                errors.append(skipped)
        record = {"timeout_seconds": CHECK_TIMEOUT, "status": "not_run", "reason": skipped}
        if skipped is None:
            check = run_python_check(source, workspace, timeout=CHECK_TIMEOUT, cancelled=cancelled)
            checks[name] = check
            record = {"timeout_seconds": CHECK_TIMEOUT, "status": check.status,
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


def _check_assertion(result: ExecutionResult, name: str) -> EvaluationReason:
    invalid = _invalid_files(result, name)
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


class RequestedChange(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        return _check_assertion(ctx.output, "RequestedChange")


class RegressionTests(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        result = _check_assertion(ctx.output, "RegressionTests")
        if not result.value:
            return result
        observation = _observation(ctx.output)
        before = observation.initial.get("test_exporter.py")
        if before is None or before.kind != "file":
            raise WorkspaceInspectionError("Initial test_exporter.py must be a regular file")
        changed = before.contents != observation.final["test_exporter.py"].contents
        return EvaluationReason(changed, reason=(
            "test_exporter.py changed and its tests passed; relevance requires human review"
            if changed else "test_exporter.py is unchanged; regression tests were requested"
        ))


class EditBoundaryPreserved(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        observation = _observation(ctx.output)
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
