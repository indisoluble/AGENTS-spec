"""Own temporary workspaces, safe fixture reads, and filesystem observations.

Snapshots describe final state, not the operations that produced it. The caller
owns their lifetime and must keep the initial snapshot outside the agent's reach.
"""

import base64
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from difflib import unified_diff
import json
import os
from pathlib import Path
import stat
from tempfile import TemporaryDirectory


CONTRACT_PATH = Path(__file__).resolve().parents[1] / "AGENTS.md"


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


@contextmanager
def prepare_workspace(*, fixture_files: Mapping[str, bytes]) -> Iterator[Path]:
    """Copy the current contract and explicit fixture into a disposable directory.

    The root contract is always supplied separately and cannot be overridden by
    a case. An empty mapping creates only the contract; callers own case defaults.
    """
    with TemporaryDirectory(prefix="agents-spec-eval-") as directory:
        workspace = Path(directory)
        (workspace / "AGENTS.md").write_bytes(CONTRACT_PATH.read_bytes())
        for name, contents in fixture_files.items():
            path = Path(name)
            if (path.is_absolute() or not path.parts or ".." in path.parts
                    or path.parts[0].casefold() == "agents.md"):
                raise ValueError(f"Invalid fixture path: {name!r}; use a relative path outside root AGENTS.md")
            target = workspace / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(contents)
        # The caller uses this directory; leaving the context removes it.
        yield workspace


def read_fixture_file(path: Path) -> bytes | None:
    """Read a regular fixture safely; a missing file returns None."""
    try:
        # Do not follow links or wait for a named pipe's writer when opening.
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return None
    try:
        # Check the opened file itself, avoiding a separate check/read race.
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError(f"{path.name} must be a regular fixture file")
        with os.fdopen(descriptor, "rb", closefd=False) as fixture:
            return fixture.read()
    finally:
        os.close(descriptor)


def workspace_changes(observation: WorkspaceObservation) -> str:
    """Describe all observed differences without deciding whether they are allowed."""
    if observation.initial is None or observation.final is None:
        return "Workspace comparison unavailable: initial or final inspection is incomplete.\n"

    def describe(entry: WorkspaceEntry | None) -> str:
        if entry is None:
            return "absent"
        description = f"{entry.kind}, mode={entry.mode:04o}"
        if entry.link_target is not None:
            description += f", target={json.dumps(entry.link_target)}"
        return description

    def content_lines(entry: WorkspaceEntry | None) -> list[str]:
        if entry is None or entry.contents is None:
            return []
        try:
            text = entry.contents.decode("utf-8")
        except UnicodeDecodeError:
            return ["base64: " + base64.b64encode(entry.contents).decode("ascii") + "\n"]
        # Quoted lines expose CRLF, missing final newlines, tabs, and other bytes
        # that an ordinary text diff can hide. Manifests retain the exact bytes.
        return [json.dumps(line) + "\n" for line in text.splitlines(keepends=True)]

    blocks = []
    initial, final = observation.initial, observation.final
    for path in sorted(initial.keys() | final.keys()):
        before, after = initial.get(path), final.get(path)
        if before == after:
            continue
        block = f"Path: {json.dumps(path)}\nBefore: {describe(before)}\nAfter: {describe(after)}\n"
        block += "".join(unified_diff(content_lines(before), content_lines(after),
                                      fromfile="initial contents", tofile="final contents"))
        blocks.append(block)
    if not blocks:
        return "No observed workspace changes.\n"
    return ("Observed differences only; authorization requires case-specific assessment.\n"
            "Text diffs use JSON-quoted lines; binary contents use base64.\n\n"
            + "\n".join(blocks))


def workspace_violations(
    initial: WorkspaceSnapshot, final: WorkspaceSnapshot,
    *, content_violation: Callable[[str, bytes, bytes], str | None],
) -> list[str]:
    """Compare all entries; the case supplies its regular-file content rule."""
    violations = []
    for path in sorted(initial.keys() | final.keys()):
        before, after = initial.get(path), final.get(path)
        if before is None:
            violations.append(f"{path}: created ({after.kind})")
            continue
        if after is None:
            violations.append(f"{path}: deleted ({before.kind})")
            continue
        if before.kind != after.kind:
            violations.append(f"{path}: type changed from {before.kind} to {after.kind}")
        if before.mode != after.mode:
            violations.append(f"{path}: permissions changed from {before.mode:04o} to {after.mode:04o}")
        if before.kind != after.kind:
            continue
        if before.kind == "file":
            assert before.contents is not None and after.contents is not None
            reason = content_violation(path, before.contents, after.contents)
            if reason is not None:
                violations.append(f"{path}: {reason}")
        elif before.kind == "symlink" and before.link_target != after.link_target:
            violations.append(f"{path}: link target changed from {before.link_target!r} to {after.link_target!r}")
    return violations


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
