# Maintaining evaluations

Paths beginning with `deliverables/` are relative to `04-evaluations/`. For both scenario and shared evaluator changes, use ordinary functions and existing typed result records for composition, `Path` for filesystem boundaries, and bytes where exact fixture or evidence preservation matters.

When applied in a consuming project, the candidate contract's [engineering rules](../../03-contract/prerelease_AGENTS.md#12-do--perform-the-authorized-work) and [validation rules](../../03-contract/prerelease_AGENTS.md#13-study--assess-completion-and-learning) cover production modules, tests, fixtures, and testing utilities alike. In this repository the staged candidate serves only as source material.

## Change a scenario

Start with the [case specification](../README.md#case-specifications) for the intended behavior, assessment criteria, and links to the scenario module and tests. A scenario change should normally involve those local owners, one `CASES` entry where configuration changes, and affected documentation.

The scenario module owns the task, fixture, dataset, evaluators, and optional human rubric. Reuse shared execution, workspace observation, response capture, and evidence mechanisms. In the CLI entry, register a lazy dataset factory. Select the existing observation and review settings and, only where needed, the post-execution functional check. Keep that check after agent cleanup and before fixture removal.

## Add a scenario

1. Create `deliverables/scenarios/<module>.py` with `PROMPT`, the fixture bytes, its evaluators, and a dataset factory returning a one-case `Dataset`. Add `REVIEW_RUBRIC` and a `check_execution` wrapper over `functional_checks.run_checks` only if the case needs them. Import shared mechanisms from `deliverables.runtime`.
2. Add a `CaseConfig` entry to `CASES` in [deliverables/__main__.py](../deliverables/__main__.py) at the position defined by [E15](../deliverables/requirements/suite-execution-and-results.md#e15). The `--case` choices and the `all` order come from that collection.
3. Teach [fake_codex.py](../deliverables/tests/support/fake_codex.py) to recognize the case from its prompt or fixture and to produce the scripted responses its tests need.
4. Add `deliverables/tests/scenarios/test_<module>.py` with grading tests through `evaluate()` and a `<Name>CLITests(FakeCodexCLI, unittest.TestCase)` class for CLI composition, evidence, and failure classification.
5. In [test_cli.py](../deliverables/tests/runtime/test_cli.py), update the tests that enumerate every case. They cover all-cases order and evidence, late-case precedence, and aggregate exit codes.
6. Create `deliverables/cases/<case-name>.md` with its assessment, interpretation limits, case-specific requirements, and links to its module and tests. Link it from the [stage README](../README.md#case-specifications). Adding a case requires authorization to change the [accepted selections (E12)](../deliverables/requirements/suite-execution-and-results.md#e12) and [suite order (E15)](../deliverables/requirements/suite-execution-and-results.md#e15).
7. [Verify the change](#verify-a-behavior-change), including the offline checks.

## Change shared evaluator functionality

Locate the affected component in [framework responsibilities](framework-design.md#responsibilities-and-dependency-direction) and its applicable [shared requirements and their Checks](../README.md#evaluator-requirements). Keep common mechanisms with the component responsible for them. Two callers alone do not justify a generic utility. Keep case-specific grading policy in the scenario module.

Preserve the [interfaces used by scenarios and substitutes](framework-design.md#interfaces-used-by-scenarios-and-substitutes). Supply execution dependencies at the existing callable boundary for offline tests. Keep missing observations distinct from empty state and infrastructure errors distinct from false assertions.

## Verify a behavior change

Use the existing substitutes and fake CLI to verify outcomes, independent assertions, error classification, evidence, and resource cleanup at the affected boundary. Preserve meaningful negative cases. Derive expected results independently of production grading and configuration logic. Keep scenario-specific test expectations local, sharing setup only when it clarifies the tests.

When behavior changes, update the assessment and interpretation in the affected [case specification](../README.md#case-specifications). Update [E1–E40](../README.md#evaluator-requirements) only through an authorized requirement change. Source remains canonical for exact fixture bytes, prompts, check scripts, and rubric text. Check direct documentation links.

Behavioral case specifications link their assessments to contract clauses. Rubrics in [assumptions.py](../deliverables/scenarios/assumptions.py), [inquiry.py](../deliverables/scenarios/inquiry.py), and [findings.py](../deliverables/scenarios/findings.py) cite section numbers and rule strengths. Other rubrics refer to retained rules without numbering them. Assertions can encode a clause implicitly, as `ScopePreserved` does for §1.2 in [scope.py](../deliverables/scenarios/scope.py). No repository check detects when renumbering, a heading change, or a change in meaning leaves those expectations stale.

Run the [offline checks](running-and-reviewing.md#run-offline-checks). The [case specifications](../README.md#case-specifications) and [evaluator requirements](../README.md#evaluator-requirements) link the relevant regression tests. The [shared tests](../deliverables/tests/runtime) cover authentication, cancellation, filesystem observation, and evidence failures. For human-rubric changes, also compare the revised criteria with the applicable contract provisions, preserving rule strengths, triggers, exceptions, evidence limits, and unaffected technical checks. Offline tests verify infrastructure and technical assertions. They cannot establish rubric semantic validity or live contractual compliance. See the [evaluation model](evaluation-model.md#purpose-and-evaluation-model) for the limits of behavioral evidence.

Live verification requires inspecting one [separately authorized run](running-and-reviewing.md#run-a-case-or-the-suite). If authorization covers only offline work, stop after that verification and report live assessment as pending. The [functional-check sandbox probe](framework-design.md#functional-check-execution) checks that separate boundary's runtime enforcement. Verification of the evaluated-agent permission profile and authenticated integration follows the distinct scopes in [agent execution](framework-design.md#agent-execution).

Inspect the [retained evidence](running-and-reviewing.md#retained-evidence) for the live run's selected case, assertions and reasons, initial/final bytes and available manifests, contract hash, model settings, and cleaned workspace path. For human-review cases, also inspect response capture, readable differences, the retained rubric, and pending-review reporting, and follow the [human review procedure](running-and-reviewing.md#response-presence-and-human-review) to assess the rubric with the requester. For independent-execution and contract-change-followthrough, include functional-check evidence. Each executed case should produce a distinct workspace and evidence directory. Keep run-specific findings and results with that evidence.
