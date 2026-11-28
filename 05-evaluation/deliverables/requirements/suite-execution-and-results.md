# Suite execution and results

These requirements cover case selection and order, exit status, report identity, pending human review, and execution and reporting obligations for registered cases. See the case and suite commands ([`05-evaluation/docs/running-and-reviewing.md` § Run a case or the suite](../../docs/running-and-reviewing.md#run-a-case-or-the-suite)) and the outcome definitions ([`05-evaluation/docs/running-and-reviewing.md` § Outcomes and exit codes](../../docs/running-and-reviewing.md#outcomes-and-exit-codes)).

These requirements govern evaluator behavior. The product baseline ([`02.0-formulation/deliverables/baseline.md`](../../../02.0-formulation/deliverables/baseline.md)) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E11

The suite shall return 2 for any setup, execution, capture, inspection, interruption, evaluation, or evidence-write failure; otherwise 1 for any automated assertion failure; otherwise 3 for pending human review; otherwise 0 for fully graded success.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/runtime/test_auth.py`](../evaluation/tests/runtime/test_auth.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_codex.py`](../evaluation/tests/runtime/test_codex.py), [`engine/tests/runtime/test_codex.py`](../../../engine/tests/runtime/test_codex.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_cli.py`](../evaluation/tests/runtime/test_cli.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_evidence.py`](../evaluation/tests/runtime/test_evidence.py), [`05-evaluation/deliverables/evaluation/tests/scenarios/test_guidance.py`](../evaluation/tests/scenarios/test_guidance.py)

## E12

When an evaluation is requested, the suite shall accept `smoke`, `scope-discipline`, `requester-guidance`, `independent-execution`, `assumption-disclosure`, `missing-permission`, `no-safe-next-step`, `contract-change-followthrough`, `bounded-inquiry`, `durable-finding-review`, or `all`, default to `smoke`, and reject unknown selections before launching Codex.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/runtime/test_codex.py`](../evaluation/tests/runtime/test_codex.py), [`engine/tests/runtime/test_codex.py`](../../../engine/tests/runtime/test_codex.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_cli.py`](../evaluation/tests/runtime/test_cli.py), [`05-evaluation/deliverables/evaluation/tests/scenarios/test_findings.py`](../evaluation/tests/scenarios/test_findings.py), [`03.1-conformance/deliverables/conformance/tests/test_findings.py`](../../../03.1-conformance/deliverables/conformance/tests/test_findings.py)

## E13

When scope-discipline execution and inspection complete, the suite shall report independent `RequestedChange` and `ScopePreserved` assertions according to [`03.1-conformance/deliverables/cases/scope-discipline.md` § Automated assessment](../../../03.1-conformance/deliverables/cases/scope-discipline.md#automated-assessment), failing both for missing or non-regular `message.txt`.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_scope.py`](../evaluation/tests/scenarios/test_scope.py), [`03.1-conformance/deliverables/conformance/tests/test_scope.py`](../../../03.1-conformance/deliverables/conformance/tests/test_scope.py)

## E14

When writing a JSON report, the suite shall include the selected case name, including failure reports.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/runtime/test_codex.py`](../evaluation/tests/runtime/test_codex.py), [`engine/tests/runtime/test_codex.py`](../../../engine/tests/runtime/test_codex.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_cli.py`](../evaluation/tests/runtime/test_cli.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_evidence.py`](../evaluation/tests/runtime/test_evidence.py)

## E15

When `all` is selected, the suite shall run `smoke`, `scope-discipline`, `requester-guidance`, `independent-execution`, `assumption-disclosure`, `missing-permission`, `no-safe-next-step`, `contract-change-followthrough`, `bounded-inquiry`, then `durable-finding-review` sequentially with independent evidence, complete each case's cleanup before the next, continue after ordinary failures, and stop the sequence on interruption.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/runtime/test_cli.py`](../evaluation/tests/runtime/test_cli.py)

## E25

When running requester-guidance, the suite shall use the fixture and prompt in [`03.1-conformance/deliverables/conformance/guidance.py`](../../../03.1-conformance/deliverables/conformance/guidance.py), enable final-response capture, and report only the two automated assertions defined in [`03.1-conformance/deliverables/cases/requester-guidance.md` § Automated assessment](../../../03.1-conformance/deliverables/cases/requester-guidance.md#automated-assessment), leaving semantic assessment to the retained human rubric.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_guidance.py`](../evaluation/tests/scenarios/test_guidance.py), live run

## E26

When reporting requester-guidance, independent-execution, assumption-disclosure, missing-permission, no-safe-next-step, contract-change-followthrough, bounded-inquiry, or durable-finding-review, the suite shall retain `review_required: true` even if an error or assertion failure determines the outcome, report outcome `review_required` when automated checks pass, and display that human assessment remains pending without collecting a verdict.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_guidance.py`](../evaluation/tests/scenarios/test_guidance.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_cli.py`](../evaluation/tests/runtime/test_cli.py), [`05-evaluation/deliverables/evaluation/tests/scenarios/test_assumptions.py`](../evaluation/tests/scenarios/test_assumptions.py)

## E32

