# Agent execution

These requirements cover authentication, command permissions, execution errors, cancellation, and workspace cleanup. See the [execution and security boundaries](../../docs/framework-design.md#execution-and-security-boundaries) and the [operator guidance on credentials](../../docs/running-and-reviewing.md#authentication-and-credential-lifetime).

These requirements govern evaluator behavior. The [product baseline](../../../02-formulation/deliverables/baseline.md) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E3

If execution reports an error or raises an exception, then the suite shall report an execution failure separately from content assertions.

**Checks.** [test_smoke.py](../tests/scenarios/test_smoke.py), [test_cli.py](../tests/runtime/test_cli.py)

## E4

When a case finishes or raises, the suite shall remove its temporary workspace.

**Checks.** [test_smoke.py](../tests/scenarios/test_smoke.py), [test_cli.py](../tests/runtime/test_cli.py)

## E6

The suite shall use `~/.codex-evals` by default, or the selected `--codex-home`, for login, logout, and evaluation, retaining credentials until explicit logout and delegating credential removal to Codex for that profile only.

**Checks.** [test_auth.py](../tests/runtime/test_auth.py)

## E7

When launching a case, the suite shall require ChatGPT authentication, exclude API-key overrides and personal configuration, and explicitly select model, effort, noninteractive approvals, and a native agent-command permission profile permitting workspace reads/writes, Codex-defined minimal runtime reads, and, on macOS only, read-only access to `/Library/Developer/CommandLineTools`, while denying unrelated filesystem access and command networking.

**Checks.** [test_codex.py](../tests/runtime/test_codex.py), [test_cli.py](../tests/runtime/test_cli.py), retained command/live run

## E10

If a launched evaluation subprocess times out or evaluation receives SIGINT or SIGTERM, then the suite shall stop the launched process group and retain available evidence under the [execution boundaries](../../docs/framework-design.md#execution-and-security-boundaries).

**Checks.** [test_cli.py](../tests/runtime/test_cli.py)
