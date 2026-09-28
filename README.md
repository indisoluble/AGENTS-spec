# AGENTS.md Specification

This repository provides a reusable, opinionated [AGENTS.md](AGENTS.md) for developers and teams using coding agents in new or established projects. Its standing rules cover engineering quality, decision-making, documentation, and collaboration, reducing the need to repeat routine instructions in each conversation.

## TL;DR

- **Goal:** prevent unconstrained token consumption through **intentionally small, complete increments**, without cutting short the reasoning, work, or validation needed to complete each one properly.
- **Control:** you set scope and direction. The agent reports results and waits for your guidance before taking on materially more work than expected.
- **Methods:** [PDSA](https://deming.org/explore/pdsa/) organizes the workflow and learning; [Simple Design](https://martinfowler.com/bliki/BeckDesignRules.html) guides implementation; [DRY](https://media.pragprog.com/titles/tpp20/dry.pdf) governs knowledge ownership; [arc42](https://arc42.org/overview/), [EARS](https://alistairmavin.com/ears/), [ADRs](https://docs.arc42.org/section-9/), and [Diátaxis](https://diataxis.fr/) structure architecture, requirements, decisions, and guides.
- **Limits:** token control is best effort, not guaranteed. Hard quotas are deliberately avoided because they could compromise reasoning, completeness, or validation. Instructions also cannot guarantee compliance.

## Reading guide

This README explains adoption and everyday use. Current design rationale and guidance for changing the contract are in [README-maintainers.md](README-maintainers.md).

| Purpose | Suggested reading route |
| --- | --- |
| **Evaluate the contract** | Read [how work proceeds](#what-working-with-the-agent-looks-like), [what adoption means](#what-adopting-it-means), and the [method overview](#why-it-is-built-this-way). |
| **Adopt and use it** | Follow [Get started](#get-started), check [tool compatibility](#tool-compatibility), and use [project alignment](#bringing-an-existing-project-into-alignment) or [continuation guidance](#continuing-unfinished-work) as needed. |
| **Understand or change its design** | Use the maintainer guide's [method rationale](README-maintainers.md#why-it-is-built-this-way), [effort-control rationale](README-maintainers.md#collaboration-and-effort-control), and [review criteria](README-maintainers.md#maintaining-the-design). |

## Get started

1. Read [AGENTS.md](AGENTS.md) to see whether its expectations fit your project.
2. Before replacing existing instruction files, preserve useful project facts found only there, such as build commands or established system constraints, in appropriate project documentation. Check those facts against the current project and identify anything uncertain.
3. Copy the supplied `AGENTS.md` to the repository root: create the file if absent, or replace the previous one if present. The supplied file becomes the repository's collaboration contract.
4. Install the applicable supplied bridges, replacing existing copies: [CLAUDE.md](CLAUDE.md) for Claude Code and [.github/copilot-instructions.md](.github/copilot-instructions.md) for Copilot interfaces that use it.
5. [Check that your tool loads the new contract](#checking-adoption), then try a bounded task and review the result.

Keep the adopted files in version control. Project facts, build commands, and architecture belong in project documentation and code; the generic contract normally needs no customization. Changes to collaboration policy belong in `AGENTS.md`. Keep bridges minimal while preserving necessary loading and application instructions.

Adoption establishes standing expectations for subsequent tasks. Bringing existing documentation and code into alignment is work to request and scope explicitly, as described [below](#bringing-an-existing-project-into-alignment). Installing the contract does not authorize every improvement it describes.

## Small, complete steps toward the objective

An increment is a deliberately small piece of work with a useful result that can normally be understood and reviewed on its own. Limiting its scope is intended to prevent unexpectedly heavy work and token use within a single step. Completeness is relative to that scope: the increment includes the affected artifacts and checks needed for its result. That result may be a change or the evidence needed for a decision; it need not resolve the whole objective.

The **task objective** is the overall requested outcome; the **increment objective** is the bounded outcome sought in the current authorized step toward it. For an import tool, an increment might implement field-count validation or investigate a parser. The [worked definitions and example in the maintainer guide](README-maintainers.md#objectives-acceptance-predictions-and-stopping) distinguish completion criteria, validation, predictions, and investigation limits.

The agent plans the next increment in enough detail to carry it out. Later work stays at outline level, and its details develop in response to results, new evidence, and your direction. This keeps planning and investigation focused on decisions approaching execution while preserving the larger objective.

Small, complete increments are intended to provide frequent opportunities to review progress and cumulative effort and to steer subsequent work. You retain control of goals, constraints, and direction through your instructions and the [review arrangements below](#what-working-with-the-agent-looks-like).

The contract requires reports about work and results, but does not require token totals in each report or provide a token meter. For numerical usage, consult any usage data your tool or provider exposes and check which activity or period it covers before attributing it to an increment. You can ask the agent to include figures it can actually access. Where measurements are unavailable, exact consumption remains unknown; the reported work gives a qualitative view of effort.

Behavior, conditions, and exceptions are defined in [AGENTS.md](AGENTS.md), written for developers and agents.

## What working with the agent looks like

You can start with a larger objective or a specific change. The agent establishes the intended outcome, relevant project context, and what you have authorized. You can specify the next increment; otherwise, the agent defaults to the smallest useful scope within the permitted work, including during planning or approval workflows. It asks about important unresolved questions concerning intended behavior or permission. A straightforward, authorized change can proceed without a separate planning exchange.

Your tool's procedures govern how work is proposed, reviewed, or approved. Entering a tool mode does not itself authorize a larger scope.

The request starts a **Plan–Do–Study–Act (PDSA)** cycle. The same cycle applies to implementation, investigation, and documentation:

| Phase | What the agent does | What this establishes |
| --- | --- | --- |
| **Plan** | Read relevant project context; distinguish the task and increment objectives; establish authorized scope, acceptance conditions, an approach, and a prediction. On resumption, reconcile retained context with current files and instructions. | A small step with enough direction to perform and assess it. Existing requirements, architecture, and decisions constrain the choices. |
| **Do** | Perform the authorized work using the applicable engineering or documentation methods; keep affected artifacts consistent and record significant choices as they arise. | The changed artifacts or investigation evidence to assess. Documentation can itself be the deliverable. |
| **Study** | Validate against acceptance conditions, compare observations with the prediction, and identify uncertainty or missing checks. | Separate conclusions about completion and what was learned about the approach. |
| **Act** | Use findings to retain, revise, or discard the approach within scope; retain relevant learning, report the outcome, and determine what follows. | Finish if the task objective is fulfilled; otherwise pause when direction is needed or return to Plan for another authorized increment. |

These phases can overlap or repeat. Tests may be planned before implementation and written during it; documentation changes as facts and decisions become established. A routine change needs no separate worksheet, phase report, or formal experiment. The phase headings provide a readable route through the work; scope and requester-interaction rules apply throughout. The [applicability guide](README-maintainers.md#when-each-method-applies) shows where individual methods contribute.

Before investigating blocking uncertainty, the agent states the question, scope, investigation objective, effort limit, and needed evidence. It stops when that evidence is obtained or the limit is reached and reports remaining uncertainty. The [acceptance distinctions](README-maintainers.md#objectives-acceptance-predictions-and-stopping) explain when an investigation is complete or must stop incomplete.

When new evidence shows that an increment needs materially more work or investigation than expected, the agent reassesses before taking on that additional work. It briefly explains what changed, what remains unfinished or uncertain, and the smallest useful complete next step, then waits for your direction. This checkpoint applies even when the requested outcome is unchanged and existing authorization covers the work, so you can review the unexpected increase in effort before it proceeds. Dividing the work preserves the correctness, consistency, and validation needed within each increment's scope.

**Recognizing material growth.** Suppose an increment adds field-count validation to an existing importer, including the affected tests and documentation:

| Finding | Effect on the increment | Response |
| --- | --- | --- |
| An untested malformed row falls under the already agreed rule. | One additional regression case fits the expected local work and checks; scope, uncertainty, and risk are essentially unchanged. | Complete the case within the increment and report the result. |
| Rejecting invalid rows requires redesigning a shared parser and investigating compatibility with its other callers. | The same requested behavior now needs substantially more investigation, implementation, and validation than expected. | Pause before that additional work, explain the discovery and unfinished result, propose the smallest useful complete next step, and await your direction, even if existing permission covers it. |

The comparison concerns expected work and investigation, assessed through scope, uncertainty, consequences, and reversibility. These examples illustrate the [reassessment rule](AGENTS.md#51-scope-effort-and-requester-interaction); they add no numerical threshold or exception to other required checkpoints.

At the handoff, the agent explains what was completed, why, where to review it, which checks were run or omitted, and what remains uncertain or unfinished. The result distinguishes completion of this small step from completion of the larger objective. You can assess it and use that evidence to refine subsequent work.

When showing file contents to explain edits, the agent defaults to the changed portions with enough context for review. A report can use a summary, paths, and links without including a diff. For new files and extensive rewrites, the strong default is to provide complete-file links when available, with an explanation in chat. If editing is blocked, the agent provides a focused patch or exact changes when possible, including the paths and context needed to apply them. The contract also permits full copyable contents on request or when needed to make blocked edits usable. These defaults and permissions follow the [reporting rule](AGENTS.md#44-report-the-result-and-choose-the-next-step).

An **increment** bounds the work undertaken at once. A **report** makes its result visible. An **approval checkpoint** reserves a decision for you before work continues. Existing authorization can cover further increments, subject to your review conditions, the reassessment requirement above, and the tool's rules; completing an increment supplies no additional permission. If you want to approve each step separately, make that checkpoint arrangement explicit. Instruction files describe the expected behavior; the tool's own approval controls govern any enforced approvals.

The [rules for requester involvement](AGENTS.md#51-scope-effort-and-requester-interaction) distinguish required involvement, a strong recommendation to consult, and decisions the agent may make within agreed limits:

| Type | Meaning for you |
| --- | --- |
| **Required involvement (`MUST`)** | The agent must bring material unresolved questions about intended behavior or permission to you and agree missing consequential constraints with you as needed. The reassessment checkpoint above requires waiting for your direction before additional work. |
| **Recommended consultation (`SHOULD`)** | For an unsettled consequential choice, asking you first is the strong default. Exceptions need justification after considering the consequences; material departures must be explained. |
| **Permitted routine choices (`MAY`)** | Within agreed limits, the agent may decide local details that are easy to undo, such as private helper names. Material assumptions must still be disclosed. |

An exception to recommended consultation does not waive mandatory involvement, authorization limits, or checkpoints. Reporting an unforeseen consequential choice afterward exposes it for review and does not supply advance authorization.

For an existing project with a reader that already parses input rows, an exchange could look like this:

| Participant | Illustrative request or response |
| --- | --- |
| Requester | “I want to add file imports. Propose one small first step, and wait for approval before implementing it.” |
| Agent | “The existing reader already parses rows. One increment could check each row against the header's field count, report mismatches, and include relevant tests and documentation. Should an invalid row stop the import, or should processing continue?” |
| Requester | “Reject mismatched rows and continue with the others. Complete and check that step, then wait for my review.” |
| Agent | Implements that behavior, reports the changed files, checks, and any remaining uncertainty, and waits for review. Further import capabilities remain outside the authorized increment. |

Here, the requester chose checkpoints before implementation and after its checked result. The [connected example in the maintainer guide](README-maintainers.md#a-connected-example-developing-an-import-tool) explains how the methods support such increments. The operational conditions remain in [Workflow overview](AGENTS.md#workflow-overview).

## What adopting it means

This is an opinionated baseline: it favors clear implementations, limited commitments, explicit responsibility, and established engineering practices. Your instructions take priority within the tool's actual permissions and instruction hierarchy. You remain responsible for assessing and accepting the work.

Adoption can precede complete documentation and includes **architecture documentation aligned with [arc42](README-maintainers.md#arc42-shared-architectural-context-as-the-project-grows)**. The agent must propose improvements for gaps and should implement them within authorized scope; you can defer, limit, or decline them. Large changes proceed in increments.

During a bounded repair, the agent updates affected documentation and records significant choices within scope. A wider documentation audit, conversion of untouched requirements, or reconstruction of past decisions needs corresponding authorization. The coverage expectations remain in place while documentation develops through authorized increments.

Architecture document names and folders remain flexible, and coverage grows with the project. The conventions have distinct roles: [EARS](README-maintainers.md#ears-making-required-behavior-explicit) for wording system requirements, [Architecture Decision Records (ADRs)](README-maintainers.md#adrs-preserving-the-reasons-for-lasting-choices) through arc42 for significant lasting choices, and [Diátaxis](README-maintainers.md#diátaxis-choosing-content-for-the-readers-need) for guides when needed and agreed.

### Bringing an existing project into alignment

After installing the contract, synchronizing the project with its expectations means assessing and, where needed, improving its documentation and code. The new contract supplies the collaboration policy; the project's existing requirements, accepted decisions, and implementation supply the context to assess. This applies even when the project previously had no `AGENTS.md`.

Request the alignment work explicitly and choose a limited area to address first, such as one component or an architectural concern. Begin with its documentation, then use that context to review the code. Work can progress one area at a time, with the rest of the project remaining visible as later work.

1. **Assess the documentation.** Compare the agreed area's documentation with the applicable arc42 coverage and the contract's expectations for requirements, significant decisions, and guides. Identify useful existing content, gaps, contradictions, duplication, and unclear ownership. Keep material unknowns visible; missing explanations require evidence or requester input.
2. **Reorganize, refactor, or improve it.** Make the needed information accurate, accessible, and consistently maintained. An adequate existing arrangement can remain. Requirements being written or revised follow EARS; significant decision records preserve known reasons and history. Describe the system as it exists, with proposed changes clearly identified. New guides address requested or agreed needs. Complete each documentation increment within its scope before taking on further work.
3. **Review the relevant code.** Use the clarified project context and the contract's engineering practices to identify concrete issues, affected behavior, and the reasons a change would help. Apply each practice with its conditions and exceptions. The review determines which improvements are justified; authorization to review alone grants no permission to edit.
4. **Implement agreed improvements.** Carry out authorized changes in small, complete increments, with relevant checks and updates to affected documentation. Report the result, remaining issues, and uncertainty so you can decide subsequent work. Changes intended only as refactoring preserve observable behavior; intended behavior changes need corresponding authorization and updates to requirements and checks.

For example, an initial request could be: “Using `AGENTS.md`, assess the import component's documentation. Identify gaps and propose one small alignment increment. Report your findings and wait before editing.” Later requests can authorize documentation changes, then code review and selected improvements as the evidence develops.

An empty project can develop its documentation and implementation under the contract as useful work establishes them. The detailed conditions are in [Maintain canonical knowledge and consistent artifacts](AGENTS.md#52-maintain-canonical-knowledge-and-consistent-artifacts), [Do — perform the authorized work](AGENTS.md#2-do--perform-the-authorized-work), and the [increment rules](AGENTS.md#12-bound-the-work-and-choose-an-approach).

## Why it is built this way

Mature repositories constrain agents through code, tests, requirements, and decisions. New, empty, or poorly documented projects provide fewer boundaries. The contract combines small increments with established methods to give work structure while project-specific knowledge develops. Those methods guide recurring tasks; they cannot supply missing project facts or replace agreement on consequential constraints.

The methods have distinct roles. Their conditions and exceptions remain in [AGENTS.md](AGENTS.md), and no separate deliverable is required merely because a method is listed.

| Method | What adopting it means |
| --- | --- |
| PDSA | Work follows Plan–Do–Study–Act proportionally: define a small step, perform it, assess completion and learning, then decide what follows within authorization. |
| Simple Design and focused engineering practices | Implement current requirements with clear, necessary structure. Use techniques such as dependency injection or value objects when their benefits justify their costs. |
| DRY | Give shared knowledge a canonical owner across code and documentation, with links or a clear update process for necessary copies. |
| arc42 | Develop architecture documentation around applicable, known topics. Keep unknowns visible and address gaps within authorized scope. Shared content expectations aim to reduce relearning across projects. |
| EARS | Express new or revised in-scope system requirements using consistent condition-and-response patterns. Unchanged requirements need no automatic conversion. |
| Architecture Decision Records | Record significant lasting choices and their reasons within scope; routine local choices normally need no ADR. |
| Diátaxis | Shape guides around learning, completing a task, looking up facts, or understanding reasons. New guides require a requested or agreed need. |

The [maintainer guide](README-maintainers.md#why-it-is-built-this-way) explains the methods, their connections, examples, and source boundaries in detail. Its [connected import-tool example](README-maintainers.md#a-connected-example-developing-an-import-tool) follows several possible increments and one complete implementation cycle.

## Continuing unfinished work

Agents use **`.agent-continuation-context.md` at the repository root** for unfinished work that needs context beyond code, tests, and permanent project documentation. It records the task and current increment objectives, authorization, progress, open questions, and next steps. Agents check the path at session start and read it if present; creating or maintaining one is conditional on the need for extra continuation context. When needed, it stays current at meaningful review boundaries.

Small, complete increments can leave a larger objective unfinished. Continuing that work requires distinguishing three kinds of information:

| Kind of information | Where it is maintained | Example from the import tool |
| --- | --- | --- |
| What exists and what has been checked | Code, tests, check results, and current-state documentation | Field-count validation is implemented; recorded checks establish what was verified. |
| Why a lasting choice was made | Architecture documentation and ADRs | The reasons and trade-offs behind an accepted parser choice. |
| What remains to be done and under what direction | The work record, when additional continuation context is needed | The next proposed capability, unresolved questions, and the extent of existing authorization. |

The work record tells a later session where the task stands. Keeping it at a fixed path makes that context easy to find. A concise record can preserve the agreed direction and gathered evidence without carrying over the full conversation or detailed plans for distant work. The aim is to reduce the effort of reconstructing the task when work resumes.

The convention applies PDSA's concern for retained learning and DRY's concern for ownership. Lasting findings move to their appropriate permanent owners, with links from the work record where needed. The record holds the continuation state that those owners do not capture. A small task that leaves no such context needs no record merely to demonstrate that the method was followed.

On resumption, the agent checks the record against current instructions and project files. An interruption can leave it stale. The comparison distinguishes completed, partial, unverified, and proposed work. A proposed next increment grants no authorization, and discovering the record does not itself authorize resuming the task.

If an existing record has not been acknowledged by the requester in the session, the agent mentions its path and summarizes it once early. The notice requires no reply and is distinct from any actual permission question. This lets a new session start with visible context without turning discovery into automatic resumption or a mandatory approval exchange.

When maintaining a needed record, reuse relevant known earlier context, retire superseded copies, and repair their links. Competing records encountered during ordinary work must be reported. If unrelated content occupies the fixed path, preserve it and seek direction instead of overwriting it or automatically choosing another filename.

When the extra continuation context is no longer needed, remove or archive the record. Preserve lasting findings and unresolved issues with suitable owners, and update affected links. This keeps temporary task context from becoming a competing source of project facts. The practical conditions are in [Establish the starting context](AGENTS.md#11-establish-the-starting-context) and [Retain context for unfinished work](AGENTS.md#43-retain-context-for-unfinished-work).

## Tool compatibility

Loading behavior depends on the product, interface, and settings; consult the provider's current documentation.

| Tool | Instruction loading and setup |
| --- | --- |
| [OpenAI Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Native `AGENTS.md` discovery, subject to override precedence and the combined instruction limit. |
| [Claude Code](https://code.claude.com/docs/en/memory#agentsmd) | The supplied `CLAUDE.md` imports `AGENTS.md`; direct discovery is also available under documented conditions. |
| [GitHub Copilot](https://docs.github.com/en/copilot/reference/custom-instructions-support) | Native `AGENTS.md` support varies by feature. The supplied bridge contains explicit discovery and application instructions. |
| [ChatGPT Projects](https://learn.chatgpt.com/docs/projects) | Project instructions and shared files or connected context; use the product's documented setup. |
| [Claude Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects) | Project instructions and project knowledge; use the product's documented setup. |

The supplied `CLAUDE.md` imports the root contract. The Copilot bridge explicitly asks the tool to read and apply it and report access failures; actual loading depends on the interface and settings. Both keep operating policy in `AGENTS.md`. See [why the bridges differ](README-maintainers.md#why-the-bridges-differ) for the design rationale.

### Checking adoption

Check three things: whether the tool finds the file, includes its instructions in the request, and follows them during a task. A listed file alone does not show that its instructions shaped the result; use a representative task to look for that evidence. [VS Code's verification guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#verify-your-instructions) illustrates checking discovery and application. The appropriate diagnostics depend on the selected interface; a successful check in one interface does not establish compatibility with another.

The contract expresses expected behavior. Actual planning modes, approval controls, permissions, and instruction-loading mechanisms belong to the tool.

[Codex Goal mode](https://learn.chatgpt.com/use-cases/follow-goals) illustrates sustained execution toward a verifiable stopping condition. Use it for an authorized increment with explicit scope and acceptance checks; continued execution does not expand authorization or bypass review conditions.

When uncertainty about instruction loading, scope, or precedence could affect the task, use available diagnostics or ask the agent which repository instruction sources were loaded or consulted and what remains uncertain. Reports should distinguish confirmed loading from files merely inspected.

The recorded documentation-check dates are **2026-09-25** for Codex and Claude Code discovery and size guidance, plus Copilot and VS Code instruction guidance; **2026-09-24** for Projects and Goal mode; and **2026-09-26** for Anthropic's line-count recommendation. These dates identify the evidence supporting the guidance, not conformance-test results. Instruction files guide behavior but cannot guarantee pauses or compliance. Review remains necessary; native planning, approval, and security controls retain their own rules.

## Maintaining the contract

[README-maintainers.md](README-maintainers.md) owns the current design rationale, source assignments, bridge explanations, portability criteria, trade-offs, and review guidance. Read its [maintenance guidance](README-maintainers.md#maintaining-the-design) before proposing changes to the contract or bridges.

The [portability budget](README-maintainers.md#keeping-the-contract-portable) concerns the size of the standing instructions. It does not cap task effort or guarantee compatibility. `AGENTS.md` remains self-contained for ordinary agent work; the maintainer guide adds explanation, not another operating policy.
