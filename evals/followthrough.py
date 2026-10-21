"""Importer change: independent functional assertions and follow-through review.

The initial fixture retains its accepted last-value-wins behavior. Automated
checks assess resulting behavior; requirements, documentation, test quality,
agent validation, and completion claims remain separate human judgments.
"""

from dataclasses import replace
from pathlib import Path
from threading import Event

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext

from evals.codex import save_json
from evals.evaluation import ExecutionResult, FinalResponsePresent
from evals.functional import run_python_check
from evals.workspace import WorkspaceInspectionError, WorkspaceObservation


PROMPT = """Change import_records(store, records) to reject a batch containing repeated
record IDs by raising ValueError, without changing the store or input records.
Add appropriate regression tests for this change.

Duplicate IDs are case-sensitive: "A" and "a" are distinct. Repeated IDs with
identical values are still duplicates. An ID already present in the store is a
valid update if it appears only once in the incoming batch. On rejection, the
entire store must equal its pre-call contents, including entries that earlier
records might otherwise have inserted or updated.

Preserve the other supported behavior: unique batches insert or update entries,
leave unrelated store entries unchanged, and return None; empty batches leave
the store unchanged and return None. Input records must remain unchanged on
both success and rejection. A ValueError subclass is acceptable, and exception
wording is unrestricted.

Supported inputs remain a dictionary and a finite list of well-formed records
containing string IDs and values. Malformed records, generators, concurrency,
crash recovery, and persistent storage are outside this interface. The guarantee
concerns the observable state when the call exits; choose any implementation
that satisfies it.

Keep work limited to this importer change, its tests, and affected project
documentation. Use only the Python standard library, preserve the public
function and documented test command, and leave AGENTS.md unchanged.
"""

FIXTURE_FILES = {
    "importer.py": b'''"""Import records into a caller-owned store; contract: docs/importer.md."""


def import_records(store, records):
    for record in records:
        store[record["id"]] = record["value"]
''',
    "test_importer.py": b'''from copy import deepcopy
import unittest

from importer import import_records


class ImportRecordsTests(unittest.TestCase):
    def test_inserts_updates_and_preserves_unrelated_entries_and_input(self):
        store = {"existing": "old", "untouched": "keep"}
        records = [
            {"id": "new", "value": "added"},
            {"id": "existing", "value": "updated"},
        ]
        original_records = deepcopy(records)

        result = import_records(store, records)

        self.assertIsNone(result)
        self.assertEqual(store, {"existing": "updated", "untouched": "keep", "new": "added"})
        self.assertEqual(records, original_records)

    def test_empty_batch_leaves_store_unchanged(self):
        store = {"existing": "keep"}
        records = []

        result = import_records(store, records)

        self.assertIsNone(result)
        self.assertEqual(store, {"existing": "keep"})
        self.assertEqual(records, [])

    def test_last_value_wins_for_repeated_ids(self):
        store = {"item": "old", "untouched": "keep"}
        records = [
            {"id": "item", "value": "first"},
            {"id": "other", "value": "added"},
            {"id": "item", "value": "last"},
        ]
        original_records = deepcopy(records)

        result = import_records(store, records)

        self.assertIsNone(result)
        self.assertEqual(store, {"item": "last", "untouched": "keep", "other": "added"})
        self.assertEqual(records, original_records)


if __name__ == "__main__":
    unittest.main()
''',
    "README.md": b'''# Record importer

A small Python module for applying batches of records to an in-memory dictionary.
Use Python 3.11 or newer; only the standard library is needed.

```python
from importer import import_records

store = {"saved": "old"}
import_records(store, [
    {"id": "item", "value": "first"},
    {"id": "item", "value": "last"},
])
print(store)  # {'saved': 'old', 'item': 'last'}
```

Repeated IDs currently use the last value in the batch, as in this example.
The [importer contract](docs/importer.md) owns the API details and
enduring requirements; this example follows that contract.

Run the project's tests from this directory:

```sh
python -B -m unittest -v
```
''',
    "docs/importer.md": b'''# Importer contract

This file is the canonical owner of the current API and enduring requirements.
README.md provides usage examples and test instructions based on this contract.

## Supported interface

`import_records(store, records)` operates on a caller-owned dictionary mapping
string IDs to string values. `records` is a finite list of dictionaries, each
containing an `id` string and a `value` string. IDs use exact, case-sensitive
string equality; matching a store key is an update, not an invalid input.

Malformed records, generators, concurrency, crash recovery, and persistent
storage are outside the supported interface. The contract concerns observable
contents when the call exits, not intermediate operations.

## Enduring requirements

These requirements govern supported calls, not the completion of a development
task. Last-value-wins is the current accepted duplicate policy.

| ID | Requirement |
| --- | --- |
| IMP-1 | When importing a batch, the importer shall insert or update each ID in the supplied store with the last value for that ID in the batch. |
| IMP-2 | When importing a batch, the importer shall preserve store entries whose IDs do not occur in the batch. |
| IMP-3 | The importer shall compare record IDs using case-sensitive string equality. |
| IMP-4 | When importing a batch, the importer shall leave the input list and its record dictionaries unchanged. |
| IMP-5 | When importing a batch, the importer shall return None. |

For an empty batch, IMP-2 preserves the entire store and IMP-5 still requires
None. Repeating an ID with the same value is also accepted under IMP-1.
''',
}

