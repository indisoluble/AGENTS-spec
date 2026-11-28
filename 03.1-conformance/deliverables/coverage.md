# Provisional clause-based coverage

Conformance provisionally owns these nine behavioral definitions. Their expectations were drawn substantially from Candidate clauses. An accepted requirement or selected mechanism may independently justify a property today. Establishing that justification requires examining the particular criterion, its strength and the conditions it grades. A correspondence found today leaves the original derivation intact.

| Case | Assessment |
| --- | --- |
| [assumption-disclosure](cases/assumption-disclosure.md) | Automated checks and required human judgment |
| [bounded-inquiry](cases/bounded-inquiry.md) | Automated checks and required human judgment |
| [contract-change-followthrough](cases/contract-change-followthrough.md) | Automated checks and required human judgment |
| [durable-finding-review](cases/durable-finding-review.md) | Automated checks and required human judgment |
| [independent-execution](cases/independent-execution.md) | Automated checks and required human judgment |
| [missing-permission](cases/missing-permission.md) | Automated checks and required human judgment |
| [no-safe-next-step](cases/no-safe-next-step.md) | Automated checks and required human judgment |
| [requester-guidance](cases/requester-guidance.md) | Automated checks and required human judgment |
| [scope-discipline](cases/scope-discipline.md) | Automated |

Each case specification explains the assertions, evidence and interpretation limits and links to the module with the exact prompt, fixture, graders and any human rubric.

## Criteria awaiting a decision

| Case and criterion | Basis to examine |
| --- | --- |
| IE3 · [`03.1-conformance/deliverables/cases/independent-execution.md` § Human review and interpretation](cases/independent-execution.md#human-review-and-interpretation) | The rubric can fail this criterion for asking about a routine authorized detail. BR3 permits an easily reversible local choice and the selected decision guard uses MAY. Discovery records the open question about the strength of that expectation. [`02.0-formulation/deliverables/baseline.md` § BR3 — Autonomy within authorization and prior direction](../../02.0-formulation/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction) · [`03.0-design/deliverables/mechanisms/requester-decisions-and-reporting.md` § Authorization and requester decisions](../../03.0-design/deliverables/mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions) · [`01-discovery/deliverables/open-questions.md` § Routine local choices](../../01-discovery/deliverables/open-questions.md#routine-local-choices) |
| NS3 · [`03.1-conformance/deliverables/cases/no-safe-next-step.md` § Human review and interpretation](cases/no-safe-next-step.md#human-review-and-interpretation) | The scheduling fixture blocks activation while allowing investigation or a reversible draft. The rubric assesses the alternatives presented at that point. The scope of BR3's no-safe-step trigger remains open. [`01-discovery/deliverables/open-questions.md` § When no safe step is possible](../../01-discovery/deliverables/open-questions.md#when-no-safe-step-is-possible) |
| BI4 · [`03.1-conformance/deliverables/cases/bounded-inquiry.md` § Human review](cases/bounded-inquiry.md#human-review) | BR4 establishes the blocking-uncertainty trigger. The selected Design distinguishes investigation from validation by purpose, including when the procedure is prescribed. The prompt already communicates the primary uncertainty and its significance. Discovery records both the unresolved product question about the benchmark and the separate reading conclusion awaiting requirements review. [`02.0-formulation/deliverables/baseline.md` § BR4 — Bounded investigation and timely reassessment](../../02.0-formulation/deliverables/baseline.md#br4--bounded-investigation-and-timely-reassessment) · [`03.0-design/deliverables/mechanisms/bounded-inquiry.md` § When inquiry applies](../../03.0-design/deliverables/mechanisms/bounded-inquiry.md#when-inquiry-applies) · [`01-discovery/deliverables/open-questions.md` § Prescribed benchmarks](../../01-discovery/deliverables/open-questions.md#prescribed-benchmarks) · [`01-discovery/deliverables/open-questions.md` § Reading existing project documentation](../../01-discovery/deliverables/open-questions.md#reading-existing-project-documentation) |

## Remaining dependency exceptions

All nine specifications cite the Candidate. Some citations explain where an expectation came from. Where an assertion or rubric uses a clause to decide a verdict, the clause still supplies operative meaning. Renumbering can also invalidate rubric references in assumption-disclosure, bounded-inquiry and durable-finding-review. A passing offline test can miss a change in meaning, including one implicit in a grader.

The eight human rubrics embedded in the scenario modules depend on Evaluation for the events, responses and workspace evidence they link to. Their text also embeds parts of Evaluation's review procedure. The independent-execution and contract-change-followthrough rubrics use retained functional-check evidence as well. These dependencies concern the contents and layout of a run bundle. At execution, setup and the durable-finding grader receive trusted contract bytes through the caller's reader. Neither needs to open the staged Candidate path.

E18 remains provisionally with the scope definition because its comparison exempts only the fixture's first-line greeting value. Its **Checks** line still names integrated verification, whose test routes are indexed by Evaluation. Review each outstanding reference according to its use. An exception can close when the responsible owner accepts its disposition and the remaining operative dependencies follow the stage direction. [`03.1-conformance/deliverables/cases/scope-discipline.md` § E18](cases/scope-discipline.md#e18)

## Establishing complementary coverage

Permanent ownership and independent Design derivation remain open across the nine cases. Review individual properties within a case. For example, the UTC fixture defines correct exporter output, the human rubric judges conduct, and the integrated evaluator reports the assertions and retains evidence. For a proposed product or mechanism criterion, identify the governing Formulation rule or authorized Design prescription and its version, then compare the criterion's trigger, permitted outcomes, observations and limits with that source. Record unsupported inferences or refer the distinction to its decision owner. A permanent allocation needs a reviewed trace and disposition.

Acceptance independently pursues feasible requirements coverage and currently has no definitions. Conformance has yet to establish which checks add mechanism-specific evidence. No omission for redundancy has been adjudicated. Any future omission belongs to Conformance and needs the applicable Acceptance criterion and version, the property it covers and the reason its verification suffices. [`02.1-acceptance/deliverables/coverage.md`](../../02.1-acceptance/deliverables/coverage.md) · [`03.1-conformance/README.md`](../README.md)
