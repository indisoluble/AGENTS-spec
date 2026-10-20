from contextlib import redirect_stdout
from io import StringIO
import unittest

from pydantic_evals import Case, Dataset

from evals.evaluation import ExecutionResult, read_result
from evals.smoke import PROMPT, evaluate
from evals.workspace import CONTRACT_PATH
from tests.offline_smoke import write_after


# unittest checks our evaluation infrastructure using predictable task substitutes.
class SmokeEvaluationTests(unittest.TestCase):
    def test_correct_file_passes(self):
        report = evaluate(write_after)

        # failures holds execution errors; assertions holds the grading results.
        self.assertEqual(report.failures, [])
        self.assertEqual(len(report.cases), 1)
        self.assertTrue(report.cases[0].assertions["ExactFileContents"].value)
        self.assertEqual(report.cases[0].output.file_contents, "after\n")

    def test_incorrect_or_unchanged_content_fails_exact_comparison(self):
        for contents in (b"wrong\n", b"before\n", b"after", b"after\r\n", b"after\n\n"):
            with self.subTest(contents=contents):
                def write_content(prompt, workspace):
                    (workspace / "message.txt").write_bytes(contents)
                    return read_result(workspace)

                report = evaluate(write_content)

                self.assertEqual(report.failures, [])
                # This unit test passes when the evaluator rejects the wrong content.
                self.assertFalse(report.cases[0].assertions["ExactFileContents"].value)

    def test_missing_file_is_an_assertion_failure(self):
        def delete_file(prompt, workspace):
            (workspace / "message.txt").unlink()
            return read_result(workspace)

        report = evaluate(delete_file)

        self.assertEqual(report.failures, [])
        self.assertIsNone(report.cases[0].output.file_contents)
        self.assertFalse(report.cases[0].assertions["ExactFileContents"].value)

    def test_reported_execution_error_is_not_a_content_assertion(self):
        calls = []

        def cannot_execute(prompt, workspace):
            calls.append(workspace)
            return ExecutionResult("error", error="Test executor unavailable")

        report = evaluate(cannot_execute)

        # One attempt, cleaned workspace, and an execution failure with no graded case.
        self.assertEqual(len(calls), 1)
        self.assertFalse(calls[0].exists())
        self.assertEqual(report.cases, [])
        self.assertEqual(len(report.failures), 1)
        self.assertIn("Test executor unavailable", report.failures[0].error_message)

    def test_exception_is_reported_and_workspace_is_cleaned(self):
        workspaces = []

        def crash(prompt, workspace):
            # Keep the path so cleanup can be checked after the exception.
            workspaces.append(workspace)
            raise OSError("Test execution interrupted")

        report = evaluate(crash)

        self.assertEqual(len(workspaces), 1)
        self.assertFalse(workspaces[0].exists())
        self.assertEqual(report.cases, [])
        self.assertEqual(len(report.failures), 1)
        self.assertIn("Test execution interrupted", report.failures[0].error_message)

    def test_each_run_gets_fresh_fixture_and_unchanged_contract(self):
        original_contract = CONTRACT_PATH.read_bytes()
        observations = []

        def inspect_then_edit(prompt, workspace):
            observations.append((
                prompt,
                workspace,
                (workspace / "message.txt").read_bytes(),
                (workspace / "AGENTS.md").read_bytes(),
                sorted(path.name for path in workspace.iterdir()),
            ))
            # Deliberately dirty the copy to detect leakage into the next run.
            (workspace / "AGENTS.md").write_text("Changed by test", encoding="utf-8")
            (workspace / "extra.txt").write_text("Residue", encoding="utf-8")
            return write_after(prompt, workspace)

        for _ in range(2):
            report = evaluate(inspect_then_edit)
            self.assertEqual(report.failures, [])

        self.assertEqual(len(observations), 2)
        self.assertNotEqual(observations[0][1], observations[1][1])
        for prompt, workspace, initial, contract, files in observations:
            self.assertEqual(prompt, PROMPT)
            self.assertEqual(initial, b"before\n")
            self.assertEqual(contract, original_contract)
            self.assertEqual(files, ["AGENTS.md", "message.txt"])
            self.assertFalse(workspace.exists())
            self.assertFalse(workspace.is_relative_to(CONTRACT_PATH.parent))
        self.assertEqual(CONTRACT_PATH.read_bytes(), original_contract)

    def test_terminal_report_shows_case_and_assertion(self):
        report = evaluate(write_after)
        output = StringIO()

        # Capture the printed report in memory so its visible content can be checked.
        with redirect_stdout(output):
            report.print(include_durations=False)

        self.assertIn("replace-message", output.getvalue())
        self.assertIn("Assertions", output.getvalue())

    def test_explicit_dataset_and_fixture_arguments_override_smoke_defaults(self):
        dataset = Dataset(
            name="fixture-arguments",
            cases=[Case(name="inspect-fixture", inputs="Inspect the supplied fixture.")],
        )
        fixtures = (
            (None, {"message.txt": b"custom\r\n"}),
            ({"nested/data.bin": b"\x00\xff"}, {"nested/data.bin": b"\x00\xff"}),
            ({}, {}),
        )
        for supplied, expected in fixtures:
            with self.subTest(fixture_files=supplied):
                observations = []

                def inspect_fixture(prompt, workspace):
                    files = {
                        path.relative_to(workspace).as_posix(): path.read_bytes()
                        for path in workspace.rglob("*")
                        if path.is_file() and path.name != "AGENTS.md"
                    }
                    observations.append((prompt, files))
                    return ExecutionResult("completed")

                report = evaluate(inspect_fixture, dataset=dataset,
                                  initial_contents=b"custom\r\n", fixture_files=supplied)

                self.assertEqual(report.failures, [])
                self.assertEqual([case.name for case in report.cases], ["inspect-fixture"])
                self.assertEqual(observations, [("Inspect the supplied fixture.", expected)])


if __name__ == "__main__":
    unittest.main()
