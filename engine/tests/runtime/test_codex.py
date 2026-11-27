"""Verify the execution command, including platform-specific permission configuration."""

from pathlib import Path
import tomllib
import unittest
from unittest.mock import patch

from engine.runtime.codex import execution_command


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
                with patch("engine.runtime.codex.sys.platform", platform):
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
                    with patch("engine.runtime.codex.sys.platform", platform):
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


if __name__ == "__main__":
    unittest.main()
