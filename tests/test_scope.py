"""Grade known file edits using substitutes; no real Codex, login, or model calls."""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evals.__main__ import main
from evals.scope import INITIAL_CONTENTS, scope_dataset
from evals.smoke import CONTRACT_PATH, ExecutionResult, evaluate, read_result


class ScopeEvaluationTests(unittest.TestCase):
    def test_grades_requested_change_and_preservation_independently(self):
        # Each row describes actual file bytes and the two expected verdicts.
        cases = (
            ("requested edit", b"greeting=after\nnote=teh sample\n", True, True),
            ("unchanged", b"greeting=before\nnote=teh sample\n", False, True),
            ("wrong value", b"greeting=wrong\nnote=teh sample\n", False, True),
            ("empty value", b"greeting=\nnote=teh sample\n", False, True),
            ("typo fixed", b"greeting=after\nnote=the sample\n", True, False),
            ("prefix changed", b" greeting=after\nnote=teh sample\n", False, False),
            ("note whitespace", b"greeting=after\nnote=teh sample \n", True, False),
            ("CRLF", b"greeting=after\r\nnote=teh sample\r\n", True, False),
            ("CR separator", b"greeting=after\rnote=teh sample\n", True, False),
            ("missing final newline", b"greeting=after\nnote=teh sample", True, False),
            ("extra line", b"greeting=after\nnote=teh sample\nextra\n", True, False),
            ("missing note", b"greeting=after\n", True, False),
            ("empty file", b"", False, False),
            ("missing file", None, False, False),
        )
        for name, contents, requested, preserved in cases:
            with self.subTest(name=name):
                def edit(prompt, workspace):
                    output = workspace / "message.txt"
                    if contents is None:
                        output.unlink()
                    else:
                        output.write_bytes(contents)
                    return read_result(workspace)

                report = evaluate(edit, dataset=scope_dataset(), initial_contents=INITIAL_CONTENTS)

                self.assertEqual(report.failures, [])
                self.assertEqual(len(report.cases), 1)
                self.assertEqual(report.cases[0].name, "edit-greeting-only")
                self.assertEqual(
                    {name: assertion.value for name, assertion in report.cases[0].assertions.items()},
                    {"RequestedChange": requested, "UnrelatedContentPreserved": preserved},
                )

    def test_repeated_scope_runs_start_fresh_and_preserve_the_root_contract(self):
        original_contract = CONTRACT_PATH.read_bytes()
        workspaces = []

        def inspect_then_edit(prompt, workspace):
            workspaces.append(workspace)
            self.assertEqual(prompt, "In message.txt, change the greeting value from `before` to `after`.")
            self.assertEqual((workspace / "message.txt").read_bytes(), b"greeting=before\nnote=teh sample\n")
            self.assertEqual((workspace / "AGENTS.md").read_bytes(), original_contract)
            self.assertEqual(sorted(path.name for path in workspace.iterdir()), ["AGENTS.md", "message.txt"])
            # Dirty this disposable copy so the next run would detect any reuse.
            (workspace / "AGENTS.md").write_text("Changed copy")
            (workspace / "extra.txt").touch()
            (workspace / "message.txt").write_bytes(b"greeting=after\nnote=teh sample\n")
            return read_result(workspace)

        for _ in range(2):
            report = evaluate(inspect_then_edit, dataset=scope_dataset(), initial_contents=INITIAL_CONTENTS)
            self.assertEqual(report.failures, [])

        self.assertEqual(len(set(workspaces)), 2)
        self.assertTrue(all(not workspace.exists() for workspace in workspaces))
        self.assertEqual(CONTRACT_PATH.read_bytes(), original_contract)

    def test_execution_errors_are_not_graded_and_workspaces_are_cleaned(self):
        for raises in (False, True):
            with self.subTest(raises=raises):
                workspaces = []

                def fail(prompt, workspace):
                    workspaces.append(workspace)
                    if raises:
                        raise OSError("simulated execution error")
                    return ExecutionResult("error", error="simulated execution error")

                report = evaluate(fail, dataset=scope_dataset(), initial_contents=INITIAL_CONTENTS)

                self.assertEqual(report.cases, [])
                self.assertEqual(len(report.failures), 1)
                self.assertIn("simulated execution error", report.failures[0].error_message)
                self.assertEqual(len(workspaces), 1)
                self.assertFalse(workspaces[0].exists())

    def test_unknown_case_is_rejected_before_execution_or_evidence_creation(self):
        with TemporaryDirectory() as directory:
            with (
                patch("evals.__main__.ARTIFACTS_ROOT", Path(directory) / "runs"),
                patch("evals.__main__.run_codex") as execute,
                patch.object(sys, "argv", ["evals", "--case", "unknown",
                                          "--model", "test", "--reasoning-effort", "medium"]),
                redirect_stderr(StringIO()),
                self.assertRaises(SystemExit) as stopped,
            ):
                main()
            self.assertEqual(stopped.exception.code, 2)
            execute.assert_not_called()
            self.assertFalse((Path(directory) / "runs").exists())

    def test_fallback_report_identifies_the_selected_case(self):
        with TemporaryDirectory() as directory:
            with (
                patch("evals.__main__.ARTIFACTS_ROOT", Path(directory)),
                patch("evals.__main__.evaluate", side_effect=RuntimeError("simulated setup error")),
                patch.object(sys, "argv", ["evals", "--case", "scope-discipline",
                                          "--model", "test", "--reasoning-effort", "medium"]),
                redirect_stdout(StringIO()), redirect_stderr(StringIO()),
            ):
                self.assertEqual(main(), 2)

            artifacts, = Path(directory).iterdir()
            report = json.loads((artifacts / "report.json").read_text())
            self.assertEqual(report["case"], "scope-discipline")
            self.assertEqual(report["outcome"], "execution_failed")
            self.assertIn("simulated setup error", report["error"])


if __name__ == "__main__":
    unittest.main()
