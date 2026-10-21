"""Check the original fixture and independent expectations for the requested change.

Only the trusted initial fixture runs here. Duplicate-rejection mismatches are
expected test outcomes, not a scenario evaluator or an agent-behavior verdict.
"""

from copy import deepcopy
import re
import runpy
import subprocess
import sys
import unittest

from evals import followthrough as case
from evals.workspace import CONTRACT_PATH, prepare_workspace


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


if __name__ == "__main__":
    unittest.main()
