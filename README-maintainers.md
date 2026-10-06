# The design of AGENTS.md

[AGENTS.md](AGENTS.md) is a reusable, opinionated contract whose primary aim is to prevent unconstrained token consumption through small, complete steps toward a task objective. Necessary reasoning, work, and validation remain requirements within each step. This guide explains the design choices, their trade-offs, and the constraints that inform repairs, improvements, or redesign.

For adoption, use [README.md](README.md). For practical guidance, use [Getting more from AGENTS.md](README-powerusers.md). This guide has four parts:

1. [Design overview](#design-overview): the [design goals and boundaries](#design-goals-and-boundaries) and [a worked task](#how-the-design-works-in-a-task) showing how the parts connect.
2. [Design choices](#design-choices): [workflow choices](#workflow-design-choices) for the contract's layers, scope, learning, investigation, and requester control; [engineering choices](#engineering-choices) and [documentation choices](#documentation-choices) for methods, reasons, and conditions; and [why the bridges differ](#why-the-bridges-differ) across tools.
3. [Evolving the contract](#evolving-the-contract): [method selection](#choosing-or-replacing-methods), [portability](#keeping-the-contract-portable), and [current wording trade-offs](#current-wording-trade-offs) as constraints on changing `AGENTS.md`.
4. [Design reference](#design-reference): [design scenarios](#assessing-design-changes) for reviewing changes and the exact [reference assignments](#principles-and-reference-boundaries).

For a sequential understanding of the design, read the parts in order. For a proposed change, start with the relevant design choices, then use the evolution constraints and design reference to assess it.

## Design overview

### Design goals and boundaries

The motivating risk is especially visible in a new or poorly documented project. Without established requirements, interfaces, decisions, and conventions, planning and autonomous design have fewer constraints. Even a bounded objective can permit a large amount of work. The contract therefore limits each commitment and requires reassessment before unexpectedly greater effort, including sudden heavy use within one increment.

Its controls work together: small increments limit the immediate commitment; progressive detail defers distant decisions; bounded investigations limit inquiry; PDSA connects findings to subsequent choices. Engineering practices support quality within each step, while documentation retains knowledge for later work. Adequate analysis, completeness, and validation constrain every effort-saving choice.

Reports consolidate unreported work at task completion, handoff, or when seeking requester input. Routine progress reports are suppressed unless requested or otherwise required, reducing narration while authorized work continues. These mechanisms are best effort: total consumption may remain substantial. The design requires no pause after every increment and provides no token quota or guarantee of savings. The [practical explanation](README-powerusers.md#understanding-token-use) distinguishes reported results from consumption measurement.

The contract is self-contained. Guides explain it and bridges help tools apply it; neither supplies hidden operating duties. Project facts, build commands, requirements, and architecture come from the adopting project's code and documentation. This separation supports reuse without embedding an application's design in generic instructions.

Requester instructions take priority within the tool's actual hierarchy and permissions. The tool determines discovery, scope, and precedence of directory instructions, which may add subtree rules only when compatible with the root contract. The contract cannot supply capabilities, enforce permissions, or override native approvals. Its protection of instruction files and its authorization rules for external actions keep those limits explicit. It also does not supply a complete product-development process, branching strategy, workflow engine, or framework tutorial. Established methods cannot invent missing requirements or requester authority.

### How the design works in a task

Consider the CSV-import scenario from the [practical walkthrough](README-powerusers.md#from-a-request-to-a-result): report invalid rows and continue with valid rows. The **task objective** is that overall outcome. An **increment** is the next deliberately small, bounded step toward it, normally useful, understandable, reviewable, and verifiable on its own.

[PDSA—Plan–Do–Study–Act](https://deming.org/explore/pdsa/) begins with that request. Plan selects and bounds the work; Do performs it; Study assesses completion and the approach; Act uses the findings. Throughout, progression guards determine whether work may proceed, and triggered rules apply when their conditions arise; the [layer design](#three-interacting-layers) explains this division.

1. **Plan:** establish the objective and permitted work, then inspect the relevant project context. Suppose the requirements settle the input format, invalid-row rules, and line-number convention; existing tests support the reader's suitability; and inspection shows that field-count validation is missing. The row-processing code exposes the fields, header, and line number, suggesting a local implementation.

   This evidence supports choosing field-count validation: it advances an agreed requirement, addresses one concern, and can produce a useful, testable result without implementing every remaining invalid-row rule. The scope includes the affected code, tests, and documentation. Its limited dependencies and expected ease of reversal support a small commitment; neither substitutes for validation.

   Define **acceptance conditions**—reject mismatched rows, report their line numbers, and continue with valid rows, including one after a rejection—and a **prediction** that the existing row boundary will support the approach. These derived conditions follow the agreed requirements and define this increment's completion; they are not new system requirements. Selection, scope, conditions, and approach can be refined together as context becomes clear, within the governing instructions and requirements. Later work remains at outline level.
2. **Do:** implement the validation using current project conventions and Simple Design. Add relevant tests and update affected documentation at its authoritative location. Record an ADR if a significant lasting choice arises.
3. **Study:** check acceptance before completing the increment, including a valid row after a rejection. Separately assess whether the predicted local approach sufficed. Failed, unavailable, or omitted checks remain subject to disclosure under the reporting rules.
4. **Act:** use the evidence to retain, revise, or discard the approach within authorization. Material findings that are durable project knowledge trigger the [record rule](AGENTS.md#32-durable-findings-and-permanent-records). The [composition rules](AGENTS.md#4-how-the-layers-compose) then lead to finishing, a handoff, seeking required direction, or planning the next increment already covered by authorization. Continuing to another increment does not require drafting or emitting a routine report; reporting follows [§3.7](AGENTS.md#37-reporting).

The initial choice therefore depends on what Plan establishes. Unsettled consequential requirements need requester input; uncertainty about the reader may call for a bounded investigation before implementation. The agent is responsible for choosing and defining the next increment, within the contract's consultation and authorization rules.

The example connects the design's parts. Requirements provide intended behavior; inspection and existing checks establish the starting point; Study supplies new evidence; Act uses it to inform subsequent Plan phases. Records preserve durable material findings and lasting choices; transient task facts are only reported when the reporting rules require it. The supported local validation approach may help plan another rule, while evidence of wider parser limitations changes the basis for that next decision.

The field-count result can therefore inform another authorized validation increment before any routine chat report is produced. At task completion, a handoff, or when seeking requester input, the agent consolidates unreported work. Required disclosures still apply: a discovery that requires an unexpectedly larger shared-parser redesign triggers explanation and reassessment immediately, in whichever phase it occurs. The agent then waits for requester direction before the added work. A requested operator guide could be another increment, shaped by its reader's need. Neither a completed step nor a named method automatically creates an ADR, guide, or fresh approval requirement.

The [practical walkthrough](README-powerusers.md#from-a-request-to-a-result) shows the user-facing interaction. The following sections explain the reasons and boundaries behind it.

## Design choices

Each choice below connects a design problem with the approach taken, its reasons, and its trade-offs. The linked `AGENTS.md` clauses remain authoritative for exact operating behavior.

### Workflow design choices

#### Three interacting layers

The contract separates three concerns that interact during every task. The [work cycle](AGENTS.md#1-work-cycle) describes what the agent is doing with an increment: planning, performing, studying, and acting on findings. [Progression guards](AGENTS.md#2-progression-guards) determine whether work may proceed or needs requester direction: authority and scope, requester decisions, effort baselines and growth, bounded inquiry, and continuation to another increment. [Triggered rules](AGENTS.md#3-triggered-rules) are duties and permissions that arise whenever their conditions occur—for example, a new system requirement, a durable finding, a significant decision, affected documentation, a reporting point, or an external action—each at its stated strength.

The division follows how these concerns behave. Authorization, effort growth, and requester involvement can matter in any phase, and a durable finding can emerge while planning as easily as while acting. Placing such rules inside one phase would suggest they apply only there, or require readers to reinterpret earlier phases after reaching later material. Presenting the cycle first shows the ordinary path; the guards then make the control state explicit; triggered rules stay independent of phase. A final [composition section](AGENTS.md#4-how-the-layers-compose) states how the layers combine: work proceeds through the cycle, guards govern relevant transitions and decisions, triggered rules apply when their conditions arise, and after Study and Act the agent completes, hands off, seeks required direction, or returns to Plan for another increment already covered by authorization.

No layer grants authorization by itself. A next cycle step, a satisfied guard, or a fulfilled duty never extends what the requester and tool permit, and completing an increment, reporting, recording a decision, discovering a finding, or exhausting an inquiry creates none. Guards are not additional phases; triggered duties authorize no otherwise unauthorized work, and triggered permissions authorize nothing beyond their terms.

This organization expresses design intent: making the operating model and its cross-cutting relationships explicit while preserving normative behavior. The repository holds no measurement showing that it improves human comprehension, agent adherence, or token use.

#### Small commitments with sufficient depth

The requester supplies goals, permission, and relevant constraints. The agent supplies decomposition, acceptance conditions, validation, effort assessment, and recognition of required consultation. These standing responsibilities let an ordinary outcome-oriented request start useful work. A requester may still select a step or add review points.

Within Plan, increment selection connects the requested outcome and permission with current behavior, relevant dependencies, and available evidence. The agent looks for the smallest useful result that can be completed within scope, including the affected artifacts and checks. When blocking uncertainty prevents a sound implementation choice, obtaining bounded evidence can itself be the useful result.

The [four effort factors](AGENTS.md#22-decisions-and-requester-interaction)—scope, uncertainty, consequence, and reversibility—guide that judgment. Scope includes affected behavior, artifacts, dependencies, and system boundaries. A few changed lines can affect many callers or an irreversible migration; a narrow, understood, low-impact, reversible change can use brief inspection, action, and validation. Reporting follows its own triggers and remains proportionate.

These criteria constrain selection without prescribing a numeric score, an exhaustive comparison of possible increments, or a uniquely correct sequence. Requiring a complete ranking or detailed backlog before starting would expand the initial planning commitment. The design instead calls for enough reasoning to support the next useful step and uses its evidence to refine later work. This contributes to the token-control goal while preserving the analysis and validation needed for a complete result.

Depth follows the next decision at the current abstraction level. Architecture analysis may need careful examination of boundaries, alternatives, and risks without specifying every future API or function. Later work stays at outline level until the next decision needs detail; depth follows uncertainty, consequence, risk, reversibility, and proximity to execution. Explicit authorization can cover broader analysis at the relevant abstraction level.

Completeness is assessed within the increment's scope. Evidence, enabling infrastructure, or migration groundwork can be useful results as well as functionality. Before a step that cannot stand alone, the agent explains why, what remains usable or testable, and how to undo it. Recovery reduces the cost of a mistaken approach; it grants no permission for destructive effects. A required stop may leave work incomplete, while review-boundary coherence still applies. A small scope cannot excuse shallow reasoning, omitted dependencies, or incomplete work presented as finished.

#### Learning throughout the work

The [Deming Institute's PDSA account](https://deming.org/explore/pdsa/) connects an approach and expected result with observation and the next decision. Small increments bound commitments; PDSA's contribution is learning which approach remains suitable and what to do next. Passing tests alone does not establish that learning role: the implications still inform Act and subsequent planning.

The contract's [work cycle](AGENTS.md#1-work-cycle) starts with the request. Plan includes context gathering, the overall objective and permitted work, outlining an approach, and selecting the next increment. Study assesses completion and observations; Act uses those findings to retain, revise, or discard the approach within authorization. Results can reshape later detail without changing the agreed outcome or granting more authority.

Terms and the layer overview precede the work cycle. Methods appear near their principal contribution—engineering practices in Do, validation in Study, and documentation and decision methods among the triggered rules—but apply whenever triggered in any phase, and the progression guards apply throughout. Tests can be planned before implementation; decisions and documentation are maintained as facts emerge. Phases can overlap or repeat, and routine work needs no worksheet, formal experiment, or separate phase reports.

PDSA's Plan phase organizes reasoning. A tool's Plan mode has its own proposal and approval procedures. Neither expands authorization. These distinctions let the workflow apply proportionally to implementation, investigation, and documentation without inventing separate mandatory deliverables.

#### Completion, predictions, and bounded investigation

**Acceptance conditions** define the observable result needed to complete the increment; **validation** is the separate act of checking results against them. The conditions are completion criteria, not system requirements; new or revised required behavior needs authorized requirement work under the EARS and canonical-owner rule. The boundary is whether authorized work establishes or changes behavior as required of the system beyond the current task's execution: such behavior is a system requirement whatever its source. Task objectives, acceptance conditions, and requester statements are not requirements merely by being stated, restating a canonical requirement creates no duplicate, and analysis or review alone cannot create or change requirements. The agent first identifies conditions already set by the requester or authoritative project sources, then inspects relevant context before deriving or refining the rest, so derived conditions are not settled before the evidence is read. A **prediction** states the expected result of the approach; comparison with observations informs whether to retain or revise that approach. Revising a prediction changes neither requirements nor acceptance conditions.

Revision authority follows the source of each condition. Requester-supplied requirements or conditions change only with requester authority; canonical requirements change only through authorized requirement work; agent-derived conditions can be refined only within requester instructions, project requirements, scope, and decision authority. A failed check or difficult implementation never justifies weakening, replacing, or reinterpreting any of them, so failed validation cannot lower the completion bar.

This separation allows an investigation to succeed by disproving an assumption. Evidence that a reader splits a quoted comma can answer a question about its behavior, while an implementation required to preserve that field remains incomplete. A successful sample also supports only the conclusion justified by that sample. The [practical investigation example](README-powerusers.md#when-an-investigation-is-needed) develops both outcomes.

Inspecting the relevant code, callers, tests, configuration, and directly related dependencies to establish starting context, and all reading of existing project documentation, are context gathering. The documentation exemption still applies when reading is needed to answer a material question blocking the next decision. The boundary depends on the activity's purpose, not its label or a numeric threshold: other activity aimed at resolving such uncertainty, such as experiments or exploration beyond that context, is inquiry and requires framing under the [inquiry guard](AGENTS.md#24-context-gathering-and-bounded-inquiry): state the question, scope, objective, effort limit, and needed evidence before starting or continuing it. An **investigation effort limit** ends that inquiry even without the evidence. This makes the commitment visible before consuming it; the requester need not prescribe or approve every limit. Context gathering remains subject to scope and material-growth controls. Consequential unresolved intent or constraints still require involvement.

No default amount, unit, or selection formula is prescribed. Choosing a useful bound therefore requires judgment and provides no automatically enforced timeout or token quota. The one-attempt allowance in the practical example is illustrative.

Obtaining the evidence or reaching the limit ends the inquiry, not necessarily the task. The required report is not itself an approval checkpoint: work may continue under existing authorization unless another rule—such as missing evidence that blocks safe continuation, material effort growth, unresolved consequential intent, or a requester checkpoint—requires direction. If acceptance conditions remain unmet, the report identifies incomplete work, missing evidence, and uncertainty. Neither a negative finding nor an exhausted allowance supplies more authority. Existing scope and authority may nevertheless permit a new bounded attempt at an unresolved question, with new framing under §2.4 and the [growth reassessment](AGENTS.md#23-effort-baselines-and-material-growth). Requester limits and checkpoints remain binding; materially greater effort requires direction before it proceeds. The agent must explain any need for broader research or a wider design decision. The [Study rules](AGENTS.md#13-study--assess-completion-and-learning) preserve the distinction between learning and completion across all work types.

#### Authorization and requester decisions

An increment limits work undertaken at once; a report can summarize several increments; a checkpoint reserves a decision for the requester. Ordinary increments can [continue under existing authorization](AGENTS.md#25-continuing-to-another-increment) without routine reports. Their completion supplies no additional permission and creates no automatic pause.

The [material-growth checkpoint](AGENTS.md#23-effort-baselines-and-material-growth) addresses a separate problem: authorized work can turn out to require unexpectedly greater effort. The agent establishes increment and cumulative-task effort baselines from requester direction where supplied, otherwise from its own judgment without routine notification. Baselines can be qualitative; they are not token quotas. The task baseline is set at its start and each increment's when that increment is planned. Evidence can change current estimates, but both increment and cumulative growth are assessed against the baselines, not the latest estimate. Only requester direction can revise an established baseline; approving disclosed growth revises the affected baselines to include only that commitment, so it does not retrigger the checkpoint while later growth is still measured from the revised baselines; new increments or attempts do not reset the task baseline, and a new increment baseline cannot absorb growth already found without requester direction. Retaining the baselines prevents repeated small additions, renewed attempts, or relabeled estimates from evading the checkpoint. The agent must explain a material increase and await direction before taking it on, even when the outcome and broad authorization are unchanged. This gives the requester control that a scope boundary alone cannot provide. Baselines are working task state for that comparison; establishing them requires no project record, worksheet, or chat report. A handoff report transfers the task baseline, any unfinished increment's baseline, and still-relevant approved revisions so the next context continues the same comparison rather than starting a fresh one; if they were not transferred, it recovers them from available task state or obtains requester direction before further effort-bearing work; without that transfer, a multi-context task could evade the checkpoint. See the [practical growth cases](README-powerusers.md#when-the-work-grows-unexpectedly).

In the [requester-interaction guard](AGENTS.md#22-decisions-and-requester-interaction), the [requirement keywords](AGENTS.md#terms-and-requirement-keywords) preserve distinct strengths:

- Material unresolved intent or permission must be escalated; missing consequential constraints must be agreed as needed.
- Asking before an unsettled consequential choice is a strong recommendation with justified exceptions.
- Easily reversible routine details may be chosen within agreed limits; material assumptions remain visible.

A SHOULD exception cannot bypass a MUST checkpoint or invent a consequential constraint. Reporting a consequential choice without prior direction exposes reasons, effects, uncertainty, and revision or reversal options; it cannot retroactively authorize the choice. Native permissions and approval controls remain the enforceable boundaries.

Analysis and review can establish lasting project knowledge before implementation, so the contract separates two questions. The [assessment write ceiling](AGENTS.md#21-authority-and-scope), a progression guard, decides which writes an assessment-only task may make at all, alongside the other limits on permitted work. The triggered [material-findings rule](AGENTS.md#32-durable-findings-and-permanent-records), [decision rule](AGENTS.md#33-significant-decisions-adrs), and [debt rule](AGENTS.md#34-technical-debt) decide whether a record is due, each with its own trigger and strength; they apply whenever their conditions arise, not only at the end of a cycle. Neither substitutes for the other: the ceiling cannot make an optional debt entry mandatory, and a triggered record cannot widen the ceiling into implementation, new or changed system requirements, accepting or changing decisions beyond existing authority, unrelated documentation repairs, or backfills. A **permanent record**—the canonical project document owning the topic, not chat or working notes—preserves the finding and evidence; it cannot act as permission to implement the recommendation.

The findings trigger requires both materiality and durability so that assessment retains what later work needs, including lasting learning from discarded approaches, without becoming a work log; transient task facts, such as a temporary CI outage, follow only the reporting rules. Requiring the minimum record when no suitable owner exists keeps a mandatory finding from being lost while preventing an assessment from turning into a documentation backfill: no placeholders or empty sections are added, and other arc42 gaps remain proposals. A prohibited write leaves the obligation visible as unfinished work instead of treating chat as a record. Verified factual corrections are a separate permission because they align an existing description of current project facts with its owner rather than retaining new knowledge; excluding requirements, decision records, and protected instruction files keeps changes of intent out of assessment. All these writes remain subject to authorized scope, [requester restrictions](AGENTS.md#21-authority-and-scope), [protected-file rules](AGENTS.md#38-instructions-protected-files-and-external-actions), and tool permissions and approvals, which can prevent them; broader documentation repairs and external actions retain their own authorization requirements. The [practical examples](README-powerusers.md#records-during-review-and-exploration) show each case and the effect of a no-edit instruction.

#### Reporting and continued execution

Completing an increment and reporting to the requester serve different purposes. PDSA requires the work to be assessed and its findings used, even when no chat report follows. [AGENTS.md §3.7](AGENTS.md#37-reporting) consolidates unreported work at task completion, handoff, or when seeking requester input. It prohibits drafting or outputting routine progress reports at other times unless requested or required.

Suppressing drafting as well as output avoids preparing reports merely to hold them back from chat. Disclosures affecting authorization or the next decision precede the affected work; other disclosures join the next consolidated report unless earlier timing is explicit. The report when a bounded inquiry ends retains its timing but is not itself an approval checkpoint. Nonblocking debt recording, for example, does not require an immediate chat interruption. Material findings, decisions, and affected documentation retain their owners and maintenance triggers; record maintenance does not wait for the report. No separate reporting log or record is required for every increment. Tool instructions and requester-selected reporting remain applicable.

The trade-off is less routine visibility during autonomous work and a consolidated account at the next reporting occasion. Reporting alone reserves no time for review and creates no approval checkpoint. Scope limits, bounded investigations, and mandatory reassessment for material growth continue to control the work; fewer reports establish no measured token saving.

Reports remain proportionate and follow the contract's requirements for content, file delivery, and blocked-edit fallbacks. The [usage guide](README-powerusers.md#assess-the-result) explains what the requester receives.

### Engineering choices

#### Simple Design: choosing what the current solution needs

Beck's [Simple Design, explained by Fowler](https://martinfowler.com/bliki/BeckDesignRules.html), supplies four criteria: meet requirements and pass tests, express intent, avoid duplicated knowledge, and retain only necessary elements. They assess the current solution; fewer classes or lines alone cannot establish simplicity.

Hard memory, latency, throughput, concurrency, cost, or scale requirements may justify complexity. An imagined future extension does not provide equivalent evidence. Supporting one agreed input format can be complete without a framework for unspecified formats, while still including its necessary error handling and checks. A documented optimization strategy supplies project context and is a strong default unless the task conflicts with or materially extends it. Material trade-offs remain visible.

#### DRY: keeping knowledge consistent as work progresses

The [Pragmatic Programmer's DRY account](https://media.pragprog.com/titles/tpp20/dry.pdf) concerns knowledge that would otherwise need independent maintenance in several places. Canonical ownership reduces the risk of divergent facts, rules, or explanations across code and documents.

A setting can own a retry limit while a guide explains its purpose and links to it. Two unrelated limits may have the same value without representing shared knowledge. Necessary test, example, summary, generated, protocol, migration, and compatibility copies can remain with a clear canonical owner and update process. Resemblance alone supplies no reason to merge them.

#### Component boundaries, refactoring, and validation

Clear responsibilities, limited coupling, visible side effects, and explicit resource ownership make the effects of a change easier to understand. The [public tips](https://pragprog.com/tips/) and [shared-state extract](https://media.pragprog.com/titles/tpp20/shared-state.pdf) support these concerns; their exact assignments appear [below](#principles-and-reference-boundaries). Separating concurrent coordination from sequential logic where practical supports clear ownership without prescribing a universal asynchronous architecture.

[Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) preserves observable behavior. An intended and authorized behavior change needs corresponding requirements, tests, and documentation. Documented design invariants protect promised properties; project patterns can change through scoped, justified, validated improvements. Neither distinction requires preserving a defect when changing it is intended and authorized.

The dead-code condition matters because registration, reflection, or external callers may make apparently unused code reachable. Clear unreachability or direct obsolescence from the authorized change is needed for removal *as dead code*. Explicitly authorized removal of live functionality is a different case.

#### Validation and test evidence

Relevant available checks against acceptance conditions are mandatory before completing each increment, independently of whether a report is produced then. Appropriate tests for behavior changes, defect repairs, and clarified edge cases are a SHOULD default with justified exceptions. Validation covers affected behavior, risk, and hard operational limits for every work type; passing tests cannot replace a missing requirement or necessary check. Failed, unavailable, and omitted checks must be disclosed under the [reporting rule](AGENTS.md#37-reporting); any need for requester involvement still follows the [progression guards](AGENTS.md#2-progression-guards).

An unavailable verification method and an unverified acceptance condition are distinct. Sufficient alternative evidence may substitute only when the original check is unavailable and is not specifically required. Availability depends on current authorization, tool access, permissions, credentials or resources, and prerequisites with ordinary expected setup, not on convenience: an available relevant acceptance check still runs even if an alternative could provide equally sufficient evidence. Needing missing access or resources, or materially more work, to run it is disclosed and handled by the authorization and growth rules rather than silently absorbed. Without sufficient evidence, the condition remains unverified and validation incomplete unless that condition is validly revised under existing authority; disclosure alone cannot establish it. A pre-existing failure is assessed for relevance and disclosed, without automatically blocking unrelated work. The [practical validation examples](README-powerusers.md#assess-the-result) distinguish available checks, equivalent local checks, insufficient mocked evidence, and a specifically required CI result.

[Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html) makes a unit test's starting conditions, action, and expected result understandable. For a quoted field containing a comma, those parts are the sample, the parser call, and the intact-field assertion. The contract requires neither literal labels nor a testing framework, and prohibits weakening tests merely to pass.

#### Focused techniques and how they work together

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

### Documentation choices

Requirements describe intended behavior, accepted decisions retain choices and reasons, architecture describes boundaries and guarantees, and schemas and package metadata declare their own constraints. Code, tests, and execution provide evidence of implemented behavior. Examples and notes govern only when explicitly labeled as rules. Their roles explain why executable behavior does not automatically overrule a requirement. The contract intentionally has no global precedence ladder among these artifacts: an earlier total ordering was removed because a single ranking cannot fit artifacts that own different kinds of knowledge. Conflicts need visible evidence and inference, and the governing artifact is identified by the kind of knowledge and its canonical owner. If ownership does not resolve a consequential conflict, the agent escalates under the requester-interaction rules instead of inventing a fallback order. Instruction files govern agent conduct rather than proving project facts, while requirements, constraints, and facts stated by the requester remain legitimate task context.

Documentation informs Plan and changes as work establishes facts and choices. Producing a guide or updating affected documentation is Do work. Study checks its acceptance conditions; Act uses the findings and retains relevant learning. Requirement, record, decision, debt, documentation, and architecture duties are [triggered rules](AGENTS.md#3-triggered-rules) because their conditions can arise in any phase; their records are read and maintained whenever needed, and the rules authorize no work beyond their terms.

Updates follow affected documentation: the canonical owners of changed knowledge and the known documents that directly depend on it, such as a README repeating a changed value, whether or not they link to the owner and whether or not they have been read yet. Such dependents are typically known from the task, artifacts being inspected, explicit references, canonical-owner relationships, or established source/update relationships. A link alone makes a document worth checking, not necessarily editing. Neither this duty nor coverage expectations authorize searching for unknown dependents or a repository-wide audit, backfill, or reorganization; signs of wider staleness may lead to a proposal, not automatically expanded scope. Documentation-only work uses the same increment, validation, and review rules as other work. Current-system descriptions follow reality, with proposals and unfinished work clearly identified.

#### arc42: shared architectural context as the project grows

[arc42](https://arc42.org/overview/) supplies twelve architectural topics spanning goals and constraints, structure and operation, crosscutting concepts, decisions, quality, risks, and terminology. Shared content expectations aim to reduce reinvention and relearning across repositories. They give an empty project questions to answer as evidence develops, without requiring the entire design to be settled first.

Applicable topics set the target coverage. Architecture content uses known facts and keeps material unknowns visible; empty headings and invented details do not establish coverage. An uncovered topic is a known gap that triggers an improvement proposal, which authorized work should implement and the requester may decline, postpone, or limit, so a partial or minimal architecture document does not itself breach the contract. [Incremental documentation](https://faq.arc42.org/questions/B-14/) and [appropriate depth](https://faq.arc42.org/questions/B-4/) support keeping content useful as the system develops. [Quality scenarios](https://docs.arc42.org/section-10/) make goals assessable: “imports should be fast” still needs an agreed workload and measure.

One architecture document is the initial SHOULD default, using the existing documentation folder stated in `README.md`, otherwise repository-root `docs/`. Because root `docs/` is the standard default, `README.md` needs to state documentation locations only when they differ from it; creating a document in `docs/` therefore needs no `README.md` edit. This keeps early information together. An adequate existing arrangement can remain, and coherent parts can separate as reading and maintenance warrant it. Layout is flexible; known coverage gaps still require proposals and warrant improvements within authorized scope, subject to requester limits or deferral. Summaries link to canonical requirements and ADRs, while implementation detail stays near code and tests.

Topic 11 covers known risks as well as technical debt under the contract's definition. The risk category is not restricted to internal-quality compromises: external dependencies and operational circumstances can create known risks even when implementation quality is adequate. The distinction preserves the scope of [arc42's risks and debt topic](https://docs.arc42.org/section-11/) without classifying every risk as debt or importing an additional risk-management procedure.

#### EARS: making required behavior explicit

[EARS (Easy Approach to Requirements Syntax)](https://alistairmavin.com/ears/) gives natural-language requirements consistent condition-and-response patterns. For example:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

The pattern exposes behavior to implement and check. It cannot decide whether to reject one row or the whole file, or define a row's line number for a particular format. Those remain project decisions. EARS applies to new or revised in-scope system requirements; unchanged requirements need no automatic conversion. The [contract](AGENTS.md#31-new-or-revised-system-requirements) owns the five patterns and combined state-before-event form. Rationale belongs with significant choices; EARS adds no mandatory rationale field to each requirement.

#### ADRs: preserving the reasons for lasting choices

[Architecture Decision Records](https://docs.arc42.org/section-9/) retain reasons that code alone may not reveal. A streaming-parser decision can connect a memory constraint and experiment evidence with consequences for error reporting. Later work can assess that reasoning against new evidence instead of reconstructing it.

Significant lasting choices in scope need an ADR when a concrete proposal is ready for decision or review, in or linked from arc42's decision section. This timing captures developed proposals before acceptance without requiring an ADR for every exploratory idea; routine local choices normally need none. Status distinguishes proposed, accepted, rejected, and superseded decisions. Accepted records a decision made under existing authority and consultation rules, not completed implementation or a new ADR-specific approval. Material history, influential failed approaches, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links explain the basis and applicability of those project decisions. This does not require exploring every possible alternative or backfilling decisions outside authorized scope.

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

Exceeding the target is exceptional but acceptable when further reduction would materially compromise normative fidelity or human comprehensibility. Before such excess is accepted, the contract receives a deliberate compression review. That review removes genuine redundancy and low-value explanatory detail before it compresses core control semantics, such as authorization, effort growth, requester interaction, inquiry, and continuation. Even over target, the contract keeps meaningful headroom below applicable provider and project combined instruction-loading limits, such as Codex's default above, so directory instructions and other context can coexist. The project defines no separate provider-independent ceiling; those applicable combined limits bound the acceptable excess.

Check the normalized byte count after edits. Automated counts can help; automated enforcement is not required. Normalization defines this project's measurement; provider compatibility still depends on the actual delivered files, other loaded instructions, and tool configuration. Preserve useful spacing and headings. Meeting the target does not establish clarity, compatibility, equivalent behavior, agent adherence, or token savings. Vendor changes can prompt a review but do not automatically change the project policy.

The size target concerns the standing contract itself, not the reasoning or work allowed for a task. Operational meaning remains self-contained in `AGENTS.md`; necessary operating semantics must not move into a README to satisfy the target, because that would undermine portability even if the resulting file were smaller. Compactness is therefore subordinate to normative fidelity and usable comprehension, while standing instruction context remains a constrained resource.

### Current wording trade-offs

Compact instructions reduce standing text while increasing the risk that readers must infer relationships. Ambiguity can cause clarification, reference consultation, or rework; a smaller contract does not establish lower total token use. Review these current treatments when editing:

| Treatment | Interpretation risk and review focus |
| --- | --- |
| Implicit agent subjects, short labels, and slash groups | Keep the actor, every duty, and the relationship between grouped actions clear. |
| Broad knowledge-ownership and permitted-copy categories | Ensure readers can recognize facts, schemas, requirements, rationale, invariants, procedures, conventions, tests, and examples under the appropriate rule. |
| Concise definitions, architecture topics, record fields, and reports | Preserve distinguishing meaning and conditions; matching a name or keyword alone is insufficient. |
| Layered organization with section cross-references | Guards and triggered rules apply across work-cycle phases. Keep the composition section and section references accurate, keep consequential conditions visible where a rule is applied, and avoid placement that implies a guard is a phase or a triggered rule applies only in one phase. |
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
| Ordinary authorized change | The agent selects a small increment and completes its checks before completing the increment, even without a chat report. Completion grants no additional permission or automatic documentation artifact; another increment can proceed under existing authorization unless a checkpoint requires a pause. |
| Completed exploration without a record trigger | Without durable material findings or significant lasting choices, no record is required merely to log the discussion. Transient task facts, such as a temporary CI outage or a failed experiment relevant only to the current attempt, follow the reporting rules only. |
| Material findings or significant proposals during review | A [finding](AGENTS.md#32-durable-findings-and-permanent-records) needs a permanent record only when it is both material and durable, even if it comes from a discarded approach; a missing owner leads to the minimum record rather than backfill, and a prohibited write is reported as unfinished work. A concrete significant proposal ready for decision or review requires an [ADR](AGENTS.md#33-significant-decisions-adrs) retaining the evidence that materially shaped it rather than routine PDSA history; brainstorming or a finding alone does not. Status reflects existing decision authority. Recording supplies no implementation authority or new approval checkpoint. |
| Verified factual documentation error during assessment | The agent may make an existing description of current project facts within the assessed scope match the canonical owner of that kind of knowledge, subject to scope, requester restrictions, §3.8, and tool permissions. Requirements, decision records, and protected instruction files are excluded. A verified mismatch with authoritative package configuration can justify correcting a README command; it does not authorize changing implementation, intended requirements, accepted decisions, or protected instruction files. |
| Task-relevant debt found during assessment | Evidenced debt may be recorded after considering accepted requirements and trade-offs. Any entry triggers classification-uncertainty and chat-disclosure duties. The general material-findings requirement still applies; neither classification nor recording authorizes a fix. |
| Requester or tool prohibits writes | Assessment permissions remain subject to requester restrictions (§2.1) and §3.8. An explicit ban on creating, modifying, or deleting files covers records and factual documentation corrections; tool restrictions also remain binding. Findings and proposed text can be supplied in chat within those limits, but chat does not satisfy a permanent-record obligation; the unmade record is reported as unfinished work. |
| Continued execution and reporting | Several increments can complete without routine report drafting or output. At task completion, handoff, or when seeking input, the agent consolidates unreported work. Required findings and records are maintained throughout. |
| Requested or required disclosures | Disclosures affecting authorization or the next decision precede affected work. Other disclosures join the next consolidated report unless earlier timing is explicit. Requested timing and reports when inquiries stop still apply. Reporting alone creates no approval checkpoint. |
| Selecting and revisiting work | Plan connects the requested outcome, permission, relevant context, and evidence to a useful next increment from the first request. Assess whether that connection is understandable, including when missing evidence or consequential constraints change the next step. Study and Act inform later planning; later work stays at outline level until detail is needed and revisions stay within authorization. |
| Investigation contradicts its prediction | An evidenced answer can complete the investigation while disproving the prediction; unmet implementation behavior remains incomplete. |
| Reading existing project documentation | Reading remains context gathering and needs no investigation framing even when answering a material question blocking the next decision. Inspecting relevant code, callers, tests, configuration, and directly related dependencies to establish context is also context gathering. Scope and material-growth rules apply to all of it. Other activity aimed at resolving material uncertainty blocking the next decision is inquiry whatever its label and requires framing. |
| Material uncertainty blocking the next decision requires inquiry beyond exempt context gathering | Before starting or continuing it, the agent must state the question, scope, objective, effort limit, and needed evidence. No universal limit or requester-defined allowance is assumed. |
| Investigation reaches its stated effort limit | That inquiry ends, not necessarily the task, and unmet acceptance conditions, missing evidence, and uncertainty are reported. The report is not itself an approval checkpoint; other rules decide whether work continues. Existing scope/authority may permit a newly framed bounded attempt; requester caps/checkpoints and material-growth reassessment still apply. Exhaustion or a new label supplies no extra authority. |
| Acceptance-critical verification is unavailable | Sufficient alternative evidence can establish the same condition unless a specific check is required. Otherwise the condition remains unverified and validation incomplete unless validly revised. Disclosure alone does not satisfy it. |
| Equivalent evidence exists for an available acceptance check | The relevant available check must run. Equivalence alone does not permit substitution; the unavailable-check exception does not apply. |
| Known risk without an internal-quality compromise | Preserve the known risk under topic 11 without inventing a technical-debt classification. |
| Documentation-only work | Applicable methods and validation apply without requiring code or unit tests for their own sake. |
| Unexpected material growth in any phase | Establish increment/task baselines from requester direction or otherwise agent judgment without routine notice. Assess both increment and cumulative growth against the baselines, not the latest estimate; only requester direction may revise an established baseline, and approval of disclosed growth revises the affected baselines to include only that commitment. New increments, attempts, or handoffs do not reset the task baseline, and new increment baselines do not absorb growth already found unless requester direction permits it. Handoff reports transfer the baselines; a continuing context without them recovers them or obtains direction rather than setting fresh ones. Direction is required before materially greater effort, even within broad authorization. |
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
