"""Command-line entry point for selected live evaluations, run sequentially.

See META-EVALUATIONS.md for commands, exit codes, and requirements.
"""

import argparse
from contextlib import redirect_stdout
from datetime import datetime, timezone
from functools import partial
from io import StringIO
import math
from pathlib import Path
import sys
from threading import Event
from uuid import uuid4

from pydantic_evals.reporting import EvaluationReport

from evals import auth
from evals.codex import run_codex, save_json
from evals.process import cancellation_signals
from evals.scope import INITIAL_CONTENTS, scope_dataset
from evals.smoke import ExecutionResult, evaluate


ARTIFACTS_ROOT = Path(__file__).resolve().parents[1] / ".eval-runs"
CASE_NAMES = ("smoke", "scope-discipline")


def report_failure(artifacts: Path, message: str, *, case_name: str = "smoke") -> int:
    """Keep the primary error visible even when the fallback report cannot be saved."""
    print(message, file=sys.stderr)
    try:
        save_json(artifacts / "report.json", {"case": case_name, "outcome": "execution_failed", "error": message})
    except (OSError, ValueError) as exc:
        print(f"Could not save report.json: {exc}", file=sys.stderr)
    return 2


def write_report(
    report: EvaluationReport[str, ExecutionResult, None], artifacts: Path, *, case_name: str = "smoke",
) -> int:
    """Print the result and attempt both report files independently."""
    rendered = StringIO()
    with redirect_stdout(rendered):
        report.print(include_output=True, include_reasons=True)
    # Show the evaluation result even if the evidence directory is no longer writable.
    print(rendered.getvalue(), end="")
    execution_failed = bool(report.failures or report.report_evaluator_failures or not report.cases)
    execution_failed |= any(case.evaluator_failures for case in report.cases)
    passed = all(assertion.value for case in report.cases for assertion in case.assertions.values())
    exit_code = 2 if execution_failed else (0 if passed else 1)
    errors = []
    try:
        (artifacts / "report.txt").write_text(rendered.getvalue(), encoding="utf-8")
    except OSError as exc:
        errors.append(f"report.txt: {exc}")

    # Keep machine-readable results simple; Pydantic's full report includes internal objects.
    summary = {
        "case": case_name,
        "outcome": {0: "passed", 1: "assertion_failed", 2: "execution_failed"}[2 if errors else exit_code],
        "cases": [{
            "name": case.name,
            "file_contents": case.output.file_contents,
            "assertions": {name: assertion.value for name, assertion in case.assertions.items()},
            "assertion_reasons": {name: assertion.reason for name, assertion in case.assertions.items()},
            "evaluator_errors": [str(error) for error in case.evaluator_failures],
        } for case in report.cases],
        "execution_errors": [failure.error_message for failure in report.failures],
        "report_evaluator_errors": [str(error) for error in report.report_evaluator_failures],
        "evidence_errors": errors,
    }
    try:
        save_json(artifacts / "report.json", summary)
    except (OSError, ValueError) as exc:
        errors.append(f"report.json: {exc}")
    for error in errors:
        print(f"Could not save {error}", file=sys.stderr)
    return 2 if errors else exit_code


def run_case(case_name: str, *, model: str, effort: str, timeout: float, profile: Path, cancelled: Event) -> int:
    """Own one case's evidence and reporting; finish cleanup before the next case."""
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    artifacts = ARTIFACTS_ROOT / run_id
    try:
        artifacts.mkdir(parents=True, mode=0o700)
    except OSError as exc:
        print(f"Cannot create the evidence directory for {case_name}: {exc}", file=sys.stderr)
        return 2
    print(f"Case: {case_name}\nEvidence: {artifacts}", flush=True)
    try:
        execute = partial(
            run_codex, model=model, effort=effort,
            timeout=timeout, artifacts=artifacts, profile=profile, cancelled=cancelled,
            observe_workspace=case_name == "scope-discipline",
        )
        if case_name == "scope-discipline":
            report = evaluate(execute, dataset=scope_dataset(), initial_contents=INITIAL_CONTENTS)
        else:
            report = evaluate(execute)
        exit_code = write_report(report, artifacts, case_name=case_name)
        # Also handle a signal arriving after the worker, including during reporting.
        if cancelled.is_set() and not report.failures:
            return report_failure(artifacts, "Evaluation interrupted.", case_name=case_name)
        return exit_code
    except KeyboardInterrupt:
        cancelled.set()
        return report_failure(artifacts, "Evaluation interrupted.", case_name=case_name)
    except (OSError, RuntimeError, ValueError) as exc:
        return report_failure(artifacts, f"Evaluation failed: {exc}", case_name=case_name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Codex text-edit evaluations using ChatGPT authentication.")
    authentication = parser.add_mutually_exclusive_group()
    authentication.add_argument("--login", action="store_true", help="Sign into the dedicated evaluation profile; do not run a case.")
    authentication.add_argument("--logout", action="store_true", help="Remove saved credentials from the evaluation profile; do not run a case.")
    parser.add_argument("--codex-home", type=Path, default=Path("~/.codex-evals"),
                        help="Dedicated profile directory for login, logout, and runs (default: ~/.codex-evals).")
    parser.add_argument("--model", help="Codex model ID (required for an evaluation).")
    parser.add_argument("--reasoning-effort", help="Reasoning effort supported by the selected model (required for an evaluation).")
    parser.add_argument("--case", choices=(*CASE_NAMES, "all"),
                        help="Run one case or all cases sequentially (default: smoke).")
    parser.add_argument("--timeout", type=float, default=180, help="Maximum Codex execution seconds per case (default: 180).")
    args = parser.parse_args()
    # Resolve before Codex changes its working directory to the temporary fixture.
    try:
        profile = args.codex_home.expanduser().resolve()
    except (OSError, RuntimeError) as exc:
        parser.error(f"Invalid --codex-home: {exc}")
    if args.login or args.logout:
        action = "Login" if args.login else "Logout"
        if args.model or args.reasoning_effort or args.case:
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
    selected_cases = CASE_NAMES if args.case == "all" else (args.case or "smoke",)
    exit_code = 0
    with cancellation_signals() as cancelled:
        for case_name in selected_cases:
            if cancelled.is_set():
                break
            case_exit = run_case(
                case_name, model=args.model, effort=args.reasoning_effort,
                timeout=args.timeout, profile=profile, cancelled=cancelled,
            )
            # Execution errors (2) take precedence over assertion failures (1).
            exit_code = max(exit_code, case_exit)
        return 2 if cancelled.is_set() else exit_code


if __name__ == "__main__":
    raise SystemExit(main())
