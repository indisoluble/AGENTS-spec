# Product requirements and design of AGENTS.md

**Engineering-only document.** This file is a temporary consolidation document within the requirements project at `requirements/docs/contract-design.md` and remains excluded from the intended consumer release. It is not a runtime instruction file, provider bridge, or adoption guide, and creates no additional consumer operating duties.

This document is the authoritative design source for the reusable, opinionated [AGENTS.md](../../contract/prerelease_AGENTS.md) contract's remaining currently binding design prescriptions and their semantics, selected mechanisms, rationale, trade-offs, and subsequent engineering evolution. [Contract architecture](architecture.md) owns the transferred design overview, goals and boundaries, three-layer interaction and continuation, bounded-work design, PDSA learning design, completion and prediction distinctions, bounded-inquiry design, authorization and requester decisions, reporting and continued execution, Simple Design, DRY, component boundaries, refactoring, validation, focused techniques, arc42 documentation design, EARS requirements-writing design, ADR-writing design, technical-debt recording, Diátaxis documentation design, method-selection and portability rationale, current wording trade-offs, worked task example, shared current-semantics vocabulary and contract-clause coverage index, and [selected decisions and historical alternatives](architecture.md#architecture-decisions), as well as [method-reference semantics and source assignments](architecture.md#principles-and-reference-boundaries) under Crosscutting Concepts and the non-normative [assessment scenarios](architecture.md#assessing-design-changes) under Design Reference. [Product requirements](product-requirements.md) owns the established objectives, PR1, and product constraints; [requirement candidates](requirement-candidates.md) owns provisional RC1–RC10 and their unresolved acceptance questions. [Status and evidence boundaries](architecture.md#status-and-evidence-boundaries), [engineering scope boundaries](architecture.md#engineering-scope-boundaries), and [provider integration](architecture.md#context-and-scope) also belong to the contract architecture; this temporary document retains forwarding anchors and its other remaining material. Internal requirements and explanations add no runtime duties: `AGENTS.md` remains the independently self-contained normative runtime contract delivered to consuming agents.

