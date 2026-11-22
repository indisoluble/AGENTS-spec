# 05 — Evaluations

Evaluations defines what a check will look for and assesses what happened when an agent received the [staged contract](../04-candidate/pre_AGENTS.md). In requirements-led work the expectation comes from accepted intent in Formulation, before it guides authorized Design and Candidate work. The current behavioral cases instead exercise selected contract clauses. The [shared stage interfaces](../docs/architecture.md#stage-interfaces) and [shared clause index](../docs/contract-traces.md#contract-clause-index) identify the upstream owners.

Start with the [case catalog](#case-specifications) for a fixture and its assessment, or the [evaluator requirements](#evaluator-requirements) for what the suite itself must do.

- To understand what the suite assesses, read the [evaluation model and coverage limits](docs/evaluation-model.md#purpose-and-evaluation-model).
- For a first run, start with [setup](docs/running-and-reviewing.md#setup-and-running-evaluations). Use the [offline checks](docs/running-and-reviewing.md#run-offline-checks) to test the evaluator, or the [case and suite commands](docs/running-and-reviewing.md#run-a-case-or-the-suite) for a live agent evaluation.
- To interpret a result, read the [outcomes and exit codes](docs/running-and-reviewing.md#outcomes-and-exit-codes) and inspect the [retained evidence](docs/running-and-reviewing.md#retained-evidence). Use the [human review guidance](docs/running-and-reviewing.md#response-presence-and-human-review) or the [failure investigation guide](docs/running-and-reviewing.md#investigate-a-failure-or-incomplete-result) as applicable.
- To understand the framework, follow a [case through its components](docs/framework-design.md#walkthrough-scope-discipline), look up the [shared interfaces](docs/framework-design.md#interfaces-used-by-scenarios-and-substitutes), or trace the [agent permissions and their validation](docs/framework-design.md#agent-execution) to the [architecture decisions](docs/framework-design.md#architecture-decisions).
- To define or revise an expectation, first [identify its source](docs/maintaining-evaluations.md#establish-the-expectation). Then follow [Change a scenario](docs/maintaining-evaluations.md#change-a-scenario) or [Add a scenario](docs/maintaining-evaluations.md#add-a-scenario).
- To maintain shared evaluator code, follow [Change shared evaluator functionality](docs/maintaining-evaluations.md#change-shared-evaluator-functionality). Both workflows use [Verify a behavior change](docs/maintaining-evaluations.md#verify-a-behavior-change).

## Case specifications

Each specification explains the task, assessment and limits, with links to the scenario that owns the exact inputs and grading and to its offline tests. Of the ten registered cases, smoke checks the evaluator path and the other nine exercise contract clauses. The groupings below tell you who grades the case. [E12](deliverables/requirements/suite-execution-and-results.md#e12) defines the accepted selections and [E15](deliverables/requirements/suite-execution-and-results.md#e15) defines suite order.

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

E1–E40 specify what the evaluator must do. Eleven belong to the [individual cases above](#case-specifications). The other 29 are grouped below. Under each requirement, **Checks** identifies ways to verify it. A listed live check or human review requires corresponding run evidence before anyone can claim it succeeded.

| Shared specification | IDs | What the requirements protect |
| --- | --- | --- |
| [Agent execution](deliverables/requirements/agent-execution.md) | E3, E4, E6, E7, E10 | Run within the selected authentication and command boundaries, stop launched work, clean up the workspace and distinguish execution errors from grades. [Execution boundaries](docs/framework-design.md#execution-and-security-boundaries) |
| [Workspace preparation and observation](deliverables/requirements/workspace-and-observation.md) | E1, E5, E16, E17, E19, E20, E22 | Give each case its intended starting state and obtain comparable observations, including when a file is missing or inspection fails. [Workspace implementation](deliverables/runtime/workspace.py) |
| [Evidence retention and capture](deliverables/requirements/evidence-and-capture.md) | E8, E9, E21, E23, E24, E27 | Let a reviewer reconstruct what was observed and why an assertion passed or failed after the workspace is gone. [Retained evidence](docs/running-and-reviewing.md#retained-evidence) |
| [Suite execution and results](deliverables/requirements/suite-execution-and-results.md) | E11, E12, E14, E15, E26 | Attribute each result to its case and keep errors, false assertions and pending human review distinguishable across a suite run. [CLI and reporting](deliverables/__main__.py) |
| [Functional checks](deliverables/requirements/functional-checks.md) | E28–E31, E33, E34 | Run evaluator-owned scripts on eligible fixture files within a separate sandbox and retain enough evidence to distinguish a failed check from a launcher error. [Functional-check execution](docs/framework-design.md#functional-check-execution) |
