"""Test our authentication code without signing in to any account.

These unittest tests never launch real Codex or contact OpenAI. They replace
login with a test substitute or launch a small fake CLI using dummy credentials.
File operations are real, but confined to temporary test directories; your
credentials are untouched. No model calls or subscription usage occur.
"""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from evals import auth
from evals.__main__ import main


class AuthenticationTests(unittest.TestCase):
    def test_default_and_custom_home_paths_are_resolved_before_login(self):
        cases = (
            ([], Path.home() / ".codex-evals"),
            (["--codex-home", "~/custom-evals"], Path.home() / "custom-evals"),
            (["--codex-home", "relative-evals"], Path.cwd() / "relative-evals"),
        )
        for arguments, expected in cases:
            # patch temporarily replaces login and command-line arguments, then restores them.
            # The substitute records the path: no login runs and no profile is created.
            with (
                self.subTest(arguments=arguments),
                patch("evals.auth.login", return_value=0) as login,
                patch.object(sys, "argv", ["evals", "--login", *arguments]),
            ):
                self.assertEqual(main(), 0)
                login.assert_called_once_with(expected.resolve())

    def test_login_persists_until_explicit_logout_and_preserves_other_files(self):
        # Both profiles and the report are disposable fixtures, removed when this block ends.
        with TemporaryDirectory() as directory:
            root = Path(directory)
            profile = root / "evaluation-profile"
            everyday = root / "everyday-profile"
            everyday.mkdir()
            (everyday / "auth.json").write_text("everyday dummy credential")
            report = root / "report.json"
            report.write_text("retained evidence")
            executable = root / "codex"
            # Write a Python program that imitates login, status, and logout.
            # It runs as a real subprocess, but only creates/checks/deletes dummy files.
            executable.write_text(f"#!{sys.executable}\n" + '''
import os
from pathlib import Path
import sys

profile = Path(os.environ["CODEX_HOME"])
credential = profile / "auth.json"
if "logout" in sys.argv:
    # This marker lets the test deliberately simulate a CLI failure.
    if (profile / "fail-logout").exists():
        sys.exit(1)
    credential.unlink()
elif "status" in sys.argv:
    if not credential.exists():
        sys.exit(1)
    print("Logged in using ChatGPT")
else:
    assert "--device-auth" in sys.argv
    credential.write_text("evaluation dummy credential")
''')
            executable.chmod(0o700)
            # Force our code to launch the fake executable. The inherited home points
            # at the dummy everyday profile to check that --codex-home overrides it.
            with (
                patch("evals.auth.codex_executable", return_value=str(executable)),
                patch.dict("os.environ", {"CODEX_HOME": str(everyday)}),
                redirect_stdout(StringIO()),
            ):
                # Run our real command handler; the fake CLI supplies authentication results.
                with patch.object(sys, "argv", ["evals", "--login", "--codex-home", str(profile)]):
                    self.assertEqual(main(), 0)
                self.assertEqual((profile / "config.toml").read_text(), auth.PROFILE_CONFIG)
                auth.require_chatgpt_login(str(executable), profile)
                self.assertEqual((profile / "auth.json").read_text(), "evaluation dummy credential")

                # Failed logout returns 2 and keeps credentials; successful logout returns 0.
                failure = profile / "fail-logout"
                failure.touch()
                with patch.object(sys, "argv", ["evals", "--logout", "--codex-home", str(profile)]):
                    self.assertEqual(main(), 2)
                    self.assertTrue((profile / "auth.json").exists())
                    failure.unlink()
                    self.assertEqual(main(), 0)
                self.assertFalse((profile / "auth.json").exists())
                # After logout, our status check must reject the now-unauthenticated profile.
                with self.assertRaisesRegex(RuntimeError, "ChatGPT authentication is required"):
                    auth.require_chatgpt_login(str(executable), profile)

            # Logout must preserve configuration and unrelated dummy credentials/evidence.
            self.assertEqual((profile / "config.toml").read_text(), auth.PROFILE_CONFIG)
            self.assertEqual((everyday / "auth.json").read_text(), "everyday dummy credential")
            self.assertEqual(report.read_text(), "retained evidence")


if __name__ == "__main__":
    unittest.main()
