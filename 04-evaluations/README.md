# 04 — Evaluations

Evaluations exercises the staged contract and verifies the evaluator machinery. Current cases are clause-based; results concern the cases run, and offline tests do not establish agent compliance.

- [Evaluation model and evidence limits](docs/evaluation-model.md) explains assessment stages, coverage gaps, and future requirements-derived expectations.
- [Cases and requirements](deliverables/cases-and-requirements.md): ten cases and E1–E40, with links to scenario modules and tests.
- [Running and reviewing](docs/running-and-reviewing.md): setup, offline checks, authentication, commands, evidence, human review, and failure investigation.
- [Framework design](docs/framework-design.md) covers execution and security boundaries. Go directly to the [framework architecture](docs/framework-design.md#framework-architecture), [maintenance tasks](docs/framework-design.md#framework-maintenance), or [architecture decisions](docs/framework-design.md#architecture-decisions).

Run `python -m deliverables` from `04-evaluations/` after following setup and offline checks. The [Python entry point](deliverables/__main__.py) composes the cases; scenario modules own exact prompts, fixtures, assertions, checks, and rubrics. Use [authority and change](../docs/authority-and-change.md#cross-domain-traceability-and-feedback) for cross-stage dependencies and acceptance boundaries.
