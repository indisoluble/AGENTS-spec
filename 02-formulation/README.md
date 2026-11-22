# 02 — Formulation

Formulation records what the requester or an authorized delegate has accepted about the product. It uses Discovery’s proposals, examples, and open questions to express the agreed behavior in the baseline, alongside applicable constraints and any expressly accepted defining examples. Design uses the specification to choose a mechanism. Evaluations uses it to establish an independent expectation. The shared [stage interfaces](../docs/architecture.md#stage-interfaces) define these handoffs.

| Contributor task | Where to look |
| --- | --- |
| Look up an agent duty, permission, or recommendation | The [behavioral requirements BR1–BR10 in deliverables/baseline.md](deliverables/baseline.md#accepted-behavioral-requirements) link each rule to its rationale and current realization. |
| Check what must travel in the delivered contract and which constraints apply | [PR1 and its R5 rationale](deliverables/baseline.md#established-product-requirement) and the [authority, method-selection, and portability constraints](deliverables/baseline.md#established-constraints). |
| Understand why a rule exists and what authorized it | Discovery’s [objectives and rationale map](../01-discovery/deliverables/objectives-and-rationale.md) and the baseline’s [acceptance sources and editorial limits](deliverables/baseline.md#status-and-provenance). |
| Find an example or a question awaiting decision | Discovery indexes [proposed examples by requirement](../01-discovery/deliverables/example-coverage.md#requirement-to-scenario-coverage) and explains the [unsettled choices](../01-discovery/deliverables/open-questions.md). All current Discovery examples remain proposed. |
| Formulate or revise an authorized rule or defining example | [Maintaining Formulation](docs/maintaining-formulation.md) starts at the Discovery handoff and follows the decision through verification. |
| Trace an implementation or assess a behavioral claim | Design’s [contract clause index](../03-design/deliverables/contract-design.md#contract-clause-index) connects rules to mechanisms and instructions. The [test-first evaluation handoff](docs/maintaining-formulation.md#hand-accepted-intent-to-evaluations) explains what evidence can support a claim about a requirement. |
