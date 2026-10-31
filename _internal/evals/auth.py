"""Own the dedicated evaluation profile and its authentication lifecycle.

See EVALUATIONS.md for credential storage, lifetime, and logout semantics.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
from threading import Event

from evals.process import run_process


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
        raise RuntimeError("Codex CLI was not found on PATH. Install it separately or add its directory to PATH.")
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


def require_chatgpt_login(executable: str, profile: Path, cancelled: Event | None = None) -> None:
    """Check the login method without exposing credential contents."""
    check_profile(profile)
    status = run_process(
        [executable, "--no-daemon", "login", "status"],
        env=codex_environment(profile), cwd=profile, timeout=15, cancelled=cancelled,
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
