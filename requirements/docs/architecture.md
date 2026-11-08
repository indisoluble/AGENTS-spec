# AGENTS.md contract architecture

This requirements-domain document explains the architecture of the reusable [AGENTS.md](../../contract/prerelease_AGENTS.md) operating instructions: its design goals and boundaries, interacting layers, and continuation behavior. It owns the material transferred from the [design overview and workflow design choices](contract-design.md#design-overview). The [engineering-system architecture](../../docs/architecture.md) owns AGENTS-spec repository relationships and development authority; an adopting application's architecture belongs to that project. This document adds no development-pipeline stage.

**Status: current binding design, with rationale and historical context distinguished.** Selected mechanisms and their rationale are distinct from independently accepted enduring product requirements. [product-requirements.md](product-requirements.md) owns established objectives, PR1, and product constraints; [requirement-candidates.md](requirement-candidates.md) owns provisional RC1–RC10 and unresolved acceptance questions. [Classification and evidence](contract-design.md#classification-and-evidence) and [design choices](contract-design.md#design-choices) retain the shared status distinctions and current design's authority and revision qualifications. This document adds no operating duties beyond the delivered contract.

Following the [selected arc42 approach](contract-design.md#arc42-shared-architectural-context-as-the-project-grows), [Design overview](#design-overview) supplies the **Solution Strategy**, and [Workflow design choices](#workflow-design-choices) supplies the **Runtime View** of layer interaction and continuation. The remaining current semantics, detailed mechanisms, rationale, decisions, history, and assessment scenarios stay in [contract-design.md](contract-design.md).

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
