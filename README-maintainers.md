# The design of AGENTS.md

[AGENTS.md](AGENTS.md) is a reusable, opinionated contract for collaboration with coding agents. This document explains its attributes, the choices behind them, and the principles on which they rest. These explanations provide a technical foundation for understanding the contract and for informed repairs, improvements, or redesign.

For installation and a first task, start with [README.md](README.md). For practical examples and fuller usage guidance, see [Getting more from AGENTS.md](README-powerusers.md).

- [Design goals and the PDSA cycle](#why-it-is-built-this-way)
- [Collaboration and effort control](#collaboration-and-effort-control)
- [Engineering methods](#engineering-methods-quality-within-a-small-increment)
- [Documentation methods](#documentation-as-input-and-output)
- [Principles and source boundaries](#principles-and-reference-boundaries)
- [Continuation](#continuation-design), [bridges](#why-the-bridges-differ), and [portability](#keeping-the-contract-portable)
- [Assessing design changes](#assessing-design-changes)

## The contract and its boundaries

The operating rules, definitions, conditions, and exceptions are self-contained in `AGENTS.md`. Its companion bridges allow tools to discover and apply the same local contract. The technical explanations here describe that design; the agent does not need to read this guide to obtain additional operating obligations.

The contract supplies collaboration policy. Project facts, build commands, requirements, and architecture come from the adopting project's documentation and code. This separation permits reuse across new and established projects without embedding a particular application's design in the generic instructions.

Requester instructions take priority within the tool's actual hierarchy and permissions. Directory instructions follow the tool's scope and precedence rules. The contract cannot supply capabilities, enforce permissions, or override native approval controls. Its protection of instruction files and its authorization rules for external actions keep those limits explicit.

## Why it is built this way

The contract aims to control effort through intentionally small, complete increments. A bounded task can still be large; small increments make results and unexpected growth visible while preserving the reasoning and validation needed for each result. Total consumption may remain substantial. This is a best-effort collaboration mechanism, with no token quota or guarantee of savings; the [usage explanation](README-powerusers.md#understanding-token-use) explains usage visibility.

Established methods give recurring tasks a defined approach, especially while an empty or poorly documented project has few facts to constrain exploration. They cannot supply missing requirements or requester authority. PDSA organizes work and learning; Simple Design guides implementation; focused engineering and documentation references address distinct concerns. The contract defines their scope, strength, and collaboration boundaries. It does not attempt to supply a complete product-development process, branching strategy, workflow engine, or framework tutorial.

### PDSA: learning through small increments

The [Deming Institute's Plan–Do–Study–Act account](https://deming.org/explore/pdsa/) connects an approach and its expected result with observation and the next decision. Its contribution here is learning as work progresses: evidence can change the approach and later detail without changing the agreed outcome or granting more authority.

The contract presents terms and a workflow overview before the four phases. This gives readers a route from the request through work, assessment, reporting, and the next decision. Methods appear near their principal contribution, while their triggers and the shared rules apply throughout. Tests can be planned before implementation; decisions and documentation are maintained as facts become established. Phase placement does not postpone those duties or require worksheets, separate phase reports, or a formal experiment for routine work.

PDSA's Plan phase and a tool's Plan mode have different roles. The former organizes reasoning; the latter has the tool's own proposal and approval procedures. Neither supplies wider authorization.

### Objectives, acceptance, predictions, and stopping

These distinctions prevent useful learning from being mistaken for completed work:

| Concept | Question answered | Parser-investigation example |
| --- | --- | --- |
| Task objective | What overall outcome was requested? | Develop an import tool. |
| Increment objective | What bounded outcome is sought now? | Determine whether one candidate preserves a quoted field containing a comma. |
| Acceptance conditions | What establishes completion? | Report an evidenced answer for a relevant sample, including its limits. |
| Prediction | What result is expected from the approach? | The quoted field remains intact. |
| Validation | Does the evidence establish acceptance? | Check the sample, observed output, and reported conclusion. |
| Investigation effort limit | When must inquiry stop despite incomplete evidence? | After the focused experiment stated for this inquiry. |

The agent establishes the increment and its acceptance conditions from the request and relevant project evidence. Before a blocking inquiry, it states the question, scope, objective, effort limit, and needed evidence. These are standing responsibilities under [Plan](AGENTS.md#1-plan--define-the-next-increment); the requester need not prescribe them for each task. Consequential unresolved intent or constraints still require requester involvement.

If the parser splits the field, the observation can complete that investigation while disproving its prediction. An implementation required to preserve the field remains incomplete if it splits it. Revising a prediction changes neither requirements nor acceptance conditions.

If the experiment cannot produce the needed evidence before its limit, the investigation stops incomplete. Obtaining the needed evidence also ends the blocking inquiry; contrary results do not authorize attempts merely to make the prediction true. A successful sample supports only the conclusion justified by that sample. The [Study rules](AGENTS.md#3-study--assess-completion-and-learning) apply this separation to implementation, investigation, and documentation.

### When each method applies

This map explains the methods' connections. Their operational definitions and conditions remain in the linked contract sections.

| Method or convention | Contribution and boundary |
| --- | --- |
| [PDSA](AGENTS.md#workflow-overview) | Organizes every work type proportionally. Repetition of the cycle grants no additional authority. |
| [EARS](AGENTS.md#13-express-new-or-revised-system-requirements-with-ears) | Makes new or revised in-scope system requirements explicit; they guide implementation and validation. |
| [Simple Design and engineering techniques](AGENTS.md#2-do--perform-the-authorized-work) | Guide code and design choices using current requirements and the techniques' benefit/cost conditions. |
| [Given/When/Then](AGENTS.md#31-use-unit-tests-and-other-evidence) | A SHOULD default for understandable unit tests, with no prescribed labels or framework. It does not replace broader validation. |
| [Diátaxis](AGENTS.md#24-write-guides-and-supporting-documentation) | Shapes in-scope guides around reader needs; new guides need an explicitly requested or agreed purpose. |
| [ADRs](AGENTS.md#41-record-significant-decisions-and-technical-debt) | Preserve significant lasting choices in scope and their reasons; routine local choices normally need none. |
| [arc42](AGENTS.md#42-maintain-architectural-knowledge-with-arc42) | Carries architectural knowledge into later decisions, with applicable known content and visible unknowns. |
| [DRY](AGENTS.md#52-maintain-canonical-knowledge-and-consistent-artifacts) | Maintains canonical knowledge across code and documentation throughout the cycle. |
| [Continuation record](AGENTS.md#43-retain-context-for-unfinished-work) | Carries unfinished task context that permanent artifacts do not capture. Maintenance depends on that need; startup lookup is required. |

Listing a method creates no separate deliverable for every increment. Existing requirements, architecture, decisions, code, and tests inform Plan; affected artifacts stay current during work; Study checks completion; Act uses and retains findings before the next authorized step.

## Collaboration and effort control

The requester supplies the objective, permission, and relevant constraints; the agent organizes authorized work into small, complete increments. This allocation makes decomposition, validation, effort assessment, and appropriate consultation part of the contract's default behavior. A requester can select a particular step or impose extra review points without needing to manage the process for ordinary use.

The [four effort factors](AGENTS.md#51-scope-effort-and-requester-interaction)—scope, uncertainty, consequence, and reversibility—make the concerns behind a decision explicit without a numeric score or task-classification scheme. Scope includes affected behavior, artifacts, dependencies, and system boundaries. Few changed lines can affect many callers or an irreversible migration. A narrow, understood, low-impact, reversible change can instead use brief inspection, action, validation, and reporting.

Planning depth follows the next decision at the current abstraction level. Architecture analysis may examine boundaries and alternatives deeply without specifying every future API or function. Detail follows uncertainty, risk, reversibility, and proximity to execution. Explicit authorization can cover broader analysis; provisional later detail does not prohibit it.

The material-growth checkpoint makes an unexpected increase in effort available for requester review before the additional work proceeds, even when the desired outcome and broad authorization remain unchanged. It therefore controls something a scope boundary alone cannot. Ordinary increments can continue under existing authorization, subject to applicable checkpoints. The [usage examples](README-powerusers.md#when-the-work-grows-unexpectedly) distinguish expected local work from material growth.

The [requirement keywords](AGENTS.md#terms-and-requirement-keywords) distinguish obligations, strong defaults with justified exceptions, and permissions. This matters particularly for requester involvement: required escalation of unresolved intent or permission, agreement on consequential constraints, and recommended consultation about unsettled choices have different strengths. A SHOULD exception cannot bypass a MUST checkpoint; a routine local choice cannot invent a consequential constraint.

Completeness applies within an increment's scope. An increment can deliver evidence, enabling infrastructure, or migration groundwork as well as functionality. When a stage cannot stand alone, the explanation of what remains usable or testable and how to undo it makes the commitment assessable. Reversibility and recovery reduce the cost of a mistaken approach; they do not authorize destructive effects.

Reporting exposes results, assumptions, uncertainty, and recovery options, but cannot retroactively authorize a consequential choice. Native tool permissions and approval controls govern enforceable boundaries. The contract's reporting defaults support review without requiring a full-file dump or diff for every task; [the usage guide](README-powerusers.md#read-the-result) explains what a requester sees at a handoff.

## Engineering methods: quality within a small increment

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

Relevant available checks against acceptance conditions are mandatory before claiming completion. Appropriate tests for behavior changes, defect repairs, and clarified edge cases are a SHOULD default with justified exceptions. Validation covers affected behavior, risk, and hard operational limits for every work type; passing tests cannot replace a missing requirement or necessary check. Failed, unavailable, and omitted checks stay visible.

[Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html) makes a unit test's starting conditions, action, and expected result understandable. For a quoted field containing a comma, those parts are the sample, the parser call, and the intact-field assertion. The contract requires neither literal labels nor a testing framework, and prohibits weakening tests merely to pass.

### Focused techniques and how they work together

These techniques support Simple Design when their benefits justify their costs. Their selection grants no authority for unrelated restructuring or new dependencies.

| Technique and account | Design reason and boundary |
| --- | --- |
| Gross's [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/) | Make behavior understandable near its implementation while balancing separate responsibilities and canonical ownership. A clear invocation can expose intent without inlining everything or adopting htmx. |
| The [Law of Demeter](https://www2.ccs.neu.edu/research/demeter/demeter-method/LawOfDemeter/general-formulation.html) | Reduce knowledge of other components' internals through direct collaborators. Clarity and interface costs matter; there is no blanket ban on chained access or requirement for an aspect-oriented solution. |
| Fowler's [Value Object](https://martinfowler.com/bliki/ValueObject.html) | Express domain meaning and validation through values equal by contents, with practical immutability. Preserve required identity and state changes; neither wrapping every primitive nor adopting Domain-Driven Design is required. |
| The [inheritance extract](https://media.pragprog.com/titles/tpp20/inheritance-tax.pdf) | Prefer interfaces, protocols, and composition when they reduce coupling; use polymorphism for complex conditional dispatch when clearer. Keep abstractions justified and allow suitable inheritance. |
| Fowler's [dependency injection](https://martinfowler.com/articles/injection.html), “Separating Configuration from Use” | Separate assembly from use when this improves separation, clarity, or testing. Supplying a clock as a parameter can suffice. Configuration normally stays at assembly, initialization, or external-system boundaries; no container or new dependency is required. |

## Documentation as input and output

Requirements describe intended behavior, accepted decisions retain choices and reasons, architecture describes boundaries and guarantees, and schemas and package metadata declare their own constraints. Code, tests, and execution provide evidence of implemented behavior. Their roles explain why executable behavior does not automatically overrule a requirement. Conflicts need visible evidence, inference, and an identified governing source; personal or external instructions cannot supply project facts.

Documentation informs Plan and changes as work establishes facts and choices. Producing a guide or updating affected documentation is Do work. Study checks its acceptance conditions; Act uses the findings and retains relevant learning. Architecture and ADRs appear under Act for that retention role, while their records are read and maintained whenever needed.

Updates follow affected canonical owners and direct references. Coverage expectations do not authorize a repository-wide audit, backfill, or reorganization. Documentation-only work uses the same increment, validation, review, and conditional continuation rules as other work. Current-system descriptions follow reality, with proposals and unfinished work clearly identified.

### arc42: shared architectural context as the project grows

[arc42](https://arc42.org/overview/) supplies twelve architectural topics spanning goals and constraints, structure and operation, crosscutting concepts, decisions, quality, risks, and terminology. Shared content expectations aim to reduce reinvention and relearning across repositories. They give an empty project questions to answer as evidence develops, without requiring the entire design to be settled first.

The contract covers applicable topics with known facts and visible material unknowns. Empty headings and invented details do not establish coverage. [Incremental documentation](https://faq.arc42.org/questions/B-14/) and [appropriate depth](https://faq.arc42.org/questions/B-4/) support keeping content useful as the system develops. [Quality scenarios](https://docs.arc42.org/section-10/) make goals assessable: “imports should be fast” still needs an agreed workload and measure.

One architecture document is the initial SHOULD default, using the existing documentation folder or repository-root `docs/`. This keeps early information together. An adequate existing arrangement can remain, and coherent parts can separate as reading and maintenance warrant it. Layout is flexible; known coverage gaps still require proposals and warrant improvements within authorized scope, subject to requester limits or deferral. Summaries link to canonical requirements and ADRs, while implementation detail stays near code and tests.

### EARS: making required behavior explicit

[EARS (Easy Approach to Requirements Syntax)](https://alistairmavin.com/ears/) gives natural-language requirements consistent condition-and-response patterns. For example:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

The pattern exposes behavior to implement and check. It cannot decide whether to reject one row or the whole file, or define a row's line number for a particular format. Those remain project decisions. EARS applies to new or revised in-scope system requirements; unchanged requirements need no automatic conversion. The [contract](AGENTS.md#13-express-new-or-revised-system-requirements-with-ears) owns the five patterns and combined state-before-event form. Rationale belongs with significant choices; EARS adds no mandatory rationale field to each requirement.

### ADRs: preserving the reasons for lasting choices

[Architecture Decision Records](https://docs.arc42.org/section-9/) retain reasons that code alone may not reveal. A streaming-parser decision can connect a memory constraint and experiment evidence with consequences for error reporting. Later work can assess that reasoning against new evidence instead of reconstructing it.

Significant lasting choices in scope need an ADR in or linked from arc42's decision section; routine local choices normally need none. Status distinguishes proposed, accepted, and superseded decisions. Material history, influential failed approaches, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links explain the basis and applicability of those project decisions. This does not require exploring every possible alternative or backfilling decisions outside authorized scope.

### Recording technical debt

Debt describes a current compromise that increases future maintenance cost or risk, assessed against accepted requirements and trade-offs. A deferred feature, rejected option, or different preference alone does not establish debt. Intended behavior is not automatically a defect, although an accepted compromise can carry debt.

Permission to record evidenced, task-relevant debt makes concerns visible without requiring separate authorization for each entry. Chat notification—what, why, where, and uncertainty—makes the classification assessable. Records in [arc42's risks and debt section](https://docs.arc42.org/section-11/) track in-scope changes and fixes. Recording grants no permission to fix the issue or override an accepted decision; contract-file protection still applies.

### Diátaxis: choosing content for the reader's need

[Diátaxis](https://diataxis.fr/) separates four needs: tutorials teach through guided practice, how-to guides help complete a task, reference supplies precise facts and interfaces, and explanation develops understanding. The [introductory guide](https://diataxis.fr/start-here/) explains these forms. A guide for correcting rejected rows can focus on the task and link to maintained format rules and background rationale.

New guides require an explicitly requested or agreed need; simple or low-level software may need none. Affected existing guides stay current. [Applying Diátaxis incrementally](https://diataxis.fr/how-to-use-diataxis/) avoids empty categories and a four-document requirement. Comments, docstrings, and generated API documentation instead follow suitable language and tool conventions, with requester choices recommended when a new convention materially affects public documentation or maintenance.

## A connected example: developing an import tool

Suppose the agreed input format has a header and quoted fields. A requirements increment can settle malformed-row handling using EARS and record known system boundaries in the architecture description. A separate parser investigation can answer the quoted-comma question above. These are possible increments, each with its own complete result; they are not a prescribed sequence.

For an implementation increment, suppose the requester authorizes rejecting mismatched rows, reporting their line numbers, and continuing with valid rows using the existing parser:

| Phase | Application |
| --- | --- |
| Plan | Read the relevant requirements, code, tests, architecture, and decisions. Establish acceptance checks for rejection, diagnostics, and continued processing. Predict that validation at the existing row boundary will suffice. |
| Do | Add scoped validation using Simple Design and project conventions. Write relevant tests and update affected documentation at its owner. Record an ADR only if a significant lasting choice arises. |
| Study | Run relevant available checks, including a valid row after a rejection. Assess acceptance separately from whether the predicted local approach sufficed; disclose failures or missing checks. |
| Act | Report results, paths, evidence, and unfinished work. Retain material findings and otherwise missing continuation context. Distinguish this completed behavior from the larger import objective, then finish, seek required direction, or plan another authorized increment. |

A necessary shared-parser redesign triggers the material-growth checkpoint when discovered; it does not wait for Act. A requested how-to guide may be another increment, using Diátaxis and linking to the maintained format rules. No example step automatically requires an ADR, guide, work record, or new approval solely because an increment ends.

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

## Continuation design

The root path `.agent-continuation-context.md` makes unfinished context discoverable without an index link or broad search. Its descriptive name and leading dot reduce accidental collisions; “continuation context” describes information useful throughout unfinished work. The name and format are local conventions applying retained learning and canonical ownership.

Required startup lookup finds retained context even when a new session does not know it exists. Conditional creation and maintenance avoid an extra artifact when permanent records already suffice. The once-per-session notice exposes context without requiring a reply or authorizing resumption. Reconciliation matters because abrupt interruption can leave the record stale.

Current reality belongs in code, checks, and current-system documents; lasting rationale belongs with decisions; the work record holds otherwise missing task intent and direction. This separation prevents proposals from masquerading as implementation or creating competing permanent facts. The [usage guide](README-powerusers.md#continue-unfinished-work) explains how this lifecycle works when resuming a task, including collisions, stale records, and retirement.

## Why the bridges differ

Both bridges apply the same local contract through their tool's instruction mechanisms. [CLAUDE.md](CLAUDE.md) uses `@AGENTS.md`, Claude Code's [native import syntax](https://code.claude.com/docs/en/memory#import-additional-files), to include the referenced content. The single line can therefore perform its loading role.

[Copilot support](https://docs.github.com/en/copilot/reference/custom-instructions-support) varies by interface. A Markdown link identifies a file but is not a universal import mechanism. The supplied bridge explicitly requests reading the contract before planning, editing, refactoring, reviewing, validating, or updating documentation; application within the actual hierarchy and permissions; and access-failure reporting without a false claim of compliance. Those provisions explain its additional text.

Discovery, inclusion, precedence, and application are distinct. [VS Code's conflict guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#resolve-conflicting-instructions), its [instruction settings](https://code.visualstudio.com/docs/agents/reference/ai-settings#custom-instructions-settings), and [GitHub.com's precedence guidance](https://docs.github.com/en/copilot/concepts/prompting/response-customization#precedence-of-custom-instructions) describe different aspects. File order or a link alone cannot establish all four. The [adoption checks](README-powerusers.md#check-adoption) and [recorded evidence dates](README-powerusers.md#evidence-dates) qualify the integration guidance; exact settings and support depend on the provider's documentation and the actual environment.

The Copilot title and header identify the associated release and upstream origin. Its release date and source URL match `AGENTS.md`. Metadata adds no policy authority, and the adopted local contract remains canonical. Permitting provenance does not require a header on the one-line Claude import. Minimality preserves each bridge's loading and application role.

## Keeping the contract portable

The entire `AGENTS.md` is assessed against two distinct criteria:

- **Hard constraint: fewer than 24,000 UTF-8 bytes.** Count the whole file. The project budget sits below [Codex's default 32 KiB combined instruction limit](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance); other loaded instructions consume that limit too.
- **Advisory review signal: fewer than 200 lines.** This applies Anthropic's [recommendation for `CLAUDE.md`](https://code.claude.com/docs/en/memory#write-effective-instructions) as a prompt to review unnecessary content, repetition, or density in `AGENTS.md`. Reaching the count is not a compliance failure and does not itself require cuts.

Check the actual file after edits. Automated counts can help; automated enforcement is not required. Line count depends on wrapping and Markdown layout, so preserve useful spacing and headings. Neither criterion establishes clarity, adherence, or compatibility. They concern standing instruction size, not the reasoning or work allowed for a task. Vendor changes can prompt a review but do not automatically change the project policy.

The byte constraint and line-count signal concern the contract itself. Operational meaning remains self-contained in `AGENTS.md`; moving necessary conditions out of it would undermine portability even if the resulting file were smaller.

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

## Assessing design changes

The design can be assessed at two levels: whether the contract works as a self-contained set of instructions, and whether a proposed change preserves or deliberately alters the meaning of its clauses. A standalone reading tests the first; comparison of strength, trigger, scope, exception, and meaning tests the second. The detailed patterns, fields, and obligations remain in `AGENTS.md`.

| Scenario | Design distinction to assess |
| --- | --- |
| Ordinary authorized change | The agent selects a small increment and establishes its checks. Completion grants no additional permission or automatic documentation artifact; another increment can proceed under existing authorization unless a checkpoint requires a pause. |
| Investigation contradicts its prediction | An evidenced answer can complete the investigation while disproving the prediction; unmet implementation behavior remains incomplete. |
| Investigation reaches its effort limit | Inquiry stops with missing evidence and uncertainty visible; a stopping condition does not establish completion. |
| Documentation-only work | Applicable methods and validation apply without requiring code or unit tests for their own sake. |
| Unexpected material growth in any phase | Direction is required before the additional work, even within broad authorization. |
| Resuming recorded work | Current evidence and authority are reconciled; discovery and notification supply no permission to resume. |

The relevant dependencies span [engineering](AGENTS.md#2-do--perform-the-authorized-work), [validation](AGENTS.md#3-study--assess-completion-and-learning), [knowledge retention](AGENTS.md#4-act--use-the-findings-and-determine-what-follows), and [shared policy](AGENTS.md#5-rules-throughout-the-cycle). Method conditions, appropriate-test recommendations, required validation, documentation scope, and requester authority all contribute to the resulting behavior.

Changes to protected instruction files follow [their authorization rule](AGENTS.md#53-instructions-contract-files-and-external-actions), including file-specific recommendations and necessary companion edits. Substantive policy changes need explicit identification. An explanation or review checklist cannot substitute for the actual clauses, and a shorter contract does not by itself establish equivalent agent behavior or token savings.
