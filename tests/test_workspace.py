"""Inspect disposable local files only; these tests never launch Codex or sign in."""

import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evals.workspace import WorkspaceInspectionError, snapshot_workspace


class WorkspaceSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(TemporaryDirectory()))
        self.workspace = self.root / "workspace"
        self.workspace.mkdir(mode=0o700)

    def test_snapshot_includes_root_hidden_nested_and_empty_entries_with_exact_bytes(self):
        (self.workspace / ".hidden").write_bytes(b"\x00\xff\r\n")
        (self.workspace / "nested" / "empty").mkdir(parents=True)
        (self.workspace / "nested" / "text").write_bytes(b"line \r\n")

        snapshot = snapshot_workspace(self.workspace)

        self.assertEqual(list(snapshot), [".", ".hidden", "nested", "nested/empty", "nested/text"])
        self.assertEqual(snapshot["."].kind, "directory")
        self.assertEqual(snapshot["nested/empty"].kind, "directory")
        self.assertIsNone(snapshot["nested/empty"].contents)
        self.assertEqual(snapshot[".hidden"].kind, "file")
        self.assertEqual(snapshot[".hidden"].contents, b"\x00\xff\r\n")
        self.assertEqual(snapshot["nested/text"].contents, b"line \r\n")

    def test_snapshot_records_permission_and_special_mode_bits(self):
        target = self.workspace / "file"
        target.write_bytes(b"data")
        target.chmod(0o4640)
        self.workspace.chmod(0o1750)

        snapshot = snapshot_workspace(self.workspace)

        self.assertEqual(snapshot["file"].mode, 0o4640)
        self.assertEqual(snapshot["."].mode, 0o1750)

    def test_links_are_recorded_without_reading_or_traversing_their_targets(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "private").write_bytes(b"outside contents")
        targets = {
            "directory-link": str(outside),
            "file-link": str(outside / "private"),
            "dangling-link": "missing",
            "loop": ".",
        }
        for name, target in targets.items():
            (self.workspace / name).symlink_to(target)

        snapshot = snapshot_workspace(self.workspace)

        self.assertEqual(set(snapshot), {".", *targets})
        for name, target in targets.items():
            self.assertEqual(snapshot[name].kind, "symlink")
            self.assertEqual(snapshot[name].link_target, target)
            self.assertIsNone(snapshot[name].contents)

    def test_fifo_and_socket_are_inspected_without_blocking_on_contents(self):
        os.mkfifo(self.workspace / "pipe")
        connection = self.enterContext(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
        connection.bind(str(self.workspace / "socket"))
        # Bound the check in a Python child so an accidental FIFO read cannot hang
        # unittest. This subprocess runs our inspector, never a coding agent.
        script = """
from pathlib import Path
import sys
from evals.workspace import snapshot_workspace
snapshot = snapshot_workspace(Path(sys.argv[1]))
for name, kind in (("pipe", "fifo"), ("socket", "socket")):
    assert snapshot[name].kind == kind
    assert snapshot[name].contents is None
"""
        result = subprocess.run(
            [sys.executable, "-W", "error::ResourceWarning", "-c", script, str(self.workspace)],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_root_is_empty_and_root_symlink_is_not_followed(self):
        self.workspace.rmdir()
        self.assertEqual(snapshot_workspace(self.workspace), {})
        self.workspace.symlink_to(self.root)

        snapshot = snapshot_workspace(self.workspace)

        self.assertEqual(list(snapshot), ["."])
        self.assertEqual(snapshot["."].kind, "symlink")
        self.assertEqual(snapshot["."].link_target, str(self.root))

    def test_snapshot_survives_later_edits_and_workspace_removal(self):
        target = self.workspace / "file"
        target.write_bytes(b"original")
        initial = snapshot_workspace(self.workspace)

        target.write_bytes(b"changed")
        target.unlink()
        self.workspace.rmdir()

        self.assertEqual(initial["file"].contents, b"original")

    def test_timestamps_are_excluded(self):
        target = self.workspace / "file"
        target.write_bytes(b"data")
        initial = snapshot_workspace(self.workspace)

        os.utime(target, ns=(1_000_000_000, 2_000_000_000))
        os.utime(self.workspace, ns=(3_000_000_000, 4_000_000_000))

        self.assertEqual(snapshot_workspace(self.workspace), initial)

    def test_ownership_and_inode_metadata_are_excluded(self):
        (self.workspace / "file").write_bytes(b"data")
        initial = snapshot_workspace(self.workspace)
        actual_fstat = os.fstat

        def different_metadata(descriptor):
            # Simulate ownership/identity changes without chown or privileged operations.
            fields = list(actual_fstat(descriptor))
            for index in (stat.ST_INO, stat.ST_UID, stat.ST_GID):
                fields[index] += 1
            return os.stat_result(fields)

        with patch("evals.workspace.os.fstat", side_effect=different_metadata):
            self.assertEqual(snapshot_workspace(self.workspace), initial)

    def test_inspection_errors_raise_instead_of_returning_partial_snapshots(self):
        (self.workspace / "file").write_bytes(b"data")
        (self.workspace / "link").symlink_to("missing")
        for operation in ("stat", "open", "fstat", "listdir", "readlink", "fdopen"):
            with self.subTest(operation=operation), patch(
                f"evals.workspace.os.{operation}", side_effect=PermissionError("simulated inspection failure"),
            ):
                with self.assertRaisesRegex(WorkspaceInspectionError, "simulated inspection failure"):
                    snapshot_workspace(self.workspace)

    def test_child_disappearing_during_inspection_is_an_error(self):
        (self.workspace / "file").write_bytes(b"data")
        actual_stat = os.stat

        def missing_child(name, **kwargs):
            if name == "file":
                raise FileNotFoundError("simulated disappearance")
            return actual_stat(name, **kwargs)

        with patch("evals.workspace.os.stat", side_effect=missing_child):
            with self.assertRaisesRegex(WorkspaceInspectionError, "file: .*simulated disappearance"):
                snapshot_workspace(self.workspace)

    def test_directory_replaced_with_symlink_during_inspection_is_rejected(self):
        nested = self.workspace / "nested"
        nested.mkdir()
        actual_open = os.open

        def replace_before_open(name, flags, **kwargs):
            if name == "nested":
                nested.rmdir()
                nested.symlink_to(self.root)
            return actual_open(name, flags, **kwargs)

        with patch("evals.workspace.os.open", side_effect=replace_before_open):
            with self.assertRaisesRegex(WorkspaceInspectionError, "nested:"):
                snapshot_workspace(self.workspace)


if __name__ == "__main__":
    unittest.main()
