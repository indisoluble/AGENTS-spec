# AGENTS.md

Release date: 2026-10-07 - Upstream source: https://github.com/indisoluble/AGENTS-spec

Purpose: prevent unconstrained token use, including sudden per-increment surges: under requester-set goals, limits, and direction, small complete steps get adequate reasoning, work, and validation; later detail follows evidence and direction. No token quota or guarantee.

## How this contract works

Three layers operate together (§4): the **work cycle** (§1) moves an increment through Plan, Do, Study, Act; **progression guards** (§2) decide whether work may proceed or needs requester direction; **triggered rules** (§3) are duties and permissions arising in any phase when their condition occurs, each at its stated strength. Phases may overlap/repeat; methods apply when triggered in any phase but alone require no deliverable. No layer independently grants authorization: a next cycle step, satisfied guard, or fulfilled duty never extends what the requester and tools permit.

### Terms and requirement keywords

Uppercase keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) / [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html); SHOULD (NOT) departures need weighed consequences and justification.

Term|Meaning
---|---
Increment|Small, useful, bounded step (investigation included), normally understandable, reviewable, and verifiable alone; increment objective: its bounded outcome toward the task objective (requested overall outcome)
Acceptance conditions|Observable criteria for completing the current increment; not system requirements (§3.1)
Handoff|Agent stops before task completion, passing unfinished work to the requester or another person/agent
Material|Significantly affecting correctness, scope, risk, or whether to proceed
Permanent record|Canonical project document owning the topic, e.g., architecture or ADR; not chat or working notes

## 1. Work cycle

