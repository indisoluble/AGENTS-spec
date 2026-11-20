# Functional checks

These requirements cover the sandbox, results, failures, cleanup, and evidence for evaluator-owned checks. [E33](#e33) and [E34](#e34) govern both [independent-execution](../cases/independent-execution.md) and [contract-change-followthrough](../cases-and-requirements.md#contract-change-followthrough). The [functional-check design](../../docs/framework-design.md#functional-check-execution) explains how the runner and scenarios divide this work.

These requirements govern evaluator behavior. The [product baseline](../../../01-behavior/deliverables/baseline.md) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E28

When executing an evaluator-owned Python check, the functional-check runner shall use the Codex read-only, network-disabled sandbox and a fresh temporary profile without authentication, model calls, or an unsandboxed fallback.

**Checks.** [test_functional.py](../tests/runtime/test_functional.py), [sandbox probe](../tests/probe_functional_sandbox.py)

## E29

When a functional check returns, the runner shall report its exit status and exact output bytes separately from launcher diagnostics, including nonzero exits as observations rather than inventing a behavioral verdict.

**Checks.** [test_functional.py](../tests/runtime/test_functional.py)

## E30

If functional-check setup, launch, adapter response, timeout, or cancellation fails, then the runner shall return an explicit error and retain available captured output without retrying.

**Checks.** [test_functional.py](../tests/runtime/test_functional.py)

## E31

When a functional-check invocation finishes, the runner shall stop its launched process group and remove its temporary profile; checks shall use the [defined positive finite timeout and outer allowance](../../docs/framework-design.md#deadlines-and-cleanup).

**Checks.** [test_functional.py](../tests/runtime/test_functional.py)

## E33

When checking independent-execution or contract-change-followthrough output after agent cleanup, the suite shall run the selected case's evaluator-owned scripts (two for independent-execution, three for contract-change-followthrough) sequentially before workspace removal, fail affected assertions for observed missing/non-regular required files without executing them, and distinguish completed nonzero checks from infrastructure errors.

**Checks.** [test_independence.py](../tests/scenarios/test_independence.py), [test_followthrough.py](../tests/scenarios/test_followthrough.py), [test_cli.py](../tests/runtime/test_cli.py), [test_functional.py](../tests/runtime/test_functional.py), [test_functional_checks.py](../tests/runtime/test_functional_checks.py)

## E34

When retaining independent-execution or contract-change-followthrough evidence, the suite shall attempt to save each check's source, status, exit code or error, exact available output and launcher diagnostics, and skipped-check reasons independently, preserving primary errors and treating evidence-write failures as infrastructure errors.

**Checks.** [test_independence.py](../tests/scenarios/test_independence.py), [test_followthrough.py](../tests/scenarios/test_followthrough.py), [test_functional_checks.py](../tests/runtime/test_functional_checks.py)
