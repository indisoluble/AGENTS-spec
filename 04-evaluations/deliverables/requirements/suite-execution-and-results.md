# Suite execution and results

These requirements cover case selection and order, exit status, report identity, and pending human review. See the [case and suite commands](../../docs/running-and-reviewing.md#run-a-case-or-the-suite) and the [outcome definitions](../../docs/running-and-reviewing.md#outcomes-and-exit-codes).

These requirements govern evaluator behavior. The [product baseline](../../../01-behavior/deliverables/baseline.md) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E11

The suite shall return 2 for any setup, execution, capture, inspection, interruption, evaluation, or evidence-write failure; otherwise 1 for any automated assertion failure; otherwise 3 for pending human review; otherwise 0 for fully graded success.

**Checks.** [test_auth.py](../tests/runtime/test_auth.py), [test_codex.py](../tests/runtime/test_codex.py), [test_cli.py](../tests/runtime/test_cli.py), [test_evidence.py](../tests/runtime/test_evidence.py), [test_guidance.py](../tests/scenarios/test_guidance.py)

## E12

When an evaluation is requested, the suite shall accept `smoke`, `scope-discipline`, `requester-guidance`, `independent-execution`, `assumption-disclosure`, `missing-permission`, `no-safe-next-step`, `contract-change-followthrough`, `bounded-inquiry`, `durable-finding-review`, or `all`, default to `smoke`, and reject unknown selections before launching Codex.

**Checks.** [test_codex.py](../tests/runtime/test_codex.py), [test_cli.py](../tests/runtime/test_cli.py), [test_findings.py](../tests/scenarios/test_findings.py)

## E14

When writing a JSON report, the suite shall include the selected case name, including failure reports.

**Checks.** [test_codex.py](../tests/runtime/test_codex.py), [test_cli.py](../tests/runtime/test_cli.py), [test_evidence.py](../tests/runtime/test_evidence.py)

## E15

When `all` is selected, the suite shall run `smoke`, `scope-discipline`, `requester-guidance`, `independent-execution`, `assumption-disclosure`, `missing-permission`, `no-safe-next-step`, `contract-change-followthrough`, `bounded-inquiry`, then `durable-finding-review` sequentially with independent evidence, complete each case's cleanup before the next, continue after ordinary failures, and stop the sequence on interruption.

**Checks.** [test_cli.py](../tests/runtime/test_cli.py)

## E26

When reporting requester-guidance, independent-execution, assumption-disclosure, missing-permission, no-safe-next-step, contract-change-followthrough, bounded-inquiry, or durable-finding-review, the suite shall retain `review_required: true` even if an error or assertion failure determines the outcome, report outcome `review_required` when automated checks pass, and display that human assessment remains pending without collecting a verdict.

**Checks.** [test_guidance.py](../tests/scenarios/test_guidance.py), [test_cli.py](../tests/runtime/test_cli.py), [test_assumptions.py](../tests/scenarios/test_assumptions.py)
