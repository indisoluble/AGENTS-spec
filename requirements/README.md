# AGENTS-spec product requirements

`requirements/` is the product-requirements home for coding-agent collaboration. This entry point explains the requirements domain, links to its current authoritative sources, and identifies the remaining requirements work.

**[docs/product-requirements.md](docs/product-requirements.md) owns the established objectives, PR1, and product constraints; [docs/requirement-candidates.md](docs/requirement-candidates.md) owns provisional RC1–RC10 and their unresolved acceptance questions.** [docs/architecture.md](docs/architecture.md) owns the reusable operating contract's status and evidence boundaries, engineering scope boundaries, provider integration and instruction loading, design goals and boundaries, layer interaction, continuation behavior, shared current-semantics vocabulary and contract-clause coverage index, and [selected contract-design decisions and historical alternatives](docs/architecture.md#architecture-decisions), with [method-reference semantics and source assignments](docs/architecture.md#principles-and-reference-boundaries) under Crosscutting Concepts and non-normative [assessment scenarios](docs/architecture.md#assessing-design-changes) under Design Reference. This README provides orientation and navigation; it establishes no competing requirement definitions and changes no acceptance or decision status.

## Responsibility and boundaries

The requirements project defines the collaboration outcomes wanted and why, the applicable product constraints, and which objectives and requirements are established versus provisional candidates awaiting developer acceptance. It remains independent of the current contract implementation and evaluation machinery.

The staged candidate contract expresses those outcomes as instructions. An existing contract clause establishes what the current contract prescribes; it does not by itself establish an accepted product requirement. PDSA, EARS, the three-layer contract organization, and other selected methods do not become enduring requirements merely through their use in the current design. Their present contractual force and any future authorized revision remain distinct from product-requirement acceptance.

The evaluation project's responsibility is to derive behavioral evaluations from product requirements and own the evaluation machinery and its evaluator requirements E1–E40. The current framework assesses the staged contract; explicit product-requirement traceability remains later work. Evaluation results supply evidence for review without accepting requirements or authorizing changes to them.

