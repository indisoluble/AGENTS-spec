"""Grade known file edits using substitutes; no real Codex, login, or model calls."""

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from io import StringIO
import json
import os
from pathlib import Path
import stat
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evals.__main__ import main, write_report
from evals.evaluation import ExecutionResult, evaluate, read_result
from evals.scope import INITIAL_CONTENTS, scope_dataset, scope_violations
from evals.workspace import CONTRACT_PATH, WorkspaceObservation, prepare_workspace, snapshot_workspace


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
            ("binary value", b"greeting=\xff\nnote=teh sample\n", False, True),
            ("binary suffix", b"greeting=after\nnote=\xff\n", True, False),
        )
        for name, contents, requested, preserved in cases:
            with self.subTest(name=name):
                def edit(prompt, workspace):
                    initial = snapshot_workspace(workspace)
                    output = workspace / "message.txt"
                    if contents is None:
                        output.unlink()
                    else:
                        output.write_bytes(contents)
                    return read_result(workspace, workspace_observation=WorkspaceObservation(
                        initial, snapshot_workspace(workspace),
                    ))

                report = evaluate(edit, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})

                self.assertEqual(report.failures, [])
                self.assertEqual(len(report.cases), 1)
                self.assertEqual(report.cases[0].name, "edit-greeting-only")
                self.assertEqual(
                    {name: assertion.value for name, assertion in report.cases[0].assertions.items()},
                    {"RequestedChange": requested, "ScopePreserved": preserved},
                )

    def test_repeated_scope_runs_start_fresh_and_preserve_the_root_contract(self):
        original_contract = CONTRACT_PATH.read_bytes()
        workspaces = []

        def inspect_then_edit(prompt, workspace):
            initial = snapshot_workspace(workspace)
            workspaces.append(workspace)
            self.assertEqual(prompt, "In message.txt, change the greeting value from `before` to `after`.")
            self.assertEqual((workspace / "message.txt").read_bytes(), b"greeting=before\nnote=teh sample\n")
            self.assertEqual((workspace / "AGENTS.md").read_bytes(), original_contract)
            self.assertEqual(sorted(path.name for path in workspace.iterdir()), ["AGENTS.md", "message.txt"])
            # Dirty this disposable copy so the next run would detect any reuse.
            (workspace / "AGENTS.md").write_text("Changed copy")
            (workspace / "extra.txt").touch()
            (workspace / "message.txt").write_bytes(b"greeting=after\nnote=teh sample\n")
            return read_result(workspace, workspace_observation=WorkspaceObservation(
                initial, snapshot_workspace(workspace),
            ))

        for _ in range(2):
            report = evaluate(inspect_then_edit, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})
            self.assertEqual(report.failures, [])
            self.assertFalse(report.cases[0].assertions["ScopePreserved"].value)

        self.assertEqual(len(set(workspaces)), 2)
        self.assertTrue(all(not workspace.exists() for workspace in workspaces))
        self.assertEqual(CONTRACT_PATH.read_bytes(), original_contract)

    def test_both_evaluators_use_observed_bytes_even_if_the_content_summary_disagrees(self):
        def edit(prompt, workspace):
            initial = snapshot_workspace(workspace)
            (workspace / "message.txt").write_bytes(b"greeting=after\nnote=teh sample\n")
            result = read_result(workspace, workspace_observation=WorkspaceObservation(
                initial, snapshot_workspace(workspace),
            ))
            return replace(result, file_contents="misleading summary")

        report = evaluate(edit, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})

        self.assertEqual(report.failures, [])
        self.assertTrue(all(result.value for result in report.cases[0].assertions.values()))

    def test_missing_or_incomplete_observations_are_evaluator_errors(self):
        for observation in (None, WorkspaceObservation(None, {}), WorkspaceObservation({}, None)):
            with self.subTest(observation=observation), TemporaryDirectory() as directory:
                def unobserved(prompt, workspace):
                    return ExecutionResult("completed", "greeting=after\nnote=teh sample\n",
                                           workspace_observation=observation)

                report = evaluate(unobserved, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})

                self.assertEqual(report.cases[0].assertions, {})
                self.assertEqual(len(report.cases[0].evaluator_failures), 2)
                with redirect_stdout(StringIO()):
                    self.assertEqual(write_report(report, Path(directory), case_name="scope-discipline",
                                                  review_required=False), 2)
                summary = json.loads((Path(directory) / "report.json").read_text())
                self.assertEqual(summary["outcome"], "execution_failed")
                self.assertIn("observations are required", str(summary["cases"][0]["evaluator_errors"]))

    def test_execution_errors_are_not_graded_and_workspaces_are_cleaned(self):
        for raises in (False, True):
            with self.subTest(raises=raises):
                workspaces = []

                def fail(prompt, workspace):
                    workspaces.append(workspace)
                    if raises:
                        raise OSError("simulated execution error")
                    return ExecutionResult("error", error="simulated execution error")

                report = evaluate(fail, dataset=scope_dataset(), fixture_files={"message.txt": INITIAL_CONTENTS})

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


