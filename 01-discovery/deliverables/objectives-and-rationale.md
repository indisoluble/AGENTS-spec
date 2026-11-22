# Established objectives and rationale for AGENTS-spec

This document records what AGENTS-spec aims to achieve and why its [accepted requirements](../../02-formulation/deliverables/baseline.md) support those aims. Established objectives state desired outcomes and are supported by explicit requester direction or accepted project records beyond the implemented clause alone.

## Established objectives

| Objective | Intended outcome and qualifications |
| --- | --- |
| **[O1 — Control token consumption, first](#r1)** | Bound the next commitment and keep work proportionate. The current design uses small, meaningful increments and progressive detail. O1 leaves the choice of mechanism open to authorized redesign within the accepted requirements and constraints. Necessary reasoning, completeness, consistency, and validation remain part of the work; a smaller commitment is not permission for insufficient depth. This is a qualitative objective, with no token quota or guarantee of savings. |
| **[O2 — Requester awareness and consequential control, second](#r2)** | Keep the requester informed and in control of consequential direction without constant supervision. Routine execution can remain autonomous within authorization. The exact consultation, notification, reporting, and limit mechanisms are explained in the [authorization and requester decisions](../../03-design/deliverables/mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions), [inquiry design](../../03-design/deliverables/mechanisms/bounded-inquiry.md), and [reporting design](../../03-design/deliverables/mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution); this objective alone does not establish each mechanism's permanent trigger or strength. |
| **Knowledge continuity** | Preserve project facts and reasons for maintainers, users, and future agents through reliable canonical documentation. This supports both ordered objectives without making every discussion a permanent record or every method a deliverable. |

These are intended effects. Textual consistency, contract size, message counts, selected methods, and passing evaluator tests cannot establish measured token savings, comprehension, or agent adherence. Assessing the benefits calls for [comparative evidence and requester feedback where relevant](../../docs/traceability.md#what-evidence-can-establish). Quantitative thresholds and comprehensive behavioral acceptance criteria have not been independently established here.

The priority order follows established requester direction. No comparative reason for ranking O1 ahead of O2 was recorded. The [contract design](../../03-design/deliverables/contract-design.md#design-goals-and-boundaries) explains how the selected mechanisms serve both objectives.

## Rationale map

R1–R4 link accepted behavioral requirements to the [objectives](#established-objectives) and supporting reasons. Direct contributions describe intended effects. Supporting reasons need not correspond one-to-one to the objectives. Each BR links back to its rationale and separately to Design for its current realization. [R5](../../02-formulation/deliverables/baseline.md#r5) explains PR1’s delivery boundary alongside the requirement in Formulation. R1–R5 are navigation IDs and add no requirements.

### R1

**Direct contribution to O1:** proportionate commitments and bounded inquiry control the next commitment while retaining sufficient depth, coherence, and evidence-based reassessment.

Accepted requirements: [BR1](../../02-formulation/deliverables/baseline.md#br1--focused-proportionate-authorized-work), [BR4](../../02-formulation/deliverables/baseline.md#br4--bounded-investigation-and-timely-reassessment).

### R2

**Direct contribution to O2:** routine autonomy, timely awareness, and prior direction for consequential choices keep the requester in control without constant supervision.

Accepted requirements: [BR3](../../02-formulation/deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction), [BR4](../../02-formulation/deliverables/baseline.md#br4--bounded-investigation-and-timely-reassessment), [BR7](../../02-formulation/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs).

### R3

**Supporting evidence and quality:** distinguish intent from observations, learn from results, validate completion, and preserve engineering guarantees so proportionate work remains correct and complete. These support O1/O2 without establishing savings or adherence.

Accepted requirements: [BR2](../../02-formulation/deliverables/baseline.md#br2--evidence-based-planning-and-knowledge-ownership), [BR5](../../02-formulation/deliverables/baseline.md#br5--completion-supported-by-validation), [BR6](../../02-formulation/deliverables/baseline.md#br6--learning-from-observed-results), [BR9](../../02-formulation/deliverables/baseline.md#br9--engineering-quality-and-preservation).

### R4

**Supporting knowledge continuity:** canonical facts, lasting reasons, affected documentation, and actionable handoffs let maintainers, users, and future agents continue with the relevant evidence and authority state.

Accepted requirements: [BR2](../../02-formulation/deliverables/baseline.md#br2--evidence-based-planning-and-knowledge-ownership), [BR7](../../02-formulation/deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs), [BR8](../../02-formulation/deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority), [BR10](../../02-formulation/deliverables/baseline.md#br10--affected-requirements-and-documentation).
