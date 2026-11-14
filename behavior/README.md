# AGENTS-spec behavior and product requirements

`behavior/` is the product-requirements home for coding-agent collaboration. This entry point explains the behavior domain, links to its current authoritative sources, and identifies the remaining requirements work.

**[baseline.md](baseline.md) owns the established objectives, accepted BR1–BR10, PR1, and product constraints; [discovery.md](discovery.md) owns proposed acceptance examples, their coverage matrix, remaining formulation questions, and the historical RC inventory with its disposition.** [design/contract-design.md](../design/contract-design.md) owns the reusable operating contract's engineering scope boundaries, provider integration and instruction loading, design goals and boundaries, layer interaction, continuation behavior, shared current-semantics vocabulary and contract-clause coverage index, and [selected contract-design decisions and historical alternatives](../design/contract-design.md#architecture-decisions), with [method-reference semantics and source assignments](../design/contract-design.md#principles-and-reference-boundaries) under Crosscutting Concepts; a companion [Design Reference](../design/design-review.md#design-reference) owns non-normative [assessment scenarios](../design/design-review.md#assessing-design-changes) under Design Reference. The [Global status and evidence boundaries](../docs/architecture.md#status-and-evidence-boundaries) section owns the shared authority classification. This README provides orientation and navigation; it establishes no competing requirement definitions and changes no acceptance or decision status.

## Starting a BDD topic

