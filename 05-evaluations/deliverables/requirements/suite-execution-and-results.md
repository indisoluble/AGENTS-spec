# Suite execution and results

These requirements cover case selection and order, exit status, report identity, and pending human review. See the case and suite commands ([`05-evaluations/docs/running-and-reviewing.md` § Run a case or the suite](../../docs/running-and-reviewing.md#run-a-case-or-the-suite)) and the outcome definitions ([`05-evaluations/docs/running-and-reviewing.md` § Outcomes and exit codes](../../docs/running-and-reviewing.md#outcomes-and-exit-codes)).

These requirements govern evaluator behavior. The product baseline ([`02-formulation/deliverables/baseline.md`](../../../02-formulation/deliverables/baseline.md)) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E11

The suite shall return 2 for any setup, execution, capture, inspection, interruption, evaluation, or evidence-write failure; otherwise 1 for any automated assertion failure; otherwise 3 for pending human review; otherwise 0 for fully graded success.

**Checks.** [`05-evaluations/deliverables/tests/runtime/test_auth.py`](../tests/runtime/test_auth.py), [`05-evaluations/deliverables/tests/runtime/test_codex.py`](../tests/runtime/test_codex.py), [`05-evaluations/deliverables/tests/runtime/test_cli.py`](../tests/runtime/test_cli.py), [`05-evaluations/deliverables/tests/runtime/test_evidence.py`](../tests/runtime/test_evidence.py), [`05-evaluations/deliverables/tests/scenarios/test_guidance.py`](../tests/scenarios/test_guidance.py)

## E12

When an evaluation is requested, the suite shall accept `smoke`, `scope-discipline`, `requester-guidance`, `independent-execution`, `assumption-disclosure`, `missing-permission`, `no-safe-next-step`, `contract-change-followthrough`, `bounded-inquiry`, `durable-finding-review`, or `all`, default to `smoke`, and reject unknown selections before launching Codex.

**Checks.** [`05-evaluations/deliverables/tests/runtime/test_codex.py`](../tests/runtime/test_codex.py), [`05-evaluations/deliverables/tests/runtime/test_cli.py`](../tests/runtime/test_cli.py), [`05-evaluations/deliverables/tests/scenarios/test_findings.py`](../tests/scenarios/test_findings.py)

## E14

When writing a JSON report, the suite shall include the selected case name, including failure reports.

**Checks.** [`05-evaluations/deliverables/tests/runtime/test_codex.py`](../tests/runtime/test_codex.py), [`05-evaluations/deliverables/tests/runtime/test_cli.py`](../tests/runtime/test_cli.py), [`05-evaluations/deliverables/tests/runtime/test_evidence.py`](../tests/runtime/test_evidence.py)

## E15

When `all` is selected, the suite shall run `smoke`, `scope-discipline`, `requester-guidance`, `independent-execution`, `assumption-disclosure`, `missing-permission`, `no-safe-next-step`, `contract-change-followthrough`, `bounded-inquiry`, then `durable-finding-review` sequentially with independent evidence, complete each case's cleanup before the next, continue after ordinary failures, and stop the sequence on interruption.

**Checks.** [`05-evaluations/deliverables/tests/runtime/test_cli.py`](../tests/runtime/test_cli.py)

## E26

When reporting requester-guidance, independent-execution, assumption-disclosure, missing-permission, no-safe-next-step, contract-change-followthrough, bounded-inquiry, or durable-finding-review, the suite shall retain `review_required: true` even if an error or assertion failure determines the outcome, report outcome `review_required` when automated checks pass, and display that human assessment remains pending without collecting a verdict.

**Checks.** [`05-evaluations/deliverables/tests/scenarios/test_guidance.py`](../tests/scenarios/test_guidance.py), [`05-evaluations/deliverables/tests/runtime/test_cli.py`](../tests/runtime/test_cli.py), [`05-evaluations/deliverables/tests/scenarios/test_assumptions.py`](../tests/scenarios/test_assumptions.py)
