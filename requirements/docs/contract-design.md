# Product requirements and design of AGENTS.md

**Engineering-only document.** This file is a temporary consolidation document within the requirements project at `requirements/docs/contract-design.md` and remains excluded from the intended consumer release. It is not a runtime instruction file, provider bridge, or adoption guide, and creates no additional consumer operating duties.

This document is the authoritative design source for the reusable, opinionated [AGENTS.md](../../contract/prerelease_AGENTS.md) contract's remaining currently binding design prescriptions and their semantics, selected mechanisms, rationale, trade-offs, and subsequent engineering evolution. [Contract architecture](architecture.md) owns the transferred design overview, goals and boundaries, three-layer interaction and continuation, bounded-work design, PDSA learning design, completion and prediction distinctions, bounded-inquiry design, authorization and requester decisions, reporting and continued execution, Simple Design, DRY, component boundaries, refactoring, validation, focused techniques, arc42 documentation design, EARS requirements-writing design, ADR-writing design, technical-debt recording, Diátaxis documentation design, method-selection and portability rationale, current wording trade-offs, worked task example, shared current-semantics vocabulary and contract-clause coverage index, and [selected decisions and historical alternatives](architecture.md#architecture-decisions). [Product requirements](product-requirements.md) owns the established objectives, PR1, and product constraints; [requirement candidates](requirement-candidates.md) owns provisional RC1–RC10 and their unresolved acceptance questions. [Status and evidence boundaries](architecture.md#status-and-evidence-boundaries), [engineering scope boundaries](architecture.md#engineering-scope-boundaries), and [provider integration](architecture.md#context-and-scope) also belong to the contract architecture; the remaining design explanations, assessment scenarios, and reference material stay here. Internal requirements and explanations add no runtime duties: `AGENTS.md` remains the independently self-contained normative runtime contract delivered to consuming agents.

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

Use this material when reviewing a proposed change or an explanation of the contract: the design scenarios check combinations of rules against their intended distinctions, and the reference assignments preserve attribution and consultation limits.

### Assessing design changes

