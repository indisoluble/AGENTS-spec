# AGENTS-spec

AGENTS-spec develops a reusable operating contract for collaboration with coding agents. Its [accepted objectives](01-behavior/deliverables/baseline.md#established-objectives) are ordered: **O1, control token consumption, first; O2, requester awareness and consequential control, second.** Durable project knowledge supports both by preserving facts and reasons for maintainers, users, and future agents. These are intended outcomes, not claims of measured savings or demonstrated compliance.

The engineering pipeline has four stages:

| Stage | Principal inputs → outputs | Start here |
| --- | --- | --- |
| **01 — Behavior** | Requester intent, constraints, and feedback → accepted product requirements and separately proposed examples. | [Behavior](01-behavior/README.md), [accepted baseline](01-behavior/deliverables/baseline.md) |
| **02 — Design** | Accepted behavioral intent and product constraints → contract design, mechanisms, and their rationale. | [Design](02-design/README.md) |
| **03 — Contract** | Selected design → five staged consumer artifacts, including the self-contained runtime instructions. | [Consumer adoption guide](03-contract/prerelease_README.md), [staged-source mapping](docs/architecture.md#staged-sources-and-release-relative-references) |
| **04 — Evaluations** | Versioned candidate and case definitions → observations, automated results, and evidence for human review. | [Evaluations](04-evaluations/README.md) |

BDD Discovery, Formulation, and Automation iterate across these stages; numbering does not impose sequential gates. Proposed examples remain unaccepted, and current evaluations remain clause-based rather than requirements-derived acceptance tests. [Traceability and feedback](docs/authority-and-change.md#cross-domain-traceability-and-feedback) explains the intended relationships and current gaps.

For maintenance, start with the relevant stage and [find the owner and its affected dependents](docs/authority-and-change.md#finding-an-owner-and-checking-a-change). Use the [engineering architecture](docs/architecture.md) to locate detailed owners and [documented risks and limits](docs/architecture.md#risks-and-technical-debt). Consult the [authority model](docs/authority-and-change.md#development-time-and-runtime-authority) for acceptance and authorization, the [documentation convention](docs/authority-and-change.md#engineering-documentation-convention) for placement and naming, and [system-wide engineering decisions](docs/decisions.md) for rationale. The consumer contract contains all runtime instructions; consumer artifacts do not depend on this engineering documentation.
