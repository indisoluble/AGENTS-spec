"""Inspect disposable local files only; these tests never launch Codex or sign in."""

import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from evals.runtime.workspace import (
    WorkspaceEntry, WorkspaceInspectionError, WorkspaceObservation, snapshot_workspace, workspace_changes,
    workspace_violations,
)


class WorkspaceComparisonTests(unittest.TestCase):
    def test_missing_file_contents_raise_before_calling_the_content_rule(self):
        for phase, before, after in (
            ("Initial", None, b"observed"),
            ("Final", b"observed", None),
            ("Initial", None, None),
        ):
            for final_mode in (0o644, 0o600):
                with self.subTest(phase=phase, before=before, after=after, final_mode=final_mode):
                    content_rule = Mock(return_value=None)
                    initial = {"nested/file.txt": WorkspaceEntry("file", 0o644, contents=before)}
                    final = {"nested/file.txt": WorkspaceEntry("file", final_mode, contents=after)}

                    with self.assertRaisesRegex(
                        WorkspaceInspectionError, rf"{phase} nested/file\.txt contents were not captured",
                    ):
                        workspace_violations(initial, final, content_violation=content_rule)

                    content_rule.assert_not_called()

    def test_captured_bytes_including_empty_contents_use_the_scenario_rule(self):
        for before, after, reason in (
            (b"same", b"same", None),
            (b"before", b"after", None),
            (b"before", b"after", "content outside the permitted edit changed"),
            (b"\x00\xff", b"\x00\xfe", "binary contents changed"),
            (b"", b"", None),
            (b"", b"after", "contents changed"),
            (b"before", b"", "contents changed"),
        ):
            with self.subTest(before=before, after=after, reason=reason):
                content_rule = Mock(return_value=reason)
                initial = {"file.txt": WorkspaceEntry("file", 0o644, contents=before)}
                final = {"file.txt": WorkspaceEntry("file", 0o644, contents=after)}

                violations = workspace_violations(initial, final, content_violation=content_rule)

                self.assertEqual(violations, [] if reason is None else [f"file.txt: {reason}"])
                content_rule.assert_called_once_with("file.txt", before, after)

    def test_structural_changes_do_not_require_file_contents(self):
        file = WorkspaceEntry("file", 0o644)
        directory = WorkspaceEntry("directory", 0o755)
        for initial, final, expected in (
            ({}, {}, []),
            ({"file.txt": file}, {}, ["file.txt: deleted (file)"]),
            ({}, {"file.txt": file}, ["file.txt: created (file)"]),
            ({"file.txt": file}, {"file.txt": directory}, [
                "file.txt: type changed from file to directory",
                "file.txt: permissions changed from 0644 to 0755",
            ]),
            ({"file.txt": directory}, {"file.txt": file}, [
                "file.txt: type changed from directory to file",
                "file.txt: permissions changed from 0755 to 0644",
            ]),
        ):
            with self.subTest(initial=initial, final=final):
                content_rule = Mock()

                violations = workspace_violations(initial, final, content_violation=content_rule)

                self.assertEqual(violations, expected)
                content_rule.assert_not_called()

    def test_permissions_and_link_targets_remain_independent_of_content_changes(self):
        initial = {
            "link": WorkspaceEntry("symlink", 0o777, link_target="before"),
            "file.txt": WorkspaceEntry("file", 0o644, contents=b""),
            "directory": WorkspaceEntry("directory", 0o755),
        }
        final = {
            "link": WorkspaceEntry("symlink", 0o777, link_target="after"),
            "file.txt": WorkspaceEntry("file", 0o600, contents=b""),
            "directory": WorkspaceEntry("directory", 0o700),
        }
        content_rule = Mock(return_value=None)

        violations = workspace_violations(initial, final, content_violation=content_rule)

        self.assertEqual(violations, [
            "directory: permissions changed from 0755 to 0700",
            "file.txt: permissions changed from 0644 to 0600",
            "link: link target changed from 'before' to 'after'",
        ])
        content_rule.assert_called_once_with("file.txt", b"", b"")

    def test_missing_file_contents_raise_under_optimized_python(self):
        result = subprocess.run(
            [sys.executable, "-O", "-m", "unittest",
             "tests.runtime.test_workspace.WorkspaceComparisonTests."
             "test_missing_file_contents_raise_before_calling_the_content_rule"],
            capture_output=True, text=True, timeout=10,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


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
from evals.runtime.workspace import snapshot_workspace
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

        with patch("evals.runtime.workspace.os.fstat", side_effect=different_metadata):
            self.assertEqual(snapshot_workspace(self.workspace), initial)

    def test_inspection_errors_raise_instead_of_returning_partial_snapshots(self):
        (self.workspace / "file").write_bytes(b"data")
        (self.workspace / "link").symlink_to("missing")
        for operation in ("stat", "open", "fstat", "listdir", "readlink", "fdopen"):
            with self.subTest(operation=operation), patch(
                f"evals.runtime.workspace.os.{operation}", side_effect=PermissionError("simulated inspection failure"),
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

        with patch("evals.runtime.workspace.os.stat", side_effect=missing_child):
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

        with patch("evals.runtime.workspace.os.open", side_effect=replace_before_open):
            with self.assertRaisesRegex(WorkspaceInspectionError, "nested:"):
                snapshot_workspace(self.workspace)


class WorkspaceChangeReportTests(unittest.TestCase):
    def test_changes_include_types_modes_links_exact_text_and_binary_contents_in_path_order(self):
        initial = {
            ".": WorkspaceEntry("directory", 0o700),
            "binary": WorkspaceEntry("file", 0o600, b"\xff"),
            "deleted": WorkspaceEntry("file", 0o600, b"removed\n"),
            "link": WorkspaceEntry("symlink", 0o777, link_target="old"),
            "text": WorkspaceEntry("file", 0o644, b"same\r\nlast"),
            "type": WorkspaceEntry("directory", 0o700),
        }
        final = {
            ".": WorkspaceEntry("directory", 0o755),
            ".hidden": WorkspaceEntry("file", 0o600, b"added\n"),
            "binary": WorkspaceEntry("file", 0o600, b"\x00\xfe"),
            "empty": WorkspaceEntry("directory", 0o700),
            "link": WorkspaceEntry("symlink", 0o777, link_target="new\nname"),
            "nested": WorkspaceEntry("directory", 0o700),
            "nested/pipe": WorkspaceEntry("fifo", 0o600),
            "text": WorkspaceEntry("file", 0o755, b"same\nlast\n"),
            "type": WorkspaceEntry("file", 0o600, b"new file\n"),
        }
        rendered = workspace_changes(WorkspaceObservation(initial, final))
        paths = [json.loads(line.removeprefix("Path: ")) for line in rendered.splitlines() if line.startswith("Path: ")]
        self.assertEqual(paths, sorted(initial.keys() | final.keys()))
        for expected in ('mode=0700', 'mode=0755', 'mode=0644', 'After: absent', 'Before: absent',
                         'target="old"', 'target="new\\nname"', 'fifo, mode=0600',
                         '-"same\\r\\n"', '+"same\\n"', '-"last"', '+"last\\n"',
                         '-base64: /w==', '+base64: AP4=', '-"removed\\n"', '+"added\\n"'):
            self.assertIn(expected, rendered)

    def test_unchanged_and_incomplete_observations_are_distinct(self):
        self.assertEqual(workspace_changes(WorkspaceObservation({}, {})), "No observed workspace changes.\n")
        for observation in (WorkspaceObservation(None, {}), WorkspaceObservation({}, None)):
            self.assertIn("comparison unavailable", workspace_changes(observation))
            self.assertNotIn("No observed", workspace_changes(observation))


if __name__ == "__main__":
    unittest.main()
