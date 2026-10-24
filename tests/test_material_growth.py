"""Offline checks of the initial fixture, not grading of an evaluated agent.

Loss-of-state assertions characterize the defective starting application. They
stay outside its workspace and must not become requirements for a repaired queue.
No durable-queue acceptance suite or live agent execution is included here.
"""

import re
import runpy
import subprocess
import sys
import unittest

from evals import material_growth as fixture
from evals.workspace import CONTRACT_PATH, prepare_workspace


class MaterialGrowthFixtureTests(unittest.TestCase):
    def setUp(self):
        self.workspace = self.enterContext(prepare_workspace(fixture_files=fixture.FIXTURE_FILES))
        self.JobQueue = runpy.run_path(str(self.workspace / "job_queue.py"))["JobQueue"]

    def test_fixture_preparation_preserves_bytes_and_separately_injects_root_contract(self):
        expected = {"job_queue.py", "test_job_queue.py", "README.md", "docs/job-queue.md"}
        self.assertEqual(set(fixture.FIXTURE_FILES), expected)
        paths = {path.relative_to(self.workspace).as_posix() for path in self.workspace.rglob("*")}
        self.assertEqual(paths, expected | {"AGENTS.md", "docs"})
        for name, contents in fixture.FIXTURE_FILES.items():
            with self.subTest(path=name):
                self.assertIsInstance(contents, bytes)
                self.assertEqual((self.workspace / name).read_bytes(), contents)
        self.assertEqual((self.workspace / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())

    def test_application_docs_link_to_canonical_contract_and_existing_files(self):
        readme = (self.workspace / "README.md").read_text(encoding="utf-8")
        self.assertIn("[application contract](docs/job-queue.md)", readme)
        for name in ("README.md", "docs/job-queue.md"):
            path = self.workspace / name
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                with self.subTest(document=name, target=target):
                    self.assertTrue((path.parent / target).is_file())
        contract = (self.workspace / "docs/job-queue.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^\| (JQ-\d+) \|", contract, re.MULTILINE),
                         [f"JQ-{number}" for number in range(1, 11)])
        for statement in ("file-backed SQLite", "30 seconds", "at most 3 attempts",
                          "not exactly-once external side effects", "Current implementation and known gaps"):
            self.assertIn(statement, contract)

    def test_existing_sequential_application_tests_are_discovered_and_pass(self):
        completed = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "-v"],
            cwd=self.workspace, capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertRegex(completed.stderr, r"Ran [1-9][0-9]* tests?\b")

    def test_starting_implementation_loses_every_job_state_on_reopening(self):
        # These are fixture-defect checks, deliberately absent from test_job_queue.py.
        for state, attempts, action in (
            ("pending", 0, None), ("leased", 1, None), ("pending", 1, "fail"),
            ("completed", 1, "ack"), ("exhausted", 3, "fail"),
        ):
            with self.subTest(state=state, attempts=attempts):
                path = self.workspace / "jobs.sqlite3"
                queue = self.JobQueue(path, clock=lambda: 1000.0)
                queue.submit("job", {"message": "retained only in memory"})
                for _ in range(attempts):
                    lease = queue.claim("worker")
                    if action is not None:
                        self.assertIs(getattr(queue, action)("job", lease["token"]), True)
                self.assertEqual(queue.status("job"), {"state": state, "attempts": attempts})

                del queue
                reopened = self.JobQueue(path, clock=lambda: 1001.0)

                self.assertIsNone(reopened.status("job"))
                self.assertIsNone(reopened.claim("replacement"))
                self.assertFalse(path.exists(), "The initial fixture must not create a durable store")
                reopened.submit("job", "resubmitted")
                self.assertEqual(reopened.claim("replacement")["token"], 1)

    def test_starting_instances_do_not_share_work_or_coordinate_leases(self):
        path = self.workspace / "jobs.sqlite3"
        first = self.JobQueue(path, clock=lambda: 1000.0)
        second = self.JobQueue(path, clock=lambda: 1000.0)
        first.submit("job", "work")
        self.assertIsNone(second.status("job"))
        self.assertIsNone(second.claim("second"))

        second.submit("job", "work")
        first_lease = first.claim("first")
        second_lease = second.claim("second")

        self.assertEqual(first_lease, second_lease)
        self.assertIs(first.ack("job", first_lease["token"]), True)
        self.assertIs(second.ack("job", second_lease["token"]), True)

    def test_fixture_uses_existing_workspace_lifecycle(self):
        with prepare_workspace(fixture_files=fixture.FIXTURE_FILES) as workspace:
            self.assertTrue((workspace / "job_queue.py").is_file())
            self.assertTrue((workspace / "docs/job-queue.md").is_file())
        self.assertFalse(workspace.exists())


if __name__ == "__main__":
    unittest.main()
