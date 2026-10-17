"""Command-line entry point for one live smoke evaluation.

Setup: python -m evals --login
Run: python -m evals --model MODEL --reasoning-effort EFFORT
Clear saved credentials: python -m evals --logout
Use --codex-home PATH with each command to select a different profile.

The suite shall use ~/.codex-evals unless --codex-home specifies another path.
The suite shall use the selected home for login, logout, and evaluation.

The suite shall exit with 0 for success, 1 for a content assertion failure,
and 2 for a setup, execution, or evaluation error.
"""

import argparse
from contextlib import redirect_stdout
from datetime import datetime, timezone
from functools import partial
from io import StringIO
import math
from pathlib import Path
import sys
from uuid import uuid4

from evals import auth
from evals.codex import run_codex, save_json
from evals.smoke import evaluate


ARTIFACTS_ROOT = Path(__file__).resolve().parents[1] / ".eval-runs"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one Codex text-edit evaluation using ChatGPT authentication.")
    authentication = parser.add_mutually_exclusive_group()
    authentication.add_argument("--login", action="store_true", help="Sign into the dedicated evaluation profile; do not run a case.")
    authentication.add_argument("--logout", action="store_true", help="Remove saved credentials from the evaluation profile; do not run a case.")
    parser.add_argument("--codex-home", type=Path, default=Path("~/.codex-evals"),
                        help="Dedicated profile directory for login, logout, and runs (default: ~/.codex-evals).")
    parser.add_argument("--model", help="Codex model ID (required for an evaluation).")
    parser.add_argument("--reasoning-effort", help="Reasoning effort supported by the selected model (required for an evaluation).")
    parser.add_argument("--timeout", type=float, default=180, help="Maximum Codex execution seconds (default: 180).")
    args = parser.parse_args()
    # Resolve before Codex changes its working directory to the temporary fixture.
    try:
        profile = args.codex_home.expanduser().resolve()
    except (OSError, RuntimeError) as exc:
        parser.error(f"Invalid --codex-home: {exc}")
    if args.login or args.logout:
        action = "Login" if args.login else "Logout"
        if args.model or args.reasoning_effort:
            parser.error("--login/--logout cannot be combined with evaluation settings")
        try:
            return 0 if (auth.login(profile) if args.login else auth.logout(profile)) == 0 else 2
        except KeyboardInterrupt:
            print(f"{action} interrupted.", file=sys.stderr)
            return 2
        except (OSError, RuntimeError) as exc:
            print(f"{action} failed: {exc}", file=sys.stderr)
            return 2
    if not args.model or not args.reasoning_effort:
        parser.error("--model and --reasoning-effort are required unless using --login or --logout")
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout must be a positive, finite number")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    artifacts = ARTIFACTS_ROOT / run_id
    try:
        artifacts.mkdir(parents=True, mode=0o700)
    except OSError as exc:
        print(f"Cannot create the evidence directory: {exc}", file=sys.stderr)
        return 2
    print(f"Evidence: {artifacts}", flush=True)
    execute = partial(
        run_codex, model=args.model, effort=args.reasoning_effort,
        timeout=args.timeout, artifacts=artifacts, profile=profile,
    )
    try:
        report = evaluate(execute)
        # Save the same human-readable report that appears in the terminal.
        rendered = StringIO()
        with redirect_stdout(rendered):
            report.print(include_output=True, include_reasons=True)
        (artifacts / "report.txt").write_text(rendered.getvalue(), encoding="utf-8")
        print(rendered.getvalue(), end="")
        execution_failed = bool(report.failures or report.report_evaluator_failures or not report.cases)
        execution_failed |= any(case.evaluator_failures for case in report.cases)
        passed = all(assertion.value for case in report.cases for assertion in case.assertions.values())
        exit_code = 2 if execution_failed else (0 if passed else 1)
        # Keep machine-readable results simple; Pydantic's full report includes internal objects.
        save_json(artifacts / "report.json", {
            "outcome": {0: "passed", 1: "assertion_failed", 2: "execution_failed"}[exit_code],
            "cases": [{
                "name": case.name,
                "file_contents": case.output.file_contents,
                "assertions": {name: assertion.value for name, assertion in case.assertions.items()},
                "evaluator_errors": [str(error) for error in case.evaluator_failures],
            } for case in report.cases],
            "execution_errors": [failure.error_message for failure in report.failures],
            "report_evaluator_errors": [str(error) for error in report.report_evaluator_failures],
        })
        return exit_code
    except KeyboardInterrupt:
        save_json(artifacts / "report.json", {"outcome": "execution_failed", "error": "Interrupted"})
        print("Evaluation interrupted.", file=sys.stderr)
        return 2
    except (OSError, RuntimeError, ValueError) as exc:
        save_json(artifacts / "report.json", {"outcome": "execution_failed", "error": str(exc)})
        print(f"Evaluation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
