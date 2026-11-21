# Making a cross-stage contract change

## Find the owner and the decision

1. Start with the question. Use the [stage interfaces](architecture.md#stage-interfaces) to find the responsible stage. Read its deliverable alongside the assumptions, constraints, and decisions that explain it. For a question about a run, start with the [case specification](../05-evaluations/README.md#case-specifications) and [retained evidence](../05-evaluations/docs/running-and-reviewing.md#results-evidence-and-failure-investigation).
2. Identify what is settled. Discovery's [rationale map](../01-discovery/deliverables/objectives-and-rationale.md#rationale-map) explains the outcome, Formulation's [baseline](../02-formulation/deliverables/baseline.md) identifies accepted behavior, and Design's [clause index](../03-design/deliverables/contract-design.md#contract-clause-index) locates its current realization. If several formulations or mechanisms fit, weigh them against the stage's purpose and constraints. Keep unresolved intent in [Discovery](../01-discovery/deliverables/open-questions.md).
3. Distinguish an editorial clarification from a change to operating behavior. Check the [decision authority and authorized scope](authority.md#development-decisions) before changing a requirement, mechanism, or instruction. An explanation of current behavior draws on the applicable contract clauses and rationale.

## Change the owner and verify its dependents

Identify direct dependents and what would verify the change. Follow the [design and evaluation paths](traceability.md#tracing-a-requirement-and-its-evaluation) separately. PR1, for example, can be checked by [direct inspection of the delivered artifact](../02-formulation/deliverables/baseline.md#r5). For behavior, use the [test-first iteration](pipeline.md#test-first-iteration).

Make the authorized change at the canonical owner first. For an authorized behavior change, update the runtime contract and affected documentation to reflect the established intent, constraints, and decisions. Preserve applicable [method-selection constraints](../02-formulation/deliverables/baseline.md#method-selection-qualifications), [portability qualifications](../02-formulation/deliverables/baseline.md#portability-and-standing-context-qualifications), and the limited acceptance of [wording trade-offs](../03-design/deliverables/delivery-and-portability.md#current-wording-trade-offs).

Follow a reference further when the change affects what the next owner relies on.

- For affected explanations, inspect summaries, examples, references, and bridge guidance in the context of the complete reader task. Use Design's [explanation checks](../03-design/docs/design-review.md#reviewing-contract-explanations) and relevant [non-normative illustrations](../03-design/docs/design-review.md#assessing-design-changes). These checks establish what the text communicates. Behavioral claims need observations.
- For affected clauses, assess the [impact on evaluation expectations and references](traceability.md#specification-to-evaluation-dependencies). Where a case needs a change, follow [`05-evaluations/docs/maintaining-evaluations.md`](../05-evaluations/docs/maintaining-evaluations.md#change-a-scenario).

## Route a finding

In the [requester-guidance case](../05-evaluations/deliverables/cases/requester-guidance.md#human-review-and-interpretation), an agent can pass the response-presence check while guessing the missing timezone. Read the response and workspace evidence against the rubric. If the fixture supplied the timezone by mistake, take the correction to Evaluations. If the review exposes unsettled intent about when the agent may assume a value, take that question to Discovery. The passing assertion establishes only that a response was present.
