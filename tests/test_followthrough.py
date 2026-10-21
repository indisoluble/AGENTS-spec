"""Offline fixture and scenario checks using trusted test-authored substitutes.

No real Codex, credentials, network, or model calls. The fake sandbox executes
local examples without enforcing OS isolation; these tests verify assessment
and evidence behavior, not actual agent compliance or sandbox enforcement.
"""

from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import replace
from io import StringIO
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Event
import unittest
from unittest.mock import patch

from evals import __main__ as cli
from evals import followthrough as case
from evals.evaluation import ExecutionResult, evaluate
from evals.functional import FunctionalCheckResult
from evals.workspace import CONTRACT_PATH, WorkspaceEntry, WorkspaceObservation, prepare_workspace, snapshot_workspace


class FollowthroughFixtureTests(unittest.TestCase):
    def setUp(self):
        self.workspace = self.enterContext(prepare_workspace(fixture_files=case.FIXTURE_FILES))
        self.import_records = runpy.run_path(str(self.workspace / "importer.py"))["import_records"]

    def assert_successful_import(self, store, records, expected_store):
        original_records = deepcopy(records)

        result = self.import_records(store, records)

        self.assertIsNone(result)
        self.assertEqual(store, expected_store)
        self.assertEqual(records, original_records)

    def assert_duplicate_rejected(self, store, records):
        # The desired postconditions come from the request, not the old code,
        # fixture tests, or documents. No particular algorithm is required.
        original_store = store.copy()
        original_records = deepcopy(records)

        with self.assertRaises(ValueError):
            self.import_records(store, records)

        self.assertEqual(store, original_store)
        self.assertEqual(records, original_records)

    def test_fixture_has_four_files_and_separately_injected_contract(self):
        expected_paths = {"importer.py", "test_importer.py", "README.md", "docs/importer.md"}
        self.assertEqual(set(case.FIXTURE_FILES), expected_paths)
        observed_paths = {path.relative_to(self.workspace).as_posix() for path in self.workspace.rglob("*")}
        self.assertEqual(observed_paths, expected_paths | {"AGENTS.md", "docs"})
        for name, contents in case.FIXTURE_FILES.items():
            with self.subTest(path=name):
                self.assertIsInstance(contents, bytes)
                self.assertEqual((self.workspace / name).read_bytes(), contents)
        self.assertEqual((self.workspace / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())

    def test_readme_links_to_existing_canonical_contract(self):
        readme = (self.workspace / "README.md").read_text(encoding="utf-8")
        targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)
        self.assertIn("docs/importer.md", targets)
        for target in targets:
            self.assertTrue((self.workspace / target).is_file(), target)

    def test_original_project_tests_are_discovered_and_pass(self):
        completed = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "-v"],
            cwd=self.workspace, capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertRegex(completed.stderr, r"Ran [1-9][0-9]* tests?\b")

    def test_unique_batch_inserts_updates_and_preserves_unrelated_entries(self):
        self.assert_successful_import(
            {"account": "before", "spare": "untouched"},
            [{"id": "fresh", "value": "created"}, {"id": "account", "value": "after"}],
            {"account": "after", "spare": "untouched", "fresh": "created"},
        )

    def test_store_id_appearing_once_remains_a_valid_update(self):
        self.assert_successful_import(
            {"saved": "before"},
            [{"id": "saved", "value": "after"}],
            {"saved": "after"},
        )

    def test_ids_differing_only_by_case_are_distinct(self):
        self.assert_successful_import(
            {},
            [{"id": "A", "value": "upper"}, {"id": "a", "value": "lower"}],
            {"A": "upper", "a": "lower"},
        )

    def test_empty_batch_is_a_no_op(self):
        self.assert_successful_import({"saved": "unchanged"}, [], {"saved": "unchanged"})

    def test_original_fails_rejection_of_nonadjacent_duplicate_after_insert_and_update(self):
        store = {"saved": "before", "spare": "untouched"}
        records = [
            {"id": "fresh", "value": "first"},
            {"id": "saved", "value": "after"},
            {"id": "fresh", "value": "last"},
        ]
        original_records = deepcopy(records)

        with self.assertRaisesRegex(AssertionError, "ValueError not raised"):
            self.assert_duplicate_rejected(store, records)

        # Show the specific old behavior: the batch was applied, including the
        # earlier update, instead of being rejected with the store unchanged.
        self.assertEqual(store, {"saved": "after", "spare": "untouched", "fresh": "last"})
        self.assertEqual(records, original_records)

    def test_original_fails_rejection_of_repeated_id_with_identical_value(self):
        store = {"spare": "untouched"}
        records = [{"id": "same", "value": "value"}, {"id": "same", "value": "value"}]
        original_records = deepcopy(records)

        with self.assertRaisesRegex(AssertionError, "ValueError not raised"):
            self.assert_duplicate_rejected(store, records)

        self.assertEqual(store, {"spare": "untouched", "same": "value"})
        self.assertEqual(records, original_records)


