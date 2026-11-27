# Structural migration inventory

Baseline **39fbcfdd20ec72b9bc9f7a9f6eb805757224fbad**, branch **clarify**. Use the [119-path relocation record](migration-relocations.md), [297-purpose ledger](migration-test-purposes.tsv) and [E1–E40 verification map](../05-evaluation/docs/evaluator-verification.md) to trace relocated material. Identifiers below remain stable until their recorded closure conditions are met.

## Current ownership

Discovery explores needs and rationale. Formulation owns accepted rules and constraints. Acceptance defines requirements-derived evaluation independently of mechanisms. Design selects mechanisms using Formulation and authorized design decisions. Conformance defines complementary mechanism checks, considering Design, applicable requirements and Acceptance coverage. Candidate realizes Design within delivery constraints. Evaluation selects the Candidate, applies definitions, retains evidence, assesses results and reports findings. Engine interfaces supply reusable execution facilities independently of numbered stages.

This sequence guides test-first work in Acceptance and Conformance. Activities can overlap and findings can reopen earlier decisions. Neither set of test definitions supplies new requirements or design authority. The dependency rule covers links, imports, fixture and helper lookups, subprocesses and test infrastructure. Shared documentation owns cross-stage navigation. The temporary exceptions below preserve existing engineering knowledge.

## Deferred issues

All original paths below refer to **39fbcfdd20ec72b9bc9f7a9f6eb805757224fbad**. Each entry names the preserved material, owner, reason for deferral and observable closure condition.

