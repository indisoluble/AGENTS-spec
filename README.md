# AGENTS-spec

AGENTS-spec develops a reusable operating contract for collaboration with coding agents.

To install or use the contract in your project, start with the [consumer adoption guide](04-candidate/pre_README.md).

## Development pipeline

Five stages realize the three practices of behavior-driven development (BDD). Discovery and Formulation each have a stage. Design, Candidate, and Evaluations share Automation. The [stage interfaces](docs/architecture.md#stage-interfaces) describe what each consumes and produces.

| Engineering task | Where to start |
| --- | --- |
| Explore a product question or proposed example | [Discovery](01-discovery/README.md) |
| Revise accepted behavior under a requester decision | [Formulation](02-formulation/README.md) |
| Revise a selected mechanism or find its rationale | [Design](03-design/README.md) |
| Maintain a staged instruction, bridge, or consumer guide | [Candidate files](04-candidate/) and their [installed locations](docs/architecture.md#staged-sources-and-release-relative-references) |
| Add or change a case, or investigate a result | [Evaluations](05-evaluations/README.md) |
| Update engineering documentation or locate an architectural decision | [Shared engineering index](docs/README.md) |

If your task crosses stages, use the [cross-stage change guide](docs/changing-the-contract.md) to find the decision, affected owners, and verification path. Work can begin in any stage. The [BDD workflow](docs/pipeline.md#test-first-iteration) explains test-first iteration.

The [accepted objectives](01-discovery/deliverables/objectives-and-rationale.md#established-objectives) put **O1 (control token consumption)** ahead of **O2 (requester awareness and consequential control)**. Durable project knowledge supports both. Evidence of savings or compliance requires separate assessment.
