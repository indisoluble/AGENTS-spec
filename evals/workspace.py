"""Capture filesystem state without following links or opening special files.

Snapshots describe final state, not the operations that produced it. The caller
owns their lifetime and must keep the initial snapshot outside the agent's reach.
"""

from dataclasses import dataclass
import os
from pathlib import Path
import stat


@dataclass(frozen=True)
class WorkspaceEntry:
    kind: str
    mode: int
    contents: bytes | None = None
    link_target: str | None = None


WorkspaceSnapshot = dict[str, WorkspaceEntry]


@dataclass(frozen=True)
class WorkspaceObservation:
    # None means inspection failed or never finished, not an empty workspace.
    initial: WorkspaceSnapshot | None
    final: WorkspaceSnapshot | None


_ENTRY_TYPES = {
    stat.S_IFREG: "file",
    stat.S_IFDIR: "directory",
    stat.S_IFLNK: "symlink",
    stat.S_IFIFO: "fifo",
    stat.S_IFSOCK: "socket",
    stat.S_IFCHR: "character-device",
    stat.S_IFBLK: "block-device",
}


class WorkspaceInspectionError(OSError):
    """Inspection failed; a partial snapshot cannot support a scope verdict."""


def snapshot_workspace(workspace: Path) -> WorkspaceSnapshot:
    """Record entries by relative path, with '.' representing the workspace root.

    A missing root is an empty state. Failures inspecting an existing tree raise
    instead of returning partial observations. Timestamps, ownership, and inode
    identity are intentionally absent from the records.
    """
    entries: WorkspaceSnapshot = {}

    def inspect(name: str, relative_path: str, parent_fd: int | None = None) -> None:
        try:
            try:
                metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            except FileNotFoundError:
                if relative_path == ".":
                    return
                # A listed child disappearing during inspection is not a complete snapshot.
                raise
            file_type = stat.S_IFMT(metadata.st_mode)
            kind = _ENTRY_TYPES.get(file_type, f"type {file_type:#o}")
            mode = stat.S_IMODE(metadata.st_mode)
            if kind == "symlink":
                target = os.readlink(name, dir_fd=parent_fd)
                entries[relative_path] = WorkspaceEntry(kind, mode, link_target=target)
            elif kind in ("file", "directory"):
                # Anchor child operations to an open directory. NOFOLLOW also rejects
                # a file/directory replaced by a link between inspection and opening.
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                if kind == "directory":
                    flags |= os.O_DIRECTORY
                descriptor = os.open(name, flags, dir_fd=parent_fd)
                try:
                    opened = os.fstat(descriptor)
                    if stat.S_IFMT(opened.st_mode) != file_type:
                        raise OSError("Entry type changed during inspection")
                    mode = stat.S_IMODE(opened.st_mode)
                    if kind == "file":
                        with os.fdopen(descriptor, "rb", closefd=False) as source:
                            contents = source.read()
                        entries[relative_path] = WorkspaceEntry(kind, mode, contents=contents)
                    else:
                        entries[relative_path] = WorkspaceEntry(kind, mode)
                        for child in sorted(os.listdir(descriptor)):
                            child_path = child if relative_path == "." else f"{relative_path}/{child}"
                            inspect(child, child_path, descriptor)
                finally:
                    os.close(descriptor)
            else:
                # FIFOs, sockets, and device files have state but no readable payload here.
                entries[relative_path] = WorkspaceEntry(kind, mode)
        except WorkspaceInspectionError:
            raise
        except OSError as exc:
            raise WorkspaceInspectionError(f"{relative_path}: {exc}") from exc

    inspect(str(workspace), ".")
    return entries
