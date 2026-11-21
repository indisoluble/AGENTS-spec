# AGENTS-spec

AGENTS-spec develops a reusable operating contract for collaboration with coding agents.

To install the contract, start with the [consumer adoption guide in `04-candidate/`](04-candidate/pre_README.md). To change it, start with the stage that owns your question.

## Development pipeline

Five stages own the engineering work from discovery through evaluation. The [stage interfaces](docs/architecture.md#stage-interfaces) describe what each consumes and produces.

| Stage | Where to begin a change |
| --- | --- |
| [`01-discovery/`](01-discovery/README.md) | Find objectives and rationale, explore proposals and examples, or raise an open question. |
| [`02-formulation/`](02-formulation/README.md) | Find accepted requirements, applicable constraints, and the decisions that establish their scope. |
| [`03-design/`](03-design/README.md) | Find the mechanism selected for a requirement, its rationale, and the contract clauses that express it. |
| [`04-candidate/`](04-candidate/) | Inspect the staged instructions, bridges, and guides that consumers receive. |
| [`05-evaluations/`](05-evaluations/README.md) | Find a case, run it against an identified candidate, or interpret the evidence. |

Work can begin in any stage. The [behavior-driven development (BDD) workflow](docs/authority-and-change.md#bdd-activities-and-complementary-responsibilities) shows how test-first checks and feedback guide development.

The [accepted objectives](01-discovery/deliverables/objectives-and-rationale.md#established-objectives) put **O1 (control token consumption)** ahead of **O2 (requester awareness and consequential control)**. Durable project knowledge supports both. Evidence of savings or compliance requires separate assessment.

## Finding your way around

Discovery, Formulation, Design, and Evaluations use stage READMEs for orientation, `deliverables/` for substantive outputs, and `docs/` for supporting knowledge. Candidate stages the five [consumer files](docs/architecture.md#staged-sources-and-release-relative-references).

The root [`docs/`](docs/) directory covers engineering questions shared across stages.

- [`docs/architecture.md`](docs/architecture.md) defines the stage interfaces and documentation layout.
- [`docs/authority-and-change.md`](docs/authority-and-change.md#finding-an-owner-and-checking-a-change) explains where to begin a change, who can decide it, and how to follow affected dependencies.
- [`docs/decisions.md`](docs/decisions.md) records the reasons, status, and scope of architectural decisions.
