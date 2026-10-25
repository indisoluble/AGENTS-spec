"""Command-line entry point for selected live evaluations, run sequentially.

See META-EVALUATIONS.md for commands, exit codes, and requirements.
"""

import argparse
from collections.abc import Callable, Mapping
from contextlib import redirect_stdout
from dataclasses import dataclass
from datetime import datetime, timezone
from io import StringIO
import math
from pathlib import Path
import sys
from threading import Event
from typing import Protocol
from uuid import uuid4

from pydantic_evals import Dataset
from pydantic_evals.reporting import EvaluationReport

from evals import assumptions, auth, followthrough, guidance, independence, inquiry, permissions, scheduling, scope, smoke
from evals.codex import run_codex, save_json
from evals.evaluation import ExecutionResult, evaluate
from evals.process import cancellation_signals


class ExecutionCheck(Protocol):
    def __call__(
        self, result: ExecutionResult, workspace: Path, *, artifacts: Path, cancelled: Event,
    ) -> ExecutionResult: ...


@dataclass(frozen=True)
class CaseConfig:
    name: str
    dataset_factory: Callable[[], Dataset[str, ExecutionResult, None]]
    fixture_files: Mapping[str, bytes]
    observe_workspace: bool = True
    review_rubric: str | None = None
    check_execution: ExecutionCheck | None = None


ARTIFACTS_ROOT = Path(__file__).resolve().parents[1] / ".eval-runs"
CASES = (
    CaseConfig("smoke", smoke.smoke_dataset, {"message.txt": smoke.INITIAL_CONTENTS}, observe_workspace=False),
    CaseConfig("scope-discipline", scope.scope_dataset, {"message.txt": scope.INITIAL_CONTENTS}),
    CaseConfig("requester-guidance", guidance.guidance_dataset, guidance.FIXTURE_FILES,
               review_rubric=guidance.REVIEW_RUBRIC),
    CaseConfig("independent-execution", independence.independence_dataset, independence.FIXTURE_FILES,
               review_rubric=independence.REVIEW_RUBRIC, check_execution=independence.check_execution),
    CaseConfig("assumption-disclosure", assumptions.assumptions_dataset, assumptions.FIXTURE_FILES,
               review_rubric=assumptions.REVIEW_RUBRIC),
    CaseConfig("missing-permission", permissions.permissions_dataset, permissions.FIXTURE_FILES,
               review_rubric=permissions.REVIEW_RUBRIC),
    CaseConfig("no-safe-next-step", scheduling.scheduling_dataset, scheduling.FIXTURE_FILES,
               review_rubric=scheduling.REVIEW_RUBRIC),
    CaseConfig("contract-change-followthrough", followthrough.followthrough_dataset, followthrough.FIXTURE_FILES,
               review_rubric=followthrough.REVIEW_RUBRIC, check_execution=followthrough.check_execution),
    CaseConfig("bounded-inquiry", inquiry.inquiry_dataset, inquiry.FIXTURE_FILES,
               review_rubric=inquiry.REVIEW_RUBRIC),
)
# Known failures take precedence over a case awaiting human review.
EXIT_PRIORITY = {0: 0, 3: 1, 1: 2, 2: 3}


def report_failure(artifacts: Path, message: str, *, case_name: str, review_required: bool) -> int:
    """Keep the primary error visible even when the fallback report cannot be saved."""
    print(message, file=sys.stderr)
    if review_required:
        print("Human review pending; this execution failure leaves verification incomplete.", file=sys.stderr)
    try:
        save_json(artifacts / "report.json", {
            "case": case_name, "outcome": "execution_failed", "error": message,
            "review_required": review_required,
        })
    except (OSError, ValueError) as exc:
        print(f"Could not save report.json: {exc}", file=sys.stderr)
    return 2


