# Agent execution

These requirements cover authentication, command permissions, execution errors, cancellation, and workspace cleanup. See [`engine/docs/framework-design.md` § Execution and security boundaries](../../../engine/docs/framework-design.md#execution-and-security-boundaries) and the operator guidance on credentials ([`05-evaluation/docs/running-and-reviewing.md` § Authentication and credential lifetime](../../docs/running-and-reviewing.md#authentication-and-credential-lifetime)).

These requirements govern evaluator behavior. The product baseline ([`02.0-formulation/deliverables/baseline.md`](../../../02.0-formulation/deliverables/baseline.md)) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E3

If execution reports an error or raises an exception, then the suite shall report an execution failure separately from content assertions.

**Checks.** [`engine/tests/test_smoke.py`](../../../engine/tests/test_smoke.py), [`05-evaluation/deliverables/evaluation/tests/runtime/test_cli.py`](../evaluation/tests/runtime/test_cli.py)

## E6

The suite shall use `~/.codex-evals` by default, or the selected `--codex-home`, for login, logout, and evaluation, retaining credentials until explicit logout and delegating credential removal to Codex for that profile only.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/runtime/test_auth.py`](../evaluation/tests/runtime/test_auth.py)
