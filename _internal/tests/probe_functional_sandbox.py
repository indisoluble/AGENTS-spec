"""Opt-in policy check using the real Codex sandbox, without login or a model.

Not named test_*.py: the ordinary offline suite must use only fake CLI processes.
Run this separately when verifying the installed sandbox implementation.
See [Functional-check execution](../EVALUATIONS.md#functional-check-execution)
for the longer explanation and execution limits.
"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from evals.functional import run_python_check


class FunctionalSandboxProbe(unittest.TestCase):
    def test_reads_succeed_but_fixture_writes_host_writes_and_network_are_denied(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            workspace.mkdir()
            fixture = workspace / "sample.txt"
            fixture.write_bytes(b"original\n")
            outside = root / "outside.txt"
            outside.write_bytes(b"outside\n")
            # Every path and operation is supplied by this test. The connection
            # only targets loopback; no model, credentials, or external service.
            source = f'''import errno, json, socket
from pathlib import Path
result = {{"contents": Path("sample.txt").read_text()}}
for label, path in (("fixture_write_denied", Path("sample.txt")),
                    ("host_write_denied", Path({str(outside)!r}))):
    try:
        path.write_text("changed")
        result[label] = False
    except PermissionError:
        result[label] = True
try:
    with socket.socket() as connection:
        connection.settimeout(1)
        connection.connect(("127.0.0.1", 9))
    result["network_denied"] = False
except OSError as exc:
    result["network_denied"] = exc.errno in (errno.EPERM, errno.EACCES)
print(json.dumps(result))
'''
            result = run_python_check(source, workspace)
            self.assertEqual((result.status, result.returncode), ("completed", 0), result)
            self.assertEqual(json.loads(result.stdout), {
                "contents": "original\n", "fixture_write_denied": True,
                "host_write_denied": True, "network_denied": True,
            })
            self.assertEqual(fixture.read_bytes(), b"original\n")
            self.assertEqual(outside.read_bytes(), b"outside\n")


if __name__ == "__main__":
    unittest.main()
