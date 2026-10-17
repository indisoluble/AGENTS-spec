"""Own the dedicated evaluation profile and its authentication lifecycle.

The suite shall retain credentials between runs until explicit logout.
When logout is requested, the suite shall ask Codex to remove credentials
from the evaluation profile only.

Codex stores plaintext credentials in auth.json under the selected Codex home.
Codex manages token refresh; the suite never reads or copies credential contents.
Logout removes local credentials; server-side revocation is not guaranteed.
See https://learn.chatgpt.com/docs/auth for Codex's storage and refresh behavior.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess


AUTH_SETTINGS = {"forced_login_method": "chatgpt", "cli_auth_credentials_store": "file"}
PROFILE_CONFIG = "".join(f"{key} = {json.dumps(value)}\n" for key, value in AUTH_SETTINGS.items())


def codex_environment(profile: Path) -> dict[str, str]:
    # An allowlist excludes API keys, parent-session settings, and provider overrides.
    names = (
        "HOME", "PATH", "USER", "LOGNAME", "TMPDIR", "LANG", "LC_ALL",
        "SSL_CERT_FILE", "SSL_CERT_DIR", "CODEX_CA_CERTIFICATE",
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
        "http_proxy", "https_proxy", "all_proxy", "no_proxy",
    )
    environment = {name: os.environ[name] for name in names if name in os.environ}
    environment["CODEX_HOME"] = str(profile)
    return environment


def check_profile(profile: Path) -> None:
    if not (profile / "config.toml").is_file():
        raise RuntimeError("Evaluation profile is missing. Run python -m evals --login with the same --codex-home")
    if (profile / "config.toml").read_text() != PROFILE_CONFIG:
        raise RuntimeError(f"Unexpected evaluation profile configuration: {profile}")
    for name in ("AGENTS.md", "AGENTS.override.md"):
        if (profile / name).exists():
            raise RuntimeError(f"Personal instructions are not allowed in the evaluation profile: {name}")


def codex_executable() -> str:
    executable = shutil.which("codex")
    if executable is None:
        raise RuntimeError("Codex CLI was not found on PATH.")
    return executable


def login(profile: Path) -> int:
    """Authenticate separately from everyday Codex; never copy existing credentials."""
    executable = codex_executable()
    profile.mkdir(parents=True, exist_ok=True, mode=0o700)
    config = profile / "config.toml"
    if not config.exists():
        config.write_text(PROFILE_CONFIG, encoding="utf-8")
    check_profile(profile)
    print(f"Signing into the evaluation profile at {profile}", flush=True)
    return subprocess.call(
        [executable, "--no-daemon", "login", "--device-auth"],
        cwd=profile,
        env=codex_environment(profile),
    )


def require_chatgpt_login(executable: str, profile: Path) -> None:
    """Check the login method without exposing credential contents."""
    check_profile(profile)
    status = subprocess.run(
        [executable, "--no-daemon", "login", "status"], capture_output=True,
        text=True, env=codex_environment(profile), cwd=profile, timeout=15,
    )
    if status.returncode or "Logged in using ChatGPT" not in status.stdout + status.stderr:
        raise RuntimeError("ChatGPT authentication is required. Run python -m evals --login with the same --codex-home")


def logout(profile: Path) -> int:
    """Clear the dedicated login; keep its configuration and evaluation reports."""
    executable = codex_executable()
    check_profile(profile)
    print(f"Removing saved credentials from the evaluation profile at {profile}", flush=True)
    return subprocess.call(
        [executable, "--no-daemon", "logout"],
        cwd=profile,
        env=codex_environment(profile),
    )
