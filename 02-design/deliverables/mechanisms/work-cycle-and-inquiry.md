# Work cycle and inquiry

[Contract architecture](../contract-design.md) supplies status, vocabulary, and clause-to-intent traceability. This document explains contract §§1.1, 1.3–1.4, and 2.4, with the planning and quality constraints of §§2.2–2.3.

## Small commitments with sufficient depth

The requester supplies goals, permission, and relevant constraints; the agent supplies decomposition, acceptance conditions, planning, validation, reassessment, and recognition of required consultation. An outcome-oriented request can therefore start useful work without continuous supervision. The requester may still select a step or add checkpoints.

From the request and project evidence, the agent MUST define the next increment's **objective**, **acceptance conditions**, **approach**, and **prediction** (expected approach/experiment result). It MUST identify task/increment objectives, permitted work, constraints, current abstraction level (for example, architecture or function), and requirements or conditions already set by the requester or authoritative project sources. Before choosing an approach or deriving/refining conditions, it MUST inspect relevant code/callers, tests, configuration, and canonical documentation. This ordering prevents self-selected completion criteria from preceding their evidence.

Work MUST stay within the authorized increment, defaulting to the smallest useful next one, including in planning/approval workflows. Increments and subdivisions MUST address one concern unless others are inseparable. Scope includes affected artifacts, dependencies, and checks. Evidence, enabling infrastructure, or migration groundwork can be useful results as well as functionality.

For the next decision, the agent MUST assess:

| Factor | Assessment |
| --- | --- |
| Scope | Necessary versus authorized work, including affected behavior, artifacts, dependencies, and boundaries. |
| Uncertainty | Missing or conflicting evidence affecting approach or acceptance. |
| Consequence | Effects on core/public behavior, architecture, compatibility, security, data, operations, cost, and future options. |
| Reversibility | Restoration difficulty, including migrations and external effects. |

A few changed lines can affect many callers or an irreversible migration. Understood, narrow, low-impact, easily reversible changes SHOULD receive brief inspection, action, and validation without unnecessary plans or records. The factors require neither a numeric score nor an exhaustive ranking or detailed backlog: those would enlarge the initial planning commitment without necessarily improving the next decision.

The agent MUST reason enough for that decision at the current abstraction level, keeping later work at outline level. Detail MUST reflect uncertainty, consequence, risk, reversibility, and how soon work starts. Architecture analysis may need careful boundaries, alternatives, and risks without specifying future APIs. Explicit authorization can cover broader analysis at that level. A limited experiment or implementation SHOULD replace speculation when it gives better evidence.

At review boundaries—review, handoff, or deliberate pause after a meaningful step—work MUST be coherent. Before an increment that cannot stand alone, the agent MUST explain why, what stays usable/testable, and how to undo it. Changes SHOULD be easy to undo, minimizing irreversible effects and preparing recovery or harm mitigation; material limits on undoing proposed/completed changes MUST be reported. Recovery reduces the cost of mistakes without authorizing destructive effects. Required stops MAY leave work incomplete; coherence cannot justify continuing past them or claiming completion.

