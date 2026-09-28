# The design of AGENTS.md

[AGENTS.md](AGENTS.md) is a reusable, opinionated contract whose primary aim is to prevent unconstrained token consumption through small, complete steps toward a task objective. Necessary reasoning, work, and validation remain requirements within each step. This guide explains the design choices, their trade-offs, and the constraints that inform repairs, improvements, or redesign.

For adoption, use [README.md](README.md). For practical guidance, use [Getting more from AGENTS.md](README-powerusers.md). Here, start with the design goals and example, or go directly to the area a proposed change affects:

- [Workflow choices](#workflow-design-choices): scope, learning, investigation, and requester control.
- [Engineering choices](#engineering-choices) and [documentation choices](#documentation-choices): methods, reasons, and conditions.
- [Continuation](#continuation-design), [bridges](#why-the-bridges-differ), and [portability](#keeping-the-contract-portable): retaining context and applying the contract across tools.
- [Method selection](#choosing-or-replacing-methods), [design review](#assessing-design-changes), and [source assignments](#principles-and-reference-boundaries): constraints and evidence for evolution.

## Design goals and boundaries

The motivating risk is especially visible in a new or poorly documented project. Without established requirements, interfaces, decisions, and conventions, planning and autonomous design have fewer constraints. Even a bounded objective can permit a large amount of work. The contract therefore limits each commitment and requires reassessment before unexpectedly greater effort, including sudden heavy use within one increment.

Its controls work together: small increments limit the immediate commitment; progressive detail defers distant decisions; bounded investigations limit inquiry; PDSA connects findings to subsequent choices. Engineering practices support quality within each step, while documentation and continuation context retain knowledge for later work. Adequate analysis, completeness, and validation constrain every effort-saving choice.

Reports consolidate unreported work at task completion, handoff, or when seeking requester input. Routine progress reports are suppressed unless requested or otherwise required, reducing narration while authorized work continues. These mechanisms are best effort: total consumption may remain substantial. The design requires no pause after every increment and provides no token quota or guarantee of savings. The [practical explanation](README-powerusers.md#understanding-token-use) distinguishes reported results from consumption measurement.

The contract is self-contained. Guides explain it and bridges help tools apply it; neither supplies hidden operating duties. Project facts, build commands, requirements, and architecture come from the adopting project's code and documentation. This separation supports reuse without embedding an application's design in generic instructions.

Requester instructions take priority within the tool's actual hierarchy and permissions. Directory instructions follow that tool's scope and precedence rules. The contract cannot supply capabilities, enforce permissions, or override native approvals. Its protection of instruction files and its authorization rules for external actions keep those limits explicit. It also does not supply a complete product-development process, branching strategy, workflow engine, or framework tutorial. Established methods cannot invent missing requirements or requester authority.

## How the design works in a task

Consider the CSV-import scenario from the [practical walkthrough](README-powerusers.md#from-a-request-to-a-result): report invalid rows and continue with valid rows. The **task objective** is that overall outcome. An **increment** is the next deliberately small, bounded step toward it, normally useful, understandable, reviewable, and verifiable on its own.

[PDSA—Plan–Do–Study–Act](https://deming.org/explore/pdsa/) begins with that request. Plan selects and bounds the work; Do performs it; Study assesses completion and the approach; Act uses the findings to decide what follows.

1. **Plan:** establish the objective and permitted work, then inspect the relevant project context. Suppose the requirements settle the input format, invalid-row rules, and line-number convention; existing tests support the reader's suitability; and inspection shows that field-count validation is missing. The row-processing code exposes the fields, header, and line number, suggesting a local implementation.

   This evidence supports choosing field-count validation: it advances an agreed requirement, addresses one concern, and can produce a useful, testable result without implementing every remaining invalid-row rule. The scope includes the affected code, tests, and documentation. Its limited dependencies and expected ease of reversal support a small commitment; neither substitutes for validation.

   Define **acceptance conditions**—reject mismatched rows, report their line numbers, and continue with valid rows, including one after a rejection—and a **prediction** that the existing row boundary will support the approach. Selection, scope, conditions, and approach can be refined together as context becomes clear. Later work remains at outline level.
2. **Do:** implement the validation using current project conventions and Simple Design. Add relevant tests and update affected documentation at its authoritative location. Record an ADR if a significant lasting choice arises.
3. **Study:** check acceptance before completing the increment, including a valid row after a rejection. Separately assess whether the predicted local approach sufficed. Failed, unavailable, or omitted checks remain subject to disclosure under the reporting rules.
4. **Act:** use the evidence to retain, revise, or discard the approach within authorization. Preserve material findings and otherwise missing continuation context, then finish, seek required direction, or plan the next authorized increment. Continuing to another increment does not require drafting or emitting a routine report; reporting follows [§4.4](AGENTS.md#44-report-the-result-and-choose-the-next-step).

The initial choice therefore depends on what Plan establishes. Unsettled consequential requirements need requester input; uncertainty about the reader may call for a bounded investigation before implementation. The agent is responsible for choosing and defining the next increment, within the contract's consultation and authorization rules.

The example connects the design's parts. Requirements provide intended behavior; inspection and existing checks establish the starting point; Study supplies new evidence; Act uses it to inform subsequent Plan phases. Records preserve material findings and lasting choices. The supported local validation approach may help plan another rule, while evidence of wider parser limitations changes the basis for that next decision.

The field-count result can therefore inform another authorized validation increment before any routine chat report is produced. At task completion, a handoff, or when seeking requester input, the agent consolidates unreported work. Required disclosures still apply: a discovery that requires an unexpectedly larger shared-parser redesign triggers explanation and reassessment immediately, in whichever phase it occurs. The agent then waits for requester direction before the added work. A requested operator guide could be another increment, shaped by its reader's need. Neither a completed step nor a named method automatically creates an ADR, guide, work record, or fresh approval requirement.

The [practical walkthrough](README-powerusers.md#from-a-request-to-a-result) shows the user-facing interaction. The following sections explain the reasons and boundaries behind it.

## Workflow design choices

### Small commitments with sufficient depth

The requester supplies goals, permission, and relevant constraints. The agent supplies decomposition, acceptance conditions, validation, effort assessment, and recognition of required consultation. These standing responsibilities let an ordinary outcome-oriented request start useful work. A requester may still select a step or add review points.

Within Plan, increment selection connects the requested outcome and permission with current behavior, relevant dependencies, and available evidence. The agent looks for the smallest useful result that can be completed within scope, including the affected artifacts and checks. When blocking uncertainty prevents a sound implementation choice, obtaining bounded evidence can itself be the useful result.

The [four effort factors](AGENTS.md#51-scope-effort-and-requester-interaction)—scope, uncertainty, consequence, and reversibility—guide that judgment. Scope includes affected behavior, artifacts, dependencies, and system boundaries. A few changed lines can affect many callers or an irreversible migration; a narrow, understood, low-impact, reversible change can use brief inspection, action, and validation. Reporting follows its own triggers and remains proportionate.

These criteria constrain selection without prescribing a numeric score, an exhaustive comparison of possible increments, or a uniquely correct sequence. Requiring a complete ranking or detailed backlog before starting would expand the initial planning commitment. The design instead calls for enough reasoning to support the next useful step and uses its evidence to refine later work. This contributes to the token-control goal while preserving the analysis and validation needed for a complete result.

Depth follows the next decision at the current abstraction level. Architecture analysis may need careful examination of boundaries, alternatives, and risks without specifying every future API or function. Later work stays at outline level until the next decision needs detail; depth follows uncertainty, consequence, risk, reversibility, and proximity to execution. Explicit authorization can cover broader analysis at the relevant abstraction level.

Completeness is assessed within the increment's scope. Evidence, enabling infrastructure, or migration groundwork can be useful results as well as functionality. Before a step that cannot stand alone, the agent explains why, what remains usable or testable, and how to undo it. Recovery reduces the cost of a mistaken approach; it grants no permission for destructive effects. A required stop may leave work incomplete, while review-boundary coherence and context retention still apply. A small scope cannot excuse shallow reasoning, omitted dependencies, or incomplete work presented as finished.

### Learning throughout the work

The [Deming Institute's PDSA account](https://deming.org/explore/pdsa/) connects an approach and expected result with observation and the next decision. Small increments bound commitments; PDSA's contribution is learning which approach remains suitable and what to do next. Passing tests alone does not establish that learning role: the implications still inform Act and subsequent planning.

The contract's [workflow overview](AGENTS.md#workflow-overview) starts with the request. Plan includes context gathering, the overall objective and permitted work, outlining an approach, and selecting the next increment. Study assesses completion and observations; Act uses those findings to retain, revise, or discard the approach within authorization. Results can reshape later detail without changing the agreed outcome or granting more authority.

Terms and a workflow overview precede the contract's four phases. Methods appear near their principal contribution, but their triggers and the shared rules apply throughout. Tests can be planned before implementation; decisions and documentation are maintained as facts emerge. Phases can overlap or repeat, and routine work needs no worksheet, formal experiment, or separate phase reports.

PDSA's Plan phase organizes reasoning. A tool's Plan mode has its own proposal and approval procedures. Neither expands authorization. These distinctions let the workflow apply proportionally to implementation, investigation, and documentation without inventing separate mandatory deliverables.

### Completion, predictions, and bounded investigation

**Acceptance conditions** define the observable result needed to complete the increment. **Validation** checks them. A **prediction** states the expected result of the approach; comparison with observations informs whether to retain or revise that approach. Revising a prediction changes neither requirements nor acceptance conditions.

This separation allows an investigation to succeed by disproving an assumption. Evidence that a reader splits a quoted comma can answer a question about its behavior, while an implementation required to preserve that field remains incomplete. A successful sample also supports only the conclusion justified by that sample. The [practical investigation example](README-powerusers.md#when-an-investigation-is-needed) develops both outcomes.

Routine code, test, and configuration inspection and all reading of existing project documentation are context gathering. The documentation exemption still applies when reading is needed to answer a material question blocking the next decision. Other inquiry into such uncertainty requires framing under [AGENTS.md §1.2](AGENTS.md#12-bound-the-work-and-choose-an-approach): state the question, scope, objective, effort limit, and needed evidence before starting. An **investigation effort limit** ends that inquiry even without the evidence. This makes the commitment visible before consuming it; the requester need not prescribe or approve every limit. Context gathering remains subject to scope and material-growth controls. Consequential unresolved intent or constraints still require involvement.

No default amount, unit, or selection formula is prescribed. Choosing a useful bound therefore requires judgment and provides no automatically enforced timeout or token quota. The one-attempt allowance in the practical example is illustrative.

Obtaining the evidence or reaching the limit ends the inquiry. If acceptance conditions remain unmet, the report identifies incomplete work, missing evidence, and uncertainty. Neither a negative finding nor an exhausted allowance supplies more authority. Existing scope and authority may nevertheless permit a new bounded attempt at an unresolved question, with new framing under §1.2 and the [§5.1 renewal conditions](AGENTS.md#51-scope-effort-and-requester-interaction). Requester limits and checkpoints remain binding; materially greater effort requires direction before it proceeds. The agent must explain any need for broader research or a wider design decision. The [Study rules](AGENTS.md#3-study--assess-completion-and-learning) preserve the distinction between learning and completion across all work types.

### Authorization and requester decisions

An increment limits work undertaken at once; a report can summarize several increments; a checkpoint reserves a decision for the requester. Ordinary increments can continue under existing authorization without routine reports. Their completion supplies no additional permission and creates no automatic pause.

The material-growth checkpoint addresses a separate problem: authorized work can turn out to require unexpectedly greater effort. The agent establishes increment and cumulative-task effort baselines from requester direction where supplied, otherwise from its own judgment without routine notification. Baselines can be qualitative; they are not token quotas. Assess both increment and cumulative growth against them. Only requester direction can revise the task baseline; new increments, attempts, and conversations do not reset it. Retaining that baseline and known cumulative effort prevents repeated small additions or a restart from evading the checkpoint. The agent must explain a material increase and await direction before taking it on, even when the outcome and broad authorization are unchanged. This gives the requester control that a scope boundary alone cannot provide. See the [practical growth cases](README-powerusers.md#when-the-work-grows-unexpectedly).

The [requirement keywords](AGENTS.md#terms-and-requirement-keywords) preserve distinct strengths:

- Material unresolved intent or permission must be escalated; missing consequential constraints must be agreed as needed.
- Asking before an unsettled consequential choice is a strong recommendation with justified exceptions.
- Easily reversible routine details may be chosen within agreed limits; material assumptions remain visible.

A SHOULD exception cannot bypass a MUST checkpoint or invent a consequential constraint. Reporting a consequential choice without prior direction exposes reasons, effects, uncertainty, and revision or reversal options; it cannot retroactively authorize the choice. Native permissions and approval controls remain the enforceable boundaries.

Analysis and review can establish lasting project knowledge before implementation. The [assessment permissions](AGENTS.md#11-establish-the-starting-context) let the [material-findings, decision/debt, and continuation rules](AGENTS.md#4-act--use-the-findings-and-determine-what-follows) operate in those tasks, with each rule's own trigger and strength. They also permit corrections of verified factual errors in ordinary documentation within the assessed scope. These permissions do not authorize implementation or changed requirements or accepted decisions. An appropriate record preserves the finding and evidence under its canonical owner; it cannot act as permission to implement the recommendation. Broader documentation repairs and external actions retain their own authorization requirements. [Requester instructions, protected-file rules, and tool restrictions](AGENTS.md#53-instructions-contract-files-and-external-actions) can prevent these writes. The [practical examples](README-powerusers.md#records-during-review-and-exploration) distinguish factual corrections from changed intent and show the effect of a no-edit instruction.

### Reporting and continued execution

Completing an increment and reporting to the requester serve different purposes. PDSA requires the work to be assessed and its findings used, even when no chat report follows. [AGENTS.md §4.4](AGENTS.md#44-report-the-result-and-choose-the-next-step) consolidates unreported work at task completion, handoff, or when seeking requester input. It prohibits drafting or outputting routine progress reports at other times unless requested or required.

Suppressing drafting as well as output avoids preparing reports merely to hold them back from chat. Disclosures affecting authorization or the next decision precede the affected work; other disclosures join the next consolidated report unless earlier timing is explicit. The early continuation notice and the report when a bounded inquiry stops retain their timing. Nonblocking debt recording, for example, does not require an immediate chat interruption. Material findings, decisions, affected documentation, and necessary continuation context retain their owners and maintenance triggers; record maintenance does not wait for the report. No separate reporting log or record is required for every increment. Tool instructions and requester-selected reporting remain applicable.

The trade-off is less routine visibility during autonomous work and a consolidated account at the next reporting occasion. Reporting alone reserves no time for review and creates no approval checkpoint. Scope limits, bounded investigations, and mandatory reassessment for material growth continue to control the work; fewer reports establish no measured token saving.

Reports remain proportionate and follow the contract's requirements for content, file delivery, and blocked-edit fallbacks. The [usage guide](README-powerusers.md#assess-the-result) explains what the requester receives.

## Engineering choices

### Simple Design: choosing what the current solution needs

Beck's [Simple Design, explained by Fowler](https://martinfowler.com/bliki/BeckDesignRules.html), supplies four criteria: meet requirements and pass tests, express intent, avoid duplicated knowledge, and retain only necessary elements. They assess the current solution; fewer classes or lines alone cannot establish simplicity.

Hard memory, latency, throughput, concurrency, cost, or scale requirements may justify complexity. An imagined future extension does not provide equivalent evidence. Supporting one agreed input format can be complete without a framework for unspecified formats, while still including its necessary error handling and checks. A documented optimization strategy supplies project context and is a strong default unless the task conflicts with or materially extends it. Material trade-offs remain visible.

### DRY: keeping knowledge consistent as work progresses

The [Pragmatic Programmer's DRY account](https://media.pragprog.com/titles/tpp20/dry.pdf) concerns knowledge that would otherwise need independent maintenance in several places. Canonical ownership reduces the risk of divergent facts, rules, or explanations across code and documents.

A setting can own a retry limit while a guide explains its purpose and links to it. Two unrelated limits may have the same value without representing shared knowledge. Necessary test, example, summary, generated, protocol, migration, and compatibility copies can remain with a clear source and update process. Resemblance alone supplies no reason to merge them.

### Component boundaries, refactoring, and validation

Clear responsibilities, limited coupling, visible side effects, and explicit resource ownership make the effects of a change easier to understand. The [public tips](https://pragprog.com/tips/) and [shared-state extract](https://media.pragprog.com/titles/tpp20/shared-state.pdf) support these concerns; their exact assignments appear [below](#principles-and-reference-boundaries). Separating concurrent coordination from sequential logic where practical supports clear ownership without prescribing a universal asynchronous architecture.

[Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) preserves observable behavior. An intended and authorized behavior change needs corresponding requirements, tests, and documentation. Documented design invariants protect promised properties; project patterns can change through scoped, justified, validated improvements. Neither distinction requires preserving a defect when changing it is intended and authorized.

The dead-code condition matters because registration, reflection, or external callers may make apparently unused code reachable. Clear unreachability or direct obsolescence from the authorized change is needed for removal *as dead code*. Explicitly authorized removal of live functionality is a different case.

### Validation and test evidence

Relevant available checks against acceptance conditions are mandatory before completing each increment, independently of whether a report is produced then. Appropriate tests for behavior changes, defect repairs, and clarified edge cases are a SHOULD default with justified exceptions. Validation covers affected behavior, risk, and hard operational limits for every work type; passing tests cannot replace a missing requirement or necessary check. Failed, unavailable, and omitted checks must be disclosed under §4.4; any need for requester involvement still follows §5.1.

An unavailable verification method and an unverified acceptance condition are distinct. Sufficient alternative evidence may substitute only when the original check is unavailable and is not specifically required. An available relevant acceptance check still runs even if an alternative could provide equally sufficient evidence. Without sufficient evidence, the condition remains unverified and validation incomplete unless that condition is validly revised under existing authority; disclosure alone cannot establish it. A pre-existing failure is assessed for relevance and disclosed, without automatically blocking unrelated work. The [practical validation examples](README-powerusers.md#assess-the-result) distinguish available checks, equivalent local checks, insufficient mocked evidence, and a specifically required CI result.

[Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html) makes a unit test's starting conditions, action, and expected result understandable. For a quoted field containing a comma, those parts are the sample, the parser call, and the intact-field assertion. The contract requires neither literal labels nor a testing framework, and prohibits weakening tests merely to pass.

### Focused techniques and how they work together

These techniques support Simple Design when their benefits justify their costs. Their selection grants no authority for unrelated restructuring or new dependencies.

**Gross's [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/)**

Make behavior understandable near its implementation while balancing separate responsibilities and canonical ownership. A clear invocation can expose intent without inlining everything or adopting htmx.

**The [Law of Demeter](https://www2.ccs.neu.edu/research/demeter/demeter-method/LawOfDemeter/general-formulation.html)**

Reduce knowledge of other components' internals through direct collaborators. Clarity and interface costs matter; there is no blanket ban on chained access or requirement for an aspect-oriented solution.

**Fowler's [Value Object](https://martinfowler.com/bliki/ValueObject.html)**

Express domain meaning and validation through values equal by contents, with practical immutability. Preserve required identity and state changes; neither wrapping every primitive nor adopting Domain-Driven Design is required.

**The [inheritance extract](https://media.pragprog.com/titles/tpp20/inheritance-tax.pdf)**

Prefer interfaces, protocols, and composition when they reduce coupling; use polymorphism for complex conditional dispatch when clearer. Keep abstractions justified and allow suitable inheritance.

**Fowler's [dependency injection](https://martinfowler.com/articles/injection.html), “Separating Configuration from Use”**

Separate assembly from use when this improves separation, clarity, or testing. Supplying a clock as a parameter can suffice. Configuration normally stays at assembly, initialization, or external-system boundaries; no container or new dependency is required.

## Documentation choices

Requirements describe intended behavior, accepted decisions retain choices and reasons, architecture describes boundaries and guarantees, and schemas and package metadata declare their own constraints. Code, tests, and execution provide evidence of implemented behavior. Their roles explain why executable behavior does not automatically overrule a requirement. Conflicts need visible evidence, inference, and an identified governing source; personal or external instructions cannot supply project facts.

Documentation informs Plan and changes as work establishes facts and choices. Producing a guide or updating affected documentation is Do work. Study checks its acceptance conditions; Act uses the findings and retains relevant learning. Architecture and ADRs appear under Act for that retention role, while their records are read and maintained whenever needed.

Updates follow affected canonical owners and direct references. Coverage expectations do not authorize a repository-wide audit, backfill, or reorganization. Documentation-only work uses the same increment, validation, review, and conditional continuation rules as other work. Current-system descriptions follow reality, with proposals and unfinished work clearly identified.

### arc42: shared architectural context as the project grows

[arc42](https://arc42.org/overview/) supplies twelve architectural topics spanning goals and constraints, structure and operation, crosscutting concepts, decisions, quality, risks, and terminology. Shared content expectations aim to reduce reinvention and relearning across repositories. They give an empty project questions to answer as evidence develops, without requiring the entire design to be settled first.

The contract covers applicable topics with known facts and visible material unknowns. Empty headings and invented details do not establish coverage. [Incremental documentation](https://faq.arc42.org/questions/B-14/) and [appropriate depth](https://faq.arc42.org/questions/B-4/) support keeping content useful as the system develops. [Quality scenarios](https://docs.arc42.org/section-10/) make goals assessable: “imports should be fast” still needs an agreed workload and measure.

One architecture document is the initial SHOULD default, using the existing documentation folder or repository-root `docs/`. This keeps early information together. An adequate existing arrangement can remain, and coherent parts can separate as reading and maintenance warrant it. Layout is flexible; known coverage gaps still require proposals and warrant improvements within authorized scope, subject to requester limits or deferral. Summaries link to canonical requirements and ADRs, while implementation detail stays near code and tests.

Topic 11 covers known risks as well as technical debt under the contract's definition. The risk category is not restricted to internal-quality compromises: external dependencies and operational circumstances can create known risks even when implementation quality is adequate. The distinction preserves the scope of [arc42's risks and debt topic](https://docs.arc42.org/section-11/) without classifying every risk as debt or importing an additional risk-management procedure.

### EARS: making required behavior explicit

[EARS (Easy Approach to Requirements Syntax)](https://alistairmavin.com/ears/) gives natural-language requirements consistent condition-and-response patterns. For example:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

The pattern exposes behavior to implement and check. It cannot decide whether to reject one row or the whole file, or define a row's line number for a particular format. Those remain project decisions. EARS applies to new or revised in-scope system requirements; unchanged requirements need no automatic conversion. The [contract](AGENTS.md#13-express-new-or-revised-system-requirements-with-ears) owns the five patterns and combined state-before-event form. Rationale belongs with significant choices; EARS adds no mandatory rationale field to each requirement.

### ADRs: preserving the reasons for lasting choices

[Architecture Decision Records](https://docs.arc42.org/section-9/) retain reasons that code alone may not reveal. A streaming-parser decision can connect a memory constraint and experiment evidence with consequences for error reporting. Later work can assess that reasoning against new evidence instead of reconstructing it.

Significant lasting choices in scope need an ADR when a concrete proposal is ready for decision or review, in or linked from arc42's decision section. This timing captures developed proposals before acceptance without requiring an ADR for every exploratory idea; routine local choices normally need none. Status distinguishes proposed, accepted, rejected, and superseded decisions. Accepted records a decision made under existing authority and consultation rules, not completed implementation or a new ADR-specific approval. Material history, influential failed approaches, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links explain the basis and applicability of those project decisions. This does not require exploring every possible alternative or backfilling decisions outside authorized scope.

### Recording technical debt

Debt describes a current compromise that increases future maintenance cost or risk, assessed against accepted requirements and trade-offs. A deferred feature, rejected option, or different preference alone does not establish debt. Intended behavior is not automatically a defect, although an accepted compromise can carry debt.

Permission to record evidenced, task-relevant debt makes concerns visible without requiring separate authorization for each entry or an in-scope fix. It applies to assessment-only work too. Chat notification—what, why, where, and uncertainty—makes the classification assessable; nonblocking disclosures join the next consolidated report under §4.4. When in-scope work changes or resolves debt, its records in [arc42's risks and debt section](https://docs.arc42.org/section-11/) must be updated. Recording grants no permission to fix the issue or override an accepted decision; contract-file protection still applies.

### Diátaxis: choosing content for the reader's need

[Diátaxis](https://diataxis.fr/) separates four needs: tutorials teach through guided practice, how-to guides help complete a task, reference supplies precise facts and interfaces, and explanation develops understanding. The [introductory guide](https://diataxis.fr/start-here/) explains these forms. A guide for correcting rejected rows can focus on the task and link to maintained format rules and background rationale.

New guides require an explicitly requested or agreed need; simple or low-level software may need none. Affected existing guides stay current. [Applying Diátaxis incrementally](https://diataxis.fr/how-to-use-diataxis/) avoids empty categories and a four-document requirement. Comments, docstrings, and generated API documentation should instead follow suitable existing language and tool conventions, with requester choices recommended when a new convention materially affects public documentation or maintenance.

## Continuation design

The continuation mechanism supports resuming unfinished work in a new conversation without the original chat. Its design criterion is that each task's record entry, together with available project artifacts and applicable instructions, preserves the context needed for resumption. Material missing context remains visible. One root file, `.agent-continuation-context.md`, holds separate, identified task entries, making the record discoverable without an index link or broad search. Its descriptive name and leading dot reduce accidental collisions. The path and task-entry arrangement are local conventions applying retained learning and canonical ownership.

Conditional creation avoids an extra task entry or file when code, tests, and permanent documentation already preserve enough context. When needed, an entry is maintained during the work: material changes, review boundaries, and planned stops or handoffs trigger updates. This ongoing maintenance serves the purpose of starting a new conversation. Waiting until a requester announces a handoff would leave unexpected loss of the old conversation uncovered. An abrupt interruption can still leave the record stale, which is why resumption in a new conversation compares available task context, including the record if present, with current files, checks, and instructions. An absent record is not itself a context gap when permanent artifacts suffice.

Objectives, acceptance conditions, and relevant approach and prediction preserve what unfinished work is intended to establish. Effort baselines and known cumulative effort or uncertainty preserve the comparison needed for growth reassessment in every kind of work, including implementation. Interrupted investigations also retain their framing, explicit limit, known effort consumed, and uncertainty. Retaining pending decisions and checkpoints keeps those boundaries explicit across conversation changes. The record and resumption supply no additional authority or fresh task baseline; the startup notice exposes saved context without requiring a reply. Continuing follows the request, applicable instructions, and remaining checkpoints.

Current reality belongs in code, checks, and current-system documents; lasting rationale belongs with decisions; each work-record entry holds otherwise missing task intent and direction. Canonical links avoid competing copies of permanent facts, while status distinguishes proposed steps from implemented behavior. Identifying partial or uncommitted work and missing artifacts helps a new agent establish what is actually available, especially in another environment. A description of changes does not transfer their contents. Starting another task, updating its entry, or retiring it must preserve context still needed by other tasks. Only when no task entry is needed can the whole record be retired. The [usage guide](README-powerusers.md#continue-unfinished-work) explains the practical handoff through examples, including stale records, multiple tasks, collisions, and retirement.

The contract defines startup and resumption for this mechanism as a new conversation. A pause or compaction within an ongoing conversation does not trigger record reloading or reconciliation. The ongoing conversation uses its available context while ordinary inspection, contradiction reporting, and record-maintenance rules remain applicable. The [design scenarios](#assessing-design-changes) below assess restart behavior without assuming tool-specific memory or compaction features.

## Why the bridges differ

Both bridges apply the same local contract through their tool's instruction mechanisms. [CLAUDE.md](CLAUDE.md) uses `@AGENTS.md`, Claude Code's [native import syntax](https://code.claude.com/docs/en/memory#import-additional-files), to include the referenced content. The single line can therefore perform its loading role.

[Copilot support](https://docs.github.com/en/copilot/reference/custom-instructions-support) varies by interface. A Markdown link identifies a file but is not a universal import mechanism. The supplied bridge explicitly directs reading and following the local contract within the actual hierarchy and permissions. Neither supplied bridge defines independent behavior for a failure to load the contract. The contract cannot govern an agent that never received it, so the package supplies no common stop/report/resume protocol for that case. Actual tool and requester instructions govern the situation. The [practical compatibility guidance](README-powerusers.md#tool-compatibility) explains this limitation and adoption diagnostics; it adds no fallback operating policy.

The bridge-only role and special edit-request protection apply to the three supplied root-relative instruction paths. Directory-level instructions may contain compatible subtree additions under the actual tool hierarchy; compatibility is an authoring rule, not an invented precedence rule. Adoption therefore includes human validation of which existing practices, conventions, and workflows persist, following the [basic installation precautions](README.md#get-started). Project facts and operating rules have different owners.

Discovery, inclusion, precedence, and application are distinct. [VS Code's conflict guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#_resolve-conflicting-instructions), its [instruction settings](https://code.visualstudio.com/docs/agents/reference/ai-settings#_custom-instructions-settings), and [GitHub.com's precedence guidance](https://docs.github.com/en/copilot/concepts/prompting/response-customization#precedence-of-custom-instructions) describe different aspects. File order or a link alone cannot establish all four. The [adoption checks](README-powerusers.md#check-adoption) and [recorded evidence dates](README-powerusers.md#evidence-dates) qualify the integration guidance; exact settings and support depend on the provider's documentation and the actual environment.

The Copilot title and header identify the associated release and upstream origin. Its release date and source URL match `AGENTS.md`. Metadata adds no policy authority, and the adopted local contract remains canonical. Permitting provenance does not require a header on the one-line Claude import. Minimality preserves each bridge's loading and application role.

## Choosing or replacing methods

The method set was selected for recognized practices, freely accessible material sufficient to interpret their assigned roles, and distinct responsibilities. PDSA and Simple Design were judged sufficient for the agreed design alongside the focused engineering references, documentation conventions, and explicit collaboration rules. Additional umbrella frameworks were not needed to supply those responsibilities.

These selection criteria remain constraints on future additions or replacements unless explicitly revised. A proposed method change should explain the need it addresses, the accessibility of its required interpretive material, and any overlap or expansion of obligations. Changing a selection criterion is itself a design decision to identify explicitly; these constraints on the contract's evolution add no operating duties to ordinary project tasks.

## Keeping the contract portable

The entire `AGENTS.md` has a **hard project budget of fewer than 24,000 UTF-8 bytes after normalizing line endings to LF**. Replace each CRLF pair and any remaining CR with LF before counting the whole file's UTF-8 bytes; do not otherwise trim or reformat its contents. LF and CRLF copies of the same content therefore have the same budget count.

This conservative project budget is informed by [Codex's default 32 KiB combined instruction limit](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance) and Anthropic's [guidance to keep `CLAUDE.md` concise and human-readable](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md). The exact 24,000-byte threshold is a project choice: it leaves room below Codex's default for other loaded instructions and reflects Claude Code's guidance on limiting standing context. Importing the contract through `CLAUDE.md` still [loads its contents into context](https://code.claude.com/docs/en/memory#import-additional-files).

Check the normalized byte count after edits. Automated counts can help; automated enforcement is not required. Normalization defines this project's measurement; provider compatibility still depends on the actual delivered files, other loaded instructions, and tool configuration. Preserve useful spacing and headings. Meeting the budget does not establish clarity, adherence, or compatibility. Vendor changes can prompt a review but do not automatically change the project policy.

The byte budget concerns the standing contract itself, not the reasoning or work allowed for a task. Operational meaning remains self-contained in `AGENTS.md`; moving necessary conditions out of it would undermine portability even if the resulting file were smaller.

### Current wording trade-offs

Compact instructions reduce standing text while increasing the risk that readers must infer relationships. Ambiguity can cause clarification, source consultation, or rework; a smaller contract does not establish lower total token use. Review these current treatments when editing:

| Treatment | Interpretation risk and review focus |
| --- | --- |
| Implicit agent subjects, short labels, and slash groups | Keep the actor, every duty, and the relationship between grouped actions clear. |
| Broad knowledge-ownership and permitted-copy categories | Ensure readers can recognize facts, schemas, requirements, rationale, invariants, procedures, conventions, tests, and examples under the appropriate rule. |
| Concise definitions, architecture topics, record fields, and reports | Preserve distinguishing meaning and conditions; matching a name or keyword alone is insufficient. |
| Duties connected across sections | Preserve when knowledge is read, created, and updated; keep consequential conditions visible where the rule is applied. |
| Source links without per-rule numeric locators | The [exact assignments](#principles-and-reference-boundaries) preserve attribution; narrow consultation limits prevent the links from becoming open-ended research. |

These are interpretation risks, not additional operating rules or measured agent outcomes. Do not meet the byte budget by removing essential conditions or transferring them into a README.

Acceptance of the current wording compromises covers only the identified trade-offs. It does not authorize further loss of precision. Any new trade-off, including reduced explicitness without an intended rule change, is a design decision to identify for requester review. Its rationale needs to record what becomes less explicit, where the operative meaning remains, and the likely interpretation or effort consequences. Previous acceptance and matching counts do not establish that a further reduction is lossless or behaviorally equivalent.

## Assessing design changes

The design can be assessed at two levels: whether the contract works as a self-contained set of instructions, and whether a proposed change preserves or deliberately alters the meaning of its clauses. A standalone reading tests the first; comparison of strength, trigger, scope, exception, and meaning tests the second. The detailed patterns, fields, and obligations remain in `AGENTS.md`.

| Scenario | Design distinction to assess |
| --- | --- |
| Broad objective, including a new project | The agent limits its next commitment and keeps later work at outline level until detail is needed for the next decision. Necessary depth, affected dependencies, and validation remain within scope; the breadth of the goal does not justify an unconstrained first increment. |
| Ordinary authorized change | The agent selects a small increment and completes its checks before completing the increment, even without a chat report. Completion grants no additional permission or automatic documentation artifact; another increment can proceed under existing authorization unless a checkpoint requires a pause. |
| Completed exploration without a record trigger | Without material findings, significant lasting choices, or missing unfinished-work context, no record is required merely to log the discussion. |
| Material findings or significant proposals during review | Material findings reach appropriate permanent records even for discarded approaches. A concrete significant proposal ready for decision/review requires an ADR; brainstorming or a finding alone does not. Status reflects proposal, acceptance, rejection, or supersession under existing decision authority. Recording supplies no implementation authority or new approval checkpoint. |
| Verified factual documentation error during assessment | The agent may correct an ordinary document within the assessed scope, subject to §5.3. A verified mismatch with authoritative package configuration can justify correcting a README command; it does not authorize changing implementation, intended requirements, accepted decisions, or protected instruction files. |
| Task-relevant debt found during assessment | Evidenced debt may be recorded after considering accepted requirements and trade-offs. Any entry triggers classification-uncertainty and chat-disclosure duties. The general material-findings requirement still applies; neither classification nor recording authorizes a fix. |
| Requester or tool prohibits writes | Assessment permissions remain subject to §5.3. An explicit ban on creating, modifying, or deleting files covers records and factual documentation corrections; tool restrictions also remain binding. Findings and proposed text can be supplied in chat within those limits. |
| Continued execution and reporting | Several increments can complete without routine report drafting or output. At task completion, handoff, or when seeking input, the agent consolidates unreported work. Required findings and records are maintained throughout. |
| Requested or required disclosures | Disclosures affecting authorization or the next decision precede affected work. Other disclosures join the next consolidated report unless earlier timing is explicit. Requested timing, the early continuation notice, and reports when inquiries stop still apply. Reporting alone creates no approval checkpoint. |
| Selecting and revisiting work | Plan connects the requested outcome, permission, relevant context, and evidence to a useful next increment from the first request. Assess whether that connection is understandable, including when missing evidence or consequential constraints change the next step. Study and Act inform later planning; later work stays at outline level until detail is needed and revisions stay within authorization. |
| Investigation contradicts its prediction | An evidenced answer can complete the investigation while disproving the prediction; unmet implementation behavior remains incomplete. |
| Reading existing project documentation | Reading remains context gathering and needs no investigation framing even when answering a material question blocking the next decision. Routine code/test/configuration inspection is also context gathering. Scope and material-growth rules apply to all of it. Other blocking inquiry requires framing. |
| Blocking uncertainty requires inquiry beyond exempt context gathering | Before starting, the agent must state the question, scope, objective, effort limit, and needed evidence. No universal limit or requester-defined allowance is assumed. |
| Investigation reaches its stated effort limit | The attempt stops and unmet acceptance conditions, missing evidence, and uncertainty are reported. Existing scope/authority may permit a newly framed bounded attempt; requester caps/checkpoints and material-growth reassessment still apply. Exhaustion or a new label supplies no extra authority. |
| Acceptance-critical verification is unavailable | Sufficient alternative evidence can establish the same condition unless a specific check is required. Otherwise the condition remains unverified and validation incomplete unless validly revised. Disclosure alone does not satisfy it. |
| Equivalent evidence exists for an available acceptance check | The relevant available check must run. Equivalence alone does not permit substitution; the unavailable-check exception does not apply. |
| Known risk without an internal-quality compromise | Preserve the known risk under topic 11 without inventing a technical-debt classification. |
| Documentation-only work | Applicable methods and validation apply without requiring code or unit tests for their own sake. |
| Unexpected material growth in any phase | Establish increment/task baselines from requester direction or otherwise agent judgment without routine notice. Assess both increment and cumulative growth; only requester direction may revise the task baseline. New increments, attempts, and conversations do not reset it. Direction is required before materially greater effort, even within broad authorization. |
| New conversation without the original chat | Available project artifacts and the task's record entry, if needed, preserve resumption context. Startup lookup, conditional notice, and reconciliation establish the starting state; material gaps are reported. Work follows applicable authority; discovery and notification supply no permission. |
| Sufficient permanent context with no continuation record | Use available task context; compare a record only if present. No record needs creating merely because a new conversation starts. |
| Task B starts while task A remains unfinished | Use separate identified entries in the same root file when needed. Updating or retiring B's entry preserves A's needed context; retire the file only when no entry is needed. |
| Ongoing conversation pauses or is compacted | This does not trigger the new-conversation record-loading procedure. Ordinary context inspection, contradiction reporting, and record maintenance continue. |
| Any tool fails to load the contract | The package defines no separate bootstrap stop/report/resume policy. Neither a bridge nor a README supplies one, and an unloaded contract cannot govern the failure. Use actual tool and requester instructions and distinguish loading diagnostics from demonstrated application. |
| Root and directory instruction files | Only the three root-relative contract/bridge paths receive special edit protection. Compatible subtree additions remain possible under actual tool scope/priority; encountered conflicts are reported. |
| Abrupt interruption during an increment | Maintenance on material changes has preserved needed context, but the record may be stale. Reconciliation distinguishes completed, partial, unverified, and proposed work, with material differences or missing context reported. A previous check result does not establish the state of later edits. |
| New environment missing changes or evidence | Relevant project state, including partial/uncommitted work and missing artifacts, is identified and compared with what is available. Recorded progress is not mistaken for transferred files or verified current behavior; scope, uncertainty, and growth rules govern recovery. |
| Interrupted investigation with consumed allowance or a pending checkpoint | When project artifacts lack needed context, investigation-only work also needs a record, subject to requester and tool restrictions. It retains the inquiry's framing, known effort used, and uncertainty. Resumption or a recorded next step does not itself reset limits, clear pending checkpoints, or grant permission. Further work follows applicable direction and effort bounds. |
| Implementation resumes after substantial prior effort | Retain increment/task effort baselines, known cumulative effort, and uncertainty even without an interrupted inquiry. Compare remaining work against the retained task baseline; a new conversation does not authorize materially greater effort or create a fresh allowance. |

The relevant dependencies span [engineering](AGENTS.md#2-do--perform-the-authorized-work), [validation](AGENTS.md#3-study--assess-completion-and-learning), [knowledge retention](AGENTS.md#4-act--use-the-findings-and-determine-what-follows), and [shared policy](AGENTS.md#5-rules-throughout-the-cycle). Method conditions, appropriate-test recommendations, required validation, documentation scope, and requester authority all contribute to the resulting behavior.

Changes to protected instruction files follow [their authorization rule](AGENTS.md#53-instructions-contract-files-and-external-actions), including file-specific recommendations and necessary companion edits. Substantive policy changes need explicit identification. An explanation or review checklist cannot substitute for the actual clauses, and a shorter contract does not by itself establish equivalent agent behavior or token savings.

## Principles and reference boundaries

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

The coupling assignment excludes tip 46. The DRY, inheritance, and shared-state extracts linked above supply fuller accounts for their respective concerns. Attribution identifies supporting material, without claiming that one source states the contract's combined preservation duties verbatim.

[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) supply requirement-keyword semantics. They concern the strength of agent obligations, while EARS expresses system requirements and ADRs record choices and reasons. Supporting explanations include [IHI's testing-changes guidance](https://www.ihi.org/library/model-for-improvement/testing-changes) and [arc42's debt FAQ](https://faq.arc42.org/questions/C-11-1/); they add no operating obligations.

Under [source-consultation rules](AGENTS.md#54-consult-linked-sources-only-when-needed), material ambiguities can justify reading enough of a linked source to resolve the point, with the ambiguity, source, and answer reported. Clear rules need no principle research, and broader inquiry requires direction. Technical research for a task follows that task's scope and investigation limits. This distinction prevents an explanatory link from becoming an open-ended research assignment or importing stronger source rhetoric as policy.
