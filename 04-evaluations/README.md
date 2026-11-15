# 04 — Evaluations

Evaluations exercises the staged contract, retains observations and assessment evidence, and verifies the evaluator machinery. Results concern the cases run; offline tests establish machinery behavior, not agent compliance. The [evaluation model](docs/evaluations.md#purpose-and-evaluation-model) owns the full evidence limits, coverage gaps, and distinction between current clause-based cases and future requirements-derived expectations.

- [cases-and-requirements.md](cases-and-requirements.md) is the substantive specification of all ten cases and evaluator requirements E1–E40.
- [evaluations/](evaluations/) is the executable Python package. Its [entry point](evaluations/__main__.py) registers cases, runtime modules provide shared machinery, scenario modules own exact prompts, fixtures, assertions, checks, and rubrics, and tests verify these responsibilities.
- Local `docs/` owns the [evaluation model](docs/evaluations.md), [operations and evidence interpretation](docs/running-and-reviewing.md), and [framework architecture, maintenance, and decisions](docs/framework-design.md).

**Run evaluator commands with `04-evaluations/` as the working directory.** From the repository root, enter it with `cd 04-evaluations`; the package invocation remains `python -m evaluations`. Follow [installation and offline checks](docs/running-and-reviewing.md#setup-and-running-evaluations) before running cases. New evidence goes to the stage-local `.eval-runs/`, as [retained evidence](docs/running-and-reviewing.md#retained-evidence) explains.

For a failed run, start with [diagnosis](docs/running-and-reviewing.md#investigate-a-failure-or-incomplete-result), then the [case criteria and source links](cases-and-requirements.md#cases-and-interpretation). For maintenance, use [framework ownership and extension](docs/framework-design.md#architecture-extension-and-maintenance) and [shared change impact](../docs/authority-and-change.md#change-impact). Return to the [project README](../README.md) for the wider pipeline.
