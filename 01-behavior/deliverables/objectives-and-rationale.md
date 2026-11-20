# Established objectives and rationale for AGENTS-spec

This document records what AGENTS-spec aims to achieve and why its [accepted requirements](baseline.md) support those aims. Established objectives state desired outcomes and are supported by explicit requester direction or accepted project records beyond the implemented clause alone.

## Established objectives

| Objective | Intended outcome and qualifications |
| --- | --- |
| **[O1 — Control token consumption, first](#r1)** | Bound the next commitment and keep work proportionate. The current design uses small, meaningful increments and progressive detail. Necessary reasoning, completeness, consistency, and validation remain part of the work; a smaller commitment is not permission for insufficient depth. This is a qualitative objective, with no token quota or guarantee of savings. |
| **[O2 — Requester awareness and consequential control, second](#r2)** | Keep the requester informed and in control of consequential direction without constant supervision. Routine execution can remain autonomous within authorization. The exact consultation, notification, reporting, and limit mechanisms are explained in the [authorization and requester decisions](../../02-design/deliverables/mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions), [inquiry design](../../02-design/deliverables/mechanisms/bounded-inquiry.md), and [reporting design](../../02-design/deliverables/mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution); this objective alone does not establish each mechanism's permanent trigger or strength. |
| **Knowledge continuity** | Preserve project facts and reasons for maintainers, users, and future agents through reliable canonical documentation. This supports both ordered objectives without making every discussion a permanent record or every method a deliverable. |

These are intended effects. Textual consistency, file size, message counts, and selected methods do not establish measured token savings, comprehension, or agent adherence. Quantitative thresholds and comprehensive behavioral acceptance criteria have not been independently established here.

The [contract design](../../02-design/deliverables/contract-design.md#design-goals-and-boundaries) identifies token control as the first objective and requester awareness and consequential control as the second. The documentation-maintenance guide independently specified the same priority for the [adoption guide](../../03-contract/prerelease_README.md), as reflected in the [reader guidance](../../02-design/docs/design-review.md#reader-paths).

## Rationale map

This map explains the accepted requirements without changing their wording or status. R1–R5 are stable navigation IDs, not new objectives or requirements. Direct contributions refer to the intended [O1/O2 outcomes](#established-objectives), not measured benefits; supporting reasons need not map one-to-one to those objectives. Each requirement links back here. Its current-realization links lead to mechanism rationale and contract coverage, which remain owned by design.

### R1

**Direct contribution to O1:** proportionate commitments and bounded inquiry control the next commitment while retaining sufficient depth, coherence, and evidence-based reassessment.

Accepted requirements: [BR1](baseline.md#br1--focused-proportionate-authorized-work), [BR4](baseline.md#br4--bounded-investigation-and-timely-reassessment).

### R2

**Direct contribution to O2:** routine autonomy, timely awareness, and prior direction for consequential choices keep the requester in control without constant supervision.

Accepted requirements: [BR3](baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR4](baseline.md#br4--bounded-investigation-and-timely-reassessment), [BR7](baseline.md#br7--proportionate-communication-and-actionable-handoffs).

### R3

**Supporting evidence and quality:** distinguish intent from observations, learn from results, validate completion, and preserve engineering guarantees so proportionate work remains correct and complete. These support O1/O2 without establishing savings or adherence.

Accepted requirements: [BR2](baseline.md#br2--evidence-based-planning-and-knowledge-ownership), [BR5](baseline.md#br5--completion-supported-by-validation), [BR6](baseline.md#br6--learning-from-observed-results), [BR9](baseline.md#br9--engineering-quality-and-preservation).

### R4

**Supporting knowledge continuity:** canonical facts, lasting reasons, affected documentation, and actionable handoffs let maintainers, users, and future agents continue with the relevant evidence and authority state.

Accepted requirements: [BR2](baseline.md#br2--evidence-based-planning-and-knowledge-ownership), [BR7](baseline.md#br7--proportionate-communication-and-actionable-handoffs), [BR8](baseline.md#br8--durable-knowledge-without-expanded-editing-authority), [BR10](baseline.md#br10--affected-requirements-and-documentation).

### R5

**Established self-contained delivery boundary:** the delivered contract contains all generic operating duties; guides, bridges, and internal records supply no hidden policy. Verify the [delivered contract](../../03-contract/prerelease_AGENTS.md) by standalone inspection, using the [proposed PR1 inspection examples](proposed-examples/self-contained-delivery.md#pr1--self-contained-operating-contract); provider loading and agent behavior require separate evidence.

Accepted requirements: [PR1](baseline.md#established-product-requirement).