Begin with the [global BDD activities and authority boundaries](../docs/architecture.md#bdd-activities-and-complementary-responsibilities), then use the owner of the question:

| Starting point | Reading and feedback path |
| --- | --- |
| An existing objective, requirement, or constraint | Read [established intent](baseline.md), then the [proposed examples and coverage](discovery.md#requirement-to-scenario-coverage). BR1–BR10 are accepted; their proposed examples still need independent acceptance as defining examples. |
| An open behavioral question or counterexample | Start with [formulation questions](discovery.md#formulation-questions-and-evidence-limits) and their evidence; involve requester, implementation, and evaluation perspectives. The [baseline](baseline.md) owns accepted wording and any expressly defining examples; none of the Phase 2 examples has that status yet. |
| A design question | Consult [current mechanisms and decisions](../design/contract-design.md) and [non-normative review illustrations](../design/design-review.md). Unresolved desired behavior returns to Discovery; selected design does not itself accept a requirement. |
| An evaluation finding | Start with the [case, captured candidate, and evidence limits](../evaluations/docs/evaluations.md#results-evidence-and-failure-investigation), then use the [feedback routes](../docs/architecture.md#cross-domain-traceability-and-feedback). An observation can reopen a question; it grants no approval. |

Discovery, Formulation, and Automation iterate across these owners. This navigation creates no accepted rules, defining examples, or acceptance tests. [Phase 2 provenance](baseline.md#phase-2-acceptance-and-editorial-provenance) records the owner's behavioral acceptance; examples and automation retain the separate status described below.

## Responsibility and boundaries

The behavior domain defines the collaboration outcomes wanted and why, the applicable product constraints, and which objectives and requirements are accepted versus proposed details awaiting owner review. It remains independent of the current contract implementation and evaluation machinery.

The staged candidate contract expresses those outcomes as instructions. An existing contract clause establishes what the current contract prescribes; it does not by itself establish an accepted product requirement. PDSA, EARS, the three-layer contract organization, and other selected methods do not become enduring requirements merely through their use in the current design. Their present contractual force and any future authorized revision remain distinct from product-requirement acceptance.

The evaluation project's responsibility is to derive behavioral evaluations from product requirements and own the evaluation machinery and its evaluator requirements E1–E40. The current framework assesses the staged contract; explicit product-requirement traceability remains later work. Evaluation results supply evidence for review without accepting requirements or authorizing changes to them.

Development agents are governed by applicable development instructions and developer direction, not the staged candidate contract. See [development-time and runtime authority](../docs/architecture.md#development-time-and-runtime-authority) for the authority and instruction-loading boundaries.

## Current authoritative sources

Read the source sections for their definitions, qualifications, and evidence. The links below distinguish knowledge that must retain its own status during later work.

| Knowledge and status | Authoritative source |
| --- | --- |
| Classification and evidence: how established intent, provisional candidates, current prescriptions, rationale, and history are distinguished | [Status and evidence boundaries](../docs/architecture.md#status-and-evidence-boundaries) |
| Established-item provenance and acceptance boundaries | [Status and provenance](baseline.md#status-and-provenance) |
| Established objectives O1 (control token consumption, first) and O2 (requester awareness and consequential control, second), and knowledge continuity | [Established objectives](baseline.md#established-objectives) |
| Accepted behavioral requirements BR1–BR10, including the five clarifications and BR4 reassessment wording | [Accepted behavioral requirements](baseline.md#accepted-behavioral-requirements) |
| Proposed Given/When/Then examples, direct versus detail-review basis, requirement coverage, and corrections to the supplied draft | [Coverage matrix](discovery.md#requirement-to-scenario-coverage), [proposed scenarios](discovery.md#proposed-acceptance-scenarios), and [draft changes](discovery.md#changes-from-the-supplied-draft) |
| Established product requirement PR1: self-contained operating contract | [Established product requirement](baseline.md#established-product-requirement) |
| Established product constraints, with their retained strength, scope, exceptions, and revision conditions | [Established constraints](baseline.md#established-constraints) |
| Historical RC1–RC10 inventory and its mapping to accepted outcomes; residual design detail is not automatically accepted | [Candidate disposition](discovery.md#disposition-of-the-earlier-candidates) and [historical inventory](discovery.md#requirement-candidates) |
| Contract architecture: provider integration and instruction loading, selected design goals and boundaries, three-layer interaction and continuation, reusable crosscutting rules, and worked task example, with rationale and evidence limits | [Context and Scope](../design/contract-design.md#context-and-scope), [Solution Strategy](../design/contract-design.md#solution-strategy), [Crosscutting Concepts](../design/contract-design.md#crosscutting-concepts), and [Runtime View](../design/contract-design.md#runtime-view) |
| Current contract mechanisms and design prescriptions, with distinguishable rationale; current binding status does not establish enduring product-requirement status | [Current-semantics vocabulary and coverage](../design/contract-design.md#current-semantics-vocabulary-and-coverage) and its indexed topic sections |
| Method-selection and portability rationale and current wording trade-offs, under the established constraints | [Choosing or replacing methods](../design/contract-design.md#choosing-or-replacing-methods), [Keeping the contract portable](../design/contract-design.md#keeping-the-contract-portable), and [Current wording trade-offs](../design/contract-design.md#current-wording-trade-offs) |
| Historical rationale, retained decisions, and rejected or superseded alternatives, with their source context and status | [Architecture Decisions](../design/contract-design.md#architecture-decisions) |
| Current method-reference semantics, source assignments, and consultation boundaries; no additional operating obligations | [Principles and reference boundaries](../design/contract-design.md#principles-and-reference-boundaries) under Crosscutting Concepts |
| Non-normative textual design-review scenarios, pending later requirements-led review; no accepted product intent or evaluation expectations | [Assessing design changes](../design/design-review.md#assessing-design-changes) under Design Reference |
| Evaluator requirements E1–E40: requirements for the evaluation machinery, owned by `evaluations/` | [Verifiable requirements](../evaluations/docs/evaluations.md#verifiable-requirements) |

## Remaining requirements work

BR1–BR10 and the accepted clarifications are formalized in the baseline; PR1, objectives, and constraints retain their established status. The owner supplied an acceptance summary rather than the original wording, so [editorial provenance](baseline.md#phase-2-acceptance-and-editorial-provenance) and [remaining example detail](discovery.md#formulation-questions-and-evidence-limits) stay explicit. No BR11 is introduced.

All 60 Phase 2 scenarios are proposed, including 48 direct demonstrations and 12 whose detailed design expectations need review before becoming defining examples. Owner review of these formulations and examples, requirements-derived automation, and any separately authorized contract redesign remain future work. The 28 non-normative design illustrations remain unchanged; existing rubrics and captured evaluations are not retroactively accepted as product criteria. No exhaustive behavioral or evaluation coverage is claimed.

## Working with requirements and design documentation

For contract work, read the [development authority model](../docs/architecture.md#development-time-and-runtime-authority), the accepted requirements and proposed examples linked above, then the global [status boundaries](../docs/architecture.md#status-and-evidence-boundaries) and [current-semantics index](../design/contract-design.md#current-semantics-vocabulary-and-coverage). This entry point explains desired-outcome responsibility and remaining work; definitions stay in their owners. Maintain established items with their original qualifications, status, and provenance, and retain historical candidate evidence and remaining formulation questions without promoting selected mechanisms to enduring requirements.

Separate editorial clarification from changed operating behavior and update the authoritative owner first. For current-operation explanations, identify the relevant contract clauses and rationale. Future authorized behavior changes follow established requirements and constraints, accepted decisions, and requester authority; reflect them consistently in the runtime contract and affected canonical documentation, including evaluations where affected. A README or implementation edit alone cannot establish intent or authorize revised expectations. The [design clause index](../design/contract-design.md#current-semantics-vocabulary-and-coverage) links current mechanisms to accepted outcomes; it does not prove complete realization. Defining-example acceptance and requirement-to-evaluation traceability remain later work.

Follow affected summaries, examples, references, and bridge explanations within the [known direct-dependency boundary](../docs/architecture.md#documentation-ownership-boundaries). Walk through the reader's task and review the complete result using the design reference's [explanation checks](../design/design-review.md#reviewing-contract-explanations) and relevant non-normative [design scenarios](../design/design-review.md#assessing-design-changes). These are textual checks, not accepted product intent, evaluation expectations, or behavioral evidence. Contract edits also require the existing [portability qualifications](baseline.md#portability-and-standing-context-qualifications).

For a substantial rewrite, keep a temporary old-to-new content map with reasons for removals; consolidation must preserve unique explanations. Keep current descriptions, useful lasting rationale, significant historical reasoning, accepted decisions, and influential rejected or superseded alternatives in their canonical owners, with status and replacement links. Historical PDSA material can explain earlier intent without overriding current decisions or implementation. Transient revision narratives, draft measurements, package fingerprints, temporary maps, and validation records belong in working or delivery records.

The [engineering-system architecture](../docs/architecture.md) owns cross-domain relationships, development authority, and documentation ownership boundaries. The [evaluation guide](../evaluations/docs/evaluations.md) owns evaluation operations and maintenance. These owners and the behavior and design documentation support the [BDD activities and interfaces](../docs/architecture.md#bdd-activities-and-complementary-responsibilities) without adding a stage.
