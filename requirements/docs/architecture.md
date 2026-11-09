# AGENTS.md contract architecture

This requirements-domain document explains the architecture of the reusable [AGENTS.md](../../contract/prerelease_AGENTS.md) operating instructions: its design goals and boundaries, interacting layers, continuation behavior, bounded-work design, PDSA learning design, and shared current-semantics vocabulary and contract-clause coverage index. It owns the material transferred from the [design overview and workflow design choices](contract-design.md#design-overview) and [current-semantics vocabulary and coverage](contract-design.md#current-semantics-vocabulary-and-coverage). The [engineering-system architecture](../../docs/architecture.md) owns AGENTS-spec repository relationships and development authority; an adopting application's architecture belongs to that project. This document adds no development-pipeline stage.

**Status: current binding design, with rationale and historical context distinguished.** Selected mechanisms and their rationale are distinct from independently accepted enduring product requirements. [product-requirements.md](product-requirements.md) owns established objectives, PR1, and product constraints; [requirement-candidates.md](requirement-candidates.md) owns provisional RC1–RC10 and unresolved acceptance questions. [Classification and evidence](contract-design.md#classification-and-evidence) and [design choices](contract-design.md#design-choices) retain the shared status distinctions and current design's authority and revision qualifications. This document adds no operating duties beyond the delivered contract.

Following the [selected arc42 approach](contract-design.md#arc42-shared-architectural-context-as-the-project-grows), [Current-semantics vocabulary and coverage](#current-semantics-vocabulary-and-coverage) supplies shared terminology and navigation under **Glossary and Crosscutting Concepts**, [Design overview](#design-overview) supplies the **Solution Strategy**, and [Workflow design choices](#workflow-design-choices) supplies the **Runtime View** of layer interaction, continuation, and bounded work. The remaining current semantics, detailed mechanisms, rationale, decisions, history, and assessment scenarios stay in [contract-design.md](contract-design.md).

### Current-semantics vocabulary and coverage

Unless another actor is explicit, the agent is the subject of operating duties, recommendations, prohibitions, and permissions below. Uppercase keywords retain [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) / [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) meanings: MUST is mandatory, MUST NOT prohibits, SHOULD and SHOULD NOT are recommendations whose departures need weighed consequences and justification, and MAY permits within its stated terms. Unqualified operative language retains its source meaning; explanatory prose does not change a prescription's strength. Material SHOULD exceptions also need report explanations. No recommendation exception waives a mandatory rule.

| Term | Current meaning |
| --- | --- |
| Task objective | The requested overall outcome. |
| Increment | A small, useful, bounded step, including investigation, normally understandable, reviewable, and verifiable alone. The non-standalone case has [explicit coherence and recovery duties](#small-commitments-with-sufficient-depth). |
| Increment objective | The increment's bounded outcome toward the task objective. |
| Acceptance conditions | Observable criteria for completing the current increment; stating them does not automatically establish system requirements. |
| Handoff | Stopping before task completion and passing unfinished work to the requester or another person or agent. |
| Material | Significantly affecting correctness, scope, risk, or whether to proceed. |
| Permanent record | The canonical project document owning the topic, such as architecture or an ADR; chat and working notes are excluded. |

The following index assigns current-semantic detail within this contract architecture and the remaining [design choices](contract-design.md#design-choices). Contract clause references provide traceability; all operating detail is specified in these engineering sources. All rows remain subject to requester and tool authority, the progression guards, and each rule's own conditions. This is current contract-clause traceability, not proof of accepted product-requirement coverage or evaluation coverage.

| Contract clauses | Engineering specification locations |
| --- | --- |
| Purpose, model, terms | [Established objectives](product-requirements.md#established-objectives), this vocabulary, and [three interacting layers](#three-interacting-layers) |
| §1; §1.1 Plan | [Small commitments](#small-commitments-with-sufficient-depth), [learning](#learning-throughout-the-work), [completion and inquiry](contract-design.md#completion-predictions-and-bounded-investigation), [knowledge roles](contract-design.md#documentation-choices), and [initial framing](contract-design.md#reporting-and-continued-execution) |
| §1.2 Do | [Engineering choices](contract-design.md#engineering-choices), including Simple Design, preservation, and qualified techniques |
| §1.3 Study; §1.4 Act | [Completion and predictions](contract-design.md#completion-predictions-and-bounded-investigation), [validation and tests](contract-design.md#validation-and-test-evidence), [learning](#learning-throughout-the-work), and [composition](#three-interacting-layers) |
| §2.1 Authority; §2.2 decisions | [Decision factors](#small-commitments-with-sufficient-depth) and [authorization and requester decisions](contract-design.md#authorization-and-requester-decisions) |
| §2.3 effort/limits; §2.5 continuation | [Quality and bounds](#small-commitments-with-sufficient-depth), [authorization and continuation](contract-design.md#authorization-and-requester-decisions), and [handoff/resumption](contract-design.md#reporting-and-continued-execution) |
| §2.4 context/inquiry | [Completion, predictions, and bounded investigation](contract-design.md#completion-predictions-and-bounded-investigation) and [outcome reporting](contract-design.md#reporting-and-continued-execution) |
| §3.1 requirements | [Requirement boundary and revision](contract-design.md#completion-predictions-and-bounded-investigation) and [EARS forms](contract-design.md#ears-making-required-behavior-explicit) |
| §3.2 findings | [Assessment writes, durability, and permanent records](contract-design.md#authorization-and-requester-decisions) |
| §3.3 decisions; §3.4 debt | [ADRs](contract-design.md#adrs-preserving-the-reasons-for-lasting-choices) and [technical debt](contract-design.md#recording-technical-debt) |
| §3.5 canonical knowledge/affected docs | [DRY](contract-design.md#dry-keeping-knowledge-consistent-as-work-progresses) and [documentation synchronization](contract-design.md#documentation-choices) |
| §3.6 architecture/guides/code docs | [arc42 and README](contract-design.md#arc42-shared-architectural-context-as-the-project-grows) and [Diátaxis and code documentation](contract-design.md#diátaxis-choosing-content-for-the-readers-need) |
| §3.7 reporting | [Reporting and continued execution](contract-design.md#reporting-and-continued-execution) |
| §3.8 instructions/protection/external actions | [Why the bridges differ](contract-design.md#why-the-bridges-differ) |
| §3.9 references | [Principles and reference boundaries](contract-design.md#principles-and-reference-boundaries) |
| §4 composition | [Three interacting layers](#three-interacting-layers) |

### Design overview

#### Design goals and boundaries

The motivating risk is especially visible in a new or poorly documented project. Without established requirements, interfaces, decisions, and conventions, planning and autonomous design have fewer constraints. Even a bounded objective can permit a large amount of work. Small, meaningful increments limit the next commitment, while prior consultation reserves consequential architectural and lasting design direction for the requester unless the specific choice is already authorized. The absence of an established architecture does not confer unlimited design authority.

Small increments are the principal mechanism for controlling work and speculative token use. Developing detail only when needed avoids designing distant work before its decisions can be made. Before expanding planned work or starting another increment or attempt, cumulative reassessment connects the next step to evidence, the task objective, established direction, and limits. Bounded inquiries constrain effort spent on a blocking question even without announced effort allowances: sufficient evidence ends inquiry, and an increment's bounds require reassessment before further investigation. Plan–Do–Study–Act (PDSA) turns results into the next decision. Engineering practices protect quality, while documentation preserves facts and reasons so maintainers, users, and future agents can continue without reconstructing them. Adequate analysis, completeness, and validation constrain every effort-saving choice.

Reports consolidate unreported work at task completion, handoff, or when seeking requester input. The contract recommends minimizing routine progress reports and keeping intermediate communication concise and useful. The brief initial task outline precedes substantial work; material inquiry uncertainty and its significance must be made clear promptly unless already communicated in the request or task framing. These duties keep the requester aware without creating approval checkpoints or requiring an advance effort-limit announcement. Routine execution remains autonomous within authorization and direction; requester-imposed limits and consequential decisions retain their own consultation triggers. These mechanisms provide no token quota or guarantee of savings, and total consumption may remain substantial. The [practical explanation](../../contract/prerelease_README-powerusers.md#understanding-token-use) distinguishes reports from consumption measurements.

The contract is self-contained. Guides explain it and bridges help tools apply it; neither supplies hidden operating duties. Project facts, build commands, requirements, and architecture come from the adopting project's code and documentation. This separation supports reuse without embedding an application's design in generic instructions.

Requester instructions take priority within the tool's actual hierarchy and permissions. The tool determines discovery, scope, and precedence of directory instructions, which may add subtree rules only when compatible with the root contract. The contract cannot supply capabilities, enforce permissions, or override native approvals. Its protection of instruction files and its authorization rules for external actions keep those limits explicit. It also does not supply a complete product-development process, branching strategy, workflow engine, or framework tutorial. Established methods cannot invent missing requirements or requester authority.

### Workflow design choices

#### Three interacting layers

The contract separates three questions that need answers throughout a task:

| Layer | Question it answers | Role in the design |
| --- | --- | --- |
| [Work cycle](../../contract/prerelease_AGENTS.md#1-work-cycle) | What is the agent doing with the current increment? | Organize planning, execution, assessment, and use of the findings. |
| [Progression guards](../../contract/prerelease_AGENTS.md#2-progression-guards) | May this work proceed, or is requester direction needed? | Check authority, scope, unresolved decisions, requester limits, cumulative reassessment, inquiry bounds, and permission to continue. |
| [Triggered rules](../../contract/prerelease_AGENTS.md#3-triggered-rules) | Has something happened that creates a duty or permission? | Apply the relevant rule when, for example, a requirement changes, a durable finding emerges, documentation is affected, or a report becomes due. Each rule retains its own strength and conditions. |

The same action can involve all three. While planning an authorized importer change, the agent might discover a material, durable parser limitation and propose changing the parser's established error contract. Planning identifies the issue, the record rule preserves the finding, and the consultation guard requires requester direction before adopting or implementing that departure unless specifically authorized. Naming a cycle phase settles neither the record duty nor decision authority.

The division follows how these concerns behave. Authorization, limits, and requester involvement can matter in any phase, and a durable finding can emerge while planning as easily as while acting. Placing such rules inside one phase would suggest they apply only there, or require readers to reinterpret earlier phases after reaching later material. Presenting the cycle first shows the ordinary path; the guards then make the control state explicit; triggered rules stay independent of phase.

The current [composition rule](../../contract/prerelease_AGENTS.md#4-how-the-layers-compose) starts at Plan, applies progression guards whenever work would advance or a relevant decision is due, and applies each triggered rule whenever its trigger occurs. After Study and Act, the applicable outcome is:

| State | Prescribed next action |
| --- | --- |
| Task done | Complete and report. |
| Stopping before task completion | Hand off with a handoff report. |
| A guard or other rule requires requester direction, or no existing authorization covers another increment | Report and await direction. |
| Otherwise | Return to Plan for the next authorized increment, with proportionate intermediate communication. |

No layer grants authorization by itself. A next cycle step, a satisfied guard, or a fulfilled duty never extends what the requester and tool permit, and completing an increment, reporting, recording a decision, discovering a finding, or exhausting an inquiry creates none. Guards are not additional phases; triggered duties authorize no otherwise unauthorized work, and triggered permissions authorize nothing beyond their terms.

This organization expresses design intent: making the operating model and its cross-cutting relationships explicit while preserving normative behavior. The repository holds no measurement showing that it improves human comprehension, agent adherence, or token use.

#### Small commitments with sufficient depth

The requester supplies goals, permission, and relevant constraints. The agent supplies decomposition, acceptance conditions, proportionate planning, validation, cumulative reassessment, and recognition of required consultation. These standing responsibilities let an ordinary outcome-oriented request start useful work without requiring the requester to monitor tokens or supervise every correction. A requester may still select a step or add review points.

Within Plan, increment selection connects the requested outcome and permission with current behavior, relevant dependencies, and available evidence. From the request and project evidence, the agent MUST define four elements for the next increment: its **objective**, **acceptance conditions**, **approach**, and **prediction** (the expected result of that approach or experiment). It MUST identify task and increment objectives, permitted work, constraints, the current abstraction level (for example, architecture or function), and requirements or acceptance conditions already set by the requester or authoritative project sources. Before choosing the approach or deriving or refining acceptance conditions, it MUST inspect relevant code and callers, tests, configuration, and canonical documentation. The [context/inquiry distinction](contract-design.md#completion-predictions-and-bounded-investigation) also classifies directly related dependency inspection and every reading of existing project documents as context gathering.

Work MUST stay within the authorized increment, defaulting to the smallest useful next one, including in planning and approval workflows. Each increment or subdivision MUST address one concern unless the concerns are inseparable. Its scope includes affected artifacts and checks. When blocking uncertainty prevents a sound implementation choice, obtaining bounded evidence can itself be the useful result.

For the next decision, the agent MUST assess the [four decision factors](../../contract/prerelease_AGENTS.md#22-decisions-and-requester-interaction): **scope** (necessary versus authorized work); **uncertainty** (missing or conflicting evidence affecting the approach or acceptance); **consequence** (effects on core or public behavior, architecture, compatibility, security, data, operations, cost, and future options); and **reversibility** (difficulty of restoration, including migrations and external effects). Scope can include affected behavior, artifacts, dependencies, and system boundaries. A few changed lines can affect many callers or an irreversible migration. Understood, narrow, low-impact, easily reversible changes SHOULD receive brief inspection, action, and validation without unnecessary plans or records. Reporting follows its own triggers and remains proportionate.

These criteria constrain selection without prescribing a numeric score, an exhaustive comparison of possible increments, or a uniquely correct sequence. Requiring a complete ranking or detailed backlog before starting would expand the initial planning commitment. The design instead calls for enough reasoning to support the next useful step and uses its evidence to refine later work. This contributes to the token-control goal while preserving the analysis and validation needed for a complete result.

The agent MUST reason enough for the next decision at the current abstraction level and keep later work at outline level. Detail MUST reflect uncertainty, consequence, risk, reversibility, and how soon work starts. Architecture analysis may need careful examination of boundaries, alternatives, and risks without specifying every future API or function. A limited experiment or implementation SHOULD replace speculation when it gives better evidence. Explicit authorization can cover broader analysis at the relevant abstraction level.

Completeness is assessed within the increment's scope. Evidence, enabling infrastructure, or migration groundwork can be useful results as well as functionality. At review boundaries—review, handoff, or a deliberate pause after a meaningful step—work MUST be coherent. Before an increment that cannot stand alone, the agent MUST explain why, what stays usable or testable, and how to undo it. Changes SHOULD be easy to undo, minimizing irreversible effects and preparing recovery or harm mitigation; the agent MUST report material limits on undoing proposed or completed changes. Recovery reduces the cost of a mistaken approach; it grants no permission for destructive effects. Required stops MAY leave work incomplete, while review-boundary coherence still applies. A small scope cannot excuse shallow reasoning, omitted dependencies, or incomplete work presented as finished.

Under [§2.3](../../contract/prerelease_AGENTS.md#23-effort-estimates-and-requester-limits), correctness, completeness, consistency, and adequate reasoning, implementation, and validation MUST precede saving lines, files, or tokens and context. Among workable solutions, clarity, canonical ownership, and reversibility SHOULD precede fewer parts. These priorities apply cumulatively, including to decomposition and repeated attempts; compactness is not a reason to leave required work out.

#### Learning throughout the work

The [Deming Institute's PDSA account](https://deming.org/explore/pdsa/) connects an approach and expected result with observation and the next decision. Small increments bound commitments; PDSA's contribution is learning which approach remains suitable and what to do next. Passing tests alone does not establish that learning role: the implications still inform Act and subsequent planning.

The agent MUST apply the contract's [PDSA work cycle](../../contract/prerelease_AGENTS.md#1-work-cycle) proportionally to implementation, investigation, and documentation: Plan the next small authorized increment from context and objectives, Do it, Study the results, and Act on the findings. Plan starts with the request and includes context gathering, the overall objective and permitted work, the [four increment elements](#small-commitments-with-sufficient-depth), and selection of the next increment. Study assesses completion and observations; Act uses those findings to retain, revise, or discard the approach and retains learning for Plan. Act also applies the triggered record rules for durable findings, significant decisions, or technical debt, then follows the [composition outcomes](#three-interacting-layers). Results can reshape later detail without changing the agreed outcome or granting more authority.

Terms and the layer overview precede the work cycle. Methods appear near their principal contribution—engineering practices in Do, validation in Study, and documentation and decision methods among the triggered rules—but apply whenever triggered in any phase, and the progression guards apply throughout. Tests can be planned before implementation; decisions and documentation are maintained as facts emerge. Phases may overlap or repeat. Methods alone require no deliverable; routine work needs no worksheet, formal experiment, or special mode. Separate phase reports are not required; reporting has its own triggers.

PDSA's Plan phase organizes reasoning. A tool's Plan mode has its own proposal and approval procedures. Neither expands authorization. These distinctions let the workflow apply proportionally to implementation, investigation, and documentation without inventing separate mandatory deliverables.