**Status: design-assessment scenarios against the current implementation, not independently accepted product requirements or evaluation results.** The rows preserve interpretation distinctions for textual review. The [candidate inventory](requirement-candidates.md#requirement-candidates) identifies where independent product acceptance remains unresolved. [Architecture](../../docs/architecture.md#what-evaluation-evidence-can-establish) owns the relationship to behavioral evidence; [evaluations.md](../../evaluations/docs/evaluations.md#purpose-and-evaluation-model) owns evaluation strategy and limits. These scenarios establish neither comprehensive coverage nor a new evaluation procedure.

The design can be assessed at two levels: whether the contract works as a self-contained set of instructions, and whether a proposed change preserves or deliberately alters the meaning of its clauses. A standalone reading tests the first; comparison of strength, trigger, scope, exception, and meaning tests the second. The detailed patterns, fields, and obligations are specified in the [current-semantic topic sections](#current-semantics-vocabulary-and-coverage); `AGENTS.md` remains the normative runtime authority.

| Scenario | Design distinction to assess |
| --- | --- |
| Broad objective, including a new project | The agent limits its next commitment and keeps later work at outline level until detail is needed for the next decision. Necessary depth, affected dependencies, and validation remain within scope; the breadth of the goal does not justify an unconstrained first increment. |
| Starting a task | After proportionate preliminary context gathering, assess whether the agent briefly communicates the task outline and first increment's objective and bounds before substantial work. The statement creates no approval checkpoint. It can also communicate material inquiry uncertainty and its significance, satisfying that notification without a second message. |
| Requester expectation or binding limit | “I expect a small fix” is not automatically a budget; “consult before a second increment” is a checkpoint. Material ambiguity about the intended force needs clarification. Only requester direction can revise requester-imposed limits or checkpoints; subdivision and retries do not reset them. |
| Ordinary authorized change | The agent selects a small increment and completes its checks before completing the increment, even without a chat report. Completion grants no additional permission or automatic documentation artifact; another increment can proceed under existing authorization unless a checkpoint requires a pause. |
| Completed exploration without a record trigger | Without durable material findings or significant lasting choices, no record is required merely to log the discussion. Transient task facts, such as a temporary CI outage or a failed experiment relevant only to the current attempt, follow the reporting rules only. |
| Material findings or significant proposals during review | A [finding](../../contract/prerelease_AGENTS.md#32-durable-findings-and-permanent-records) needs a permanent record only when it is both material and durable, even if it comes from a discarded approach; a missing owner leads to the minimum record rather than backfill, and a prohibited write is reported as unfinished work. A concrete significant proposal ready for decision or review requires an [ADR](../../contract/prerelease_AGENTS.md#33-significant-decisions-adrs) retaining the evidence that materially shaped it rather than routine PDSA history; brainstorming or a finding alone does not. Status reflects existing decision authority. Recording supplies no implementation authority or new approval checkpoint. |
| Verified factual documentation error during assessment | The agent may make an existing description of current project facts within the assessed scope match the canonical owner of that kind of knowledge, subject to scope, requester restrictions, §3.8, and tool permissions. Requirements, decision records, and protected instruction files are excluded. A verified mismatch with authoritative package configuration can justify correcting a README command; it does not authorize changing implementation, intended requirements, accepted decisions, or protected instruction files. |
| Task-relevant debt found during assessment | Evidenced debt may be recorded after considering accepted requirements and trade-offs. Any entry triggers classification-uncertainty and chat-disclosure duties. The general material-findings requirement still applies; neither classification nor recording authorizes a fix. |
| Requester or tool prohibits writes | Assessment permissions remain subject to requester restrictions (§2.1) and §3.8. An explicit ban on creating, modifying, or deleting files covers records and factual documentation corrections; tool restrictions also remain binding. Findings and proposed text can be supplied in chat within those limits, but chat does not satisfy a permanent-record obligation; the unmade record is reported as unfinished work. |
| Continued execution and reporting | Several increments can complete without a report for each one. At task completion, handoff, or when seeking input, the agent consolidates unreported work. Routine progress reports should be minimized and intermediate communication should be concise and useful. Assess a routine update against those recommendations and any requester or tool instructions; its presence alone is not an automatic violation. Required findings and records are maintained throughout. |
| Requested or required disclosures | Disclosures affecting authorization or a decision requiring requester input must precede affected work. Other information, including inquiry outcomes, should normally join the next consolidated report. Initial task framing precedes substantial work, and material inquiry uncertainty and its significance must be made clear promptly unless already communicated in the request or task framing. Reporting or notification alone creates no approval checkpoint and cannot replace required consultation. |
| Selecting and revisiting work | Plan connects the requested outcome, permission, relevant context, and evidence to a useful next increment from the first request. Assess whether that connection is understandable, including when missing evidence or consequential constraints change the next step. Study and Act inform later planning; later work stays at outline level until detail is needed and revisions stay within authorization. |
| Investigation contradicts its prediction | An evidenced answer can complete the investigation while disproving the prediction; unmet implementation behavior remains incomplete. |
| Reading existing project documentation | Reading remains context gathering without inspection-by-inspection announcements, even for a material blocking question. Inspecting relevant code, callers, tests, configuration, and directly related dependencies to establish context is also context gathering. Scope, requester limits, proportionate work, and cumulative reassessment apply to all of it. |
| Prescribed empirical operation or acceptance check | Unknown output alone does not establish inquiry. Contrast executing a settled measurement/calculation or checking acceptance with using the same procedure to investigate an unsettled approach. Classify purpose before assessing inquiry duties; a procedure neither automatically triggers nor exempts inquiry. |
| Material uncertainty about how to proceed blocks the next decision after context gathering | Promptly make the uncertainty and its significance clear unless already communicated in the request or task framing. Private planning or a retrospective report cannot replace a required timely notification. Assess actual bounded, proportionate investigation; the absence of a five-element announcement or declared effort allowance is not itself a violation. |
| The request already communicates inquiry uncertainty and its significance | No duplicate inquiry notification is required. Initial task framing, bounded conduct, sufficient evidence, cumulative reassessment, and any required consultation still apply. Coverage by the request does not authorize every consequential direction that the inquiry might suggest. |
| Inquiry exposes an unsettled consequential direction | Narrow investigation may establish facts for consultation within existing authorization. Obtain requester direction before adopting or implementing a choice requiring consultation under §2.2; merely notifying the requester or presenting evidence does not satisfy that requirement. |
| Investigation obtains sufficient evidence or reaches an increment's bounds | End inquiry when evidence is sufficient. At an increment's bounds with insufficient evidence, reassess before further investigation without claiming completion. Further attempts need justification from preceding findings and must respect authorization, limits, and checkpoints; a new advance announcement is not automatic. Report outcomes at §3.7's occasions and seek required direction before affected work. Neither an exhausted attempt nor a new increment supplies authority or resets a requester limit. |
| Acceptance-critical verification is unavailable | Sufficient alternative evidence can establish the same condition unless a specific check is required. Otherwise the condition remains unverified and validation incomplete unless validly revised. Disclosure alone does not satisfy it. |
| Equivalent evidence exists for an available acceptance check | The relevant available check must run. Equivalence alone does not permit substitution; the unavailable-check exception does not apply. |
| Known risk without an internal-quality compromise | Preserve the known risk under topic 11 without inventing a technical-debt classification. |
| Documentation-only work | Applicable methods and validation apply without requiring code or unit tests for their own sake. |
| Additional work | Reassess cumulative progress, remaining work, direction, and limits before expanding planned work or starting another increment/attempt. Each next increment needs evidence supporting its contribution and must remain within existing authorization, direction, and limits. |
| New consequential design direction or material departure | Obtain requester direction before adoption or implementation unless the specific choice is already authorized, including in a new project without established architecture. A Proposed ADR can prepare the decision; recording it or reporting later cannot supply prior authorization. |
| Handoff and resumption | Transfer meaningful results and continuation state: task objective and established direction; applicable limits/checkpoints and consumed allowances; next or unfinished increment objective/bounds/acceptance conditions; and relevant inquiry conclusions, supporting evidence, and unresolved uncertainty. A chronological activity log is insufficient. Use that state on resumption; recover missing authorization or limit state or obtain direction before dependent work. |
| Any tool fails to load the contract | The package defines no separate bootstrap stop/report/resume policy. Neither a bridge nor a README supplies one, and an unloaded contract cannot govern the failure. Use actual tool and requester instructions and distinguish loading diagnostics from demonstrated application. |
| Root and directory instruction files | Only the three root-relative contract/bridge paths receive special edit protection. Subtree rules may be added only when compatible with the root contract; the tool decides discovery, scope, and precedence, which never makes conflicting policy acceptable; encountered conflicts are reported. |

The relevant dependencies span [engineering](../../contract/prerelease_AGENTS.md#12-do--perform-the-authorized-work), [validation](../../contract/prerelease_AGENTS.md#13-study--assess-completion-and-learning), the [progression guards](../../contract/prerelease_AGENTS.md#2-progression-guards), the [triggered rules](../../contract/prerelease_AGENTS.md#3-triggered-rules) for knowledge retention and documentation, and [how the layers compose](../../contract/prerelease_AGENTS.md#4-how-the-layers-compose). Method conditions, appropriate-test recommendations, required validation, documentation scope, and requester authority all contribute to the resulting behavior.

Changes to protected instruction files follow [their authorization rule](../../contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions), including file-specific recommendations and necessary companion edits to the other two listed files; other affected documentation follows the ordinary synchronization rules. Substantive policy changes need explicit identification. An explanation or review checklist cannot substitute for the actual clauses, and a shorter contract does not by itself establish equivalent agent behavior or token savings.

### Principles and reference boundaries

Method references are linked sources explaining methods or practices named in the contract; they clarify those methods without adding rules. The accounts linked in this guide provide interpretive material within those conditions. The design draws on specific accounts rather than requiring whole frameworks or access to a paid book. The [Pragmatic Programmer book](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) is paid; its assigned public tips and extracts are freely available.

The exact [public-tip assignments](https://pragprog.com/tips/) are maintained here because the contract's links do not carry per-rule tip numbers:

| Concern | Assigned tips |
| --- | --- |
| Documentation synchronization | 13 |
| Components, boundaries, and coupling | 17, 44–45, 47–48 |
| Failures and contracts | 36–37 |
| Resources and mutation scope | 40–41 |
| Root causes | 65 |
| Attack surface | 72 |
| Naming | 74 |
| Regression checks | 94 |

The coupling assignment excludes tip 46. The DRY, inheritance, and shared-state extracts linked from their respective design explanations supply fuller accounts for their respective concerns. Attribution identifies supporting material, without claiming that one reference states the contract's combined preservation duties verbatim.

[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) supply requirement-keyword semantics. They concern the strength of agent obligations, while EARS expresses system requirements and ADRs record choices and reasons. Supporting explanations include [IHI's testing-changes guidance](https://www.ihi.org/library/model-for-improvement/testing-changes) and [arc42's debt FAQ](https://faq.arc42.org/questions/C-11-1/); they add no operating obligations.

The contract should normally suffice for ordinary cases. Under the [method-reference rules](../../contract/prerelease_AGENTS.md#39-method-references), an agent may consult a linked source when the contract leaves a material ambiguity in applying that method, reading only enough to resolve it. The ambiguity, consulted reference, and resulting interpretation must be reported, and no other practices are imported. Research stays bounded by §§1.1 and 2.4: if the consultation is inquiry into material uncertainty blocking the next decision, its notification and conduct requirements apply, including the exception for uncertainty and significance already communicated in the request or task framing. Clear rules must not be researched. Before broader research, the agent must explain the unresolved uncertainty and ask the requester. Technical research for a task follows its scope, authorization, and applicable inquiry rules. This distinction prevents an explanatory link from becoming an open-ended research assignment or importing a reference's stronger rhetoric as policy.
