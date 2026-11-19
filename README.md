# AGENTS-spec

AGENTS-spec develops a reusable operating contract for collaboration with coding agents.

## Development pipeline

**Objectives → Requirements → Mechanisms → AGENTS.md → Evaluations**

The five conceptual steps map to four stage directories. Behavior owns both Objectives and Requirements.

| Stage | Responsibility |
| --- | --- |
| [01 — Behavior](01-behavior/README.md) | Establish the objectives and define the accepted requirements and constraints that express them. |
| [02 — Design](02-design/README.md) | Select mechanisms that realize accepted intent within those constraints. |
| [03 — Contract](03-contract/prerelease_AGENTS.md) | Express the selected design in `prerelease_AGENTS.md`, the staged source for the self-contained `AGENTS.md` delivered to consumers. |
| [04 — Evaluations](04-evaluations/README.md) | Exercise the versioned contract candidate in defined cases and collect observations, automated results, and evidence for human review. |

Developers can start at any stage without repeating earlier work. Evaluation findings can reopen work at any relevant stage. Existing requirements, decisions, and [authority boundaries](docs/authority-and-change.md#development-time-and-runtime-authority) still apply. In behavior-driven development (BDD), Discovery, Formulation, and Automation [iterate across these responsibilities](docs/authority-and-change.md#bdd-activities-and-complementary-responsibilities), so the numbered stages are not mandatory sequential gates.

The [accepted objectives](01-behavior/deliverables/baseline.md#established-objectives) put **O1 (control token consumption)** ahead of **O2 (requester awareness and consequential control)**. Durable project knowledge supports both. Evidence of savings or compliance requires separate assessment.

For installation, start with the [consumer adoption guide](03-contract/prerelease_README.md). The [staged source map](docs/architecture.md#staged-sources-and-release-relative-references) gives the delivery filename for each of the five consumer artifacts. For engineering changes, see [how to find the owner and check affected dependencies](docs/authority-and-change.md#finding-an-owner-and-checking-a-change) and the [engineering architecture](docs/architecture.md).
