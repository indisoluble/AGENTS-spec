# AGENTS-spec

AGENTS-spec develops a reusable operating contract for collaboration with coding agents. Its [accepted objectives](01-behavior/deliverables/baseline.md#established-objectives) are ordered: **O1, control token consumption, first; O2, requester awareness and consequential control, second.** Durable project knowledge supports both by preserving facts and reasons for maintainers, users, and future agents. These are intended outcomes, not claims of measured savings or demonstrated compliance.

The repository has four numbered responsibilities:

| Stage | Principal inputs → outputs | Start here |
| --- | --- | --- |
| **01 — Behavior** | Requester intent, constraints, and feedback → accepted product requirements and separately proposed examples. | [Behavior](01-behavior/README.md), [accepted baseline](01-behavior/deliverables/baseline.md) |
| **02 — Design** | Accepted behavioral intent and product constraints → contract design, mechanisms, and their rationale. | [Design](02-design/README.md) |
| **03 — Contract** | Selected design → five staged consumer artifacts, including the self-contained runtime instructions. | [Consumer adoption guide](03-contract/prerelease_README.md), [staged-source mapping](docs/architecture.md#staged-sources-and-release-relative-references) |
| **04 — Evaluations** | Versioned candidate and case definitions → observations, automated results, and evidence for human review. | [Evaluations](04-evaluations/README.md) |

Numbering shows conceptual progression, not mandatory sequential gates. BDD Discovery, Formulation, and Automation iterate across these owners; feedback can reopen a behavioral question. Current cases retain their clause-based interpretation, and proposed examples are not yet accepted defining criteria. [Shared interfaces and traceability](docs/authority-and-change.md#cross-domain-traceability-and-feedback) explain these relationships and gaps.

This README and the stage READMEs introduce and navigate the engineering project. Each engineering stage separates substantive artifacts in `deliverables/` from stage-specific supporting knowledge in `docs/`; definitions retain their canonical owners. `03-contract/` is the artifact-only exception, containing exactly five consumer files without an engineering README, `docs/`, or `deliverables/`. Those files do not depend on the engineering documentation.

For a narrow maintenance task, follow the relevant stage link, then its authoritative artifact and directly affected dependents. Use [architecture](docs/architecture.md) for the current layout, [authority and change](docs/authority-and-change.md#finding-an-owner-and-checking-a-change) for ownership, approval distinctions, and change routes, and [engineering history](docs/engineering-history.md) for system-wide decisions and their rationale.
