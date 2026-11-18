# AGENTS.md contract architecture

This document explains the selected architecture of the [AGENTS.md operating contract](../../03-contract/prerelease_AGENTS.md): boundaries, vocabulary, clause traceability, and layer composition. [Detailed mechanisms](#crosscutting-concepts) keep prescriptions with their rationale.

**Status: current binding design, distinct from enduring product requirements.** The [baseline](../../01-behavior/deliverables/baseline.md) owns accepted intent and constraints; [authority and change](../../docs/authority-and-change.md#status-and-evidence-boundaries) defines status, revision authority, and evidence limits. Design explanations add no runtime duties beyond the delivered contract. [Design review](../docs/design-review.md) supplies editorial checks and non-normative illustrations.

## Glossary

The agent is the subject of operating rules unless another actor is explicit. Uppercase keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) / [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html): MUST requires, MUST NOT prohibits, SHOULD (NOT) recommends with weighed, justified departures, and MAY permits within stated terms. Unqualified operative language retains its source strength; explanation does not alter it. Material SHOULD exceptions need report explanations and waive no mandatory duty.

| Term | Current meaning |
| --- | --- |
| Task objective | The requested overall outcome. |
| Increment | A small, useful, bounded step, including investigation, normally understandable, reviewable, and verifiable alone. The non-standalone case has [explicit coherence and recovery duties](mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth). |
| Increment objective | The increment's bounded outcome toward the task objective. |
| Acceptance conditions | Observable criteria for completing the current increment; stating them does not automatically establish system requirements. |
| Handoff | Stopping before task completion and passing unfinished work to the requester or another person or agent. |
| Material | Significantly affecting correctness, scope, risk, or whether to proceed. |
| Permanent record | The canonical project document owning the topic, such as architecture or an ADR; chat and working notes are excluded. |

## Contract clause index

This index relates contract clauses, canonical mechanism explanations, and accepted intent. It does not establish acceptance of every prescription, complete realization, or evaluation coverage. All rows retain their own conditions and remain subject to requester/tool authority and progression guards. [Proposed-example coverage](../../01-behavior/deliverables/discovery.md#requirement-to-scenario-coverage) remains separate.

| Contract clauses | Engineering specification locations | Accepted intent supported |
| --- | --- | --- |
| [Purpose](../../03-contract/prerelease_AGENTS.md), [model](../../03-contract/prerelease_AGENTS.md#how-this-contract-works), [terms](../../03-contract/prerelease_AGENTS.md#terms-and-requirement-keywords) | [Established objectives](../../01-behavior/deliverables/baseline.md#established-objectives), the [glossary](#glossary), and [three interacting layers](#three-interacting-layers) | Established objectives (linked at left) |
| [Whole delivered contract](../../03-contract/prerelease_AGENTS.md) | [Design goals and boundaries](#design-goals-and-boundaries) | [PR1](../../01-behavior/deliverables/baseline.md#established-product-requirement) |
| [§1](../../03-contract/prerelease_AGENTS.md#1-work-cycle); [§1.1 Plan](../../03-contract/prerelease_AGENTS.md#11-plan--define-the-next-increment) | [Small commitments](mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth), [learning](mechanisms/work-cycle-and-inquiry.md#learning-throughout-the-work), [completion and inquiry](mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation), [knowledge roles](mechanisms/knowledge-and-documentation.md#documentation-choices), and [initial framing](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) | [BR1](../../01-behavior/deliverables/baseline.md#br1--focused-proportionate-authorized-work), [BR2](../../01-behavior/deliverables/baseline.md#br2--evidence-based-planning-and-knowledge-ownership), [BR4](../../01-behavior/deliverables/baseline.md#br4--bounded-investigation-and-timely-reassessment), [BR6](../../01-behavior/deliverables/baseline.md#br6--learning-from-observed-results), [BR7](../../01-behavior/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs) |
| [§1.2 Do](../../03-contract/prerelease_AGENTS.md#12-do--perform-the-authorized-work) | [Engineering scope boundaries](mechanisms/engineering-and-validation.md#engineering-scope-boundaries), [Simple Design](mechanisms/engineering-and-validation.md#simple-design-choosing-what-the-current-solution-needs), [component boundaries, refactoring, and validation](mechanisms/engineering-and-validation.md#component-boundaries-refactoring-and-validation), [qualified techniques](mechanisms/engineering-and-validation.md#focused-techniques-and-how-they-work-together) | [BR9](../../01-behavior/deliverables/baseline.md#br9--engineering-quality-and-preservation) |
| [§1.3 Study](../../03-contract/prerelease_AGENTS.md#13-study--assess-completion-and-learning); [§1.4 Act](../../03-contract/prerelease_AGENTS.md#14-act--use-the-findings) | [Completion and predictions](mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation), [validation and tests](mechanisms/engineering-and-validation.md#validation-and-test-evidence), [learning](mechanisms/work-cycle-and-inquiry.md#learning-throughout-the-work), and [composition](#three-interacting-layers) | [BR5](../../01-behavior/deliverables/baseline.md#br5--completion-supported-by-validation), [BR6](../../01-behavior/deliverables/baseline.md#br6--learning-from-observed-results) |
| [§2.1 Authority](../../03-contract/prerelease_AGENTS.md#21-authority-and-scope); [§2.2 decisions](../../03-contract/prerelease_AGENTS.md#22-decisions-and-requester-interaction) | [Decision factors](mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth) and [authorization and requester decisions](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions) | [BR3](../../01-behavior/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR8](../../01-behavior/deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority) |
| [§2.3 effort/limits](../../03-contract/prerelease_AGENTS.md#23-effort-estimates-and-requester-limits); [§2.5 continuation](../../03-contract/prerelease_AGENTS.md#25-continuing-to-another-increment) | [Quality and bounds](mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth), [authorization and continuation](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions), and [handoff/resumption](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) | [BR1](../../01-behavior/deliverables/baseline.md#br1--focused-proportionate-authorized-work), [BR3](../../01-behavior/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR7](../../01-behavior/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs) |
| [§2.4 context/inquiry](../../03-contract/prerelease_AGENTS.md#24-context-gathering-and-bounded-inquiry) | [Completion, predictions, and bounded investigation](mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation) and [outcome reporting](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) | [BR4](../../01-behavior/deliverables/baseline.md#br4--bounded-investigation-and-timely-reassessment) |
| [§3.1 requirements](../../03-contract/prerelease_AGENTS.md#31-new-or-revised-system-requirements) | [Requirement boundary](mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation), [revision authority](mechanisms/engineering-and-validation.md#validation-and-test-evidence), and [EARS forms](mechanisms/knowledge-and-documentation.md#ears-making-required-behavior-explicit) | [BR10](../../01-behavior/deliverables/baseline.md#br10--affected-requirements-and-documentation) |
| [§3.2 findings](../../03-contract/prerelease_AGENTS.md#32-durable-findings-and-permanent-records) | [Assessment writes, durability, and permanent records](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions) | [BR8](../../01-behavior/deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority) |
| [§3.3 decisions](../../03-contract/prerelease_AGENTS.md#33-significant-decisions-adrs); [§3.4 debt](../../03-contract/prerelease_AGENTS.md#34-technical-debt) | [ADRs](mechanisms/knowledge-and-documentation.md#adrs-preserving-the-reasons-for-lasting-choices) and [technical debt](mechanisms/knowledge-and-documentation.md#recording-technical-debt) | [BR8](../../01-behavior/deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority) |
| [§3.5 canonical knowledge/affected docs](../../03-contract/prerelease_AGENTS.md#35-canonical-knowledge-and-affected-documentation) | [DRY](mechanisms/knowledge-and-documentation.md#dry-keeping-knowledge-consistent-as-work-progresses) and [documentation synchronization](mechanisms/knowledge-and-documentation.md#documentation-choices) | [BR10](../../01-behavior/deliverables/baseline.md#br10--affected-requirements-and-documentation) |
| [§3.6 architecture/guides/code docs](../../03-contract/prerelease_AGENTS.md#36-architecture-guides-and-code-documentation) | [arc42 and README](mechanisms/knowledge-and-documentation.md#arc42-shared-architectural-context-as-the-project-grows) and [Diátaxis and code documentation](mechanisms/knowledge-and-documentation.md#diátaxis-choosing-content-for-the-readers-need) | [BR10](../../01-behavior/deliverables/baseline.md#br10--affected-requirements-and-documentation) |
| [§3.7 reporting](../../03-contract/prerelease_AGENTS.md#37-reporting) | [Reporting and continued execution](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) | [BR7](../../01-behavior/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs) |
| [§3.8 instructions/protection/external actions](../../03-contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions) | [Why the bridges differ](delivery-and-portability.md#why-the-bridges-differ) | [BR3](../../01-behavior/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR8](../../01-behavior/deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority), [PR1](../../01-behavior/deliverables/baseline.md#established-product-requirement) |
| [§3.9 references](../../03-contract/prerelease_AGENTS.md#39-method-references) | [Principles and reference boundaries](methods-and-references.md#principles-and-reference-boundaries) | [PR1](../../01-behavior/deliverables/baseline.md#established-product-requirement) |
| [§4 composition](../../03-contract/prerelease_AGENTS.md#4-how-the-layers-compose) | [Three interacting layers](#three-interacting-layers) | [BR1](../../01-behavior/deliverables/baseline.md#br1--focused-proportionate-authorized-work), [BR3](../../01-behavior/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR6](../../01-behavior/deliverables/baseline.md#br6--learning-from-observed-results), [BR7](../../01-behavior/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs) |

## Context and Scope

The contract governs agent conduct in adopting projects. [Delivery and portability](delivery-and-portability.md#context-and-scope) explains provider integration; [shared authority](../../docs/authority-and-change.md#development-time-and-runtime-authority) defines applicability to AGENTS-spec development.

## Solution Strategy

### Design goals and boundaries

The ordered objectives are token control first, then requester awareness and consequential control. Small increments are the principal mechanism for bounding work and speculative token use.

A broad objective can permit extensive work, especially in a new or poorly documented project with few established requirements, interfaces, or decisions. Small, meaningful increments limit the next commitment; progressive detail avoids designing distant work prematurely. Absence of architecture grants no unrestricted design authority: consequential direction still needs prior requester consultation unless specifically authorized.

Cumulative reassessment connects further work to evidence, objectives, direction, and limits. Bounded inquiry stops at sufficient evidence and requires reassessment at increment bounds; PDSA (Plan–Do–Study–Act) uses results to inform the next decision. Engineering practices protect quality, and canonical documentation preserves facts and reasons. Adequate reasoning, completeness, and validation constrain every effort-saving choice.

Initial framing and timely disclosure of blocking inquiry uncertainty provide awareness; consolidated reports and required consultation provide accountability and consequential control. Routine execution remains autonomous within authorization. These mechanisms impose no token quota or guarantee of savings; see [reporting design](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) for their distinct timings and strengths.

The contract is self-contained: guides explain it and bridges load/apply it without hidden operating duties. Adopting-project artifacts supply project facts, build commands, requirements, and architecture. This separation permits reuse without embedding an application's design in generic instructions.

Requester instructions take priority within the tool's actual hierarchy and permissions. The contract supplies no capabilities, technical enforcement, or override of native approvals. It is not a complete product-development process, branching strategy, workflow engine, or method tutorial; methods cannot invent requirements or authority. [Method selection](methods-and-references.md#choosing-or-replacing-methods) and [portability](delivery-and-portability.md#keeping-the-contract-portable) explain the remaining design constraints and trade-offs.

### Three interacting layers

The contract separates three questions that need answers throughout a task:

| Layer | Question it answers | Role in the design |
| --- | --- | --- |
| [Work cycle](../../03-contract/prerelease_AGENTS.md#1-work-cycle) | What is the agent doing with the current increment? | Organize planning, execution, assessment, and use of the findings. |
| [Progression guards](../../03-contract/prerelease_AGENTS.md#2-progression-guards) | May this work proceed, or is requester direction needed? | Check authority, scope, unresolved decisions, requester limits, cumulative reassessment, inquiry bounds, and permission to continue. |
| [Triggered rules](../../03-contract/prerelease_AGENTS.md#3-triggered-rules) | Has something happened that creates a duty or permission? | Apply the relevant rule when, for example, a requirement changes, a durable finding emerges, documentation is affected, or a report becomes due. Each rule retains its own strength and conditions. |

One action can involve all three layers. While planning an importer change, a material, durable parser limitation triggers a record duty, while a proposed departure from its established error contract requires requester direction before adoption or implementation unless specifically authorized. Naming the phase settles neither duty nor authority.

The separation follows cross-phase behavior: authorization and limits matter throughout, and findings can emerge in any phase. Embedding these concerns in one phase would imply restricted applicability or require rereading earlier phases. The cycle presents the ordinary path; guards expose control state; triggered rules remain phase-independent. Phases may overlap or repeat, and guards are not extra phases.

The current [composition rule](../../03-contract/prerelease_AGENTS.md#4-how-the-layers-compose) starts at Plan, applies progression guards whenever work would advance or a relevant decision is due, and applies each triggered rule whenever its trigger occurs. After Study and Act, the applicable outcome is:

| State | Prescribed next action |
| --- | --- |
| Task done | Complete and report. |
| Stopping before task completion | Hand off with a handoff report. |
| A guard or other rule requires requester direction, or no existing authorization covers another increment | Report and await direction. |
| Otherwise | Return to Plan for the next authorized increment, with proportionate intermediate communication. |

No cycle step, satisfied guard, or fulfilled duty extends authorization. Completing increments, reporting, recording decisions, discovering findings, or exhausting inquiry grants none; triggered permissions stay within their terms.

The organization aims to make these relationships understandable. No measurement establishes improved comprehension, agent adherence, or token use.

## Crosscutting Concepts

| Canonical document | Responsibility |
| --- | --- |
| [Work cycle and inquiry](mechanisms/work-cycle-and-inquiry.md) | Small commitments, PDSA, completion and predictions, bounded investigation, and the worked runtime example. |
| [Requester decisions and reporting](mechanisms/requester-decisions-and-reporting.md) | Authorization, consultation, limits, assessment writes and durable findings, reporting, and handoffs. |
| [Engineering and validation](mechanisms/engineering-and-validation.md) | Scope boundaries, Simple Design, component practices, preservation, validation, and focused techniques. |
| [Knowledge and documentation](mechanisms/knowledge-and-documentation.md) | Canonical knowledge, documentation roles, EARS, arc42, ADRs, debt, and Diátaxis. |
| [Delivery and portability](delivery-and-portability.md) | Provider bridges, portability rationale and evidence, standing context, and wording trade-offs. |
| [Methods and references](methods-and-references.md) | Selection and replacement rationale, exact source assignments and exclusions, and consultation limits. |
| [Decisions and alternatives](../docs/decisions.md) | Decision status, historical interpretation, alternatives, superseded mechanisms, and documentation organization. |

## Runtime View

[Work cycle and inquiry](mechanisms/work-cycle-and-inquiry.md#runtime-view) owns the complete [worked CSV task example](mechanisms/work-cycle-and-inquiry.md#how-the-design-works-in-a-task).

## Architecture Decisions

The [design decision index](../docs/decisions.md#architecture-decisions) records current choices, superseded controls, and the [ownership of contract-design documentation](../docs/decisions.md#ownership-of-contract-design-documentation).
