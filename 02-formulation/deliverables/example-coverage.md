# Requirement-to-scenario coverage

Discovery owns the [proposed examples and their status](../../01-discovery/deliverables/example-coverage.md#reading-a-proposed-example). Formulation compares each mapped example with an [accepted requirement](baseline.md). Read across a requirement’s row to find its examples, or look up an EX identifier to find every requirement it illustrates.

- **Direct** (51 examples). The proposed outcome illustrates the primary requirement with its qualifications and can be described without prescribing how to achieve it.
- **Detail review** (9 examples). The proposed outcome depends on a particular procedure or interpretation. The note beside each link names that detail. Its inclusion in an example does not establish it as a requirement. This classification can apply even after the requester has answered the underlying question.

Each of the 60 examples appears once in those two columns. “Also exercised by” lists examples whose primary association is elsewhere. For instance, [EX-027] illustrates BR4 and also exercises BR3 and BR6. These relationships record what the proposals illustrate. Acceptance as a defining example takes a separate decision. Completeness, behavioral compliance and evaluation coverage each require separate evidence.

| Accepted requirement | Direct examples | Detail review examples | Also exercised by |
| --- | --- | --- | --- |
| [BR1](baseline.md#br1--focused-proportionate-authorized-work) | [EX-001], [EX-002], [EX-003], [EX-004], [EX-005], [EX-006] | — | [EX-014], [EX-022] |
| [BR2](baseline.md#br2--evidence-based-planning-and-knowledge-ownership) | [EX-007], [EX-008], [EX-009] | [EX-010] (which source owns a project fact and what an instruction file can establish) | [EX-039] |
| [BR3](baseline.md#br3--autonomy-within-authorization-and-prior-direction) | [EX-011], [EX-012], [EX-013], [EX-014], [EX-015], [EX-016], [EX-017], [EX-019] | [EX-018] (an informal expectation compared with an explicit limit) | [EX-004], [EX-027], [EX-023], [EX-045] |
| [BR4](baseline.md#br4--bounded-investigation-and-timely-reassessment) | [EX-025], [EX-026], [EX-027], [EX-029], [EX-032] | [EX-028] (routine reading and ordinary regression checks), [EX-030] (whether the purpose of a benchmark changes the need for notice), [EX-031] (reading existing project documents to resolve a blocker) | — |
| [BR5](baseline.md#br5--completion-supported-by-validation) | [EX-033], [EX-034], [EX-035], [EX-036], [EX-037], [EX-038] | — | [EX-005], [EX-053] |
| [BR6](baseline.md#br6--learning-from-observed-results) | [EX-039], [EX-040], [EX-041] | — | [EX-002], [EX-027], [EX-037], [EX-042] |
| [BR7](baseline.md#br7--proportionate-communication-and-actionable-handoffs) | [EX-020], [EX-021], [EX-022], [EX-023], [EX-024] | — | [EX-015], [EX-016], [EX-025], [EX-046] |
| [BR8](baseline.md#br8--durable-knowledge-without-expanded-editing-authority) | [EX-042], [EX-043], [EX-045], [EX-046], [EX-047] | [EX-044] (when recording a compromise as technical debt is optional), [EX-048] (maintaining an existing debt entry after resolution, even though creating it was optional) | [EX-040], [EX-051] |
| [BR9](baseline.md#br9--engineering-quality-and-preservation) | [EX-053], [EX-054], [EX-055], [EX-056] | [EX-057] (evidence for treating code as dead) | [EX-001], [EX-038] |
| [BR10](baseline.md#br10--affected-requirements-and-documentation) | [EX-049], [EX-050], [EX-051] | [EX-052] (how a coverage proposal, a requester deferral and an agreed need for a guide affect the response) | [EX-045], [EX-054] |
| [PR1](baseline.md#established-product-requirement) | [EX-058], [EX-059], [EX-060] | — | — |

The proposed examples illustrating accepted clarifications are [EX-003] and [EX-005] (coherence and recovery), [EX-016] (unauthorized consequential choice), [EX-022] and [EX-023] (limits, consumed allowances, and resumption), [EX-045] and [EX-046] (assessment-write boundaries), and [EX-051] (out-of-scope gaps). [EX-027] and [EX-032] distinguish justified continuation after an inconclusive step from repetition without supporting findings. Limits of two attempts in particular fixtures are requester-imposed examples, not a default investigation budget.

## Historical example IDs

Use this lookup for references written before Discovery assigned its own IDs. Each pair names the same example. The matrix above records its current requirement associations.

| Former ID | Discovery ID |
| --- | --- |
| BR1.1 | [EX-001] |
| BR1.2 | [EX-002] |
| BR1.3 | [EX-003] |
| BR1.4 | [EX-004] |
| BR1.5 | [EX-005] |
| BR1.6 | [EX-006] |
| BR2.1 | [EX-007] |
| BR2.2 | [EX-008] |
| BR2.3 | [EX-009] |
| BR2.4 | [EX-010] |
| BR3.1 | [EX-011] |
| BR3.2 | [EX-012] |
| BR3.3 | [EX-013] |
| BR3.4 | [EX-014] |
| BR3.5 | [EX-015] |
| BR3.6 | [EX-016] |
| BR3.7 | [EX-017] |
| BR3.8 | [EX-018] |
| BR3.9 | [EX-019] |
| BR7.1 | [EX-020] |
| BR7.2 | [EX-021] |
| BR7.3 | [EX-022] |
| BR7.4 | [EX-023] |
| BR7.5 | [EX-024] |
| BR4.1 | [EX-025] |
| BR4.2 | [EX-026] |
| BR4.3 | [EX-027] |
| BR4.4 | [EX-028] |
| BR4.5 | [EX-029] |
| BR4.6 | [EX-030] |
| BR4.7 | [EX-031] |
| BR4.8 | [EX-032] |
| BR5.1 | [EX-033] |
| BR5.2 | [EX-034] |
| BR5.3 | [EX-035] |
| BR5.4 | [EX-036] |
| BR5.5 | [EX-037] |
| BR5.6 | [EX-038] |
| BR6.1 | [EX-039] |
| BR6.2 | [EX-040] |
| BR6.3 | [EX-041] |
| BR8.1 | [EX-042] |
| BR8.2 | [EX-043] |
| BR8.3 | [EX-044] |
| BR8.4 | [EX-045] |
| BR8.5 | [EX-046] |
| BR8.6 | [EX-047] |
| BR8.7 | [EX-048] |
| BR10.1 | [EX-049] |
| BR10.2 | [EX-050] |
| BR10.3 | [EX-051] |
| BR10.4 | [EX-052] |
| BR9.1 | [EX-053] |
| BR9.2 | [EX-054] |
| BR9.3 | [EX-055] |
| BR9.4 | [EX-056] |
| BR9.5 | [EX-057] |
| PR1.1 | [EX-058] |
| PR1.2 | [EX-059] |
| PR1.3 | [EX-060] |

[EX-001]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-001--fix-the-defect-and-its-necessary-dependents
[EX-002]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-002--reassess-before-extending-the-work
[EX-003]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-003--explain-a-step-that-cannot-stand-alone-before-starting-it
[EX-004]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-004--stop-at-the-end-of-the-authorized-task
[EX-005]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-005--honor-a-required-stop-with-unfinished-work
[EX-006]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-006--match-planning-depth-to-the-next-decision
[EX-007]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-007--inspect-what-matters-before-choosing-the-fix
[EX-008]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-008--a-passing-test-does-not-settle-what-the-product-should-do
[EX-009]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-009--ask-when-the-sources-cannot-settle-a-consequential-choice
[EX-010]: ../../01-discovery/deliverables/proposed-examples/planning-and-scope.md#ex-010--use-instruction-files-for-conduct-not-proof-of-project-facts
[EX-011]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-011--a-routine-local-choice-needs-no-new-requester-decision
[EX-012]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-012--do-not-infer-permission-for-a-consequential-change
[EX-013]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-013--use-specific-direction-already-given
[EX-014]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-014--do-not-pass-a-checkpoint-or-enlarge-a-limit-on-your-own
[EX-015]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-015--disclose-a-material-assumption-at-the-applicable-reporting-occasion
[EX-016]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-016--disclose-a-consequential-choice-made-without-prior-direction
[EX-017]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-017--normally-ask-about-other-unsettled-material-choices
[EX-018]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-018--distinguish-an-expectation-from-a-binding-limit
[EX-019]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-019--local-work-and-tool-capability-do-not-authorize-an-external-action
[EX-020]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-020--frame-substantial-work-without-creating-an-approval-gate
[EX-021]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-021--report-results-and-disclose-blockers-in-time
[EX-022]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-022--transfer-remaining-work-and-used-allowances
[EX-023]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-023--recover-missing-authority-before-dependent-work
[EX-024]: ../../01-discovery/deliverables/proposed-examples/authorization-and-communication.md#ex-024--useful-updates-are-permitted-without-a-report-per-increment
[EX-025]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-025--tell-the-requester-what-is-blocking-progress
[EX-026]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-026--stop-when-there-is-enough-evidence
[EX-027]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-027--review-an-inconclusive-step-before-doing-more
[EX-028]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-028--ordinary-checking-does-not-require-an-inquiry-notice
[EX-029]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-029--a-notice-already-given-need-not-be-repeated
[EX-030]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-030--a-prescribed-procedure-can-still-be-inquiry
[EX-031]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-031--reading-existing-project-documents-remains-context-gathering
[EX-032]: ../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#ex-032--an-unanswered-question-is-not-evidence-for-another-attempt
[EX-033]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-033--run-relevant-checks-that-are-available
[EX-034]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-034--substitute-evidence-only-when-the-missing-check-was-not-required
[EX-035]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-035--a-required-check-remains-required-when-it-is-unavailable
[EX-036]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-036--failure-is-not-permission-to-lower-the-bar
[EX-037]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-037--validate-research-against-its-own-objective
[EX-038]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-038--a-passing-smoke-check-does-not-establish-a-hard-limit
[EX-039]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-039--change-the-approach-without-changing-the-goal
[EX-040]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-040--keep-useful-learning-without-creating-paperwork-for-its-own-sake
[EX-041]: ../../01-discovery/deliverables/proposed-examples/validation-and-learning.md#ex-041--retain-an-approach-that-the-evidence-supports
[EX-042]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-042--record-a-lasting-finding-where-it-belongs
[EX-043]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-043--record-a-proposal-without-accepting-it
[EX-044]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-044--optional-debt-recording-does-not-authorize-a-fix
[EX-045]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-045--keep-review-only-edits-inside-the-narrow-permission
[EX-046]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-046--report-an-unmet-record-duty-when-edits-are-prohibited
[EX-047]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-047--preserve-decision-history-when-an-authorized-choice-changes
[EX-048]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-048--update-recorded-debt-when-authorized-work-resolves-it
[EX-049]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-049--separate-lasting-behavior-from-task-only-checks
[EX-050]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-050--update-known-direct-dependents-without-widening-the-audit
[EX-051]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-051--report-gaps-outside-the-authorized-work
[EX-052]: ../../01-discovery/deliverables/proposed-examples/knowledge-and-documentation.md#ex-052--a-documentation-gap-does-not-require-a-new-guide
[EX-053]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-053--refactor-without-changing-observable-behavior
[EX-054]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-054--change-behavior-only-as-intended-and-authorized
[EX-055]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-055--do-not-build-for-a-hypothetical-need-alone
[EX-056]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-056--current-requirements-can-justify-complexity
[EX-057]: ../../01-discovery/deliverables/proposed-examples/engineering-quality.md#ex-057--no-textual-caller-is-not-proof-of-dead-code
[EX-058]: ../../01-discovery/deliverables/proposed-examples/self-contained-delivery.md#ex-058--check-the-delivered-file-against-the-full-duty-set
[EX-059]: ../../01-discovery/deliverables/proposed-examples/self-contained-delivery.md#ex-059--fail-when-a-companion-supplies-missing-policy
[EX-060]: ../../01-discovery/deliverables/proposed-examples/self-contained-delivery.md#ex-060--allow-loading-aids-and-adopting-project-facts