Correctness, completeness, consistency, and adequate reasoning, implementation, and validation MUST precede saving lines, files, or tokens/context. Among workable solutions, clarity, canonical ownership, and reversibility SHOULD precede fewer parts. Small scope cannot excuse shallow reasoning or omitted dependencies. [Cumulative reassessment and requester limits](requester-decisions-and-reporting.md#authorization-and-requester-decisions) constrain expansion and repeated attempts.

## Learning throughout the work

The [Deming Institute's PDSA account](https://deming.org/explore/pdsa/) connects an approach and prediction with observation and the next decision. Increments bound commitments; PDSA uses their results to assess the approach and choose what follows. Passing tests alone does not supply that learning: the implications must inform subsequent work.

The agent MUST apply PDSA proportionally to implementation, investigation, and documentation: **Plan** the next small authorized increment from context and objectives; **Do** it; **Study** completion and observations; **Act** to retain, revise, or discard the approach and retain learning for Plan. Act applies triggered record rules and follows the [composition outcomes](../contract-design.md#three-interacting-layers). Results can reshape later detail without changing requirements or granting authority.

Methods appear near their principal contribution but apply whenever relevant. Tests can be planned before implementation, and records maintained as facts emerge. Phases may overlap or repeat; methods alone require no deliverable. Routine work needs no worksheet, formal experiment, special mode, or phase reports. PDSA's Plan organizes reasoning; a tool's Plan mode has its own procedures. Neither widens authorization.

## Completion, predictions, and bounded investigation

The contract separates three questions:

| Concept | Question | Response to contrary evidence |
| --- | --- | --- |
| System requirement | What behavior must the system provide beyond this task's execution? | Assess whether required behavior is unmet; changing it still needs the relevant authority. |
| Acceptance condition | What observable result completes this increment? | Missing evidence leaves completion unestablished; revision follows its source and authority. |
| Prediction | What result is expected from the approach or experiment? | Retain, revise, or discard the approach; changing a prediction changes neither requirements nor acceptance conditions. |

Study compares results with acceptance conditions for completion and observations with predictions for learning. Learning cannot replace required in-scope behavior; an implementation may meet its conditions through a different approach from the one predicted. An approach can fail while an investigation succeeds: evidence that a reader splits a quoted comma can answer the investigation, while required intact-field behavior remains unimplemented. A successful sample supports only conclusions justified by that sample. See [validation](engineering-and-validation.md#validation-and-test-evidence) for check availability, evidence sufficiency, and revision authority.

Authorized work establishing or changing behavior required beyond the task's execution creates a new/revised system requirement, whatever its source. It needs a canonical owner and [EARS form](knowledge-and-documentation.md#ears-making-required-behavior-explicit). Task objectives, acceptance conditions, and requester statements do not become requirements merely by being stated; restating an owned requirement MUST NOT create a duplicate. Analysis/review alone cannot create or change requirements.

**Context versus inquiry.** Inspecting relevant code, callers, tests, configuration, and directly related dependencies to establish context, and *all reading of existing project documentation*, are context gathering—even for a material blocking question. No inspection-by-inspection announcement is needed. Scope, limits, proportionality, and cumulative reassessment still apply.

Beyond context gathering, [§2.4 inquiry](../../../03-contract/prerelease_AGENTS.md#24-context-gathering-and-bounded-inquiry) means investigating material uncertainty about how to proceed that blocks the next decision. Purpose distinguishes inquiry from settled execution and validation: unknown output alone does not trigger inquiry, and using a prescribed procedure does not exempt an investigation. The same measurement or test can serve any of these purposes.

The agent MUST promptly make the blocking uncertainty and its significance clear unless already communicated in the request or task framing. This supplies timely awareness without duplicate messages, a five-element announcement, an advance estimate, or a declared allowance. It neither grants authority nor creates an approval checkpoint. [Initial framing and reporting](requester-decisions-and-reporting.md#reporting-and-continued-execution) retain their separate timings.

Inquiry MUST focus on the blocking question through small, bounded, proportionate increments and end when evidence is sufficient. Sufficiency and bounds prevent different failures: treating any output as an answer, and continuing simply because the answer is unknown. At increment bounds with insufficient evidence, the agent MUST reassess before further investigation. Further attempts MUST be justified by preceding findings and remain within authorization, limits, and checkpoints. No numeric budget is required; announced bounds cannot substitute for disciplined conduct. The [practical example's](../../../03-contract/prerelease_README-powerusers.md#when-an-investigation-is-needed) single sample illustrates a bounded experiment; its optional one-attempt checkpoint is a separate requester control. An inconclusive result alone establishes neither completion nor additional authority.

Narrow authorized investigation MAY establish facts for consultation. If it exposes a decision requiring requester direction, consultation MUST precede adoption or implementation. Without evidence justifying the next increment, the agent MUST seek direction. Inquiry outcomes are reported at completion, handoff, or input requests; there is no automatic inquiry-end report or new announcement per attempt. The [superseded announcement rule](../../docs/decisions-and-alternatives.md#superseded-inquiry-announcement-and-stopping-rule) explains the replaced mechanism. Wording changes alone establish no behavioral equivalence or token-efficiency result.

## Runtime View

### How the design works in a task

The [practical CSV walkthrough](../../../03-contract/prerelease_README-powerusers.md#from-a-request-to-a-result) owns the scenario facts: report invalid rows and continue with valid ones. This technical view explains how evidence selects a step and how the layers interact.

1. **Plan:** establish the objective and permitted work, then inspect context. Suppose requirements settle the format, invalid-row rules, and line numbers; existing tests support the reader; and inspection exposes missing field-count validation at a row boundary providing fields, header, and line number.

   Select field-count validation: it advances an agreed requirement, addresses one concern, and offers a useful, testable result without implementing every invalid-row rule. Include affected code, tests, and documentation. Limited dependencies and expected reversibility support the scope without replacing validation.

   Define acceptance conditions: reject mismatched rows, report their line numbers, and continue with valid rows, including one after a rejection. Predict that the existing row boundary supports the approach. These derived conditions are not new requirements. Refine selection, scope, conditions, and approach together within authority; keep later work at outline level. After preliminary context, briefly communicate the task outline and first increment's objective and bounds before substantial work, without creating an approval checkpoint.
2. **Do:** implement using project conventions and Simple Design, with relevant tests and canonical documentation updates. Significant lasting proposals need ADRs; required requester direction precedes adoption or implementation.
3. **Study:** run relevant available acceptance checks before completing the increment, including continuation after rejection. Separately assess whether the predicted local approach sufficed. Disclose failed, unavailable, or omitted checks under the reporting rules.
4. **Act:** use findings to retain, revise, or discard the approach within authority. Record material durable findings; transient attempt facts follow reporting rules. Then complete, hand off, seek required direction, or plan another already-authorized increment under the [composition rules](../contract-design.md#three-interacting-layers).

Different evidence changes the path. Unsettled consequential requirements require requester input; uncertainty about the reader may require inquiry. A routine local correction can proceed within established direction and limits; changing the shared parser's error contract requires prior direction unless specifically authorized. Findings can inform another validation increment without a routine report. Consolidate unreported work at completion, handoff, or input requests. A requested operator guide could be a later increment shaped by its reader's need; neither a completed step nor a named method automatically creates a guide, ADR, or approval requirement.