Development agents are governed by applicable development instructions and developer direction, not the staged candidate contract. See [development-time and runtime authority](../docs/architecture.md#development-time-and-runtime-authority) for the authority and instruction-loading boundaries.

## Current authoritative sources

Read the source sections for their definitions, qualifications, and evidence. The links below distinguish knowledge that must retain its own status during later work.

| Knowledge and status | Authoritative source |
| --- | --- |
| Classification and evidence: how established intent, provisional candidates, current prescriptions, rationale, and history are distinguished | [Status and evidence boundaries](docs/architecture.md#status-and-evidence-boundaries) |
| Established-item provenance and acceptance boundaries | [Status and provenance](docs/product-requirements.md#status-and-provenance) |
| Established objectives O1 (control token consumption, first) and O2 (requester awareness and consequential control, second), and knowledge continuity | [Established objectives](docs/product-requirements.md#established-objectives) |
| Established product requirement PR1: self-contained operating contract | [Established product requirement](docs/product-requirements.md#established-product-requirement) |
| Established product constraints, with their retained strength, scope, exceptions, and revision conditions | [Established constraints](docs/product-requirements.md#established-constraints) |
| Provisional requirement candidates RC1–RC10 awaiting developer acceptance; their existing explanations do not establish acceptance | [Requirement candidates](docs/requirement-candidates.md#requirement-candidates) |
| Contract architecture: provider integration and instruction loading, selected design goals and boundaries, three-layer interaction and continuation, reusable crosscutting rules, and worked task example, with rationale and evidence limits | [Context and Scope](docs/architecture.md#context-and-scope), [Solution Strategy](docs/architecture.md#solution-strategy), [Crosscutting Concepts](docs/architecture.md#crosscutting-concepts), and [Runtime View](docs/architecture.md#runtime-view) |
| Current contract mechanisms and design prescriptions, with distinguishable rationale; current binding status does not establish enduring product-requirement status | [Current-semantics vocabulary and coverage](docs/architecture.md#current-semantics-vocabulary-and-coverage) and its indexed topic sections |
| Method-selection and portability rationale and current wording trade-offs, under the established constraints | [Choosing or replacing methods](docs/architecture.md#choosing-or-replacing-methods), [Keeping the contract portable](docs/architecture.md#keeping-the-contract-portable), and [Current wording trade-offs](docs/architecture.md#current-wording-trade-offs) |
| Historical rationale, retained decisions, and rejected or superseded alternatives, with their source context and status | [Architecture Decisions](docs/architecture.md#architecture-decisions) |
| Current method-reference semantics, source assignments, and consultation boundaries; no additional operating obligations | [Principles and reference boundaries](docs/architecture.md#principles-and-reference-boundaries) under Crosscutting Concepts |
| Non-normative textual design-review scenarios, pending later requirements-led review; no accepted product intent or evaluation expectations | [Assessing design changes](docs/architecture.md#assessing-design-changes) under Design Reference |
| Evaluator requirements E1–E40: requirements for the evaluation machinery, owned by `evaluations/` | [Verifiable requirements](../evaluations/docs/evaluations.md#verifiable-requirements) |

## Remaining requirements work

Further requirements extraction requires separately reviewed changes that preserve provenance and decision status, keep desired outcomes distinct from current implementation mechanisms, and preserve provisional candidates as provisional unless separately accepted. The 28 non-normative assessment scenarios remain pending later requirements-led review.

The requirements baseline is not complete. Candidate acceptance, further requirements extraction, contract redesign, and requirement-to-evaluation traceability remain separate future work; this entry point performs none of them.

## Working with requirements and design documentation

For contract work, read the [development authority model](../docs/architecture.md#development-time-and-runtime-authority), the established requirements and provisional candidates linked above, then the contract architecture's [status boundaries](docs/architecture.md#status-and-evidence-boundaries) and [current-semantics index](docs/architecture.md#current-semantics-vocabulary-and-coverage). This entry point explains desired-outcome responsibility and remaining work; definitions stay in their owners. Maintain established items with their original qualifications, status, and provenance, and retain candidate evidence and unresolved acceptance questions without promoting selected mechanisms to enduring requirements.

Separate editorial clarification from changed operating behavior and update the authoritative owner first. For current-operation explanations, identify the relevant contract clauses and rationale. Future authorized behavior changes follow established requirements and constraints, accepted decisions, and requester authority; reflect them consistently in the runtime contract and affected canonical documentation, including evaluations where affected. A README or implementation edit alone cannot establish intent or authorize revised expectations. Candidate acceptance and requirement-to-contract/evaluation traceability remain later work.

Follow affected summaries, examples, references, and bridge explanations within the [known direct-dependency boundary](../docs/architecture.md#documentation-ownership-boundaries). Walk through the reader's task and review the complete result using the contract architecture's [explanation checks](docs/architecture.md#reviewing-contract-explanations) and relevant non-normative [design scenarios](docs/architecture.md#assessing-design-changes). These are textual checks, not accepted product intent, evaluation expectations, or behavioral evidence. Contract edits also require the existing [portability qualifications](docs/product-requirements.md#portability-and-standing-context-qualifications).

For a substantial rewrite, keep a temporary old-to-new content map with reasons for removals; consolidation must preserve unique explanations. Keep current descriptions, useful lasting rationale, significant historical reasoning, accepted decisions, and influential rejected or superseded alternatives in their canonical owners, with status and replacement links. Historical PDSA material can explain earlier intent without overriding current decisions or implementation. Transient revision narratives, draft measurements, package fingerprints, temporary maps, and validation records belong in working or delivery records.

The [engineering-system architecture](../docs/architecture.md) owns cross-domain relationships, development authority, and documentation ownership boundaries. The [evaluation guide](../evaluations/docs/evaluations.md) owns evaluation operations and maintenance. These owners and the requirements-domain design documentation support the existing pipeline without adding a stage.
