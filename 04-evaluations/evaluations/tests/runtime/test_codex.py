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
import tomllib
import unittest
from unittest.mock import patch

from evaluations.__main__ import main
from evaluations.runtime.auth import PROFILE_CONFIG
from evaluations.runtime.codex import execution_command
from evaluations.runtime.workspace import CONTRACT_PATH
from evaluations.scenarios.smoke import PROMPT


class ExecutionCommandTests(unittest.TestCase):
    def test_native_permissions_use_unquoted_selector_keys_and_toml_values(self):
        expected_settings = {
            "model_reasoning_effort": "medium",
            "model_provider": "openai",
            "forced_login_method": "chatgpt",
            "cli_auth_credentials_store": "file",
            "approval_policy": "never",
            "web_search": "disabled",
            "default_permissions": "agents-spec-eval",
            "permissions.agents-spec-eval.extends": ":workspace",
            "permissions.agents-spec-eval.filesystem.:root": "deny",
            "permissions.agents-spec-eval.filesystem.:minimal": "read",
            "permissions.agents-spec-eval.filesystem.:tmpdir": "deny",
            "permissions.agents-spec-eval.filesystem.:slash_tmp": "deny",
            "permissions.agents-spec-eval.network.enabled": False,
            "shell_environment_policy.inherit": "none",
            "analytics.enabled": False,
        }
        clt_key = "permissions.agents-spec-eval.filesystem./Library/Developer/CommandLineTools"
        workspace = Path("/evaluation/workspace")
        for platform, expected_clt in (("darwin", "read"), ("linux", None), ("freebsd", None)):
            with self.subTest(platform=platform):
                with patch("evaluations.runtime.codex.sys.platform", platform):
                    command = execution_command("codex", workspace, "test-model", "medium")
                overrides = [command[index + 1] for index, argument in enumerate(command) if argument == "--config"]
                # Codex splits dotted keys itself; only each value is TOML. Parsing the
                # whole override as TOML would incorrectly require quoted selector keys.
                settings = {}
                for override in overrides:
                    key, value = override.split("=", 1)
                    self.assertNotIn(key, settings, "Duplicate overrides could change the effective policy")
                    settings[key] = tomllib.loads(f"value = {value}")["value"]
                expected = expected_settings.copy()
                if expected_clt is not None:
                    expected[clt_key] = expected_clt
                    self.assertIn(f'{clt_key}="read"', overrides)
                else:
                    self.assertNotIn(clt_key, settings)
                self.assertEqual(settings, expected)
                self.assertIn('permissions.agents-spec-eval.filesystem.:minimal="read"', overrides)
                self.assertIn('permissions.agents-spec-eval.network.enabled=false', overrides)
                self.assertFalse(any(key == "sandbox_mode" or key.startswith("sandbox_workspace_write") for key in settings))
                for flag in ("--sandbox", "-s", "--permission-profile", "-P", "--full-auto",
                             "--dangerously-bypass-approvals-and-sandbox", "--yolo"):
                    self.assertNotIn(flag, command)

    def test_execution_controls_and_optional_response_capture_are_preserved(self):
        workspace = Path("/evaluation/disposable workspace")
        for platform in ("darwin", "linux", "freebsd"):
            for response in (None, Path("/evaluation/evidence/final response.txt")):
                with self.subTest(platform=platform, response=response):
                    with patch("evaluations.runtime.codex.sys.platform", platform):
                        command = execution_command("codex", workspace, "test-model", "medium", final_response_path=response)
                    # Check argument boundaries, including paths containing spaces.
                    arguments = []
                    iterator = iter(command)
                    for argument in iterator:
                        if argument == "--config":
                            next(iterator)
                        else:
                            arguments.append(argument)
                    expected = [
                        "codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules",
                        "--ephemeral", "--json", "--color", "never", "--skip-git-repo-check",
                        "--cd", str(workspace), "--model", "test-model",
                        "--enable", "skip_host_skill_discovery",
                        "--disable", "apps", "--disable", "plugins", "--disable", "remote_plugin",
                        "--disable", "hooks", "--disable", "memories", "--disable", "multi_agent",
                        "--disable", "skill_search", "--disable", "shell_snapshot", "--disable", "daemon_auto_start",
                    ]
                    if response is not None:
                        expected.extend(["--output-last-message", str(response)])
                    self.assertEqual(arguments, [*expected, "-"])


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
    (Path(os.environ["CODEX_HOME"]) / "received-argv.json").write_text(json.dumps(sys.argv))
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
                patch("evaluations.runtime.auth.codex_executable", return_value=str(executable)),
                patch("evaluations.__main__.ARTIFACTS_ROOT", root / "runs"),
                patch.dict(os.environ, {
                    "OPENAI_API_KEY": "test-secret", "CODEX_API_KEY": "test-secret",
                    "CODEX_ACCESS_TOKEN": "test-secret", "CODEX_THREAD_ID": "parent-session",
                }),
                patch.object(sys, "argv", ["evaluations", "--codex-home", str(profile), "--model", "test-model", "--reasoning-effort", "medium"]),
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
            self.assertEqual(json.loads((profile / "received-argv.json").read_text()), execution["command"])
            self.assertEqual(execution["command"], execution_command(
                str(executable), Path(execution["workspace"]), "test-model", "medium",
            ))
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