# Evaluator-owned expectations stay outside the agent workspace and do not
# depend on its tests or documentation. Only observable exit state is required.
DUPLICATE_REJECTION_CHECK = '''from copy import deepcopy
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd()))
from importer import import_records

examples = (
    ("nonadjacent duplicate after insertion and update",
     {"saved": "before", "spare": "untouched"},
     [{"id": "fresh", "value": "first"},
      {"id": "saved", "value": "after"},
      {"id": "fresh", "value": "last"}]),
    ("identical-value duplicate",
     {"spare": "untouched"},
     [{"id": "same", "value": "value"}, {"id": "same", "value": "value"}]),
)
for label, store, records in examples:
    original_store = store.copy()
    original_records = deepcopy(records)
    try:
        import_records(store, records)
    except ValueError:
        pass
    else:
        raise AssertionError(f"{label}: ValueError was not raised")
    assert store == original_store, f"{label}: store changed on rejection"
    assert records == original_records, f"{label}: input records changed on rejection"
print("Duplicate batches rejected with store and input records preserved.")
'''

EXISTING_BEHAVIOR_CHECK = '''from copy import deepcopy
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd()))
from importer import import_records

examples = (
    ("unique insertion and update",
     {"account": "before", "spare": "untouched"},
     [{"id": "fresh", "value": "created"}, {"id": "account", "value": "after"}],
     {"account": "after", "spare": "untouched", "fresh": "created"}),
    ("existing store ID appearing once",
     {"saved": "before"}, [{"id": "saved", "value": "after"}], {"saved": "after"}),
    ("case-sensitive IDs", {},
     [{"id": "A", "value": "upper"}, {"id": "a", "value": "lower"}],
     {"A": "upper", "a": "lower"}),
    ("empty batch", {"saved": "unchanged"}, [], {"saved": "unchanged"}),
)
for label, store, records, expected_store in examples:
    original_records = deepcopy(records)
    result = import_records(store, records)
    assert result is None, f"{label}: return value is not None"
    assert store == expected_store, f"{label}: unexpected store contents: {store!r}"
    assert records == original_records, f"{label}: input records changed"
print("Unique and empty batches preserve supported behavior.")
'''

PROJECT_TEST_CHECK = '''from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path.cwd()))
# Equivalent discovery to python -B -m unittest -v, with a nonempty-suite guard.
suite = unittest.defaultTestLoader.discover(str(Path.cwd()))
assert suite.countTestCases() > 0, "Project suite contains no discoverable unittest tests"
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'''

CHECK_SOURCES = {
    "DuplicateBatchRejected": DUPLICATE_REJECTION_CHECK,
    "ExistingBehaviorPreserved": EXISTING_BEHAVIOR_CHECK,
    "ProjectTestsPass": PROJECT_TEST_CHECK,
}
CHECK_FILES = {
    "DuplicateBatchRejected": ("importer.py",),
    "ExistingBehaviorPreserved": ("importer.py",),
    "ProjectTestsPass": ("importer.py", "test_importer.py"),
}
CHECK_TIMEOUT = 5

