# AGENTS-spec

AGENTS-spec develops a reusable operating contract for collaboration with coding agents.

To install the contract, start with the [consumer adoption guide in `03-candidate/`](03-candidate/pre_README.md). To change it, start with the stage that owns your question.

## Development pipeline

The repository currently has four stage directories. Behavior owns both Discovery and Formulation. The [approved five-stage target](docs/architecture.md#approved-five-stage-target) gives those practices separate stages. The [migration](docs/architecture.md#migration-from-the-implemented-layout) is pending.

| Stage | Where to begin a change |
| --- | --- |
| [`01-behavior/`](01-behavior/README.md) | Find the objectives, accepted requirements and constraints, or explore a proposed change in Discovery. |
| [`02-design/`](02-design/README.md) | Find the mechanism selected for a requirement, its rationale, and the contract clauses that express it. |
| [`03-candidate/`](03-candidate/) | Inspect the staged instructions, bridges, and guides that consumers receive. |
| [`04-evaluations/`](04-evaluations/README.md) | Find a case, run it against an identified candidate, or interpret the evidence. |

Work can begin in any stage. The [behavior-driven development (BDD) workflow](docs/authority-and-change.md#bdd-activities-and-complementary-responsibilities) shows how test-first checks and feedback guide development.

The [accepted objectives](01-behavior/deliverables/objectives-and-rationale.md#established-objectives) put **O1 (control token consumption)** ahead of **O2 (requester awareness and consequential control)**. Durable project knowledge supports both. Evidence of savings or compliance requires separate assessment.

## Finding your way around

Behavior, Design, and Evaluations use stage READMEs for orientation, `deliverables/` for substantive outputs, and `docs/` for supporting knowledge. Candidate stages the five [consumer files](docs/architecture.md#staged-sources-and-release-relative-references).

The root [`docs/`](docs/) directory covers engineering questions shared across stages.

- [`docs/architecture.md`](docs/architecture.md) defines the implemented and target stage interfaces and documentation layout.
- [`docs/authority-and-change.md`](docs/authority-and-change.md#finding-an-owner-and-checking-a-change) explains where to begin a change, who can decide it, and how to follow affected dependencies.
- [`docs/decisions.md`](docs/decisions.md) records the reasons, status, and scope of architectural decisions.
