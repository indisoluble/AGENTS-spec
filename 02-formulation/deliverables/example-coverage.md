# Requirement-to-scenario coverage

Discovery owns the [proposed examples and their status](../../01-discovery/deliverables/example-coverage.md#reading-a-proposed-example). Formulation compares each mapped example with an [accepted requirement](baseline.md). Read across a requirement’s row to find its examples, or look up an EX identifier to find every requirement it illustrates.

- **Direct** (51 examples). The proposed outcome illustrates the primary requirement with its qualifications and can be described without prescribing how to achieve it.
- **Detail review** (9 examples). The proposed outcome depends on a particular procedure or interpretation. The note beside each link names that detail. Its inclusion in an example does not establish it as a requirement. This classification can apply even after the requester has answered the underlying question.

Each of the 60 examples appears once in those two columns. “Also exercised by” lists examples whose primary association is elsewhere. For instance, [EX-BI-003] illustrates BR4 and also exercises BR3 and BR6. These relationships record what the proposals illustrate. Acceptance as a defining example takes a separate decision. Completeness, behavioral compliance and evaluation coverage each require separate evidence.

| Accepted requirement | Direct examples | Detail review examples | Also exercised by |
| --- | --- | --- | --- |
| [BR1](baseline.md#br1--focused-proportionate-authorized-work) | [EX-PS-001], [EX-PS-002], [EX-PS-003], [EX-PS-004], [EX-PS-005], [EX-PS-006] | — | [EX-AC-004], [EX-AC-012] |
| [BR2](baseline.md#br2--evidence-based-planning-and-knowledge-ownership) | [EX-PS-007], [EX-PS-008], [EX-PS-009] | [EX-PS-010] (which source owns a project fact and what an instruction file can establish) | [EX-VL-007] |
| [BR3](baseline.md#br3--autonomy-within-authorization-and-prior-direction) | [EX-AC-001], [EX-AC-002], [EX-AC-003], [EX-AC-004], [EX-AC-005], [EX-AC-006], [EX-AC-007], [EX-AC-009] | [EX-AC-008] (an informal expectation compared with an explicit limit) | [EX-PS-004], [EX-BI-003], [EX-AC-013], [EX-KD-004] |
| [BR4](baseline.md#br4--bounded-investigation-and-timely-reassessment) | [EX-BI-001], [EX-BI-002], [EX-BI-003], [EX-BI-005], [EX-BI-008] | [EX-BI-004] (routine reading and ordinary regression checks), [EX-BI-006] (whether the purpose of a benchmark changes the need for notice), [EX-BI-007] (reading existing project documents to resolve a blocker) | — |
| [BR5](baseline.md#br5--completion-supported-by-validation) | [EX-VL-001], [EX-VL-002], [EX-VL-003], [EX-VL-004], [EX-VL-005], [EX-VL-006] | — | [EX-PS-005], [EX-EQ-001] |
| [BR6](baseline.md#br6--learning-from-observed-results) | [EX-VL-007], [EX-VL-008], [EX-VL-009] | — | [EX-PS-002], [EX-BI-003], [EX-VL-005], [EX-KD-001] |
| [BR7](baseline.md#br7--proportionate-communication-and-actionable-handoffs) | [EX-AC-010], [EX-AC-011], [EX-AC-012], [EX-AC-013], [EX-AC-014] | — | [EX-AC-005], [EX-AC-006], [EX-BI-001], [EX-KD-005] |
| [BR8](baseline.md#br8--durable-knowledge-without-expanded-editing-authority) | [EX-KD-001], [EX-KD-002], [EX-KD-004], [EX-KD-005], [EX-KD-006] | [EX-KD-003] (when recording a compromise as technical debt is optional), [EX-KD-007] (maintaining an existing debt entry after resolution, even though creating it was optional) | [EX-VL-008], [EX-KD-010] |
| [BR9](baseline.md#br9--engineering-quality-and-preservation) | [EX-EQ-001], [EX-EQ-002], [EX-EQ-003], [EX-EQ-004] | [EX-EQ-005] (evidence for treating code as dead) | [EX-PS-001], [EX-VL-006] |
| [BR10](baseline.md#br10--affected-requirements-and-documentation) | [EX-KD-008], [EX-KD-009], [EX-KD-010] | [EX-KD-011] (how a coverage proposal, a requester deferral and an agreed need for a guide affect the response) | [EX-KD-004], [EX-EQ-002] |
| [PR1](baseline.md#established-product-requirement) | [EX-SD-001], [EX-SD-002], [EX-SD-003] | — | — |

The proposed examples illustrating accepted clarifications are [EX-PS-003] and [EX-PS-005] (coherence and recovery), [EX-AC-006] (unauthorized consequential choice), [EX-AC-012] and [EX-AC-013] (limits, consumed allowances, and resumption), [EX-KD-004] and [EX-KD-005] (assessment-write boundaries), and [EX-KD-010] (out-of-scope gaps). [EX-BI-003] and [EX-BI-008] distinguish justified continuation after an inconclusive step from repetition without supporting findings. Limits of two attempts in particular fixtures are requester-imposed examples, not a default investigation budget.

## Historical example IDs

Use this lookup to resolve older references. Each row names the same example across all three schemes. The matrix above records its current requirement associations.

| Original BR/PR example ID | Previous sequential ID | Current Discovery ID |
| --- | --- | --- |
| BR1.1 | EX-001 | [EX-PS-001] |
| BR1.2 | EX-002 | [EX-PS-002] |
| BR1.3 | EX-003 | [EX-PS-003] |
| BR1.4 | EX-004 | [EX-PS-004] |
| BR1.5 | EX-005 | [EX-PS-005] |
| BR1.6 | EX-006 | [EX-PS-006] |
| BR2.1 | EX-007 | [EX-PS-007] |
| BR2.2 | EX-008 | [EX-PS-008] |
| BR2.3 | EX-009 | [EX-PS-009] |
| BR2.4 | EX-010 | [EX-PS-010] |
| BR3.1 | EX-011 | [EX-AC-001] |
| BR3.2 | EX-012 | [EX-AC-002] |
| BR3.3 | EX-013 | [EX-AC-003] |
| BR3.4 | EX-014 | [EX-AC-004] |
| BR3.5 | EX-015 | [EX-AC-005] |
| BR3.6 | EX-016 | [EX-AC-006] |
| BR3.7 | EX-017 | [EX-AC-007] |
| BR3.8 | EX-018 | [EX-AC-008] |
| BR3.9 | EX-019 | [EX-AC-009] |
| BR7.1 | EX-020 | [EX-AC-010] |
| BR7.2 | EX-021 | [EX-AC-011] |
| BR7.3 | EX-022 | [EX-AC-012] |
| BR7.4 | EX-023 | [EX-AC-013] |
| BR7.5 | EX-024 | [EX-AC-014] |
| BR4.1 | EX-025 | [EX-BI-001] |
| BR4.2 | EX-026 | [EX-BI-002] |
| BR4.3 | EX-027 | [EX-BI-003] |
| BR4.4 | EX-028 | [EX-BI-004] |
| BR4.5 | EX-029 | [EX-BI-005] |
| BR4.6 | EX-030 | [EX-BI-006] |
| BR4.7 | EX-031 | [EX-BI-007] |
| BR4.8 | EX-032 | [EX-BI-008] |
| BR5.1 | EX-033 | [EX-VL-001] |
| BR5.2 | EX-034 | [EX-VL-002] |
| BR5.3 | EX-035 | [EX-VL-003] |
| BR5.4 | EX-036 | [EX-VL-004] |
| BR5.5 | EX-037 | [EX-VL-005] |
| BR5.6 | EX-038 | [EX-VL-006] |
| BR6.1 | EX-039 | [EX-VL-007] |
| BR6.2 | EX-040 | [EX-VL-008] |
| BR6.3 | EX-041 | [EX-VL-009] |
| BR8.1 | EX-042 | [EX-KD-001] |
| BR8.2 | EX-043 | [EX-KD-002] |
| BR8.3 | EX-044 | [EX-KD-003] |
| BR8.4 | EX-045 | [EX-KD-004] |
| BR8.5 | EX-046 | [EX-KD-005] |
| BR8.6 | EX-047 | [EX-KD-006] |
| BR8.7 | EX-048 | [EX-KD-007] |
| BR10.1 | EX-049 | [EX-KD-008] |
| BR10.2 | EX-050 | [EX-KD-009] |
| BR10.3 | EX-051 | [EX-KD-010] |
| BR10.4 | EX-052 | [EX-KD-011] |
| BR9.1 | EX-053 | [EX-EQ-001] |
| BR9.2 | EX-054 | [EX-EQ-002] |
| BR9.3 | EX-055 | [EX-EQ-003] |
| BR9.4 | EX-056 | [EX-EQ-004] |
| BR9.5 | EX-057 | [EX-EQ-005] |
| PR1.1 | EX-058 | [EX-SD-001] |
| PR1.2 | EX-059 | [EX-SD-002] |
| PR1.3 | EX-060 | [EX-SD-003] |

[EX-PS-001]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-001--fix-the-defect-and-its-necessary-dependents
[EX-PS-002]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-002--reassess-before-extending-the-work
[EX-PS-003]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-003--explain-a-step-that-cannot-stand-alone-before-starting-it
[EX-PS-004]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-004--stop-at-the-end-of-the-authorized-task
[EX-PS-005]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-005--honor-a-required-stop-with-unfinished-work
[EX-PS-006]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-006--match-planning-depth-to-the-next-decision
[EX-PS-007]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-007--inspect-what-matters-before-choosing-the-fix
[EX-PS-008]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-008--a-passing-test-does-not-settle-what-the-product-should-do
[EX-PS-009]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-009--ask-when-the-sources-cannot-settle-a-consequential-choice
[EX-PS-010]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-ps-010--use-instruction-files-for-conduct-not-proof-of-project-facts
[EX-AC-001]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-001--a-routine-local-choice-needs-no-new-requester-decision
[EX-AC-002]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-002--do-not-infer-permission-for-a-consequential-change
[EX-AC-003]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-003--use-specific-direction-already-given
[EX-AC-004]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-004--do-not-pass-a-checkpoint-or-enlarge-a-limit-on-your-own
[EX-AC-005]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-005--disclose-a-material-assumption-at-the-applicable-reporting-occasion
[EX-AC-006]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-006--disclose-a-consequential-choice-made-without-prior-direction
[EX-AC-007]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-007--normally-ask-about-other-unsettled-material-choices
[EX-AC-008]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-008--distinguish-an-expectation-from-a-binding-limit
[EX-AC-009]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-009--local-work-and-tool-capability-do-not-authorize-an-external-action
[EX-AC-010]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-010--frame-substantial-work-without-creating-an-approval-gate
[EX-AC-011]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-011--report-results-and-disclose-blockers-in-time
[EX-AC-012]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-012--transfer-remaining-work-and-used-allowances
[EX-AC-013]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-013--recover-missing-authority-before-dependent-work
[EX-AC-014]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-ac-014--useful-updates-are-permitted-without-a-report-per-increment
[EX-BI-001]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-bi-001--tell-the-requester-what-is-blocking-progress
[EX-BI-002]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-bi-002--stop-when-there-is-enough-evidence
[EX-BI-003]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-bi-003--review-an-inconclusive-step-before-doing-more
[EX-BI-004]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-bi-004--ordinary-checking-does-not-require-an-inquiry-notice
[EX-BI-005]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-bi-005--a-notice-already-given-need-not-be-repeated
[EX-BI-006]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-bi-006--a-prescribed-procedure-can-still-be-inquiry
[EX-BI-007]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-bi-007--reading-existing-project-documents-remains-context-gathering
[EX-BI-008]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-bi-008--an-unanswered-question-is-not-evidence-for-another-attempt
[EX-VL-001]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-vl-001--run-relevant-checks-that-are-available
[EX-VL-002]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-vl-002--substitute-evidence-only-when-the-missing-check-was-not-required
[EX-VL-003]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-vl-003--a-required-check-remains-required-when-it-is-unavailable
[EX-VL-004]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-vl-004--failure-is-not-permission-to-lower-the-bar
[EX-VL-005]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-vl-005--validate-research-against-its-own-objective
[EX-VL-006]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-vl-006--a-passing-smoke-check-does-not-establish-a-hard-limit
[EX-VL-007]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-vl-007--change-the-approach-without-changing-the-goal
[EX-VL-008]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-vl-008--keep-useful-learning-without-creating-paperwork-for-its-own-sake
[EX-VL-009]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-vl-009--retain-an-approach-that-the-evidence-supports
[EX-KD-001]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-001--record-a-lasting-finding-where-it-belongs
[EX-KD-002]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-002--record-a-proposal-without-accepting-it
[EX-KD-003]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-003--optional-debt-recording-does-not-authorize-a-fix
[EX-KD-004]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-004--keep-review-only-edits-inside-the-narrow-permission
[EX-KD-005]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-005--report-an-unmet-record-duty-when-edits-are-prohibited
[EX-KD-006]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-006--preserve-decision-history-when-an-authorized-choice-changes
[EX-KD-007]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-007--update-recorded-debt-when-authorized-work-resolves-it
[EX-KD-008]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-008--separate-lasting-behavior-from-task-only-checks
[EX-KD-009]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-009--update-known-direct-dependents-without-widening-the-audit
[EX-KD-010]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-010--report-gaps-outside-the-authorized-work
[EX-KD-011]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-kd-011--a-documentation-gap-does-not-require-a-new-guide
[EX-EQ-001]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-eq-001--refactor-without-changing-observable-behavior
[EX-EQ-002]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-eq-002--change-behavior-only-as-intended-and-authorized
[EX-EQ-003]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-eq-003--do-not-build-for-a-hypothetical-need-alone
[EX-EQ-004]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-eq-004--current-requirements-can-justify-complexity
[EX-EQ-005]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-eq-005--no-textual-caller-is-not-proof-of-dead-code
[EX-SD-001]: ../../01-discovery/deliverables/proposed-examples/self-contained-delivery.md#ex-sd-001--check-the-delivered-file-against-the-full-duty-set
[EX-SD-002]: ../../01-discovery/deliverables/proposed-examples/self-contained-delivery.md#ex-sd-002--fail-when-a-companion-supplies-missing-policy
[EX-SD-003]: ../../01-discovery/deliverables/proposed-examples/self-contained-delivery.md#ex-sd-003--allow-loading-aids-and-adopting-project-facts
