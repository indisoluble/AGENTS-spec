# Functional checks

These evaluator requirements govern reusable infrastructure. Checks identify verification methods. Evidence of agent compliance depends on the individual run and assessment.

## E28

When executing an evaluator-owned Python check, the functional-check runner shall use the Codex read-only, network-disabled sandbox and a fresh temporary profile without authentication, model calls, or an unsandboxed fallback.

**Checks.** [`engine/tests/runtime/test_functional.py`](../tests/runtime/test_functional.py), sandbox probe ([`engine/tests/probe_functional_sandbox.py`](../tests/probe_functional_sandbox.py))

## E29

When a functional check returns, the runner shall report its exit status and exact output bytes separately from launcher diagnostics, including nonzero exits as observations rather than inventing a behavioral verdict.

**Checks.** [`engine/tests/runtime/test_functional.py`](../tests/runtime/test_functional.py)

## E30

If functional-check setup, launch, adapter response, timeout, or cancellation fails, then the runner shall return an explicit error and retain available captured output without retrying.

**Checks.** [`engine/tests/runtime/test_functional.py`](../tests/runtime/test_functional.py)

## E31

When a functional-check invocation finishes, the runner shall stop its launched process group and remove its temporary profile; checks shall use the defined positive finite timeout and outer allowance ([`engine/docs/framework-design.md` § Deadlines and cleanup](../docs/framework-design.md#deadlines-and-cleanup)).

**Checks.** [`engine/tests/runtime/test_functional.py`](../tests/runtime/test_functional.py)