| ID | Original → current source and owner | Issue and reason retained | Resolution and closure |
| --- | --- | --- | --- |
| M01 | Nine original case specifications and scenario modules under 05-evaluations/deliverables → [Conformance](../03.1-conformance/deliverables/coverage.md). Individual routes follow below. | Clause-based intent, exact fixtures, assertions, functional checks, and the eight human rubrics are operative criteria. Several rely on particular Candidate clauses, explicitly or implicitly. Independent Design derivation has not been established. Reclassification would change the evidence claim. | For each case trace the mechanism and qualifications to approved Design, review the exact criteria and determine their coverage and limits. Close each exception only after the owner accepts the versioned trace and disposition. |
| M02 | Original case Markdown under 05-evaluations/deliverables/cases → [Conformance case specifications](../03.1-conformance/deliverables/cases/). | Preserved forward documentation links reference the Candidate for clause meaning, and integrated evidence, review, reporting and evaluator obligations for interpretation. These links are distinct from executable resource access. | At the owner review, distinguish historical citations from operative criteria and move cross-stage operating instructions or navigation downstream. Close when each forward reference has an accepted disposition and all remaining live references follow the dependency rule. |
| M03 | Original shared evaluator requirements, case **Checks** and runtime verification under 05-evaluations/deliverables → engine, Conformance and [Evaluation verification map](../05-evaluation/docs/evaluator-verification.md). | Compound E obligations retain one canonical owner even when parts are implemented or verified elsewhere. Case-aware runtime modules and mixed scenario tests provisionally stay downstream to preserve coherent verification. | Review local versus integrated responsibilities individually if repartitioning is authorized. Close when each mixed item has an accepted permanent owner and its original verification routes still execute. |
| M04 | Original Formulation baseline, acceptance record, Design decisions and shared clause traces → [Formulation](../02.0-formulation/docs/acceptance-record.md), [Design](../03.0-design/docs/decisions.md), [cross-stage traces](traceability.md#current-traceability-gaps). | Owner-reported acceptance, reconstruction from design/contract, inherited choices lacking independent requirement traces, proposed examples, 28 design illustrations and superseded controls retain their recorded status. Re-deriving intent or inventing traceability exceeds structural scope. | Under appropriate authority, substantiate any missing relationship or explicitly retain its qualification. A reviewed disposition for each claimed trace closes the corresponding gap. |
| M05 | Root README and shared architecture, methodology, authority, traceability, documentation and decision records → root README and docs. | Five-stage provisions and rationale include historical decisions and earlier methodology; status notices mark the transition. Consolidated editorial reconciliation was deferred. | In the documentation increment distinguish historical decisions from current seven-stage guidance, check the newcomer diagram and authority rules, and review links and commands. Close after requester review. |
| M06 | Original clause-based cases and Formulation baseline → [Acceptance coverage](../02.1-acceptance/deliverables/coverage.md) and [Conformance coverage](../03.1-conformance/deliverables/coverage.md). | No independently derived Acceptance cases or adjudicated redundancy decisions exist. Reuse of scenarios alone proves neither coverage nor redundancy. | Develop authorized Acceptance definitions with gaps and limitations. Conformance then reviews potential omissions against criterion and version, independent of past outcomes. Close when the respective owners publish reviewed coverage dispositions. |
| M07 | Original Candidate consumer guides → unchanged [staged sources](architecture.md#staged-sources-and-release-relative-references). Owner: consumer delivery. | The guides' staged pre_* links and the adoption guide's ../LICENSE do not resolve as intended after installation. This inherited delivery issue is outside the structural migration. | Under separate Candidate authorization, verify installed names and license resolution. Close on a tested consumer delivery or an explicitly accepted disposition. |
| M08 | Original integrated operations, framework evidence limits and retained run paths → [running and reviewing](../05-evaluation/docs/running-and-reviewing.md#identify-the-candidate-and-evaluator-used) and engine execution boundaries. Owner: Evaluation. | Existing reports identify the injected contract but do not automatically identify the evaluator revision or dependency versions. Human assessment and environment-specific live/probe verification remain separate obligations. | Preserve any historical run in place, link available contemporaneous provenance and qualify missing data. Close a particular evidence gap only with the corresponding recorded verification or an accepted limitation. |

### Case-level exceptions

The case and module rows in the relocation record supply both original paths. All of the following retain M01/M02 status. The last column lists actual downstream Markdown link destinations by group; a link records a reference, and never by itself demonstrates compliance.

| Original specification (under 05-evaluations/deliverables/cases) | Current definition | Forward references retained |
| --- | --- | --- |
| assumption-disclosure.md | [03.1-conformance/deliverables/cases/assumption-disclosure.md](../03.1-conformance/deliverables/cases/assumption-disclosure.md) | pre_AGENTS.md, running-and-reviewing.md, suite-execution-and-results.md, workspace-and-observation.md |
| bounded-inquiry.md | [03.1-conformance/deliverables/cases/bounded-inquiry.md](../03.1-conformance/deliverables/cases/bounded-inquiry.md) | README.md, agent-execution.md, evidence-and-capture.md, pre_AGENTS.md, running-and-reviewing.md, suite-execution-and-results.md, workspace-and-observation.md |
| contract-change-followthrough.md | [03.1-conformance/deliverables/cases/contract-change-followthrough.md](../03.1-conformance/deliverables/cases/contract-change-followthrough.md) | pre_AGENTS.md, running-and-reviewing.md |
| durable-finding-review.md | [03.1-conformance/deliverables/cases/durable-finding-review.md](../03.1-conformance/deliverables/cases/durable-finding-review.md) | evidence-and-capture.md, pre_AGENTS.md, running-and-reviewing.md, suite-execution-and-results.md, workspace-and-observation.md |
| independent-execution.md | [03.1-conformance/deliverables/cases/independent-execution.md](../03.1-conformance/deliverables/cases/independent-execution.md) | pre_AGENTS.md, running-and-reviewing.md |
| missing-permission.md | [03.1-conformance/deliverables/cases/missing-permission.md](../03.1-conformance/deliverables/cases/missing-permission.md) | evidence-and-capture.md, pre_AGENTS.md, running-and-reviewing.md, suite-execution-and-results.md, workspace-and-observation.md |
| no-safe-next-step.md | [03.1-conformance/deliverables/cases/no-safe-next-step.md](../03.1-conformance/deliverables/cases/no-safe-next-step.md) | evidence-and-capture.md, pre_AGENTS.md, running-and-reviewing.md, suite-execution-and-results.md, workspace-and-observation.md |
| requester-guidance.md | [03.1-conformance/deliverables/cases/requester-guidance.md](../03.1-conformance/deliverables/cases/requester-guidance.md) | pre_AGENTS.md, running-and-reviewing.md, suite-execution-and-results.md, workspace-and-observation.md |
| scope-discipline.md | [03.1-conformance/deliverables/cases/scope-discipline.md](../03.1-conformance/deliverables/cases/scope-discipline.md) | pre_AGENTS.md, workspace-and-observation.md |


Numbered rubric references in assumptions, inquiry and findings, and implicit conditions in the other graders, can become stale without changing offline test results. The technical definition of a correct initial contract is a separate, now resolved executable dependency.

## Relocation of live dependencies

- The former runtime workspace loader read the staged Candidate directly. The durable-finding grader separately reopened the same repository path. The [integrated runner](../05-evaluation/deliverables/evaluation/__main__.py) now selects the path and retains the first successful immutable bytes per invocation. Setup and the [grader](../03.1-conformance/deliverables/conformance/findings.py) receive that reference separately from the observed workspace. A bad initial snapshot remains an infrastructure failure; a later unauthorized edit fails preservation. The launcher continues to retain and hash actual workspace bytes. Engine and isolated definition tests supply synthetic content.
- Some tests formerly grouped under shared runtime verification imported named scenarios or ran the integrated entry point. Case-aware tests, the fake executable and the CLI harness now belong to Evaluation. The functional sandbox adapter remains beside its launcher. Test-only inquiry values can be imported by the downstream verification without collecting another test module.
- The historical run roots are `05-evaluations/.eval-runs/`, `04-evaluations/.eval-runs/`, `evaluations/.eval-runs/` and `_internal/.eval-runs/`. Preflight found none in this checkout. Future integrated runs use `05-evaluation/.eval-runs/`. A timestamp, case name or current checkout cannot supply missing historical provenance. The prior directory may still contain local, ignored Python caches.

## Additional regression purposes

The method ledger counts only original purposes. Four separately discovered checks cover the new interface.

- `conformance.tests.test_findings.FindingsEvaluationTests.test_matching_corrupt_snapshots_cannot_validate_contract_injection`
- `evaluation.tests.runtime.test_candidate_binding.CandidateBindingTests.test_argument_and_auth_operations_do_not_read_the_contract`
- `evaluation.tests.runtime.test_candidate_binding.CandidateBindingTests.test_suite_keeps_first_contract_for_setup_and_independent_grading`
- `evaluation.tests.runtime.test_candidate_binding.CandidateBindingTests.test_unreadable_candidate_is_a_task_failure_with_review_retained`

## Structural verification record

The source checkout began clean at the baseline above. The comparison used Python 3.15.2 and Pydantic Evals 2.68.0 with the original dependency declaration. The three documented [discovery commands and standalone demonstration](../05-evaluation/docs/running-and-reviewing.md#run-offline-checks) passed.

| Discovery root | Original purposes | Added | Executed |
| --- | ---: | ---: | ---: |
| Engine | 58 | 0 | 58 |
| Conformance | 115 | 1 | 116 |
| Evaluation | 124 | 3 | 127 |

The 301 discovered IDs are unique. A separate run copied only the engine into an empty directory and executed its 58 tests and standalone smoke. A second copied only the engine and the Conformance Python package and executed its 116 tests. Both isolated processes ran with the source-checkout import environment removed. Three process-group checks using `/bin/ps`, Unix-socket creation and two special-permission-bit checks required host execution on macOS.

The ordered ten-case configuration comparison included dataset and case IDs, prompts, exact fixtures, expected outputs, evaluator classes, rubrics, functional-check settings and observation flags. The before/after serialized inventories had SHA-256 `7aa8053d60724189fd73e3e40ec3f284ce7089c901857a4a1c279afb4431694a`. Running the same fake success inputs through both full suites returned exit 3 with identical JSON reports, assertion reasons and artifact lists. Text reports differed only in measured durations. The offline tests also exercised non-success outcomes, precedence, continuation, interruption and cleanup.

In a disposable source checkout, the unmodified module command with its default case produced a passing smoke report in `05-evaluation/.eval-runs/`. Its retained contract bytes matched the selected Candidate and its execution hash was `3d7b6c240e0f4b02713d166662d7d95ec74985b9939b23838863acd596407e81`. The complete five-file working Candidate, including modes, reproduced Git tree `68d90bdd425c6f745d5058ebc0f4735f0f0a30c4`. The original and current local run inventories were empty in the working repository.

These are offline structural comparisons. Authenticated agent behavior, real sandbox enforcement and human behavioral verdicts require their own evidence.
