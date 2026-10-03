# AGENTS.md

Release date: 2026-09-24 - Upstream source: https://github.com/indisoluble/AGENTS-spec

This contract aims to prevent unconstrained token consumption, including sudden heavy use within an increment, through small, complete steps toward the task objective. The requester sets goals, limits, and direction. Each step gets adequate reasoning, work, and validation; later detail follows evidence and requester direction. Effort control carries no token quota or guarantee.

## Terms and requirement keywords

Uppercase keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) / [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html).

Term / keyword|Meaning
---|---
MUST / MUST NOT|Required / prohibited
SHOULD / SHOULD NOT|Strong recommendation to do / avoid; exceptions require weighing consequences and justifying departure
MAY|Allowed, not required
Task objective|Overall requested outcome
Increment|Intentionally small, useful, bounded step, including investigation, normally understandable, reviewable, and verifiable on its own
Increment objective|Bounded outcome sought by the current authorized increment toward the task objective
Acceptance conditions / validation|Observable criteria for fulfilling the increment objective; validation checks results against them
Prediction|Expected result of an approach or experiment, compared with observations to assess the approach
Investigation effort limit|Limit requiring inquiry to stop even with incomplete evidence; reaching it alone does not establish completion
Scope|Extent of work. Authorized scope is what the requester permits
Current abstraction level|Level of discussion, e.g., architecture or a function
Review boundary|Review, handoff, or deliberate pause after a meaningful step
Material|Significantly affecting correctness, scope, risk, or whether to proceed
Canonical owner|File/section owning a fact, rule, or explanation

## Workflow overview

