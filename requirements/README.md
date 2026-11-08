# AGENTS-spec product requirements

`requirements/` is the future canonical home of the product requirements for coding-agent collaboration. This entry point explains the requirements domain, links to its current authoritative sources, and identifies the remaining migration work.

**Current authority remains in [_internal/docs/contract-design.md](../_internal/docs/contract-design.md).** No detailed requirements ownership has transferred to `requirements/`. This README provides orientation and navigation; it establishes no competing requirement definitions and changes no acceptance or decision status.

## Responsibility and boundaries

The requirements project defines the collaboration outcomes wanted and why, the applicable product constraints, and which objectives and requirements are established versus provisional candidates awaiting developer acceptance. It remains independent of the current contract implementation and evaluation machinery.

The contract project determines how instructions express those outcomes. An existing contract clause establishes what the current contract prescribes; it does not by itself establish an accepted product requirement. PDSA, EARS, the three-layer contract organization, and other selected methods do not become enduring requirements merely through their use in the current design. Their present contractual force and any future authorized revision remain distinct from product-requirement acceptance.

The evaluation project's responsibility is to derive behavioral evaluations from product requirements and own the evaluation machinery and its evaluator requirements E1–E40. The current framework assesses the staged contract; explicit product-requirement traceability remains later work. Evaluation results supply evidence for review without accepting requirements or authorizing changes to them.

Development agents are governed by applicable development instructions and developer direction, not the staged candidate contract. See [development-time and runtime authority](../_internal/docs/architecture.md#development-time-and-runtime-authority) for the authority and instruction-loading boundaries.

## Current authoritative sources

Read the source sections for their definitions, qualifications, and evidence. The links below distinguish knowledge that must retain its own status during any later transfer.

| Knowledge and status | Authoritative source |
| --- | --- |
| Classification and evidence: how established intent, provisional candidates, current prescriptions, rationale, and history are distinguished | [Classification and evidence](../_internal/docs/contract-design.md#classification-and-evidence) |
| Established objectives O1 (control token consumption, first) and O2 (requester awareness and consequential control, second), and knowledge continuity | [Established objectives](../_internal/docs/contract-design.md#established-objectives) |
| Established product requirement PR1: self-contained operating contract | [Established product requirement](../_internal/docs/contract-design.md#established-product-requirement) |
| Established product constraints, with their retained strength, scope, exceptions, and revision conditions | [Established constraints](../_internal/docs/contract-design.md#established-constraints) |
| Provisional requirement candidates RC1–RC10 awaiting developer acceptance; their existing explanations do not establish acceptance | [Requirement candidates](../_internal/docs/contract-design.md#requirement-candidates) |
| Current contract mechanisms and design prescriptions, with distinguishable rationale; current binding status does not establish enduring product-requirement status | [Design choices](../_internal/docs/contract-design.md#design-choices) and [current-semantics vocabulary and coverage](../_internal/docs/contract-design.md#current-semantics-vocabulary-and-coverage) |
| Historical rationale, retained decisions, and rejected or superseded alternatives, with their source context and status | [Decision status and historical alternatives](../_internal/docs/contract-design.md#decision-status-and-historical-alternatives) |
| Evaluator requirements E1–E40: requirements for the evaluation machinery, owned by `evaluations/` | [Verifiable requirements](../evaluations/docs/evaluations.md#verifiable-requirements) |

## Remaining migration work

Detailed requirements will transfer to `requirements/` only through separately reviewed changes. Those changes must preserve provenance and decision status, including each established constraint's qualifications and links to the retained rationale, decisions, and significant historical alternatives. They must keep desired outcomes distinct from current implementation mechanisms and preserve provisional candidates as provisional unless separately accepted.

Until such transfers are reviewed and made, `contract-design.md` remains the authoritative source for all existing product requirements and candidates. Candidate acceptance, requirements extraction, contract redesign, and requirement-to-evaluation traceability remain separate future work; this entry point performs none of them.

For repository navigation, use the [engineering entry point](../_internal/README.md). [Architecture](../_internal/docs/architecture.md) owns cross-domain relationships; [documentation maintenance](../_internal/docs/documentation-maintenance.md#document-ownership) owns the documentation ownership map and editing guidance.
