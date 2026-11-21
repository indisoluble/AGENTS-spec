# AGENTS-spec

AGENTS-spec develops a reusable operating contract for collaboration with coding agents.

To install the contract, start with the [consumer adoption guide in `03-candidate/`](03-candidate/pre_README.md). To change it, start with the stage that owns your question.

## Development pipeline

**Objectives → Requirements → Mechanisms → Candidate AGENTS.md → Evaluations**

The five conceptual steps map to four stage directories. Behavior owns both Objectives and Requirements.

| Stage | Where to begin a change |
| --- | --- |
| [`01-behavior/`](01-behavior/README.md) | Find the objectives, accepted requirements and constraints, or explore a proposed change in Discovery. |
| [`02-design/`](02-design/README.md) | Find the mechanism selected for a requirement, its rationale, and the contract clauses that express it. |
| [`03-candidate/`](03-candidate/) | Inspect the staged instructions, bridges, and guides that consumers receive. |
| [`04-evaluations/`](04-evaluations/README.md) | Find a case, run it against an identified candidate, or interpret the evidence. |

Work can begin in any stage. In behavior-driven development (BDD), [Discovery, Formulation, and Automation](docs/authority-and-change.md#bdd-activities-and-complementary-responsibilities) iterate across these owners. An evaluation finding can reopen work wherever the issue belongs.

The [accepted objectives](01-behavior/deliverables/objectives-and-rationale.md#established-objectives) put **O1 (control token consumption)** ahead of **O2 (requester awareness and consequential control)**. Durable project knowledge supports both. Evidence of savings or compliance requires separate assessment.

## Finding your way around

Behavior, Design, and Evaluations use the same layout.

- `README.md` introduces the stage and points to the file for your task.
- `deliverables/` is the authoritative home of the stage's outputs. Each output retains its own status. For example, Behavior keeps accepted requirements and proposed examples here.
- `docs/` holds supporting architecture, decisions, rationale, and maintenance guidance. Rationale essential to applying a specification stays with that specification.

`03-candidate/` stages exactly five files for consumers. The package is independent of engineering documentation. The [staged source map](docs/architecture.md#staged-sources-and-release-relative-references) gives their installation paths.

The root [`docs/`](docs/) directory covers engineering questions shared across stages.

- [`docs/architecture.md`](docs/architecture.md#stage-interfaces) shows what each stage uses, owns, and makes available to others.
- [`docs/authority-and-change.md`](docs/authority-and-change.md#finding-an-owner-and-checking-a-change) explains where to begin a change, who can decide it, and how to follow affected dependencies.
- [`docs/decisions.md`](docs/decisions.md) records why the project chose this structure and the scope of the decisions.
