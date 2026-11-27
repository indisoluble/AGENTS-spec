# Workspace preparation and observation

These requirements cover the workspace each case receives, the fixture mappings used to prepare it, and the filesystem state available for grading. The observation boundaries ([`engine/docs/framework-design.md` § Observation and capture boundaries](../../../engine/docs/framework-design.md#observation-and-capture-boundaries)) explain what a snapshot records and which changes it can reveal.

These requirements govern evaluator behavior. The product baseline ([`02.0-formulation/deliverables/baseline.md`](../../../02.0-formulation/deliverables/baseline.md)) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E5

If a fixture is a symbolic link or non-regular file, then the suite shall avoid reading its contents, treating it as an execution error for smoke and using its observed entry type for behavioral-case assessment.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/runtime/test_evidence.py`](../evaluation/tests/runtime/test_evidence.py), [`05-evaluation/deliverables/evaluation/tests/scenarios/test_scope.py`](../evaluation/tests/scenarios/test_scope.py), [`03.1-conformance/deliverables/conformance/tests/test_scope.py`](../../../03.1-conformance/deliverables/conformance/tests/test_scope.py), [`05-evaluation/deliverables/evaluation/tests/scenarios/test_assumptions.py`](../evaluation/tests/scenarios/test_assumptions.py)

## E19

When running a behavioral case, the suite shall capture initial state before execution and final state after process cleanup, retain available snapshot manifests and fixture bytes ([`05-evaluation/docs/running-and-reviewing.md` § Retained evidence](../../docs/running-and-reviewing.md#retained-evidence)), and grade the captured observations.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_scope.py`](../evaluation/tests/scenarios/test_scope.py), [`03.1-conformance/deliverables/conformance/tests/test_scope.py`](../../../03.1-conformance/deliverables/conformance/tests/test_scope.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_evidence.py`](../evaluation/tests/runtime/test_evidence.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_cli.py`](../evaluation/tests/runtime/test_cli.py), live run

## E20

If a required workspace observation is missing or inspection fails, then the suite shall report an error rather than successful scope preservation, preserving any primary execution error and available evidence.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_scope.py`](../evaluation/tests/scenarios/test_scope.py), [`03.1-conformance/deliverables/conformance/tests/test_scope.py`](../../../03.1-conformance/deliverables/conformance/tests/test_scope.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_evidence.py`](../evaluation/tests/runtime/test_evidence.py)
