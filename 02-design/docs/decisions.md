# Contract design decisions and alternatives

Current choices and superseded controls are distinguished below. [Shared authority](../../docs/authority-and-change.md#status-and-evidence-boundaries) defines their status; the [clause index](../deliverables/contract-design.md#contract-clause-index) relates mechanisms to accepted intent. Engineering-system and evaluator decisions remain in [system-wide engineering decisions](../../docs/decisions.md#architecture-decisions) and [framework design](../../04-evaluations/docs/framework-design.md#architecture-decisions).

## Architecture decisions

### Selected design and retained decisions

The index points to canonical reasons and consequences without turning every explanation into an ADR or product requirement.

| Choice | Status and rationale |
| --- | --- |
| Work cycle, progression guards, triggered rules | **Selected current design.** [Layer composition](../deliverables/contract-design.md#three-interacting-layers) explains cross-phase applicability and why phase placement must not confine duties. No permanent three-layer requirement or measured benefit is claimed. |
| Bounded commitments, PDSA, focused practices | **Selected current design; recorded as sufficient for the agreed design.** [Method selection](../deliverables/methods-and-references.md#choosing-or-replacing-methods) explains complementary responsibilities without additional umbrella frameworks; replacement remains possible under selection constraints. |
| Role-specific knowledge ownership | **Selected current design.** Role-specific ownership supersedes the default ranking of project sources. [Documentation choices](../deliverables/mechanisms/knowledge-and-documentation.md#documentation-choices) explains why different knowledge owners cannot share one precedence ladder and how unresolved conflicts are handled. |
| Provider-specific bridges | **Selected integration design.** [Bridge rationale](../deliverables/delivery-and-portability.md#why-the-bridges-differ) distinguishes import from read/follow, preserves provenance, and explains provider limits and the absence of common bootstrap policy. |
| Qualified size target and compact wording | **Retained established constraint; identified wording compromises recorded as accepted.** [Portability qualifications](../../01-behavior/deliverables/baseline.md#portability-and-standing-context-qualifications) and [wording trade-offs](../deliverables/delivery-and-portability.md#current-wording-trade-offs) retain exception/review conditions and acceptance limited to those compromises. |
| Effort-baseline checkpoints, advance inquiry declarations, routine-report suppression and consultation strength, method-reference inquiry exemption | **Historical/superseded.** The records below retain useful control/visibility rationale and identify current replacements. |

### Historical source and interpretation

The PDSA-era maintainer guide (`README-maintainers.md`) explains how effort baselines, inquiry declarations, and reporting restrictions were intended to bound work and keep it visible. The four records below concern superseded operating mechanisms. The guide supplies no independent evidence of product acceptance of each detail, agent adherence, or token savings. The [staged contract](../../03-contract/prerelease_AGENTS.md) contains the current operating rules.

### Superseded effort-baseline checkpoint

The agent set task and increment effort baselines using requester direction where available and its own judgment otherwise. The baselines could be qualitative and served as fixed comparison points across attempts and handoffs. Material growth required disclosure and requester direction before added effort, even within agreed scope. Only the requester could revise a baseline or approve the disclosed growth. The checkpoint aimed to expose both unexpectedly heavy work within an increment and cumulative growth across increments. It depended on judgment about material growth and had no automatic enforcement.

Under the [current authorization and limit rules](../deliverables/mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions), a higher agent estimate alone creates no checkpoint. The agent must respect requester-imposed limits and checkpoints, reassess cumulative progress before expanding work or starting another increment or attempt, and seek direction if the evidence does not justify the next increment. The separate duty to consult on consequential choices still applies.

### Superseded inquiry announcement and stopping rule

Inquiry beyond context gathering required an advance declaration of the question, scope, objective, effort limit, and evidence needed. Sufficient evidence or the declared limit ended the attempt and triggered a report, including when the answer remained inconclusive. Declaring an allowance made the commitment visible without enforcing a quota or reserving an approval decision.

[Current inquiry rules](../deliverables/mechanisms/bounded-inquiry.md) require prompt notice of material uncertainty blocking the next decision and its significance unless already communicated in the request or task framing. Context gathering is exempt from inquiry notification and remains subject to scope and limits. Inquiry ends when evidence is sufficient. At an increment's bounds, insufficient evidence requires reassessment before any further investigation. Each further attempt needs justification from preceding findings and must stay within authorization, limits, and checkpoints. Report relevant inquiry outcomes at completion, handoff, or when seeking requester input. Neither a declared allowance nor a report for each attempt is required. Removing the declaration does not establish equivalent behavior or token savings.

### Superseded report suppression and consultation strength

The prohibition on drafting or sending routine reports unless requested or required aimed to avoid spending effort on unused narration. It reduced opportunities for routine visibility without demonstrating savings. [Current reporting](../deliverables/mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) recommends minimizing routine reports and keeping intermediate updates concise and useful. Consolidation remains mandatory at completion, handoff, or a request for input. Initial framing, inquiry notification, and disclosures affecting authorization or decisions retain their separate triggers and timing.

The superseded consultation rule treated asking about unsettled consequential choices as a SHOULD alongside mandatory controls for unresolved intent, permission, and baseline growth. Where no mandatory trigger applied, the timing of consultation remained a matter of judgment. The [current decision guard](../deliverables/mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions) requires requester direction before adopting or implementing new consequential architectural or lasting design direction, or materially departing from established direction, unless the specific choice is already authorized. Asking first about other unsettled material choices remains a SHOULD. Retrospective reports and ADRs cannot supply prior authorization.

### Superseded method-reference inquiry exemption

Narrow consultation to clarify material method ambiguity was exempt from inquiry framing. The exemption kept explanatory links usable without opening a broader research assignment, but it also exempted consultation that investigated a blocking uncertainty. Disclosure of the ambiguity, source, and interpretation was still required.

[Current reference rules](../deliverables/methods-and-references.md#principles-and-reference-boundaries) permit the same narrow reading and require disclosure without importing obligations. Its purpose determines whether inquiry notification and conduct rules apply, including the exception for uncertainty and significance already communicated in the request or task framing. Clear rules must not be researched. Before broader research, the agent must explain the unresolved uncertainty and ask the requester for direction.

### Ownership of contract-design documentation

**The requester approved the documentation structure and authorized local implementation.** The requester's [navigation decision](../../docs/decisions.md#separate-owners-for-architecture-authority-and-decision-rationale) records completion and independent review of the documentation split. That review supplies evidence about organization only. Acceptance of the underlying mechanisms or contract behavior requires separate evidence.

[Contract design](../deliverables/contract-design.md) explains the architecture and leads to five mechanism owners, delivery and portability, and methods and references. Each keeps prescriptions with the rationale needed to apply them. This record owns decisions and alternatives. [Design review](design-review.md) owns editorial guidance and non-normative illustrations. A single file would save links but mix these reading and maintenance tasks. Direct references let readers go to the owner of a question and require maintenance when owners move.

The owner authorized separate specifications for the [work cycle](../deliverables/mechanisms/work-cycle.md) and [bounded inquiry](../deliverables/mechanisms/bounded-inquiry.md) within the approved structure. The former explains how an authorized increment progresses. The latter explains when a blocking question calls for investigation and what evidence justifies stopping or continuing. This amendment concerns documentation ownership only. The selected mechanisms and product requirements retain their existing meaning and status.

The [stage architecture](../../docs/architecture.md#current-bdd-first-organization) locates these owners within Design. Product requirements, runtime instructions, and evaluation criteria each retain their own authority.
