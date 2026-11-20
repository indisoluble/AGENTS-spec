# 04 — Evaluations

Evaluations uses a [staged contract candidate](../03-contract/prerelease_AGENTS.md) and defined cases to assess how agents behave. Runs produce observations and automated assertion results, with human review for criteria that require judgment. The current behavioral cases exercise contract clauses. Requirements-derived acceptance testing remains future work. Behavioral verification is limited to what the evidence supports for the candidate and cases run. Offline tests verify evaluator machinery.

- To understand what the suite assesses, read the [evaluation model and coverage limits](docs/evaluation-model.md#purpose-and-evaluation-model).
- To find a case, use the [case catalogue](deliverables/cases-and-requirements.md#cases-and-interpretation) for its purpose, assertions, human review, and links to source and tests.
- To understand what the evaluator itself must do, see the [verifiable evaluator requirements E1–E40](deliverables/cases-and-requirements.md#verifiable-requirements).
- To run an evaluation, follow the [setup and run guide](docs/running-and-reviewing.md#setup-and-running-evaluations) or go to the [case and suite commands](docs/running-and-reviewing.md#run-a-case-or-the-suite).
- To interpret a result, read the [outcomes and exit codes](docs/running-and-reviewing.md#outcomes-and-exit-codes) and inspect the [retained evidence](docs/running-and-reviewing.md#retained-evidence). Use the [human review guidance](docs/running-and-reviewing.md#response-presence-and-human-review) or the [failure investigation guide](docs/running-and-reviewing.md#investigate-a-failure-or-incomplete-result) as applicable.
- To understand the framework, see its [component responsibilities](docs/framework-design.md#responsibilities-and-dependency-direction), [interfaces](docs/framework-design.md#interfaces-used-by-scenarios-and-substitutes), and [architecture decisions](docs/framework-design.md#architecture-decisions).
- To maintain a case, follow [Change a scenario](docs/maintaining-evaluations.md#change-a-scenario) or [Add a scenario](docs/maintaining-evaluations.md#add-a-scenario).
- To maintain shared evaluator code, follow [Change shared evaluator functionality](docs/maintaining-evaluations.md#change-shared-evaluator-functionality). Both workflows use [Verify a behavior change](docs/maintaining-evaluations.md#verify-a-behavior-change).