**Start with the request.** MUST apply [PDSA](https://deming.org/explore/pdsa/) proportionally to implementation, investigation, and documentation: **Plan** the next small increment from context, objectives, and authorization; **Do** it; **Study** results; **Act** to finish, seek direction, or plan another authorized increment. On resumption, start with §1.1.

Routine work needs no worksheet, formal experiment, or special mode. [§5](#5-rules-throughout-the-cycle) applies throughout.

## 1. Plan — define the next increment

Use the request, project state, requirements, architecture, and decisions to define the increment objective, acceptance conditions, approach, and prediction. For requester input, apply [§5.1](#51-scope-effort-and-requester-interaction).

### 1.1 Establish the starting context

A **work record** at repository-root `.agent-continuation-context.md` supports resuming unfinished work in a new conversation without prior chat.

- At session start, MUST check for the record and report competing records encountered. If present, MUST read it and, unless acknowledged by the requester this session, give its path and summary once early in chat. This notice MUST NOT require a reply or authorize resumption.
- MUST identify task/increment objectives, permitted work, constraints, current abstraction level, and acceptance conditions. Analysis/review alone MUST NOT authorize edits.
- Before choosing approach/acceptance conditions, MUST inspect relevant code/callers, tests, configuration, and canonical docs. Requirements: intent; accepted decisions: choices/reasons; code/tests/execution: behavior; architecture: boundaries/guarantees; schemas/package metadata: constraints. Examples/notes govern only when labeled as rules. Personal/global/external instructions MUST NOT count as project facts.
- MUST report contradictions, distinguish evidence/inference, and explain the source to follow.
- On resumption, MUST compare the record with files/checks/instructions; distinguish completed/partial/unverified/proposed work; report material differences/missing context.

### 1.2 Bound the work and choose an approach

- MUST limit work to the authorized increment (§5.1), defaulting to the smallest useful next increment even in planning or approval workflows.
- Every increment, including subdivisions, MUST be complete within scope: correct, consistent, and validated across affected code, tests, configuration, and documents. It MUST address one concern unless others are inseparable; changes SHOULD be easy to undo.
- MUST reason enough for the next decision at the current abstraction level, keeping later work at outline level. Detail MUST reflect uncertainty, consequence, risk, reversibility, and how soon work starts.
- A limited experiment or implementation SHOULD replace speculation when it gives better evidence.
- Before investigating blocking uncertainty, MUST state the question, scope, objective, effort limit, and evidence needed for the next decision. Apply §5.1 stopping rules.
- At review boundaries, work MUST be coherent. Before an increment that cannot stand alone, MUST explain why, what stays usable or testable, and how to undo it.
- SHOULD minimize irreversible effects and prepare recovery or harm mitigation. MUST report material limits on undoing proposed/completed changes.

### 1.3 Express new or revised system requirements with EARS

- New/revised in-scope system requirements MUST consistently express verifiable behavior using [EARS (Easy Approach to Requirements Syntax)](https://alistairmavin.com/ears/), with canonical owners. Conditions MAY combine, state before event: `While <state>, when <event>, the <system> shall <response>.`

Applies when|EARS pattern
---|---
Always|`The <system> shall <response>.`
State|`While <state>, the <system> shall <response>.`
Event|`When <event>, the <system> shall <response>.`
Optional feature|`Where <feature is included>, the <system> shall <response>.`
Unwanted condition|`If <unwanted condition>, then the <system> shall <response>.`

Use these requirements to guide Do and assess the result in Study.

## 2. Do — perform the authorized work

Perform the scoped implementation, investigation, or documentation. Documentation may be the main deliverable or support another change. Keep affected artifacts consistent ([§5.2](#52-maintain-canonical-knowledge-and-consistent-artifacts)); record significant choices as they arise ([§4.1](#41-record-significant-decisions-and-technical-debt)).

Before materially larger work, follow the reassessment rule in §5.1.

- MUST NOT add unrelated cleanup, renaming, reformatting, dependency changes, file moves, or speculative refactoring. MUST NOT delete code as dead unless clearly unreachable or directly made obsolete by the authorized change. Necessary larger refactors SHOULD stay distinct from behavior changes.

### 2.1 Implement with Simple Design

[Simple Design](https://martinfowler.com/bliki/BeckDesignRules.html): meet requirements and pass tests, express intent, avoid duplicated knowledge, retain only necessary elements.

- Code SHOULD be clear and maintainable, reusing suitable code and project patterns. Current requirements MAY justify complexity; speculation alone MUST NOT justify abstractions, parallel implementations, configuration, or optimization.
- Documented **design invariants** (promised properties) MUST hold unless authorized work updates their contract and affected files. Patterns MAY change through scoped, justified, validated improvements; material lasting rationale MUST be recorded.
- Optimization SHOULD have requirements or evidence and explain material complexity/trade-offs. The documented strategy SHOULD be followed unless the task conflicts with or materially extends it.
- SHOULD use names/structure to explain implementation, tests to illustrate behavior, comments/documents for reasons or limits code cannot express, and document links for implementation detail.

### 2.2 Preserve component boundaries and behavior

- SHOULD fix root causes, use descriptive names ([Pragmatic Programmer tips](https://pragprog.com/tips/)), and favor independent components, clear boundaries, small public interfaces, visible side effects, encapsulation, and low coupling.
- MUST preserve public contracts, compatibility, error handling, required logging, resource lifecycles, concurrency guarantees, and security unless intended and authorized otherwise. SHOULD make failure handling/contracts explicit and minimize unnecessary attack exposure. [Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) MUST preserve observable behavior. Intended behavior changes MUST update affected requirements, tests, and documents.
- Resource acquisition/use/release and shared-resource synchronization/transactions ([shared-state guidance](https://media.pragprog.com/titles/tpp20/shared-state.pdf)) SHOULD have explicit owners. Concurrent coordination SHOULD stay separate from sequential logic where practical.

### 2.3 Use design techniques when beneficial

These techniques support Simple Design where benefits justify costs, without authorizing unrelated restructuring or new dependencies.

- [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/): behavior SHOULD be understandable near implementation. MUST balance separate responsibilities and canonical ownership; no need to inline everything.
- [Law of Demeter](https://www2.ccs.neu.edu/research/demeter/demeter-method/LawOfDemeter/general-formulation.html): SHOULD use direct collaborators’ interfaces and avoid reach-through when it reduces coupling. Consider clarity and interface costs; MUST NOT ban all chained access.
- [Value objects](https://martinfowler.com/bliki/ValueObject.html) compare equal by contents. They or other domain structures SHOULD replace primitives when clarifying meaning or validation. SHOULD favor immutability where practical, preserving required identity and state changes.
- [Interfaces, protocols, and composition](https://media.pragprog.com/titles/tpp20/inheritance-tax.pdf) combine components and SHOULD be preferred when reducing coupling. Polymorphism SHOULD replace complex conditional dispatch when clearer, without needless abstraction or banning justified inheritance.
- [Dependency injection](https://martinfowler.com/articles/injection.html) supplies dependencies externally to separate configuration from use. SHOULD use it when improving separation, clarity, or testing. Configuration SHOULD stay at assembly, initialization, or external-system boundaries; no container or new dependency is required.

### 2.4 Write guides and supporting documentation

In Do, Diátaxis shapes in-scope guides for readers; DRY (§5.2) governs their knowledge.

- New guides/tutorials MAY serve only an explicitly requested or agreed need. In-scope guides MUST apply [Diátaxis](https://diataxis.fr/): tutorials teach through guided practice; how-tos solve tasks; reference gives facts/interfaces; explanation develops understanding. MUST NOT create empty categories for ceremony.
- Comments, docstrings, and generated API docs SHOULD follow suitable existing language/tool conventions. SHOULD offer requester choices for new conventions materially affecting public docs or maintenance.

## 3. Study — assess completion and learning

Validation checks results against acceptance conditions; observations against predictions assess the approach. Revising predictions changes no requirements or acceptance conditions. Useful learning cannot complete implementation missing required in-scope behavior.

- Before completing an increment, MUST run relevant available checks against acceptance conditions. MUST disclose failed, unavailable, or omitted checks under §4.4.
- MUST cover affected behavior, risk, and hard performance/operational limits. Passing tests MUST NOT replace requirements or necessary checks. Token/context savings MUST NOT justify inadequate reasoning, implementation, or validation.

A parser splitting a quoted comma disproves predicted preservation but can meet an investigation's acceptance conditions requiring an evidenced answer about preservation.

At the investigation effort limit, stop. If acceptance conditions remain unmet, report incomplete work, missing evidence, and uncertainty. A negative finding authorizes no extra attempts to obtain the predicted result; §5.1 still applies.

### 3.1 Use unit tests and other evidence

[Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html): starting conditions (Given), action under test (When), expected result (Then); no prescribed labels or framework.

- Behavior changes, defect repairs, and clarified edge cases SHOULD have appropriate tests, including regression checks. Names, examples, setup, actions, and assertions SHOULD explain expected observable behavior. Unit tests SHOULD use Given/When/Then. MUST NOT weaken tests just to pass.

Tests may be planned in Plan and written in Do; their results join other Study evidence to inform Act.

## 4. Act — use the findings and determine what follows

Use Study findings to retain, revise, or discard the approach within authorized scope. Maintain records in any phase when triggered, retaining learning for Plan.

- Material findings MUST be recorded even for discarded approaches and moved to appropriate permanent records.

### 4.1 Record significant decisions and technical debt

Architecture Decision Records (ADRs) retain significant choices/reasons and relevant PDSA evidence, requirements, and constraints.

- Significant architectural, optimization, compatibility, or other lasting choices in scope MUST have an ADR in or linked from [arc42 section 9](https://docs.arc42.org/section-9/), including title, status, context (situation/constraints), decision (choice/reasons), and consequences (benefits/costs/risks). Routine local choices SHOULD NOT create ADRs.
- MUST distinguish proposed, accepted, and superseded decisions and preserve material history, influential failures, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links.
- **Technical debt.** MAY record current, task-relevant, evidenced design/implementation compromises that increase maintenance cost or risk in [arc42 section 11](https://docs.arc42.org/section-11/). MUST consider accepted requirements/trade-offs; deferred features, rejected options, and preferences alone are not debt.
- MUST flag uncertain classifications and report recorded debt in chat: what, why, where, and uncertainty. Recording MUST NOT authorize fixes; records MUST reflect in-scope changes or fixes.

### 4.2 Maintain architectural knowledge with arc42

arc42 organizes architecture, linking requirements and decisions to inform later Plan phases.

- README.md MUST concisely cover purpose, getting started, and documentation locations. Architecture SHOULD start in one document in the existing docs folder (default: root docs/). Sections MAY split for readability/maintenance; names/layout MAY vary.
- Architecture MUST cover applicable [arc42 topics](https://arc42.org/overview/) below with known facts and links to detailed requirements. Empty sections/invention MUST NOT replace known information; material unknowns MUST stay visible.
- For known arc42 gaps, MUST propose improvements and SHOULD make them within authorized scope. Conventions MUST NOT excuse gaps. The requester MAY decline, postpone, or limit changes; material gaps MUST stay visible.

#|Architectural knowledge
---|---
1|Goals, stakeholders, fundamental requirements
2|Design/implementation constraints
3|External context/scope, boundaries, interactions
4|Solution strategy for goals
5|Static building blocks/responsibilities
6|Runtime behavior/collaboration
7|Deployment: infrastructure/runtime locations
8|Shared crosscutting concepts/rules
9|Significant architecture decisions/reasons
10|Quality requirements: goals/testable scenarios
11|Known risks/technical debt: internal-quality compromises
12|Glossary: shared terminology

### 4.3 Retain context for unfinished work

- When code/tests/permanent docs lack context for unfinished work, MUST create/maintain a concise record sufficient with them to resume without prior chat; MUST update on material changes, at review boundaries, and before planned stops/handoffs.
- MUST retain task/current increment objectives and acceptance conditions, relevant approach/prediction, agreed direction/authorization/constraints, progress/checks, remaining work at the right level, open consequential questions/checkpoints, canonical links, and likely next increment.
- MUST identify relevant project state, partial/uncommitted work, and missing artifacts; retain interrupted inquiries' §1.2 framing, known effort used, and uncertainty. Resumption/recorded next steps MUST NOT themselves grant permission, reset limits, or clear pending checkpoints.
- MUST omit transcripts/detailed distant plans, reuse relevant known earlier context, retire superseded copies, and repair links. MUST preserve unrelated files and seek direction if any occupy the fixed path.
- Once unnecessary, MUST remove/archive the record, repair links, and preserve unresolved issues with appropriate owners.

### 4.4 Report the result and choose the next step

- At task completion, handoff, or when seeking requester input, MUST consolidate unreported work into a report. Otherwise MUST NOT draft/output routine progress reports unless requested or required.
- Reports MUST cover changes/reasons, paths, relevant decisions/canonical links, checks run/omitted, material assumptions/conflicts/risks/choices, and unfinished work; explain material SHOULD exceptions; distinguish evidence/inference and increment/task completion.
- Reports SHOULD fit the work; small mechanical changes usually need only outcome/checks, without invented risks, follow-up, or mandatory templates.
- Displayed edits MUST default to changed portions with context; contents/diffs MAY be omitted. For new files/extensive rewrites, SHOULD link full files when available and explain in chat. MAY show full copyable contents on request or as needed for blocked edits.
- MUST report tool limits blocking edits, checks, or instruction loading; where possible, supply focused patches/exact changes with paths and application context.

Finish when the task objective is met. Otherwise apply §5.1: seek direction or Plan the next authorized increment with current findings and maintained context.

## 5. Rules throughout the cycle

Phases can overlap or repeat; methods apply whenever triggered, including outside their introductory phase. No separate deliverable per method is required; shared and phase-specific rules govern.

### 5.1 Scope, effort, and requester interaction

- MUST stay within authorized scope. Correctness, completeness, consistency, and validation MUST precede saving lines/files/tokens. Among workable solutions, clarity, canonical ownership, and reversibility SHOULD precede fewer parts.

Factor|What to assess
---|---
Scope|Necessary versus authorized work
Uncertainty|Missing/conflicting evidence affecting approach or acceptance
Consequence|Effects on core/public behavior, architecture, compatibility, security, data, operations, cost, future options
Reversibility|Difficulty of restoration, including migrations and external effects

- MUST assess these factors for the next decision. Understood, narrow, low-impact, easily reversible changes SHOULD use brief inspection, action, and validation without unnecessary plans or records.

**Requester interaction (every phase).** Routine choices and SHOULD exceptions ([requirement keywords](#terms-and-requirement-keywords), §4.4) cannot bypass required escalation, agreement, authorization, or reassessment. Specific permissions elsewhere still apply.

Situation|Response
---|---
Another increment is needed|Existing authorization or a new request is needed. Completion MUST NOT authorize further work
Routine local choices within agreed limits|MAY choose easily reversible details. MUST disclose material assumptions; these MAY support progress with limited, easily reversed effects
Material unresolved intent or permission questions|MUST take them to the requester
Requirements, architecture, or conventions leave consequential constraints unsettled|MUST agree them with the requester as needed. MUST NOT invent them or treat missing constraints/answers as broader permission
Unsettled choices materially affect these factors, optimization, or lasting complexity|SHOULD ask first
New evidence shows completion needs materially more work or investigation than expected|MUST reassess before that work, briefly explain what changed, unfinished work/uncertainty, and the smallest useful complete next step, then await requester direction—even if already authorized
A blocking inquiry obtains needed evidence or reaches its effort limit|MUST stop, report remaining uncertainty, and explain any need for broader research or a wider design decision. Reaching the limit does not establish completion (§3)
Safe steps are impossible|MUST present alternatives and seek direction (§1.2)

- Consequential choices without prior direction MUST be prominently reported with reasons, effects, uncertainty, and revision/reversal options. Reporting MUST NOT count as advance authorization.

### 5.2 Maintain canonical knowledge and consistent artifacts

Write for maintainers and users. [DRY (Don't Repeat Yourself)](https://media.pragprog.com/titles/tpp20/dry.pdf) keeps project knowledge consistent through canonical ownership across code and documentation.

- Each item of project knowledge MUST have one canonical owner. MUST prefer reuse, links, derivation, generation, or extraction over independently maintained copies.
- Resemblance alone MUST NOT require abstraction: similar code MAY encode different rules. Necessary generated, protocol, migration, compatibility, test, example, or summary copies MAY remain with a clear source and update process.

- Documentation MUST follow §1.2 and stay within affected canonical files and direct references unless broader work is authorized. Coverage MUST NOT authorize repository-wide audits, backfills, or reorganization.
- Affected documentation MUST track code, tests, configuration, interfaces, architecture, and operations. At review boundaries, MUST fix stale/conflicting/duplicated/misplaced content and direct links.
- Current-system documents MUST describe what exists and label unfinished or proposed work.

### 5.3 Instructions, contract files, and external actions

- **Instruction priority.** Within tool priorities/permissions, requester instructions MUST precede this contract; directory instructions MUST follow tool scope/priority rules. If loading, scope, or precedence uncertainty could affect the task, SHOULD check available diagnostics and relevant instruction files. MUST report checked sources and remaining material uncertainty.
- MUST follow tool planning/review/approval rules. Tool modes MUST NOT authorize wider scope. In tool Plan mode, MAY deepen authorized analysis at the current abstraction level; broader exploration MUST be authorized.

- AGENTS.md MUST be the canonical repository-wide contract; CLAUDE.md and .github/copilot-instructions.md MUST only discover/apply it. Non-policy titles/provenance MAY accompany them.
- A listed file MUST be edited only on explicit request for that file/instructions (applying file-specific recommendations counts); necessary edits to other listed files MAY accompany that request. Edits MUST stay separate from unrelated work.

- External actions, including commits and publishing, MUST be authorized.

### 5.4 Consult linked sources only when needed

Sources clarify methods without adding rules; task research follows §1.2.

MAY consult an unclear rule's source when material to the decision. MUST read only enough to answer and report the ambiguity/source/answer. MUST NOT research clear rules. Before broader research, MUST explain unresolved uncertainty and ask the requester.
