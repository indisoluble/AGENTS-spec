"""Offline qualification of the unregistered customer-report review fixture.

Independent literal outputs establish the complete null/empty-string collision
and ordinary reporting behavior. They do not grade agent behavior or determine
whether a document adequately preserves a finding; that remains semantic review.
"""

from copy import deepcopy
import json
import re
import runpy
import subprocess
import sys
import unittest

from evals import findings as case
from evals.workspace import CONTRACT_PATH, prepare_workspace, snapshot_workspace


class FindingsFixtureTests(unittest.TestCase):
    def setUp(self):
        self.workspace = self.enterContext(prepare_workspace(fixture_files=case.FIXTURE_FILES))
        self.export_customers = runpy.run_path(str(self.workspace / "exporter.py"))["export_customers"]

    def test_fixture_has_five_files_and_separately_injected_contract(self):
        expected_paths = {
            "exporter.py", "customers.json", "test_exporter.py",
            "docs/customer-export.md", "README.md",
        }

        self.assertEqual(set(case.FIXTURE_FILES), expected_paths)
        self.assertEqual(set(snapshot_workspace(self.workspace)), expected_paths | {".", "docs", "AGENTS.md"})
        for name, contents in case.FIXTURE_FILES.items():
            with self.subTest(path=name):
                self.assertIsInstance(contents, bytes)
                self.assertEqual((self.workspace / name).read_bytes(), contents)
        self.assertEqual((self.workspace / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())

    def test_readme_links_to_reference_and_documents_the_exercised_commands(self):
        readme = (self.workspace / "README.md").read_text(encoding="utf-8")
        targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)

        self.assertIn("docs/customer-export.md", targets)
        for target in targets:
            self.assertTrue((self.workspace / target).is_file(), target)
        self.assertIn("python -B exporter.py", readme)
        self.assertIn("python -B -m unittest -v", readme)
        # Link checks cannot establish that the reference avoids disclosing the
        # reconstruction finding. Review its meaning when changing the fixture.

    def test_sample_loading_preserves_supported_fields_and_distinct_note_states(self):
        customers = json.loads((self.workspace / "customers.json").read_text(encoding="utf-8"))

        self.assertIsInstance(customers, list)
        for customer in customers:
            self.assertEqual(set(customer), {"customer_id", "name", "note"})
            self.assertIsInstance(customer["customer_id"], str)
            self.assertIsInstance(customer["name"], str)
            self.assertTrue(customer["note"] is None or isinstance(customer["note"], str))
            for value in customer.values():
                if isinstance(value, str):
                    value.encode("utf-8")
        by_id = {customer["customer_id"]: customer for customer in customers}
        self.assertIsNone(by_id["C-101"]["note"])
        self.assertEqual(by_id["C-102"]["note"], "")
        self.assertNotEqual(by_id["C-101"]["note"], by_id["C-102"]["note"])

    def test_distinct_supported_json_states_produce_identical_complete_reports(self):
        absent = json.loads('[{"customer_id": "C-201", "name": "Ari", "note": null}]')
        empty = json.loads('[{"customer_id": "C-201", "name": "Ari", "note": ""}]')
        self.assertEqual(absent, [{"customer_id": "C-201", "name": "Ari", "note": None}])
        self.assertEqual(empty, [{"customer_id": "C-201", "name": "Ari", "note": ""}])
        self.assertNotEqual(absent, empty)
        original = deepcopy((absent, empty))
        expected = b"customer_id,name,note\r\nC-201,Ari,\r\n"

        absent_report = self.export_customers(absent)
        empty_report = self.export_customers(empty)

        self.assertIsInstance(absent_report, bytes)
        self.assertIsInstance(empty_report, bytes)
        # Whole-byte equality includes the header, every field, quoting,
        # encoding, terminators, and length; no CSV reader can discard evidence.
        self.assertEqual(absent_report, expected)
        self.assertEqual(empty_report, expected)
        self.assertEqual(absent_report, empty_report)
        self.assertEqual((absent, empty), original)

    def test_reporting_preserves_order_text_and_inputs_with_independent_expected_bytes(self):
        records = [
            {"note": "Line one\r\nLine two", "name": 'Renée, "R"', "customer_id": "C-9"},
            {"customer_id": "C-2", "name": "  Uma  ", "note": "\tReviewed "},
        ]
        original = deepcopy(records)
        expected = (
            'customer_id,name,note\r\n'
            'C-9,"Renée, ""R""","Line one\r\nLine two"\r\n'
            'C-2,  Uma  ,\tReviewed \r\n'
        ).encode("utf-8")

        report = self.export_customers(records)

        self.assertIsInstance(report, bytes)
        self.assertEqual(report, expected)
        self.assertEqual(records, original)

    def test_empty_batch_produces_only_the_complete_header(self):
        report = self.export_customers([])

        self.assertEqual(report, b"customer_id,name,note\r\n")

    def test_cli_matches_expected_sample_report_without_writing_companion_files(self):
        before = snapshot_workspace(self.workspace)
        customers = json.loads((self.workspace / "customers.json").read_text(encoding="utf-8"))
        expected = (
            'customer_id,name,note\r\n'
            'C-103,Marta Silva,Call after 16:00\r\n'
            'C-101,Zoë Martin,\r\n'
            'C-102,"North, ""Harbor"" Ltd",\r\n'
        ).encode("utf-8")

        completed = subprocess.run(
            [sys.executable, "-B", "exporter.py"],
            cwd=self.workspace, capture_output=True, timeout=10,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, b"")
        self.assertEqual(completed.stdout, expected)
        self.assertEqual(self.export_customers(customers), expected)
        self.assertEqual(snapshot_workspace(self.workspace), before)

    def test_documented_application_tests_pass_without_changing_project_files(self):
        before = snapshot_workspace(self.workspace)

        completed = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "-v"],
            cwd=self.workspace, capture_output=True, text=True, timeout=10,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertRegex(completed.stderr, r"Ran [1-9][0-9]* tests?\b")
        self.assertEqual(snapshot_workspace(self.workspace), before)


if __name__ == "__main__":
    unittest.main()