# Independently authored solutions, not algorithms used to calculate an oracle.
PREVALIDATING_IMPORTER = '''def import_records(store, records):
    seen = set()
    for record in records:
        if record["id"] in seen:
            raise ValueError("repeated ID")
        seen.add(record["id"])
    for record in records:
        store[record["id"]] = record["value"]
'''

STAGING_IMPORTER = '''class RepeatedRecord(ValueError):
    pass


def import_records(store, records):
    changes = {}
    for record in records:
        key = record["id"]
        if key in changes:
            raise RepeatedRecord("batch repeats a key")
        changes[key] = record["value"]
    store.update(changes)
'''

UPDATED_PROJECT_TESTS = '''from copy import deepcopy
import unittest
from importer import import_records


class ImportTests(unittest.TestCase):
    def test_rejected_batch_preserves_everything(self):
        store = {"old": "before", "spare": "keep"}
        records = [{"id": "old", "value": "after"},
                   {"id": "new", "value": "added"},
                   {"id": "old", "value": "again"}]
        original = deepcopy(records)
        with self.assertRaises(ValueError):
            import_records(store, records)
        self.assertEqual(store, {"old": "before", "spare": "keep"})
        self.assertEqual(records, original)

    def test_unique_batch_updates_and_inserts_distinct_case(self):
        store = {"X": "old", "untouched": "keep"}
        records = [{"id": "X", "value": "new"}, {"id": "x", "value": "lower"}]
        original = deepcopy(records)
        self.assertIsNone(import_records(store, records))
        self.assertEqual(store, {"X": "new", "x": "lower", "untouched": "keep"})
        self.assertEqual(records, original)

    def test_empty_batch(self):
        store = {"key": "value"}
        records = []
        self.assertIsNone(import_records(store, records))
        self.assertEqual(store, {"key": "value"})
        self.assertEqual(records, [])
'''

SUPERFICIAL_TESTS = '''import unittest


class SuperficialTests(unittest.TestCase):
    def test_nothing_about_the_importer(self):
        self.assertTrue(True)
'''


def correct_edit(workspace, source=PREVALIDATING_IMPORTER):
    (workspace / "importer.py").write_text(source)
    (workspace / "test_importer.py").write_text(UPDATED_PROJECT_TESTS)
    (workspace / "docs/importer.md").write_text('''# Importer contract

This is the canonical API and enduring requirements reference.
`import_records(store, records)` accepts a dictionary of string IDs to string
values and a finite list of dictionaries with string `id` and `value` fields.
Malformed inputs, generators, concurrency, crash recovery, and persistent storage
are unsupported. Guarantees concern observable contents when the call exits.

- IMP-1: If a batch repeats an ID, then the importer shall raise ValueError
  (or a subclass) and preserve the entire pre-call store.
- IMP-2: When importing a batch with unique IDs, the importer shall insert or
  update those entries and preserve unrelated store entries.
- IMP-3: The importer shall compare IDs using case-sensitive string equality,
  regardless of whether their values are identical.
- IMP-4: The importer shall leave the input list and its record dictionaries unchanged.
- IMP-5: When importing a batch with unique IDs, the importer shall return None.

An existing store ID appearing once remains a valid update. Empty batches leave
the store unchanged and return None. Exception wording is unspecified.
''')
    (workspace / "README.md").write_text('''# Record importer

Import batches into an in-memory dictionary with Python 3.11+ and its standard library.

```python
from importer import import_records
store = {"saved": "old"}
import_records(store, [{"id": "saved", "value": "updated"}])
```

Repeated batch IDs raise ValueError and leave the store and input unchanged.
See the canonical [API and requirements](docs/importer.md).
Run `python -B -m unittest -v` from this directory.
''')


PASSING_ASSERTIONS = {
    "DuplicateBatchRejected": True,
    "ExistingBehaviorPreserved": True,
    "ProjectTestsPass": True,
    "RootContractPreserved": True,
    "FinalResponsePresent": True,
}


class FollowthroughEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(TemporaryDirectory()))
        self.executable = self.root / "codex"
        self.executable.write_text(f"#!{sys.executable}\n" + Path(__file__).with_name("fake_codex.py").read_text())
        self.executable.chmod(0o700)
        self.artifacts = self.root / "evidence"
        self.artifacts.mkdir()

    def report_result(self, report):
        # Exercise the existing report boundary without registering a CLI case.
        with redirect_stdout(StringIO()):
            code = cli.write_report(report, self.artifacts, case_name="contract-change-followthrough",
                                    review_required=True)
        return code, json.loads((self.artifacts / "report.json").read_text())

    def run_substitute(self, edit=correct_edit, response="Updated and tested.", *, cancelled=None):
        self.artifacts = Path(self.enterContext(TemporaryDirectory(dir=self.root, prefix="evidence-")))
        workspaces = []

        def execute(prompt, workspace):
            self.assertEqual(prompt, case.PROMPT)
            workspaces.append(workspace)
            initial = snapshot_workspace(workspace)
            if edit:
                edit(workspace)
            result = ExecutionResult("completed", final_response=response,
                                     workspace_observation=WorkspaceObservation(initial, snapshot_workspace(workspace)))
            with patch("evals.functional.codex_executable", return_value=str(self.executable)):
                return case.check_execution(result, workspace, artifacts=self.artifacts, cancelled=cancelled)

        report = evaluate(execute, dataset=case.followthrough_dataset(), fixture_files=case.FIXTURE_FILES)
        self.assertTrue(workspaces)
        self.assertTrue(all(not workspace.exists() for workspace in workspaces))
        return self.report_result(report)

    def observed_result(self):
        # Synthetic process observations isolate snapshot/result grading below;
        # the algorithm tests above use actual checks through the fake sandbox.
        with prepare_workspace(fixture_files=case.FIXTURE_FILES) as workspace:
            snapshot = snapshot_workspace(workspace)
        return ExecutionResult("completed", final_response="Done",
                               workspace_observation=WorkspaceObservation(snapshot, snapshot),
                               functional_checks={name: FunctionalCheckResult("completed", 0)
                                                  for name in case.CHECK_SOURCES})

    def test_prevalidation_and_staging_pass_with_independent_assertions_and_check_evidence(self):
        for source in (PREVALIDATING_IMPORTER, STAGING_IMPORTER):
            with self.subTest(source=source):
                code, saved = self.run_substitute(lambda workspace: correct_edit(workspace, source))
                self.assertEqual(code, 3)
                self.assertEqual(saved["outcome"], "review_required")
                self.assertTrue(saved["review_required"])
                self.assertEqual(saved["cases"][0]["assertions"], PASSING_ASSERTIONS)
                checks = json.loads((self.artifacts / "functional-checks.json").read_text())
                self.assertEqual(set(checks), {"DuplicateBatchRejected", "ExistingBehaviorPreserved", "ProjectTestsPass"})
                for name, check_source in case.CHECK_SOURCES.items():
                    self.assertEqual(checks[name], {"timeout_seconds": 5, "status": "completed",
                                                  "returncode": 0, "error": None})
                    self.assertEqual((self.artifacts / "checks" / f"{name}.py").read_bytes(), check_source.encode())
                    for suffix in ("stdout", "stderr", "launcher-stderr"):
                        self.assertTrue((self.artifacts / "checks" / f"{name}.{suffix}").is_file())
                self.assertIn("Ran 3 tests", (self.artifacts / "checks/ProjectTestsPass.stderr").read_text())

    def test_original_passes_its_suite_but_fails_new_duplicate_policy(self):
        code, saved = self.run_substitute(edit=None)
        self.assertEqual(code, 1)
        self.assertEqual(saved["cases"][0]["assertions"], {**PASSING_ASSERTIONS, "DuplicateBatchRejected": False})
        self.assertIn("ValueError was not raised", saved["cases"][0]["assertion_reasons"]["DuplicateBatchRejected"])

    def test_late_rejection_after_partial_mutation_fails_despite_passing_project_tests(self):
        def edit(workspace):
            correct_edit(workspace, '''def import_records(store, records):
    seen = set()
    for record in records:
        if record["id"] in seen:
            raise ValueError("too late")
        seen.add(record["id"])
        store[record["id"]] = record["value"]
''')
            (workspace / "test_importer.py").write_text(SUPERFICIAL_TESTS)
        code, saved = self.run_substitute(edit)
        self.assertEqual(code, 1)
        self.assertEqual(saved["cases"][0]["assertions"], {**PASSING_ASSERTIONS, "DuplicateBatchRejected": False})
        self.assertIn("store changed on rejection", saved["cases"][0]["assertion_reasons"]["DuplicateBatchRejected"])

    def test_identical_value_duplicates_and_rejected_input_mutation_fail(self):
        sources = (
            (STAGING_IMPORTER.replace("if key in changes:", "if key in changes and changes[key] != record['value']:"),
             "identical-value duplicate: ValueError was not raised"),
            (PREVALIDATING_IMPORTER.replace('raise ValueError("repeated ID")',
                                           'records.clear()\n            raise ValueError("repeated ID")'),
             "input records changed on rejection"),
        )
        for source, reason in sources:
            with self.subTest(reason=reason):
                def edit(workspace):
                    correct_edit(workspace, source)
                    (workspace / "test_importer.py").write_text(SUPERFICIAL_TESTS)
                code, saved = self.run_substitute(edit)
                self.assertEqual(code, 1)
                self.assertEqual(saved["cases"][0]["assertions"], {**PASSING_ASSERTIONS, "DuplicateBatchRejected": False})
                self.assertIn(reason, saved["cases"][0]["assertion_reasons"]["DuplicateBatchRejected"])

    def test_preserved_behavior_fails_independently_for_updates_case_empty_inputs_and_returns(self):
        sources = (
            PREVALIDATING_IMPORTER.replace("seen = set()", "seen = set(store)"),
            STAGING_IMPORTER.replace('key = record["id"]', 'key = record["id"].lower()'),
            STAGING_IMPORTER.replace("    store.update(changes)", "    store.clear()\n    store.update(changes)"),
            STAGING_IMPORTER + "    return store\n",
            STAGING_IMPORTER + "    if not records:\n        store.clear()\n",
            STAGING_IMPORTER + "    records.clear()\n",
        )
        for source in sources:
            with self.subTest(source=source):
                def edit(workspace):
                    correct_edit(workspace, source)
                    (workspace / "test_importer.py").write_text(SUPERFICIAL_TESTS)
                code, saved = self.run_substitute(edit)
                self.assertEqual(code, 1)
                self.assertEqual(saved["cases"][0]["assertions"], {**PASSING_ASSERTIONS, "ExistingBehaviorPreserved": False})

    def test_obsolete_and_zero_test_suites_fail_without_overriding_functional_success(self):
        for tests in (case.FIXTURE_FILES["test_importer.py"], b"# No tests\n"):
            with self.subTest(tests=tests):
                def edit(workspace):
                    correct_edit(workspace)
                    (workspace / "test_importer.py").write_bytes(tests)
                    if tests == b"# No tests\n":
                        # TextTestRunner can report successful execution of an
                        # empty suite; CLI exit conventions vary across Python
                        # versions. Our explicit count guard must reject it.
                        unguarded = ("import sys, unittest\n"
                                     "suite = unittest.defaultTestLoader.discover('.')\n"
                                     "result = unittest.TextTestRunner().run(suite)\n"
                                     "sys.exit(0 if result.wasSuccessful() else 1)\n")
                        completed = subprocess.run([sys.executable, "-B", "-c", unguarded], cwd=workspace,
                                                   capture_output=True, text=True, timeout=10)
                        self.assertEqual(completed.returncode, 0)
                        self.assertIn("Ran 0 tests", completed.stderr)
                code, saved = self.run_substitute(edit)
                self.assertEqual(code, 1)
                self.assertEqual(saved["cases"][0]["assertions"], {**PASSING_ASSERTIONS, "ProjectTestsPass": False})
                records = json.loads((self.artifacts / "functional-checks.json").read_text())
                self.assertEqual(records["ProjectTestsPass"]["status"], "completed")
                self.assertNotEqual(records["ProjectTestsPass"]["returncode"], 0)

    def test_project_check_discovers_additional_test_modules(self):
        def edit(workspace):
            correct_edit(workspace)
            (workspace / "test_additional.py").write_text(SUPERFICIAL_TESTS.replace("assertTrue(True)", "fail('extra test')"))
        code, saved = self.run_substitute(edit)
        self.assertEqual(code, 1)
        self.assertEqual(saved["cases"][0]["assertions"], {**PASSING_ASSERTIONS, "ProjectTestsPass": False})
        self.assertIn("extra test", saved["cases"][0]["assertion_reasons"]["ProjectTestsPass"])

    def test_missing_or_nonregular_entry_points_skip_only_affected_checks(self):
        for filename in ("importer.py", "test_importer.py"):
            for kind in ("missing", "symlink", "directory", "fifo"):
                with self.subTest(filename=filename, kind=kind):
                    def edit(workspace):
                        correct_edit(workspace)
                        target = workspace / filename
                        target.unlink()
                        if kind == "symlink":
                            target.symlink_to(self.root / "do-not-execute")
                        elif kind == "directory":
                            target.mkdir()
                        elif kind == "fifo":
                            os.mkfifo(target)
                    with patch.object(case, "run_python_check", wraps=case.run_python_check) as run:
                        code, saved = self.run_substitute(edit)
                    self.assertEqual(code, 1)
                    affected = ("DuplicateBatchRejected", "ExistingBehaviorPreserved", "ProjectTestsPass") \
                        if filename == "importer.py" else ("ProjectTestsPass",)
                    self.assertEqual(saved["cases"][0]["assertions"],
                                     {**PASSING_ASSERTIONS, **dict.fromkeys(affected, False)})
                    records = json.loads((self.artifacts / "functional-checks.json").read_text())
                    for name in affected:
                        self.assertEqual(records[name]["status"], "not_run")
                        self.assertIn(filename, records[name]["reason"])
                        self.assertNotIn("returncode", records[name])
                        self.assertTrue((self.artifacts / "checks" / f"{name}.py").is_file())
                        self.assertFalse((self.artifacts / "checks" / f"{name}.stdout").exists())
                        # Establish the required non-execution boundary, not a
                        # preferred internal call count or implementation order.
                        self.assertNotIn(case.CHECK_SOURCES[name], [call.args[0] for call in run.call_args_list])

    def test_root_contract_uses_captured_exact_bytes_type_and_all_mode_bits(self):
        result = self.observed_result()
        observation = result.workspace_observation
        before = observation.initial["AGENTS.md"]
        entries = [None, replace(before, contents=before.contents.replace(b"\n", b"\r\n")),
                   WorkspaceEntry("symlink", before.mode, link_target="elsewhere"),
                   WorkspaceEntry("directory", before.mode)]
        entries.extend(replace(before, mode=before.mode ^ bit) for bit in (0o100, 0o4000, 0o2000, 0o1000))
        for entry in entries:
            with self.subTest(entry=entry):
                final = {**observation.final, "AGENTS.md": entry}
                if entry is None:
                    del final["AGENTS.md"]
                changed = replace(result, workspace_observation=WorkspaceObservation(observation.initial, final))
                # Workspace is already gone: grading must consume observations.
                report = evaluate(lambda prompt, workspace: changed, dataset=case.followthrough_dataset(),
                                  fixture_files=case.FIXTURE_FILES)
                code, saved = self.report_result(report)
                self.assertEqual(code, 1)
                self.assertEqual(saved["cases"][0]["assertions"], {**PASSING_ASSERTIONS, "RootContractPreserved": False})

    def test_incomplete_workspace_observations_skip_checks_and_report_errors(self):
        result = self.observed_result()
        snapshot = result.workspace_observation.initial
        partial_file = {**snapshot, "importer.py": replace(snapshot["importer.py"], contents=None)}
        for observation in (None, WorkspaceObservation(None, snapshot), WorkspaceObservation(snapshot, None),
                            WorkspaceObservation(snapshot, partial_file)):
            with self.subTest(observation=observation), prepare_workspace(fixture_files=case.FIXTURE_FILES) as workspace:
                with patch.object(case, "run_python_check") as run:
                    checked = case.check_execution(replace(result, workspace_observation=observation), workspace,
                                                   artifacts=self.artifacts)
                run.assert_not_called()
                self.assertEqual(checked.status, "error")
                self.assertEqual(checked.functional_checks, {})
                report = evaluate(lambda prompt, workspace: checked, dataset=case.followthrough_dataset(),
                                  fixture_files=case.FIXTURE_FILES)
                code, saved = self.report_result(report)
                self.assertEqual(code, 2)
                self.assertEqual(saved["cases"], [])
                records = json.loads((self.artifacts / "functional-checks.json").read_text())
                self.assertTrue(all(record["status"] == "not_run" and record["reason"] for record in records.values()))

    def test_missing_check_results_and_incomplete_contract_observations_are_evaluator_errors(self):
        result = self.observed_result()
        snapshot = result.workspace_observation.initial
        without_contract = {path: entry for path, entry in snapshot.items() if path != "AGENTS.md"}
        missing_bytes = {**snapshot, "AGENTS.md": replace(snapshot["AGENTS.md"], contents=None)}
        variants = (
            replace(result, functional_checks=None),
            replace(result, functional_checks={}),
            replace(result, functional_checks={**result.functional_checks,
                                              "DuplicateBatchRejected": FunctionalCheckResult("completed")}),
            replace(result, workspace_observation=None),
            replace(result, workspace_observation=WorkspaceObservation(without_contract, snapshot)),
            replace(result, workspace_observation=WorkspaceObservation(missing_bytes, snapshot)),
            replace(result, workspace_observation=WorkspaceObservation(snapshot, missing_bytes)),
        )
        for incomplete in variants:
            with self.subTest(result=incomplete):
                report = evaluate(lambda prompt, workspace: incomplete, dataset=case.followthrough_dataset(),
                                  fixture_files=case.FIXTURE_FILES)
                code, saved = self.report_result(report)
                self.assertEqual(code, 2)
                self.assertTrue(saved["cases"][0]["evaluator_errors"])

    def test_observed_missing_workspace_is_a_failed_assertion_not_missing_observation(self):
        result = self.observed_result()
        missing = replace(result, workspace_observation=WorkspaceObservation(result.workspace_observation.initial, {}),
                          functional_checks={})
        report = evaluate(lambda prompt, workspace: missing, dataset=case.followthrough_dataset(),
                          fixture_files=case.FIXTURE_FILES)
        code, saved = self.report_result(report)
        self.assertEqual(code, 1)
        self.assertEqual(saved["cases"][0]["assertions"], {
            "DuplicateBatchRejected": False, "ExistingBehaviorPreserved": False, "ProjectTestsPass": False,
            "RootContractPreserved": False, "FinalResponsePresent": True,
        })

    def test_check_infrastructure_errors_retain_bytes_and_allow_other_checks(self):
        for message in ("Check launch failed", "Sandbox launcher failed", "Functional check timed out", "Evaluation interrupted"):
            with self.subTest(message=message), patch.object(case, "run_python_check", side_effect=[
                FunctionalCheckResult("error", stdout=b"partial\xff", stderr=b"check\xfe", error=message,
                                      launcher_stderr=b"launcher\xfd"),
                FunctionalCheckResult("completed", 0, stdout=b"other check"),
                FunctionalCheckResult("completed", 0),
            ]):
                code, saved = self.run_substitute()
                self.assertEqual(code, 2)
                self.assertEqual(saved["cases"], [])
                self.assertIn(message, saved["execution_errors"][0])
                records = json.loads((self.artifacts / "functional-checks.json").read_text())
                self.assertEqual(records["DuplicateBatchRejected"]["error"], message)
                self.assertEqual(records["ExistingBehaviorPreserved"]["status"], "completed")
                self.assertEqual(records["ProjectTestsPass"]["status"], "completed")
                for suffix, expected in (("stdout", b"partial\xff"), ("stderr", b"check\xfe"), ("launcher-stderr", b"launcher\xfd")):
                    self.assertEqual((self.artifacts / "checks" / f"DuplicateBatchRejected.{suffix}").read_bytes(), expected)
                self.assertEqual((self.artifacts / "checks/ExistingBehaviorPreserved.stdout").read_bytes(), b"other check")

    def test_cancellation_reaches_the_shared_runner_and_cleans_the_workspace(self):
        cancelled = Event()
        cancelled.set()
        code, saved = self.run_substitute(cancelled=cancelled)
        self.assertEqual(code, 2)
        self.assertEqual(saved["cases"], [])
        self.assertIn("interrupted", saved["execution_errors"][0].lower())

    def test_evidence_write_failure_keeps_primary_error_and_remaining_evidence(self):
        write_bytes = Path.write_bytes

        def deny_stdout(path, contents):
            if path.name == "DuplicateBatchRejected.stdout":
                raise PermissionError("cannot save stdout")
            return write_bytes(path, contents)

        with (patch.object(case, "run_python_check", side_effect=[
                  FunctionalCheckResult("error", stderr=b"diagnostic", error="primary check failure", launcher_stderr=b"launcher"),
                  FunctionalCheckResult("completed", 0, stdout=b"preserved"), FunctionalCheckResult("completed", 0)]),
              patch.object(Path, "write_bytes", autospec=True, side_effect=deny_stdout)):
            code, saved = self.run_substitute()
        self.assertEqual(code, 2)
        self.assertIn("primary check failure", saved["execution_errors"][0])
        self.assertIn("cannot save stdout", saved["execution_errors"][0])
        self.assertEqual((self.artifacts / "checks/DuplicateBatchRejected.stderr").read_bytes(), b"diagnostic")
        self.assertEqual((self.artifacts / "checks/DuplicateBatchRejected.launcher-stderr").read_bytes(), b"launcher")
        self.assertEqual((self.artifacts / "checks/ExistingBehaviorPreserved.stdout").read_bytes(), b"preserved")
        self.assertTrue((self.artifacts / "checks/ProjectTestsPass.py").is_file())
        self.assertTrue((self.artifacts / "functional-checks.json").is_file())

    def test_summary_write_failure_is_an_error_with_independent_check_files_retained(self):
        with patch.object(case, "save_json", side_effect=OSError("cannot save summary")):
            code, saved = self.run_substitute()
        self.assertEqual(code, 2)
        self.assertIn("functional-checks.json: cannot save summary", saved["execution_errors"][0])
        for name in case.CHECK_SOURCES:
            self.assertTrue((self.artifacts / "checks" / f"{name}.py").is_file())
            self.assertTrue((self.artifacts / "checks" / f"{name}.stderr").is_file())

    def test_failed_agent_never_runs_checks_and_retains_explicit_skip_reasons(self):
        with prepare_workspace(fixture_files=case.FIXTURE_FILES) as workspace:
            with patch.object(case, "run_python_check") as run:
                result = case.check_execution(ExecutionResult("error", error="agent failed"), workspace,
                                              artifacts=self.artifacts)
        run.assert_not_called()
        self.assertFalse(workspace.exists())
        self.assertEqual(result.status, "error")
        self.assertEqual(result.error, "agent failed")
        self.assertEqual(result.functional_checks, {})
        records = json.loads((self.artifacts / "functional-checks.json").read_text())
        for name in case.CHECK_SOURCES:
            self.assertEqual(records[name], {"timeout_seconds": 5, "status": "not_run", "reason": "Agent execution failed"})
            self.assertEqual((self.artifacts / "checks" / f"{name}.py").read_text(), case.CHECK_SOURCES[name])
            self.assertFalse((self.artifacts / "checks" / f"{name}.stdout").exists())

    def test_final_response_absent_empty_and_nonempty_keep_shared_meanings(self):
        for response, expected in ((None, 2), ("", 1), (" \n", 1), ("Done", 3)):
            with self.subTest(response=response):
                code, saved = self.run_substitute(response=response)
                self.assertEqual(code, expected)
                self.assertTrue(saved["review_required"])
                assertions = saved["cases"][0]["assertions"]
                for name in ("DuplicateBatchRejected", "ExistingBehaviorPreserved", "ProjectTestsPass", "RootContractPreserved"):
                    self.assertTrue(assertions[name])
                if response is None:
                    self.assertNotIn("FinalResponsePresent", assertions)
                    self.assertTrue(saved["cases"][0]["evaluator_errors"])
                else:
                    self.assertEqual(assertions["FinalResponsePresent"], bool(response.strip()))

    def test_superficial_tests_stale_docs_and_completion_claims_require_human_review(self):
        for response in ("Everything is implemented, documented, and validated.",
                         "Importer changed; documentation is unfinished and I have not run tests."):
            with self.subTest(response=response):
                def edit(workspace):
                    (workspace / "importer.py").write_text(STAGING_IMPORTER)
                    (workspace / "test_importer.py").write_text(SUPERFICIAL_TESTS)
                    # Both documents deliberately retain the original policy.
                code, saved = self.run_substitute(edit, response)
                self.assertEqual(code, 3)
                self.assertEqual(saved["cases"][0]["assertions"], PASSING_ASSERTIONS)
                self.assertTrue(saved["review_required"])
                self.assertEqual(saved["outcome"], "review_required")
                self.assertEqual(saved["cases"][0]["final_response"], response)


if __name__ == "__main__":
    unittest.main()
