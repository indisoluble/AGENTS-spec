# Functional checks

These evaluator requirements govern the selected functional checks for independent-execution and contract-change-followthrough. Both [independent-execution](../cases/independent-execution.md) and [contract-change-followthrough](../cases/contract-change-followthrough.md) apply these requirements through the [functional-check runner](../../../engine/docs/framework-design.md#functional-check-execution). Checks identify verification methods. Evidence of agent compliance depends on the individual run and assessment.

## E33

When checking independent-execution or contract-change-followthrough output after agent cleanup, the suite shall run the selected case's evaluator-owned scripts (two for independent-execution, three for contract-change-followthrough) sequentially before workspace removal, fail affected assertions for observed missing/non-regular required files without executing them, and distinguish completed nonzero checks from infrastructure errors.

**Checks.** integrated tests for independent-execution, integrated tests for contract-change-followthrough, [`03.1-conformance/deliverables/conformance/tests/test_followthrough.py`](../conformance/tests/test_followthrough.py), integrated tests for CLI execution policy, [`engine/tests/runtime/test_functional.py`](../../../engine/tests/runtime/test_functional.py), [`engine/tests/runtime/test_functional_checks.py`](../../../engine/tests/runtime/test_functional_checks.py)

## E34

When retaining independent-execution or contract-change-followthrough evidence, the suite shall attempt to save each check's source, status, exit code or error, exact available output and launcher diagnostics, and skipped-check reasons independently, preserving primary errors and treating evidence-write failures as infrastructure errors.

**Checks.** integrated tests for independent-execution, integrated tests for contract-change-followthrough, [`03.1-conformance/deliverables/conformance/tests/test_followthrough.py`](../conformance/tests/test_followthrough.py), [`engine/tests/runtime/test_functional_checks.py`](../../../engine/tests/runtime/test_functional_checks.py)
