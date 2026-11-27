"""Grade known file edits using substitutes; no real Codex, login, or model calls."""

import os
import stat
import unittest

from engine.smoke import synthetic_contract
from engine.runtime.workspace import prepare_workspace, snapshot_workspace
from conformance.scope import INITIAL_CONTENTS, scope_violations


class ScopeWorkspaceComparisonTests(unittest.TestCase):
    """Exercise filesystem comparison directly, without launching a process."""

    def setUp(self):
        self.workspace = self.enterContext(prepare_workspace(contract_bytes=synthetic_contract(), fixture_files={"message.txt": INITIAL_CONTENTS}))

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
            with self.subTest(kind=kind), prepare_workspace(contract_bytes=synthetic_contract(), fixture_files={"message.txt": INITIAL_CONTENTS}) as workspace:
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
