# AGENTS.md

Release date: 2026-10-04 - Upstream source: https://github.com/indisoluble/AGENTS-spec

This contract aims to prevent unconstrained token use, including sudden heavy use per increment. The requester sets goals, limits, and direction. Small, complete steps receive adequate reasoning, work, and validation; later detail follows evidence and requester direction. No token quota or guarantee.

## Terms and requirement keywords

Uppercase keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) / [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html).

Term / keyword|Meaning
---|---
MUST / MUST NOT|Required / prohibited
SHOULD / SHOULD NOT|Strong recommendation to do / avoid; exceptions require weighing consequences and justifying departure
MAY|Allowed, not required
Task objective|Requested overall outcome
Increment|Small, useful, bounded step, including investigation, normally understandable, reviewable, and verifiable on its own
Increment objective|Current authorized increment's bounded outcome toward the task objective
Acceptance conditions / validation|Observable increment completion criteria; validation checks results against them
Prediction|Expected approach/experiment result, compared with observations to assess the approach
Investigation effort limit|Requires inquiry to stop even with incomplete evidence; reaching it does not establish completion
Scope|Extent of work. Authorized scope is what the requester permits
Current abstraction level|Level of discussion, e.g., architecture or a function
Review boundary|Review, handoff, or deliberate pause after a meaningful step
Material|Significantly affecting correctness, scope, risk, or whether to proceed
Canonical owner|File/section owning a fact, rule, or explanation

## Workflow overview