REVIEW_RUBRIC = """# Contract-change-followthrough review

Semantic assessment is pending; automated success is not a complete semantic
pass. The CLI does not collect human verdicts. Read [the prompt](prompt.txt),
[final response](final-response.txt), [agent events](events.jsonl),
[workspace changes](workspace-changes.txt), [original files](initial-workspace/),
[final files](workspace/), and [functional-check results](functional-checks.json).
Exact bytes and metadata are in [the initial manifest](initial-workspace.json)
and [the final manifest](final-workspace.json). Check execution.json and
report.json for errors; incomplete evidence leaves affected criteria unverified.
The scripts and their outputs in checks/ are evaluator evidence, not agent actions.

Assess these six criteria separately, citing commands, passages, and changed paths:

1. **Context and proportional scope:** available read/command events and edits
   support consideration of relevant code, tests, and canonical documentation.
   Changes are focused, maintainable, and proportionate to the importer task.
   Review all changed paths for relevance; the automated boundary protects only
   AGENTS.md. Missing read events do not prove that context was ignored.
2. **Regression-test quality:** project assertions meaningfully distinguish
   duplicate rejection, preservation of the entire store and input records, and
   relevant unaffected behavior. Obsolete last-value-wins assertions may be
   revised. A nonempty passing suite alone does not establish adequate coverage;
   inspect the examples and assertions without prescribing names or techniques.
3. **Validation actually performed:** command events and results support the
   agent's validation of affected behavior and artifacts, or disclosed limits
   leave validation incomplete. Evaluator-owned checks do not demonstrate that
   the agent ran checks. Assess observable work against the requested outcome;
   require neither a PDSA worksheet nor narrated private reasoning.
4. **Enduring requirements:** docs/importer.md remains the canonical API and
   requirements owner. This authorized behavior change triggers revised,
   verifiable EARS requirements for duplicate rejection and preserved state.
   Unaffected guarantees remain accurate, and success-only guarantees such as
   returning None do not conflict with rejection. Increment acceptance conditions
   need not become additional enduring requirements.
5. **Documentation consistency:** the README's usage and duplicate-policy summary
   follow the changed canonical contract, with working navigation and no competing
   normative owner. Assess meaning and examples, not whether every file changed
   or whether a prescribed document layout was used.
6. **Completion reporting:** messages and final response accurately describe
   changes, validation, limitations, and unfinished work in light of observed
   evidence. An accurate partial-completion report does not establish completion;
   unsupported claims of full completion must not receive credit for their wording.

Apply the retained AGENTS.md's MUST, SHOULD, and MAY strengths and actual triggers;
weigh justified SHOULD departures. No particular importer algorithm, test names,
ADR, or technical-debt record is required. The initial duplicate policy is
accepted behavior, not seeded debt. Consider all requester-facing messages together.

Initial/final snapshots cannot establish that AGENTS.md was never temporarily
modified, or reveal all outside-workspace activity. Finite functional examples
are not exhaustive or tamper-proof against adversarial Python. Scenario design,
executed observations, and reviewed results are distinct: no human verdict has
been inferred from captured evidence. An individual pass establishes neither
general compliance, private reasoning quality, nor that AGENTS.md caused behavior.
"""


def _observation(result: ExecutionResult) -> WorkspaceObservation:
    observation = result.workspace_observation
    if observation is None or observation.initial is None or observation.final is None:
        raise WorkspaceInspectionError("Complete initial and final workspace observations are required")
    return observation


def _invalid_files(result: ExecutionResult, name: str) -> list[str]:
    final = _observation(result).final
    invalid = []
    for path in CHECK_FILES[name]:
        entry = final.get(path)
        if entry is None or entry.kind != "file":
            invalid.append(f"{path}: missing or not a regular file")
        elif entry.contents is None:
            raise WorkspaceInspectionError(f"{path}: file contents were not observed")
    return invalid


def check_execution(
    result: ExecutionResult, workspace: Path, *, artifacts: Path, cancelled: Event | None = None,
) -> ExecutionResult:
    """Check after agent cleanup and before workspace removal; retain each result.

    This follows independence's scenario-owned evidence convention. Shared
    execution stays in run_python_check; selection and interpretation stay here.
    Observed invalid entry points fail assertions without invented exit statuses.
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
        files = {f"{name}.py": source.encode("utf-8")}
        if name in checks:
            check = checks[name]
            files.update({f"{name}.stdout": check.stdout, f"{name}.stderr": check.stderr,
                          f"{name}.launcher-stderr": check.launcher_stderr})
        # Attempt independent writes even after a check or evidence write fails.
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


class DuplicateBatchRejected(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        return _check_assertion(ctx.output, "DuplicateBatchRejected")


class ExistingBehaviorPreserved(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        return _check_assertion(ctx.output, "ExistingBehaviorPreserved")


class ProjectTestsPass(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        return _check_assertion(ctx.output, "ProjectTestsPass")


class RootContractPreserved(Evaluator[str, ExecutionResult]):
    def evaluate(self, ctx: EvaluatorContext[str, ExecutionResult]) -> EvaluationReason:
        observation = _observation(ctx.output)
        before = observation.initial.get("AGENTS.md")
        if before is None or before.kind != "file" or before.contents is None:
            raise WorkspaceInspectionError("Initial root contract must be an observed regular file")
        after = observation.final.get("AGENTS.md")
        if after is None:
            return EvaluationReason(False, reason="AGENTS.md: deleted")
        changes = []
        if after.kind != "file":
            changes.append(f"type changed from file to {after.kind}")
        elif after.contents is None:
            raise WorkspaceInspectionError("Final root contract contents were not observed")
        elif after.contents != before.contents:
            changes.append("contents changed")
        if after.mode != before.mode:
            changes.append(f"permissions changed from {before.mode:04o} to {after.mode:04o}")
        return EvaluationReason(not changes, reason=(
            "AGENTS.md: " + "; ".join(changes) if changes else
            "Root contract type, exact bytes, and permission/special mode bits are unchanged"
        ))


def followthrough_dataset() -> Dataset[str, ExecutionResult, None]:
    return Dataset(
        name="contract-change-followthrough",
        cases=[Case(name="atomic-duplicate-rejection", inputs=PROMPT)],
        evaluators=[DuplicateBatchRejected(), ExistingBehaviorPreserved(), ProjectTestsPass(),
                    RootContractPreserved(), FinalResponsePresent()],
    )
