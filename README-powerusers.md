# Getting more from AGENTS.md

Once you have followed [Get started](README.md#get-started), this guide explains how the agent organizes work, when it involves you, and how you can tailor the collaboration. It is for anyone who wants fuller explanations and examples; the collaboration guidance assumes no technical background.

The methods appear where they help explain what you experience. Their deeper rationale is in [The design of AGENTS.md](README-maintainers.md), and [AGENTS.md](AGENTS.md) defines the actual rules and exceptions.

| What you want to do | Where to start |
| --- | --- |
| Understand how work proceeds from your request | [PDSA starts with your request](#pdsa-starts-with-your-request) |
| Understand how the agent selects the next step | [Plan the next useful increment](#plan-the-next-useful-increment) |
| See how findings affect the broader approach | [Use results to shape what follows](#use-results-to-shape-what-follows) |
| Understand when the agent asks, pauses, or continues | [Control effort and decisions](#control-effort-and-decisions) |
| Understand what bounds a blocking investigation | [How investigation limits work](#how-investigation-limits-work) |
| Specify a particular step or add review points | [Optional controls you can add](#optional-controls-you-can-add) |
| Assess what was delivered | [Read the result](#read-the-result) |
| Understand implementation and documentation choices | [Understand implementation choices](#understand-implementation-choices) and [Use requirements and documentation](#use-requirements-and-documentation) |
| Adopt the expectations in an existing project | [Bring an existing project into alignment](#bring-an-existing-project-into-alignment) |
| Pick up unfinished work | [Continue unfinished work](#continue-unfinished-work) |
| Check instruction loading | [Tool compatibility](#tool-compatibility) |

## PDSA starts with your request

Start with the outcome you want and the constraints that matter to you. The contract applies [PDSA—Plan–Do–Study–Act](https://deming.org/explore/pdsa/) from that request onward, for implementation, investigation, and documentation. Understanding the objective, considering the approach, and selecting the next useful step all belong to Plan.

The **task objective** is the overall outcome you want. An **increment** is a deliberately small step toward it, normally useful, understandable, reviewable, and verifiable on its own. Its **increment objective** describes the result sought in that step.

| Phase | What happens | What you can assess |
| --- | --- | --- |
| **Plan** | The agent understands the overall objective and permitted work, reads relevant context, and selects the next useful increment. It defines that step's objective, scope, acceptance conditions, approach, and prediction, keeping later work at outline level. On resumption, it reconciles retained context with current evidence. | Does this step address the objective and current knowledge, with a meaningful way to assess it? |
| **Do** | It performs the authorized work, keeps affected artifacts consistent, and records significant choices as they arise. | Are the changes or investigation focused on the agreed result? |
| **Study** | It validates the result against acceptance conditions, compares observations with the prediction, and identifies what the evidence establishes about the approach, including uncertainty or missing checks. | What is complete, and what does the result imply for further work? |
| **Act** | It uses the findings to retain, revise, or discard the approach within scope, preserves useful learning, and reports the outcome. It finishes, seeks direction, or returns to Plan with the new knowledge. | Is the task fulfilled? If work remains, how should the approach develop and what direction is needed? |

The overall objective guides successive cycles. The agent develops the next step in detail and revisits the outline of later work as evidence changes. A complete sequence of increments does not need to be settled beforehand.

These phases can overlap or repeat. Tests may be planned before implementation and written during it; documentation changes as facts and decisions become established. Routine work needs no worksheet, formal experiment, or separate report for each phase.

PDSA's Plan phase is part of the reasoning process. A tool's Plan mode has its own proposal and approval procedures. Entering a mode does not expand what you have authorized.

### Plan the next useful increment

Within Plan, the agent is responsible for selecting the smallest useful next increment within your authorization and establishing how to assess it. This default also applies in planning or approval workflows. You do not need to decompose the task or specify a stopping condition for every step.

The agent reasons enough for the next decision at the current level of discussion, whether that concerns architecture, an investigation, a document, or a local change. Acceptance conditions come from the request and project context, with consequential unresolved intent or constraints brought to you. Later detail develops in response to findings and your direction.

An increment can produce evidence for a decision as well as an implementation. Completeness applies within its scope: a code change includes affected tests, configuration, and documentation needed for its result; an investigation includes the evidence and conclusion needed for the relevant decision. Either can be complete while the overall task remains unfinished.

A straightforward, authorized correction can proceed without a separate planning exchange. If a step cannot stand alone, the agent must first explain why, what remains usable or testable, and how to undo it. When no safe step is possible, it presents alternatives and seeks direction. Small increments do not justify incomplete implementation or inadequate checking.

See the contract's [workflow overview](AGENTS.md#workflow-overview) and [increment rules](AGENTS.md#12-bound-the-work-and-choose-an-approach).

### Use results to shape what follows

For example, you might ask:

> Add CSV imports that report invalid rows and continue processing valid rows.

Suppose the project has an existing reader, and the required input format includes quoted fields. While considering the approach in Plan, the agent finds that the reader's handling of quoted commas is uncertain. That uncertainty can make a focused investigation the next useful increment:

| Phase | Example |
| --- | --- |
| **Plan** | Determine whether the reader preserves a quoted comma in one sample, to assess its suitability for the import approach. Scope: the existing reader and test setup. State the effort limit before starting: one execution attempt and inspection of any output. Evidence needed: the parsed fields for that sample. Predict that the quoted field remains intact. |
| **Do** | Run the stated experiment and capture the resulting fields. |
| **Study** | Observe that the reader splits the quoted field. Check whether the evidence answers the investigation question and recognize that the prediction was disproved. |
| **Act** | Revise the assumption that the reader already supports the required input, retain the finding, and report its effect on the approach to imports. Determine whether direction is needed before returning to Plan. |

The next Plan now addresses the parser limitation in light of current evidence and authorization. Had the evidence supported the original assumption, a useful next increment might instead have been row validation. The chosen next step emerges from what was learned.

If the discovery means completion needs materially more work or investigation than expected, the agent must explain that increase and wait for direction before the additional work. That checkpoint applies as soon as its condition arises, in any phase. Updating the approach supplies no permission to change your objective or expand the work.

### Completion and learning are different

**Acceptance conditions** are the observable criteria for completing the increment. A **prediction** is the expected result of the chosen approach. **Validation** checks the acceptance conditions; comparing observations with the prediction helps assess the approach.

In the quoted-field example above, an evidenced answer can complete the investigation while disproving its prediction. An implementation required to preserve the field would still be incomplete if it split it. If you had requested only the investigation, that request alone would not authorize changing the parser.

Changing a prediction does not change your requirements or acceptance conditions. A successful sample also supports only the conclusion justified by that sample.

A negative finding supplies no permission for more attempts merely to obtain the predicted result. An inquiry also has a stated effort limit that can require stopping while its acceptance conditions remain unmet; see [how investigation limits work](#how-investigation-limits-work).

Completing an increment, reaching an investigation limit, and waiting for requester approval are different events. The agent determines what can follow under existing authorization and the applicable checkpoints; the end of an increment does not automatically require a new instruction from you.

These distinctions come from the [Study rules](AGENTS.md#3-study--assess-completion-and-learning); the [technical explanation](README-maintainers.md#objectives-acceptance-predictions-and-stopping) develops their design rationale.

## Control effort and decisions

The agent applies the contract's effort controls and consultation rules as standing instructions. You can state a goal without repeating directions to work in small increments, validate results, or recognize when further direction is needed.

An increment bounds the work undertaken at once. A report makes its result visible. An approval checkpoint reserves a decision for you before work continues. These serve different purposes: reporting a completed step does not itself create a requirement to wait.

The agent finishes when the task objective is fulfilled. Otherwise, it can proceed to another increment under existing authorization, or seek direction when needed. Completing an increment supplies no additional permission and does not remove permission already granted. Your conditions, the contract's checkpoints, and the tool's rules still apply. Your instructions take priority within the tool's actual hierarchy and permissions.

### How investigation limits work

An **investigation effort limit** caps the effort spent answering a particular question that blocks the next decision. Before investigating that blocking uncertainty, the agent **must establish and state the question, scope, objective, effort limit, and evidence needed**, as required by [AGENTS.md §1.2](AGENTS.md#12-bound-the-work-and-choose-an-approach). This is part of its standing responsibility for framing the inquiry; you do not need to request it or supply the limit yourself.

The contract prescribes no universal value, measurement unit, or formula for choosing the limit. A limit could bound specified checks or experiment attempts, or use a time allowance where elapsed time can be tracked. These are possible forms, not required defaults. The limit must be stated for the particular inquiry; there is no hidden value to assume if the agent omits it.

In the [quoted-field example](#use-results-to-shape-what-follows), the stated allowance is one execution attempt using the existing test setup and inspection of any output. That is an illustrative bound, not a one-attempt rule for all investigations:

| What happens | What it means |
| --- | --- |
| The output answers whether the sample's quoted field was preserved. | The agent stops the inquiry with an evidenced answer, including the limits of that evidence. A result that disproves the prediction can still complete the investigation. |
| The attempt fails to produce the needed output. | The allowance is exhausted while the acceptance conditions remain unmet. The agent stops and reports the incomplete investigation, missing evidence, and remaining uncertainty. Repairing the test environment or running further experiments would be additional work. |

The bound applies to that inquiry. Reaching it alone establishes neither completion of the investigation nor completion of the overall task. Under the [Study and stopping rules](AGENTS.md#3-study--assess-completion-and-learning), needed evidence and the effort limit are distinct reasons to stop; any remaining uncertainty stays visible.

You can supply a tighter limit or an extra approval checkpoint. The requirement to state a limit does not itself require your approval of every limit. The agent must still involve you over consequential unresolved constraints, explain any need for broader research or a wider design decision, and apply the [interaction rules](AGENTS.md#51-scope-effort-and-requester-interaction). In particular, unexpected material growth requires direction before the additional work proceeds.

### When the work grows unexpectedly

When new evidence shows that completion needs materially more work or investigation than expected, the agent must reassess before taking on that additional effort. It explains what changed, what remains unfinished or uncertain, and the smallest useful complete next step, then waits for your direction. This applies even when the requested outcome is unchanged and broad authorization already covers the work.

For an increment adding field-count validation to an importer:

| Finding | Expected response |
| --- | --- |
| An additional malformed row falls under the agreed validation rule and fits the expected local checks. | Complete the regression case within the increment and report it. |
| Rejecting invalid rows requires redesigning a shared parser and investigating compatibility with other callers. | Explain the larger effort and unfinished result, propose a next step, and wait for direction. |

The assessment considers scope, uncertainty, consequences, and reversibility. There is no numerical threshold based on changed lines or token count. Subdividing the work must preserve correctness, consistency, and validation within each increment.

### When the agent asks you

The contract uses the requirement keywords defined by [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html). They distinguish obligations, strong defaults, and permissions:

| Situation | Meaning for you |
| --- | --- |
| Material unresolved questions about intended behavior or permission | The agent **must** bring them to you. It must agree missing consequential constraints with you as needed. |
| An unsettled consequential choice | Asking first is a **strong recommendation**. Departures need justification after considering the consequences; material departures must be explained. |
| Routine local choices within agreed limits | The agent **may** choose easily reversible details, such as private helper names. Material assumptions remain visible. |
| Unexpected material growth | The agent **must** wait for direction before the additional work, as described above. |

An exception to recommended consultation cannot bypass mandatory involvement or authorization limits. Missing answers do not grant broader permission. Reporting a consequential choice afterward makes it reviewable but does not supply advance authorization.

### Optional controls you can add

You can tailor the collaboration by selecting a particular increment, specifying your own investigation limit, or reserving an extra decision for yourself. These are optional requester controls; establishing and stating a limit before a blocking investigation is already mandatory for the agent.

For example, if you want to review a proposal before implementation and check each result before work continues:

> Propose the first increment and wait for my approval before editing. After implementing and checking it, wait for my review before starting another increment.

This request adds specific checkpoints. Without that instruction, the agent still chooses small increments, validates them, reports results, and observes every required checkpoint; it can also continue under existing authorization when no checkpoint requires a pause.

You may instead identify the exact behavior to address next, or place a tighter limit on an investigation. The agent remains responsible for a coherent approach and adequate validation within the resulting scope. The precise interaction conditions are in [AGENTS.md §5.1](AGENTS.md#51-scope-effort-and-requester-interaction).

### Understanding token use

Small, complete increments give you opportunities to review cumulative effort and steer subsequent work. They are a best-effort control mechanism; total consumption may still be substantial.

The contract has no token meter, hard quota, or required token total in every report. For figures, use data your tool or provider exposes and check which activity or period it covers before attributing it to an increment. You can ask the agent to include usage figures it can actually access. Without measurements, exact consumption remains unknown; the reported work provides a qualitative view.

Correctness, completeness, consistency, and validation take priority over saving tokens.

## Read the result

At a handoff, expect an explanation of what was completed, why, where to review it, what was checked, and what remains uncertain or unfinished. Material assumptions, decisions, conflicts, risks, and justified departures from strong recommendations should be visible. The report distinguishes completion of the increment from completion of the overall task.

Before claiming completion, the agent must run relevant available checks against acceptance conditions. It must disclose failed, unavailable, or omitted checks. Passing tests cannot stand in for an unimplemented requirement or a necessary performance or operational check.

[Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html) helps make unit tests understandable: the starting situation, the action, and the expected result. Appropriate tests are a strong default for behavior changes, defect repairs, and clarified edge cases; the contract does not require a particular framework or literal labels. Tests must not be weakened merely to pass.

When edits are displayed, changed portions with enough context are the default. A report may instead use a summary, paths, and links without a diff. For new files or extensive rewrites, complete-file links with an explanation are the strong default where available. You can request full copyable contents.

If a tool blocks edits, the agent reports the limitation and, where possible, supplies a focused patch or exact changes with paths and application context. Full contents may be appropriate when needed to make blocked edits usable.

Small mechanical changes normally need only a concise outcome and checks. No template or invented follow-up is required. See the [reporting rules](AGENTS.md#44-report-the-result-and-choose-the-next-step).

## Understand implementation choices

The contract is opinionated about engineering: it favors understandable implementations, clear responsibilities, and complexity justified by current requirements.

[Simple Design](https://martinfowler.com/bliki/BeckDesignRules.html) provides the basic direction: meet requirements and pass tests, express intent, avoid duplicated knowledge, and retain only necessary elements. This allows complexity needed for an agreed performance limit or other requirement; an imagined future feature alone does not justify it.

For you, that means a request to support one input format should produce a complete solution for that format. It need not create a framework for formats you have not requested. Suitable existing code and patterns can be reused, and unrelated cleanup remains outside scope.

Techniques such as dependency injection, value objects, and composition are used when their benefits justify their costs. They do not automatically require new libraries or restructuring. Public behavior, compatibility, error handling, resource lifecycles, concurrency guarantees, and security must be preserved unless changing them is intended and authorized.

If you ask for [refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html), observable behavior must remain the same. If you want different behavior, state that outcome so the affected requirements, tests, and documentation can change with it.

The [engineering rules](AGENTS.md#2-do--perform-the-authorized-work) contain the conditions; the [technical guide](README-maintainers.md#engineering-methods-quality-within-a-small-increment) explains the methods and their trade-offs.

## Use requirements and documentation

Documentation supplies context for decisions and develops as work establishes facts. During a bounded repair, affected documentation stays current and significant in-scope choices are recorded. A wider audit, conversion of untouched requirements, or reconstruction of past decisions needs corresponding authorization.

The methods have different practical roles:

| Method | What you will see |
| --- | --- |
| [EARS](https://alistairmavin.com/ears/) | New or revised system requirements express verifiable behavior through consistent condition-and-response wording. |
| [arc42](https://arc42.org/overview/) | Architecture documentation covers applicable topics such as goals, boundaries, structure, operation, decisions, quality, and risks. |
| [Architecture Decision Records](https://docs.arc42.org/section-9/) | Significant lasting choices retain their context, reasons, consequences, and status. |
| [DRY](https://media.pragprog.com/titles/tpp20/dry.pdf) | Shared knowledge has one authoritative owner, with links or a clear update process for necessary copies. |
| [Diátaxis](https://diataxis.fr/) | Guides address a reader's particular need: learning, completing a task, finding a fact, or understanding an explanation. |

### Make expected behavior explicit

EARS helps expose decisions that otherwise remain implicit. For example:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

You still need to decide whether processing should continue with later rows. The wording pattern helps express your decision; it cannot make the decision for you. Its scope is new or revised in-scope requirements, so adoption does not automatically convert every existing requirement.

### Let architectural knowledge grow with the project

You can adopt the contract before documentation is complete. Architecture follows applicable arc42 topics using known facts and visible unknowns. Document names and folders remain flexible; the initial default is one architecture document in the existing documentation folder, or `docs/` if there is none.

For known coverage gaps, the agent must propose improvements and should make them within authorized scope. You may defer, limit, or decline them; material gaps remain visible. Empty headings and invented project facts do not establish coverage.

An ADR is appropriate for a significant lasting choice, such as a parser selected to meet a memory constraint. Routine local choices normally need none. Proposed, accepted, and superseded decisions remain distinguishable, with useful history and replacement links.

The agent may record current, task-relevant, evidenced technical debt in the architecture's risks and debt section. It explains what was recorded, why, where, and any uncertainty. A deferred feature, rejected alternative, or different preference alone is not debt; recording debt does not authorize a fix.

### Ask for the guide you need

Diátaxis distinguishes a tutorial that teaches through practice from a how-to that helps someone complete a task, a reference that supplies facts, and an explanation that develops understanding. For example, “Show an operator how to correct rejected rows and retry an import” identifies a practical how-to need.

New guides need an explicitly requested or agreed purpose. Listing these methods does not require four documents, an ADR, or a new guide for every increment. Existing comments, docstrings, and generated API documentation follow suitable language and tool conventions.

DRY helps keep those materials consistent: a guide can explain a retry setting and link to its definition rather than independently maintain the same limit. Similar-looking code may express different rules, so resemblance alone does not require an abstraction.

See the contract's [documentation and knowledge rules](AGENTS.md#52-maintain-canonical-knowledge-and-consistent-artifacts) and the [technical explanation of these methods](README-maintainers.md#documentation-as-input-and-output).

## Bring an existing project into alignment

Installing the files establishes standing expectations for subsequent tasks. Alignment of existing documentation and code is work to request explicitly, even if the project previously had no `AGENTS.md`.

You can request alignment as a broader goal. The agent identifies the next small, useful area to address, such as one component or architectural concern, within that authorization. You may name an area yourself if you have a particular priority. The contract supplies collaboration policy; the project's requirements, accepted decisions, and implementation supply the evidence to assess.

For the authorized work, the agent:

1. **Assesses the documentation.** It compares the area's known content with applicable arc42 coverage and expectations for requirements, decisions, and guides. It identifies useful material, gaps, contradictions, duplication, and unclear ownership, keeping material unknowns visible.
2. **Improves the material when authorized.** It preserves an adequate existing arrangement, expresses revised requirements with EARS, retains known decision reasons and history, and describes the current system accurately. It marks proposed or unfinished changes clearly and completes each increment within scope.
3. **Reviews the relevant code.** It uses the clarified context and engineering practices to identify concrete issues and explain why changes would help. Permission to review alone does not authorize edits.
4. **Implements authorized improvements.** It works in small, complete increments with relevant checks and affected documentation. Refactoring preserves observable behavior; intended behavior changes need corresponding authorization.

For example:

> Assess how this project's documentation aligns with AGENTS.md.

The agent selects a useful first assessment increment, checks the relevant evidence, and reports findings. The request authorizes assessment, so edits need further permission even without an explicit “wait before editing” instruction. A request that already authorizes improvements can cover subsequent implementation increments, subject to the contract's consultation and reassessment rules.

An empty project can develop its documentation and implementation through useful authorized work. Coverage expectations alone do not grant permission for a repository-wide audit or reorganization.

## Continue unfinished work

When unfinished work needs context beyond code, tests, and permanent documentation, agents maintain **`.agent-continuation-context.md` at the repository root**. It retains task and current increment objectives, agreed direction, authorization, constraints, progress and checks, remaining work, open questions, canonical links, and a likely next increment.

| Information | Where to find it |
| --- | --- |
| What exists and what was checked | Code, tests, check results, and current-state documentation |
| Why a lasting choice was made | Architecture documentation and ADRs |
| What remains to be done and under what direction | The continuation record, when additional task context is needed |

The fixed path makes the record discoverable in a later session. Agents check it at session start and read it if present. Unless you have acknowledged it in that session, the agent mentions the path and summarizes it once early. This notice requires no reply and does not itself authorize resuming the task.

On resumption, the agent compares the record with current files, checks, and instructions. An interruption can leave it stale. Completed, partial, unverified, and proposed work must remain distinguishable, and material differences are reported. A proposed next step grants no permission.

When needed, the record stays concise and current at meaningful review boundaries and planned stops. It avoids transcripts and detailed plans for distant work. Relevant earlier context is reused; superseded copies are retired and their links repaired. Competing records encountered during ordinary work are reported. If unrelated content occupies the fixed path, the agent preserves it and seeks direction.

This convention applies PDSA's retained learning and DRY's knowledge ownership. Lasting findings belong in permanent records, with links from continuation context where useful. When the extra context is no longer needed, the work record is removed or archived; lasting findings and unresolved issues retain suitable owners, and affected links are updated.

A task leaving no extra continuation context needs no record merely to demonstrate compliance. The detailed conditions are in [starting context](AGENTS.md#11-establish-the-starting-context) and [context retention](AGENTS.md#43-retain-context-for-unfinished-work).

## Tool compatibility

Use the [basic setup](README.md#get-started) to install the supplied files. Loading behavior depends on the product, interface, and settings. The following guidance carries the [recorded evidence dates below](#evidence-dates); consult the provider's current documentation for your environment.

| Tool | Instruction loading and setup |
| --- | --- |
| [OpenAI Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Native `AGENTS.md` discovery, subject to override precedence and the combined instruction limit. |
| [Claude Code](https://code.claude.com/docs/en/memory#agentsmd) | The supplied `CLAUDE.md` imports `AGENTS.md`; direct discovery is also available under documented conditions. |
| [GitHub Copilot](https://docs.github.com/en/copilot/reference/custom-instructions-support) | Native `AGENTS.md` support varies by feature. The supplied bridge explicitly directs discovery and application. |
| [ChatGPT Projects](https://learn.chatgpt.com/docs/projects) | Project instructions and shared files or connected context; use the product's documented setup. |
| [Claude Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects) | Project instructions and project knowledge; use the product's documented setup. |

The bridges keep operating policy in the local `AGENTS.md`. The Claude file imports it; the Copilot file asks the tool to read and apply it and report access failures. Actual loading remains dependent on the interface and settings. The [technical guide](README-maintainers.md#why-the-bridges-differ) explains the different mechanisms.

### Check adoption

Check whether the tool **finds the file**, **includes its instructions**, and **follows them during a task**. A listed file alone does not show application. Try a representative task and inspect both the result and available diagnostics.

[VS Code's verification guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#verify-your-instructions) illustrates discovery and application checks. A successful check in one interface does not establish compatibility with another.

If loading, scope, or precedence is uncertain, ask which repository instruction sources were loaded or consulted and what remains unconfirmed. Distinguish files merely inspected from confirmed loading. If a source is inaccessible, the agent should report that limitation rather than claim to have followed it.

Planning modes, permissions, approvals, and loading mechanisms belong to the tool. [Codex Goal mode](https://learn.chatgpt.com/use-cases/follow-goals), for example, supports sustained execution toward a verifiable stopping condition. The contract still requires the agent to establish the authorized increment's scope and acceptance checks. Continued execution does not expand authorization or bypass review conditions.

Instruction files cannot guarantee pauses or compliance. Review remains necessary, and native planning, approval, and security controls retain their own rules.

### Evidence dates

The project's recorded documentation-check dates are:

- **2026-09-25:** Codex and Claude Code discovery and size guidance, plus Copilot and VS Code instruction guidance.
- **2026-09-24:** Projects and Goal mode.
- **2026-09-26:** Anthropic's line-count recommendation, discussed in the [portability rationale](README-maintainers.md#keeping-the-contract-portable).

These identify the evidence supporting the guidance; they are not cross-tool conformance-test results.