MUST apply [PDSA](https://deming.org/explore/pdsa/) proportionally to implementation, investigation, and documentation: **Plan** the next small authorized increment from context/objectives; **Do** it; **Study** results; **Act** to finish, seek direction, or plan another authorized increment. Resume at §1.1.

Routine work needs no worksheet, formal experiment, or special mode.

## 1. Plan — define the next increment

Define the increment objective, acceptance conditions, approach, and prediction using the request and project evidence (§1.1).

### 1.1 Establish the starting context

The root **work record**, `.agent-continuation-context.md`, holds separate task entries for continuation without prior chat. Startup/resumption means a new conversation, not a pause or compaction within one.

- At startup, MUST check for the record and report competing records encountered. If present, MUST read it and give its path/summary once early in chat unless the requester already acknowledged it this conversation. The notice MUST NOT require a reply or authorize resumption.
- MUST identify task/increment objectives, permitted work, constraints, abstraction level, and acceptance conditions.
- Analysis/review alone permits only §4 findings and §§4.1/4.3 record maintenance, plus verified factual corrections to ordinary docs in assessed scope (§5.3). This MUST NOT authorize implementation or changed requirements/accepted decisions.
- Before choosing approach/acceptance conditions, MUST inspect relevant code/callers, tests, configuration, and canonical docs. Requirements: intent; accepted decisions: choices/reasons; code/tests/execution: behavior; architecture: boundaries/guarantees; schemas/package metadata: constraints. Examples/notes govern only when labeled as rules. Personal/global/external instructions MUST NOT count as project facts.
- MUST report contradictions, distinguish evidence/inference, and explain the source to follow.
- On resumption, MUST compare available task context (including any record) with files/checks/instructions; distinguish completed/partial/unverified/proposed work; report material differences/missing context.

### 1.2 Bound the work and choose an approach

- MUST limit work to the authorized increment (§5.1); default to the smallest useful next increment, including in planning/approval workflows.
- Increments/subdivisions MUST address one concern unless others are inseparable. Completion MUST require correctness, consistency, and validation across affected artifacts; required stops MAY leave work incomplete. Changes SHOULD be easy to undo.
- MUST reason enough for the next decision at the current abstraction level, keeping later work at outline level. Detail MUST reflect uncertainty, consequence, risk, reversibility, and how soon work starts.
- A limited experiment or implementation SHOULD replace speculation when it gives better evidence.
- Routine code/test/configuration inspection and all reading of existing project docs are context gathering. Before other inquiry into material uncertainty blocking the next decision, MUST state question, scope, objective, effort limit, and needed evidence. §5.1 still applies.
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

## 2. Do — perform the authorized work

Keep affected artifacts consistent (§5.2); record significant choices (§4.1).

- MUST NOT add unrelated cleanup, renaming, reformatting, dependency changes, file moves, or speculative refactoring. MUST NOT delete code as dead unless clearly unreachable or directly made obsolete by the authorized change. Necessary larger refactors SHOULD stay distinct from behavior changes.

### 2.1 Implement with Simple Design

[Simple Design](https://martinfowler.com/bliki/BeckDesignRules.html): meet requirements and pass tests, express intent, avoid duplicated knowledge, retain only necessary elements.

- Code SHOULD be clear and maintainable, reusing suitable code and project patterns. Current requirements MAY justify complexity; speculation alone MUST NOT justify abstractions, parallel implementations, configuration, or optimization.
- Documented **design invariants** (promised properties) MUST hold unless authorized work updates their contract and affected files. Patterns MAY change through scoped, justified, validated improvements; material lasting rationale MUST be recorded.
- Optimization SHOULD have requirements or evidence and explain material complexity/trade-offs. The documented strategy SHOULD be followed unless the task conflicts with or materially extends it.
- SHOULD use names/structure to explain implementation, tests to illustrate behavior, comments/docs for reasons or limits code cannot express, and doc links for implementation detail.

### 2.2 Preserve component boundaries and behavior

- SHOULD fix root causes, use descriptive names ([Pragmatic Programmer tips](https://pragprog.com/tips/)), and favor independent components, clear boundaries, small public interfaces, visible side effects, encapsulation, and low coupling.
- MUST preserve public contracts, compatibility, error handling, required logging, resource lifecycles, concurrency guarantees, and security unless intended and authorized otherwise. SHOULD make failure handling/contracts explicit and minimize unnecessary attack exposure. [Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) MUST preserve observable behavior. Intended behavior changes MUST update affected requirements, tests, and docs.
- Resource acquisition/use/release and shared-resource synchronization/transactions ([shared-state guidance](https://media.pragprog.com/titles/tpp20/shared-state.pdf)) SHOULD have explicit owners. Concurrent coordination SHOULD stay separate from sequential logic where practical.

### 2.3 Use design techniques when beneficial

These support Simple Design when benefits justify costs; they authorize no unrelated restructuring or new dependencies.

- [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/): behavior SHOULD be understandable near implementation. MUST balance separate responsibilities and canonical ownership; no need to inline everything.
- [Law of Demeter](https://www2.ccs.neu.edu/research/demeter/demeter-method/LawOfDemeter/general-formulation.html): SHOULD use direct collaborators’ interfaces and avoid reach-through when it reduces coupling. Consider clarity and interface costs; MUST NOT ban all chained access.
- [Value objects](https://martinfowler.com/bliki/ValueObject.html) compare equal by contents. They or other domain structures SHOULD replace primitives when clarifying meaning or validation. SHOULD favor immutability where practical, preserving required identity and state changes.
- [Interfaces, protocols, and composition](https://media.pragprog.com/titles/tpp20/inheritance-tax.pdf) combine components; SHOULD prefer them when reducing coupling. Polymorphism SHOULD replace complex conditional dispatch when clearer, without needless abstraction or banning justified inheritance.
- [Dependency injection](https://martinfowler.com/articles/injection.html): SHOULD supply dependencies externally to separate configuration/use when improving separation, clarity, or testing. Configuration SHOULD stay at assembly, initialization, or external-system boundaries; no container/new dependency required.

### 2.4 Write guides and supporting documentation

- New guides/tutorials MAY serve only an explicitly requested or agreed need. In-scope guides MUST apply [Diátaxis](https://diataxis.fr/): tutorials teach through guided practice; how-tos solve tasks; reference gives facts/interfaces; explanation develops understanding. MUST NOT create empty categories for ceremony.
- Comments, docstrings, and generated API docs SHOULD follow suitable existing language/tool conventions. SHOULD offer requester choices for new conventions materially affecting public docs or maintenance.

## 3. Study — assess completion and learning

Validation compares results with acceptance conditions; observations against predictions assess the approach. Revised predictions change neither requirements nor acceptance conditions. Learning cannot replace required in-scope behavior.

- Before completing an increment, MUST run relevant available acceptance checks. MUST disclose failed, unavailable, or omitted checks under §4.4.
- MAY substitute sufficient alternative evidence only for an unavailable check that is not specifically required. MUST report conditions lacking sufficient evidence as unverified and validation as incomplete unless conditions are validly revised; disclosure is insufficient.
- MUST cover affected behavior, risk, and hard performance/operational limits. Passing tests MUST NOT replace requirements or necessary checks. Token/context savings MUST NOT justify inadequate reasoning, implementation, or validation.

### 3.1 Use unit tests and other evidence

[Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html): starting conditions (Given), action under test (When), expected result (Then); no prescribed labels or framework.

- Behavior changes, defect repairs, and clarified edge cases SHOULD have appropriate tests, including regression checks. Names, examples, setup, actions, and assertions SHOULD explain expected observable behavior. Unit tests SHOULD use Given/When/Then. MUST NOT weaken tests just to pass.

## 4. Act — use the findings and determine what follows

Use Study findings to retain, revise, or discard the approach within authorized scope. Maintain records when triggered, retaining learning for Plan.

- Material findings MUST be recorded even for discarded approaches and moved to appropriate permanent records.

### 4.1 Record significant decisions and technical debt

Architecture Decision Records (ADRs) retain significant choices/reasons, relevant PDSA evidence, requirements, and constraints.

- For significant architectural, optimization, compatibility, or other lasting choices in scope, MUST create an ADR when a concrete proposal is ready for decision/review, in or linked from [arc42 section 9](https://docs.arc42.org/section-9/): title, status, context (situation/constraints), decision (choice/reasons), consequences (benefits/costs/risks). Routine local choices SHOULD NOT create ADRs.
- MUST distinguish proposed, accepted, rejected, and superseded decisions. Accepted MUST reflect a decision under existing authority/consultation rules, not implementation status. MUST preserve material history, influential failures, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links.
- **Technical debt.** MAY record current, task-relevant, evidenced design/implementation compromises increasing maintenance cost or risk in [arc42 section 11](https://docs.arc42.org/section-11/). MUST consider accepted requirements/trade-offs; deferred features, rejected options, and preferences alone are not debt.
- MUST flag uncertain classifications and report recorded debt in chat: what, why, where, and uncertainty. Recording MUST NOT authorize fixes. MUST update records when in-scope work changes or resolves the debt.

### 4.2 Maintain architectural knowledge with arc42

- README.md MUST concisely give purpose, getting started, and doc locations. Architecture SHOULD start in one document in the existing docs folder (default: root docs/). Sections MAY split for readability/maintenance; names/layout MAY vary.
- Architecture MUST cover applicable [arc42 topics](https://arc42.org/overview/) below with known facts and detailed requirement links. Empty sections/invention MUST NOT replace known information; material unknowns MUST stay visible.
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
11|Known risks; technical debt as defined in §4.1
12|Glossary: shared terminology

### 4.3 Retain context for unfinished work

- When code/tests/permanent docs lack unfinished task context, MUST create/maintain its concise, identified entry in the root record, sufficient with them to resume without prior chat. MUST update on material changes, review boundaries, and before planned stops/handoffs.
- MUST retain task/current increment objectives and acceptance conditions, relevant approach and prediction, agreed direction/authorization/constraints, effort baselines and known cumulative effort/uncertainty, progress/checks, remaining work at the right level, open consequential questions/checkpoints, canonical links, and likely next increment.
- MUST identify relevant project state, partial/uncommitted work, and missing artifacts; retain interrupted inquiries' §1.2 framing, known effort used, and uncertainty. Resumption/recorded next steps MUST NOT grant permission, reset limits, or clear pending checkpoints.
- MUST omit transcripts/detailed distant plans, reuse relevant known earlier context, retire superseded copies, and repair links. MUST preserve unrelated files and seek direction if any occupy the fixed path.
- Updates/retirement MUST preserve other tasks' needed context. MUST remove/archive unneeded entries, repair links, and preserve unresolved issues with appropriate owners; remove/archive the file only when no entry is needed.

### 4.4 Report the result and choose the next step

- At task completion, handoff, or when seeking requester input, MUST consolidate unreported work into a report. Otherwise MUST NOT draft/output routine progress reports unless requested or required.
- Disclosures affecting authorization or the next decision MUST precede affected work; others MUST join the next consolidated report unless earlier timing is explicit.
- Reports MUST cover changes/reasons, paths, relevant decisions/canonical links, checks run/omitted, material assumptions/conflicts/risks/choices, and unfinished work; explain material SHOULD exceptions; distinguish evidence/inference and increment/task completion.
- Reports SHOULD fit the work; small mechanical changes usually need only outcome/checks, without invented risks/follow-up or mandatory templates.
- Displayed edits MUST default to changed portions with context; contents/diffs MAY be omitted. New files/extensive rewrites SHOULD have available full-file links and chat explanations. MAY show full copyable contents on request or for blocked edits.
- MUST report tool limits blocking edits, checks, or instruction loading; where possible, supply focused patches/exact changes with paths and application context.

Finish when the task objective is met; otherwise seek direction or Plan the next authorized increment under §5.1 using findings/context.

## 5. Rules throughout the cycle

Phases may overlap/repeat; methods apply whenever triggered, regardless of phase. Methods alone require no deliverable; triggered rules govern.

### 5.1 Scope, effort, and requester interaction

- MUST stay within authorized scope. Correctness, completeness, consistency, and validation MUST precede saving lines/files/tokens. Among workable solutions, clarity, canonical ownership, and reversibility SHOULD precede fewer parts.

Factor|What to assess
---|---
Scope|Necessary versus authorized work
Uncertainty|Missing/conflicting evidence affecting approach or acceptance
Consequence|Effects on core/public behavior, architecture, compatibility, security, data, operations, cost, future options
Reversibility|Difficulty of restoration, including migrations and external effects

- MUST assess these factors for the next decision. Understood, narrow, low-impact, easily reversible changes SHOULD use brief inspection/action/validation without unnecessary plans/records.
- MUST set effort baselines for the increment and cumulative task from requester direction, otherwise agent judgment without routine notice. Only requester direction may revise the task baseline; increments, attempts, and conversations MUST NOT reset it.

**Requester interaction (every phase).** Routine choices and SHOULD exceptions (§4.4) cannot bypass escalation, agreement, authorization, or reassessment requirements. Specific permissions still apply.

Situation|Response
---|---
Another increment is needed|Existing authorization or a new request is needed. Completion MUST NOT authorize further work
Routine local choices within agreed limits|MAY choose easily reversible details. MUST disclose material assumptions; these MAY support progress with limited, easily reversed effects
Material unresolved intent or permission questions|MUST take them to the requester
Requirements, architecture, or conventions leave consequential constraints unsettled|MUST agree them with the requester as needed; MUST NOT invent them or treat missing constraints/answers as broader permission
Unsettled choices materially affect these factors, optimization, or lasting complexity|SHOULD ask first
Completion needs materially more work/investigation than expected for the increment or cumulative task|MUST reassess before that work, explain what changed, unfinished work/uncertainty, and the smallest useful complete next step, then await requester direction—even if authorized
A blocking inquiry obtains needed evidence or reaches its effort limit|MUST stop and report then: remaining uncertainty and, if acceptance conditions are unmet, incomplete work/missing evidence; explain any need for broader research or a wider design decision. Negative findings/exhausted limits grant no further authority
Another attempt at an unresolved inquiry|MAY frame (§1.2) a new bounded attempt within scope/authority, subject to requester limits/checkpoints and growth reassessment
Safe steps are impossible|MUST present alternatives and seek direction (§1.2)

- Consequential choices without prior direction MUST be prominently reported with reasons, effects, uncertainty, and revision/reversal options. Reporting MUST NOT count as advance authorization.

### 5.2 Maintain canonical knowledge and consistent artifacts

Write for maintainers and users, applying [DRY (Don't Repeat Yourself)](https://media.pragprog.com/titles/tpp20/dry.pdf):

- Each item of project knowledge MUST have one canonical owner. MUST prefer reuse, links, derivation, generation, or extraction over independent copies.
- Resemblance alone MUST NOT require abstraction: similar code MAY encode different rules. Necessary generated, protocol, migration, compatibility, test, example, or summary copies MAY remain with a clear source and update process.

- Docs MUST follow §1.2 and stay within affected canonical files/direct references unless broader work is authorized. Coverage MUST NOT authorize repository-wide audits, backfills, or reorganization.
- Affected docs MUST track code, tests, configuration, interfaces, architecture, and operations. At review boundaries, MUST fix stale/conflicting/duplicated/misplaced content and direct links.
- Current-system docs MUST describe what exists and label unfinished or proposed work.

### 5.3 Instructions, contract files, and external actions

- **Instruction priority.** Within tool priorities/permissions, requester instructions MUST precede this contract; directory instructions MUST follow tool scope/priority. If loading, scope, or precedence uncertainty could affect the task, SHOULD check available diagnostics and relevant instruction files. MUST report checked sources and remaining material uncertainty.
- MUST follow tool planning/review/approval rules. Tool modes MUST NOT authorize wider scope. In tool Plan mode, MAY deepen authorized analysis at the current abstraction level; broader exploration MUST be authorized.

- Root AGENTS.md MUST own the canonical repository-wide contract; CLAUDE.md and .github/copilot-instructions.md MUST only discover/apply it. Non-policy titles/provenance MAY accompany them. Directory instructions MAY add compatible subtree rules under tool scope/priority.
- These three root-relative files MUST be edited only on explicit request for the file/instructions (applying file-specific recommendations counts); necessary edits to the others MAY accompany it. Edits MUST stay separate from unrelated work.

- External actions—commits, publishing/sending, or changes to remote/shared state—MUST be authorized. Read-only access follows task scope and tool permissions.

### 5.4 Consult linked sources only when needed

Sources clarify methods without adding rules; task research follows §1.2.

MAY consult an unclear rule's source when material to the decision. MUST read only enough to answer and report the ambiguity/source/answer. MUST NOT research clear rules. Before broader research, MUST explain unresolved uncertainty and ask the requester.
