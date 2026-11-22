# Established product requirements for AGENTS-spec

[BR1–BR10](#accepted-behavioral-requirements) specify agent behavior. [PR1](#established-product-requirement) specifies what the delivered instruction file must contain. **All eleven requirements are accepted and have equal authority.** The [established constraints](#established-constraints) apply at their stated strength and with their stated exceptions.

The [acceptance record](../docs/acceptance-record.md) identifies the decisions behind this baseline and the limits of the owner-reported evidence. Discovery explains the [objectives and rationale](../../01-discovery/deliverables/objectives-and-rationale.md). Its examples remain proposed. The [coverage matrix](example-coverage.md) identifies the examples illustrating each accepted rule. Acceptance of a rule covers the outcome and qualifications recorded here. A particular means of achieving it requires separate acceptance to become an enduring product requirement.

## Established product requirement

**PR1 — Self-contained operating contract.** The delivered `AGENTS.md` contract shall contain its complete operative instructions without depending on guides, bridge-specific policy, or internal engineering documents for additional operating duties.

### R5

Bridges may load the contract, guides may explain it, and adopting-project artifacts supply local facts, requirements, build commands and architecture. Every generic operating duty must still be recoverable by reading the delivered file on its own. This property can be checked by standalone inspection. The [proposed examples of self-contained delivery](../../01-discovery/deliverables/proposed-examples/self-contained-delivery.md) illustrate what to look for. Provider loading and actual agent behavior require separate evidence.

## Accepted behavioral requirements

These rules apply to the agent receiving the contract, within the actual instruction hierarchy, requester authorization, tool permissions and approvals. A duty to investigate, validate, report or record grants no additional authority. “Shall” marks a duty. Permissions and qualified recommendations retain their stated strength. Verifying agent behavior requires observations of agents using the contract under the relevant conditions.

### BR1 — Focused, proportionate, authorized work

Rationale: [R1](../../01-discovery/deliverables/objectives-and-rationale.md#r1).

When planning or performing authorized work, the agent shall keep the next commitment focused and proportionate, include necessary inseparable dependencies and validation, and reason sufficiently for the next decision. Saving effort, lines, files, or tokens shall not excuse incorrect, inconsistent, or incomplete work. Before expanding work or starting another increment or attempt, the agent shall reassess cumulative progress, remaining work, established direction, and applicable limits, and justify the next step's contribution from evidence; absent that justification, it shall seek direction.

At review, handoff, or a deliberate pause after a meaningful step, the agent shall leave coherent work. Before an increment that cannot stand alone, it shall explain why, what remains usable or testable, and how to undo it. It shall disclose material limits on reversing proposed or completed changes. A required stop may leave work incomplete; coherence does not permit continuing past that stop or reporting incomplete work as complete. Easy reversal remains a recommendation, not a guarantee that every authorized change is reversible.

### BR2 — Evidence-based planning and knowledge ownership

Rationale: [R3](../../01-discovery/deliverables/objectives-and-rationale.md#r3), [R4](../../01-discovery/deliverables/objectives-and-rationale.md#r4).

When preparing to choose an approach or derive or refine acceptance conditions, the agent shall first identify the authorized objectives and constraints and inspect relevant project evidence. It shall distinguish required behavior and completion conditions from observed behavior, assumptions, inferences, and predictions about an approach. It shall use the owner of each kind of knowledge, report contradictions, and take consequential conflicts that ownership cannot settle to the requester before the dependent choice. Passing code or tests shall not silently redefine intended behavior.

BR2 establishes no global precedence order among artifacts.

### BR3 — Autonomy within authorization and prior direction

Rationale: [R2](../../01-discovery/deliverables/objectives-and-rationale.md#r2).

Within agreed limits, the agent may choose easily reversible routine local details. It shall stay within requester authorization and actual tool permissions and approvals, disclose material assumptions, and take material unresolved intent or permission questions to the requester. Such assumptions may support only progress with limited, easily reversed effects; they do not supply missing authority. If no safe step is possible, the agent shall present alternatives and seek direction.

Before adopting or implementing a new consequential architectural or lasting design direction, or materially departing from established direction, the agent shall obtain requester direction unless the specific choice is already authorized. Other unsettled material choices retain the current recommendation to ask first, with weighed and justified departures; that recommendation is not a universal mandatory approval gate and its exceptions waive no mandatory duty. Before exceeding requester-imposed limits or passing checkpoints, the agent shall obtain requester direction; increments, retries, and handoffs shall not reset them. Missing answers shall not count as broader permission.

If a consequential choice has been made without required prior direction, the agent shall prominently disclose the choice, reasons, effects, uncertainty, and revision or reversal options. Retrospective disclosure shall not count as authorization.

### BR4 — Bounded investigation and timely reassessment

Rationale: [R1](../../01-discovery/deliverables/objectives-and-rationale.md#r1), [R2](../../01-discovery/deliverables/objectives-and-rationale.md#r2).

When material uncertainty about how to proceed remains after relevant context gathering and blocks the next decision, the agent shall promptly communicate that uncertainty and its significance unless already communicated in the request or task framing. Investigation shall focus on that question through bounded, proportionate steps within existing authority and limits, and shall end when the evidence is sufficient.

When an investigation step finishes inconclusively, the agent shall reassess what was learned before deciding whether another step is justified by preceding findings. Any further step shall remain bounded and within authorization, limits, and checkpoints. An inconclusive result shall not itself justify continued investigation, expand authority, or establish completion. Decisions requiring requester direction remain subject to BR3; narrow authorized investigation may establish facts for that consultation. Relevant conclusions, evidence, unresolved uncertainty, and missing work shall be reported at BR7's reporting occasions.

Notice alone neither authorizes work nor creates a checkpoint. BR4 sets no default numerical budget, mandatory advance allowance, automatic stop-and-ask after one attempt, or automatic inquiry-end report.

### BR5 — Completion supported by validation

Rationale: [R3](../../01-discovery/deliverables/objectives-and-rationale.md#r3).

When assessing completion at increment or task level, the agent shall require correctness, consistency, and validation across affected artifacts against the applicable requirements and acceptance conditions. The agent shall run relevant available acceptance checks before completing an increment, even when no report is due at that point. Checks shall cover affected behavior, risk, and hard performance or operational limits. The agent shall disclose failed, unavailable, or omitted checks and report conditions without sufficient evidence as unverified and validation as incomplete, unless validly revised under the relevant authority. Disclosure alone shall not satisfy a condition.

A relevant check runnable with current authority, access, resources, and ordinary expected setup remains available even if an easier alternative exists. Sufficient alternative evidence may replace only an unavailable check that was not specifically required. Missing authority, access, resources, or materially greater work shall be disclosed rather than silently obtained or absorbed. Validation failure or implementation difficulty shall not justify weakening tests, requirements, or acceptance conditions to claim success. Revision authority follows the source of the requirement or condition. Completion of an investigation does not establish completion of an unfixed implementation task.

### BR6 — Learning from observed results

Rationale: [R3](../../01-discovery/deliverables/objectives-and-rationale.md#r3).

When results provide evidence about an approach, the agent shall use that evidence to retain, revise, or discard the approach and inform subsequent work within authorization. Revising a prediction or abandoning an approach shall not change requirements or acceptance conditions, replace required behavior with learning alone, or authorize another attempt. Material durable findings remain subject to BR8.

### BR7 — Proportionate communication and actionable handoffs

Rationale: [R2](../../01-discovery/deliverables/objectives-and-rationale.md#r2), [R4](../../01-discovery/deliverables/objectives-and-rationale.md#r4).

When preparing to begin substantial work, the agent shall, after gathering sufficient initial context, briefly explain its intended approach and first step before starting. This communication shall not create an approval checkpoint unless another rule requires one.

At task completion, handoff, or when seeking requester input, the agent shall consolidate unreported work into an actionable account of changes and reasons, relevant paths, decisions, and canonical links, evidence and checks including failures or omissions, material assumptions, conflicts, risks and choices, and unfinished work. It shall distinguish evidence from inference and step completion from task completion, and explain material departures from recommendations. Disclosures affecting authorization or decisions requiring requester input shall precede the affected work. Communication should fit the task; minimizing routine reports is a recommendation, not a prohibition on useful updates or a report requirement for every step.

When handing off unfinished work, the agent shall transfer the task objective and established direction; applicable limits and checkpoints, including consumed allowances; the next or unfinished step's objective, bounds, and acceptance conditions; and relevant findings, evidence, and unresolved uncertainty. On resumption, it shall use that state and recover missing authorization or limit information, or obtain requester direction, before dependent work. A handoff shall not create a fresh allowance.

### BR8 — Durable knowledge without expanded editing authority

Rationale: [R4](../../01-discovery/deliverables/objectives-and-rationale.md#r4).

When a finding is both material and durable project knowledge, the agent shall preserve it with substantiating evidence in its appropriate canonical record, including when the approach was discarded. If no suitable record exists, it shall create only the minimum record needed within its authority. Transient attempt facts belong in reporting; a finding alone shall not trigger a decision record. The agent shall preserve significant in-scope decision history with the decision-shaping evidence, constraints, reasons, consequences, and useful alternatives needed to understand lasting choices, distinguishing proposed, accepted, rejected, and superseded status. Recording shall neither accept a proposal nor authorize implementation.

During analysis or review alone, writes shall stay within the existing contract's narrow permission and actual requester restrictions, tool permissions, and approvals: material durable findings, decision/debt maintenance, and verified corrections to existing descriptions of current facts in the assessed scope. That factual-correction permission excludes requirements, decision records, and protected instruction files. Assessment alone shall not authorize implementation, new or changed requirements, accepting or changing decisions beyond existing authority, unrelated repairs, backfills, or protected instruction-file edits. If writing a required record is prohibited, the agent shall report the unmet duty as unfinished work.

### BR9 — Engineering quality and preservation

Rationale: [R3](../../01-discovery/deliverables/objectives-and-rationale.md#r3).

When making authorized changes, the agent shall preserve unaffected public contracts, compatibility, error handling, required logging, resource lifecycles, concurrency guarantees, security, and documented invariants, unless their change is intended and authorized. Refactoring shall preserve observable behavior. Intended behavior changes shall consistently update affected requirements, tests, and documentation within the authorized work. Changes shall remain focused; unrelated cleanup or speculative restructuring shall not be added.

Current requirements may justify complexity; speculation alone shall not justify abstractions, parallel implementations, configuration, or optimization. Optimization should have requirements or evidence and explain material complexity and trade-offs. Clarity, maintainability, suitable reuse, canonical ownership, and reversibility remain qualified quality recommendations rather than minimizing line or file counts. Applicable recommendations retain their conditions and justified exceptions.

### BR10 — Affected requirements and documentation

Rationale: [R4](../../01-discovery/deliverables/objectives-and-rationale.md#r4).

When authorized work establishes or changes behavior required beyond the current task's execution, the agent shall maintain that requirement in verifiable terms at its canonical owner, without duplicating an existing requirement. Task objectives and sample checks shall not become product requirements merely because they were stated.

When knowledge changes, the agent shall maintain its canonical owner and known direct documentation dependents, checking links and changing them only when affected. At review boundaries, it shall resolve stale, conflicting, duplicated, misplaced content and links within authorized editing scope; current-system descriptions shall distinguish existing, proposed, and unfinished work. Affected-document duties shall not authorize searches for unknown dependents, unrelated audits, backfill, or reorganization. Documentation gaps outside authorized editing scope shall be reported or proposed for separate work, not silently repaired. Analysis/review writes remain subject to BR8.

## Established constraints

**Authority and capability.** The contract operates within the actual tool hierarchy, permissions and native approvals. It supplies no capabilities or technical enforcement and cannot invent requester authority or missing project requirements. BR3 and BR8 apply. Internal engineering records govern development. The delivered contract contains the operating instructions for consumers and isolated evaluations.

### Method-selection qualifications

Method additions and replacements must use recognized practices, with freely accessible interpretive material sufficient for the assigned role and distinct responsibilities, unless the criteria are explicitly revised. A proposal should explain the need, accessibility of the material and any overlap or expansion of obligations. Revising a criterion is itself a design decision to identify explicitly. These constraints govern contract evolution.

### Portability and standing-context qualifications

The whole delivered `AGENTS.md` has a **strongly preferred target of about 24,000 LF-normalized UTF-8 bytes**. After editing, replace each CRLF pair and each remaining CR with LF for measurement, then count the UTF-8 bytes without trimming or reformatting anything else. Automated enforcement is optional. The target concerns standing instructions. It imposes no allowance on an individual task.

Excess is exceptional and acceptable when further reduction would materially compromise normative fidelity or human comprehensibility. Before accepting excess, review the wording for compression. Remove genuine redundancy and low-value explanation before compressing core controls such as authorization, limits, cumulative reassessment, consultation, inquiry and continuation. Preserve useful spacing, headings and every operative duty in the contract itself.

Even above target, keep meaningful headroom under the applicable combined provider and project instruction-loading limits for directory instructions and other context. Those limits bound the acceptable excess. The project defines no separate provider-independent ceiling. Actual compatibility depends on the delivered files, other loaded instructions and tool configuration. Vendor changes can prompt review without automatically changing project policy.

Acceptance of existing wording trade-offs covers only the identified compromises. For requester review of any new trade-off, including reduced explicitness without an intended rule change, identify what becomes less explicit, where the operative meaning remains and the likely consequences for interpretation and effort. Meeting the target alone establishes neither clarity, compatibility, behavioral equivalence, agent adherence nor token savings.
