# Cross-stage traceability and evidence

## Reading a reference

Read a cross-stage reference according to the question it answers. A link can serve more than one purpose.

| Relationship | Question it answers | Example |
| --- | --- | --- |
| Authority dependency | Which source governs this decision, and within what scope? | An accepted requirement constrains mechanism selection. Its conditions and exceptions apply to the design choice. |
| Traceability relationship | Which items are connected, and what does the connection establish? | A clause-index entry connects a contract clause to its mechanism and supported intent. The link records that correspondence without granting product acceptance to the mechanism. |
| Navigation reference | Where should the reader go next? | A stage README points to a case or a specification. A moved destination calls for a link correction. |

## Tracing a requirement and its evaluation

Trace a claim in two steps. First identify the versioned source that justifies the criterion and the conditions the definition can distinguish. Then identify the Candidate, what was actually observed, and the criterion and assessment used for that run. The first trace describes prospective coverage. The second supports a conclusion only for the conditions exercised. A requester decision can establish a requirement before either trace exists.

| Relationship | What to retain |
| --- | --- |
| Objective or constraint → proposal → accepted behavior | Discovery keeps sources, uncertainty, and decision links. The Formulation baseline ([`02.0-formulation/deliverables/baseline.md`](../02.0-formulation/deliverables/baseline.md)) keeps accepted wording, conditions, exceptions, any expressly accepted defining examples, and a link to [`02.0-formulation/docs/acceptance-record.md`](../02.0-formulation/docs/acceptance-record.md). Preserve provisional IDs and unresolved aspects. Link replacements without erasing earlier status. |
| Accepted intent → design → contract | Shared engineering links accepted intent and its Design mechanism to implementation through the clause index ([`docs/contract-traces.md` § Contract clause index](contract-traces.md#contract-clause-index)). Inherited design without independently accepted intent retains its design authority and trace gap. PR1 permits direct artifact inspection without inventing an intermediary mechanism. Trace metadata stays outside consumer text. |
| Accepted requirement → Acceptance definition | Identify the Formulation rule and version, conditions, constraints and any expressly accepted defining example. Acceptance owns the criterion, method, coverage and limitations independently of the chosen mechanism. |
| Design prescription → Conformance definition | Identify the mechanism and version, applicable requirements and Acceptance coverage considered. Keep a versioned link to the Acceptance criterion for any check omitted as redundant. A change to its coverage reopens that decision even if every prior run passed. |
| Legacy clause → provisional definition | For the existing cases, retain the actual source clause and version, case, technical assertions and rubric. Trace a fixture's application rules separately. A clause-to-mechanism correspondence does not establish independent derivation of the case from Design. |
| Candidate and expectation → observation → review | Run bundles identify candidate bytes/digest, case, settings, observations, assertions, and applicable rubric. Requirements-led claims also identify the accepted requirement/expectation and evaluator versions in a review reference or run-associated record. Retain failed, pending, inconclusive, and unexercised distinctions. |
| Finding → responsible owner | Evaluation records the finding, uncertainty and evidence. Route a fixture or criterion defect to its definition owner, a capture fault to the engine, and an execution-policy or assessment issue to Evaluation. Take implementation discrepancies to Candidate or Design, and unsettled intent or consequential trade-offs to Discovery and the decision owner. Keep insufficient evidence explicit. |

The Formulation matrix ([`02.0-formulation/deliverables/example-coverage.md`](../02.0-formulation/deliverables/example-coverage.md)) maps accepted rules to Discovery EX identifiers, including interactions and coverage classifications. Use its historical ID lookup ([`02.0-formulation/deliverables/example-coverage.md` § Historical example IDs](../02.0-formulation/deliverables/example-coverage.md#historical-example-ids)) for an older reference. The example source references ([`docs/contract-traces.md` § Sources for the proposed examples](contract-traces.md#sources-for-the-proposed-examples)) identify the mechanisms and contract passages used in drafting the proposals.

Store a relationship at its dependent or shared index. Use exact IDs, targets, and applicable versions. To find direct dependents, look up the changed ID, heading, or path in the clause index and affected owners. Inspect what each dependent relies on before following the next link. A fixture change raises observation and comparability questions. A changed expected verdict under unchanged accepted conditions raises an interpretation or authority question. Shared terminology alone proves no trace link.

The owner-reported acceptance account ([`02.0-formulation/docs/acceptance-record.md`](../02.0-formulation/docs/acceptance-record.md)) establishes the scope of BR acceptance. The editors also used design accounts and contract wording to recover qualifications and exceptions. The selected and superseded decisions ([`03.0-design/docs/decisions.md` § Selected design and retained decisions](../03.0-design/docs/decisions.md#selected-design-and-retained-decisions)), the 28 Design illustrations ([`03.0-design/docs/design-illustrations.md`](../03.0-design/docs/design-illustrations.md)) and clause-based evaluation cases each retain their own status.

### Current traceability gaps

No existing proposed example has been accepted as defining. Explicit requirement-to-evaluation traceability remains incomplete. Existing behavioral cases exercise contract clauses and support regression or design-conformance review. The clause index connects accepted outcomes to current mechanisms. Neither those links nor passing cases establish complete realization or requirements-derived acceptance. Discovery ([`01-discovery/deliverables/open-questions.md`](../01-discovery/deliverables/open-questions.md)) records questions and requester conclusions awaiting requirements review. [`05-evaluation/docs/evaluation-model.md` § Purpose and evaluation model](../05-evaluation/docs/evaluation-model.md#purpose-and-evaluation-model) identifies suite coverage and limits.

## What evidence can establish

| Evidence | What it establishes |
| --- | --- |
| Contract-text review | Whether the text expresses intended obligations, permissions, conditions, exceptions, and constraints. PR1 primarily uses standalone artifact inspection. |
| Behavioral evaluation | What agents receiving the identified contract did in the cases run, assessed against assertions and human rubrics. |
| Evaluator tests | Specified machinery behavior for execution, observation, grading, reporting, and failures within the checks run. Agent compliance and the semantic validity of expectations require separate evidence. |

Limit claims to the tools, environments, and behavior actually exercised. [`05-evaluation/docs/evaluation-model.md` § Purpose and evaluation model](../05-evaluation/docs/evaluation-model.md#purpose-and-evaluation-model) explains the suite's coverage, variability between runs, human-review limits, and the evidence needed for causal attribution. Missing evidence remains unverified. Claims about O1/O2 benefits require suitable comparative evidence, representative tasks, and requester feedback where relevant. Textual alignment or evaluator success alone cannot establish them. Human review distinguishes evaluator faults, unsuitable expectations or scenarios, contract defects, agent behavior, and unresolved intent before proposing a change.

## Specification-to-evaluation dependencies

For a changed Formulation rule, review Acceptance definitions, Design decisions and their dependents. For a changed Design prescription, review Conformance and Candidate. Acceptance expectations normally remain applicable if the requirement and its conditions still hold. Review a changed Acceptance definition for its effect on Conformance coverage or an omission.

A run exercises the staged contract even when its expectations have not been reviewed. A clause edit can invalidate a case’s expectations while its assertions still pass. A moved or renumbered clause can break a rubric or case reference. Design specifications, design-review guidance, and consumer guides also refer to contract headings.

| What changed? | Impact on dependents |
| --- | --- |
| An exercised rule’s strength, trigger, condition, exception, or scope | Compare the affected scenario, fixture, assertions, and rubric against the authority for the expectation. A contract edit alone cannot authorize a new expected result. |
| Only a clause’s number, heading, or location | Correct affected references in rubrics, cases, and linking documents while preserving their meaning. |
| Behavior no case exercises | No case edit is needed without a demonstrated impact. Adding coverage is a separate decision. |

A case or rubric edit changes the assessment. Earlier runs retain their captured candidate and criteria. Revised criteria neither rewrite those conclusions nor transfer them to a revised contract. E1–E40 ([`05-evaluation/README.md` § Evaluator requirements](../05-evaluation/README.md#evaluator-requirements)) govern evaluator behavior. They change only through authorized requirement work when the evaluator’s required behavior changes. Evaluation documents how to integrate and verify a change with the responsible definition or engine owner ([`05-evaluation/docs/maintaining-evaluations.md`](../05-evaluation/docs/maintaining-evaluations.md)).
