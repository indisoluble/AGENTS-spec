# Getting more from AGENTS.md

Once you have followed [Get started](README.md#get-started), this guide explains how the agent organizes work, when it involves you, and how you can tailor the collaboration. It is for anyone who wants fuller explanations and examples; the collaboration guidance assumes no technical background.

The methods appear where they help explain what you experience. Their deeper rationale is in [The design of AGENTS.md](README-maintainers.md), and [AGENTS.md](AGENTS.md) defines the actual rules and exceptions.

| What you want to do | Where to start |
| --- | --- |
| Understand how the agent breaks down a larger goal | [From your goal to an increment](#from-your-goal-to-an-increment) |
| Understand how a step proceeds | [Follow an increment](#follow-an-increment) |
| Understand when the agent asks, pauses, or continues | [Control effort and decisions](#control-effort-and-decisions) |
| Specify a particular step or add review points | [Optional controls you can add](#optional-controls-you-can-add) |
| Assess what was delivered | [Read the result](#read-the-result) |
| Understand implementation and documentation choices | [Understand implementation choices](#understand-implementation-choices) and [Use requirements and documentation](#use-requirements-and-documentation) |
| Adopt the expectations in an existing project | [Bring an existing project into alignment](#bring-an-existing-project-into-alignment) |
| Pick up unfinished work | [Continue unfinished work](#continue-unfinished-work) |
| Check instruction loading | [Tool compatibility](#tool-compatibility) |

## From your goal to an increment

Start with the outcome you want and the constraints that matter to you. The agent is responsible for selecting the next small, useful increment within your authorization and establishing how to assess it. You do not need to decompose the task or specify a stopping condition for every step.

The **task objective** is the overall outcome you want. An **increment** is a deliberately small step toward it, normally useful, understandable, reviewable, and verifiable on its own. Its **increment objective** describes the result sought in that step.

For example:

> Add CSV imports that report invalid rows and continue processing valid rows.

In a project whose existing reader already parses CSV rows, the agent might identify field-count validation as the next useful increment. It reads the relevant requirements and implementation, establishes checks for rejecting mismatched rows and continuing with valid ones, then performs and validates the authorized work. If handling a particular kind of invalid row requires a consequential decision that the request and project evidence do not settle, it asks you.

You supplied the intended behavior. The agent chose a bounded step and its checks. Another increment might investigate whether the reader preserves quoted fields; the agent also frames and bounds that investigation under the contract's rules.

The smallest useful next increment is the default, including in planning or approval workflows. The agent develops enough detail to carry out that step; later work stays at outline level until evidence and your direction justify more detail. Acceptance conditions come from the request and project context, with consequential unresolved constraints brought to you.

Completeness applies within the chosen scope. A code change includes the affected tests, configuration, and documentation needed for its result. An investigation includes the evidence and conclusion needed for the relevant decision. Either can be complete without fulfilling the overall task. Small increments do not justify incomplete implementation or inadequate checking.

A straightforward, authorized correction can proceed without a separate planning exchange. If a step cannot stand alone, the agent must first explain why, what remains usable or testable, and how to undo it. When no safe step is possible, it presents alternatives and seeks direction.

See the contract's [increment rules](AGENTS.md#12-bound-the-work-and-choose-an-approach).

## Follow an increment

The contract applies [PDSA—Plan–Do–Study–Act](https://deming.org/explore/pdsa/) to implementation, investigation, and documentation. Its practical purpose is to connect an approach with observed results and the next decision.

| Phase | What happens | What you can assess |
| --- | --- | --- |
| **Plan** | The agent reads relevant project context, establishes the task and increment objectives, and identifies scope, acceptance conditions, an approach, and a prediction. On resumption, it reconciles retained context with current evidence. | Is this the intended next step, with a meaningful way to check it? |
| **Do** | It performs the authorized work, keeps affected artifacts consistent, and records significant choices as they arise. | Are the changes or investigation focused on the agreed result? |
| **Study** | It validates the result against acceptance conditions, compares observations with the prediction, and identifies missing checks or uncertainty. | What is complete, and what was learned about the approach? |
| **Act** | It uses the findings to retain, revise, or discard the approach within scope, preserves useful learning, and reports the outcome. | Is the task finished, is direction needed, or can another authorized increment begin? |

These phases can overlap or repeat. Tests may be planned before implementation and written during it; documentation changes as facts and decisions become established. Routine work needs no worksheet, formal experiment, or separate report for each phase.

PDSA's Plan phase is part of the reasoning process. A tool's Plan mode has its own proposal and approval procedures. Entering a mode does not expand what you have authorized.

### Completion and learning are different

**Acceptance conditions** are the observable criteria for completing the increment. A **prediction** is the expected result of the chosen approach. **Validation** checks the acceptance conditions; comparing observations with the prediction helps assess the approach.

Suppose you ask whether a parser preserves a quoted field containing a comma. The agent uses the relevant context to define a focused experiment and predicts that the field will remain intact. If the experiment shows the parser splitting that field, an evidenced answer can complete the investigation while disproving the prediction. An implementation required to preserve the field would still be incomplete if it split it. A request to investigate alone does not authorize changing the parser.

Changing a prediction does not change your requirements or acceptance conditions. A successful sample also supports only the conclusion justified by that sample.

Before investigating blocking uncertainty, the agent states the question, scope, objective, effort limit, and evidence needed. Framing this inquiry is its responsibility; you can supply additional limits, and unresolved consequential constraints still require your involvement. It stops the inquiry when it has the evidence or reaches the limit. If the limit arrives first, it reports incomplete work, missing evidence, and uncertainty. A negative finding supplies no permission for more attempts merely to obtain the predicted result.

Completing an increment, reaching an investigation limit, and waiting for requester approval are different events. The agent determines what can follow under existing authorization and the applicable checkpoints; the end of an increment does not automatically require a new instruction from you.

These distinctions come from the [Study rules](AGENTS.md#3-study--assess-completion-and-learning); the [technical explanation](README-maintainers.md#objectives-acceptance-predictions-and-stopping) develops their design rationale.

## Control effort and decisions

The agent applies the contract's effort controls and consultation rules as standing instructions. You can state a goal without repeating directions to work in small increments, validate results, or recognize when further direction is needed.

An increment bounds the work undertaken at once. A report makes its result visible. An approval checkpoint reserves a decision for you before work continues. These serve different purposes: reporting a completed step does not itself create a requirement to wait.

The agent finishes when the task objective is fulfilled. Otherwise, it can proceed to another increment under existing authorization, or seek direction when needed. Completing an increment supplies no additional permission and does not remove permission already granted. Your conditions, the contract's checkpoints, and the tool's rules still apply. Your instructions take priority within the tool's actual hierarchy and permissions.

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

You can tailor the collaboration by selecting a particular increment, adding an investigation limit, or reserving an extra decision for yourself. These are optional controls on top of the agent's standing responsibilities.

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
