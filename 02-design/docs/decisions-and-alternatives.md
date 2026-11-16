# Decisions and alternatives

Current choices and superseded controls are distinguished below. [Shared authority](../../docs/authority-and-change.md#status-and-evidence-boundaries) defines their status; the [clause index](../deliverables/contract-design.md#current-semantics-vocabulary-and-coverage) relates mechanisms to accepted intent. Engineering-system and evaluator decisions remain in [engineering history](../../docs/architecture.md#decisions) and [framework design](../../04-evaluations/docs/framework-design.md#engineering-decisions).

## Architecture Decisions

### Selected design and retained decisions

The index points to canonical reasons and consequences without turning every explanation into an ADR or product requirement.

| Choice | Status and rationale |
| --- | --- |
| Work cycle, progression guards, triggered rules | **Selected current design.** [Layer composition](../deliverables/contract-design.md#three-interacting-layers) explains cross-phase applicability and why phase placement must not confine duties. No permanent three-layer requirement or measured benefit is claimed. |
| Bounded commitments, PDSA, focused practices | **Selected current design; recorded as sufficient for the agreed design.** [Method selection](../deliverables/methods-and-references.md#choosing-or-replacing-methods) explains complementary responsibilities without additional umbrella frameworks; replacement remains possible under selection constraints. |
| Role-specific knowledge ownership | **Selected current design; total ordering rejected/superseded.** [Documentation choices](../deliverables/mechanisms/knowledge-and-documentation.md#documentation-choices) explains why different knowledge owners cannot share one precedence ladder and how unresolved conflicts are handled. |
| Provider-specific bridges | **Selected integration design.** [Bridge rationale](../deliverables/delivery-and-portability.md#why-the-bridges-differ) distinguishes import from read/follow, preserves provenance, and explains provider limits and the absence of common bootstrap policy. |
| Qualified size target and compact wording | **Retained established constraint; identified wording compromises recorded as accepted.** [Portability qualifications](../../01-behavior/deliverables/baseline.md#portability-and-standing-context-qualifications) and [wording trade-offs](../deliverables/delivery-and-portability.md#current-wording-trade-offs) retain exception/review conditions and acceptance limited to those compromises. |
| Effort baselines, mandatory inquiry framing, routine-report suppression | **Historical/superseded.** The records below retain useful control/visibility rationale and identify current replacements. |

### Historical source and interpretation

The historical source is [`README-maintainers.md` at `9a078b3`](https://github.com/indisoluble/AGENTS-spec/blob/9a078b3833297ca33357391bb60e6d469bceeff4/README-maintainers.md); accepted-contract alignment and later moves include [`c4bc519`](https://github.com/indisoluble/AGENTS-spec/commit/c4bc51938ef7a4890f1f353e46e764f226c3b42f) and [`96947a8`](https://github.com/indisoluble/AGENTS-spec/commit/96947a8a8644e744525c0209dcc2a5b290f3589f). These are repository provenance, not fresh external-source verification or detailed product acceptance. Historical mechanisms below have no current operative force; linked mechanism documents own present interpretation.

### Superseded effort-baseline checkpoint

**Mechanism and reason.** The PDSA version kept an increment baseline at planning and a cumulative-task baseline at task start, using requester direction or otherwise agent judgment without routine notification. Baselines could be qualitative working state, not quotas or required records. New estimates did not replace the comparison points. Material growth required reassessment, disclosure of changes, unfinished work and uncertainty, and the smallest useful complete next step, followed by requester direction before added effort—even within unchanged broad scope.

Only requester direction could revise baselines. Approval covered only disclosed growth, avoiding repeated consultation while keeping later growth detectable. New increments could not absorb unapproved growth; attempts/handoffs could not reset the task baseline. Handoffs transferred relevant baseline/revision state; missing state required recovery or direction before effort-bearing continuation.

The mechanism aimed to catch unexpectedly heavy work within one increment and cumulative growth across small additions. It required judgment about qualitative estimates and material growth, with no automatic enforcement. A larger shared-parser redesign in the historical CSV example therefore triggered the checkpoint in any phase.

**Replacement.** [Current authorization/limits](../deliverables/mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions) uses requester-imposed limits, evidence-based cumulative reassessment, and consequential consultation. §2.3 requires neither agent-created baselines nor consultation solely because an agent estimate grows. Old baseline state and automatic material-growth checkpoints are not current handoff/continuation duties.

### Superseded inquiry announcement and stopping rule

**Mechanism and trade-off.** Beyond exempt context gathering, starting/continuing inquiry required advance question, scope, objective, effort limit, and needed evidence. The agent could choose a bound without approval of every limit; there was no default unit, amount, or formula. Sufficient evidence or the declared limit ended that inquiry, even inconclusively, followed by a report of unmet conditions, missing evidence, uncertainty, and broader research/design needs. The report was not an approval checkpoint.

Existing authorization could cover a newly framed attempt, subject to caps, checkpoints, safe continuation, consequential intent, and the historical growth rule. Exhaustion/negative findings granted no authority. Advance declarations exposed commitment but supplied no tool-enforced timeout or quota. Context gathering, including existing-document reading for a blocking question, remained exempt from framing while subject to scope/effort controls.

**Replacement.** [Current inquiry](../deliverables/mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation) retains purpose-based classification and adds timely uncertainty/significance notification unless already communicated. It requires bounded conduct without the five-element announcement or declared allowance. Sufficient evidence ends inquiry; insufficient evidence at bounds requires reassessment before justified continuation. There is no automatic inquiry-end report or announcement per attempt; requester limits remain binding. Removing framing proves neither equivalent behavior nor improved efficiency.

### Superseded report suppression and consultation strength

**Historical reporting.** Routine report drafting/output was prohibited unless requested or required, aiming to avoid effort preparing narration only to withhold it. Reports consolidated work at completion, handoff, or input requests, with advance decision/authorization disclosures and an inquiry-end report. Other disclosures had to join the next report unless earlier timing was explicit; records retained independent timing. The cost was less routine visibility, without measured savings or a reserved review opportunity.

**Replacement.** [Current reporting](../deliverables/mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) recommends minimizing routine reports and keeping updates concise/useful. Consolidation, initial framing, inquiry notification, and advance disclosures retain mandatory timings. Useful updates remain possible; the categorical ban and inquiry-end timing are superseded.

**Consultation strength.** Historically, asking before unsettled consequential choices was a SHOULD, alongside mandatory unresolved-intent/permission and baseline-growth controls. The [current decision guard](../deliverables/mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions) requires prior direction for new consequential architectural/lasting direction or material departure unless specifically authorized; other unsettled material choices retain SHOULD. Historical strength cannot replace current modality. Neither design permits reports/ADRs to authorize retrospectively.

### Superseded method-reference inquiry exemption

Historically, narrow clarification of material method ambiguity was exempt from §2.4 framing, while ambiguity/source/interpretation disclosure and no imported obligations kept links from becoming full research assignments.

[Current reference boundaries](../deliverables/methods-and-references.md#principles-and-reference-boundaries) retain narrow consultation without imported rules, but qualifying consultation follows purpose-based context/inquiry classification and notification/conduct duties, including the already-communicated exception. Clear rules must not be researched; broader research needs explanation and requester direction. The blanket exemption is superseded.

### Contract-design documentation extraction (15 November 2026)

**Status and provenance.** The requester approved the split and local implementation against [`13cb028`](https://github.com/indisoluble/AGENTS-spec/commit/13cb028aa9c61a4ed808b55d2ffe0a314b9f98c7). A [later navigation assignment](../../docs/engineering-history.md#shared-engineering-documentation-extraction-15-november-2026) records that migration as complete and independently reviewed and removes the original compatibility-forwarding requirement. This records the earlier migration, not acceptance of subsequent edits.

**Decision and rationale.** Separate the architecture entry point, four mechanism owners, delivery/portability, methods/references, and decision history, keeping prescriptions with necessary explanations. One file would reduce links but mix distinct reading/maintenance tasks; the split lets maintainers reach one canonical explanation directly at the cost of maintaining cross-references. [Design review](design-review.md) remains the owner of editorial guidance and non-normative illustrations.

The split refines the [BDD-first organization](../../docs/engineering-history.md#bdd-first-reorganization-13-november-2026); the [numbered-pipeline successor](../../docs/engineering-history.md#numbered-pipeline-and-documentation-ownership-15-november-2026) establishes stage placement. These structural decisions preserve substantive responsibilities and decision statuses without changing requirements, runtime semantics, evaluation expectations, or consumer dependencies. Full migration chronology remains in Git history.
