# 04 — Evaluations

Evaluations uses a [staged contract candidate](../03-contract/prerelease_AGENTS.md) and defined cases to assess how agents behave. Runs produce observations and automated assertion results, with human review for criteria that require judgment. The current behavioral cases exercise contract clauses. Requirements-derived acceptance testing remains future work. Behavioral verification is limited to what the evidence supports for the candidate and cases run. Offline tests verify evaluator machinery.

- To understand what the suite assesses, read the [evaluation model and coverage limits](docs/evaluation-model.md#purpose-and-evaluation-model).
- For the infrastructure check, see [smoke](deliverables/cases/smoke.md). For the greeting edit and its scope boundary, see [scope-discipline](deliverables/cases/scope-discipline.md).
- For a missing source timezone, see [requester-guidance](deliverables/cases/requester-guidance.md). For routine exporter changes with a known UTC source, see [independent-execution](deliverables/cases/independent-execution.md). For a date interpretation authorized for a disposable preview, see [assumption-disclosure](deliverables/cases/assumption-disclosure.md).
- For cleanup involving a designated rollback release, see [missing-permission](deliverables/cases/missing-permission.md). For a schedule that exceeds its budget or delivery window, see [no-safe-next-step](deliverables/cases/no-safe-next-step.md).
- For the importer duplicate-policy change and its follow-through across code, tests, requirements, and documentation, see [contract-change-followthrough](deliverables/cases/contract-change-followthrough.md).
- To find any registered case, use the [case overview](deliverables/cases-and-requirements.md#cases-and-interpretation) for its purpose, assertions, human review, and links to source and tests.
- To assess the exporter decision, interpret partial measurements, or review inquiry conduct, use the [bounded-inquiry case specification](deliverables/cases/bounded-inquiry.md).
- To run an evaluation, follow the [setup and run guide](docs/running-and-reviewing.md#setup-and-running-evaluations) or go to the [case and suite commands](docs/running-and-reviewing.md#run-a-case-or-the-suite).
- To interpret a result, read the [outcomes and exit codes](docs/running-and-reviewing.md#outcomes-and-exit-codes) and inspect the [retained evidence](docs/running-and-reviewing.md#retained-evidence). Use the [human review guidance](docs/running-and-reviewing.md#response-presence-and-human-review) or the [failure investigation guide](docs/running-and-reviewing.md#investigate-a-failure-or-incomplete-result) as applicable.
- To understand the framework, see its [component responsibilities](docs/framework-design.md#responsibilities-and-dependency-direction), [interfaces](docs/framework-design.md#interfaces-used-by-scenarios-and-substitutes), and [architecture decisions](docs/framework-design.md#architecture-decisions).
- To maintain a case, follow [Change a scenario](docs/maintaining-evaluations.md#change-a-scenario) or [Add a scenario](docs/maintaining-evaluations.md#add-a-scenario).
- To maintain shared evaluator code, follow [Change shared evaluator functionality](docs/maintaining-evaluations.md#change-shared-evaluator-functionality). Both workflows use [Verify a behavior change](docs/maintaining-evaluations.md#verify-a-behavior-change).

## Evaluator requirements

For obligations specific to a case, see [E2 for smoke](deliverables/cases/smoke.md#e2), [E13](deliverables/cases/scope-discipline.md#e13) and [E18](deliverables/cases/scope-discipline.md#e18) for scope-discipline, [E25 for requester-guidance](deliverables/cases/requester-guidance.md#e25), [E32 for independent-execution](deliverables/cases/independent-execution.md#e32), [E35 for assumption-disclosure](deliverables/cases/assumption-disclosure.md#e35), [E36 for missing-permission](deliverables/cases/missing-permission.md#e36), [E37 for no-safe-next-step](deliverables/cases/no-safe-next-step.md#e37), [E38 for contract-change-followthrough](deliverables/cases/contract-change-followthrough.md#e38), [E39 for bounded-inquiry](deliverables/cases/bounded-inquiry.md#e39), and [E40 for durable-finding-review](deliverables/cases-and-requirements.md#e40). For shared evaluator behavior, choose the responsibility you are working on.

- [Agent execution](deliverables/requirements/agent-execution.md)
- [Workspace preparation and observation](deliverables/requirements/workspace-and-observation.md)
- [Evidence retention and capture](deliverables/requirements/evidence-and-capture.md)
- [Suite execution and results](deliverables/requirements/suite-execution-and-results.md)
- [Functional checks](deliverables/requirements/functional-checks.md)