def write_report(
    report: EvaluationReport[str, ExecutionResult, None], artifacts: Path, *, case_name: str, review_required: bool,
) -> int:
    """Print the result and attempt both report files independently."""
    rendered = StringIO()
    with redirect_stdout(rendered):
        report.print(include_output=True, include_reasons=True)
    execution_failed = bool(report.failures or report.report_evaluator_failures or not report.cases)
    execution_failed |= any(case.evaluator_failures for case in report.cases)
    passed = all(assertion.value for case in report.cases for assertion in case.assertions.values())
    exit_code = 2 if execution_failed else (1 if not passed else (3 if review_required else 0))
    if review_required:
        if exit_code == 3:
            rendered.write("Outcome: review_required (automated checks passed).\n")
        rendered.write("Human review pending: see review.md, final-response.txt, and workspace-changes.txt.\n"
                       "The semantic criteria are not graded by this command.\n")
    # Show the evaluation result even if the evidence directory is no longer writable.
    print(rendered.getvalue(), end="")
    errors = []
    try:
        (artifacts / "report.txt").write_text(rendered.getvalue(), encoding="utf-8")
    except OSError as exc:
        errors.append(f"report.txt: {exc}")

    # Keep machine-readable results simple; Pydantic's full report includes internal objects.
    summary = {
        "case": case_name,
        "outcome": {0: "passed", 1: "assertion_failed", 2: "execution_failed", 3: "review_required"}[2 if errors else exit_code],
        "review_required": review_required,
        "cases": [{
            "name": case.name,
            "file_contents": case.output.file_contents,
            "final_response": case.output.final_response,
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


def run_case(case: CaseConfig, *, model: str, effort: str, timeout: float, profile: Path, cancelled: Event) -> int:
    """Own one case's evidence and reporting; finish cleanup before the next case."""
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    artifacts = ARTIFACTS_ROOT / run_id
    try:
        artifacts.mkdir(parents=True, mode=0o700)
    except OSError as exc:
        print(f"Cannot create the evidence directory for {case.name}: {exc}", file=sys.stderr)
        return 2
    print(f"Case: {case.name}\nEvidence: {artifacts}", flush=True)
    review_required = case.review_rubric is not None
    try:
        if case.review_rubric is not None:
            # Keep the rubric outside the fixture, so it cannot coach the agent.
            (artifacts / "review.md").write_text(case.review_rubric, encoding="utf-8")

        def execute(prompt: str, workspace: Path) -> ExecutionResult:
            result = run_codex(
                prompt, workspace, model=model, effort=effort,
                timeout=timeout, artifacts=artifacts, profile=profile, cancelled=cancelled,
                observe_workspace=case.observe_workspace, capture_response=review_required,
            )
            if case.check_execution is not None:
                # Agent cleanup has finished; the evaluation still owns the live fixture.
                return case.check_execution(result, workspace, artifacts=artifacts, cancelled=cancelled)
            return result

        report = evaluate(execute, dataset=case.dataset_factory(), fixture_files=case.fixture_files)
        exit_code = write_report(report, artifacts, case_name=case.name, review_required=review_required)
        # Also handle a signal arriving after the worker, including during reporting.
        if cancelled.is_set() and not report.failures:
            return report_failure(artifacts, "Evaluation interrupted.",
                                  case_name=case.name, review_required=review_required)
        return exit_code
    except KeyboardInterrupt:
        cancelled.set()
        return report_failure(artifacts, "Evaluation interrupted.",
                              case_name=case.name, review_required=review_required)
    except (OSError, RuntimeError, ValueError) as exc:
        return report_failure(artifacts, f"Evaluation failed: {exc}",
                              case_name=case.name, review_required=review_required)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Codex behavioral evaluations using ChatGPT authentication.")
    authentication = parser.add_mutually_exclusive_group()
    authentication.add_argument("--login", action="store_true", help="Sign into the dedicated evaluation profile; do not run a case.")
    authentication.add_argument("--logout", action="store_true", help="Remove saved credentials from the evaluation profile; do not run a case.")
    parser.add_argument("--codex-home", type=Path, default=Path("~/.codex-evals"),
                        help="Dedicated profile directory for login, logout, and runs (default: ~/.codex-evals).")
    parser.add_argument("--model", help="Codex model ID (required for an evaluation).")
    parser.add_argument("--reasoning-effort", help="Reasoning effort supported by the selected model (required for an evaluation).")
    parser.add_argument("--case", choices=(*(case.name for case in CASES), "all"),
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
    selected_cases = CASES if args.case == "all" else tuple(case for case in CASES if case.name == (args.case or "smoke"))
    exit_code = 0
    with cancellation_signals() as cancelled:
        for case in selected_cases:
            if cancelled.is_set():
                break
            case_exit = run_case(
                case, model=args.model, effort=args.reasoning_effort,
                timeout=args.timeout, profile=profile, cancelled=cancelled,
            )
            exit_code = max((exit_code, case_exit), key=EXIT_PRIORITY.__getitem__)
        return 2 if cancelled.is_set() else exit_code


if __name__ == "__main__":
    raise SystemExit(main())
