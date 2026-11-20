# 04 — Evaluations

Evaluations uses a [staged contract candidate](../03-contract/prerelease_AGENTS.md) and defined cases to assess how agents behave. Runs produce observations and automated assertion results, with human review for criteria that require judgment. The current behavioral cases exercise contract clauses. Requirements-derived acceptance testing remains future work. Behavioral verification is limited to what the evidence supports for the candidate and cases run. Offline tests verify evaluator machinery.

- To understand what the suite assesses, read the [evaluation model and coverage limits](docs/evaluation-model.md#purpose-and-evaluation-model).
- To run an evaluation, follow the [setup and run guide](docs/running-and-reviewing.md#setup-and-running-evaluations) or go to the [case and suite commands](docs/running-and-reviewing.md#run-a-case-or-the-suite).
- To interpret a result, read the [outcomes and exit codes](docs/running-and-reviewing.md#outcomes-and-exit-codes) and inspect the [retained evidence](docs/running-and-reviewing.md#retained-evidence). Use the [human review guidance](docs/running-and-reviewing.md#response-presence-and-human-review) or the [failure investigation guide](docs/running-and-reviewing.md#investigate-a-failure-or-incomplete-result) as applicable.
- To understand the framework, see its [component responsibilities](docs/framework-design.md#responsibilities-and-dependency-direction), [interfaces](docs/framework-design.md#interfaces-used-by-scenarios-and-substitutes), and [architecture decisions](docs/framework-design.md#architecture-decisions).
- To maintain a case, follow [Change a scenario](docs/maintaining-evaluations.md#change-a-scenario) or [Add a scenario](docs/maintaining-evaluations.md#add-a-scenario).
- To maintain shared evaluator code, follow [Change shared evaluator functionality](docs/maintaining-evaluations.md#change-shared-evaluator-functionality). Both workflows use [Verify a behavior change](docs/maintaining-evaluations.md#verify-a-behavior-change).

## Case specifications

Each specification gives the case's assessment criteria, interpretation limits, case-specific evaluator requirements, and links to source and tests. The suite requirements define [accepted case selections](deliverables/requirements/suite-execution-and-results.md#e12) and [execution order](deliverables/requirements/suite-execution-and-results.md#e15).

**Fully automated**

- [smoke](deliverables/cases/smoke.md) checks the execution and grading path with an exact text edit. [E2](deliverables/cases/smoke.md#e2)
- [scope-discipline](deliverables/cases/scope-discipline.md) checks a greeting change with an unrelated typo in the same file. [E13](deliverables/cases/scope-discipline.md#e13), [E18](deliverables/cases/scope-discipline.md#e18)

**Human review required**

- [requester-guidance](deliverables/cases/requester-guidance.md) asks for UTC output when the source timezone is unknown. [E25](deliverables/cases/requester-guidance.md#e25)
- [independent-execution](deliverables/cases/independent-execution.md) requests the exporter change and regression tests when the source timezone is known. [E32](deliverables/cases/independent-execution.md#e32)
- [assumption-disclosure](deliverables/cases/assumption-disclosure.md) permits either date interpretation for a disposable preview. [E35](deliverables/cases/assumption-disclosure.md#e35)
- [missing-permission](deliverables/cases/missing-permission.md) requests cleanup where retiring a designated rollback release needs approval. [E36](deliverables/cases/missing-permission.md#e36)
- [no-safe-next-step](deliverables/cases/no-safe-next-step.md) presents a scheduling conflict that requires changing a consequential constraint. [E37](deliverables/cases/no-safe-next-step.md#e37)
- [contract-change-followthrough](deliverables/cases/contract-change-followthrough.md) follows an importer policy change across code, tests, requirements, and documentation. [E38](deliverables/cases/contract-change-followthrough.md#e38)
- [bounded-inquiry](deliverables/cases/bounded-inquiry.md) assesses an exporter choice under a fixed workload and resource limit. [E39](deliverables/cases/bounded-inquiry.md#e39)
- [durable-finding-review](deliverables/cases/durable-finding-review.md) examines exact reconstruction from a customer CSV report and recording a substantiated limitation. [E40](deliverables/cases/durable-finding-review.md#e40)

## Evaluator requirements

The [case specifications](#case-specifications) own the case-specific requirements. Five shared specifications cover the following evaluator responsibilities.

- [Agent execution](deliverables/requirements/agent-execution.md)
- [Workspace preparation and observation](deliverables/requirements/workspace-and-observation.md)
- [Evidence retention and capture](deliverables/requirements/evidence-and-capture.md)
- [Suite execution and results](deliverables/requirements/suite-execution-and-results.md)
- [Functional checks](deliverables/requirements/functional-checks.md)
