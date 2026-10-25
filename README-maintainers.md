# The design of AGENTS.md

[AGENTS.md](AGENTS.md) is a reusable, opinionated contract with two ordered objectives: control token consumption through bounded, proportionate work, then keep the requester informed and in control of consequential direction. Necessary reasoning, work, and validation remain requirements within each increment. Canonical documentation preserves shared knowledge for humans and future agents. This guide explains the design choices, trade-offs, and constraints that inform changes to the contract.

For adoption, use [README.md](README.md). For practical guidance, use [Getting more from AGENTS.md](README-powerusers.md). This guide has four parts:

1. [Design overview](#design-overview): the [design goals and boundaries](#design-goals-and-boundaries) and [a worked task](#how-the-design-works-in-a-task) showing how the parts connect.
2. [Design choices](#design-choices): [workflow choices](#workflow-design-choices) for the contract's layers, scope, learning, investigation, and requester control; [engineering choices](#engineering-choices) and [documentation choices](#documentation-choices) for methods, reasons, and conditions; and [why the bridges differ](#why-the-bridges-differ) across tools.
3. [Evolving the contract](#evolving-the-contract): [method selection](#choosing-or-replacing-methods), [portability](#keeping-the-contract-portable), and [current wording trade-offs](#current-wording-trade-offs) as constraints on changing `AGENTS.md`.
4. [Design reference](#design-reference): [design scenarios](#assessing-design-changes) for reviewing changes and the exact [reference assignments](#principles-and-reference-boundaries).

For a sequential understanding of the design, read the parts in order. For a proposed change, start with the relevant design choices, then use the evolution constraints and design reference to assess it.

## Design overview

### Design goals and boundaries

The motivating risk is especially visible in a new or poorly documented project. Without established requirements, interfaces, decisions, and conventions, planning and autonomous design have fewer constraints. Even a bounded objective can permit a large amount of work. Small, meaningful increments limit the next commitment, while prior consultation reserves consequential architectural and lasting design direction for the requester unless the specific choice is already authorized. The absence of an established architecture does not confer unlimited design authority.

Small increments are the principal mechanism for controlling work and speculative token use. Developing detail only when needed avoids designing distant work before its decisions can be made. Before expanding planned work or starting another increment or attempt, cumulative reassessment connects the next step to evidence, the task objective, established direction, and limits. Bounded inquiries constrain effort spent on a blocking question. Plan–Do–Study–Act (PDSA) turns results into the next decision. Engineering practices protect quality, while documentation preserves facts and reasons so humans and future agents can continue without reconstructing them. Adequate analysis, completeness, and validation constrain every effort-saving choice.

Reports consolidate unreported work at task completion, handoff, or when seeking requester input. Routine progress reports are suppressed unless requested or otherwise required. The brief initial task outline and advance inquiry framing make upcoming work visible without creating approval checkpoints. Routine execution remains autonomous within authorization and direction; requester-imposed limits and consequential decisions retain their own consultation triggers. These mechanisms provide no token quota or guarantee of savings, and total consumption may remain substantial. The [practical explanation](README-powerusers.md#understanding-token-use) distinguishes reports and optional forecasts from consumption measurements.

The contract is self-contained. Guides explain it and bridges help tools apply it; neither supplies hidden operating duties. Project facts, build commands, requirements, and architecture come from the adopting project's code and documentation. This separation supports reuse without embedding an application's design in generic instructions.

Requester instructions take priority within the tool's actual hierarchy and permissions. The tool determines discovery, scope, and precedence of directory instructions, which may add subtree rules only when compatible with the root contract. The contract cannot supply capabilities, enforce permissions, or override native approvals. Its protection of instruction files and its authorization rules for external actions keep those limits explicit. It also does not supply a complete product-development process, branching strategy, workflow engine, or framework tutorial. Established methods cannot invent missing requirements or requester authority.

### How the design works in a task

Consider the CSV-import scenario from the [practical walkthrough](README-powerusers.md#from-a-request-to-a-result): report invalid rows and continue with valid rows. The **task objective** is that overall outcome. An **increment** is the next deliberately small, bounded step toward it, normally useful, understandable, reviewable, and verifiable on its own.

[PDSA—Plan–Do–Study–Act](https://deming.org/explore/pdsa/) begins with that request. Plan selects and bounds the work; Do performs it; Study assesses completion and the approach; Act uses the findings. Throughout, progression guards determine whether work may proceed, and triggered rules apply when their conditions arise; the [layer design](#three-interacting-layers) explains this division.

1. **Plan:** establish the objective and permitted work, then inspect the relevant project context. Suppose the requirements settle the input format, invalid-row rules, and line-number convention; existing tests support the reader's suitability; and inspection shows that field-count validation is missing. The row-processing code exposes the fields, header, and line number, suggesting a local implementation.

   This evidence supports choosing field-count validation: it advances an agreed requirement, addresses one concern, and can produce a useful, testable result without implementing every remaining invalid-row rule. The scope includes the affected code, tests, and documentation. Its limited dependencies and expected ease of reversal support a small commitment; neither substitutes for validation.

   Define **acceptance conditions**—reject mismatched rows, report their line numbers, and continue with valid rows, including one after a rejection—and a **prediction** that the existing row boundary will support the approach. These derived conditions follow the agreed requirements and define this increment's completion; they are not new system requirements. Selection, scope, conditions, and approach can be refined together as context becomes clear, within the governing instructions and requirements. Later work remains at outline level.

   The initial planning statement in the [practical walkthrough](README-powerusers.md#from-a-request-to-a-result) relates the overall task to the first increment's objective and bounds. Preliminary context makes the plan meaningful; communicating it before substantial work lets the requester understand the direction and next action. It requires neither a cost forecast nor detailed planning of later increments, and creates no approval checkpoint.
2. **Do:** implement the validation using current project conventions and Simple Design. Add relevant tests and update affected documentation at its authoritative location. Significant lasting choices need ADRs; choices requiring prior consultation must receive requester direction before adoption or implementation.
3. **Study:** check acceptance before completing the increment, including a valid row after a rejection. Separately assess whether the predicted local approach sufficed. Failed, unavailable, or omitted checks remain subject to disclosure under the reporting rules.
4. **Act:** use the evidence to retain, revise, or discard the approach within authorization. Material findings that are durable project knowledge trigger the [record rule](AGENTS.md#32-durable-findings-and-permanent-records). The [composition rules](AGENTS.md#4-how-the-layers-compose) then lead to finishing, a handoff, seeking required direction, or planning the next increment already covered by authorization. Continuing to another increment does not require drafting or emitting a routine report; reporting follows [§3.7](AGENTS.md#37-reporting).

The initial choice therefore depends on what Plan establishes. Unsettled consequential requirements need requester input; uncertainty about the reader may call for a bounded investigation. A new consequential design direction also needs prior requester direction unless specifically authorized. Within those boundaries, choosing and defining routine increments remains the agent's responsibility.

The example connects the design's parts. Requirements provide intended behavior; inspection and existing checks establish the starting point; Study supplies new evidence; Act uses it to inform subsequent Plan phases. Records preserve durable material findings and lasting choices; transient task facts are only reported when the reporting rules require it. The supported local validation approach may help plan another rule, while evidence of wider parser limitations changes the basis for that next decision.

The field-count result can therefore inform another authorized validation increment before any routine chat report is produced. A local implementation correction can proceed within the existing direction and limits. A proposal to change the shared parser's established error contract instead requires requester direction before adoption or implementation unless that specific change is already authorized. At completion, handoff, or when seeking input, the agent consolidates unreported work. A requested operator guide could be another increment, shaped by its reader's need. Neither a completed step nor a named method automatically creates an ADR, guide, or approval requirement.

The [practical walkthrough](README-powerusers.md#from-a-request-to-a-result) shows the user-facing interaction. The following sections explain the reasons and boundaries behind it.

## Design choices

Each choice below connects a design problem with the approach taken, its reasons, and its trade-offs. The linked `AGENTS.md` clauses remain authoritative for exact operating behavior.

### Workflow design choices

#### Three interacting layers

The contract separates three questions that need answers throughout a task:

| Layer | Question it answers | Role in the design |
| --- | --- | --- |
| [Work cycle](AGENTS.md#1-work-cycle) | What is the agent doing with the current increment? | Organize planning, execution, assessment, and use of the findings. |
| [Progression guards](AGENTS.md#2-progression-guards) | May this work proceed, or is requester direction needed? | Check authority, scope, unresolved decisions, requester limits, cumulative reassessment, inquiry bounds, and permission to continue. |
| [Triggered rules](AGENTS.md#3-triggered-rules) | Has something happened that creates a duty or permission? | Apply the relevant rule when, for example, a requirement changes, a durable finding emerges, documentation is affected, or a report becomes due. Each rule retains its own strength and conditions. |

The same action can involve all three. While planning an authorized importer change, the agent might discover a material, durable parser limitation and propose changing the parser's established error contract. Planning identifies the issue, the record rule preserves the finding, and the consultation guard requires requester direction before adopting or implementing that departure unless specifically authorized. Naming a cycle phase settles neither the record duty nor decision authority.

The division follows how these concerns behave. Authorization, limits, and requester involvement can matter in any phase, and a durable finding can emerge while planning as easily as while acting. Placing such rules inside one phase would suggest they apply only there, or require readers to reinterpret earlier phases after reaching later material. Presenting the cycle first shows the ordinary path; the guards then make the control state explicit; triggered rules stay independent of phase. A final [composition section](AGENTS.md#4-how-the-layers-compose) states how the layers combine: work proceeds through the cycle, guards govern relevant transitions and decisions, triggered rules apply when their conditions arise, and after Study and Act the agent completes, hands off, seeks required direction, or returns to Plan for another increment already covered by authorization.

No layer grants authorization by itself. A next cycle step, a satisfied guard, or a fulfilled duty never extends what the requester and tool permit, and completing an increment, reporting, recording a decision, discovering a finding, or exhausting an inquiry creates none. Guards are not additional phases; triggered duties authorize no otherwise unauthorized work, and triggered permissions authorize nothing beyond their terms.

This organization expresses design intent: making the operating model and its cross-cutting relationships explicit while preserving normative behavior. The repository holds no measurement showing that it improves human comprehension, agent adherence, or token use.

#### Small commitments with sufficient depth

The requester supplies goals, permission, and relevant constraints. The agent supplies decomposition, acceptance conditions, proportionate planning, validation, cumulative reassessment, and recognition of required consultation. These standing responsibilities let an ordinary outcome-oriented request start useful work without requiring the requester to monitor tokens or supervise every correction. A requester may still select a step or add review points.

Within Plan, increment selection connects the requested outcome and permission with current behavior, relevant dependencies, and available evidence. The agent looks for the smallest useful result that can be completed within scope, including the affected artifacts and checks. When blocking uncertainty prevents a sound implementation choice, obtaining bounded evidence can itself be the useful result.

The [four decision factors](AGENTS.md#22-decisions-and-requester-interaction)—scope, uncertainty, consequence, and reversibility—guide that judgment. Scope includes affected behavior, artifacts, dependencies, and system boundaries. A few changed lines can affect many callers or an irreversible migration; a narrow, understood, low-impact, reversible change can use brief inspection, action, and validation. Reporting follows its own triggers and remains proportionate.

These criteria constrain selection without prescribing a numeric score, an exhaustive comparison of possible increments, or a uniquely correct sequence. Requiring a complete ranking or detailed backlog before starting would expand the initial planning commitment. The design instead calls for enough reasoning to support the next useful step and uses its evidence to refine later work. This contributes to the token-control goal while preserving the analysis and validation needed for a complete result.

Depth follows the next decision at the current abstraction level. Architecture analysis may need careful examination of boundaries, alternatives, and risks without specifying every future API or function. Later work stays at outline level until the next decision needs detail; depth follows uncertainty, consequence, risk, reversibility, and proximity to execution. Explicit authorization can cover broader analysis at the relevant abstraction level.

Completeness is assessed within the increment's scope. Evidence, enabling infrastructure, or migration groundwork can be useful results as well as functionality. Before a step that cannot stand alone, the agent explains why, what remains usable or testable, and how to undo it. Recovery reduces the cost of a mistaken approach; it grants no permission for destructive effects. A required stop may leave work incomplete, while review-boundary coherence still applies. A small scope cannot excuse shallow reasoning, omitted dependencies, or incomplete work presented as finished.

#### Learning throughout the work

The [Deming Institute's PDSA account](https://deming.org/explore/pdsa/) connects an approach and expected result with observation and the next decision. Small increments bound commitments; PDSA's contribution is learning which approach remains suitable and what to do next. Passing tests alone does not establish that learning role: the implications still inform Act and subsequent planning.

The contract's [work cycle](AGENTS.md#1-work-cycle) starts with the request. Plan includes context gathering, the overall objective and permitted work, outlining an approach, and selecting the next increment. Study assesses completion and observations; Act uses those findings to retain, revise, or discard the approach within authorization. Results can reshape later detail without changing the agreed outcome or granting more authority.

Terms and the layer overview precede the work cycle. Methods appear near their principal contribution—engineering practices in Do, validation in Study, and documentation and decision methods among the triggered rules—but apply whenever triggered in any phase, and the progression guards apply throughout. Tests can be planned before implementation; decisions and documentation are maintained as facts emerge. Phases can overlap or repeat, and routine work needs no worksheet, formal experiment, or separate phase reports.

PDSA's Plan phase organizes reasoning. A tool's Plan mode has its own proposal and approval procedures. Neither expands authorization. These distinctions let the workflow apply proportionally to implementation, investigation, and documentation without inventing separate mandatory deliverables.

#### Completion, predictions, and bounded investigation

The contract keeps three ideas separate because they answer different questions:

| Concept | Question it answers | What changes when evidence contradicts it? |
| --- | --- | --- |
| System requirement | What behavior must the system provide beyond this task's execution? | A failure supplies evidence that the required behavior may be unmet. Changing the requirement still needs the relevant authority. |
| Acceptance condition | What observable result is needed to complete this increment? | Missing evidence leaves completion unestablished. Any revision must respect the condition's source and existing authority. |
| Prediction | What result does the agent expect from its approach or experiment? | The evidence informs whether to retain, revise, or discard that approach. Revising the prediction changes neither requirements nor acceptance conditions. |

Study uses acceptance conditions to assess completion and predictions to assess the approach. Keeping these comparisons separate allows the agent to revise an unsuccessful approach without weakening what the increment must deliver. An implementation can meet its acceptance conditions through a different approach from the one initially predicted.

The system-requirement boundary depends on what the authorized work establishes. If it establishes or changes behavior required of the system beyond the current task's execution, that behavior is a new or revised system requirement, whatever its source. It needs an authoritative owner and the [EARS requirement form](AGENTS.md#31-new-or-revised-system-requirements). A task objective, acceptance condition, or requester statement does not become a system requirement merely because it was stated. Restating a requirement that already has an authoritative owner creates no duplicate, and analysis or review alone cannot create or change requirements.

The agent first identifies requirements and acceptance conditions already set by the requester or authoritative project sources. It then inspects relevant context before deriving or refining the remaining increment conditions. This order prevents the agent from settling its own completion criteria before reading the evidence those criteria depend on.

Revision authority follows the source of each condition. Requester-supplied requirements or conditions change only with requester authority; canonical requirements change only through authorized requirement work; agent-derived conditions can be refined only within requester instructions, project requirements, scope, and decision authority. A failed check or difficult implementation never justifies weakening, replacing, or reinterpreting any of them, so failed validation cannot lower the completion bar.

This separation allows an investigation to succeed by disproving an assumption. Evidence that a reader splits a quoted comma can answer a question about its behavior, while an implementation required to preserve that field remains incomplete. A successful sample also supports only the conclusion justified by that sample. The [practical investigation example](README-powerusers.md#when-an-investigation-is-needed) develops both outcomes.

Inspecting relevant code, callers, tests, configuration, and directly related dependencies to establish starting context, and all reading of existing project documentation, are context gathering. The documentation exemption still applies to a material blocking question; no inspection-by-inspection announcement is needed. Scope, limits, proportionate work, and cumulative reassessment apply throughout.

Beyond context gathering, the [inquiry guard](AGENTS.md#24-context-gathering-and-bounded-inquiry) turns on the purpose of resolving material uncertainty about how to proceed that blocks the next decision. This purpose-based distinction matters because the same command can serve different jobs. It might execute an already settled task, validate an implementation, or investigate which approach to choose. Unknown output alone does not distinguish those jobs. Conversely, a documented procedure used to investigate a blocking approach question remains inquiry. The [practical distinctions](README-powerusers.md#when-an-investigation-is-needed) show these different uses of measurements and tests.

An inquiry's advance statement ties a proportionate effort limit to its question, scope, objective, and evidence sufficient to conclude or reassess. It makes the intended boundary visible before the investigation; revised framing must precede the actions it changes. The [reporting design](#reporting-and-continued-execution) explains why this framing and the initial task outline use chat despite suppressing routine narration.

The evidence threshold defines what would suffice to conclude or reassess; the **investigation effort limit** bounds effort even if that evidence is not obtained. This addresses two failure modes: treating any output as sufficient evidence and continuing merely because the answer is still unknown. The limit is proportionate, with no prescribed amount, unit, or selection formula; the practical example's one-attempt allowance is illustrative. An inquiry limit is a stopping condition, distinct from an optional forecast. [Requester limits](#authorization-and-requester-decisions) can constrain the task across attempts; neither an estimate nor its revision overrides those limits or the inquiry's framing.

Obtaining the evidence or reaching the limit ends the inquiry, not necessarily the task. [Study and Act](AGENTS.md#13-study--assess-completion-and-learning) govern assessment and what follows. Reporting occurs at task completion, handoff, or when seeking requester input, with earlier disclosures where required. There is no automatic inquiry-end message. An ended inquiry need not be a completed increment or task: ending an unsuccessful attempt does not supply missing acceptance evidence.

Another attempt needs advance chat framing explaining why the preceding result justifies it. This permits useful work under existing authority while making the next bounded attempt visible. The [progression guards](AGENTS.md#2-progression-guards) still require cumulative reassessment and compliance with scope, direction, and requester limits. Repeated attempts cannot reset a cap or bypass a checkpoint, and without evidence justifying a next increment the agent seeks direction. A changed forecast alone is not a continuation barrier.

#### Authorization and requester decisions

An increment limits work undertaken at once; a report can summarize several increments; a checkpoint reserves a decision for the requester. Ordinary increments can [continue under existing authorization](AGENTS.md#25-continuing-to-another-increment) without routine reports. Their completion supplies no additional permission and creates no automatic pause.

The [effort and limit guard](AGENTS.md#23-effort-estimates-and-requester-limits) separates forecasting from decision authority. An optional agent estimate describes anticipated effort; it neither sets a limit nor creates a checkpoint when revised. An informal requester expectation is not automatically binding either. Explicit requester-imposed effort or scope limits and checkpoints remain binding, and material ambiguity about a statement's force requires clarification under §2.2.

This distinction keeps the agent responsible for managing execution without making the requester supervise forecast accuracy. Preliminary context supports a useful initial plan, not a compulsory estimate. The requester controls consequential direction and any limits they impose; routine local corrections remain autonomous within that direction and authorization.

Cumulative reassessment prevents each small increment from being considered in isolation. Before expanding work or starting another increment or attempt, the agent considers progress, remaining work, direction, and applicable limits, and justifies the next increment's contribution from evidence. A series of small changes cannot authorize unrelated improvements or conceal a material departure from agreed direction. If no next increment can be justified, the agent seeks direction.

This does not impose a default cumulative budget. Additional justified increments may consume more effort than anticipated while remaining authorized and architecturally consistent. Small increments and bounded inquiries constrain how work proceeds; they do not guarantee low total consumption. The [practical examples](README-powerusers.md#when-the-work-grows-unexpectedly) distinguish a revised forecast, an explicit checkpoint, and a consequential parser change.

In the [requester-interaction guard](AGENTS.md#22-decisions-and-requester-interaction), the [requirement keywords](AGENTS.md#terms-and-requirement-keywords) preserve distinct strengths:

- Material unresolved intent or permission must be taken to the requester; missing consequential constraints must be agreed as needed.
- Before adopting or implementing a new consequential architectural or lasting design direction or a material departure from established direction, the agent must obtain requester direction unless the specific choice is already authorized.
- Other unsettled choices materially affecting the decision factors, optimization, or lasting complexity warrant asking first, with justified SHOULD exceptions.
- Easily reversible routine local details may be chosen within agreed limits; material assumptions remain visible.

A broad outcome does not specifically authorize every consequential design choice that might achieve it. This matters in new projects as well as established ones: absent architecture is not a delegation of unrestricted architectural authority. Conversely, a local correction within the established design does not become a mandatory consultation merely because the original implementation approach failed.

A SHOULD exception cannot bypass a MUST checkpoint or invent a consequential constraint. Recording an ADR or reporting afterward cannot replace required prior direction. Consequential choices made without prior direction still require prominent reporting of reasons, effects, uncertainty, and revision or reversal options. Native permissions and approval controls remain the enforceable boundaries.

Analysis and review can establish lasting project knowledge before implementation, so the contract separates permission to write from the conditions that call for a record. The [limits on assessment writes](AGENTS.md#21-authority-and-scope) decide which writes an assessment-only task may make at all, alongside the other limits on permitted work. The [material-findings rule](AGENTS.md#32-durable-findings-and-permanent-records), [decision rule](AGENTS.md#33-significant-decisions-adrs), and [debt rule](AGENTS.md#34-technical-debt) then decide whether a record is due. Each has its own trigger and strength, applying whenever its conditions arise.

Keeping these questions separate preserves both restraint and knowledge retention. Permission to record debt cannot make an optional debt entry mandatory. A required record cannot authorize implementation, new or changed system requirements, accepting or changing decisions beyond existing authority, unrelated documentation repairs, or backfills. A **permanent record** is the canonical project document owning the topic; chat and working notes do not fulfill that role. It preserves the finding and evidence for future work; neither that document nor a chat discussion supplies permission to implement the recommendation.

The findings trigger requires both materiality and durability so that assessment retains what later work needs, including lasting learning from discarded approaches, without becoming a work log. Transient task facts, such as a temporary CI outage, follow only the reporting rules. If no suitable owner exists, a minimal record preserves the required finding and evidence without starting a documentation backfill: no placeholders or empty sections are added, and other arc42 gaps remain proposals. If the write is prohibited, the record remains unfinished work; reporting the finding in chat does not satisfy that obligation.

Verified factual corrections are a separate permission because they align an existing description of current project facts with its owner. Excluding requirements, decision records, and protected instruction files prevents that permission from being used to change intended behavior or accepted decisions. All these writes remain subject to authorized scope, [requester restrictions](AGENTS.md#21-authority-and-scope), [protected-file rules](AGENTS.md#38-instructions-protected-files-and-external-actions), and tool permissions and approvals, which can prevent them. Broader documentation repairs and external actions retain their own authorization requirements. The [practical examples](README-powerusers.md#records-during-review-and-exploration) show each case and the effect of a no-edit instruction.

#### Reporting and continued execution

Completing an increment and reporting to the requester serve different purposes. PDSA requires the work to be assessed and its findings used, even when no chat report follows. [AGENTS.md §3.7](AGENTS.md#37-reporting) consolidates unreported work at task completion, handoff, or when seeking requester input. It prohibits drafting or outputting routine progress reports at other times unless requested or required.

Suppressing drafting as well as output avoids preparing reports merely to hold them back from chat. The design allows the agent to use evidence for the next authorized step while keeping information needed for a requester decision timely. Disclosures affecting authorization or a decision requiring requester input therefore precede the affected work. Other disclosures join the next consolidated report unless earlier timing is explicit.

The initial task outline and inquiry framing have explicit advance timing. After proportionate preliminary context gathering, the agent communicates the task outline and first increment's objective and bounds before substantial work. Inquiry framing communicates the question and boundaries before starting or acting on revised framing. One concise message can cover both when applicable. Neither statement needs an effort forecast or creates an approval checkpoint.

These statements make the intended direction and upcoming work understandable while the requester can still correct a misunderstanding. Private planning or a retrospective report cannot supply that advance communication. The statements do not reserve a review interval, reveal exact consumption, or prove that the agent respected its bounds. Required consultation, rather than an informational message alone, gives the requester control before a consequential choice.

The trade-off is a brief message at those specific points, even when the agent already has authority to proceed. There is no mandatory planning message for each later increment, worksheet, or new record type. Unchanged inquiry framing needs no repetition. Ending an inquiry does not itself require another message, and nonblocking debt disclosures wait for the next reporting occasion.

Maintaining project knowledge has its own timing. Material findings, decisions, and affected documentation retain their owners and maintenance triggers; their maintenance does not wait for the report. The agent can therefore update a required record during the work and describe that update in the later consolidated report. No separate reporting log or record is required for every increment. Tool instructions and requester-selected reporting remain applicable.

A handoff preserves the information needed for another person or agent to continue: the objective and established direction, applicable limits and consumed allowances, the next or unfinished increment's objective, bounds, and acceptance conditions, and relevant inquiry framing, findings, and remaining allowance. This retains permission and evidence across a change of context without making optional forecasts mandatory task state. Missing authorization or limit information must be recovered or resolved before dependent work.

The trade-off is less routine visibility during autonomous work and a consolidated account at the next reporting occasion. Reporting alone reserves no time for review and creates no approval checkpoint. Scope limits, bounded investigations, cumulative reassessment, and required consequential consultation continue to control the work; fewer reports establish no measured token saving.

Reports remain proportionate and follow the contract's requirements for content, file delivery, and blocked-edit fallbacks. The [usage guide](README-powerusers.md#assess-the-result) explains what the requester receives.

### Engineering choices

#### Simple Design: choosing what the current solution needs

Beck's [Simple Design, explained by Fowler](https://martinfowler.com/bliki/BeckDesignRules.html), supplies four criteria: meet requirements and pass tests, express intent, avoid duplicated knowledge, and retain only necessary elements. They assess the current solution; fewer classes or lines alone cannot establish simplicity.

Hard memory, latency, throughput, concurrency, cost, or scale requirements may justify complexity. An imagined future extension does not provide equivalent evidence. Supporting one agreed input format can be complete without a framework for unspecified formats, while still including its necessary error handling and checks. A documented optimization strategy supplies project context and is a strong default; a task that conflicts with or materially extends it remains subject to the consultation rules. Material trade-offs remain visible.

#### DRY: keeping knowledge consistent as work progresses

The [Pragmatic Programmer's DRY account](https://media.pragprog.com/titles/tpp20/dry.pdf) concerns knowledge that would otherwise need independent maintenance in several places. Canonical ownership reduces the risk of divergent facts, rules, or explanations across code and documents.

A setting can own a retry limit while a guide explains its purpose and links to it. Two unrelated limits may have the same value without representing shared knowledge. Necessary test, example, summary, generated, protocol, migration, and compatibility copies can remain with a clear canonical owner and update process. Resemblance alone supplies no reason to merge them.

#### Component boundaries, refactoring, and validation

Clear responsibilities, limited coupling, visible side effects, and explicit resource ownership make the effects of a change easier to understand. The [public tips](https://pragprog.com/tips/) and [shared-state extract](https://media.pragprog.com/titles/tpp20/shared-state.pdf) support these concerns; their exact assignments appear [below](#principles-and-reference-boundaries). Separating concurrent coordination from sequential logic where practical supports clear ownership without prescribing a universal asynchronous architecture.

[Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) preserves observable behavior. An intended and authorized behavior change needs corresponding requirements, tests, and documentation. Documented design invariants protect promised properties; project patterns can change through scoped, justified, validated improvements. Neither distinction requires preserving a defect when changing it is intended and authorized.

The dead-code condition matters because registration, reflection, or external callers may make apparently unused code reachable. Clear unreachability or direct obsolescence from the authorized change is needed for removal *as dead code*. Explicitly authorized removal of live functionality is a different case.

#### Validation and test evidence

Relevant available checks against acceptance conditions are mandatory before completing each increment, independently of whether a report is produced then. Appropriate tests for behavior changes, defect repairs, and clarified edge cases are a SHOULD default with justified exceptions. Validation covers affected behavior, risk, and hard operational limits for every work type; passing tests cannot replace a missing requirement or necessary check. Failed, unavailable, and omitted checks must be disclosed under the [reporting rule](AGENTS.md#37-reporting); any need for requester involvement still follows the [progression guards](AGENTS.md#2-progression-guards).

Distinguishing check availability from acceptance prevents a tooling limitation from being treated as successful validation. It also allows sufficient alternative evidence to establish a condition when the contract's substitution rules permit it.

Sufficient alternative evidence may substitute only when the original check is unavailable and is not specifically required. Availability depends on current authorization, tool access, permissions, credentials or resources, and prerequisites with ordinary expected setup. Convenience does not decide availability: a relevant available acceptance check still runs even if an alternative could provide equally sufficient evidence. Missing access or resources, or materially more work needed to run a check, must be disclosed and handled through the authorization, limit, and reassessment rules. More work alone does not create a checkpoint.

Without sufficient evidence, the condition remains unverified and validation incomplete unless the condition is validly revised under existing authority. Disclosure alone cannot establish it. A pre-existing failure is assessed for relevance and disclosed, without automatically blocking unrelated work. The [practical validation examples](README-powerusers.md#assess-the-result) distinguish available checks, equivalent local checks, insufficient mocked evidence, and a specifically required CI result.

[Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html) makes a unit test's starting conditions, action, and expected result understandable. For a quoted field containing a comma, those parts are the sample, the parser call, and the intact-field assertion. The contract requires neither literal labels nor a testing framework, and prohibits weakening tests merely to pass.

#### Focused techniques and how they work together

These techniques support Simple Design when their benefits justify their costs. Their selection grants no authority for unrelated restructuring or new dependencies.

**Gross's [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/)**

Make behavior understandable near its implementation while balancing separate responsibilities and canonical ownership. A clearly named validation call can keep the control flow readable while the rule stays in its canonical owner. The contract does not require inlining everything or adopting htmx.

**The [Law of Demeter](https://www2.ccs.neu.edu/research/demeter/demeter-method/LawOfDemeter/general-formulation.html)**

Use direct collaborators' interfaces to reduce dependence on other components' internal structure. The trade-off is reduced coupling versus interface complexity: forwarding methods that add no useful boundary can make the code harder to follow. The contract therefore weighs coupling and clarity rather than imposing a blanket ban on chained access or requiring an aspect-oriented solution.

**Fowler's [Value Object](https://martinfowler.com/bliki/ValueObject.html)**

Use values equal by contents when a domain type clarifies meaning or validation. Favor immutability where practical while preserving required identity and state changes. The contract makes this a conditional design choice; it requires neither wrapping every primitive nor adopting Domain-Driven Design.

**The [inheritance extract](https://media.pragprog.com/titles/tpp20/inheritance-tax.pdf)**

Prefer interfaces, protocols, and composition when they reduce coupling, and polymorphism over complex conditional dispatch when it improves clarity. The conditions matter: these preferences do not justify abstractions based on speculation alone or prohibit suitable inheritance.

**Fowler's [dependency injection](https://martinfowler.com/articles/injection.html), “Separating Configuration from Use”**

Separate assembly from use when this improves separation, clarity, or testing. Supplying a clock as a parameter can suffice. Configuration normally stays at assembly, initialization, or external-system boundaries; no container or new dependency is required.

### Documentation choices

Different project artifacts answer different questions. Requirements describe intended behavior. Accepted decisions retain choices and reasons. Architecture describes boundaries and guarantees. Schemas and package metadata declare their own constraints. Code, tests, and execution provide evidence of implemented behavior. Examples and notes govern only when explicitly labeled as rules.

These roles explain why executable behavior does not automatically overrule a requirement. If an implementation behaves differently from a required format, that disagreement is evidence to assess. The existence of the implementation does not by itself authorize changing the requirement. The contract intentionally has no global precedence ladder among these artifacts. An earlier total ordering was removed because a single ranking cannot fit artifacts that own different kinds of knowledge.

The agent identifies the governing artifact from the kind of knowledge and its canonical owner, and makes conflicting evidence and its own inferences visible. If ownership does not resolve a consequential conflict, it escalates under the requester-interaction rules instead of inventing a fallback order. Instruction files govern agent conduct rather than proving project facts. Requirements, constraints, and facts stated by the requester remain legitimate task context.

Documentation preserves a shared account of the project for maintainers, requesters, and future agents. Reading canonical facts and reasons supports Plan; producing a guide or updating affected documentation is Do work. Study checks acceptance; Act uses the findings and retains relevant learning. Requirement, record, decision, debt, documentation, and architecture duties are [triggered rules](AGENTS.md#3-triggered-rules) because their conditions can arise in any phase. They preserve knowledge as it emerges without authorizing work beyond their terms.

Updates follow **affected documentation**: the canonical owners of changed knowledge and the known documents that directly depend on it. A README repeating a changed value is affected even if it has no link to the owner and has not yet been read. Such dependents are typically known from the task, artifacts being inspected, explicit references, ownership, or established source/update relationships. A link alone makes a document worth checking, not necessarily editing.

This defines the required synchronization work without making every edit a repository-wide documentation project. Neither the synchronization duty nor coverage expectations authorize searching for unknown dependents, a wider audit, a backfill, or reorganization. Signs of wider staleness may lead to a proposal for additional work. Documentation-only work uses the same increment, validation, and review rules as other work. Current-system descriptions follow reality, with proposals and unfinished work clearly identified.

#### arc42: shared architectural context as the project grows

[arc42](https://arc42.org/overview/) supplies twelve architectural topics spanning goals and constraints, structure and operation, crosscutting concepts, decisions, quality, risks, and terminology. Shared content expectations aim to reduce reinvention and relearning across repositories. They give an empty project questions to answer as evidence develops, without requiring the entire design to be settled first.

Applicable topics set the target coverage. Architecture content uses known facts and keeps material unknowns visible; empty headings and invented details do not establish coverage. An uncovered topic is a known gap that triggers an improvement proposal, which authorized work should implement and the requester may decline, postpone, or limit, so a partial or minimal architecture document does not itself breach the contract. [Incremental documentation](https://faq.arc42.org/questions/B-14/) and [appropriate depth](https://faq.arc42.org/questions/B-4/) support keeping content useful as the system develops. [Quality scenarios](https://docs.arc42.org/section-10/) make goals assessable: “imports should be fast” still needs an agreed workload and measure.

One architecture document is the initial SHOULD default, using the existing documentation folder stated in `README.md`, otherwise repository-root `docs/`. Because root `docs/` is the standard default, `README.md` needs to state documentation locations only when they differ from it; creating a document in `docs/` therefore needs no `README.md` edit. This keeps early information together. An adequate existing arrangement can remain, and coherent parts can separate as reading and maintenance warrant it. Layout is flexible; known coverage gaps still require proposals and warrant improvements within authorized scope, subject to requester limits or deferral. Summaries link to canonical requirements and ADRs, while implementation detail stays near code and tests.

Topic 11 covers known risks as well as technical debt under the contract's definition. The risk category is not restricted to internal-quality compromises: external dependencies and operational circumstances can create known risks even when implementation quality is adequate. The distinction preserves the scope of [arc42's risks and debt topic](https://docs.arc42.org/section-11/) without classifying every risk as debt or importing an additional risk-management procedure.

#### EARS: making required behavior explicit

[EARS (Easy Approach to Requirements Syntax)](https://alistairmavin.com/ears/) gives natural-language requirements consistent condition-and-response patterns. The [practical guide's CSV example](README-powerusers.md#make-expected-behavior-explicit) illustrates this:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

The pattern exposes behavior to implement and check. It cannot decide whether to reject one row or the whole file, or define a row's line number for a particular format. Those remain project decisions. EARS applies to new or revised in-scope system requirements; unchanged requirements need no automatic conversion. The [contract](AGENTS.md#31-new-or-revised-system-requirements) owns the five patterns and combined state-before-event form. Rationale belongs with significant choices; EARS adds no mandatory rationale field to each requirement.

#### ADRs: preserving the reasons for lasting choices

[Architecture Decision Records](https://docs.arc42.org/section-9/) retain reasons that code alone may not reveal. A streaming-parser decision can connect a memory constraint and experiment evidence with consequences for error reporting. Later work can assess that reasoning against new evidence instead of reconstructing it.

Significant lasting choices in scope need an ADR when a concrete proposal is ready for decision or review, in or linked from arc42's decision section. This timing preserves developed proposals before acceptance without requiring an ADR for every exploratory idea; routine local choices normally need none. Status distinguishes proposed, accepted, rejected, and superseded decisions. Accepted records a decision made under existing authority and consultation rules, not completed implementation or a new ADR-specific approval. A record cannot replace required prior requester direction for a new consequential design direction or material departure. Material history, influential failed approaches, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links explain the basis and applicability of decisions. No exhaustive alternative search or out-of-scope backfill is required.

#### Recording technical debt

Debt describes a current compromise that increases future maintenance cost or risk, assessed against accepted requirements and trade-offs. A deferred feature, rejected option, or different preference alone does not establish debt. Intended behavior is not automatically a defect, although an accepted compromise can carry debt.

Permission to record evidenced, task-relevant debt makes concerns visible without requiring separate authorization for each entry or an in-scope fix. It applies to assessment-only work too. Chat notification—what, why, where, and uncertainty—makes the classification assessable; nonblocking disclosures join the next consolidated report under the [reporting rule](AGENTS.md#37-reporting). When in-scope work changes or resolves debt, its records in [arc42's risks and debt section](https://docs.arc42.org/section-11/) must be updated. Recording grants no permission to fix the issue or override an accepted decision; contract-file protection still applies.

#### Diátaxis: choosing content for the reader's need

[Diátaxis](https://diataxis.fr/) separates four needs: tutorials teach through guided practice, how-to guides help complete a task, reference supplies precise facts and interfaces, and explanation develops understanding. The [introductory guide](https://diataxis.fr/start-here/) explains these forms. A guide for correcting rejected rows can focus on the task and link to maintained format rules and background rationale.

New guides require an explicitly requested or agreed need; simple or low-level software may need none. Affected existing guides stay current. [Applying Diátaxis incrementally](https://diataxis.fr/how-to-use-diataxis/) avoids empty categories and a four-document requirement. Comments, docstrings, and generated API documentation should instead follow suitable existing language and tool conventions, with requester choices recommended when a new convention materially affects public documentation or maintenance.

### Why the bridges differ

Both bridges apply the same local contract through their tool's instruction mechanisms. [CLAUDE.md](CLAUDE.md) uses `@AGENTS.md`, Claude Code's [native import syntax](https://code.claude.com/docs/en/memory#import-additional-files), to include the referenced content. The single line can therefore perform its loading role.

[Copilot support](https://docs.github.com/en/copilot/reference/custom-instructions-support) varies by interface. A Markdown link identifies a file but is not a universal import mechanism. The supplied bridge explicitly directs reading and following the local contract within the actual hierarchy and permissions. Neither supplied bridge defines independent behavior for a failure to load the contract. The contract cannot govern an agent that never received it, so the package supplies no common stop/report/resume protocol for that case. Actual tool and requester instructions govern the situation. The [practical compatibility guidance](README-powerusers.md#tool-compatibility) explains this limitation and adoption diagnostics; it adds no fallback operating policy.

The bridge-only role and special edit-request protection apply to the three supplied root-relative instruction paths. Directory-level instructions may add subtree rules only when compatible with the root contract. The actual tool hierarchy determines discovery, scope, and precedence; that precedence never makes conflicting policy acceptable, and encountered conflicts are reported. Compatibility is a content rule, not an invented precedence mechanism. Adoption therefore includes human validation of which existing practices, conventions, and workflows persist, following the [basic installation precautions](README.md#get-started). Project facts and operating rules have different owners.

Discovery, inclusion, precedence, and application are distinct. [VS Code's conflict guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#_resolve-conflicting-instructions), its [instruction settings](https://code.visualstudio.com/docs/agents/reference/ai-settings#_custom-instructions-settings), and [GitHub.com's precedence guidance](https://docs.github.com/en/copilot/concepts/prompting/response-customization#precedence-of-custom-instructions) describe different aspects. File order or a link alone cannot establish all four. The [adoption checks](README-powerusers.md#check-adoption) and [recorded evidence dates](README-powerusers.md#evidence-dates) qualify the integration guidance; exact settings and support depend on the provider's documentation and the actual environment.

The Copilot title and header identify the associated release and upstream origin. Its release date and source URL match `AGENTS.md`. Metadata adds no policy authority, and the adopted local contract remains canonical. Permitting provenance does not require a header on the one-line Claude import. Minimality preserves each bridge's loading and application role.

## Evolving the contract

These sections constrain repairs, improvements, or redesign of `AGENTS.md`: how methods are chosen or replaced, how the contract stays portable, and which current wording trade-offs need review when editing. They guide the contract's evolution and add no operating duties to ordinary project tasks.

### Choosing or replacing methods

The method set was selected for recognized practices, freely accessible material sufficient to interpret their assigned roles, and distinct responsibilities. PDSA and Simple Design were judged sufficient for the agreed design alongside the focused engineering references, documentation conventions, and explicit collaboration rules. Additional umbrella frameworks were not needed to supply those responsibilities.

These selection criteria remain constraints on future additions or replacements unless explicitly revised. A proposed method change should explain the need it addresses, the accessibility of its required interpretive material, and any overlap or expansion of obligations. Changing a selection criterion is itself a design decision to identify explicitly; these constraints on the contract's evolution add no operating duties to ordinary project tasks.

### Keeping the contract portable

The entire `AGENTS.md` has a **strongly preferred target of about 24,000 UTF-8 bytes after normalizing line endings to LF**. Replace each CRLF pair and any remaining CR with LF before counting the whole file's UTF-8 bytes; do not otherwise trim or reformat its contents. LF and CRLF copies of the same content therefore have the same count. Normalized UTF-8 bytes remain the project's canonical measurement.

This target is informed by [Codex's default 32 KiB combined instruction limit](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance) and Anthropic's [guidance to keep `CLAUDE.md` concise and human-readable](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md). The approximate 24,000-byte figure is a project choice: it leaves room below Codex's default for directory instructions and other loaded instruction or configuration context, and reflects Claude Code's guidance on limiting standing context. Importing the contract through `CLAUDE.md` still [loads its contents into context](https://code.claude.com/docs/en/memory#import-additional-files).

Exceeding the target is exceptional but acceptable when further reduction would materially compromise normative fidelity or human comprehensibility. Before such excess is accepted, the contract receives a deliberate compression review. That review removes genuine redundancy and low-value explanatory detail before it compresses core control semantics, such as authorization, requester limits, cumulative reassessment, consultation, inquiry, and continuation. Even over target, the contract keeps meaningful headroom below applicable provider and project combined instruction-loading limits, such as Codex's default above, so directory instructions and other context can coexist. The project defines no separate provider-independent ceiling; those applicable combined limits bound the acceptable excess.

Check the normalized byte count after edits. Automated counts can help; automated enforcement is not required. Normalization defines this project's measurement; provider compatibility still depends on the actual delivered files, other loaded instructions, and tool configuration. Preserve useful spacing and headings. Meeting the target does not establish clarity, compatibility, equivalent behavior, agent adherence, or token savings. Vendor changes can prompt a review but do not automatically change the project policy.

The size target concerns the standing contract itself, not the reasoning or work allowed for a task. Operational meaning remains self-contained in `AGENTS.md`; necessary operating semantics must not move into a README to satisfy the target, because that would undermine portability even if the resulting file were smaller. Compactness is therefore subordinate to normative fidelity and usable comprehension, while standing instruction context remains a constrained resource.

### Current wording trade-offs

Compact instructions reduce standing text while increasing the risk that readers must infer relationships. Ambiguity can cause clarification, reference consultation, or rework; a smaller contract does not establish lower total token use. Review these current treatments when editing:

| Treatment | Interpretation risk and review focus |
| --- | --- |
| Implicit agent subjects, short labels, and slash groups | Keep the actor, every duty, and the relationship between grouped actions clear. |
| Broad knowledge-ownership and permitted-copy categories | Ensure readers can recognize facts, schemas, requirements, rationale, invariants, procedures, conventions, tests, and examples under the appropriate rule. |
| Concise definitions, architecture topics, record fields, and reports | Preserve distinguishing meaning and conditions; matching a name or keyword alone is insufficient. |
| Layered organization with section cross-references | Each passage should make sense where it appears. A reference can point forward to details when the surrounding text explains the relevant concept or constraint; `permitted work (§2.1)` is one example. Where a bare reference would force readers to look ahead just to understand the current passage, supply enough local explanation, accepting useful brief repetition. Keep consequential conditions explicit; guards and triggered rules apply across phases, and placement must not restrict a rule to one phase or imply an extra phase. |
| Initial task outline and first increment | Preserve advance visibility of the overall direction and next objective and bounds after proportionate preliminary context gathering. Do not turn the statement into mandatory effort estimation, detailed planning of later work, or an approval exchange. |
| Estimates, limits, and consequential direction | Keep optional forecasts distinct from binding requester constraints. Material ambiguity needs clarification; new consequential design direction and material departures need prior consultation unless the specific choice is already authorized. Routine local corrections remain autonomous. |
| Purpose-based inquiry and advance chat framing | Unknown data and prescribed procedures do not decide classification alone. Preserve the distinction between ordinary execution/validation and investigating how to proceed. Concise advance chat framing, conduct within its bounds, and consolidated outcome reporting serve different purposes. A visible commitment does not prove compliance or expose private reasoning. |
| Reference links without per-rule numeric locators | The [exact assignments](#principles-and-reference-boundaries) preserve attribution; narrow consultation limits prevent the links from becoming open-ended research. |

These are interpretation risks, not additional operating rules or measured agent outcomes. Do not approach the size target by removing essential conditions or transferring them into a README.

Acceptance of the current wording compromises covers only the identified trade-offs. It does not authorize further loss of precision. Any new trade-off, including reduced explicitness without an intended rule change, is a design decision to identify for requester review. Its rationale needs to record what becomes less explicit, where the operative meaning remains, and the likely interpretation or effort consequences. Previous acceptance and matching counts do not establish that a further reduction is lossless or behaviorally equivalent.

## Design reference

Use this material when reviewing a proposed change or an explanation of the contract: the design scenarios check combinations of rules against their intended distinctions, and the reference assignments preserve attribution and consultation limits.

### Assessing design changes

The design can be assessed at two levels: whether the contract works as a self-contained set of instructions, and whether a proposed change preserves or deliberately alters the meaning of its clauses. A standalone reading tests the first; comparison of strength, trigger, scope, exception, and meaning tests the second. The detailed patterns, fields, and obligations remain in `AGENTS.md`.

| Scenario | Design distinction to assess |
| --- | --- |
| Broad objective, including a new project | The agent limits its next commitment and keeps later work at outline level until detail is needed for the next decision. Necessary depth, affected dependencies, and validation remain within scope; the breadth of the goal does not justify an unconstrained first increment. |
| Starting a task | After proportionate preliminary context gathering, assess whether the agent briefly communicates the task outline and first increment's objective and bounds before substantial work. No cost estimate or approval is implied. Inquiry framing still applies when needed. |
| Requester expectation or binding limit | “I expect a small fix” is not automatically a budget; “consult before a second increment” is a checkpoint. Material ambiguity about the intended force needs clarification. Only requester direction can revise requester-imposed limits or checkpoints; subdivision and retries do not reset them. |
| Ordinary authorized change | The agent selects a small increment and completes its checks before completing the increment, even without a chat report. Completion grants no additional permission or automatic documentation artifact; another increment can proceed under existing authorization unless a checkpoint requires a pause. |
| Completed exploration without a record trigger | Without durable material findings or significant lasting choices, no record is required merely to log the discussion. Transient task facts, such as a temporary CI outage or a failed experiment relevant only to the current attempt, follow the reporting rules only. |
| Material findings or significant proposals during review | A [finding](AGENTS.md#32-durable-findings-and-permanent-records) needs a permanent record only when it is both material and durable, even if it comes from a discarded approach; a missing owner leads to the minimum record rather than backfill, and a prohibited write is reported as unfinished work. A concrete significant proposal ready for decision or review requires an [ADR](AGENTS.md#33-significant-decisions-adrs) retaining the evidence that materially shaped it rather than routine PDSA history; brainstorming or a finding alone does not. Status reflects existing decision authority. Recording supplies no implementation authority or new approval checkpoint. |
| Verified factual documentation error during assessment | The agent may make an existing description of current project facts within the assessed scope match the canonical owner of that kind of knowledge, subject to scope, requester restrictions, §3.8, and tool permissions. Requirements, decision records, and protected instruction files are excluded. A verified mismatch with authoritative package configuration can justify correcting a README command; it does not authorize changing implementation, intended requirements, accepted decisions, or protected instruction files. |
| Task-relevant debt found during assessment | Evidenced debt may be recorded after considering accepted requirements and trade-offs. Any entry triggers classification-uncertainty and chat-disclosure duties. The general material-findings requirement still applies; neither classification nor recording authorizes a fix. |
| Requester or tool prohibits writes | Assessment permissions remain subject to requester restrictions (§2.1) and §3.8. An explicit ban on creating, modifying, or deleting files covers records and factual documentation corrections; tool restrictions also remain binding. Findings and proposed text can be supplied in chat within those limits, but chat does not satisfy a permanent-record obligation; the unmade record is reported as unfinished work. |
| Continued execution and reporting | Several increments can complete without routine report drafting or output. At task completion, handoff, or when seeking input, the agent consolidates unreported work. Required findings and records are maintained throughout. |
| Requested or required disclosures | Disclosures affecting authorization or a decision requiring requester input precede affected work. Other disclosures, including inquiry outcomes, join the next consolidated report unless earlier timing is explicit. The initial task outline and inquiry framing require brief advance chat statements; one message can satisfy both when applicable. Reporting alone creates no approval checkpoint. |
| Selecting and revisiting work | Plan connects the requested outcome, permission, relevant context, and evidence to a useful next increment from the first request. Assess whether that connection is understandable, including when missing evidence or consequential constraints change the next step. Study and Act inform later planning; later work stays at outline level until detail is needed and revisions stay within authorization. |
| Investigation contradicts its prediction | An evidenced answer can complete the investigation while disproving the prediction; unmet implementation behavior remains incomplete. |
| Reading existing project documentation | Reading remains context gathering without investigation framing or routine announcements, even for a material blocking question. Inspecting relevant code, callers, tests, configuration, and directly related dependencies to establish context is also context gathering. Scope, requester limits, proportionate work, and cumulative reassessment apply to all of it. |
| Prescribed empirical operation or acceptance check | Unknown output alone does not establish inquiry. Contrast executing a settled measurement/calculation or checking acceptance with using the same procedure to investigate an unsettled approach. Classify purpose before assessing inquiry duties; a procedure neither automatically triggers nor exempts inquiry. |
| Material uncertainty about how to proceed blocks the next decision after context gathering | State the §2.4 framing concisely in chat before starting or acting on revisions, with a proportionate limit that governs conduct. Unchanged framing needs no repetition. Private planning or retrospective framing cannot substitute for the advance statement. |
| Investigation obtains sufficient evidence or reaches its stated effort limit | End and assess the inquiry, without claiming completion where acceptance evidence is missing. Report outcomes at §3.7's occasions, seeking direction before affected work when required. Another authorized attempt needs new advance framing justified by the preceding result and cumulative reassessment. Requester caps/checkpoints still apply; neither a new label nor an exhausted inquiry supplies authority or resets a requester limit. |
| Acceptance-critical verification is unavailable | Sufficient alternative evidence can establish the same condition unless a specific check is required. Otherwise the condition remains unverified and validation incomplete unless validly revised. Disclosure alone does not satisfy it. |
| Equivalent evidence exists for an available acceptance check | The relevant available check must run. Equivalence alone does not permit substitution; the unavailable-check exception does not apply. |
| Known risk without an internal-quality compromise | Preserve the known risk under topic 11 without inventing a technical-debt classification. |
| Documentation-only work | Applicable methods and validation apply without requiring code or unit tests for their own sake. |
| Additional work or a revised forecast | Reassess cumulative progress, remaining work, direction, and limits before expanding planned work or starting another increment/attempt. Each next increment needs evidence supporting its contribution. An optional estimate and its revision are nonbinding; authorized, justified work within direction and limits can continue without a forecast-based checkpoint. |
| New consequential design direction or material departure | Obtain requester direction before adoption or implementation unless the specific choice is already authorized, including in a new project without established architecture. A Proposed ADR can prepare the decision; recording it or reporting later cannot supply prior authorization. |
| Handoff and resumption | Transfer the task objective/direction, limits/checkpoints and consumed allowances, next or unfinished increment objective/bounds/acceptance conditions, and relevant inquiry framing/results/remaining allowance. Use that state on resumption; recover missing authorization or limit state or obtain direction before dependent work. Missing optional estimates alone do not block continuation. |
| Any tool fails to load the contract | The package defines no separate bootstrap stop/report/resume policy. Neither a bridge nor a README supplies one, and an unloaded contract cannot govern the failure. Use actual tool and requester instructions and distinguish loading diagnostics from demonstrated application. |
| Root and directory instruction files | Only the three root-relative contract/bridge paths receive special edit protection. Subtree rules may be added only when compatible with the root contract; the tool decides discovery, scope, and precedence, which never makes conflicting policy acceptable; encountered conflicts are reported. |

The relevant dependencies span [engineering](AGENTS.md#12-do--perform-the-authorized-work), [validation](AGENTS.md#13-study--assess-completion-and-learning), the [progression guards](AGENTS.md#2-progression-guards), the [triggered rules](AGENTS.md#3-triggered-rules) for knowledge retention and documentation, and [how the layers compose](AGENTS.md#4-how-the-layers-compose). Method conditions, appropriate-test recommendations, required validation, documentation scope, and requester authority all contribute to the resulting behavior.

Changes to protected instruction files follow [their authorization rule](AGENTS.md#38-instructions-protected-files-and-external-actions), including file-specific recommendations and necessary companion edits to the other two listed files; other affected documentation follows the ordinary synchronization rules. Substantive policy changes need explicit identification. An explanation or review checklist cannot substitute for the actual clauses, and a shorter contract does not by itself establish equivalent agent behavior or token savings.

### Principles and reference boundaries

The accounts linked in this guide provide freely accessible interpretive material for the named practices. Their role is to clarify those practices within the contract's conditions. The design draws on specific accounts rather than requiring whole frameworks or access to a paid book. The [Pragmatic Programmer book](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) is paid; its assigned public tips and extracts are freely available.

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

The coupling assignment excludes tip 46. The DRY, inheritance, and shared-state extracts linked above supply fuller accounts for their respective concerns. Attribution identifies supporting material, without claiming that one reference states the contract's combined preservation duties verbatim.

[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) supply requirement-keyword semantics. They concern the strength of agent obligations, while EARS expresses system requirements and ADRs record choices and reasons. Supporting explanations include [IHI's testing-changes guidance](https://www.ihi.org/library/model-for-improvement/testing-changes) and [arc42's debt FAQ](https://faq.arc42.org/questions/C-11-1/); they add no operating obligations.

The contract should normally suffice for ordinary cases. The links remain so that, under the [method-reference rules](AGENTS.md#39-method-references), an agent can occasionally read enough of a linked reference to resolve a material edge-case ambiguity in the contract's use of that method that the contract itself cannot resolve. That narrow consultation needs no §2.4 inquiry framing; the ambiguity, the reference consulted, and the resulting interpretation are reported, and no other practices from that reference become obligations. Clear rules need no principle research, and broader research requires direction. Technical research for a task follows that task's scope and investigation limits. This distinction prevents an explanatory link from becoming an open-ended research assignment or importing a reference's stronger rhetoric as policy.
