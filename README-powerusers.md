# Getting more from AGENTS.md

After [installing the files](README.md#get-started), start with an ordinary request for an outcome. The agent is responsible for organizing the work, checking its results, and recognizing when it needs your direction.

The contract's primary aim is to control token consumption through small, meaningful, bounded increments and proportionate work. Its second aim is to keep you informed and in control of consequential direction. The agent manages routine execution; documentation preserves shared knowledge for you and future agents. This guide explains what that means in practice.

Read the first example for the overall process, then use the sections relevant to your situation:

| Your question | Where to go |
| --- | --- |
| How does the agent turn my request into progress? | [From a request to a result](#from-a-request-to-a-result) |
| When will it ask me, pause, or continue? | [Pauses and decisions](#when-the-agent-pauses-or-continues) |
| How do limits and additional work affect continuation? | [Limits and changes in work](#when-the-work-grows-unexpectedly) |
| Can a review or exploration update files? | [Records during review and exploration](#records-during-review-and-exploration) |
| What happens when it needs to investigate? | [Blocking investigations](#when-an-investigation-is-needed) |
| How do I assess the work and its effort? | [Results](#assess-the-result) and [token use](#understanding-token-use) |
| Why does it make these code or documentation changes? | [Implementation](#understand-implementation-choices) and [documentation](#use-requirements-and-documentation) |
| How do I adopt this in an existing project? | [Alignment](#bring-an-existing-project-into-alignment) |
| Is my tool loading the instructions? | [Compatibility and adoption checks](#tool-compatibility) |

[AGENTS.md](AGENTS.md) defines the rules and exceptions. The [technical guide](_internal/CONTRACT-DESIGN.md) explains their design rationale.

## From a request to a result

You might ask:

> Add CSV imports that report invalid rows and continue processing valid rows.

That is the **task objective**: the overall outcome you want. The agent selects an **increment**, a deliberately small step toward it, normally useful, understandable, reviewable, and verifiable on its own. You do not need to break the task down first.

The agent uses [PDSA—Plan–Do–Study–Act](https://deming.org/explore/pdsa/) from your request onward. Plan defines the next useful step; Do carries it out; Study checks the result and the approach; Act uses those findings to decide what follows. PDSA describes what the agent is doing. Separate [progression guards](AGENTS.md#2-progression-guards) decide, in any phase, whether work may proceed or needs your direction, and [triggered rules](AGENTS.md#3-triggered-rules) add duties such as records, documentation updates, or reports whenever their conditions arise.

### Plan: choose the next increment

Choosing the first increment is part of Plan. The agent establishes your objective and permitted work, then inspects the relevant requirements, code, tests, configuration, architecture, and decisions. It needs to understand what is agreed, what already works, what is missing, and whether uncertainty blocks the next decision.

For this example, suppose that inspection finds agreed rules for invalid rows and line numbers, with tests supporting the existing reader's handling of the required CSV format. Field-count validation is missing. The existing row-processing code gives access to the fields, header, and line number, suggesting that this rule can be added locally.

That evidence supports a small, useful increment: reject rows whose field count differs from the header, report them, and continue processing. This addresses one missing behavior and can be checked independently of the remaining invalid-row rules. Its scope includes the affected implementation, tests, and documentation.

The agent defines **acceptance conditions**: reject mismatched rows, report their line numbers, and continue with valid rows, including a valid row after a rejection. These are the results that must be demonstrated before this increment is complete. The agent derives them after inspection, from the agreed rules; writing them down does not create new system requirements.

Its **prediction** concerns the proposed approach: validation at the existing row boundary will suffice. If the implementation needs a different approach, that prediction may be wrong even though the acceptance conditions can still be met. The objective, scope, conditions, and approach can be refined together as the context becomes clear, without departing from your instructions or agreed requirements. Later work stays at outline level.

After proportionate preliminary context gathering, the agent briefly states the overall task outline and the first increment's objective and bounds in chat before substantial work. For example:

> I'll add the agreed invalid-row checks while preserving processing of valid rows. First, I'll add field-count validation at the existing row boundary, check reported line numbers and continued processing, and update the affected import documentation. Later increments will cover the remaining agreed rules.

This initial plan makes the direction and next action understandable. It creates no approval checkpoint. The agent can refine routine local implementation details as evidence develops, while keeping the increment bounded and respecting the [limits and consultation rules](#when-the-work-grows-unexpectedly).

Different findings can lead to a different first step. If the intended invalid-row behavior is unsettled, the agent brings consequential questions to you and develops the relevant requirements within authorization. Behavior agreed that way, which the importer must keep providing after this task, is a new system requirement. It belongs in the project's **canonical owner**: the file or section that is authoritative for that knowledge and is kept current when it changes. New or revised requirements use the EARS wording pattern explained under [Make expected behavior explicit](#make-expected-behavior-explicit).

Where the rules already have an authoritative owner, as in this example, the agent checks against them without writing duplicates. The increment's acceptance conditions identify which of those rules must be demonstrated for this step. If the reader's suitability is uncertain, a [bounded investigation](#when-an-investigation-is-needed) may supply the evidence needed before selecting an implementation step.

### Do, Study, and Act: complete the step and use its findings

- **Do the work.** Add that validation, the relevant tests, and updates to affected documentation. Keep the changes focused on the agreed behavior. If a significant lasting choice arises, record it and obtain any required direction before adopting or implementing it.
- **Study the result.** Run relevant available checks against the acceptance conditions before completing the increment. This is **validation**. Separately, compare the observations with the prediction: did the existing row boundary support the change, or did the approach need revision? Disclose failed, unavailable, or omitted checks under the [reporting rules](#assess-the-result).
- **Act on what was learned.** Retain, revise, or discard the approach within authorization and preserve useful findings. If the task remains unfinished, use the findings to plan the next authorized increment or seek direction when required.

After checking this increment, the agent can proceed to another within existing authorization unless a checkpoint requires your direction. It should minimize routine progress reports and keep intermediate communication concise and useful; [reporting and approval checkpoints](#when-the-agent-pauses-or-continues) have separate triggers. Suppose the findings support adding an agreed check for missing required values next. The agent reassesses progress, remaining work, direction, and limits, then defines that next increment and its checks. It need not repeat the initial planning message or send a progress report for every increment.

The agent continues through the remaining agreed rules, selecting each next increment from the evidence and completing its checks. In this path, the work stays within authorization, established direction, and applicable limits, and no unresolved consequential question requires your direction. Once all agreed import behavior is implemented and validated, the task objective is fulfilled. A consolidated task-completion report could look like this, assuming the named files exist and the checks succeeded:

> Implemented field-count, required-value, and the remaining agreed row-validation rules in `src/importer.py`. Added regression coverage in `tests/test_importer.py` and updated `docs/import-format.md`.
>
> Checks passed for all agreed import rules, including mismatched field counts, missing required values, reported line numbers, and valid rows following rejections, together with the required CSV-format checks. Field-count and required-value validation worked at the existing row boundary, supporting that approach for those rules.
>
> The agreed CSV-import objective is complete.

Each increment was completed and checked while the agent continued toward the overall objective; task completion triggers the consolidated report. You did not need to request status between increments or supervise their selection. Findings guided each next choice without a complete sequence planned in advance. If evidence instead points to a consequential change in parser direction, the [consultation rules](#when-the-work-grows-unexpectedly) apply before that choice is adopted or implemented.

The phase labels explain the reasoning, not a required report format. Phases can overlap or repeat: tests may be planned before implementation, and documentation changes as facts become established. Routine work needs no worksheet, formal experiment, or separate phase reports. PDSA also applies to investigations and documentation-only work.

PDSA's Plan phase is part of this reasoning process. A tool's Plan mode has its own proposal and approval procedures; entering it grants no additional authorization.

## Keep work small and complete

A small increment limits how much the agent takes on at once. Completing it requires enough analysis for the current decision and a complete result within its scope. A required stop can leave the increment unfinished; that is not completion. Correctness, completeness, consistency, and validation take priority over saving tokens.

For example, choosing a storage approach may require careful examination of requirements, alternatives, dependencies, and risks. It need not include designing every future data structure and function. The agent develops the next decision at the current level of discussion—architecture, an investigation, a document, or a local change—and keeps later detail at outline level until needed.

The agent selects the smallest useful next increment within your authorization, including in planning or approval workflows. During Plan, it considers which unmet behavior or blocking question can usefully be addressed next and which dependencies are needed for a complete result. It assesses the [scope, uncertainty, consequences, and reversibility](AGENTS.md#22-decisions-and-requester-interaction) of that decision. These criteria guide judgment; the contract prescribes no fixed sequence or ranking formula.

Consequential unresolved intent or constraints come back to you, as do new consequential architectural or lasting design directions and material departures from established direction unless the specific choice is already authorized. Selecting and defining routine steps—their objectives, acceptance conditions, approaches, and predictions—remain agent responsibilities.

An increment can deliver evidence for a decision as well as an implementation. A code change includes the affected tests, configuration, and documentation needed for its result; an investigation includes the evidence and conclusion needed for its decision. Either can be complete while the overall task remains unfinished.

A straightforward authorized correction can proceed without an approval exchange; the brief initial planning statement still applies. If a proposed step cannot stand alone, the agent must first explain why, what remains usable or testable, and how to undo it. Material limits on undoing changes stay visible. If no safe step is possible, it presents alternatives and seeks direction.

See the contract's [increment rules](AGENTS.md#11-plan--define-the-next-increment).

## When the agent pauses or continues

The agent finishes when the task objective is fulfilled. Otherwise, it can [continue under existing authorization](AGENTS.md#25-continuing-to-another-increment) unless a checkpoint requires a pause; the contract's [composition rules](AGENTS.md#4-how-the-layers-compose) summarize these outcomes. Completing an increment neither grants additional permission nor removes permission already given.

These events have different purposes:

| Event | Purpose |
| --- | --- |
| Completing an increment | Establish that one bounded result meets its acceptance conditions. |
| Stating the initial task outline | Make the direction and first increment's objective and bounds understandable before substantial work; the statement creates no approval checkpoint. |
| Notifying you of material inquiry uncertainty | Promptly make the blocking uncertainty and its significance for the next decision clear, unless already communicated in your request or the task framing; notification grants no authority and creates no approval checkpoint. |
| Reporting a result | Show what the work produced, its checks, and what remains; one report can cover several increments. |
| Consulting at a required decision or checkpoint | Obtain your direction before the affected choice is adopted or implemented, or the checkpoint is passed. |
| Recording durable knowledge | Preserve authoritative facts, decisions, and reasons for maintainers, users, and future agents; recording supplies no decision authority. |

The agent must combine unreported work into a report at task completion, when seeking your input, or at a **handoff**. A handoff means stopping before the task is complete and passing the unfinished work to you or another person or agent. Routine progress reports should be minimized, and intermediate communication should be concise and useful. These recommendations allow judgment about useful updates; they neither prohibit intermediate messages nor require one for every increment.

Some information must arrive before the next action. If it affects permission or a decision you need to make, the agent discloses it before the affected work. Other disclosures, including investigation outcomes, should normally join the next consolidated report.

Two communication duties retain their own timing. After proportionate preliminary context gathering, the agent briefly states the [task outline and first increment's objective and bounds](#plan-choose-the-next-increment) before substantial work. For a [material inquiry](#when-an-investigation-is-needed), it must promptly explain the uncertainty and why it matters for the next decision, unless your request or the task framing already communicated that. One concise message can cover both duties when applicable. Notification does not require approval for otherwise authorized investigation, and does not substitute for consultation before an unsettled consequential choice is adopted or implemented.

A handoff report transfers the task objective and established direction; applicable limits and checkpoints, including allowances already consumed; the next or unfinished increment's objective, bounds, and acceptance conditions; and relevant inquiry conclusions, supporting evidence, and unresolved uncertainty. Together with meaningful completed and unfinished results, this gives the next person or agent the state needed to continue, without a chronological activity log. A continuing agent uses this state and recovers missing authorization or limit information, or obtains your direction before dependent work. Durable project knowledge remains in its canonical documents.

A completed increment can lead directly to the next one without a chat report. A requested or required report does not itself create an approval checkpoint. Your conditions, the contract's checkpoints, and the tool's rules all apply; your instructions take priority within the tool's actual hierarchy and permissions.

### When the agent asks you

A **material** issue significantly affects correctness, scope, risk, or whether to proceed. The contract distinguishes required involvement from recommended consultation and routine choices:

| Situation you may encounter | What the agent does |
| --- | --- |
| An unanswered question could significantly change the intended result or permitted work. For example, should an imported duplicate replace the existing record? | Must bring the question to you. |
| A missing constraint could significantly change the design or checks. For example, the import must fit a deployment's memory budget, but that budget is unsettled. | Must agree the consequential constraint with you as needed. |
| A choice establishes new consequential architectural or lasting design direction, or materially departs from established direction. For example, changing the shared parser's error contract. | Must obtain your direction before adopting or implementing the choice unless that specific choice is already authorized. |
| Another unsettled choice materially affects the decision factors, optimization, or lasting complexity, without triggering a mandatory consultation rule. | Should ask first: this is a strong recommendation with justified exceptions. |
| A local correction stays authorized, bounded, low-impact, easily reversible, and consistent with established direction. | May choose the implementation details and validate the correction independently; material assumptions remain visible. |
| Further work would exceed your explicit limit or pass your checkpoint. | Must obtain your direction first; another increment or retry does not reset the limit. |
| More increments are needed, but their contribution is justified and the work stays authorized and consistent with direction and limits. | Reassess cumulative progress and continue in small increments. |

These strengths follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html). Exceptions to a recommendation require weighing consequences and justifying the departure; material departures must be explained. They cannot bypass required involvement or authorization limits. Missing answers grant no broader permission, and reporting a consequential choice afterward cannot supply advance authorization.

### When the work grows unexpectedly

Additional work calls for reassessment, not an automatic approval request. Before expanding planned work or starting another increment or attempt, the agent considers cumulative progress, remaining work, established direction, and applicable limits. It must justify the next increment's contribution from the evidence; if it cannot, it seeks your direction.

An informal expectation such as “I expect this to be a small fix” is not automatically a binding budget. “Do not undertake more than one increment without consulting me” is a binding checkpoint. If the intended force of your statement is materially ambiguous, the agent must clarify it rather than treating it as either unlimited authority or a hard limit.

The agent must obtain your direction before exceeding requester-imposed effort or scope limits or passing checkpoints. Only your direction can revise them; new increments, retries, and handoffs do not reset them. Even without a declared effort allowance, inquiry must use [small, bounded, proportionate increments](#when-an-investigation-is-needed), end when evidence is sufficient, and reassess at an increment's bounds before further investigation.

For the field-count increment:

| Finding | Expected response |
| --- | --- |
| Another malformed row fits the agreed rule and existing validation boundary. | Make and validate a routine local correction within the bounded increment; report it when reporting is due. |
| A proposed repair changes the shared parser's established error contract. | Prepare the concrete proposal and obtain direction before adopting or implementing that material departure, unless the specific choice is already authorized. |
| The next step would pass your one-increment checkpoint. | Report the result and obtain direction before continuing. |

For an alternative path through the CSV task, suppose field-count and required-value validation have been completed and checked. Inspection shows that the shared parser aborts before the importer can handle another agreed invalid-row case; a focused reproduction confirms that the sample raises an error before a row reaches the importer. A bounded assessment supports proposing an opt-in recovery interface for the importer while preserving the fail-fast default for existing callers. That changes established direction and has not been specifically authorized.

Assuming the named files exist, the earlier checks succeeded, and no inquiry remains open and no additional requester limit or checkpoint applies, the agent could report:

> Completed field-count and required-value validation in `src/importer.py`, added regression checks in `tests/test_importer.py`, and updated `docs/import-format.md`. Checks passed for those rules, line numbers, and valid rows following rejections.
>
> The CSV-import objective remains unfinished. A focused reproduction of the next invalid-row case confirms that the shared parser raises before returning a row to the importer. I propose an opt-in recovery interface for the importer, preserving existing callers' fail-fast behavior. The evidence, proposed decision, and compatibility risks are recorded in `docs/decisions/parser-recovery.md`. The interface is unimplemented and its compatibility checks remain outstanding.
>
> If approved, the next increment will implement that interface and its importer integration, with checks for row-error reporting, continued processing, and unchanged default behavior for other callers. Do you approve this direction, or should recovery stay within importer-specific parsing?

The decision concerns the parser's contract and responsibilities. The proposal is recorded as Proposed; recording it does not authorize its adoption or implementation. Relevant context gathering and narrow, bounded inquiry can establish facts for consultation within existing authorization. Any material inquiry uncertainty and its significance must be made clear promptly unless already communicated in the request or task framing; that notification does not authorize the proposed direction.

The report preserves completed work, the unfinished objective, established behavior, the proposed direction, and the next increment's scope and acceptance conditions. A handoff with active limits or inquiries must also preserve their state as described under [reporting and handoffs](#when-the-agent-pauses-or-continues).

### Instruction files and external actions

The special edit protection covers exactly three root-relative paths: `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md`. Edits require an explicit request concerning the file or its instructions. Asking the agent to apply recommendations specific to that file qualifies. Necessary companion edits to the other two listed files may accompany that request; other affected documentation follows the ordinary synchronization rules under its own authorization and scope; edits to these files stay separate from unrelated work. This condition also applies to editorial changes.

Directory-level instruction files may add subtree rules only when those rules are compatible with the root contract. They are not automatically subject to that special three-file protection, although ordinary edit authorization and tool restrictions still apply. The tool determines actual discovery, scope, and precedence, but that precedence never makes conflicting policy acceptable. Encountered conflicts must be reported. During adoption, a person validates which existing practices, conventions, and workflows persist, as the [installation steps](README.md#get-started) explain.

External actions mean commits, publishing or sending, and changes to remote or shared state. They require authorization, which may already be part of your request. Permission to implement a change does not by itself authorize every external action that might follow. Read-only access follows task scope and tool permissions; consulting a source is not itself a publication or state-changing action. The [method-reference consultation limits](AGENTS.md#39-method-references) still apply to linked method references. See the [instruction-file and external-action rules](AGENTS.md#38-instructions-protected-files-and-external-actions).

### Records during review and exploration

Two separate questions decide whether an assessment changes files.

**First, which writes are permitted?** During analysis or review, [AGENTS.md §2.1](AGENTS.md#21-authority-and-scope) permits only material, durable findings under the findings rule, maintenance of Architecture Decision Records (ADRs) and technical-debt records under their respective rules, and verified factual corrections. An ADR retains a significant choice and its reasons. Technical debt concerns evidenced design or implementation compromises that increase maintenance cost or risk.

Assessment alone does not authorize implementation, new or changed system requirements, accepting or changing decisions beyond existing authority, unrelated documentation repairs, or documentation backfills. Authorized scope, your instructions (including a no-edit instruction), protected-file rules, and tool permissions and approvals still apply to every permitted write.

**Second, is a record required in this case?** The [findings rule](AGENTS.md#32-durable-findings-and-permanent-records), [decision rule](AGENTS.md#33-significant-decisions-adrs), and [debt rule](AGENTS.md#34-technical-debt) each have their own conditions and requirement strength. They apply whenever those conditions arise, including during assessment. Permission to write a kind of record does not mean that every assessment must produce one.

A **permanent record** is the canonical project document owning the topic, such as architecture documentation or an ADR. A finding must be recorded there when it is both **material**, meaning it significantly affects correctness, scope, risk, or whether to proceed, and **durable**, meaning it is expected to remain useful beyond this task or attempt for maintenance, operation, requirements, architecture, or technical decisions. Chat and working notes do not substitute for that project record.

Transient task facts and the routine history of the work need no permanent record, so assessment does not become a work log. A record preserves knowledge; it does not authorize implementing a recommendation, rewriting intended behavior, or accepting or changing decisions beyond existing authority. The examples below also show what happens when no suitable record exists or writes are prohibited.

A verified factual correction makes an existing description of current project facts within the assessed scope—such as a command, path, interface, or behavior—match the canonical owner of that kind of knowledge, for example correcting a documented command to match authoritative package configuration. Requirements, decision records, and protected instruction files are not corrected this way. An unresolved conflict over intended behavior remains a question or finding, not permission to choose a new requirement.

These examples assume you requested only assessment or exploration and the tool permits the described writes, except where stated:

| Situation | Permitted or required result |
| --- | --- |
| A brief discussion explores possible CSV-import approaches without establishing material findings or significant lasting choices. | No record is required merely to document that brainstorming took place. |
| An assessment establishes that the existing reader mishandles a required input format. No significant design choice has been made. | This is durable project knowledge, so preserve the material finding and its evidence in the appropriate permanent record. A finding alone does not require a decision record or authorize a parser repair. |
| A temporary CI outage blocks a check, or a failed experiment matters only to the current attempt. | These are transient task facts: disclose them as the validation and reporting rules require, but they need no permanent record. |
| The same reader finding must be recorded; it belongs to architectural knowledge, and no suitable permanent record exists because the project has no architecture documentation or other owner for that topic. | The agent must create a minimal architecture document holding only that finding and its evidence, which becomes the topic's canonical owner. The contract recommends placing it in the documentation folder stated in `README.md`, otherwise root `docs/`; that default location needs no `README.md` edit. It adds no empty sections, placeholders, or backfill; other arc42 gaps remain proposals. |
| An assessment verifies that the setup command in a README disagrees with authoritative package configuration. | The agent may correct that factual error within the assessed scope, then validate and report the correction. It may not change the package configuration to make the old command true. |
| An architectural evaluation develops a concrete, significant proposal ready for decision or review. | Create a Proposed [Architecture Decision Record (ADR)](#preserve-significant-choices-and-identify-debt) with context, reasons, consequences, and relevant evidence. The proposal itself grants no authority to accept or implement it. |
| A significant lasting decision is made under existing authority and consultation rules, such as choosing streaming over full-file buffering after requester direction or specific prior authorization. | Mark it Accepted and preserve the reasons, evidence, and useful rejected alternatives. A separately recorded proposal that was rejected has Rejected status. Recording adds no ADR-specific approval checkpoint and cannot replace required prior consultation or grant implementation permission. |
| A review identifies duplicated validation rules whose maintenance risk is supported by inconsistent past fixes. | The agent may record [technical debt](#preserve-significant-choices-and-identify-debt), considering accepted requirements and trade-offs. It reports any entry: what, why, where, and classification uncertainty. Recording grants no permission to fix the issue. |
| You request: "Assess the parser. Do not create, modify, or delete any files." | The restriction covers records and factual documentation corrections. The agent can provide findings and proposed record or correction text in its response for you to retain. That text does not satisfy the record obligation; the unmade record is reported as unfinished work. |

A debt entry is optional under the debt rule; preserving a material finding that is durable project knowledge is still required, including one revealed by a discarded approach. See the [findings and record rules](AGENTS.md#32-durable-findings-and-permanent-records), subject to [authorized scope and requester restrictions](AGENTS.md#21-authority-and-scope) and the [protected-file rules](AGENTS.md#38-instructions-protected-files-and-external-actions).

### Optional controls you can add

You can select a particular increment, impose an explicit effort or scope limit, set an investigation limit, request status updates, or add review checkpoints. Asking for updates does not by itself require approval before every next increment. An additional checkpoint can reflect a project dependency, such as a team's review of user-visible behavior:

> Our team needs to review the import error messages before the importer is connected to the upload workflow. Implement and test the standalone validation and error reporting, then show representative results and wait for my confirmation before integration.

The agent chooses and completes the increments needed for that reviewable result. Your request reserves the integration decision until the review is complete. Stating the checkpoint in advance lets the agent plan for the handoff without relying on an interruption during unfinished work.

You may instead name the exact behavior to address next or impose an investigation limit. The agent remains responsible for a coherent approach, adequate validation, and every required checkpoint. Its duty to conduct bounded, proportionate work applies whether or not you set a limit or it announces an allowance. Prompt inquiry notification and any required consultation also remain its responsibilities, as the next section explains; a numeric budget or advance effort estimate is not mandatory.

The full interaction conditions are in the contract's [progression guards](AGENTS.md#2-progression-guards), especially [requester interaction](AGENTS.md#22-decisions-and-requester-interaction) and [requester limits and cumulative reassessment](AGENTS.md#23-effort-estimates-and-requester-limits).

## When an investigation is needed

Inspecting the relevant code, callers, tests, configuration, and directly related dependencies to establish starting context, and all reading of existing project documentation, are context gathering. Following an ordinary caller or test needs no inspection-by-inspection announcement. Reading those documents remains context gathering even when answering a material blocking question. Scope, requester limits, proportionate work, and cumulative reassessment still apply; this distinction supplies no unlimited research allowance.

Inquiry begins when activity beyond that context investigates material uncertainty about how to proceed that blocks the next decision. Purpose determines the distinction:

| Activity and purpose | Treatment |
| --- | --- |
| Run a prescribed measurement and apply a settled calculation to produce the requested output. | Ordinary execution if no investigation into how to proceed is needed; unknown data alone does not trigger inquiry. |
| Run the agreed acceptance suite to check an implemented change. | Validation; an unknown result alone does not trigger inquiry. |
| Use a documented probe to determine whether buffering or streaming can meet a known memory constraint. | Inquiry: the evidence resolves uncertainty blocking the approach decision, despite the prescribed procedure. |
| Investigate an unexplained validation failure to choose a repair approach after relevant context inspection. | Inquiry when material uncertainty blocks that decision; make the uncertainty and its significance clear promptly unless already communicated in the request or task framing. The original acceptance check was validation, not inquiry merely because it could fail. |

**Notification and consultation serve different purposes.** The agent must promptly make material uncertainty and its significance for the next decision clear to you, unless already communicated in your request or the initial task framing. For example, a request to establish whether the reader preserves quoted commas before choosing a repair already communicates that uncertainty and its purpose. The agent need not repeat it as a separate inquiry announcement. If it discovers a different material uncertainty blocking the next decision, the notification duty applies to that uncertainty.

Notification neither grants authority nor creates an approval checkpoint for otherwise authorized work. Narrow technical investigation may establish facts for consultation within existing authorization. If inquiry exposes an unsettled decision requiring your direction under [§2.2](AGENTS.md#22-decisions-and-requester-interaction), the agent must consult you before adopting or implementing it. Explaining the uncertainty, or discovering evidence in favor of an approach, cannot supply that direction.

**Bounded inquiry is a requirement on the work itself.** The agent plans small, bounded, proportionate increments focused on the uncertainty blocking the next decision. It defines the increment's objective, acceptance conditions, approach, and prediction as part of Plan, and keeps later detail at outline level. The contract does not require a five-element announcement, an advance effort estimate, or a declared allowance for every inquiry or subsequent attempt. Those omissions do not permit open-ended investigation: sufficient evidence ends inquiry, and an increment's bounds require reassessment before further investigation.

Suppose, unlike the [first example](#from-a-request-to-a-result), context inspection leaves quoted-comma handling unresolved. That uncertainty blocks deciding whether the reader needs repair before row validation can proceed. Assume the inquiry is authorized and fits applicable requester limits and checkpoints. If the uncertainty and its significance have not already been communicated, a concise notification could be:

> It is unclear whether the existing reader keeps a quoted comma within one field. That determines whether parsing needs repair before I add row validation; I'll check a sample using the existing test setup.

This is an illustration, not a required template or a complete list of announced fields. For this increment, the agent chooses one execution of a quoted-comma sample with the existing reader and inspection of its output. That makes the work bounded without exploring other parsers or redesigning the importer. The acceptance condition is an evidenced answer about that sample, with its limits; parsed fields showing whether the quoted comma remains inside its field would supply it. The prediction might be that the quoted field remains intact. The agent runs the experiment, captures the output, and assesses both completion and the approach:

| Result | What it establishes |
| --- | --- |
| The output shows an intact quoted field. | The inquiry has its answer. This sample supports the prediction, within the limits of that evidence. |
| The output shows a split quoted field. | The inquiry still has its answer, but the prediction is disproved. The parser limitation informs the next Plan. |
| The attempt produces no usable output. | This increment has reached its bounds without meeting acceptance conditions. The agent reassesses before further investigation; missing evidence, incomplete work, and uncertainty belong in the report when due. |

A negative finding can complete an investigation; an implementation required to preserve the field would remain incomplete if it split it. Revising a prediction changes neither your requirements nor the acceptance conditions. If you requested only investigation, that request alone would not authorize a parser change.

Evidence sufficiency and increment bounds answer different questions. Sufficient evidence answers the blocking question to the extent needed for the next decision; it ends the inquiry without additional exploration for its own sake. The bounds constrain how much work the agent undertakes before reassessing if evidence remains insufficient. In this example, the sample result answers the quoted-comma question, not every CSV-format requirement. No usable output leaves the question unanswered; that alone cannot justify further effort or establish completion.

For example, output identifying a transient setup fault may justify a targeted retry. Before another attempt, the agent must reassess cumulative progress, remaining work, established direction, and applicable limits, and justify the next increment's contribution from the preceding evidence. The retry must remain within authorization and be proportionate to resolving the question. If the evidence does not justify a next increment, the agent seeks your direction. A subsequent attempt does not automatically require a new advance announcement; prompt notification of material uncertainty and required consultation still apply when their conditions arise. Repairing a failed test environment and running more experiments follow the same [interaction and continuation rules](#when-the-agent-pauses-or-continues).

An explicit [requester-imposed limit](#when-the-work-grows-unexpectedly) is different from the agent's choice of a small experiment. If you say “Try once, then consult me before another attempt,” even an attempt with no usable output uses that allowance. The agent must report and obtain your direction before retrying. Limits may specify checks or experiments, or time where elapsed time can be tracked; the contract prescribes no universal amount, unit, or selection formula. New labels, increments, retries, and handoffs do not reset your limits or checkpoints. Without a declared allowance there is no hidden numeric default, but actual bounded work and reassessment remain mandatory.

Ending an inquiry or reaching an increment's bounds does not by itself require a chat interruption or pause the whole task. At task completion, handoff, or when seeking your input, the agent reports relevant conclusions and supporting evidence, remaining uncertainty, incomplete work or missing acceptance evidence, and any need for broader research or a wider design decision. Other information should normally wait for that consolidated report, while disclosures affecting authorization or a decision requiring your input must precede the affected work. If no justified safe step remains, a limit or checkpoint prevents continuation, or an unsettled consequential choice needs your direction, the agent reports and seeks it. A negative result or exhausted attempt supplies no additional authority.

The findings guide what follows: evidence supporting the reader may allow row validation next; contrary evidence changes the basis for that plan. A routine local repair can proceed within authorization and established direction. A consequential new design direction or material departure needs prior direction unless that specific choice is already authorized.

See [context gathering and bounded inquiry](AGENTS.md#24-context-gathering-and-bounded-inquiry) and [assessing completion and learning](AGENTS.md#13-study--assess-completion-and-learning).

## Assess the result

When you receive a report under the [reporting and checkpoint rules](#when-the-agent-pauses-or-continues), use it to answer these questions:

| Question | What to look for |
| --- | --- |
| What was completed, and why? | The outcome and reasons, distinguishing completed increments from completion of the whole task. |
| Where can I review it? | Affected paths and relevant links to decisions and authoritative project information. |
| What evidence supports the result? | Checks performed and disclosure of failed, unavailable, or omitted checks. |
| What could affect my decision? | Material assumptions, conflicts, risks, choices, and explained departures from strong recommendations. |
| What remains? | Unfinished work, missing evidence, and uncertainty. |

One report can cover several increments. Disclosures affecting authorization or a decision requiring your input, such as a proposed change to the parser's established error contract, must precede the affected work. Other disclosures, such as nonblocking technical debt and inquiry outcomes, should normally join the next consolidated report; initial task framing and inquiry notification retain their own timing. Assessing an inquiry's result before an agent decision does not itself require a chat report. Small reports need no separate field for every question.

Before completing each increment, the agent must run relevant available checks against its acceptance conditions, whether or not it reports at that point. Failed, unavailable, or omitted checks must be disclosed under the reporting rules. Passing tests cannot substitute for an unimplemented requirement or a necessary performance or operational check. Required findings and records are maintained as work proceeds; they are not deferred until the next chat report.

The contract distinguishes an unavailable check from an unverified acceptance condition. Alternative evidence can sometimes establish the condition, but it cannot replace a specifically required check. The substitution rules below preserve that distinction.

A check is **available** when it can run with the current authorization, tool access, permissions, credentials or resources, and prerequisites with ordinary expected setup. An easier alternative does not make it unavailable. The relevant available check must run even if another method could provide equally sufficient evidence. If running it would need missing access or resources, or materially more work, the agent discloses that and applies the authorization, limit, and reassessment rules. Additional work alone does not create an approval checkpoint.

Sufficient alternative evidence may replace a check only when the original check is unavailable **and** is not specifically required. Both conditions matter. Even then, the alternative must provide enough evidence for the acceptance condition. Simply reporting that a check could not run does not fill the evidence gap: without sufficient evidence, the condition remains unverified and validation incomplete unless the condition is validly revised.

A failed check or difficult implementation never justifies weakening, replacing, or reinterpreting a requirement or acceptance condition. Revision authority depends on where the condition came from. Conditions you supplied change only with your authority, and canonical requirements only through authorized requirement changes. The agent can refine conditions it derived only when the refinement stays consistent with your instructions, project requirements, scope, and decision authority.

For example, suppose an agreed import requirement says a failed import must leave the database unchanged:

| Available evidence | What can be concluded |
| --- | --- |
| A relevant integration check is available, and the agent could also inspect equivalent evidence manually. | Run the available check; equivalent evidence does not authorize substituting for it. |
| CI is unavailable, but an equivalent integration check passes locally against the required database and configuration. No CI-specific check was mandated. | The local evidence can establish the condition if it covers the required behavior. |
| Only tests against a mocked database run. | Those results do not establish rollback in the actual database; that acceptance condition remains unverified. |
| The requester specifically requires the CI integration check to pass. | A local result does not satisfy that requirement; the required check must run or the condition must be validly revised. |

An unrelated pre-existing failure does not automatically block completion. Its relevance must be assessed and the failure disclosed; each increment still needs sufficient evidence for its acceptance conditions and applicable requirements before it is reported complete.

Appropriate tests are a strong default for behavior changes, defect repairs, and clarified edge cases. Unit tests should use [Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html): the starting situation, action, and expected result. Neither literal labels nor a particular framework are required. Tests must not be weakened merely to pass.

When edits are displayed, changed portions with enough context are the default. A report may use a summary, paths, and links without a diff. Complete-file links with an explanation are the strong default for new files or extensive rewrites where available; you can request full copyable contents.

The agent must report tool limits that block edits, checks, or instruction loading. For blocked edits, it supplies a focused patch or exact changes with paths and application context where possible. Full contents may help when needed to make those edits usable.

Reports should fit the work. Small mechanical changes normally need only a concise outcome and checks, without invented risks, follow-up, or a mandatory template. See the [reporting rules](AGENTS.md#37-reporting).

### Understanding token use

Reports summarize what the effort produced when reporting is due. They provide a qualitative view, not a token measurement or a guaranteed review opportunity between increments. The recommendation to minimize routine reports aims to keep communication proportionate; intermediate updates are neither forbidden nor required as an effort audit. Actual effort discipline comes from bounded increments, evidence-based continuation, and respect for limits, whether or not an allowance is announced. Required reasoning, validation, records, and disclosures still happen; total consumption can remain substantial even when increments are small and complete.

The contract has no token meter, hard quota, or required token total in every report. For figures, use data your tool or provider exposes and check which activity or period it covers before attributing it to an increment. You can ask the agent to include usage figures it can actually access; without measurements, exact consumption remains unknown.

The controls aim to prevent unnecessary expansion while preserving required quality. They guarantee neither a particular cost nor measured savings.

## Understand implementation choices

The contract favors understandable implementations, clear responsibilities, and complexity justified by current requirements. [Simple Design](https://martinfowler.com/bliki/BeckDesignRules.html) provides the baseline: meet requirements and pass tests, express intent, avoid duplicated knowledge, and retain only necessary elements.

A request for one input format should produce a complete solution for that format. An imagined future feature alone does not justify a framework for other formats. Agreed performance limits or other current requirements can justify complexity. Suitable existing code and patterns can be reused; unrelated cleanup stays outside scope.

Supporting techniques apply when their benefits justify their costs. Dependency injection, value objects, and composition can support clarity or testability, but selecting a technique does not automatically require new libraries or restructuring and grants no additional authority for either. The [technical guide](_internal/CONTRACT-DESIGN.md#focused-techniques-and-how-they-work-together) explains the conditions and trade-offs of each technique under this contract.

Changes must preserve public contracts, compatibility, error handling, required logging, resource lifecycles, concurrency guarantees, and security unless changing them is intended and authorized. These preservation duties apply even when an implementation technique would otherwise simplify the change.

[Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) preserves observable behavior. If you want different behavior, state that outcome so affected requirements, tests, and documentation can change with it. The [engineering rules](AGENTS.md#12-do--perform-the-authorized-work) give the conditions; the [technical guide](_internal/CONTRACT-DESIGN.md#engineering-choices) explains the methods and their trade-offs.

## Use requirements and documentation

Documentation supplies context and develops as work establishes facts. Canonical requirements, architecture, decisions, and findings let you and future agents understand the same project without reconstructing its reasoning. During a bounded repair, affected documentation stays current and significant in-scope choices are recorded. A wider audit, conversion of untouched requirements, or reconstruction of past decisions needs corresponding authorization.

### Make expected behavior explicit

New or revised in-scope system requirements use [EARS](https://alistairmavin.com/ears/), a consistent way to express verifiable behavior through conditions and responses. For example:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

The project must also settle whether processing continues with later rows. In the [worked example](#from-a-request-to-a-result), that behavior is agreed: processing continues. Acceptance checks therefore cover rejecting the mismatched row, reporting its line number, and successfully processing a valid row after it. The wording pattern expresses a decision; it cannot make that decision for you. Adoption does not automatically convert every existing requirement.

### Let architectural knowledge grow with the project

[arc42](https://arc42.org/overview/) organizes architectural knowledge: goals, boundaries, structure, operation, decisions, quality, risks, and other applicable topics. arc42 sets the target coverage; uncovered applicable topics are gaps handled by improvement proposals rather than violations, so you can adopt the contract before that documentation is complete. Use known facts and keep material unknowns visible; empty headings and invented facts do not establish coverage.

Names and folders remain flexible. The initial default is one architecture document in the existing documentation folder stated in `README.md`, or root `docs/` if none is stated. Your `README.md` needs to name documentation locations only when they differ from root `docs/`. For known coverage gaps, the agent must propose improvements and should make them within authorized scope. You may defer, limit, or decline them; material gaps remain visible.

For the CSV project, suppose the command-line interface, parser, importer, and writer already exist and the following behavior has been verified. Part of `docs/architecture.md` could read:

```markdown
### CSV import

- Context: The user supplies a CSV file through the import command.
- Building blocks: The parser supplies fields and source line numbers to
  the importer. The importer applies the agreed validation rules and
  passes valid rows to the writer.
- Runtime behavior: A rejected row produces an error with its source line
  number; processing continues with later rows.
- Constraint: Parsing preserves quoted commas in the required input format.
- Requirements: See [import-format.md](import-format.md) for validation
  rules and the source-line-number convention.
```

This excerpt explains responsibilities and behavior while linking to the detailed requirements. It is a fragment, not a complete architecture document or a required layout; other applicable topics still need coverage. Unverified behavior would need to be identified as such.

### Preserve significant choices and identify debt

A significant lasting choice within the authorized scope requires an [Architecture Decision Record (ADR)](AGENTS.md#33-significant-decisions-adrs) when a concrete proposal is ready for decision or review, in or linked from [arc42's decision section](https://docs.arc42.org/section-9/). Selecting a parser to meet a memory constraint is one possible example. The record retains context, reasons, consequences, and status. Routine local choices normally need none; exploratory ideas alone do not trigger an ADR.

Use Proposed while the choice awaits a decision, Accepted once it is made under existing authority and consultation rules, Rejected for a rejected proposal, and Superseded when a later decision replaces it. Preserve useful history, rejected alternatives, and replacement links. A new consequential architectural or lasting design direction, or a material departure from established direction, needs your direction before adoption or implementation unless the specific choice is already authorized. An ADR or retrospective report cannot supply that permission. Accepted does not mean implemented, and recording creates no extra ADR-specific approval checkpoint.

For example, suppose this CSV project has an agreed memory budget and required input sizes. Assume an evaluation has established that streaming meets its parsing and memory requirements, and the significant design choice has been accepted. A short ADR could read:

> **Title:** Process CSV files as a stream  
> **Status:** Accepted  
> **Context:** Required files can exceed available memory. Evaluation against the agreed input sizes and memory budget supports incremental processing; the project records the requirements and evaluation evidence alongside this decision.  
> **Decision:** Parse and validate rows incrementally to avoid holding the entire file in memory.  
> **Consequences:** The implementation must manage parser state and buffers across rows. Accumulated errors and rules that need information from other rows require their own memory strategy; streaming alone does not bound all memory use.

The assumptions above belong to this illustration. In a real record, link the actual requirements and evidence, preserve useful alternatives and history, and update the status to reflect the actual decision. The memory constraint and lasting implementation consequences explain why this example merits an ADR; an ordinary helper-name choice normally would not.

The agent may record current, task-relevant, evidenced technical debt in the architecture's risks and debt section, including debt discovered during assessment without a fix in scope. It considers accepted requirements and trade-offs, flags uncertain classifications, and tells you what was recorded, why, where, and with what uncertainty. Nonblocking disclosures should normally join the next consolidated report under the [reporting rules](#assess-the-result). A deferred feature, rejected alternative, or different preference alone is not debt. Recording grants no permission to fix it. When in-scope work changes or resolves recorded debt, its records must be updated.

Known risks also belong in that architectural topic and need not be internal-quality compromises. A required external service becoming unavailable can be a risk even when the implementation meets its agreed quality requirements; it need not be classified as technical debt to be recorded.

### Ask for the guide you need

[Diátaxis](https://diataxis.fr/) distinguishes four reader needs: tutorials teach through practice, how-to guides help complete a task, reference supplies facts and interfaces, and explanation develops understanding. “Show an operator how to correct rejected rows and retry an import” identifies a how-to need.

New guides require an explicitly requested or agreed purpose. These methods do not require four documents, an ADR, or a new guide for every increment. Affected existing guides stay current. Comments, docstrings, and generated API documentation should follow suitable existing language and tool conventions.

[DRY](https://media.pragprog.com/titles/tpp20/dry.pdf) keeps knowledge consistent through one authoritative owner. A guide can explain a retry setting and link to its definition; necessary copies need a clear canonical owner and update process. Similar-looking code may express different rules, so resemblance alone does not require abstraction.

See the [knowledge rules](AGENTS.md#35-canonical-knowledge-and-affected-documentation), the [architecture and guide rules](AGENTS.md#36-architecture-guides-and-code-documentation), and the [design reasons for the documentation methods](_internal/CONTRACT-DESIGN.md#documentation-choices).

## Bring an existing project into alignment

Installation establishes standing expectations for subsequent tasks; it does not itself authorize a broader alignment project. The agent must keep affected documentation consistent during authorized work. Broader alignment, audits, backfills, or reorganizations need corresponding authorization, which may already be part of your request.

You can request alignment as a broader goal. The agent identifies a small, useful area to address within that authorization, such as a component or architectural concern. You may name an area if you have a priority. Project requirements, accepted decisions, and implementation supply the evidence; the contract supplies collaboration policy.

For the authorized work, the agent:

1. **Assesses the documentation.** Compare the area's known content with applicable arc42 coverage and expectations for requirements, decisions, and guides. Identify useful material, gaps, contradictions, duplication, and unclear ownership; keep material unknowns visible.
2. **Improves it when authorized.** Preserve an adequate arrangement, express revised requirements with EARS, retain known decision reasons and history, and describe the current system accurately. Label proposed or unfinished changes and complete each increment within scope.
3. **Reviews relevant code.** Use the clarified context and engineering practices to identify concrete issues and explain why changes would help. Review permission alone does not authorize code changes; the [permissions for records and factual documentation corrections](#records-during-review-and-exploration) still apply.
4. **Implements authorized improvements.** Work in small, complete increments with relevant checks and affected documentation. Refactoring preserves observable behavior; intended behavior changes need corresponding authorization.

For example:

> Assess how this project's documentation aligns with AGENTS.md.

This authorizes assessment. After proportionate preliminary context gathering, the agent briefly states the overall assessment direction and the first increment's objective and bounds before substantial work. It can continue through justified, authorized assessment increments without a report for each one, while still giving required inquiry notification and respecting consultation rules. Routine progress reports should be minimized; useful intermediate communication remains possible. It consolidates findings at completion, handoff, or when seeking your input. Assessment permits the [records and verified factual documentation corrections](#records-during-review-and-exploration) described above; other edits need authorization. If you want no file changes, say so explicitly. A request that already authorizes improvements can cover subsequent implementation increments, subject to the consultation and reassessment rules.

An empty project can develop documentation and implementation through useful authorized work. Coverage expectations alone grant no permission for a repository-wide audit or reorganization.

## Tool compatibility

Use the [basic setup](README.md#get-started) to install the supplied files. Loading behavior depends on the product, interface, and settings. The following guidance carries the [recorded evidence dates below](#evidence-dates); consult the provider's current documentation for your environment.

| Tool | Instruction loading and setup |
| --- | --- |
| [OpenAI Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Native `AGENTS.md` discovery, subject to override precedence and the combined instruction limit. |
| [Claude Code](https://code.claude.com/docs/en/memory#agents-md) | The supplied `CLAUDE.md` imports `AGENTS.md`; direct discovery is also available under documented conditions. |
| [GitHub Copilot](https://docs.github.com/en/copilot/reference/custom-instructions-support) | Native `AGENTS.md` support varies by feature. The supplied bridge explicitly directs discovery and application. |
| [ChatGPT Projects](https://learn.chatgpt.com/docs/projects) | Project instructions and shared files or connected context; use the product's documented setup. |
| [Claude Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects) | Project instructions and project knowledge; use the product's documented setup. |

The supplied root bridges keep operating policy in the local `AGENTS.md`. The Claude file imports it; the Copilot file directs reading and application. Actual loading remains dependent on the interface and settings. Neither bridge defines a separate stop/report/resume protocol for loading failures. A contract that was never loaded cannot govern that failure through its own instructions; behavior then depends on the tool and instructions actually available. This is a limitation common to the supplied integrations, not a new fallback policy in this guide. Use the adoption diagnostics below to check loading. The [technical guide](_internal/CONTRACT-DESIGN.md#why-the-bridges-differ) explains the different mechanisms.

### Check adoption

Check whether the tool **finds the file**, **includes its instructions**, and **follows them during a task**. A listed file alone does not show application. Try a representative task and inspect both the result and available diagnostics.

[VS Code's verification guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#_verify-your-instructions) illustrates discovery and application checks. A successful check in one interface does not establish compatibility with another.

If loading, scope, or precedence is uncertain, ask which repository instruction sources were loaded or consulted and what remains unconfirmed. Distinguish files merely inspected from confirmed loading. Once the contract is available, its reporting rule covers tool limits that block instruction loading. That rule cannot establish behavior when the contract itself was never loaded, as explained above.

Planning modes, permissions, approvals, and loading mechanisms belong to the tool. [Codex Goal mode](https://learn.chatgpt.com/use-cases/follow-goals), for example, supports sustained execution toward a verifiable stopping condition. The contract still requires the agent to establish the authorized increment's scope and acceptance checks. Continued execution does not expand authorization or bypass review conditions.

Instruction files cannot guarantee pauses or compliance. Review remains necessary, and native planning, approval, and security controls retain their own rules.

#### Worked adoption check

This example uses the supplied Claude Code bridge. For another interface, use its documented loading diagnostics before trying the same assessment task.

1. **Check loading.** Confirm that root `CLAUDE.md` contains `@AGENTS.md` and that root `AGENTS.md` is present. Start a new Claude Code session in the repository, run `/context`, and look for `CLAUDE.md` under **Memory files**. Anthropic documents the [import mechanism](https://code.claude.com/docs/en/memory#import-additional-files) and this [loading check](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools). If the expected file is absent, investigate the applicable settings and loading guidance before assuming adoption.
2. **Try an assessment.** In a project with a documented setup command and package configuration, ask:

   > Assess whether the setup command in README.md agrees with the project's package configuration.

3. **Inspect the result.** Look for a brief task outline and the first increment's objective and bounds, communicated after proportionate preliminary context gathering and before substantial work. The agent must examine the relevant files, identify evidence supporting agreement or a discrepancy, and disclose material uncertainty or unavailable checks. It may correct a verified factual error in the README and maintain triggered records under the [assessment permissions](#records-during-review-and-exploration); any correction needs validation and reporting. To test assessment without file changes, include an explicit no-edit instruction. If your project has no such setup command, choose an equivalent existing instruction and its authoritative configuration.

The diagnostic supplies evidence about loading; the task supplies a limited observation of behavior. Neither an agent's assurance nor one successful task establishes general compliance across tasks or interfaces.

### Evidence dates

The project's recorded documentation-check dates are:

- **2026-09-25:** Codex and Claude Code discovery and size guidance, plus Copilot and VS Code instruction guidance.
- **2026-09-24:** Projects and Goal mode.
- **2026-10-03:** Claude Code import syntax and the `/context` loading diagnostic used in the worked adoption check. This documentation check does not refresh the other claims or earlier dates above.
- **2026-10-04:** Codex's default combined instruction byte limit, Anthropic's guidance on concise instruction files, and the context cost of Claude Code imports, supporting the [portability rationale](_internal/CONTRACT-DESIGN.md#keeping-the-contract-portable).

These identify the evidence supporting the guidance; they are not cross-tool conformance-test results.
