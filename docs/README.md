# Shared engineering documentation

Start with [`docs/architecture.md` § Stage interfaces](architecture.md#stage-interfaces). For open questions about a requirement, mechanism or evaluation criterion, use [`docs/traceability.md` § Current traceability gaps](traceability.md#current-traceability-gaps).

## Cross-stage changes

The cross-stage change guide ([`docs/changing-the-contract.md`](changing-the-contract.md)) follows an issue from its owner to the affected dependents. Choose the example that matches your task.

- Clarify Candidate wording and check its dependents ([`docs/changing-the-contract.md` § Clarify Candidate wording](changing-the-contract.md#clarify-candidate-wording))
- [`docs/changing-the-contract.md` § Review a requester conclusion for incorporation](changing-the-contract.md#review-a-requester-conclusion-for-incorporation)
- Apply an authorized change to accepted behavior ([`docs/changing-the-contract.md` § Apply an authorized behavior change](changing-the-contract.md#apply-an-authorized-behavior-change))
- Compare a replacement for PDSA under BR6 ([`docs/changing-the-contract.md` § Compare a replacement for PDSA](changing-the-contract.md#compare-a-replacement-for-pdsa))
- Investigate a failed or inconclusive evaluation ([`docs/changing-the-contract.md` § Investigate a requester-guidance result](changing-the-contract.md#investigate-a-requester-guidance-result))
- [`docs/changing-the-contract.md` § Diagnose a delivery or loading issue](changing-the-contract.md#diagnose-a-delivery-or-loading-issue)
- Repair a reference after a heading change ([`docs/changing-the-contract.md` § Repair a documentation reference](changing-the-contract.md#repair-a-documentation-reference))

## Shared references and procedures

| What do you need to know or do? | Where to start |
| --- | --- |
| Find a stage's inputs, outputs, and boundary with the other stages. | [`docs/architecture.md` § Stage interfaces](architecture.md#stage-interfaces) |
| Work through a BDD iteration or resolve a methodology question. | [`docs/pipeline.md`](pipeline.md) |
| Identify who can accept a proposal and what governs development or runtime. | [`docs/authority.md`](authority.md) |
| Trace a requirement to its dependents, interpret evidence, or route a finding. | [`docs/traceability.md`](traceability.md) |
| Look up a Candidate clause or the mechanism behind a proposed example. | [`docs/contract-traces.md`](contract-traces.md) |
| Review the adoption and practical guides. | [`docs/consumer-documentation-review.md`](consumer-documentation-review.md) |
| Find the owner for a specification, its rationale, or a decision record. | [`docs/documentation.md`](documentation.md) |
| Decide what to write, which concerns matter, and whether it needs a separate file. | [`docs/writing-documentation.md`](writing-documentation.md) |
| Find documentation affected by a change or verify that a reader can use it. | [`docs/maintaining-documentation.md`](maintaining-documentation.md) |
| Find the rationale, status, or successor of an architectural decision. | [`docs/decisions.md` § Architecture decisions](decisions.md#architecture-decisions) · [`03.0-design/docs/decisions.md` § Architecture decisions](../03.0-design/docs/decisions.md#architecture-decisions) · [`engine/docs/framework-design.md` § Architecture decisions](../engine/docs/framework-design.md#architecture-decisions) · [`05-evaluation/docs/framework-design.md` § Architecture decisions](../05-evaluation/docs/framework-design.md#architecture-decisions) |

The repository README ([`README.md` § Development pipeline](../README.md#development-pipeline)) introduces the pipeline. The stage interfaces link to all seven owners and the shared engine.
