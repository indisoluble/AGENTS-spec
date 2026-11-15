# 04 — Evaluations

Evaluations exercises the staged contract, retains observations and assessment evidence, and verifies the evaluator machinery. Results concern the cases run; offline tests establish machinery behavior, not agent compliance. The [evaluation model](docs/evaluations.md#purpose-and-evaluation-model) owns the full evidence limits, coverage gaps, and distinction between current clause-based cases and future requirements-derived expectations.

`deliverables/` contains the case specification, [dependency requirements](deliverables/requirements.txt), and executable Python package; `docs/` contains explanatory and maintenance guidance. This README provides orientation and navigation.

- [cases-and-requirements.md](deliverables/cases-and-requirements.md) is the substantive specification of all ten cases and evaluator requirements E1–E40.
- [deliverables/](deliverables/) is the executable Python package. Its [entry point](deliverables/__main__.py) registers cases, runtime modules provide shared machinery, scenario modules own exact prompts, fixtures, assertions, checks, and rubrics, and tests verify these responsibilities.
- Local `docs/` owns the [evaluation model](docs/evaluations.md), [operations and evidence interpretation](docs/running-and-reviewing.md), and [framework architecture, maintenance, and decisions](docs/framework-design.md).

**Run evaluator commands with `04-evaluations/` as the working directory.** From the repository root, enter it with `cd 04-evaluations`; invoke the package with `python -m deliverables`. Follow [installation and offline checks](docs/running-and-reviewing.md#setup-and-running-evaluations) before running cases. New evidence goes to the stage-local `.eval-runs/`, as [retained evidence](docs/running-and-reviewing.md#retained-evidence) explains.

For a failed run, start with [diagnosis](docs/running-and-reviewing.md#investigate-a-failure-or-incomplete-result), then the [case criteria and source links](deliverables/cases-and-requirements.md#cases-and-interpretation). For maintenance, use [framework ownership and extension](docs/framework-design.md#architecture-extension-and-maintenance), [shared interfaces and authority](../docs/authority-and-change.md#cross-domain-traceability-and-feedback), and [change impact](../docs/authority-and-change.md#change-impact). Return to the [project README](../README.md) for the wider pipeline.
