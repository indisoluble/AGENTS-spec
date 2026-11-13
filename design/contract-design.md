# AGENTS.md contract architecture

This design document explains the architecture of the reusable [AGENTS.md](../contract/prerelease_AGENTS.md) operating instructions: its provider integration and instruction loading, design goals and boundaries, interacting layers, continuation behavior, bounded-work design, PDSA learning design, completion and prediction distinctions, bounded-inquiry design, authorization and requester decisions, reporting and continued execution, Simple Design, DRY, component boundaries, refactoring, validation, focused techniques, arc42 documentation design, EARS requirements-writing design, ADR-writing design, technical-debt recording, Diátaxis documentation design, method-selection and portability rationale, current wording trade-offs, shared current-semantics vocabulary and contract-clause coverage index, selected contract-design decisions, historical alternatives, method-reference semantics and source assignments, and links to the companion non-normative design-review scenarios. The [engineering-system architecture](../docs/architecture.md) owns AGENTS-spec repository relationships, development authority, and shared status and evidence boundaries; an adopting application's architecture belongs to that project. This document adds no development-pipeline stage.

**Status: current binding design, with rationale, historical context, and non-normative design reference distinguished.** Selected mechanisms and their rationale are distinct from independently accepted enduring product requirements. [baseline.md](../behavior/baseline.md) owns established objectives, PR1, and product constraints; [discovery.md](../behavior/discovery.md) owns provisional RC1–RC10 and unresolved acceptance questions. [Status and evidence boundaries](../docs/architecture.md#status-and-evidence-boundaries) retains the shared status distinctions and current design's authority and revision qualifications. This document adds no operating duties beyond the delivered contract.

The global [Status and evidence boundaries](../docs/architecture.md#status-and-evidence-boundaries) section explains the authority of documented statements before the design views. Following the [selected arc42 approach](#arc42-shared-architectural-context-as-the-project-grows), **[Glossary](#glossary)** contains [Current-semantics vocabulary and coverage](#current-semantics-vocabulary-and-coverage) for shared terminology and contract-clause coverage. **[Context and Scope](#context-and-scope)** explains provider integration and instruction-loading boundaries. **[Solution Strategy](#solution-strategy)** contains [Design overview](#design-overview) and [Workflow design choices](#workflow-design-choices): the design goals and boundaries, three interacting layers, their composition and continuation outcomes, [method selection](#choosing-or-replacing-methods), [portability rationale](#keeping-the-contract-portable), and [current wording trade-offs](#current-wording-trade-offs). **[Crosscutting Concepts](#crosscutting-concepts)** contains the reusable bounded-work, learning, completion and prediction, bounded-inquiry, authorization, requester-decision, reporting, record, communication, and continuity mechanisms that apply across phases, and the [engineering scope boundaries](#engineering-scope-boundaries), [Simple Design](#simple-design-choosing-what-the-current-solution-needs), [DRY](#dry-keeping-knowledge-consistent-as-work-progresses), [component boundaries, refactoring, and validation](#component-boundaries-refactoring-and-validation), [validation and test evidence](#validation-and-test-evidence), [focused techniques](#focused-techniques-and-how-they-work-together), [arc42 documentation design](#arc42-shared-architectural-context-as-the-project-grows), [EARS requirements-writing](#ears-making-required-behavior-explicit), [ADR-writing](#adrs-preserving-the-reasons-for-lasting-choices), [technical-debt recording](#recording-technical-debt), and [Diátaxis](#diátaxis-choosing-content-for-the-readers-need) design explanations, followed by [Principles and reference boundaries](#principles-and-reference-boundaries) for current method-reference semantics and source assignments. **[Runtime View](#runtime-view)** contains the [worked task example](#how-the-design-works-in-a-task), illustrating the design's behavior through the CSV-import Plan–Do–Study–Act sequence. **[Architecture Decisions](#architecture-decisions)** contains the [selected-design/status index](#selected-design-and-retained-decisions), [historical source and interpretation](#historical-source-and-interpretation), and four superseded-mechanism explanations. The companion **[Design Reference](design-review.md#design-reference)** contains all 28 non-normative [assessment scenarios](design-review.md#assessing-design-changes), pending later requirements-led review.

## Glossary

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

The following index assigns current-semantic detail within this contract architecture. Contract clause references provide traceability; all operating detail is specified here. All rows remain subject to requester and tool authority, the progression guards, and each rule's own conditions. This is current contract-clause traceability, not proof of accepted product-requirement coverage or evaluation coverage.

| Contract clauses | Engineering specification locations |
| --- | --- |
| Purpose, model, terms | [Established objectives](../behavior/baseline.md#established-objectives), this vocabulary, and [three interacting layers](#three-interacting-layers) |
| §1; §1.1 Plan | [Small commitments](#small-commitments-with-sufficient-depth), [learning](#learning-throughout-the-work), [completion and inquiry](#completion-predictions-and-bounded-investigation), [knowledge roles](#documentation-choices), and [initial framing](#reporting-and-continued-execution) |
| §1.2 Do | [Engineering scope boundaries](#engineering-scope-boundaries), [Simple Design](#simple-design-choosing-what-the-current-solution-needs), [component boundaries, refactoring, and validation](#component-boundaries-refactoring-and-validation), [qualified techniques](#focused-techniques-and-how-they-work-together) |
| §1.3 Study; §1.4 Act | [Completion and predictions](#completion-predictions-and-bounded-investigation), [validation and tests](#validation-and-test-evidence), [learning](#learning-throughout-the-work), and [composition](#three-interacting-layers) |
| §2.1 Authority; §2.2 decisions | [Decision factors](#small-commitments-with-sufficient-depth) and [authorization and requester decisions](#authorization-and-requester-decisions) |
| §2.3 effort/limits; §2.5 continuation | [Quality and bounds](#small-commitments-with-sufficient-depth), [authorization and continuation](#authorization-and-requester-decisions), and [handoff/resumption](#reporting-and-continued-execution) |
| §2.4 context/inquiry | [Completion, predictions, and bounded investigation](#completion-predictions-and-bounded-investigation) and [outcome reporting](#reporting-and-continued-execution) |
| §3.1 requirements | [Requirement boundary and revision](#completion-predictions-and-bounded-investigation) and [EARS forms](#ears-making-required-behavior-explicit) |
| §3.2 findings | [Assessment writes, durability, and permanent records](#authorization-and-requester-decisions) |
| §3.3 decisions; §3.4 debt | [ADRs](#adrs-preserving-the-reasons-for-lasting-choices) and [technical debt](#recording-technical-debt) |
| §3.5 canonical knowledge/affected docs | [DRY](#dry-keeping-knowledge-consistent-as-work-progresses) and [documentation synchronization](#documentation-choices) |
| §3.6 architecture/guides/code docs | [arc42 and README](#arc42-shared-architectural-context-as-the-project-grows) and [Diátaxis and code documentation](#diátaxis-choosing-content-for-the-readers-need) |
| §3.7 reporting | [Reporting and continued execution](#reporting-and-continued-execution) |
| §3.8 instructions/protection/external actions | [Why the bridges differ](#why-the-bridges-differ) |
| §3.9 references | [Principles and reference boundaries](#principles-and-reference-boundaries) |
| §4 composition | [Three interacting layers](#three-interacting-layers) |

## Context and Scope

This view describes provider integration and instruction-loading boundaries for the delivered consumer contract. AGENTS-spec development authority, instruction loading, and the scoped adoption of engineering practices remain defined by the [engineering-system architecture](../docs/architecture.md#development-time-and-runtime-authority); these consumer-contract rules are not automatically adopted for repository development.

### Why the bridges differ

The provider explanations here retain their existing source provenance; the [recorded evidence dates](../contract/prerelease_README-powerusers.md#evidence-dates) still apply, and this restructuring does not refresh them. Actual support needs checking in the adopting environment.

Both bridges apply the same local contract through their tool's instruction mechanisms. [CLAUDE.md](../contract/prerelease_CLAUDE.md) uses `@AGENTS.md`, Claude Code's [native import syntax](https://code.claude.com/docs/en/memory#import-additional-files), to include the referenced content. The single line can therefore perform its loading role.

[Copilot support](https://docs.github.com/en/copilot/reference/custom-instructions-support) varies by interface. A Markdown link identifies a file but is not a universal import mechanism. The supplied bridge explicitly directs reading and following the local contract within the actual hierarchy and permissions. Neither supplied bridge defines independent behavior for a failure to load the contract. The contract cannot govern an agent that never received it, so the package supplies no common stop/report/resume protocol for that case. Actual tool and requester instructions govern the situation. The [practical compatibility guidance](../contract/prerelease_README-powerusers.md#tool-compatibility) explains this limitation and adoption diagnostics; it adds no fallback operating policy.

The [current instruction rule](../contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions) assigns **two different scopes**:

| Scope | Current prescription |
| --- | --- |
| Canonical contract | Root `AGENTS.md` MUST own the canonical repository-wide contract. |
| Two bridges only | Root `CLAUDE.md` and root-relative `.github/copilot-instructions.md` MUST only discover and apply that contract, optionally with non-policy titles or provenance. `AGENTS.md` is not a bridge. |
| Three protected files | `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` MUST be edited only on explicit request for the file or instructions; applying file-specific recommendations counts. Necessary edits to the other two MAY accompany that request. Other affected documents follow the ordinary canonical-knowledge and synchronization rules. These instruction-file edits MUST stay separate from unrelated work. |

Directory instructions MAY add subtree rules only if contract-compatible. The actual tool sets discovery, scope, and precedence; that precedence never makes conflicting policy acceptable, and the agent MUST report conflicts. Compatibility is a content rule, not an invented precedence mechanism. Adoption guidance therefore calls for human validation of which existing practices, conventions, and workflows persist, following the [basic installation precautions](../contract/prerelease_README.md#get-started); that guidance is not an extra runtime rule. Project facts and operating rules have different owners.

If uncertainty about loading, scope, or precedence could affect the task, the agent SHOULD check available diagnostics and relevant instruction files; it MUST report what was checked and remaining material uncertainty. Tool limits blocking instruction loading also require the [tool-limit disclosure](#reporting-and-continued-execution). Diagnostic inspection and demonstrated application are different evidence, and these rules add no bootstrap protocol for a contract that was never loaded.

External actions—commits, publishing or sending, or changes to remote or shared state—MUST be authorized. Read-only access follows task scope and tool permissions. Neither documentation duties nor an instruction-file edit request independently authorizes an external action.

Discovery, inclusion, precedence, and application are distinct. [VS Code's conflict guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#_resolve-conflicting-instructions), its [instruction settings](https://code.visualstudio.com/docs/agents/reference/ai-settings#_custom-instructions-settings), and [GitHub.com's precedence guidance](https://docs.github.com/en/copilot/concepts/prompting/response-customization#precedence-of-custom-instructions) describe different aspects. File order or a link alone cannot establish all four. The [adoption checks](../contract/prerelease_README-powerusers.md#check-adoption) and [recorded evidence dates](../contract/prerelease_README-powerusers.md#evidence-dates) qualify the integration guidance; exact settings and support depend on the provider's documentation and the actual environment.

The Copilot title and header identify the associated release and upstream origin. Its release date and source URL match `AGENTS.md`. Metadata adds no policy authority, and the adopted local contract remains canonical. Permitting provenance does not require a header on the one-line Claude import. Minimality preserves each bridge's loading and application role.

## Solution Strategy

### Design overview

#### Design goals and boundaries

The motivating risk is especially visible in a new or poorly documented project. Without established requirements, interfaces, decisions, and conventions, planning and autonomous design have fewer constraints. Even a bounded objective can permit a large amount of work. Small, meaningful increments limit the next commitment, while prior consultation reserves consequential architectural and lasting design direction for the requester unless the specific choice is already authorized. The absence of an established architecture does not confer unlimited design authority.

Small increments are the principal mechanism for controlling work and speculative token use. Developing detail only when needed avoids designing distant work before its decisions can be made. Before expanding planned work or starting another increment or attempt, cumulative reassessment connects the next step to evidence, the task objective, established direction, and limits. Bounded inquiries constrain effort spent on a blocking question even without announced effort allowances: sufficient evidence ends inquiry, and an increment's bounds require reassessment before further investigation. Plan–Do–Study–Act (PDSA) turns results into the next decision. Engineering practices protect quality, while documentation preserves facts and reasons so maintainers, users, and future agents can continue without reconstructing them. Adequate analysis, completeness, and validation constrain every effort-saving choice.

Reports consolidate unreported work at task completion, handoff, or when seeking requester input. The contract recommends minimizing routine progress reports and keeping intermediate communication concise and useful. The brief initial task outline precedes substantial work; material inquiry uncertainty and its significance must be made clear promptly unless already communicated in the request or task framing. These duties keep the requester aware without creating approval checkpoints or requiring an advance effort-limit announcement. Routine execution remains autonomous within authorization and direction; requester-imposed limits and consequential decisions retain their own consultation triggers. These mechanisms provide no token quota or guarantee of savings, and total consumption may remain substantial. The [practical explanation](../contract/prerelease_README-powerusers.md#understanding-token-use) distinguishes reports from consumption measurements.

The contract is self-contained. Guides explain it and bridges help tools apply it; neither supplies hidden operating duties. Project facts, build commands, requirements, and architecture come from the adopting project's code and documentation. This separation supports reuse without embedding an application's design in generic instructions.

Requester instructions take priority within the tool's actual hierarchy and permissions. The tool determines discovery, scope, and precedence of directory instructions, which may add subtree rules only when compatible with the root contract. The contract cannot supply capabilities, enforce permissions, or override native approvals. Its protection of instruction files and its authorization rules for external actions keep those limits explicit. It also does not supply a complete product-development process, branching strategy, workflow engine, or framework tutorial. Established methods cannot invent missing requirements or requester authority.

### Choosing or replacing methods

The method set was selected under the established [method-selection qualifications](../behavior/baseline.md#method-selection-qualifications), which own the criteria for additions and replacements and their revision conditions. Selected mechanisms are distinct from independently accepted enduring product requirements: [authorized redesign may reconsider them without making current prescriptions optional](../docs/architecture.md#status-and-evidence-boundaries).

[PDSA](#learning-throughout-the-work) and [Simple Design](#simple-design-choosing-what-the-current-solution-needs) were judged sufficient for the agreed design alongside the [focused engineering references](#focused-techniques-and-how-they-work-together), [documentation conventions](#documentation-choices), and [explicit collaboration rules](#authorization-and-requester-decisions). Additional umbrella frameworks were not needed to supply those responsibilities.

### Keeping the contract portable

The established [portability and standing-context qualifications](../behavior/baseline.md#portability-and-standing-context-qualifications) own the size target and its operative conditions. This section explains the design rationale and supporting provider evidence rather than independently defining those constraints.

The provider evidence supporting the choice below retains its recorded **2026-10-04** check date in the [evidence-date owner](../contract/prerelease_README-powerusers.md#evidence-dates). It has not been newly verified by this restructuring; applicable limits still depend on the actual provider and environment.

The target was informed by [Codex's documented default 32 KiB combined instruction limit](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance) and Anthropic's [guidance to keep `CLAUDE.md` concise and human-readable](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md). The approximate 24,000-byte figure is a project choice: it leaves room below Codex's default for directory instructions and other loaded instruction or configuration context, and reflects Claude Code's guidance on limiting standing context. Importing the contract through `CLAUDE.md` still [loads its contents into context](https://code.claude.com/docs/en/memory#import-additional-files). These sources are provider evidence for the design choice, not a universal ceiling or proof of actual provider compatibility; the canonical qualifications retain the distinctions concerning delivered files, other loaded instructions, tool configuration, clarity, and precision.

### Current wording trade-offs

Compact instructions reduce standing text while increasing the risk that readers must infer relationships. Ambiguity can cause clarification, reference consultation, or rework; a smaller contract does not establish lower total token use. Review these current treatments when editing:

| Treatment | Interpretation risk and review focus |
| --- | --- |
| Implicit agent subjects, short labels, and slash groups | Keep the actor, every duty, and the relationship between grouped actions clear. |
| Broad knowledge-ownership and permitted-copy categories | Ensure readers can recognize facts, schemas, requirements, rationale, invariants, procedures, conventions, tests, and examples under the appropriate rule. |
| Concise definitions, architecture topics, record fields, and reports | Preserve distinguishing meaning and conditions; matching a name or keyword alone is insufficient. |
| Layered organization with section cross-references | Each passage should make sense where it appears. A reference can point forward to details when the surrounding text explains the relevant concept or constraint; `permitted work (§2.1)` is one example. Where a bare reference would force readers to look ahead just to understand the current passage, supply enough local explanation, accepting useful brief repetition. Keep consequential conditions explicit; guards and triggered rules apply across phases, and placement must not restrict a rule to one phase or imply an extra phase. |
| Initial task outline and first increment | Preserve advance visibility of the overall direction and next objective and bounds after proportionate preliminary context gathering. Keep later work at outline level and distinguish the statement from an approval request. |
| Requester limits and consequential direction | Distinguish informal expectations from binding requester constraints. Material ambiguity needs clarification; new consequential design direction and material departures need prior consultation unless the specific choice is already authorized. Routine local corrections remain autonomous. |
| Purpose-based inquiry, awareness, and bounded conduct | Unknown data and prescribed procedures do not decide classification alone. Preserve context gathering, execution, validation, and inquiry as distinct activities. Promptly explaining material uncertainty and its significance differs from consulting on a consequential choice. No duplicate notification is needed when the request or task framing already communicates it. A declared allowance is not required, and announcing one cannot replace actual bounded work, evidence sufficiency, or reassessment before justified continuation. |
| Proportionate intermediate communication | Minimizing routine reports and keeping updates concise and useful are recommendations, not a categorical ban or a requirement for effort-audit messages. Consolidated reporting, initial framing, prompt inquiry notification, and disclosures before affected work retain their own triggers and strengths. |
| Reference links without per-rule numeric locators | The [exact assignments](#principles-and-reference-boundaries) preserve attribution; narrow consultation limits prevent the links from becoming open-ended research. |

These are interpretation risks, not additional operating rules or measured agent outcomes. The [canonical portability qualifications](../behavior/baseline.md#portability-and-standing-context-qualifications) retain the fidelity and self-containment constraints governing compression.

Acceptance of the current wording compromises covers only the identified trade-offs. It does not authorize further loss of precision. Any new trade-off, including reduced explicitness without an intended rule change, is a design decision to identify for requester review. Its rationale needs to record what becomes less explicit, where the operative meaning remains, and the likely interpretation or effort consequences. Previous acceptance and matching counts do not establish that a further reduction is lossless or behaviorally equivalent.

### Workflow design choices

#### Three interacting layers

The contract separates three questions that need answers throughout a task:

| Layer | Question it answers | Role in the design |
| --- | --- | --- |
| [Work cycle](../contract/prerelease_AGENTS.md#1-work-cycle) | What is the agent doing with the current increment? | Organize planning, execution, assessment, and use of the findings. |
| [Progression guards](../contract/prerelease_AGENTS.md#2-progression-guards) | May this work proceed, or is requester direction needed? | Check authority, scope, unresolved decisions, requester limits, cumulative reassessment, inquiry bounds, and permission to continue. |
| [Triggered rules](../contract/prerelease_AGENTS.md#3-triggered-rules) | Has something happened that creates a duty or permission? | Apply the relevant rule when, for example, a requirement changes, a durable finding emerges, documentation is affected, or a report becomes due. Each rule retains its own strength and conditions. |

The same action can involve all three. While planning an authorized importer change, the agent might discover a material, durable parser limitation and propose changing the parser's established error contract. Planning identifies the issue, the record rule preserves the finding, and the consultation guard requires requester direction before adopting or implementing that departure unless specifically authorized. Naming a cycle phase settles neither the record duty nor decision authority.

The division follows how these concerns behave. Authorization, limits, and requester involvement can matter in any phase, and a durable finding can emerge while planning as easily as while acting. Placing such rules inside one phase would suggest they apply only there, or require readers to reinterpret earlier phases after reaching later material. Presenting the cycle first shows the ordinary path; the guards then make the control state explicit; triggered rules stay independent of phase.

The current [composition rule](../contract/prerelease_AGENTS.md#4-how-the-layers-compose) starts at Plan, applies progression guards whenever work would advance or a relevant decision is due, and applies each triggered rule whenever its trigger occurs. After Study and Act, the applicable outcome is:

| State | Prescribed next action |
| --- | --- |
| Task done | Complete and report. |
| Stopping before task completion | Hand off with a handoff report. |
| A guard or other rule requires requester direction, or no existing authorization covers another increment | Report and await direction. |
| Otherwise | Return to Plan for the next authorized increment, with proportionate intermediate communication. |

No layer grants authorization by itself. A next cycle step, a satisfied guard, or a fulfilled duty never extends what the requester and tool permit, and completing an increment, reporting, recording a decision, discovering a finding, or exhausting an inquiry creates none. Guards are not additional phases; triggered duties authorize no otherwise unauthorized work, and triggered permissions authorize nothing beyond their terms.

This organization expresses design intent: making the operating model and its cross-cutting relationships explicit while preserving normative behavior. The repository holds no measurement showing that it improves human comprehension, agent adherence, or token use.

## Crosscutting Concepts

### Small commitments with sufficient depth

The requester supplies goals, permission, and relevant constraints. The agent supplies decomposition, acceptance conditions, proportionate planning, validation, cumulative reassessment, and recognition of required consultation. These standing responsibilities let an ordinary outcome-oriented request start useful work without requiring the requester to monitor tokens or supervise every correction. A requester may still select a step or add review points.

Within Plan, increment selection connects the requested outcome and permission with current behavior, relevant dependencies, and available evidence. From the request and project evidence, the agent MUST define four elements for the next increment: its **objective**, **acceptance conditions**, **approach**, and **prediction** (the expected result of that approach or experiment). It MUST identify task and increment objectives, permitted work, constraints, the current abstraction level (for example, architecture or function), and requirements or acceptance conditions already set by the requester or authoritative project sources. Before choosing the approach or deriving or refining acceptance conditions, it MUST inspect relevant code and callers, tests, configuration, and canonical documentation. The [context/inquiry distinction](#completion-predictions-and-bounded-investigation) also classifies directly related dependency inspection and every reading of existing project documents as context gathering.

Work MUST stay within the authorized increment, defaulting to the smallest useful next one, including in planning and approval workflows. Each increment or subdivision MUST address one concern unless the concerns are inseparable. Its scope includes affected artifacts and checks. When blocking uncertainty prevents a sound implementation choice, obtaining bounded evidence can itself be the useful result.

For the next decision, the agent MUST assess the [four decision factors](../contract/prerelease_AGENTS.md#22-decisions-and-requester-interaction): **scope** (necessary versus authorized work); **uncertainty** (missing or conflicting evidence affecting the approach or acceptance); **consequence** (effects on core or public behavior, architecture, compatibility, security, data, operations, cost, and future options); and **reversibility** (difficulty of restoration, including migrations and external effects). Scope can include affected behavior, artifacts, dependencies, and system boundaries. A few changed lines can affect many callers or an irreversible migration. Understood, narrow, low-impact, easily reversible changes SHOULD receive brief inspection, action, and validation without unnecessary plans or records. Reporting follows its own triggers and remains proportionate.

These criteria constrain selection without prescribing a numeric score, an exhaustive comparison of possible increments, or a uniquely correct sequence. Requiring a complete ranking or detailed backlog before starting would expand the initial planning commitment. The design instead calls for enough reasoning to support the next useful step and uses its evidence to refine later work. This contributes to the token-control goal while preserving the analysis and validation needed for a complete result.

The agent MUST reason enough for the next decision at the current abstraction level and keep later work at outline level. Detail MUST reflect uncertainty, consequence, risk, reversibility, and how soon work starts. Architecture analysis may need careful examination of boundaries, alternatives, and risks without specifying every future API or function. A limited experiment or implementation SHOULD replace speculation when it gives better evidence. Explicit authorization can cover broader analysis at the relevant abstraction level.

Completeness is assessed within the increment's scope. Evidence, enabling infrastructure, or migration groundwork can be useful results as well as functionality. At review boundaries—review, handoff, or a deliberate pause after a meaningful step—work MUST be coherent. Before an increment that cannot stand alone, the agent MUST explain why, what stays usable or testable, and how to undo it. Changes SHOULD be easy to undo, minimizing irreversible effects and preparing recovery or harm mitigation; the agent MUST report material limits on undoing proposed or completed changes. Recovery reduces the cost of a mistaken approach; it grants no permission for destructive effects. Required stops MAY leave work incomplete, while review-boundary coherence still applies. A small scope cannot excuse shallow reasoning, omitted dependencies, or incomplete work presented as finished.

Under [§2.3](../contract/prerelease_AGENTS.md#23-effort-estimates-and-requester-limits), correctness, completeness, consistency, and adequate reasoning, implementation, and validation MUST precede saving lines, files, or tokens and context. Among workable solutions, clarity, canonical ownership, and reversibility SHOULD precede fewer parts. These priorities apply cumulatively, including to decomposition and repeated attempts; compactness is not a reason to leave required work out.

### Learning throughout the work

The [Deming Institute's PDSA account](https://deming.org/explore/pdsa/) connects an approach and expected result with observation and the next decision. Small increments bound commitments; PDSA's contribution is learning which approach remains suitable and what to do next. Passing tests alone does not establish that learning role: the implications still inform Act and subsequent planning.

The agent MUST apply the contract's [PDSA work cycle](../contract/prerelease_AGENTS.md#1-work-cycle) proportionally to implementation, investigation, and documentation: Plan the next small authorized increment from context and objectives, Do it, Study the results, and Act on the findings. Plan starts with the request and includes context gathering, the overall objective and permitted work, the [four increment elements](#small-commitments-with-sufficient-depth), and selection of the next increment. Study assesses completion and observations; Act uses those findings to retain, revise, or discard the approach and retains learning for Plan. Act also applies the triggered record rules for durable findings, significant decisions, or technical debt, then follows the [composition outcomes](#three-interacting-layers). Results can reshape later detail without changing the agreed outcome or granting more authority.

Terms and the layer overview precede the work cycle. Methods appear near their principal contribution—engineering practices in Do, validation in Study, and documentation and decision methods among the triggered rules—but apply whenever triggered in any phase, and the progression guards apply throughout. Tests can be planned before implementation; decisions and documentation are maintained as facts emerge. Phases may overlap or repeat. Methods alone require no deliverable; routine work needs no worksheet, formal experiment, or special mode. Separate phase reports are not required; reporting has its own triggers.

PDSA's Plan phase organizes reasoning. A tool's Plan mode has its own proposal and approval procedures. Neither expands authorization. These distinctions let the workflow apply proportionally to implementation, investigation, and documentation without inventing separate mandatory deliverables.

### Completion, predictions, and bounded investigation

The contract keeps three ideas separate because they answer different questions:

| Concept | Question it answers | What changes when evidence contradicts it? |
| --- | --- | --- |
| System requirement | What behavior must the system provide beyond this task's execution? | A failure supplies evidence that the required behavior may be unmet. Changing the requirement still needs the relevant authority. |
| Acceptance condition | What observable result is needed to complete this increment? | Missing evidence leaves completion unestablished. Any revision must respect the condition's source and existing authority. |
| Prediction | What result does the agent expect from its approach or experiment? | The evidence informs whether to retain, revise, or discard that approach. Revising the prediction changes neither requirements nor acceptance conditions. |

Study uses acceptance conditions to assess completion and observations against predictions to assess the approach. Revised predictions change neither requirements nor acceptance conditions; learning cannot replace required in-scope behavior. Keeping these comparisons separate allows the agent to revise an unsuccessful approach without weakening what the increment must deliver. An implementation can meet its acceptance conditions through a different approach from the one initially predicted.

The system-requirement boundary depends on what the authorized work establishes. If it establishes or changes behavior required of the system beyond the current task's execution, that behavior is a new or revised system requirement, whatever its source. It needs an authoritative owner and the [EARS requirement form](../contract/prerelease_AGENTS.md#31-new-or-revised-system-requirements). A task objective, acceptance condition, or requester statement does not become a system requirement merely because it was stated. Restating a requirement that already has an authoritative owner creates no duplicate, and analysis or review alone cannot create or change requirements.

The agent first identifies requirements and acceptance conditions already set by the requester or authoritative project sources. It then inspects relevant context before deriving or refining the remaining increment conditions. This order prevents the agent from settling its own completion criteria before reading the evidence those criteria depend on.

Revision authority follows the source of each condition. Requester-supplied requirements or conditions change only with requester authority; canonical requirements change only through authorized requirement work; agent-derived conditions can be refined only within requester instructions, project requirements, scope, and decision authority. A failed check or difficult implementation never justifies weakening, replacing, or reinterpreting any of them, so failed validation cannot lower the completion bar.

This separation allows an investigation to succeed by disproving an assumption. Evidence that a reader splits a quoted comma can answer a question about its behavior, while an implementation required to preserve that field remains incomplete. A successful sample also supports only the conclusion justified by that sample. The [practical investigation example](../contract/prerelease_README-powerusers.md#when-an-investigation-is-needed) develops both outcomes.

Inspecting relevant code, callers, tests, configuration, and directly related dependencies to establish starting context, and all reading of existing project documentation, are context gathering. The documentation exemption still applies to a material blocking question; no inspection-by-inspection announcement is needed. Scope, limits, proportionate work, and cumulative reassessment apply throughout.

Beyond context gathering, the [inquiry guard](../contract/prerelease_AGENTS.md#24-context-gathering-and-bounded-inquiry) turns on the purpose of resolving material uncertainty about how to proceed that blocks the next decision. This purpose-based distinction matters because the same command can serve different jobs. It might execute an already settled task, validate an implementation, or investigate which approach to choose. Unknown output alone does not distinguish those jobs. Conversely, a documented procedure used to investigate a blocking approach question remains inquiry. The [practical distinctions](../contract/prerelease_README-powerusers.md#when-an-investigation-is-needed) show these different uses of measurements and tests.

The inquiry rule separates timely requester awareness from control of the investigation itself. The agent must promptly make the blocking material uncertainty and its significance for the next decision clear, unless already communicated in the request or task framing. That tells the requester why investigation matters without requiring five announced elements, an advance effort estimate, or a declared allowance. Repeating information already supplied adds no required decision context. The [reporting design](#reporting-and-continued-execution) explains the distinct timing of this notification and the initial task outline.

Actual inquiry must still proceed through small, bounded, proportionate increments focused on the next decision. Evidence sufficiency and increment bounds address two different failure modes: treating any output as sufficient evidence and continuing merely because the answer is still unknown. Sufficient evidence ends the inquiry. If evidence remains insufficient at an increment's bounds, the agent must reassess before further investigation. The requirement is to constrain and assess the work, not to fill an announcement template. A numeric budget is not required; [requester-imposed limits](#authorization-and-requester-decisions), when present, constrain the work across attempts. The practical example's single sample run illustrates a bounded experiment, while its optional one-attempt checkpoint illustrates a separate requester control.

These bounds do not decide completion by themselves. [Study and Act](../contract/prerelease_AGENTS.md#13-study--assess-completion-and-learning) govern assessment and what follows: an evidenced negative answer may complete an investigation, while an unsuccessful attempt can reach its bounds with acceptance conditions unmet. Reporting occurs at task completion, handoff, or when seeking requester input, with earlier disclosures where required. There is no automatic inquiry-end message. Neither stopping nor reporting supplies missing acceptance evidence.

Further attempts must be justified by preceding findings and stay within existing authorization, limits, and checkpoints. The [progression guards](../contract/prerelease_AGENTS.md#2-progression-guards) require cumulative reassessment of progress, remaining work, established direction, and limits, not a new advance announcement for every attempt. Repeated attempts cannot reset a cap or bypass a checkpoint; without evidence justifying a next increment, the agent seeks direction. This keeps effort discipline in force even when no allowance was declared.

Narrow investigation within existing authorization may establish facts for consultation. When it exposes an unsettled decision requiring requester direction under §2.2, the agent must consult before adopting or implementing that direction. Notification neither provides that authority nor adds an approval checkpoint to otherwise authorized investigation. The design therefore preserves technical autonomy while reserving consequential choices for the requester. Removing a mandatory announcement structure does not establish equivalent agent behavior or improved token efficiency; those are evaluation questions, not conclusions from wording alone.

### Authorization and requester decisions

An increment limits work undertaken at once; a report can summarize several increments; a checkpoint reserves a decision for the requester. Another increment needs existing authorization or a new request; completion MUST NOT authorize further work. Ordinary increments can [continue under existing authorization](../contract/prerelease_AGENTS.md#25-continuing-to-another-increment) without routine reports. Their completion supplies no additional permission and creates no automatic pause.

The agent MUST stay within requester-authorized scope, and requester instructions MUST precede this contract within the tool's priorities and permissions. It MUST follow tool planning, review, and approval rules; tool modes MUST NOT widen scope. Plan mode alone permits only deepening authorized analysis at the current abstraction level. A mode is not permission to implement, expand the task, or settle a consequential choice.

Under the [rules on requester limits](../contract/prerelease_AGENTS.md#23-effort-estimates-and-requester-limits), the agent MUST obtain requester direction before exceeding requester-imposed effort or scope limits or passing checkpoints; only requester direction MAY revise them. Increments, retries, and handoffs MUST NOT reset them. Informal expectations are not automatically limits; material ambiguity MUST be resolved under the requester-interaction rules. The requester controls consequential direction and any limits they impose; routine local corrections remain autonomous within that direction and authorization.

Cumulative reassessment prevents each small increment from being considered in isolation. Before expanding planned work or starting another increment or attempt, the agent MUST reassess cumulative progress, remaining work, established direction, and applicable limits, and justify the next increment's contribution to the task objective from evidence; otherwise it MUST seek requester direction. A series of small changes cannot authorize unrelated improvements or conceal a material departure from agreed direction.

Small increments and bounded inquiries constrain how work proceeds; they do not guarantee low total consumption. The [practical examples](../contract/prerelease_README-powerusers.md#when-the-work-grows-unexpectedly) distinguish a routine correction, an explicit checkpoint, and a consequential parser change.

In the [requester-interaction guard](../contract/prerelease_AGENTS.md#22-decisions-and-requester-interaction), the [requirement keywords](../contract/prerelease_AGENTS.md#terms-and-requirement-keywords) preserve distinct strengths:

- Material unresolved intent or permission MUST be taken to the requester, agreeing as needed on consequential constraints left unsettled by requirements, architecture, or conventions. The agent MUST NOT invent these constraints or treat missing constraints or answers as broader permission.
- Before adopting or implementing a new consequential architectural or lasting design direction or a material departure from established direction, the agent MUST obtain requester direction unless the specific choice is already authorized.
- The agent SHOULD ask first for other unsettled choices materially affecting the decision factors, optimization, or lasting complexity.
- Within agreed limits, easily reversible routine local details MAY be chosen. Material assumptions MUST be disclosed and MAY support progress with limited, easily reversed effects.

A broad outcome does not specifically authorize every consequential design choice that might achieve it. This matters in new projects as well as established ones: absent architecture is not a delegation of unrestricted architectural authority. Conversely, a local correction within the established design does not become a mandatory consultation merely because the original implementation approach failed.

Routine choices and SHOULD exceptions waive no mandatory requirements. A SHOULD exception cannot bypass a MUST checkpoint or invent a consequential constraint. Recording an ADR or reporting afterward cannot replace required prior direction. Consequential choices made without prior direction MUST be prominently reported with reasons, effects, uncertainty, and revision or reversal options; reporting MUST NOT count as advance authorization. Native permissions and approval controls remain the enforceable boundaries.

If safe steps are impossible, the agent MUST present alternatives and seek requester direction. This is a stop for unresolved safe continuation, not permission to choose a new direction from those alternatives.

Analysis and review can establish lasting project knowledge before implementation, so the contract separates permission to write from the conditions that call for a record. The [limits on assessment writes](../contract/prerelease_AGENTS.md#21-authority-and-scope) decide which writes an assessment-only task may make at all, alongside the other limits on permitted work. The [material-findings rule](../contract/prerelease_AGENTS.md#32-durable-findings-and-permanent-records), [decision rule](../contract/prerelease_AGENTS.md#33-significant-decisions-adrs), and [debt rule](../contract/prerelease_AGENTS.md#34-technical-debt) then decide whether a record is due. Each has its own trigger and strength, applying whenever its conditions arise.

Keeping these questions separate preserves both restraint and knowledge retention. Permission to record debt cannot make an optional debt entry mandatory. A required record cannot authorize implementation, new or changed system requirements, accepting or changing decisions beyond existing authority, unrelated documentation repairs, or backfills. A **permanent record** is the canonical project document owning the topic; chat and working notes do not fulfill that role. It preserves the finding and evidence for future work; neither that document nor a chat discussion supplies permission to implement the recommendation.

The findings trigger requires both materiality and durability so that assessment retains what later work needs, including lasting learning from discarded approaches, without becoming a work log. Durable knowledge is expected to remain useful beyond the current task or attempt for maintenance, operation, requirements, architecture, or technical decisions, even if later updated through its owner. Material findings that are also durable MUST be recorded with substantiating evidence in appropriate permanent records. Transient facts useful only to this attempt, such as temporary conditions, one-attempt failures, or outages, follow only the reporting rules. If no suitable owner exists, the agent MUST create the minimum record holding only those findings and evidence: no placeholders, empty sections, or backfill. Other documentation gaps remain improvement proposals. A finding alone triggers no ADR. If writing is prohibited, the agent MUST report the unmet record duty as unfinished work; reporting the finding in chat does not satisfy that obligation.

Verified factual corrections are a separate permission because they align an existing description of current project facts with its owner. Excluding requirements, decision records, and protected instruction files prevents that permission from being used to change intended behavior or accepted decisions. All these writes remain subject to authorized scope, [requester restrictions](../contract/prerelease_AGENTS.md#21-authority-and-scope), [protected-file rules](../contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions), and tool permissions and approvals, which can prevent them. Broader documentation repairs and external actions retain their own authorization requirements. The [practical examples](../contract/prerelease_README-powerusers.md#records-during-review-and-exploration) show each case and the effect of a no-edit instruction.

Precisely, analysis or review alone permits **only** material, durable finding records; ADR and debt maintenance; and verified corrections aligning existing descriptions of current project facts (such as commands or paths) in the assessed scope with their owner. The correction permission excludes requirements, decision records, and the three protected instruction files. It MUST NOT authorize implementation, new or changed system requirements, accepting or changing decisions beyond existing authority, unrelated documentation repairs, or backfills. A record trigger does not remove any of these limits.

### Reporting and continued execution

Completing an increment and reporting to the requester serve different purposes. PDSA requires the work to be assessed and its findings used, even when no chat report follows. Under [AGENTS.md §3.7](../contract/prerelease_AGENTS.md#37-reporting), the agent MUST consolidate unreported work into a report at task completion, handoff, or when seeking requester input. It SHOULD minimize routine progress reports; intermediate communication SHOULD be concise and useful. This does not categorically prohibit drafting or sending an intermediate update.

The recommendation favors communication that helps the requester understand the work or a relevant change without making every increment an occasion for narration. The agent can use evidence for the next authorized step while keeping information needed for a requester decision timely. Disclosures affecting authorization or a decision requiring requester input MUST precede the affected work. Other information SHOULD normally join the next consolidated report. This preserves a strong default for concise reporting while allowing useful intermediate communication.

The initial task outline and inquiry notification retain their distinct timing. After proportionate preliminary context gathering, the agent MUST briefly state the task outline and first increment's objective and bounds in chat before substantial work. It MUST promptly make material inquiry uncertainty and its significance for the next decision clear to the requester, unless already communicated in the request or task framing. The initial statement can satisfy that notification when it includes the relevant uncertainty and significance. Neither communication creates an approval checkpoint.

These duties make the intended direction and relevant uncertainty understandable in time for the requester to respond. Private planning or a retrospective report cannot replace a required initial statement or prompt notification. If the request already communicates the uncertainty and its significance, however, a duplicate announcement is unnecessary. Informational messages do not reserve a review interval, reveal exact consumption, or prove that the agent respected its bounds. Required consultation gives the requester control before a consequential choice; notification alone cannot replace it.

The trade-off is judgment about the usefulness and timing of intermediate communication, alongside explicit duties where requester awareness or control matters. There is no mandatory planning message for each later increment, worksheet, or new record type. A subsequent inquiry attempt needs evidence and reassessment, without automatically needing another announcement. Ending an inquiry does not itself require another message, and nonblocking debt disclosures should normally join the next reporting occasion.

Maintaining project knowledge has its own timing. Material findings, decisions, and affected documentation retain their owners and maintenance triggers; their maintenance does not wait for the report. The agent can therefore update a required record during the work and describe that update in the later consolidated report. No separate reporting log or record is required for every increment. Tool instructions and requester-selected reporting remain applicable.

A handoff report MUST transfer the task objective and established direction; applicable limits and checkpoints and consumed allowances; the next or unfinished increment's objective, bounds, and acceptance conditions; and relevant inquiry conclusions, supporting evidence, and unresolved uncertainty. Meaningful results and continuation state matter; a chronological activity log does not substitute for them. This preserves knowledge of authorization and evidence across a change of context without granting new permission. On resumption, the agent MUST use that transferred state, recovering missing authorization or limit state or obtaining requester direction before dependent work.

The design permits less routine visibility during autonomous work while requiring a consolidated account at the next reporting occasion. Useful updates remain possible, and requester-selected reporting can provide more visibility. Reporting alone reserves no time for review and creates no approval checkpoint. Scope limits, bounded investigations, cumulative reassessment, and required consequential consultation continue to control the work. Neither more nor fewer messages establish compliance, measured token savings, or equivalent agent behavior.

The current [reporting rule](../contract/prerelease_AGENTS.md#37-reporting) specifies content and delivery as well as timing:

| Reporting concern | Current prescription |
| --- | --- |
| Consolidated content | Reports MUST cover changes and reasons; paths; relevant decisions and canonical links; checks run and omitted; material assumptions, conflicts, risks, and choices; and unfinished work. They MUST explain material SHOULD exceptions and distinguish evidence from inference and increment completion from task completion. |
| Inquiry outcomes | At task completion, handoff, or when seeking requester input, the agent MUST report relevant conclusions, supporting evidence, remaining uncertainty, incomplete work or missing evidence for unmet acceptance conditions, and any need for broader research or a wider design decision. Inconclusive findings grant no additional authorization. |
| Proportion | Reports SHOULD fit the work. Small mechanical changes usually need only outcome and checks, with no invented risks, follow-up, or mandatory templates. This does not omit applicable material disclosures. |
| Displayed edits | Displayed edits MUST default to changed portions with context; contents or diffs MAY be omitted. New files and extensive rewrites SHOULD receive available full-file links and chat explanations. Full copyable contents MAY be shown on request or for blocked edits. |
| Blocked tools | The agent MUST report tool limits blocking edits, checks, or instruction loading and, where possible, supply exact changes with paths and application context. A fallback explanation does not establish that the edit or check occurred. |

The [usage guide](../contract/prerelease_README-powerusers.md#assess-the-result) illustrates what the requester receives; these duties are specified here without relying on that illustration.

### Engineering scope boundaries

**Current scope boundary (§1.2).** The agent MUST NOT add unrelated cleanup, renaming, reformatting, dependency changes, file moves, or speculative refactoring. It MUST NOT delete code as dead unless the code is clearly unreachable or directly made obsolete by the authorized change. Necessary larger refactors SHOULD stay distinct from behavior changes. These boundaries apply to the practices below; method selection does not authorize unrelated work.

### Simple Design: choosing what the current solution needs

Beck's [Simple Design, explained by Fowler](https://martinfowler.com/bliki/BeckDesignRules.html), supplies four criteria: meet requirements and pass tests, express intent, avoid duplicated knowledge, and retain only necessary elements. They assess the current solution; fewer classes or lines alone cannot establish simplicity.

Code SHOULD be clear and maintainable, reusing suitable code and project patterns. Names and structure SHOULD explain implementation; tests SHOULD explain behavior; comments and documentation SHOULD explain reasons or limits code cannot express, with links for detail. These recommendations assign complementary explanatory roles rather than requiring comments to repeat the code.

Current requirements MAY justify complexity; speculation alone MUST NOT justify abstractions, parallel implementations, configuration, or optimization. Optimization SHOULD have requirements or evidence and explain material complexity and trade-offs. The documented strategy SHOULD be followed unless the task conflicts with or materially extends it; the authority and consultation guards still apply.

Hard memory, latency, throughput, concurrency, cost, or scale requirements may justify complexity. An imagined future extension does not provide equivalent evidence. Supporting one agreed input format can be complete without a framework for unspecified formats, while still including its necessary error handling and checks. A documented optimization strategy supplies project context and is a strong default; a task that conflicts with or materially extends it remains subject to the consultation rules. Material trade-offs remain visible.

### DRY: keeping knowledge consistent as work progresses

The [Pragmatic Programmer's DRY account](https://media.pragprog.com/titles/tpp20/dry.pdf) concerns knowledge that would otherwise need independent maintenance in several places. Writing for maintainers and users, the agent MUST give each project fact, rule, or explanation one canonical owner (a file or section) and MUST prefer reuse, links, derivation, generation, or extraction over independent copies. Canonical ownership reduces the risk of divergent facts, rules, or explanations across code and documents.

A setting can own a retry limit while a guide explains its purpose and links to it. Two unrelated limits may have the same value without representing shared knowledge. Necessary generated, protocol, migration, compatibility, test, example, or summary copies MAY remain with a clear canonical owner and update process. Resemblance alone MUST NOT require abstraction: similar code MAY encode different rules.

### Component boundaries, refactoring, and validation

The agent SHOULD fix root causes, use descriptive names, and favor independent components, clear boundaries, small public interfaces, visible side effects, encapsulation, and low coupling. Resource acquisition, use, and release, and shared-resource synchronization and transactions SHOULD have explicit owners; concurrent coordination SHOULD stay separate from sequential logic where practical. These properties make the effects of a change easier to understand. The [public tips](https://pragprog.com/tips/) and [shared-state extract](https://media.pragprog.com/titles/tpp20/shared-state.pdf) support these concerns; their exact assignments appear in [Principles and reference boundaries](#principles-and-reference-boundaries). Practical separation supports clear ownership without prescribing a universal asynchronous architecture.

The current preservation duties are explicit:

| Concern | Current prescription |
| --- | --- |
| Protected behavior and guarantees | The agent MUST preserve public contracts, compatibility, error handling, required logging, resource lifecycles, concurrency guarantees, and security unless intended and authorized otherwise. It SHOULD make failure handling and contracts explicit and minimize unnecessary attack exposure. |
| Refactoring and behavior changes | [Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) MUST preserve observable behavior. Intended behavior changes MUST update affected requirements, tests, and documentation. The authorization exception for intended behavior changes does not redefine refactoring. |
| Invariants and patterns | Documented design invariants (promised properties) MUST hold unless authorized work updates their contract and affected files. Patterns MAY change through scoped, justified, validated improvements; material lasting rationale MUST be recorded. |

Neither preservation distinction requires retaining a defect when changing it is intended and authorized. Lasting rationale is retained under the applicable record rules, not discarded simply because a pattern was improved.

The dead-code condition matters because registration, reflection, or external callers may make apparently unused code reachable. Clear unreachability or direct obsolescence from the authorized change is needed for removal *as dead code*. Explicitly authorized removal of live functionality is a different case.

### Validation and test evidence

Completion MUST require correctness, consistency, and validation across affected artifacts; required stops MAY leave work incomplete. Before completing an increment, the agent MUST run relevant available acceptance checks, independently of whether a report is produced then. Checks MUST cover affected behavior, risk, and hard performance and operational limits. Passing tests MUST NOT replace requirements or necessary checks. Failed, unavailable, and omitted checks MUST be disclosed under the [reporting rule](#reporting-and-continued-execution); any need for requester involvement still follows the [progression guards](../contract/prerelease_AGENTS.md#2-progression-guards).

Behavior changes, defect repairs, and clarified edge cases SHOULD have appropriate tests, including regression checks. Their names, examples, setup, actions, and assertions should explain the expected observable behavior as part of that recommendation. This does not require code or unit tests for their own sake during documentation-only work; the acceptance checks appropriate to that work still apply.

Distinguishing check availability from acceptance prevents a tooling limitation from being treated as successful validation. It also allows sufficient alternative evidence to establish a condition when the contract's substitution rules permit it.

Sufficient alternative evidence MAY substitute only when the original check is unavailable and is not specifically required. A check is available if runnable under current authorization, tool access, permissions, credentials or resources, and prerequisites with ordinary expected setup. An easier alternative MUST NOT make it unavailable: a relevant available acceptance check still runs even if an alternative could provide equally sufficient evidence. If a check needs missing authority, access, or resources, or materially more work, the agent MUST disclose this rather than silently obtain or absorb it, applying the authorization, limit, and reassessment rules. More work alone does not create a checkpoint.

Conditions lacking sufficient evidence MUST be reported unverified, and validation incomplete, unless validly revised under existing authority. Disclosure alone cannot establish them. A pre-existing failure is assessed for relevance and disclosed, without automatically blocking unrelated work. The [practical validation examples](../contract/prerelease_README-powerusers.md#assess-the-result) distinguish available checks, equivalent local checks, insufficient mocked evidence, and a specifically required CI result.

Unit tests SHOULD use [Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html): starting conditions, action under test, and expected result. For a quoted field containing a comma, those parts are the sample, the parser call, and the intact-field assertion. The contract prescribes neither literal labels nor a testing framework. The agent MUST NOT weaken tests just to pass.

### Focused techniques and how they work together

These techniques support Simple Design when their benefits justify their costs. Their selection grants no authority for unrelated restructuring or new dependencies.

**Gross's [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/)**

Behavior SHOULD be understandable near its implementation; the agent MUST balance this with separate responsibilities and canonical ownership. A clearly named validation call can keep the control flow readable while the rule stays in its canonical owner. The contract does not require inlining everything or adopting htmx.

**The [Law of Demeter](https://www2.ccs.neu.edu/research/demeter/demeter-method/LawOfDemeter/general-formulation.html)**

The agent SHOULD use direct collaborators' interfaces, avoiding reach-through when this reduces coupling and weighing clarity and interface costs; it MUST NOT ban all chained access. The trade-off is reduced coupling versus interface complexity: forwarding methods that add no useful boundary can make the code harder to follow. The contract therefore weighs coupling and clarity rather than imposing a blanket ban on chained access or requiring an aspect-oriented solution.

**Fowler's [Value Object](https://martinfowler.com/bliki/ValueObject.html)**

Value objects (equal by contents) or other domain structures SHOULD replace primitives when they clarify meaning or validation. The agent SHOULD favor immutability where practical, preserving required identity and state changes. The contract makes this a conditional design recommendation; it requires neither wrapping every primitive nor adopting Domain-Driven Design.

**The [inheritance extract](https://media.pragprog.com/titles/tpp20/inheritance-tax.pdf)**

The agent SHOULD prefer interfaces, protocols, and composition when they reduce coupling, and polymorphism over complex conditional dispatch when clearer, without banning justified inheritance. The conditions matter: these preferences do not justify abstractions based on speculation alone or prohibit suitable inheritance.

**Fowler's [dependency injection](https://martinfowler.com/articles/injection.html), “Separating Configuration from Use”**

The agent SHOULD supply dependencies externally when this improves separation, clarity, or testing. Configuration SHOULD stay at assembly, initialization, or external-system boundaries. Supplying a clock as a parameter can suffice; no container or new dependency is required.

### Documentation choices

Different project artifacts answer different questions. Requirements describe intended behavior. Accepted decisions retain choices and reasons. Architecture describes boundaries and guarantees. Schemas and package metadata declare their own constraints. Code, tests, and execution provide evidence of implemented behavior. Examples and notes govern only when explicitly labeled as rules.

These roles explain why executable behavior does not automatically overrule a requirement. If an implementation behaves differently from a required format, that disagreement is evidence to assess. The existence of the implementation does not by itself authorize changing the requirement. The contract intentionally has no global precedence ladder among these artifacts. An earlier total ordering was removed because a single ranking cannot fit artifacts that own different kinds of knowledge.

The agent MUST report contradictions, distinguish evidence from inference, and follow the knowledge's owner. If ownership leaves a consequential conflict unresolved, it MUST take that conflict to the requester under the requester-interaction rules instead of inventing a fallback order. Instruction files govern agent conduct rather than proving project facts. Requirements, constraints, and facts stated by the requester remain legitimate task context.

Documentation preserves a shared account of the project for maintainers, users, and future agents. Reading canonical facts and reasons supports Plan; producing a guide or updating affected documentation is Do work. Study checks acceptance; Act uses the findings and retains relevant learning. Requirement, record, decision, debt, documentation, and architecture duties are [triggered rules](../contract/prerelease_AGENTS.md#3-triggered-rules) because their conditions can arise in any phase. They preserve knowledge as it emerges without authorizing work beyond their terms.

Updates follow **affected documentation**: the canonical owners of changed knowledge and the known documents that directly depend on it, whether linked or not and read or not. These documents MUST track code, tests, configuration, interfaces, architecture, and operations. A README repeating a changed value is affected even if it has no link to the owner and has not yet been read. Such dependents are typically known from the task, artifacts being inspected, explicit references, ownership, or established source/update relationships. Links alone warrant checks, not necessarily edits.

Documentation work MUST stay bounded under the increment and inquiry rules and within that affected set unless broader work is authorized. Dependents and coverage expectations MUST NOT authorize searches for unknown dependents, repository-wide audits, backfills, or reorganization; wider checks MAY be proposed. This defines the required synchronization work without making every edit a repository-wide documentation project. Documentation-only work uses the same increment, validation, and review rules as other work.

At review boundaries, the agent MUST fix stale, conflicting, duplicated, or misplaced content and links within authorized scope; analysis or review alone remains limited to the [permitted assessment writes](#authorization-and-requester-decisions). Current-system documents MUST describe what exists and label unfinished or proposed work. Finding an out-of-scope gap does not override scope or protected-file limits.

### arc42: shared architectural context as the project grows

[arc42](https://arc42.org/overview/) supplies the following twelve topics. Applicable topics set target coverage, rather than a mandatory empty template:

| Topic | Target subject |
| --- | --- |
| 1 | Goals, stakeholders, and fundamental requirements |
| 2 | Design and implementation constraints |
| 3 | Context and scope |
| 4 | Solution strategy |
| 5 | Building blocks |
| 6 | Runtime behavior |
| 7 | Deployment |
| 8 | Crosscutting concepts |
| 9 | Decisions |
| 10 | Quality goals and scenarios |
| 11 | Risks and technical debt, under the debt rule's qualifications |
| 12 | Glossary |

Shared content expectations aim to reduce reinvention and relearning across repositories. They give an empty project questions to answer as evidence develops, without requiring the entire design to be settled first.

Content MUST use known facts, not empty sections or invention, and detailed requirement links. For known gaps, the agent MUST propose improvements and SHOULD make them within authorized scope; conventions MUST NOT excuse gaps. The requester MAY decline, postpone, or limit changes, and material unknowns and gaps MUST stay visible. A partial or minimal architecture document does not itself breach the contract when these qualifications are respected. [Incremental documentation](https://faq.arc42.org/questions/B-14/) and [appropriate depth](https://faq.arc42.org/questions/B-4/) support keeping content useful as the system develops. [Quality scenarios](https://docs.arc42.org/section-10/) make goals assessable: “imports should be fast” still needs an agreed workload and measure.

`README.md` MUST concisely give purpose, getting started, and any documentation locations other than root `docs/`. Architecture SHOULD start in one document in the existing documentation folder (the README-stated location, otherwise root `docs/`); sections MAY split for readability or maintenance, and names and layout MAY vary. Because root `docs/` is the standard default, creating a document there requires no README location update solely for that reason. This keeps early information together. The accepted [product/internal separation decision](../docs/architecture.md#requirements-led-engineering-and-productinternal-separation) owns the scoped README interpretation for this repository: consumer README navigation concerns user-facing documentation, while engineering navigation stays with the [behavior entry point](../behavior/README.md), [evaluation guide](../evaluations/docs/evaluations.md), and [engineering-system architecture](../docs/architecture.md). That is a compatible engineering boundary, not an extra operating duty for adopting projects. An adequate existing arrangement can remain. Known coverage gaps still require proposals and warrant improvements within authorized scope, subject to requester limits or deferral. Summaries link to canonical requirements and ADRs, while implementation detail stays near code and tests.

Topic 11 covers known risks as well as technical debt under the contract's definition. The risk category is not restricted to internal-quality compromises: external dependencies and operational circumstances can create known risks even when implementation quality is adequate. The distinction preserves the scope of [arc42's risks and debt topic](https://docs.arc42.org/section-11/) without classifying every risk as debt or importing an additional risk-management procedure.

### EARS: making required behavior explicit

[EARS (Easy Approach to Requirements Syntax)](https://alistairmavin.com/ears/) gives natural-language requirements consistent condition-and-response patterns. The [practical guide's CSV example](../contract/prerelease_README-powerusers.md#make-expected-behavior-explicit) illustrates this:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

The pattern exposes behavior to implement and check. It cannot decide whether to reject one row or the whole file, or define a row's line number for a particular format. Those remain project decisions. EARS applies to new or revised in-scope system requirements; unchanged requirements need no automatic conversion. Under the [current rule](../contract/prerelease_AGENTS.md#31-new-or-revised-system-requirements), new or revised in-scope requirements MUST have canonical owners and consistently express verifiable behavior in the form `<prefix> the <system> shall <response>.` Restating a canonical requirement MUST NOT create a duplicate. The five prefixes and their applicability are:

| Pattern | Prefix before `the <system> shall <response>.` |
| --- | --- |
| Unconditional behavior | None |
| State | `While <state>,` |
| Event | `When <event>,` |
| Optional feature | `Where <feature is included>,` |
| Unwanted condition | `If <unwanted condition>, then` |

Conditions MAY combine, with state before event: `While <state>, when <event>, the <system> shall <response>.` The [system-requirement boundary and revision rules](#completion-predictions-and-bounded-investigation) determine what needs this form and who may change it. Rationale belongs with significant choices; EARS adds no mandatory rationale field to each requirement.

### ADRs: preserving the reasons for lasting choices

[Architecture Decision Records](https://docs.arc42.org/section-9/) retain reasons that code alone may not reveal. A streaming-parser decision can connect a memory constraint and experiment evidence with consequences for error reporting. Later work can assess that reasoning against new evidence instead of reconstructing it.

For significant architectural, optimization, compatibility, or other lasting choices in scope, the agent MUST create an ADR when a concrete proposal is ready for decision or review, in or linked from arc42 section 9. It MUST retain the decision-shaping evidence, requirements, and constraints through these fields:

| Field | Required information |
| --- | --- |
| Title | The decision's title |
| Status | Proposed, accepted, rejected, or superseded, as applicable |
| Context | Situation and constraints |
| Decision | Choice and reasons |
| Consequences | Benefits, costs, and risks |

This timing preserves developed proposals before acceptance without requiring an ADR for every exploratory idea; routine local choices SHOULD NOT create ADRs. The agent MUST distinguish proposed, accepted, rejected, and superseded decisions. Accepted MUST reflect a decision under existing authority and consultation rules, not implementation status or a new ADR-specific approval. A record cannot replace required prior requester direction for a new consequential design direction or material departure. The agent MUST preserve material history, influential failures, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links, explaining the basis and applicability of decisions. No exhaustive alternative search or out-of-scope backfill is required.

### Recording technical debt

The agent MAY record current, task-relevant, evidenced design or implementation compromises increasing maintenance cost or risk in arc42 section 11. It MUST consider accepted requirements and trade-offs. A deferred feature, rejected option, or different preference alone does not establish debt. Intended behavior is not automatically a defect, although an accepted compromise can carry debt.

Permission to record evidenced, task-relevant debt makes concerns visible without requiring separate authorization for each entry or an in-scope fix. It applies to assessment-only work too, within its write limits. The agent MUST flag uncertain classifications and report recorded debt in chat—what, why, where, and uncertainty—making the classification assessable; nonblocking disclosures SHOULD normally join the next consolidated report under the [reporting rule](#reporting-and-continued-execution). When in-scope work changes or resolves debt, its records in [arc42's risks and debt section](https://docs.arc42.org/section-11/) MUST be updated. Recording MUST NOT authorize fixes or override an accepted decision; contract-file protection still applies. A separate material-and-durable finding trigger can require a record even though debt recording itself is a MAY.

### Diátaxis: choosing content for the reader's need

[Diátaxis](https://diataxis.fr/) separates four needs: tutorials teach through guided practice, how-to guides help complete a task, reference supplies precise facts and interfaces, and explanation develops understanding. The [introductory guide](https://diataxis.fr/start-here/) explains these forms. A guide for correcting rejected rows can focus on the task and link to maintained format rules and background rationale.

New guides and tutorials MAY serve only an explicitly requested or agreed need; simple or low-level software may need none. In-scope guides MUST apply Diátaxis: tutorials teach by guided practice, how-tos solve tasks, reference gives facts and interfaces, and explanation builds understanding. The agent MUST NOT create empty categories for ceremony. Affected existing guides stay current under the synchronization rules. [Applying Diátaxis incrementally](https://diataxis.fr/how-to-use-diataxis/) supports this without a four-document requirement. Comments, docstrings, and generated API documentation SHOULD follow suitable existing language and tool conventions; the agent SHOULD offer requester choices for new conventions materially affecting public documentation or maintenance.

### Principles and reference boundaries

The delivered `AGENTS.md` remains the normative runtime authority. This section explains the current contract's method-reference semantics and source assignments; it adds no operating obligations and does not expand the practices adopted for AGENTS-spec development under the [development authority model](../docs/architecture.md#development-time-and-runtime-authority).

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

The contract should normally suffice for ordinary cases. Under the [method-reference rules](../contract/prerelease_AGENTS.md#39-method-references), an agent may consult a linked source when the contract leaves a material ambiguity in applying that method, reading only enough to resolve it. The ambiguity, consulted reference, and resulting interpretation must be reported, and no other practices are imported. Research stays bounded by §§1.1 and 2.4: if the consultation is inquiry into material uncertainty blocking the next decision, its notification and conduct requirements apply, including the exception for uncertainty and significance already communicated in the request or task framing. Clear rules must not be researched. Before broader research, the agent must explain the unresolved uncertainty and ask the requester. Technical research for a task follows its scope, authorization, and applicable inquiry rules. This distinction prevents an explanatory link from becoming an open-ended research assignment or importing a reference's stronger rhetoric as policy.

## Runtime View

### How the design works in a task

Consider the CSV-import scenario from the [practical walkthrough](../contract/prerelease_README-powerusers.md#from-a-request-to-a-result): report invalid rows and continue with valid rows. The **task objective** is that overall outcome. An **increment** is the next deliberately small, bounded step toward it, normally useful, understandable, reviewable, and verifiable on its own.

[PDSA—Plan–Do–Study–Act](https://deming.org/explore/pdsa/) begins with that request. Plan selects and bounds the work; Do performs it; Study assesses completion and the approach; Act uses the findings. Throughout, progression guards determine whether work may proceed, and triggered rules apply when their conditions arise; the [layer design](#three-interacting-layers) explains this division.

1. **Plan:** establish the objective and permitted work, then inspect the relevant project context. Suppose the requirements settle the input format, invalid-row rules, and line-number convention; existing tests support the reader's suitability; and inspection shows that field-count validation is missing. The row-processing code exposes the fields, header, and line number, suggesting a local implementation.

   This evidence supports choosing field-count validation: it advances an agreed requirement, addresses one concern, and can produce a useful, testable result without implementing every remaining invalid-row rule. The scope includes the affected code, tests, and documentation. Its limited dependencies and expected ease of reversal support a small commitment; neither substitutes for validation.

   Define **acceptance conditions**—reject mismatched rows, report their line numbers, and continue with valid rows, including one after a rejection—and a **prediction** that the existing row boundary will support the approach. These derived conditions follow the agreed requirements and define this increment's completion; they are not new system requirements. Selection, scope, conditions, and approach can be refined together as context becomes clear, within the governing instructions and requirements. Later work remains at outline level.

   The initial planning statement in the [practical walkthrough](../contract/prerelease_README-powerusers.md#from-a-request-to-a-result) relates the overall task to the first increment's objective and bounds. Preliminary context makes the plan meaningful; communicating it before substantial work lets the requester understand the direction and next action. The statement creates no approval checkpoint.
2. **Do:** implement the validation using current project conventions and Simple Design. Add relevant tests and update affected documentation at its authoritative location. Significant lasting choices need ADRs; choices requiring prior consultation must receive requester direction before adoption or implementation.
3. **Study:** check acceptance before completing the increment, including a valid row after a rejection. Separately assess whether the predicted local approach sufficed. Failed, unavailable, or omitted checks remain subject to disclosure under the reporting rules.
4. **Act:** use the evidence to retain, revise, or discard the approach within authorization. Material findings that are durable project knowledge trigger the [record rule](../contract/prerelease_AGENTS.md#32-durable-findings-and-permanent-records). The [composition rules](../contract/prerelease_AGENTS.md#4-how-the-layers-compose) then lead to finishing, a handoff, seeking required direction, or planning the next increment already covered by authorization. Continuing to another increment does not require drafting or emitting a routine report; reporting follows [§3.7](../contract/prerelease_AGENTS.md#37-reporting).

The initial choice therefore depends on what Plan establishes. Unsettled consequential requirements need requester input; uncertainty about the reader may call for a bounded investigation. A new consequential design direction also needs prior requester direction unless specifically authorized. Within those boundaries, choosing and defining routine increments remains the agent's responsibility.

The example connects the design's parts. Requirements provide intended behavior; inspection and existing checks establish the starting point; Study supplies new evidence; Act uses it to inform subsequent Plan phases. Records preserve durable material findings and lasting choices; transient task facts follow the reporting rules without requiring permanent records. The supported local validation approach may help plan another rule, while evidence of wider parser limitations changes the basis for that next decision.

The field-count result can therefore inform another authorized validation increment before any routine chat report is produced. A local implementation correction can proceed within the existing direction and limits. A proposal to change the shared parser's established error contract instead requires requester direction before adoption or implementation unless that specific change is already authorized. At completion, handoff, or when seeking input, the agent consolidates unreported work. A requested operator guide could be another increment, shaped by its reader's need. Neither a completed step nor a named method automatically creates an ADR, guide, or approval requirement.

The [practical walkthrough](../contract/prerelease_README-powerusers.md#from-a-request-to-a-result) shows the user-facing interaction. The [design explanations](#engineering-scope-boundaries) explain the reasons and boundaries behind it.

## Architecture Decisions

### Selected design and retained decisions

This index identifies status and points to the reasons and consequences already owned here. It does not turn each explanation into an ADR or independently accept a product requirement. Engineering-system and evaluation-specific decisions stay with the [architecture decision index](../docs/architecture.md#decisions) and [evaluation documentation](../evaluations/docs/evaluations.md); they are not copied here.

| Choice | Status and rationale location |
| --- | --- |
| Separate work cycle, progression guards, and triggered rules | **Selected current design.** [Three interacting layers](#three-interacting-layers) explains cross-phase concerns, composition, and the rejected implication that placement confines a duty to a phase. No measured benefit or permanent three-layer requirement is claimed. |
| Bounded commitments with PDSA and focused practices | **Selected current design; recorded as sufficient for the agreed design.** [Learning](#learning-throughout-the-work), [engineering choices](#engineering-scope-boundaries), and [method selection](#choosing-or-replacing-methods) explain complementary roles. Additional umbrella frameworks were not needed; future replacement is possible under the selection criteria. |
| Role-specific knowledge ownership | **Selected current design; earlier total ordering rejected/superseded.** [Documentation choices](#documentation-choices) retains why no global artifact precedence fits different knowledge owners, and how unresolved consequential conflicts are handled. |
| Provider-specific instruction bridges | **Selected current integration design.** [Why the bridges differ](#why-the-bridges-differ) retains native import versus explicit read/follow, provenance, no common bootstrap policy, and actual-provider limits. A link is not treated as a universal import. |
| Qualified size target and compact wording | **Retained established constraint; identified wording compromises recorded as accepted in the existing design account.** [Portability](../behavior/baseline.md#portability-and-standing-context-qualifications) and [wording trade-offs](#current-wording-trade-offs) retain the exception, review conditions, and limited acceptance. This does not extend acceptance to further precision loss. |
| Effort baselines, mandatory inquiry framing, and routine-report suppression | **Historical/superseded.** The alternatives below preserve their control and visibility rationale; current §§2.3–2.4 and 3.7 describe different mechanisms. |

### Historical source and interpretation

The historical source is [`README-maintainers.md` on PDSA at `9a078b3`](https://github.com/indisoluble/AGENTS-spec/blob/9a078b3833297ca33357391bb60e6d469bceeff4/README-maintainers.md). The current guide descends from it through accepted-contract alignment and later moves; relevant records include [`c4bc519`](https://github.com/indisoluble/AGENTS-spec/commit/c4bc51938ef7a4890f1f353e46e764f226c3b42f) and [`96947a8`](https://github.com/indisoluble/AGENTS-spec/commit/96947a8a8644e744525c0209dcc2a5b290f3589f). These identify repository evidence, not new external-source verification. Historical explanations below preserve significant mechanisms and reasons without restoring their operative force. The current explanations linked beside them own present interpretation.

### Superseded effort-baseline checkpoint

**Historical mechanism.** The PDSA version established both an increment baseline when planning that increment and a cumulative-task baseline at task start, using requester direction where supplied and otherwise agent judgment without routine notification. Baselines could be qualitative; they were working state rather than token quotas, worksheets, or required project records. New evidence changed current estimates, but growth was assessed against the established baselines rather than the latest estimate. A material increase required reassessment, an explanation of what changed, unfinished work and uncertainty, and the smallest useful complete next step, followed by requester direction before taking on the added work, even within an unchanged broad objective and authorization.

Only requester direction could revise a baseline. Approval of disclosed growth revised the affected baselines to include only that commitment, avoiding repeated consultation for already approved effort while leaving later growth detectable. A new increment baseline could not absorb growth already discovered without direction, and new increments, attempts, and handoffs could not reset the task baseline. Handoffs transferred the task baseline, any unfinished increment's baseline, and still-relevant approved revisions. A continuing agent missing them recovered the state or obtained direction before further effort-bearing work rather than setting fresh baselines.

**Reason and trade-off.** A scope boundary alone did not prevent unexpectedly heavy work within one increment or cumulative growth through many small additions. Keeping original comparison points made those changes visible across attempts and contexts. The mechanism required judgment about qualitative baselines and material growth; it supplied no automatically enforced quota. The historical CSV walkthrough's unexpectedly larger shared-parser redesign therefore triggered a growth checkpoint in whichever phase it was found.

**Current replacement.** [Authorization and requester decisions](#authorization-and-requester-decisions) explains requester-imposed limits, evidence-based cumulative reassessment, and consequential-direction consultation. Current §2.3 does not require agent-created increment/task baselines or consultation solely because an agent estimate grows. The current parser example distinguishes a routine correction from a new consequential direction or material departure. The old baseline state and automatic material-growth checkpoint are not current handoff or continuation requirements.

### Superseded inquiry announcement and stopping rule

**Historical mechanism.** Beyond exempt context gathering, inquiry required advance framing before starting or continuing: question, scope, objective, effort limit, and needed evidence. The agent could choose a useful bound without requester approval of every limit; there was no default amount, unit, or formula. Obtaining the evidence or reaching the declared limit ended that inquiry even if the answer remained unknown. A report then identified unmet acceptance conditions, missing evidence, uncertainty, and any need for broader research or design direction. The report itself was not an approval checkpoint.

Existing scope and authority could permit a newly framed bounded attempt, but requester caps, checkpoints, unresolved consequential intent, missing evidence blocking safe continuation, and the historical material-growth rules still controlled it. Neither an exhausted allowance nor a negative finding granted authority. The declaration made commitment visible before consumption, but judgment about the bound supplied neither a tool-enforced timeout nor a token quota. Context gathering, including reading existing project documentation for a blocking question, remained exempt from that inquiry framing while still subject to scope and effort controls.

**Current replacement.** [Completion, predictions, and bounded investigation](#completion-predictions-and-bounded-investigation) preserves the purpose-based boundary while explaining timely uncertainty/significance notification, including the already-communicated exception, and actual bounded conduct without a five-element announcement or declared allowance. Sufficient evidence ends inquiry; insufficient evidence at an increment's bounds requires reassessment before justified further investigation. There is no automatic inquiry-end report or new announcement per attempt. Optional requester limits remain binding. Removing the older framing mechanism establishes no behavioral equivalence or token-efficiency result.

### Superseded report suppression and consultation strength

**Historical report choice.** Routine report drafting as well as output was prohibited unless requested or required. Suppressing drafting aimed to avoid consuming effort preparing narration merely to withhold it. Reporting consolidated work at completion, handoff, or input requests, with advance disclosures affecting authorization or the next decision and an explicit inquiry-end report. Other disclosures had to join the next consolidated report unless earlier timing was explicit; this was mandatory, unlike the current recommendation that other information should normally join that report. Record maintenance retained its own timing. The trade-off described in that version was less routine visibility while authorized work continued; fewer reports were not measured token savings and reserved no review opportunity.

**Current replacement.** [Reporting and continued execution](#reporting-and-continued-execution) explains the recommendation to minimize routine reports and keep intermediate communication concise and useful, with specific mandatory timings for consolidation, initial framing, inquiry notification, and advance disclosures affecting authorization or a decision requiring input. Useful intermediate updates are possible; the older categorical drafting/output ban and inquiry-end timing are superseded.

**Historical consultation strength.** The PDSA account treated asking before unsettled consequential choices as a SHOULD, while material unresolved intent or permission and the baseline-growth checkpoint had their own mandatory force. The current [requester-interaction account](#authorization-and-requester-decisions) distinguishes the MUST for a new consequential architectural or lasting design direction or material departure unless specifically authorized, from the SHOULD for other unsettled material choices. Historical strength must not be substituted for the current clause. In both designs, a report or ADR could not retroactively authorize a choice.

### Superseded method-reference inquiry exemption

The historical reference account exempted narrow consultation to clarify a material method ambiguity from §2.4 inquiry framing, while requiring disclosure of the ambiguity, source, and interpretation and forbidding imported obligations. This kept a clarification link from becoming a full research assignment.

The current [reference boundaries](#principles-and-reference-boundaries) retain limited consultation and no imported rules, but qualifying consultation now follows the purpose-based context/inquiry distinction and notification/conduct requirements, including the already-communicated exception. Clear rules must not be researched, and broader research needs explanation and requester direction. The former blanket inquiry exemption is historical only.