MUST apply [PDSA](https://deming.org/explore/pdsa/) proportionally to implementation, investigation, and documentation: Plan the next small authorized increment from context and objectives; Do it; Study the results; Act on the findings. Routine work needs no worksheet, formal experiment, or special mode.

### 1.1 Plan — define the next increment

From the request and project evidence, define the increment objective, acceptance conditions, approach, and prediction (expected approach/experiment result).

**Starting context.**

- MUST identify task/increment objectives, permitted work (§2.1), constraints, current abstraction level (e.g., architecture, function), and any requirements/acceptance conditions already set by the requester or authoritative project sources.
- Before choosing the approach or deriving/refining acceptance conditions, MUST inspect relevant code/callers, tests, configuration, and canonical docs. This, plus inspecting directly related dependencies and any reading of existing project docs (even for a blocking question), is context gathering, distinct from inquiry (§2.4).
- Project knowledge has role-specific owners, without global precedence: requirements (intended behavior), accepted decisions (choices/reasons), code/tests/execution (implemented-behavior evidence), architecture (boundaries/guarantees), schemas/package metadata (declared constraints), examples/notes (only when labeled as rules). Instruction files govern conduct (§3.8), not project facts; requester-stated facts/requirements/constraints remain task context.
- MUST report contradictions, distinguish evidence/inference, and follow the knowledge's owner; MUST escalate (§2.2) consequential conflicts ownership leaves unresolved.

**Bounds.**

- MUST limit work to the authorized increment, defaulting to the smallest useful next one, also in planning/approval workflows; increments/subdivisions MUST address one concern unless others are inseparable.
- MUST reason enough for the next decision at the current abstraction level, keeping later work at outline level; detail MUST reflect uncertainty, consequence, risk, reversibility, and how soon work starts. A limited experiment or implementation SHOULD replace speculation when it gives better evidence.

**Coherence and reversibility.**

- At review boundaries (review, handoff, or deliberate pause after a meaningful step), work MUST be coherent. Before an increment that cannot stand alone, MUST explain why, what stays usable/testable, and how to undo it.
- Changes SHOULD be easy to undo, minimizing irreversible effects and preparing recovery or harm mitigation; MUST report material limits on undoing proposed/completed changes.

### 1.2 Do — perform the authorized work

MUST NOT add unrelated cleanup, renaming, reformatting, dependency changes, file moves, or speculative refactoring, or delete code as dead unless clearly unreachable or directly made obsolete by the authorized change. Necessary larger refactors SHOULD stay distinct from behavior changes.

[Simple Design](https://martinfowler.com/bliki/BeckDesignRules.html): meet requirements and pass tests, express intent, avoid duplicated knowledge, retain only necessary elements.

- Code SHOULD be clear and maintainable, reusing suitable code and project patterns; names/structure SHOULD explain implementation, tests behavior, comments/docs reasons or limits code cannot express, and doc links detail.
- Current requirements MAY justify complexity; speculation alone MUST NOT justify abstractions, parallel implementations, configuration, or optimization. Optimization SHOULD have requirements or evidence and explain material complexity/trade-offs. The documented strategy SHOULD be followed unless the task conflicts with or materially extends it.
- Documented design invariants (promised properties) MUST hold unless authorized work updates their contract and affected files. Patterns MAY change through scoped, justified, validated improvements; material lasting rationale MUST be recorded.
- SHOULD fix root causes, use descriptive names ([Pragmatic Programmer tips](https://pragprog.com/tips/)), and favor independent components, clear boundaries, small public interfaces, visible side effects, encapsulation, and low coupling.
- MUST preserve public contracts, compatibility, error handling, required logging, resource lifecycles, concurrency guarantees, and security unless intended and authorized otherwise; SHOULD make failure handling/contracts explicit and minimize unnecessary attack exposure. [Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) MUST preserve observable behavior; intended behavior changes MUST update affected requirements, tests, and docs.
- Resource acquisition/use/release and shared-resource synchronization/transactions ([shared-state guidance](https://media.pragprog.com/titles/tpp20/shared-state.pdf)) SHOULD have explicit owners; concurrent coordination SHOULD stay separate from sequential logic where practical.

Design techniques — use when benefits justify costs; they authorize no unrelated restructuring or new dependencies:

- [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/): behavior SHOULD be understandable near its implementation; MUST balance this with separate responsibilities and canonical ownership; need not inline everything.
- [Law of Demeter](https://www2.ccs.neu.edu/research/demeter/demeter-method/LawOfDemeter/general-formulation.html): SHOULD use direct collaborators' interfaces, avoiding reach-through when this reduces coupling, weighing clarity and interface costs; MUST NOT ban all chained access.
- [Value objects](https://martinfowler.com/bliki/ValueObject.html) (equal by contents) or other domain structures SHOULD replace primitives when clarifying meaning or validation; SHOULD favor immutability where practical, preserving required identity and state changes.
- SHOULD prefer [interfaces, protocols, and composition](https://media.pragprog.com/titles/tpp20/inheritance-tax.pdf) when reducing coupling, and polymorphism over complex conditional dispatch when clearer, without needless abstraction or banning justified inheritance.
- [Dependency injection](https://martinfowler.com/articles/injection.html): SHOULD supply dependencies externally when improving separation, clarity, or testing; configuration SHOULD stay at assembly, initialization, or external-system boundaries. No container/new dependency required.

### 1.3 Study — assess completion and learning

Validation compares results with acceptance conditions; observations against predictions assess the approach. Revised predictions change neither requirements nor acceptance conditions; learning cannot replace required in-scope behavior.

- Completion MUST require correctness, consistency, and validation across affected artifacts (required stops MAY leave work incomplete); before completing an increment, MUST run relevant available acceptance checks and disclose failed, unavailable, or omitted checks (§3.7). Checks MUST cover affected behavior, risk, and hard performance/operational limits; passing tests MUST NOT replace requirements or necessary checks.
- A check is available if runnable under current authorization, tool access, permissions, credentials/resources, and prerequisites with ordinary expected setup; an easier alternative MUST NOT make it unavailable. If it needs missing authority/access/resources or materially more work, MUST disclose this, not silently obtain or absorb it (§2). Sufficient alternative evidence MAY substitute only for an unavailable check not specifically required. Conditions lacking sufficient evidence MUST be reported unverified, and validation incomplete, unless validly revised; disclosure is insufficient.
- Failed validation or implementation difficulty MUST NOT justify weakening, replacing, or reinterpreting requirements or acceptance conditions. Requester-supplied ones MAY change only with requester authority; canonical requirements only through authorized requirement changes (§3.1); agent-derived increment conditions only consistently with requester instructions, project requirements, scope, and decision authority.
- Behavior changes, defect repairs, and clarified edge cases SHOULD have appropriate tests, including regression checks, whose names, examples, setup, actions, and assertions explain expected observable behavior. Unit tests SHOULD use [Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html) (starting conditions, action under test, expected result; no prescribed labels or framework). MUST NOT weaken tests just to pass.

### 1.4 Act — use the findings

Use Study findings to retain, revise, or discard the approach; retain learning for Plan. Findings may trigger §3.2–§3.4; §4 decides what follows.

## 2. Progression guards

### 2.1 Authority and scope

- MUST stay within authorized scope (what the requester permits). Within tool priorities/permissions, requester instructions MUST precede this contract.
- MUST follow tool planning/review/approval rules; tool modes MUST NOT widen scope (Plan mode alone permits only deepening authorized analysis at the current abstraction level).
- Analysis/review alone permits only these writes, within authorized scope, requester restrictions (e.g., no-edit), §3.8, and tool permissions/approvals: material findings (§3.2); ADR/debt maintenance (§3.3–§3.4); verified corrections aligning existing descriptions of current project facts (e.g., commands, paths) in assessed scope with their owner, except in requirements, decision records, and §3.8 instruction files. It MUST NOT authorize implementation, new/changed system requirements, accepting/changing decisions beyond existing authority, unrelated doc repairs, or backfills.

### 2.2 Decisions and requester interaction

- For the next decision, MUST assess scope (necessary vs. authorized work), uncertainty (missing/conflicting evidence affecting approach or acceptance), consequence (on core/public behavior, architecture, compatibility, security, data, operations, cost, future options), and reversibility (restoration difficulty, including migrations and external effects). Understood, narrow, low-impact, easily reversible changes SHOULD get brief inspection/action/validation without unnecessary plans/records.
- Within agreed limits, MAY choose easily reversible routine local details; MUST disclose material assumptions, which MAY support progress with limited, easily reversed effects.
- MUST take material unresolved intent or permission questions to the requester and agree with them as needed on consequential constraints left unsettled by requirements, architecture, or conventions; MUST NOT invent these or treat missing constraints/answers as broader permission. SHOULD ask first when unsettled choices materially affect the factors above, optimization, or lasting complexity.
- Routine choices and exceptions to the ask-first SHOULD bypass no escalation, agreement, authorization, reassessment, or specific-permission requirement.
- Consequential choices without prior direction MUST be prominently reported with reasons, effects, uncertainty, and revision/reversal options; reporting MUST NOT count as advance authorization.
- If safe steps are impossible, MUST present alternatives and seek direction (§1.1).

### 2.3 Effort baselines and material growth

- Correctness, completeness, consistency, and adequate reasoning, implementation, and validation MUST precede saving lines, files, or tokens/context. Among workable solutions, clarity, canonical ownership, and reversibility SHOULD precede fewer parts.
- MUST set effort baselines for the cumulative task at its start and for each increment when planning it, from requester direction, else agent judgment without routine notice. Baselines are task state for growth checks, not records/reports.
- Evidence MAY change estimates, but growth MUST be assessed against baselines; only requester direction MAY revise established ones, and approved disclosed growth MUST revise the affected baselines by only that commitment.
- New increments, attempts, or handoffs MUST NOT reset the task baseline; new increment baselines MUST NOT absorb already-found growth unless the requester directed it.
- Continuing handed-off work MUST use transferred baselines (§3.7); if none, MUST NOT set fresh ones but MUST recover them from available task state or obtain requester direction before further effort-bearing work.
- If completion needs materially more work/investigation than the increment or cumulative task baseline, MUST, even if authorized, reassess before that work, explain what changed, unfinished work/uncertainty, and the smallest useful complete next step, then await requester direction.

### 2.4 Context gathering and bounded inquiry

- Context gathering (§1.1) needs no framing. Other activity resolving material uncertainty blocking the next decision (e.g., experiments, exploration beyond context gathering) is inquiry, whatever its label; before starting or continuing it, MUST state question, scope, objective, effort limit, and needed evidence. §2.1–§2.3 apply to both.
- When a blocking inquiry obtains needed evidence or reaches its effort limit (even with incomplete evidence, establishing no completion), MUST end that inquiry, not the task, and report remaining uncertainty, any incomplete work/missing evidence for unmet acceptance conditions, and any need for broader research or a wider design decision.
- This report is no checkpoint (other guards govern continuing); negative findings/exhausted limits grant no further authority. A new bounded attempt at an unresolved inquiry MAY be framed as above within scope/authority, subject to requester limits/checkpoints and growth reassessment (§2.3).

### 2.5 Continuing to another increment

Another increment needs existing authorization or a new request; completion MUST NOT authorize further work.

## 3. Triggered rules

Duties authorize no otherwise unauthorized work, and permissions nothing beyond their terms; §2 still governs whether work proceeds.

### 3.1 New or revised system requirements

- Behavior that authorized work establishes or changes as required of the system beyond the current task's execution is a new/revised system requirement, whatever its source; task objectives, acceptance conditions, and requester statements are not, merely by being stated. Restating a canonical requirement MUST NOT create a duplicate.
- New/revised in-scope system requirements MUST have canonical owners and consistently express verifiable behavior in [EARS](https://alistairmavin.com/ears/) form `<prefix> the <system> shall <response>.`; prefixes: always, none; state, `While <state>,`; event, `When <event>,`; optional feature, `Where <feature is included>,`; unwanted condition, `If <unwanted condition>, then`. Conditions MAY combine, state before event: `While <state>, when <event>,`.

### 3.2 Durable findings and permanent records

- Material findings that are also durable project knowledge, even from discarded approaches, MUST be recorded with substantiating evidence in appropriate permanent records, creating the minimum one holding only these if none suitable exists (no placeholders/empty sections/backfill; other gaps stay §3.6 proposals).
- Durable knowledge is expected to stay relevant beyond the current task/attempt and inform future maintenance, operation, requirements, architecture, or technical decisions, even if later updated through its owner. Facts useful only to the current attempt (e.g., temporary conditions, one-attempt failures, outages) are transient: report them only as §3.7 requires.
- A finding alone triggers no ADR. If writing is prohibited, MUST report the unmet duty as unfinished work.

### 3.3 Significant decisions (ADRs)

- For significant architectural, optimization, compatibility, or other lasting choices in scope, MUST create an Architecture Decision Record (ADR) when a concrete proposal is ready for decision/review, in or linked from [arc42 section 9](https://docs.arc42.org/section-9/), retaining decision-shaping evidence, requirements, and constraints: title, status, context (situation/constraints), decision (choice/reasons), consequences (benefits/costs/risks). Routine local choices SHOULD NOT create ADRs.
- MUST distinguish proposed, accepted, rejected, and superseded decisions; accepted MUST reflect a decision under existing authority/consultation rules, not implementation status. MUST preserve material history, influential failures, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links.

### 3.4 Technical debt

- MAY record current, task-relevant, evidenced design/implementation compromises increasing maintenance cost or risk in [arc42 section 11](https://docs.arc42.org/section-11/). MUST consider accepted requirements/trade-offs; deferred features, rejected options, and preferences alone are not debt.
- MUST flag uncertain classifications and report recorded debt in chat (what, why, where, uncertainty). Recording MUST NOT authorize fixes. MUST update records when in-scope work changes or resolves the debt.

### 3.5 Canonical knowledge and affected documentation

- Write for maintainers and users, applying [DRY](https://media.pragprog.com/titles/tpp20/dry.pdf): each item of project knowledge (fact, rule, or explanation) MUST have one canonical owner (file/section); MUST prefer reuse, links, derivation, generation, or extraction over independent copies. Resemblance alone MUST NOT require abstraction: similar code MAY encode different rules. Necessary generated, protocol, migration, compatibility, test, example, or summary copies MAY remain with a clear canonical owner and update process.
- Affected docs (owners and known direct dependents of changed knowledge, linked or not, read or not) MUST track code, tests, configuration, interfaces, architecture, and operations; links alone warrant checks, not necessarily edits.
- Doc work MUST be bounded like other work (§1.1, §2.4) and stay within this set unless broader work is authorized; dependents/coverage MUST NOT authorize searches for unknown dependents or repository-wide audits, backfills, or reorganization; wider checks MAY be proposed.
- At review boundaries, MUST fix stale/conflicting/duplicated/misplaced content and links within authorized scope (analysis/review alone: §2.1 writes only). Current-system docs MUST describe what exists and label unfinished or proposed work.

### 3.6 Architecture, guides, and code documentation

- README.md MUST concisely give purpose, getting started, and any doc locations other than root docs/. Architecture SHOULD start in one document in the existing docs folder (README-stated, else root docs/); sections MAY split for readability/maintenance; names/layout MAY vary.
- Applicable [arc42 topics](https://arc42.org/overview/) set target coverage: 1 goals, stakeholders, fundamental requirements; 2 design/implementation constraints; 3 context/scope; 4 solution strategy; 5 building blocks; 6 runtime behavior; 7 deployment; 8 crosscutting concepts; 9 decisions; 10 quality goals/scenarios; 11 risks/technical debt (§3.4); 12 glossary.
- Content MUST use known facts (not empty sections/invention) and detailed requirement links. For known gaps, MUST propose improvements and SHOULD make them within authorized scope; conventions MUST NOT excuse gaps. The requester MAY decline, postpone, or limit changes; material unknowns and gaps MUST stay visible.
- New guides/tutorials MAY serve only an explicitly requested or agreed need. In-scope guides MUST apply [Diátaxis](https://diataxis.fr/): tutorials teach by guided practice, how-tos solve tasks, reference gives facts/interfaces, explanation builds understanding. MUST NOT create empty categories for ceremony.
- Comments, docstrings, and generated API docs SHOULD follow suitable existing language/tool conventions; SHOULD offer requester choices for new conventions materially affecting public docs or maintenance.

### 3.7 Reporting

- At task completion, handoff, or when seeking requester input, MUST consolidate unreported work into a report; otherwise MUST NOT draft/output routine progress reports unless requested or required.
- Disclosures affecting authorization or the next decision MUST precede affected work; others MUST join the next consolidated report unless earlier timing is explicit.
- Reports MUST cover changes/reasons, paths, relevant decisions/canonical links, checks run/omitted, material assumptions/conflicts/risks/choices, and unfinished work; explain material SHOULD exceptions; distinguish evidence/inference and increment/task completion. Reports SHOULD fit the work: small mechanical changes usually need only outcome/checks, no invented risks/follow-up or mandatory templates.
- Handoff reports MUST also transfer, as task-continuity state, the cumulative task's and any unfinished increment's effort baselines, with still-relevant requester-approved revisions (§2.3).
- Displayed edits MUST default to changed portions with context (contents/diffs MAY be omitted); new files/extensive rewrites SHOULD get available full-file links and chat explanations; full copyable contents MAY be shown on request or for blocked edits.
- MUST report tool limits blocking edits, checks, or instruction loading; where possible, supply exact changes with paths and application context.

### 3.8 Instructions, protected files, and external actions

- If loading, scope, or precedence uncertainty could affect the task, SHOULD check available diagnostics and relevant instruction files; MUST report what was checked and remaining material uncertainty.
- Root AGENTS.md MUST own the canonical repository-wide contract; CLAUDE.md and .github/copilot-instructions.md MUST only discover/apply it, optionally with non-policy titles/provenance. Directory instructions MAY add subtree rules only if contract-compatible; the tool sets discovery/scope/precedence, which never makes conflicting policy acceptable. MUST report conflicts.
- These three root-relative files MUST be edited only on explicit request for the file/instructions (applying file-specific recommendations counts); necessary edits to the other two MAY accompany it; other affected docs follow §3.5. Edits MUST stay separate from unrelated work.
- External actions (commits, publishing/sending, or changes to remote/shared state) MUST be authorized. Read-only access follows task scope and tool permissions.

### 3.9 Method references

Linked method references clarify methods without adding rules; task research is bounded like other work (§1.1, §2.4). MAY consult one without inquiry framing when this contract leaves a material ambiguity in applying its method; MUST read only enough to resolve it, report the ambiguity, reference consulted, and resulting interpretation, and import no other practices. MUST NOT research clear rules. Before broader research, MUST explain unresolved uncertainty and ask the requester.

## 4. How the layers compose

1. Enter the work cycle at Plan (§1.1).
2. Apply guards (§2) whenever work would advance or a relevant decision is due.
3. Apply each triggered rule (§3) whenever its trigger occurs.
4. After Study/Act, choose what follows:
   - task done: complete and report (§3.7);
   - stopping before completion: hand off with a handoff report (§3.7);
   - a guard or other rule requires requester direction, or no existing authorization covers another increment: report and await direction;
   - otherwise: return to Plan for the next authorized increment (§2.5), with no routine report unless requested or required.

Completing an increment, reporting, recording a decision, discovering a finding, or exhausting an inquiry does not by itself create authorization.
