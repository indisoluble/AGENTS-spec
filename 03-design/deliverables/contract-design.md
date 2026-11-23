# AGENTS.md contract architecture

This document explains the selected architecture of the operating contract, including its boundaries, vocabulary and layer composition. [Detailed mechanisms](#crosscutting-concepts) keep prescriptions with their rationale.

**Status: current binding design, distinct from enduring product requirements.** [`02-formulation/deliverables/baseline.md`](../../02-formulation/deliverables/baseline.md) owns accepted requirements and constraints. Shared authority ([`docs/authority.md` § Status of engineering records](../../docs/authority.md#status-of-engineering-records)) explains what the records establish about status and revision authority. Design explanations add no runtime duties beyond the delivered contract. The editorial checks ([`03-design/docs/design-review.md`](../docs/design-review.md)) and the illustrations ([`03-design/docs/design-illustrations.md`](../docs/design-illustrations.md)) support review of explanations.

## Glossary

The agent is the subject of operating rules unless another actor is explicit. Uppercase keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) / [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html): MUST requires, MUST NOT prohibits, SHOULD (NOT) recommends with weighed, justified departures, and MAY permits within stated terms. Unqualified operative language retains its source strength; explanation does not alter it. Material SHOULD exceptions need report explanations and waive no mandatory duty.

| Term | Current meaning |
| --- | --- |
| Task objective | The requested overall outcome. |
| Increment | A small, useful, bounded step, including investigation, normally understandable, reviewable, and verifiable alone. The non-standalone case has explicit coherence and recovery duties ([`03-design/deliverables/mechanisms/work-cycle.md` § Small commitments with sufficient depth](mechanisms/work-cycle.md#small-commitments-with-sufficient-depth)). |
| Increment objective | The increment's bounded outcome toward the task objective. |
| Acceptance conditions | Observable criteria for completing the current increment; stating them does not automatically establish system requirements. |
| Handoff | Stopping before task completion and passing unfinished work to the requester or another person or agent. |
| Material | Significantly affecting correctness, scope, risk, or whether to proceed. |
| Permanent record | The canonical project document owning the topic, such as architecture or an ADR; chat and working notes are excluded. |

## Context and Scope

The contract governs agent conduct in adopting projects. [`03-design/deliverables/delivery-and-portability.md` § Context and Scope](delivery-and-portability.md#context-and-scope) explains provider integration; shared authority ([`docs/authority.md` § Repository development and instruction loading](../../docs/authority.md#repository-development-and-instruction-loading)) defines applicability to AGENTS-spec development.

## Solution Strategy

### Design goals and boundaries

The ordered objectives ([`01-discovery/deliverables/objectives-and-rationale.md` § Established objectives](../../01-discovery/deliverables/objectives-and-rationale.md#established-objectives)) are token control first, then requester awareness and consequential control. Small increments are the principal mechanism for bounding work and speculative token use.

A broad objective can permit extensive work, especially in a new or poorly documented project with few established requirements, interfaces, or decisions. Small, meaningful increments limit the next commitment; progressive detail avoids designing distant work prematurely. Absence of architecture grants no unrestricted design authority: consequential direction still needs prior requester consultation unless specifically authorized.

Cumulative reassessment connects further work to evidence, objectives, direction, and limits. Bounded inquiry stops at sufficient evidence and requires reassessment at increment bounds; PDSA (Plan–Do–Study–Act) uses results to inform the next decision. Engineering practices protect quality, and canonical documentation preserves facts and reasons. Adequate reasoning, completeness, and validation constrain every effort-saving choice.

Initial framing and timely disclosure of blocking inquiry uncertainty provide awareness; consolidated reports and required consultation provide accountability and consequential control. Routine execution remains autonomous within authorization. These mechanisms impose no token quota or guarantee of savings; see reporting design ([`03-design/deliverables/mechanisms/requester-decisions-and-reporting.md` § Reporting and continued execution](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution)) for their distinct timings and strengths.

The contract is self-contained: guides explain it and bridges load/apply it without hidden operating duties. Adopting-project artifacts supply project facts, build commands, requirements, and architecture. This separation permits reuse without embedding an application's design in generic instructions.

Requester instructions take priority within the tool's actual hierarchy and permissions. The contract supplies no capabilities, technical enforcement, or override of native approvals. It is not a complete product-development process, branching strategy, workflow engine, or method tutorial; methods cannot invent requirements or authority. Method selection ([`03-design/deliverables/methods-and-references.md` § Choosing or replacing methods](methods-and-references.md#choosing-or-replacing-methods)) and portability ([`03-design/deliverables/delivery-and-portability.md` § Keeping the contract portable](delivery-and-portability.md#keeping-the-contract-portable)) explain the remaining design constraints and trade-offs.

### Three interacting layers

The contract separates three questions that need answers throughout a task:

| Layer | Question it answers | Role in the design |
| --- | --- | --- |
| [`03-design/deliverables/mechanisms/work-cycle.md`](mechanisms/work-cycle.md) | What is the agent doing with the current increment? | Organize planning, execution, assessment, and use of the findings. |
| Progression guards ([`03-design/deliverables/mechanisms/requester-decisions-and-reporting.md` § Authorization and requester decisions](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions)) | May this work proceed, or is requester direction needed? | Check authority, scope, unresolved decisions, requester limits, cumulative reassessment, inquiry bounds, and permission to continue. |
| [Triggered rules](#crosscutting-concepts) | Has something happened that creates a duty or permission? | Apply the relevant rule when, for example, a requirement changes, a durable finding emerges, documentation is affected, or a report becomes due. Each rule retains its own strength and conditions. |

One action can involve all three layers. While planning an importer change, a material, durable parser limitation triggers a record duty, while a proposed departure from its established error contract requires requester direction before adoption or implementation unless specifically authorized. Naming the phase settles neither duty nor authority.

The separation follows cross-phase behavior: authorization and limits matter throughout, and findings can emerge in any phase. Embedding these concerns in one phase would imply restricted applicability or require rereading earlier phases. The cycle presents the ordinary path; guards expose control state; triggered rules remain phase-independent. Phases may overlap or repeat, and guards are not extra phases.

The current composition rule starts at Plan, applies progression guards whenever work would advance or a relevant decision is due, and applies each triggered rule whenever its trigger occurs. After Study and Act, the applicable outcome is:

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
| [`03-design/deliverables/mechanisms/work-cycle.md`](mechanisms/work-cycle.md) | Small commitments, PDSA, completion and predictions, and the worked runtime example. |
| [`03-design/deliverables/mechanisms/bounded-inquiry.md`](mechanisms/bounded-inquiry.md) | Context gathering, notification of blocking uncertainty, evidence for stopping or continuing, consultation, and inquiry outcomes. |
| [`03-design/deliverables/mechanisms/requester-decisions-and-reporting.md`](mechanisms/requester-decisions-and-reporting.md) | Authorization, consultation, limits, assessment writes and durable findings, reporting, and handoffs. |
| [`03-design/deliverables/mechanisms/engineering-and-validation.md`](mechanisms/engineering-and-validation.md) | Scope boundaries, Simple Design, component practices, preservation, validation, and focused techniques. |
| [`03-design/deliverables/mechanisms/knowledge-and-documentation.md`](mechanisms/knowledge-and-documentation.md) | Canonical knowledge, documentation roles, EARS, arc42, ADRs, debt, and Diátaxis. |
| [`03-design/deliverables/delivery-and-portability.md`](delivery-and-portability.md) | Provider bridges, portability rationale and evidence, standing context, and wording trade-offs. |
| [`03-design/deliverables/methods-and-references.md`](methods-and-references.md) | Selection and replacement rationale, exact source assignments and exclusions, and consultation limits. |
| Decisions and alternatives ([`03-design/docs/decisions.md`](../docs/decisions.md)) | Decision status, rationale, alternatives, superseded mechanisms, and documentation ownership. |

## Runtime View

[`03-design/deliverables/mechanisms/work-cycle.md` § Runtime View](mechanisms/work-cycle.md#runtime-view) owns the complete worked CSV task example ([`03-design/deliverables/mechanisms/work-cycle.md` § How the design works in a task](mechanisms/work-cycle.md#how-the-design-works-in-a-task)).

## Architecture Decisions

The design decision index ([`03-design/docs/decisions.md` § Architecture decisions](../docs/decisions.md#architecture-decisions)) records current choices, superseded controls, and who owns the contract-design documentation ([`03-design/docs/decisions.md` § Ownership of contract-design documentation](../docs/decisions.md#ownership-of-contract-design-documentation)).
