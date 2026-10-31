"""Trusted subprocess adapter, executed inside the functional-check sandbox.

Keep fixture output separate from the adapter's JSON response. The parent owns
the process group, including descendants left behind by a check.
"""

import base64
import json
import subprocess
import sys


def main() -> None:
    request = json.load(sys.stdin)
    status, returncode, output, errors, error = "error", None, b"", b"", None
    try:
        with subprocess.Popen(
            [sys.executable, "-I", "-B", "-S", "-X", "utf8", "-c", request["source"]],
            cwd=request["workspace"], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ) as process:
            try:
                output, errors = process.communicate(timeout=request["timeout"])
                status, returncode = "completed", process.returncode
            except subprocess.TimeoutExpired as exc:
                output, errors = exc.output or b"", exc.stderr or b""
                process.kill()
                process.wait()
                # Do not drain pipes here: a surviving descendant could keep
                # them open. The parent stops that entire group after this reply.
                error = "Functional check timed out"
    except OSError as exc:
        error = f"Could not launch functional check: {exc}"
    print(json.dumps({
        "status": status, "returncode": returncode, "error": error,
        "stdout_base64": base64.b64encode(output).decode("ascii"),
        "stderr_base64": base64.b64encode(errors).decode("ascii"),
    }))


if __name__ == "__main__":
    main()
