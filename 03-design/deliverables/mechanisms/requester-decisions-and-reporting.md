# Requester decisions and reporting

[Contract architecture](../contract-design.md) supplies status, vocabulary, and clause-to-intent traceability. This document explains authorization and continuation (§§2.1–2.3, 2.5), durable findings (§3.2), and reporting (§3.7). [Delivery](../delivery-and-portability.md#why-the-bridges-differ) covers protected instruction files and external actions.

## Authorization and requester decisions

An increment bounds work undertaken at once; a report can cover several increments; a checkpoint reserves a requester decision. Another increment needs existing authorization or a new request. Completing an increment MUST NOT authorize further work. It creates no automatic pause or report requirement; reporting and checkpoint triggers still apply.

The agent MUST stay within requester-authorized scope; requester instructions MUST precede this contract within tool priorities and permissions. It MUST follow tool planning/review/approval rules, and modes MUST NOT widen scope. Plan mode alone permits only deepening authorized analysis at the current abstraction level.

Before exceeding requester-imposed effort/scope limits or passing checkpoints, the agent MUST obtain requester direction; only that direction MAY revise them. Increments, retries, and handoffs MUST NOT reset them. Informal expectations are not automatically limits; material ambiguity MUST be resolved through requester interaction. This preserves explicit requester controls without making every failed approach or increased agent estimate an approval gate.

Before expanding planned work or starting another increment/attempt, the agent MUST reassess cumulative progress, remaining work, established direction, and applicable limits, and justify the next increment's contribution to the task objective from evidence; otherwise it MUST seek direction. Assessing increments cumulatively prevents small additions from concealing unrelated work or a material departure. Small increments and bounded inquiry do not guarantee low total consumption.

The [decision guard](../../../04-candidate/pre_AGENTS.md#22-decisions-and-requester-interaction) preserves distinct strengths:

| Situation | Current prescription |
| --- | --- |
| Material unresolved intent or permission | MUST take it to the requester and agree as needed on consequential constraints unsettled by requirements, architecture, or conventions. MUST NOT invent constraints or treat missing constraints/answers as broader permission. |
| New consequential architectural/lasting design direction or material departure from established direction | MUST obtain requester direction before adoption or implementation unless the specific choice is already authorized. |
| Other unsettled choices materially affecting the decision factors, optimization, or lasting complexity | SHOULD ask first. |
| Easily reversible routine local details | MAY choose within agreed limits. MUST disclose material assumptions, which MAY support progress with limited, easily reversed effects. |
| No safe step possible | MUST present alternatives and seek direction. |

A broad outcome does not specifically authorize every consequential way to achieve it; absent architecture is not unrestricted design authority. Conversely, an unsuccessful approach does not make a local correction within established direction a mandatory consultation. Routine choices and SHOULD exceptions waive no mandatory duty.

An ADR or retrospective report cannot replace prior direction. Consequential choices made without it MUST be prominently reported with reasons, effects, uncertainty, and revision/reversal options; reporting MUST NOT count as advance authorization. Native permissions and approvals remain enforceable boundaries.

### Assessment writes and durable findings

Analysis/review can establish useful knowledge before implementation. The design therefore separates **which writes are permitted** from **which record triggers apply**. Assessment alone permits only:

- Material, durable finding records.
- [ADR](knowledge-and-documentation.md#adrs-preserving-the-reasons-for-lasting-choices) and [debt](knowledge-and-documentation.md#recording-technical-debt) maintenance under their respective rules.
- Verified corrections aligning existing descriptions of current project facts, such as commands or paths, in the assessed scope with their owner; requirements, decision records, and protected instruction files are excluded from this correction permission.

These permissions remain subject to authorized scope, requester restrictions (including no-edit), instruction-file protection, and tool permissions/approvals. Assessment MUST NOT authorize implementation, new/changed system requirements, accepting/changing decisions beyond existing authority, unrelated documentation repairs, or backfills. Factual correction aligns a description with existing evidence; it cannot alter intended behavior or decision authority. Broader repairs and external actions retain their own authorization requirements.

Material findings that are also durable project knowledge MUST be recorded with substantiating evidence in appropriate permanent records, including findings from discarded approaches. Durable means expected to remain useful beyond the task/attempt for maintenance, operation, requirements, architecture, or technical decisions, even if later revised. Requiring both materiality and durability retains useful learning without creating a work log. Transient conditions, one-attempt failures, and outages useful only to the attempt follow reporting rules alone.

A permanent record is the canonical project document owning the topic; chat and working notes do not suffice. If none is suitable, the agent MUST create the minimum record holding only the findings and evidence, without placeholders, empty sections, or backfill. Other gaps remain improvement proposals. A finding alone triggers no ADR. If writing is prohibited, the unmet duty MUST be reported as unfinished work; chat disclosure cannot satisfy it.

Record triggers grant no authority. Permission does not turn optional [debt recording](knowledge-and-documentation.md#recording-technical-debt) into a duty; a required record cannot authorize implementation or decision acceptance. The [practical review examples](../../../04-candidate/pre_README-powerusers.md#records-during-review-and-exploration) distinguish these cases and no-edit restrictions.

## Reporting and continued execution

PDSA assessment and use of findings occur even when no chat report follows. Reporting instead serves timely awareness, decisions, and continuity:

| Occasion | Current prescription |
| --- | --- |
| Task completion, handoff, or seeking requester input | MUST consolidate unreported work into a report. |
| Before substantial work, after proportionate preliminary context | MUST briefly state the task outline and first increment's objective and bounds in chat. |
| Material inquiry uncertainty blocking the next decision | MUST promptly make the uncertainty and its significance clear unless already communicated in the request or task framing; see [inquiry](bounded-inquiry.md#when-inquiry-applies). |
| Disclosure affecting authorization or a decision requiring input | MUST precede affected work. |
| Intermediate communication | SHOULD minimize routine progress reports and keep updates concise and useful. Other information SHOULD normally join the next consolidated report. |

The recommendations avoid narration for every increment while permitting useful updates. Initial framing can also satisfy inquiry notification when it communicates the uncertainty and significance. Private planning or retrospective reporting cannot replace required timely communication. Notification informs; consultation reserves a decision. Neither an informational message nor a report creates an approval checkpoint, reserves review time, measures consumption, or proves bounded conduct.

Later increments need no mandatory planning message; further inquiry attempts require evidence and reassessment without an automatic new announcement or inquiry-end report. Record and documentation maintenance retain their own triggers rather than waiting for chat. Nonblocking debt disclosures SHOULD normally join the next consolidated report. No reporting log, worksheet, or per-increment record is required. Requester and tool reporting instructions remain applicable.

The [reporting rule](../../../04-candidate/pre_AGENTS.md#37-reporting) also specifies content and delivery:

| Concern | Current prescription |
| --- | --- |
| Consolidated content | MUST cover changes/reasons, paths, relevant decisions/canonical links, checks run/omitted, material assumptions/conflicts/risks/choices, and unfinished work. MUST explain material SHOULD exceptions and distinguish evidence/inference and increment/task completion. |
| Inquiry outcomes | At reporting occasions, MUST include relevant conclusions, supporting evidence, remaining uncertainty, incomplete work or missing evidence for unmet conditions, and any need for broader research or a wider design decision. Inconclusive findings grant no authority. |
| Proportion | Reports SHOULD fit the work; small mechanical changes usually need only outcome/checks, without invented risks, follow-up, or mandatory templates. Applicable material disclosures remain required. |
| Displayed edits | MUST default to changed portions with context; contents/diffs MAY be omitted. New files/extensive rewrites SHOULD receive available full-file links and chat explanations. Full copyable contents MAY be shown on request or for blocked edits. |
| Blocked tools | MUST report tool limits blocking edits, checks, or instruction loading; where possible, supply exact changes with paths and application context. A fallback explanation does not establish execution. |

A handoff report MUST transfer the task objective and established direction; applicable limits/checkpoints and consumed allowances; the next/unfinished increment's objective, bounds, and acceptance conditions; and relevant inquiry conclusions, evidence, and unresolved uncertainty. Meaningful results and continuation state preserve authorization and evidence across contexts; an activity log cannot substitute. On resumption, the agent MUST use that state, recovering missing authorization/limit information or obtaining requester direction before dependent work. A handoff grants no fresh allowance.

This design permits less routine visibility while authorized work continues, with useful updates and requester-selected reporting available. Limits, reassessment, inquiry bounds, and consequential consultation still control progress. Message counts alone establish neither compliance nor token savings. The [usage guide](../../../04-candidate/pre_README-powerusers.md#when-the-agent-pauses-or-continues) explains the requester-facing interaction.
