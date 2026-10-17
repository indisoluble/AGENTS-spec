"""Test the evaluation pipeline with a fake Codex executable.

Workspace creation, subprocess launching, Pydantic Evals grading, and reporting
run for real, using temporary files. The subprocess is a small Python script,
not Codex: there is no real authentication, OpenAI request, or subscription usage.
This verifies our plumbing, not real Codex compatibility or agent behavior.
"""

from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evals.__main__ import main
from evals.auth import PROFILE_CONFIG
from evals.smoke import CONTRACT_PATH, PROMPT


class CodexIntegrationTests(unittest.TestCase):
    def test_cli_saves_evidence_and_grades_file_from_subprocess(self):
        # Keep the dummy profile, fake executable, and reports in an auto-cleaned directory.
        with TemporaryDirectory() as directory:
            root = Path(directory)
            profile = root / "profile"
            profile.mkdir()
            (profile / "config.toml").write_text(PROFILE_CONFIG)
            (profile / "auth.json").write_text("test credential: must not be copied")
            executable = root / "codex"
            # Imitate version/status replies and a successful edit. No model chooses the edit.
            executable.write_text(f"#!{sys.executable}\n" + '''
import json
import os
from pathlib import Path
import sys

if "--version" in sys.argv:
    print("codex-cli test")
elif "login" in sys.argv:
    print("Logged in using ChatGPT")
else:
    # Check the environment received by the child process, not just the parent's settings.
    assert "OPENAI_API_KEY" not in os.environ
    assert "CODEX_API_KEY" not in os.environ
    assert "CODEX_ACCESS_TOKEN" not in os.environ
    assert "CODEX_THREAD_ID" not in os.environ
    assert (Path(os.environ["CODEX_HOME"]) / "auth.json").is_file()
    workspace = Path(sys.argv[sys.argv.index("--cd") + 1])
    assert (workspace / "message.txt").read_bytes() == b"before\\n"
    assert "Replace the contents" in sys.stdin.read()
    # Perform the edit directly and emit the completion event our runner expects.
    (workspace / "message.txt").write_bytes(b"after\\n")
    print(json.dumps({"type": "turn.completed"}))
''')
            executable.chmod(0o700)
            captured = StringIO()
            # patch temporarily redirects executable discovery, reports, and CLI arguments.
            # Plant dummy secrets to check that our runner excludes them from the child.
            with (
                patch("evals.auth.codex_executable", return_value=str(executable)),
                patch("evals.__main__.ARTIFACTS_ROOT", root / "runs"),
                patch.dict(os.environ, {
                    "OPENAI_API_KEY": "test-secret", "CODEX_API_KEY": "test-secret",
                    "CODEX_ACCESS_TOKEN": "test-secret", "CODEX_THREAD_ID": "parent-session",
                }),
                patch.object(sys, "argv", ["evals", "--codex-home", str(profile), "--model", "test-model", "--reasoning-effort", "medium"]),
                redirect_stdout(captured),
            ):
                # The real command handler launches the fake CLI, grades its file, and reports.
                exit_code = main()

            # Success must retain credentials and produce exactly one evaluation report.
            self.assertEqual(exit_code, 0)
            self.assertEqual((profile / "auth.json").read_text(), "test credential: must not be copied")
            runs = list((root / "runs").iterdir())
            self.assertEqual(len(runs), 1)
            artifacts = runs[0]
            report = json.loads((artifacts / "report.json").read_text())
            execution = json.loads((artifacts / "execution.json").read_text())
            # Check the graded content and recorded settings, not an agent's claim of success.
            self.assertEqual(report["outcome"], "passed")
            self.assertEqual(report["case"], "smoke")
            self.assertEqual(report["cases"][0]["file_contents"], "after\n")
            self.assertEqual(execution["codex_home"], str(profile.resolve()))
            self.assertEqual(execution["model"], "test-model")
            self.assertEqual(execution["reasoning_effort"], "medium")
            self.assertEqual(execution["codex_version"], "codex-cli test")
            # The execution workspace is gone, but its evidence must still be inspectable.
            self.assertFalse(Path(execution["workspace"]).exists())
            self.assertEqual((artifacts / "prompt.txt").read_text(), PROMPT)
            self.assertEqual((artifacts / "AGENTS.md").read_bytes(), CONTRACT_PATH.read_bytes())
            self.assertEqual((artifacts / "message.txt").read_bytes(), b"before\n")
            self.assertEqual((artifacts / "workspace" / "message.txt").read_bytes(), b"after\n")
            self.assertIn("replace-message", (artifacts / "report.txt").read_text())
            self.assertTrue((artifacts / "events.jsonl").is_file())
            self.assertTrue((artifacts / "stderr.txt").is_file())
            # Check these specific dummy secrets were not saved; this is not general redaction.
            self.assertNotIn("auth.json", [file.name for file in artifacts.rglob("*")])
            self.assertNotIn("test-secret", "".join(file.read_text() for file in artifacts.rglob("*") if file.is_file()))


if __name__ == "__main__":
    unittest.main()