For adoption, use [README.md](../../contract/prerelease_README.md); for practical guidance, use [Getting more from AGENTS.md](../../contract/prerelease_README-powerusers.md). For engineering-system relationships and authority, use [architecture.md](../../docs/architecture.md#development-time-and-runtime-authority); for editorial procedures and canonical ownership, use [documentation-maintenance.md](../../_internal/docs/documentation-maintenance.md#document-ownership). This reference explains product intent and design, rather than supplying a complete product-development process, branching strategy, workflow engine, or framework tutorial.

Read by question:

| Question | Start here |
| --- | --- |
| What is intended and established? | [Established product requirements](product-requirements.md), including their qualifications and provenance |
| What remains provisional, and how is evidence classified? | [Requirement candidates](requirement-candidates.md) and [status and evidence boundaries](architecture.md#status-and-evidence-boundaries) |
| What does the current contract prescribe? | [Current-semantics vocabulary and coverage](architecture.md#current-semantics-vocabulary-and-coverage), then the indexed topic sections here and in the [contract architecture](architecture.md); essential operating detail is specified in these engineering sources, without requiring a guide or contract link to fill gaps. |
| Why these mechanisms, and how do they interact? | [Contract architecture](architecture.md), including the [worked task](architecture.md#how-the-design-works-in-a-task), then the remaining [design choices](#design-choices) |
| Which decisions and older alternatives affect interpretation? | [Architecture Decisions](architecture.md#architecture-decisions) |
| How should the contract evolve? | [Evolving the contract](#evolving-the-contract) |
| What distinctions and sources matter in review? | [Design reference](#design-reference) |

## Product objectives, requirements, and constraints

### Classification and evidence

See the requirements-domain [contract architecture — Status and evidence boundaries](architecture.md#status-and-evidence-boundaries) for the canonical classification, six-status table, evidence limitations, and engineering/runtime authority distinctions.

### Established objectives

The canonical [established objectives](product-requirements.md#established-objectives) are O1 (control token consumption, first), O2 (requester awareness and consequential control, second), and supporting knowledge continuity. Their complete definitions, qualifications, and evidence limits now belong to `requirements/docs/product-requirements.md`; the design sections below explain the current mechanisms.

### Established product requirement

The canonical [PR1 — Self-contained operating contract](product-requirements.md#established-product-requirement), its complete EARS statement, and its distinctions between completeness, provider loading, adopting-project information, and behavioral evidence now belong to `requirements/docs/product-requirements.md`.

### Established constraints

The canonical [established constraints](product-requirements.md#established-constraints) now belong to `requirements/docs/product-requirements.md`: authority and capability boundaries, method selection, and portability and standing context, with their original strengths, qualifications, exceptions, and revision conditions. [Design boundaries](architecture.md#design-goals-and-boundaries), [method selection](architecture.md#choosing-or-replacing-methods), [portability](architecture.md#keeping-the-contract-portable), and [wording trade-offs](architecture.md#current-wording-trade-offs) retain the full engineering explanations and current design consequences; they are not independent definitions of the transferred constraints.

### Requirement candidates

The canonical [provisional RC1–RC10 inventory and unresolved acceptance questions](requirement-candidates.md#requirement-candidates) now belong to `requirements/docs/requirement-candidates.md`, with their [status and provenance](requirement-candidates.md#status-and-provenance). All entries remain provisional; their complete linked design explanations and current semantics remain in the [contract architecture](architecture.md) and this document, with historical alternatives retained in [Architecture Decisions](architecture.md#architecture-decisions).

## Design choices

**Status: current binding design, with rationale and historical context distinguished.** The sections here and in the [contract architecture](architecture.md) specify the present operating behavior and preserve its reasons, interactions, and qualifications. Statements about what an agent MUST, SHOULD, or MAY do explain `AGENTS.md` at its current strength; they are not an additional operating contract or acceptance of the provisional RC topics. The named methods and exact three-layer arrangement can be reconsidered only through future authorized change under the established objectives and constraints; they remain binding at their current strengths now.

### Current-semantics vocabulary and coverage

See the requirements-domain [contract architecture — Current-semantics vocabulary and coverage](architecture.md#current-semantics-vocabulary-and-coverage) for the canonical vocabulary and current contract-clause coverage index.

### Design overview

See the requirements-domain [contract architecture — Design overview](architecture.md#design-overview).

#### Design goals and boundaries

The canonical [design goals and boundaries](architecture.md#design-goals-and-boundaries) now belong to `requirements/docs/architecture.md`.

### Workflow design choices

See the requirements-domain [contract architecture — Workflow design choices](architecture.md#workflow-design-choices) for layer interaction and continuation within [Solution Strategy](architecture.md#solution-strategy), and [Crosscutting Concepts](architecture.md#crosscutting-concepts) for the reusable rules and mechanisms, including bounded-work design. The remaining detailed workflow mechanisms below stay here.

#### Three interacting layers

The canonical [three interacting layers](architecture.md#three-interacting-layers), their composition, four continuation outcomes, authorization qualifications, and evidence limits now belong to `requirements/docs/architecture.md`.

#### Small commitments with sufficient depth

See the requirements-domain [contract architecture — Small commitments with sufficient depth](architecture.md#small-commitments-with-sufficient-depth) for the canonical bounded-work design.

#### Learning throughout the work

See the requirements-domain [contract architecture — Learning throughout the work](architecture.md#learning-throughout-the-work) for the canonical PDSA learning design.

#### Completion, predictions, and bounded investigation

See the requirements-domain [contract architecture — Completion, predictions, and bounded investigation](architecture.md#completion-predictions-and-bounded-investigation) for the canonical design.

#### Authorization and requester decisions

See the requirements-domain [contract architecture — Authorization and requester decisions](architecture.md#authorization-and-requester-decisions) for the canonical design.

#### Reporting and continued execution

See the requirements-domain [contract architecture — Reporting and continued execution](architecture.md#reporting-and-continued-execution) for the canonical design.

### How the design works in a task

See the requirements-domain [contract architecture — How the design works in a task](architecture.md#how-the-design-works-in-a-task) for the canonical worked example.

### Engineering choices

See the requirements-domain [contract architecture — Engineering scope boundaries](architecture.md#engineering-scope-boundaries) and the engineering-practice sections linked below for the canonical current-design explanations.

#### Simple Design: choosing what the current solution needs

See the requirements-domain [contract architecture — Simple Design: choosing what the current solution needs](architecture.md#simple-design-choosing-what-the-current-solution-needs) for the canonical current-design explanation.

#### DRY: keeping knowledge consistent as work progresses

See the requirements-domain [contract architecture — DRY: keeping knowledge consistent as work progresses](architecture.md#dry-keeping-knowledge-consistent-as-work-progresses) for the canonical current-design explanation.

#### Component boundaries, refactoring, and validation

See the requirements-domain [contract architecture — Component boundaries, refactoring, and validation](architecture.md#component-boundaries-refactoring-and-validation) for the canonical current-design explanation.

#### Validation and test evidence

See the requirements-domain [contract architecture — Validation and test evidence](architecture.md#validation-and-test-evidence) for the canonical current-design explanation.

#### Focused techniques and how they work together

See the requirements-domain [contract architecture — Focused techniques and how they work together](architecture.md#focused-techniques-and-how-they-work-together) for the canonical current-design explanation.

### Documentation choices

See the requirements-domain [contract architecture — Documentation choices](architecture.md#documentation-choices) for the canonical documentation ownership and synchronization design.

#### arc42: shared architectural context as the project grows

See the requirements-domain [contract architecture — arc42: shared architectural context as the project grows](architecture.md#arc42-shared-architectural-context-as-the-project-grows) for the canonical current-design explanation.

#### EARS: making required behavior explicit

See the requirements-domain [contract architecture — EARS: making required behavior explicit](architecture.md#ears-making-required-behavior-explicit) for the canonical current-design explanation.

#### ADRs: preserving the reasons for lasting choices

See the requirements-domain [contract architecture — ADRs: preserving the reasons for lasting choices](architecture.md#adrs-preserving-the-reasons-for-lasting-choices) for the canonical current-design explanation.

#### Recording technical debt

See the requirements-domain [contract architecture — Recording technical debt](architecture.md#recording-technical-debt) for the canonical current-design explanation.

#### Diátaxis: choosing content for the reader's need

See the requirements-domain [contract architecture — Diátaxis: choosing content for the reader's need](architecture.md#diátaxis-choosing-content-for-the-readers-need) for the canonical current-design explanation.

### Why the bridges differ

See the requirements-domain [contract architecture — Why the bridges differ](architecture.md#why-the-bridges-differ) under [Context and Scope](architecture.md#context-and-scope) for the canonical provider-integration and instruction-loading boundaries, with their source provenance and recorded evidence-date limitations.

## Decision status and historical alternatives

See [Architecture Decisions](architecture.md#architecture-decisions) for the canonical decision-status index and historical alternatives.

### Selected design and retained decisions

See [Selected design and retained decisions](architecture.md#selected-design-and-retained-decisions) in the contract architecture.

### Historical source and interpretation

See [Historical source and interpretation](architecture.md#historical-source-and-interpretation) in the contract architecture.

### Superseded effort-baseline checkpoint

See [Superseded effort-baseline checkpoint](architecture.md#superseded-effort-baseline-checkpoint) in the contract architecture.

### Superseded inquiry announcement and stopping rule

See [Superseded inquiry announcement and stopping rule](architecture.md#superseded-inquiry-announcement-and-stopping-rule) in the contract architecture.

### Superseded report suppression and consultation strength

See [Superseded report suppression and consultation strength](architecture.md#superseded-report-suppression-and-consultation-strength) in the contract architecture.

### Superseded method-reference inquiry exemption

See [Superseded method-reference inquiry exemption](architecture.md#superseded-method-reference-inquiry-exemption) in the contract architecture.

## Evolving the contract

Use the canonical requirements and design explanations linked below when reviewing repairs, improvements, or redesign of `AGENTS.md`. These forwarding sections remain temporary navigation anchors and add no operating duties to ordinary project tasks.

### Choosing or replacing methods

See [method-selection qualifications](product-requirements.md#method-selection-qualifications) for the established constraints and [Choosing or replacing methods](architecture.md#choosing-or-replacing-methods) for the current selection rationale.

### Keeping the contract portable

See [portability and standing-context qualifications](product-requirements.md#portability-and-standing-context-qualifications) for the established constraints and [Keeping the contract portable](architecture.md#keeping-the-contract-portable) for the design rationale and recorded provider evidence.

### Current wording trade-offs

See the contract architecture's [Current wording trade-offs](architecture.md#current-wording-trade-offs) for the nine treatments, interpretation risks, and limited acceptance of the identified compromises.

## Design reference

See the contract architecture's non-normative [Design Reference](architecture.md#design-reference) for textual design-review scenarios and [Crosscutting Concepts](architecture.md#principles-and-reference-boundaries) for method-reference semantics and source assignments.

### Assessing design changes

See the contract architecture — [Assessing design changes](architecture.md#assessing-design-changes) for all 28 non-normative scenarios, preserved pending later requirements-led review.

### Principles and reference boundaries

See the contract architecture — [Principles and reference boundaries](architecture.md#principles-and-reference-boundaries) under Crosscutting Concepts for the canonical explanations, public-tip assignments, and consultation qualifications.
