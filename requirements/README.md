# AGENTS-spec product requirements

`requirements/` is the product-requirements home for coding-agent collaboration. This entry point explains the requirements domain, links to its current authoritative sources, and identifies the remaining migration work.

**[docs/product-requirements.md](docs/product-requirements.md) owns the established objectives, PR1, and product constraints; [docs/requirement-candidates.md](docs/requirement-candidates.md) owns provisional RC1–RC10 and their unresolved acceptance questions.** [contract/docs/prerelease_contract-design.md](../contract/docs/prerelease_contract-design.md) retains classification and evidence and all design-specific knowledge. This README provides orientation and navigation; it establishes no competing requirement definitions and changes no acceptance or decision status.

## Responsibility and boundaries

The requirements project defines the collaboration outcomes wanted and why, the applicable product constraints, and which objectives and requirements are established versus provisional candidates awaiting developer acceptance. It remains independent of the current contract implementation and evaluation machinery.

The contract project determines how instructions express those outcomes. An existing contract clause establishes what the current contract prescribes; it does not by itself establish an accepted product requirement. PDSA, EARS, the three-layer contract organization, and other selected methods do not become enduring requirements merely through their use in the current design. Their present contractual force and any future authorized revision remain distinct from product-requirement acceptance.

The evaluation project's responsibility is to derive behavioral evaluations from product requirements and own the evaluation machinery and its evaluator requirements E1–E40. The current framework assesses the staged contract; explicit product-requirement traceability remains later work. Evaluation results supply evidence for review without accepting requirements or authorizing changes to them.

Development agents are governed by applicable development instructions and developer direction, not the staged candidate contract. See [development-time and runtime authority](../docs/architecture.md#development-time-and-runtime-authority) for the authority and instruction-loading boundaries.

## Current authoritative sources

Read the source sections for their definitions, qualifications, and evidence. The links below distinguish knowledge that must retain its own status during any later transfer.

| Knowledge and status | Authoritative source |
| --- | --- |
| Classification and evidence: how established intent, provisional candidates, current prescriptions, rationale, and history are distinguished | [Classification and evidence](../contract/docs/prerelease_contract-design.md#classification-and-evidence) |
| Established-item provenance and acceptance boundaries | [Status and provenance](docs/product-requirements.md#status-and-provenance) |
| Established objectives O1 (control token consumption, first) and O2 (requester awareness and consequential control, second), and knowledge continuity | [Established objectives](docs/product-requirements.md#established-objectives) |
| Established product requirement PR1: self-contained operating contract | [Established product requirement](docs/product-requirements.md#established-product-requirement) |
| Established product constraints, with their retained strength, scope, exceptions, and revision conditions | [Established constraints](docs/product-requirements.md#established-constraints) |
| Provisional requirement candidates RC1–RC10 awaiting developer acceptance; their existing explanations do not establish acceptance | [Requirement candidates](docs/requirement-candidates.md#requirement-candidates) |
| Current contract mechanisms and design prescriptions, with distinguishable rationale; current binding status does not establish enduring product-requirement status | [Design choices](../contract/docs/prerelease_contract-design.md#design-choices) and [current-semantics vocabulary and coverage](../contract/docs/prerelease_contract-design.md#current-semantics-vocabulary-and-coverage) |
| Historical rationale, retained decisions, and rejected or superseded alternatives, with their source context and status | [Decision status and historical alternatives](../contract/docs/prerelease_contract-design.md#decision-status-and-historical-alternatives) |
| Evaluator requirements E1–E40: requirements for the evaluation machinery, owned by `evaluations/` | [Verifiable requirements](../evaluations/docs/evaluations.md#verifiable-requirements) |

## Remaining migration work

The established objectives, PR1, and constraints and the provisional RC1–RC10 inventory have transferred with their provenance, qualifications, and links to retained design rationale, decisions, and significant historical alternatives. Further requirements extraction requires separately reviewed changes that preserve provenance and decision status, keep desired outcomes distinct from current implementation mechanisms, and preserve provisional candidates as provisional unless separately accepted.

The requirements baseline is not complete. Candidate acceptance, further requirements extraction, contract redesign, and requirement-to-evaluation traceability remain separate future work; this entry point performs none of them.

For repository navigation, use the [engineering entry point](../_internal/README.md). [Architecture](../docs/architecture.md) owns cross-domain relationships; [documentation maintenance](../_internal/docs/documentation-maintenance.md#document-ownership) owns the documentation ownership map and editing guidance.
