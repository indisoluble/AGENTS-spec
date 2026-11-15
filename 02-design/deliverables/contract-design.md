# AGENTS.md contract architecture

This is the design-architecture entry point for the reusable [AGENTS.md](../../03-contract/prerelease_AGENTS.md) operating instructions. It owns design scope, goals and boundaries, shared terminology, the complete current-semantics vocabulary and contract-clause coverage index, and contract composition through three interacting layers. Detailed prescriptions and their explanations stay together in the canonical documents linked below. The [engineering-system architecture](../../docs/architecture.md) owns repository relationships; [authority and change propagation](../../docs/authority-and-change.md) owns development authority and shared status and evidence boundaries; an adopting application's architecture belongs to that project. This documentation adds no development-pipeline stage.

**Status: current binding design, with rationale, historical context, and non-normative design reference distinguished.** Selected mechanisms and their rationale are distinct from independently accepted enduring product requirements. [baseline.md](../../01-behavior/deliverables/baseline.md) owns established objectives, accepted BR1–BR10, PR1, and product constraints; [discovery.md](../../01-behavior/deliverables/discovery.md) owns proposal status, coverage, and remaining formulation questions and indexes the [proposed example suites](../../01-behavior/deliverables/discovery.md#proposed-example-suites); [candidate and example history](../../01-behavior/docs/candidate-and-example-history.md) owns the historical RC inventory and its disposition. [Status and evidence boundaries](../../docs/authority-and-change.md#status-and-evidence-boundaries) retains the shared status distinctions and current design's authority and revision qualifications. This document adds no operating duties beyond the delivered contract.

The [shared status and evidence boundaries](../../docs/authority-and-change.md#status-and-evidence-boundaries) explain the authority of documented statements. Following the [selected arc42 approach](mechanisms/knowledge-and-documentation.md#arc42-shared-architectural-context-as-the-project-grows), the views below retain the shared vocabulary, solution strategy, and navigation to context, crosscutting mechanisms, runtime behavior, and decisions. The companion [Design Reference](../docs/design-review.md#design-reference) owns editorial guidance and all 28 non-normative [assessment scenarios](../docs/design-review.md#assessing-design-changes), pending later requirements-led review.

| Canonical document | Responsibility |
| --- | --- |
| [Work cycle and inquiry](mechanisms/work-cycle-and-inquiry.md) | Small commitments, PDSA, completion and predictions, bounded investigation, and the worked runtime example. |
| [Requester decisions and reporting](mechanisms/requester-decisions-and-reporting.md) | Authorization, consultation, limits, assessment writes and durable findings, reporting, and handoffs. |
| [Engineering and validation](mechanisms/engineering-and-validation.md) | Scope boundaries, Simple Design, component practices, preservation, validation, and focused techniques. |
| [Knowledge and documentation](mechanisms/knowledge-and-documentation.md) | Canonical knowledge, documentation roles, EARS, arc42, ADRs, debt, and Diátaxis. |
| [Delivery and portability](delivery-and-portability.md) | Provider bridges, portability rationale and evidence, standing context, and wording trade-offs. |
| [Methods and references](methods-and-references.md) | Selection and replacement rationale, exact source assignments and exclusions, and consultation limits. |
| [Decisions and alternatives](../docs/decisions-and-alternatives.md) | Decision status, historical interpretation, alternatives, superseded mechanisms, and the structural successor. |

## Glossary

### Current-semantics vocabulary and coverage

Unless another actor is explicit, the agent is the subject of operating duties, recommendations, prohibitions, and permissions below and in the indexed design documents. Uppercase keywords retain [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) / [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) meanings: MUST is mandatory, MUST NOT prohibits, SHOULD and SHOULD NOT are recommendations whose departures need weighed consequences and justification, and MAY permits within its stated terms. Unqualified operative language retains its source meaning; explanatory prose does not change a prescription's strength. Material SHOULD exceptions also need report explanations. No recommendation exception waives a mandatory rule.

| Term | Current meaning |
| --- | --- |
| Task objective | The requested overall outcome. |
| Increment | A small, useful, bounded step, including investigation, normally understandable, reviewable, and verifiable alone. The non-standalone case has [explicit coherence and recovery duties](mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth). |
| Increment objective | The increment's bounded outcome toward the task objective. |
| Acceptance conditions | Observable criteria for completing the current increment; stating them does not automatically establish system requirements. |
| Handoff | Stopping before task completion and passing unfinished work to the requester or another person or agent. |
| Material | Significantly affecting correctness, scope, risk, or whether to proceed. |
| Permanent record | The canonical project document owning the topic, such as architecture or an ADR; chat and working notes are excluded. |

The following index assigns current-semantic detail within this contract architecture. Contract clause references provide traceability; the indexed canonical documents specify the operating detail. All rows remain subject to requester and tool authority, the progression guards, and each rule's own conditions. The outcome links below trace the accepted intent each current mechanism supports, not independent acceptance of every prescription in that row, proof of complete realization, or evaluation coverage. [Phase 2 example coverage](../../01-behavior/deliverables/discovery.md#requirement-to-scenario-coverage) remains proposed; the mechanism semantics and historical statuses below are unchanged.

| Contract clauses | Engineering specification locations | Accepted intent supported |
| --- | --- | --- |
| [Purpose](../../03-contract/prerelease_AGENTS.md), [model](../../03-contract/prerelease_AGENTS.md#how-this-contract-works), [terms](../../03-contract/prerelease_AGENTS.md#terms-and-requirement-keywords) | [Established objectives](../../01-behavior/deliverables/baseline.md#established-objectives), this vocabulary, and [three interacting layers](#three-interacting-layers) | Established objectives (linked at left) |
| [Whole delivered contract](../../03-contract/prerelease_AGENTS.md) | [Design goals and boundaries](#design-goals-and-boundaries) | [PR1](../../01-behavior/deliverables/baseline.md#established-product-requirement) |
| [§1](../../03-contract/prerelease_AGENTS.md#1-work-cycle); [§1.1 Plan](../../03-contract/prerelease_AGENTS.md#11-plan--define-the-next-increment) | [Small commitments](mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth), [learning](mechanisms/work-cycle-and-inquiry.md#learning-throughout-the-work), [completion and inquiry](mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation), [knowledge roles](mechanisms/knowledge-and-documentation.md#documentation-choices), and [initial framing](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) | [BR1](../../01-behavior/deliverables/baseline.md#br1--focused-proportionate-authorized-work), [BR2](../../01-behavior/deliverables/baseline.md#br2--evidence-based-planning-and-knowledge-ownership), [BR4](../../01-behavior/deliverables/baseline.md#br4--bounded-investigation-and-timely-reassessment), [BR6](../../01-behavior/deliverables/baseline.md#br6--learning-from-observed-results), [BR7](../../01-behavior/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs) |
| [§1.2 Do](../../03-contract/prerelease_AGENTS.md#12-do--perform-the-authorized-work) | [Engineering scope boundaries](mechanisms/engineering-and-validation.md#engineering-scope-boundaries), [Simple Design](mechanisms/engineering-and-validation.md#simple-design-choosing-what-the-current-solution-needs), [component boundaries, refactoring, and validation](mechanisms/engineering-and-validation.md#component-boundaries-refactoring-and-validation), [qualified techniques](mechanisms/engineering-and-validation.md#focused-techniques-and-how-they-work-together) | [BR9](../../01-behavior/deliverables/baseline.md#br9--engineering-quality-and-preservation) |
| [§1.3 Study](../../03-contract/prerelease_AGENTS.md#13-study--assess-completion-and-learning); [§1.4 Act](../../03-contract/prerelease_AGENTS.md#14-act--use-the-findings) | [Completion and predictions](mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation), [validation and tests](mechanisms/engineering-and-validation.md#validation-and-test-evidence), [learning](mechanisms/work-cycle-and-inquiry.md#learning-throughout-the-work), and [composition](#three-interacting-layers) | [BR5](../../01-behavior/deliverables/baseline.md#br5--completion-supported-by-validation), [BR6](../../01-behavior/deliverables/baseline.md#br6--learning-from-observed-results) |
| [§2.1 Authority](../../03-contract/prerelease_AGENTS.md#21-authority-and-scope); [§2.2 decisions](../../03-contract/prerelease_AGENTS.md#22-decisions-and-requester-interaction) | [Decision factors](mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth) and [authorization and requester decisions](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions) | [BR3](../../01-behavior/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR8](../../01-behavior/deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority) |
| [§2.3 effort/limits](../../03-contract/prerelease_AGENTS.md#23-effort-estimates-and-requester-limits); [§2.5 continuation](../../03-contract/prerelease_AGENTS.md#25-continuing-to-another-increment) | [Quality and bounds](mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth), [authorization and continuation](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions), and [handoff/resumption](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) | [BR1](../../01-behavior/deliverables/baseline.md#br1--focused-proportionate-authorized-work), [BR3](../../01-behavior/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR7](../../01-behavior/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs) |
| [§2.4 context/inquiry](../../03-contract/prerelease_AGENTS.md#24-context-gathering-and-bounded-inquiry) | [Completion, predictions, and bounded investigation](mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation) and [outcome reporting](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) | [BR4](../../01-behavior/deliverables/baseline.md#br4--bounded-investigation-and-timely-reassessment) |
| [§3.1 requirements](../../03-contract/prerelease_AGENTS.md#31-new-or-revised-system-requirements) | [Requirement boundary and revision](mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation) and [EARS forms](mechanisms/knowledge-and-documentation.md#ears-making-required-behavior-explicit) | [BR10](../../01-behavior/deliverables/baseline.md#br10--affected-requirements-and-documentation) |
| [§3.2 findings](../../03-contract/prerelease_AGENTS.md#32-durable-findings-and-permanent-records) | [Assessment writes, durability, and permanent records](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions) | [BR8](../../01-behavior/deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority) |
| [§3.3 decisions](../../03-contract/prerelease_AGENTS.md#33-significant-decisions-adrs); [§3.4 debt](../../03-contract/prerelease_AGENTS.md#34-technical-debt) | [ADRs](mechanisms/knowledge-and-documentation.md#adrs-preserving-the-reasons-for-lasting-choices) and [technical debt](mechanisms/knowledge-and-documentation.md#recording-technical-debt) | [BR8](../../01-behavior/deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority) |
| [§3.5 canonical knowledge/affected docs](../../03-contract/prerelease_AGENTS.md#35-canonical-knowledge-and-affected-documentation) | [DRY](mechanisms/knowledge-and-documentation.md#dry-keeping-knowledge-consistent-as-work-progresses) and [documentation synchronization](mechanisms/knowledge-and-documentation.md#documentation-choices) | [BR10](../../01-behavior/deliverables/baseline.md#br10--affected-requirements-and-documentation) |
| [§3.6 architecture/guides/code docs](../../03-contract/prerelease_AGENTS.md#36-architecture-guides-and-code-documentation) | [arc42 and README](mechanisms/knowledge-and-documentation.md#arc42-shared-architectural-context-as-the-project-grows) and [Diátaxis and code documentation](mechanisms/knowledge-and-documentation.md#diátaxis-choosing-content-for-the-readers-need) | [BR10](../../01-behavior/deliverables/baseline.md#br10--affected-requirements-and-documentation) |
| [§3.7 reporting](../../03-contract/prerelease_AGENTS.md#37-reporting) | [Reporting and continued execution](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) | [BR7](../../01-behavior/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs) |
| [§3.8 instructions/protection/external actions](../../03-contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions) | [Why the bridges differ](delivery-and-portability.md#why-the-bridges-differ) | [BR3](../../01-behavior/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR8](../../01-behavior/deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority), [PR1](../../01-behavior/deliverables/baseline.md#established-product-requirement) |
| [§3.9 references](../../03-contract/prerelease_AGENTS.md#39-method-references) | [Principles and reference boundaries](methods-and-references.md#principles-and-reference-boundaries) | [PR1](../../01-behavior/deliverables/baseline.md#established-product-requirement) |
| [§4 composition](../../03-contract/prerelease_AGENTS.md#4-how-the-layers-compose) | [Three interacting layers](#three-interacting-layers) | [BR1](../../01-behavior/deliverables/baseline.md#br1--focused-proportionate-authorized-work), [BR3](../../01-behavior/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR6](../../01-behavior/deliverables/baseline.md#br6--learning-from-observed-results), [BR7](../../01-behavior/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs) |

## Context and Scope

[Delivery and portability](delivery-and-portability.md#context-and-scope) owns provider integration and instruction-loading boundaries. [Design goals and boundaries](#design-goals-and-boundaries) below retain the contract’s scope; [development-time and runtime authority](../../docs/authority-and-change.md#development-time-and-runtime-authority) owns repository applicability.

See [Why the bridges differ](delivery-and-portability.md#why-the-bridges-differ).

## Solution Strategy

### Design overview

#### Design goals and boundaries

The motivating risk is especially visible in a new or poorly documented project. Without established requirements, interfaces, decisions, and conventions, planning and autonomous design have fewer constraints. Even a bounded objective can permit a large amount of work. Small, meaningful increments limit the next commitment, while prior consultation reserves consequential architectural and lasting design direction for the requester unless the specific choice is already authorized. The absence of an established architecture does not confer unlimited design authority.

Small increments are the principal mechanism for controlling work and speculative token use. Developing detail only when needed avoids designing distant work before its decisions can be made. Before expanding planned work or starting another increment or attempt, cumulative reassessment connects the next step to evidence, the task objective, established direction, and limits. Bounded inquiries constrain effort spent on a blocking question even without announced effort allowances: sufficient evidence ends inquiry, and an increment's bounds require reassessment before further investigation. Plan–Do–Study–Act (PDSA) turns results into the next decision. Engineering practices protect quality, while documentation preserves facts and reasons so maintainers, users, and future agents can continue without reconstructing them. Adequate analysis, completeness, and validation constrain every effort-saving choice.

Reports consolidate unreported work at task completion, handoff, or when seeking requester input. The contract recommends minimizing routine progress reports and keeping intermediate communication concise and useful. The brief initial task outline precedes substantial work; material inquiry uncertainty and its significance must be made clear promptly unless already communicated in the request or task framing. These duties keep the requester aware without creating approval checkpoints or requiring an advance effort-limit announcement. Routine execution remains autonomous within authorization and direction; requester-imposed limits and consequential decisions retain their own consultation triggers. These mechanisms provide no token quota or guarantee of savings, and total consumption may remain substantial. The [practical explanation](../../03-contract/prerelease_README-powerusers.md#understanding-token-use) distinguishes reports from consumption measurements.

The contract is self-contained. Guides explain it and bridges help tools apply it; neither supplies hidden operating duties. Project facts, build commands, requirements, and architecture come from the adopting project's code and documentation. This separation supports reuse without embedding an application's design in generic instructions.

Requester instructions take priority within the tool's actual hierarchy and permissions. The tool determines discovery, scope, and precedence of directory instructions, which may add subtree rules only when compatible with the root contract. The contract cannot supply capabilities, enforce permissions, or override native approvals. Its protection of instruction files and its authorization rules for external actions keep those limits explicit. It also does not supply a complete product-development process, branching strategy, workflow engine, or framework tutorial. Established methods cannot invent missing requirements or requester authority.

- [Choosing or replacing methods](methods-and-references.md#choosing-or-replacing-methods)
- [Keeping the contract portable](delivery-and-portability.md#keeping-the-contract-portable)
- [Current wording trade-offs](delivery-and-portability.md#current-wording-trade-offs)

### Workflow design choices

#### Three interacting layers

The contract separates three questions that need answers throughout a task:

| Layer | Question it answers | Role in the design |
| --- | --- | --- |
| [Work cycle](../../03-contract/prerelease_AGENTS.md#1-work-cycle) | What is the agent doing with the current increment? | Organize planning, execution, assessment, and use of the findings. |
| [Progression guards](../../03-contract/prerelease_AGENTS.md#2-progression-guards) | May this work proceed, or is requester direction needed? | Check authority, scope, unresolved decisions, requester limits, cumulative reassessment, inquiry bounds, and permission to continue. |
| [Triggered rules](../../03-contract/prerelease_AGENTS.md#3-triggered-rules) | Has something happened that creates a duty or permission? | Apply the relevant rule when, for example, a requirement changes, a durable finding emerges, documentation is affected, or a report becomes due. Each rule retains its own strength and conditions. |

The same action can involve all three. While planning an authorized importer change, the agent might discover a material, durable parser limitation and propose changing the parser's established error contract. Planning identifies the issue, the record rule preserves the finding, and the consultation guard requires requester direction before adopting or implementing that departure unless specifically authorized. Naming a cycle phase settles neither the record duty nor decision authority.

The division follows how these concerns behave. Authorization, limits, and requester involvement can matter in any phase, and a durable finding can emerge while planning as easily as while acting. Placing such rules inside one phase would suggest they apply only there, or require readers to reinterpret earlier phases after reaching later material. Presenting the cycle first shows the ordinary path; the guards then make the control state explicit; triggered rules stay independent of phase.

The current [composition rule](../../03-contract/prerelease_AGENTS.md#4-how-the-layers-compose) starts at Plan, applies progression guards whenever work would advance or a relevant decision is due, and applies each triggered rule whenever its trigger occurs. After Study and Act, the applicable outcome is:

| State | Prescribed next action |
| --- | --- |
| Task done | Complete and report. |
| Stopping before task completion | Hand off with a handoff report. |
| A guard or other rule requires requester direction, or no existing authorization covers another increment | Report and await direction. |
| Otherwise | Return to Plan for the next authorized increment, with proportionate intermediate communication. |

No layer grants authorization by itself. A next cycle step, a satisfied guard, or a fulfilled duty never extends what the requester and tool permit, and completing an increment, reporting, recording a decision, discovering a finding, or exhausting an inquiry creates none. Guards are not additional phases; triggered duties authorize no otherwise unauthorized work, and triggered permissions authorize nothing beyond their terms.

This organization expresses design intent: making the operating model and its cross-cutting relationships explicit while preserving normative behavior. The repository holds no measurement showing that it improves human comprehension, agent adherence, or token use.

## Crosscutting Concepts

The following topic index links directly to each mechanism’s canonical explanation:

- [Small commitments with sufficient depth](mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth)
- [Learning throughout the work](mechanisms/work-cycle-and-inquiry.md#learning-throughout-the-work)
- [Completion, predictions, and bounded investigation](mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation)
- [Authorization and requester decisions](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions)
- [Reporting and continued execution](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution)
- [Engineering scope boundaries](mechanisms/engineering-and-validation.md#engineering-scope-boundaries)
- [Simple Design: choosing what the current solution needs](mechanisms/engineering-and-validation.md#simple-design-choosing-what-the-current-solution-needs)
- [DRY: keeping knowledge consistent as work progresses](mechanisms/knowledge-and-documentation.md#dry-keeping-knowledge-consistent-as-work-progresses)
- [Component boundaries, refactoring, and validation](mechanisms/engineering-and-validation.md#component-boundaries-refactoring-and-validation)
- [Validation and test evidence](mechanisms/engineering-and-validation.md#validation-and-test-evidence)
- [Focused techniques and how they work together](mechanisms/engineering-and-validation.md#focused-techniques-and-how-they-work-together)
- [Documentation choices](mechanisms/knowledge-and-documentation.md#documentation-choices)
- [arc42: shared architectural context as the project grows](mechanisms/knowledge-and-documentation.md#arc42-shared-architectural-context-as-the-project-grows)
- [EARS: making required behavior explicit](mechanisms/knowledge-and-documentation.md#ears-making-required-behavior-explicit)
- [ADRs: preserving the reasons for lasting choices](mechanisms/knowledge-and-documentation.md#adrs-preserving-the-reasons-for-lasting-choices)
- [Recording technical debt](mechanisms/knowledge-and-documentation.md#recording-technical-debt)
- [Diátaxis: choosing content for the reader's need](mechanisms/knowledge-and-documentation.md#diátaxis-choosing-content-for-the-readers-need)
- [Principles and reference boundaries](methods-and-references.md#principles-and-reference-boundaries)

## Runtime View

[Work cycle and inquiry](mechanisms/work-cycle-and-inquiry.md#runtime-view) owns the complete [worked CSV task example](mechanisms/work-cycle-and-inquiry.md#how-the-design-works-in-a-task).

## Architecture Decisions

[Decisions and alternatives](../docs/decisions-and-alternatives.md#architecture-decisions) owns the complete records and [approved structural successor](../docs/decisions-and-alternatives.md#contract-design-documentation-extraction-15-november-2026).