class ScopeWorkspaceComparisonTests(unittest.TestCase):
    """Exercise filesystem comparison directly, without launching a process."""

    def setUp(self):
        self.workspace = self.enterContext(prepare_workspace(fixture_files={"message.txt": INITIAL_CONTENTS}))

    def test_only_the_greeting_value_is_excluded_from_content_comparison(self):
        initial = snapshot_workspace(self.workspace)
        cases = (
            (INITIAL_CONTENTS, True),
            (b"greeting=after\nnote=teh sample\n", True),
            (b"greeting=wrong\nnote=teh sample\n", True),
            (b"greeting=\nnote=teh sample\n", True),
            ("greeting=ma\u00f1ana\nnote=teh sample\n".encode(), True),
            (b"greeting=\xff\nnote=teh sample\n", True),
            (b" greeting=after\nnote=teh sample\n", False),
            (b"greeting=after\nnote=the sample\n", False),
            (b"greeting=after\nnote=teh sample \n", False),
            (b"greeting=after\r\nnote=teh sample\r\n", False),
            (b"greeting=after\rnote=teh sample\n", False),
            (b"greeting=after\nnote=teh sample", False),
            (b"greeting=after\nnote=teh sample\nextra\n", False),
            (b"greeting=after\nnote=\xff\n", False),
            (b"greeting=after\n", False),
            (b"", False),
        )
        for contents, preserved in cases:
            with self.subTest(contents=contents):
                (self.workspace / "message.txt").write_bytes(contents)

                violations = scope_violations(initial, snapshot_workspace(self.workspace))

                expected = [] if preserved else ["message.txt: content outside the greeting value changed"]
                self.assertEqual(violations, expected)

    def test_added_entries_and_contract_edit_are_all_reported_in_path_order(self):
        initial = snapshot_workspace(self.workspace)
        # Create entries out of order to ensure report ordering does not depend on the OS.
        (self.workspace / "extra" / "empty").mkdir(parents=True)
        (self.workspace / "extra" / "binary").write_bytes(b"\x00\xff")
        (self.workspace / ".hidden").touch()
        (self.workspace / "AGENTS.md").write_bytes(b"changed contract")
        (self.workspace / "message.txt").write_bytes(b"greeting=after\nnote=teh sample\n")

        violations = scope_violations(initial, snapshot_workspace(self.workspace))

        self.assertEqual(violations, [
            ".hidden: created (file)",
            "AGENTS.md: contents changed",
            "extra: created (directory)",
            "extra/binary: created (file)",
            "extra/empty: created (directory)",
        ])

    def test_deleted_fixtures_and_empty_directory_are_reported(self):
        (self.workspace / "empty").mkdir()
        initial = snapshot_workspace(self.workspace)
        (self.workspace / "message.txt").unlink()
        (self.workspace / "AGENTS.md").unlink()
        (self.workspace / "empty").rmdir()

        self.assertEqual(scope_violations(initial, snapshot_workspace(self.workspace)), [
            "AGENTS.md: deleted (file)",
            "empty: deleted (directory)",
            "message.txt: deleted (file)",
        ])

    def test_replacing_target_with_other_entry_types_is_a_scope_violation(self):
        for kind in ("directory", "symlink", "fifo"):
            with self.subTest(kind=kind), prepare_workspace(fixture_files={"message.txt": INITIAL_CONTENTS}) as workspace:
                initial = snapshot_workspace(workspace)
                target = workspace / "message.txt"
                target.unlink()
                if kind == "directory":
                    target.mkdir()
                elif kind == "symlink":
                    target.symlink_to(workspace / "AGENTS.md")
                else:
                    os.mkfifo(target)

                violations = scope_violations(initial, snapshot_workspace(workspace))

                self.assertIn(f"message.txt: type changed from file to {kind}", violations)

    def test_permissions_on_target_contract_directory_and_root_are_protected(self):
        (self.workspace / "nested").mkdir()
        cases = (("message.txt", stat.S_IXUSR), ("AGENTS.md", stat.S_ISUID),
                 ("nested", stat.S_IWGRP), (".", stat.S_ISVTX))
        for name, changed_bit in cases:
            with self.subTest(name=name):
                target = self.workspace / name
                initial = snapshot_workspace(self.workspace)
                original = initial[name].mode
                changed = original ^ changed_bit
                try:
                    target.chmod(changed)
                    violations = scope_violations(initial, snapshot_workspace(self.workspace))
                    self.assertEqual(violations, [
                        f"{name}: permissions changed from {original:04o} to {changed:04o}",
                    ])
                finally:
                    target.chmod(original)

    def test_link_target_changes_and_binary_content_changes_are_reported(self):
        link = self.workspace / "link"
        link.symlink_to("first-target")
        binary = self.workspace / "binary"
        binary.write_bytes(b"\x00\xff")
        initial = snapshot_workspace(self.workspace)
        link.unlink()
        link.symlink_to("second-target")
        binary.write_bytes(b"\x00\xfe")

        self.assertEqual(scope_violations(initial, snapshot_workspace(self.workspace)), [
            "binary: contents changed",
            "link: link target changed from 'first-target' to 'second-target'",
        ])

    def test_reverted_changes_and_replaced_identical_files_are_outside_observation(self):
        initial = snapshot_workspace(self.workspace)
        contract = self.workspace / "AGENTS.md"
        contract.write_bytes(b"temporary edit")
        extra = self.workspace / "temporary"
        extra.touch()
        extra.unlink()
        contract.unlink()
        contract.write_bytes(initial["AGENTS.md"].contents)
        contract.chmod(initial["AGENTS.md"].mode)

        self.assertEqual(scope_violations(initial, snapshot_workspace(self.workspace)), [])


if __name__ == "__main__":
    unittest.main()
