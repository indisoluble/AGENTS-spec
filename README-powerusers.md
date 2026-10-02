# Getting more from AGENTS.md

After [installing the files](README.md#get-started), start with an ordinary request for an outcome. The agent is responsible for organizing the work, checking its results, and recognizing when it needs your direction.

The contract's primary aim is to prevent unconstrained token consumption, including unexpectedly heavy use within one step. It uses small, complete increments, develops detail as needed, and preserves the analysis and validation each result requires. This guide explains what that means in practice. No technical background is required to follow the collaboration guidance.

Read the first example for the overall process, then use the sections relevant to your situation:

| Your question | Where to go |
| --- | --- |
| How does the agent turn my request into progress? | [From a request to a result](#from-a-request-to-a-result) |
| When will it ask me, pause, or continue? | [Pauses and decisions](#when-the-agent-pauses-or-continues) |
| What happens when it needs to investigate? | [Blocking investigations](#when-an-investigation-is-needed) |
| How do I assess the work and its effort? | [Results](#assess-the-result) and [token use](#understanding-token-use) |
| Why does it make these code or documentation changes? | [Implementation](#understand-implementation-choices) and [documentation](#use-requirements-and-documentation) |
| How do I adopt this in an existing project or resume work? | [Alignment](#bring-an-existing-project-into-alignment) and [continuation](#continue-unfinished-work) |
| Is my tool loading the instructions? | [Compatibility and adoption checks](#tool-compatibility) |

[AGENTS.md](AGENTS.md) defines the rules and exceptions. The [technical guide](README-maintainers.md) explains their design rationale.

## From a request to a result

You might ask:

> Add CSV imports that report invalid rows and continue processing valid rows.

That is the **task objective**: the overall outcome you want. The agent selects an **increment**, a deliberately small step toward it, normally useful, understandable, reviewable, and verifiable on its own. You do not need to break the task down first.

The agent uses [PDSA—Plan–Do–Study–Act](https://deming.org/explore/pdsa/) from your request onward. Plan defines the next useful step; Do carries it out; Study checks the result and the approach; Act uses those findings to decide what follows.

### Plan: choose the next increment

Choosing the first increment is part of Plan. The agent establishes your objective and permitted work, then inspects the relevant requirements, code, tests, configuration, architecture, and decisions. It needs to understand what is agreed, what already works, what is missing, and whether uncertainty blocks the next decision.

For this example, suppose that inspection finds agreed rules for invalid rows and line numbers, with tests supporting the existing reader's handling of the required CSV format. Field-count validation is missing. The existing row-processing code gives access to the fields, header, and line number, suggesting that this rule can be added locally.

That evidence supports a small, useful increment: reject rows whose field count differs from the header, report them, and continue processing. This addresses one missing behavior and can be checked independently of the remaining invalid-row rules. Its scope includes the affected implementation, tests, and documentation.

The agent defines **acceptance conditions**: reject mismatched rows, report their line numbers, and continue with valid rows, including a valid row after a rejection. Its **prediction** is that validation at the existing row boundary will suffice. The objective, scope, conditions, and approach can be refined together as the context becomes clear; later work stays at outline level.

Different findings can lead to a different first step. If the intended invalid-row behavior is unsettled, the agent brings consequential questions to you and develops the relevant requirements within authorization. If the reader's suitability is uncertain, a [bounded investigation](#when-an-investigation-is-needed) may supply the evidence needed before selecting an implementation step.

### Do, Study, and Act: complete the step and use its findings

- **Do the work.** Add that validation, the relevant tests, and updates to affected documentation. Keep the changes focused on the agreed behavior. Record significant lasting choices if any arise.
- **Study the result.** Run relevant available checks against the acceptance conditions before completing the increment. This is **validation**. Separately, compare the observations with the prediction: did the existing row boundary support the change, or did the approach need revision? Disclose failed, unavailable, or omitted checks under the [reporting rules](#assess-the-result).
- **Act on what was learned.** Retain, revise, or discard the approach within authorization and preserve useful findings. If the task remains unfinished, use the findings to plan the next authorized increment or seek direction when required. A routine transition to another increment needs no progress report.

After field-count validation is complete, the agent can use its findings to select another authorized increment. Suppose that later step adds an agreed check for missing required values. Each increment gets its own validation and assessment, but the agent does not draft or post a routine report between them unless requested or otherwise required.

If you ask for status after those two increments, a consolidated report could look like this, assuming the named files exist and the checks succeeded:

> Added field-count and required-value validation in `src/importer.py`, regression checks in `tests/test_importer.py`, and updated `docs/import-format.md`.
>
> Checks passed for valid rows, mismatched field counts, missing required values, reported line numbers, and a valid row following a rejection. Both changes worked at the existing row boundary, supporting that approach for these rules.
>
> These two validation rules are complete. Other agreed invalid-row rules remain to be implemented toward the CSV-import objective.

This requested report combines work not previously reported and distinguishes it from the whole task. The agent also consolidates results at task completion, a handoff, or when seeking your input. Selection of later work uses the findings as they become available; it does not wait for a chat report or require a complete sequence in advance. If the work reveals unexpectedly greater effort, the [pause rule](#when-the-work-grows-unexpectedly) applies at that discovery.

The phase labels explain the reasoning, not a required report format. Phases can overlap or repeat: tests may be planned before implementation, and documentation changes as facts become established. Routine work needs no worksheet, formal experiment, or separate phase reports. PDSA also applies to investigations and documentation-only work.

PDSA's Plan phase is part of this reasoning process. A tool's Plan mode has its own proposal and approval procedures; entering it grants no additional authorization. On resumption, the agent first [reconciles retained context with current evidence](#continue-unfinished-work).

## Keep work small and complete

A small increment limits how much the agent takes on at once. It still needs enough analysis for the current decision and a complete result within its scope. Correctness, completeness, consistency, and validation take priority over saving tokens.

For example, choosing a storage approach may require careful examination of requirements, alternatives, dependencies, and risks. It need not include designing every future data structure and function. The agent develops the next decision at the current level of discussion—architecture, an investigation, a document, or a local change—and keeps later detail at outline level until needed.

The agent selects the smallest useful next increment within your authorization, including in planning or approval workflows. During Plan, it considers which unmet behavior or blocking question can usefully be addressed next and which dependencies are needed for a complete result. It assesses the [scope, uncertainty, consequences, and reversibility](AGENTS.md#51-scope-effort-and-requester-interaction) of that decision. These criteria guide judgment; the contract prescribes no fixed sequence or ranking formula.

Consequential unresolved intent or constraints come back to you. Selecting and defining the step—its objective, acceptance conditions, approach, and prediction—are standing agent responsibilities, so you need not prescribe a step or stopping condition for every request.

An increment can deliver evidence for a decision as well as an implementation. A code change includes the affected tests, configuration, and documentation needed for its result; an investigation includes the evidence and conclusion needed for its decision. Either can be complete while the overall task remains unfinished.

A straightforward authorized correction can proceed without a separate planning exchange. If a proposed step cannot stand alone, the agent must first explain why, what remains usable or testable, and how to undo it. Material limits on undoing changes stay visible. If no safe step is possible, it presents alternatives and seeks direction.

See the contract's [increment rules](AGENTS.md#12-bound-the-work-and-choose-an-approach).

## When the agent pauses or continues

The agent finishes when the task objective is fulfilled. Otherwise, it can continue under existing authorization unless a checkpoint requires a pause. Completing an increment neither grants additional permission nor removes permission already given.

Three events have different purposes:

| Event | Purpose |
| --- | --- |
| Completing an increment | Establish that one bounded result meets its acceptance conditions. |
| Reporting a result | Consolidate unreported work at task completion, handoff, or when seeking your input; provide other requested or required disclosures. |
| Reaching an approval checkpoint | Reserve a decision for you before the relevant work continues. |

A completed increment can lead directly to the next one without a chat report. A requested or required report does not itself create an approval checkpoint. Your conditions, the contract's checkpoints, and the tool's rules all apply; your instructions take priority within the tool's actual hierarchy and permissions.

### When the agent asks you

A **material** issue significantly affects correctness, scope, risk, or whether to proceed. The contract distinguishes required involvement from recommended consultation and routine choices:

| Situation | What the agent does |
| --- | --- |
| Material unresolved intent or permission | Must bring the question to you. |
| Missing consequential constraints in requirements, architecture, or conventions | Must agree them with you as needed. |
| An unsettled consequential choice | Should ask first: this is a strong recommendation with justified exceptions. |
| Routine local choices within agreed limits | May choose easily reversible details, such as a private helper name; material assumptions remain visible. |
| Unexpectedly greater work or investigation | Must reassess and wait for direction before the additional work. |

These strengths follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html). Exceptions to a recommendation require weighing consequences and justifying the departure; material departures must be explained. They cannot bypass required involvement or authorization limits. Missing answers grant no broader permission, and reporting a consequential choice afterward cannot supply advance authorization.

### When the work grows unexpectedly

If new evidence shows that completion needs materially more work or investigation than expected, the agent must explain what changed, what remains unfinished or uncertain, and the smallest useful complete next step. It then waits for your direction **before undertaking that additional effort**, even if broad authorization already covers the outcome.

For the field-count increment:

| Finding | Expected response |
| --- | --- |
| Another malformed row fits the agreed rule and expected local checks. | Complete and validate the regression case within the increment; include it in the next report when reporting is due. |
| Rejecting rows requires redesigning a shared parser and investigating other callers. | Explain the larger effort and unfinished result, propose a next step, and wait for direction. |

This assessment considers scope, uncertainty, consequences, and reversibility. There is no numerical threshold based on changed lines or token count. The checkpoint applies in every phase, and splitting the work cannot excuse incomplete or inadequately checked results.

### Instruction files and external actions

Edits to `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` require an explicit request concerning the file or its instructions. Asking the agent to apply recommendations specific to that file qualifies. Necessary companion edits to the other listed files may accompany that request; edits to these files stay separate from unrelated work. This condition also applies to editorial changes.

Commits, publishing, and other external actions require authorization, which may already be part of your request. Permission to implement a change does not by itself authorize every external action that might follow. See the [instruction-file and external-action rules](AGENTS.md#53-instructions-contract-files-and-external-actions).

### Optional controls you can add

You can select a particular increment, supply an investigation limit, request status updates, or add review checkpoints. Asking for updates does not by itself require approval before every next increment. To add those pauses, for example:

> Propose the first increment and wait for my approval before editing. After implementing and checking it, wait for my review before starting another increment.

That request adds specific pauses. You may instead name the exact behavior to address next or impose a tighter investigation limit. The agent remains responsible for a coherent approach, adequate validation, and every required checkpoint. Establishing and stating a limit before a blocking inquiry is already its duty, as the next section explains.

The full interaction conditions are in [AGENTS.md §5.1](AGENTS.md#51-scope-effort-and-requester-interaction).

## When an investigation is needed

Sometimes the next decision depends on missing evidence. Before investigating that **blocking uncertainty**, the agent must establish and state the question, scope, objective, effort limit, and evidence needed. You do not need to request this framing or supply the limit yourself.

Suppose, unlike the first example, the existing CSV reader's handling of quoted commas is uncertain. The agent could frame an inquiry as follows:

| Item stated before starting | Illustrative inquiry |
| --- | --- |
| Question | Does this reader preserve a quoted comma in the sample? |
| Scope | The existing reader and test setup. |
| Objective | Obtain evidence about the reader's suitability for the required input format. |
| Effort limit | One execution attempt and inspection of any output. |
| Evidence needed | The resulting parsed fields for that sample. |

The acceptance condition is an evidenced answer to the question, with its limits. The prediction might be that the quoted field remains intact. The agent runs the experiment, captures the output, and assesses both completion and the approach:

| Result | What it establishes |
| --- | --- |
| The output shows an intact quoted field. | The inquiry has its answer. This sample supports the prediction, within the limits of that evidence. |
| The output shows a split quoted field. | The inquiry still has its answer, but the prediction is disproved. The parser limitation informs the next Plan. |
| The attempt produces no usable output. | The allowance is exhausted without meeting acceptance conditions. The agent stops and reports incomplete work, missing evidence, and uncertainty. |

A negative finding can complete an investigation; an implementation required to preserve the field would remain incomplete if it split it. Revising a prediction changes neither your requirements nor the acceptance conditions. If you requested only investigation, that request alone would not authorize a parser change.

An **investigation effort limit** bounds the inquiry independently of whether it succeeds. The agent must stop when it obtains the needed evidence or reaches the limit, report remaining uncertainty, and explain any need for broader research or a wider design decision. A negative result grants no permission for extra attempts merely to obtain the predicted result. Repairing a failed test environment or running more experiments is additional work subject to the [interaction and growth rules](#when-the-agent-pauses-or-continues).

The one-attempt allowance above is an example. The contract prescribes no universal amount, measurement unit, or selection formula. Limits could bound specified checks or experiments, or use time where elapsed time can be tracked. If the agent omits a limit, there is no hidden default to assume. Stating a limit does not itself require your approval of every limit; consequential unresolved constraints and mandatory checkpoints still require your involvement.

The findings guide what follows: evidence supporting the reader may allow row validation next; contrary evidence changes the basis for that plan. Either way, the next step stays within authorization, and unexpectedly greater effort requires direction before it proceeds.

See [framing an inquiry](AGENTS.md#12-bound-the-work-and-choose-an-approach) and [assessing completion and learning](AGENTS.md#3-study--assess-completion-and-learning).

## Assess the result

The agent must consolidate unreported work into a report at task completion, at a handoff, or when seeking your input. While continuing, it must not draft or output routine progress reports unless you request them or another applicable rule requires them. It still makes required disclosures, such as reporting a blocking tool limitation or explaining a need for unexpectedly greater work.

The report explains what was completed, why, where to review it, what was checked, and what remains uncertain or unfinished. Material assumptions, decisions, conflicts, risks, and justified departures from strong recommendations stay visible. One report can cover several increments while distinguishing their completion from fulfillment of the overall task.

Before completing each increment, the agent must run relevant available checks against its acceptance conditions, whether or not it reports at that point. Failed, unavailable, or omitted checks must be disclosed under the reporting rules. Passing tests cannot substitute for an unimplemented requirement or a necessary performance or operational check. Required findings and records are maintained as work proceeds; they are not deferred until the next chat report.

Appropriate tests are a strong default for behavior changes, defect repairs, and clarified edge cases. Unit tests should use [Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html): the starting situation, action, and expected result. Neither literal labels nor a particular framework are required. Tests must not be weakened merely to pass.

When edits are displayed, changed portions with enough context are the default. A report may use a summary, paths, and links without a diff. Complete-file links with an explanation are the strong default for new files or extensive rewrites where available; you can request full copyable contents.

The agent must report tool limits that block edits, checks, or instruction loading. For blocked edits, it supplies a focused patch or exact changes with paths and application context where possible. Full contents may help when needed to make those edits usable.

Reports should fit the work. Small mechanical changes normally need only a concise outcome and checks, without invented risks, follow-up, or a mandatory template. See the [reporting rules](AGENTS.md#44-report-the-result-and-choose-the-next-step).

### Understanding token use

Reports summarize what the effort produced when reporting is due. They provide a qualitative view, not a token measurement or a guaranteed review opportunity between increments. While the agent continues, suppressing routine report drafting and output avoids spending tokens on those summaries. Required reasoning, validation, records, and disclosures still happen; total consumption can remain substantial even when increments are small and complete.

The contract has no token meter, hard quota, or required token total in every report. For figures, use data your tool or provider exposes and check which activity or period it covers before attributing it to an increment. You can ask the agent to include usage figures it can actually access; without measurements, exact consumption remains unknown.

The controls aim to prevent unnecessary expansion while preserving required quality. They guarantee neither a particular cost nor measured savings.

## Understand implementation choices

The contract favors understandable implementations, clear responsibilities, and complexity justified by current requirements. [Simple Design](https://martinfowler.com/bliki/BeckDesignRules.html) provides the baseline: meet requirements and pass tests, express intent, avoid duplicated knowledge, and retain only necessary elements.

A request for one input format should produce a complete solution for that format. An imagined future feature alone does not justify a framework for other formats. Agreed performance limits or other current requirements can justify complexity. Suitable existing code and patterns can be reused; unrelated cleanup stays outside scope.

Supporting techniques apply when their benefits justify their costs. Examples include supplying a dependency from outside a component, using a value object to express domain meaning, or composing smaller components. They do not automatically require new libraries or restructuring. Public contracts, compatibility, error handling, required logging, resource lifecycles, concurrency guarantees, and security must be preserved unless changing them is intended and authorized.

[Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) preserves observable behavior. If you want different behavior, state that outcome so affected requirements, tests, and documentation can change with it. The [engineering rules](AGENTS.md#2-do--perform-the-authorized-work) give the conditions; the [technical guide](README-maintainers.md#engineering-choices) explains the methods and their trade-offs.

## Use requirements and documentation

Documentation supplies context and develops as work establishes facts. During a bounded repair, affected documentation stays current and significant in-scope choices are recorded. A wider audit, conversion of untouched requirements, or reconstruction of past decisions needs corresponding authorization.

### Make expected behavior explicit

New or revised in-scope system requirements use [EARS](https://alistairmavin.com/ears/), a consistent way to express verifiable behavior through conditions and responses. For example:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

The project must also settle whether processing continues with later rows. The wording pattern expresses a decision; it cannot make that decision for you. Adoption does not automatically convert every existing requirement.

### Let architectural knowledge grow with the project

[arc42](https://arc42.org/overview/) organizes architectural knowledge: goals, boundaries, structure, operation, decisions, quality, risks, and other applicable topics. You can adopt the contract before that documentation is complete. Use known facts and keep material unknowns visible; empty headings and invented facts do not establish coverage.

Names and folders remain flexible. The initial default is one architecture document in the existing documentation folder, or root `docs/` if there is none. For known coverage gaps, the agent must propose improvements and should make them within authorized scope. You may defer, limit, or decline them; material gaps remain visible.

### Preserve significant choices and identify debt

A significant lasting choice within the authorized scope requires an [Architecture Decision Record (ADR)](AGENTS.md#41-record-significant-decisions-and-technical-debt) in or linked from [arc42's decision section](https://docs.arc42.org/section-9/). Selecting a parser to meet a memory constraint is one possible example. The record retains context, reasons, consequences, and status. Routine local choices normally need none; proposed, accepted, and superseded decisions remain distinguishable, with useful history and replacement links.

The agent may record current, task-relevant, evidenced technical debt in the architecture's risks and debt section. It considers accepted requirements and trade-offs, flags uncertain classifications, and tells you what was recorded, why, where, and with what uncertainty. A deferred feature, rejected alternative, or different preference alone is not debt. Recording debt grants no permission to fix it; records must reflect in-scope changes or fixes.

### Ask for the guide you need

[Diátaxis](https://diataxis.fr/) distinguishes four reader needs: tutorials teach through practice, how-to guides help complete a task, reference supplies facts and interfaces, and explanation develops understanding. “Show an operator how to correct rejected rows and retry an import” identifies a how-to need.

New guides require an explicitly requested or agreed purpose. These methods do not require four documents, an ADR, or a new guide for every increment. Affected existing guides stay current. Comments, docstrings, and generated API documentation follow suitable language and tool conventions.

[DRY](https://media.pragprog.com/titles/tpp20/dry.pdf) keeps knowledge consistent through one authoritative owner. A guide can explain a retry setting and link to its definition; necessary copies need a clear source and update process. Similar-looking code may express different rules, so resemblance alone does not require abstraction.

See the [knowledge rules](AGENTS.md#52-maintain-canonical-knowledge-and-consistent-artifacts) and the [design reasons for the documentation methods](README-maintainers.md#documentation-choices).

## Bring an existing project into alignment

Installation establishes standing expectations for subsequent tasks. Alignment of existing documentation and code is work to request explicitly, even if the project previously had no `AGENTS.md`.

You can request alignment as a broader goal. The agent identifies a small, useful area to address within that authorization, such as a component or architectural concern. You may name an area if you have a priority. Project requirements, accepted decisions, and implementation supply the evidence; the contract supplies collaboration policy.

For the authorized work, the agent:

1. **Assesses the documentation.** Compare the area's known content with applicable arc42 coverage and expectations for requirements, decisions, and guides. Identify useful material, gaps, contradictions, duplication, and unclear ownership; keep material unknowns visible.
2. **Improves it when authorized.** Preserve an adequate arrangement, express revised requirements with EARS, retain known decision reasons and history, and describe the current system accurately. Label proposed or unfinished changes and complete each increment within scope.
3. **Reviews relevant code.** Use the clarified context and engineering practices to identify concrete issues and explain why changes would help. Review permission alone does not authorize edits.
4. **Implements authorized improvements.** Work in small, complete increments with relevant checks and affected documentation. Refactoring preserves observable behavior; intended behavior changes need corresponding authorization.

For example:

> Assess how this project's documentation aligns with AGENTS.md.

This authorizes assessment. The agent chooses a useful first assessment increment and can continue through further authorized assessment increments without routine progress reports. It consolidates findings at completion, handoff, or when seeking your input. Edits need further permission even without an explicit “wait before editing.” A request that already authorizes improvements can cover subsequent implementation increments, subject to the consultation and reassessment rules.

An empty project can develop documentation and implementation through useful authorized work. Coverage expectations alone grant no permission for a repository-wide audit or reorganization.

## Continue unfinished work

Agents use **`.agent-continuation-context.md` at the repository root** when unfinished work needs context beyond code, tests, and permanent documentation. A task with no extra context needs no record merely to demonstrate compliance.

### Starting or resuming a session

At session start, the agent must check the fixed path and read the record if present. Unless you have acknowledged it that session, it mentions the path and summarizes the record once early. That notice needs no reply and does not authorize resuming the task.

On resumption, the agent compares the record with current files, checks, and instructions. An interruption can leave it stale. Completed, partial, unverified, and proposed work remain distinguishable, and material differences are reported. A recorded next step supplies no permission.

### What the record preserves

When needed, the record remains concise and current, including at meaningful review boundaries and planned stops. It holds:

- Task and current increment objectives, agreed direction, authorization, and constraints.
- Progress, checks, remaining work at the appropriate level, and open consequential questions.
- Links to authoritative project information and a likely next increment.

Code, tests, checks, and current-system documentation establish what exists. Architecture and ADRs retain lasting reasons. The continuation record holds otherwise missing task context, avoiding transcripts and detailed distant plans. This applies PDSA's retained learning and DRY's knowledge ownership.

### Keeping context usable

Relevant earlier context is reused; superseded copies are retired and links repaired. Competing records encountered during ordinary work are reported. If unrelated content occupies the fixed path, the agent preserves it and seeks direction.

Lasting findings move to appropriate permanent records, linked from continuation context where useful. Once the extra context is unnecessary, the work record is removed or archived, affected links are updated, and unresolved issues retain suitable owners.

The detailed conditions are in [starting context](AGENTS.md#11-establish-the-starting-context) and [context retention](AGENTS.md#43-retain-context-for-unfinished-work).

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
