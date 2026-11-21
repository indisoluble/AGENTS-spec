# AGENTS-spec

AGENTS-spec develops a reusable operating contract for collaboration with coding agents.

To install the contract, start with the [consumer adoption guide in `04-candidate/`](04-candidate/pre_README.md). To change it, start with the stage that owns your question.

## Development pipeline

Five stages realize the three practices of behavior-driven development (BDD). Discovery and Formulation each have a stage. Design, Candidate, and Evaluations share Automation. The [stage interfaces](docs/architecture.md#stage-interfaces) describe what each consumes and produces.

| Stage | Where to begin a change |
| --- | --- |
| [`01-discovery/`](01-discovery/README.md) | Find objectives and rationale, explore proposals and examples, or raise an open question. |
| [`02-formulation/`](02-formulation/README.md) | Find accepted requirements, applicable constraints, and the decisions that establish their scope. |
| [`03-design/`](03-design/README.md) | Find the mechanism selected for a requirement, its rationale, and the contract clauses that express it. |
| [`04-candidate/`](04-candidate/) | Inspect the staged instructions, bridges, and guides that consumers receive. |
| [`05-evaluations/`](05-evaluations/README.md) | Find a case, run it against an identified candidate, or interpret the evidence. |

Work can begin in any stage. The [BDD workflow](docs/pipeline.md#test-first-iteration) shows how test-first checks and feedback guide development.

The [accepted objectives](01-discovery/deliverables/objectives-and-rationale.md#established-objectives) put **O1 (control token consumption)** ahead of **O2 (requester awareness and consequential control)**. Durable project knowledge supports both. Evidence of savings or compliance requires separate assessment.

For engineering questions that span stages, use the shared documentation index in [`docs/README.md`](docs/README.md).