When running independent-execution, the suite shall use the fixture and prompt in [`03.1-conformance/deliverables/conformance/independence.py`](../../../03.1-conformance/deliverables/conformance/independence.py), capture the response and workspace, and report the four independent assertions defined in [`03.1-conformance/deliverables/cases/independent-execution.md` § Automated assessment](../../../03.1-conformance/deliverables/cases/independent-execution.md#automated-assessment), leaving the semantic criteria to its retained human rubric.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_independence.py`](../evaluation/tests/scenarios/test_independence.py), live run

## E33

When checking independent-execution or contract-change-followthrough output after agent cleanup, the suite shall run the selected case's evaluator-owned scripts (two for independent-execution, three for contract-change-followthrough) sequentially before workspace removal, fail affected assertions for observed missing/non-regular required files without executing them, and distinguish completed nonzero checks from infrastructure errors.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_independence.py`](../evaluation/tests/scenarios/test_independence.py), [`05-evaluation/deliverables/evaluation/tests/scenarios/test_followthrough.py`](../evaluation/tests/scenarios/test_followthrough.py), [`03.1-conformance/deliverables/conformance/tests/test_followthrough.py`](../../../03.1-conformance/deliverables/conformance/tests/test_followthrough.py) (supporting fixture verification), [`05-evaluation/deliverables/evaluation/tests/runtime/test_cli.py`](../evaluation/tests/runtime/test_cli.py), [`engine/tests/runtime/test_functional.py`](../../../engine/tests/runtime/test_functional.py), [`engine/tests/runtime/test_functional_checks.py`](../../../engine/tests/runtime/test_functional_checks.py)

## E35

When running assumption-disclosure, the suite shall use the fixture and prompt in [`03.1-conformance/deliverables/conformance/assumptions.py`](../../../03.1-conformance/deliverables/conformance/assumptions.py), capture the response and workspace, and report the three independent assertions defined in [`03.1-conformance/deliverables/cases/assumption-disclosure.md` § Automated assessment](../../../03.1-conformance/deliverables/cases/assumption-disclosure.md#automated-assessment), leaving assumption disclosure assessment, including whether it was exercised, to the retained human rubric.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_assumptions.py`](../evaluation/tests/scenarios/test_assumptions.py), live run

## E36

When running missing-permission, the suite shall use the fixture and prompt in [`03.1-conformance/deliverables/conformance/permissions.py`](../../../03.1-conformance/deliverables/conformance/permissions.py), capture the response and workspace, and report the two assertions defined in [`03.1-conformance/deliverables/cases/missing-permission.md` § Automated assessment](../../../03.1-conformance/deliverables/cases/missing-permission.md#automated-assessment), permitting no cleanup or consistent partial cleanup while preserving the operational rollback relationship and leaving semantic compliance to the retained human rubric.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_permissions.py`](../evaluation/tests/scenarios/test_permissions.py), [`03.1-conformance/deliverables/conformance/tests/test_permissions.py`](../../../03.1-conformance/deliverables/conformance/tests/test_permissions.py), live run

## E37

When running no-safe-next-step, the suite shall use the fixture and prompt in [`03.1-conformance/deliverables/conformance/scheduling.py`](../../../03.1-conformance/deliverables/conformance/scheduling.py), capture the response and workspace, and report the two assertions defined in [`03.1-conformance/deliverables/cases/no-safe-next-step.md` § Automated assessment](../../../03.1-conformance/deliverables/cases/no-safe-next-step.md#automated-assessment), protecting active operational state and established constraints while allowing draft preparation and leaving alternatives, trade-offs, direction, and progress reporting to the retained human rubric.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_scheduling.py`](../evaluation/tests/scenarios/test_scheduling.py), [`03.1-conformance/deliverables/conformance/tests/test_scheduling.py`](../../../03.1-conformance/deliverables/conformance/tests/test_scheduling.py), live run

## E38

When running contract-change-followthrough, the suite shall use the fixture and prompt in [`03.1-conformance/deliverables/conformance/followthrough.py`](../../../03.1-conformance/deliverables/conformance/followthrough.py), capture the response and workspace, and report the five independent assertions defined in [`03.1-conformance/deliverables/cases/contract-change-followthrough.md` § Automated assessment](../../../03.1-conformance/deliverables/cases/contract-change-followthrough.md#automated-assessment), leaving semantic follow-through assessment to its retained human rubric.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_followthrough.py`](../evaluation/tests/scenarios/test_followthrough.py), [`03.1-conformance/deliverables/conformance/tests/test_followthrough.py`](../../../03.1-conformance/deliverables/conformance/tests/test_followthrough.py), live run/human review

## E39

When running bounded-inquiry, the suite shall use the fixture and prompt in [`03.1-conformance/deliverables/conformance/inquiry.py`](../../../03.1-conformance/deliverables/conformance/inquiry.py), capture the response and workspace, and report the three independent assertions defined in [`03.1-conformance/deliverables/cases/bounded-inquiry.md` § Automated assessment](../../../03.1-conformance/deliverables/cases/bounded-inquiry.md#automated-assessment) using evaluator-owned output and conditional feasibility expectations, distinguishing consistent partial evidence from task completion and leaving measurement provenance, actual inquiry applicability, exercised §2.4 obligations, and §3.7 reporting to its retained human rubric.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_inquiry.py`](../evaluation/tests/scenarios/test_inquiry.py), [`03.1-conformance/deliverables/conformance/tests/test_inquiry.py`](../../../03.1-conformance/deliverables/conformance/tests/test_inquiry.py), live run/human review

## E40

When running durable-finding-review, the suite shall use the fixture and prompt in [`03.1-conformance/deliverables/conformance/findings.py`](../../../03.1-conformance/deliverables/conformance/findings.py), capture the response and workspace, and report only the two automated assertions defined in [`03.1-conformance/deliverables/cases/durable-finding-review.md` § Automated assessment](../../../03.1-conformance/deliverables/cases/durable-finding-review.md#automated-assessment), retaining its human rubric outside the agent workspace and leaving technical discovery, record adequacy, and semantic compliance to human assessment without post-agent functional execution.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_findings.py`](../evaluation/tests/scenarios/test_findings.py), [`03.1-conformance/deliverables/conformance/tests/test_findings.py`](../../../03.1-conformance/deliverables/conformance/tests/test_findings.py), live run/human review
