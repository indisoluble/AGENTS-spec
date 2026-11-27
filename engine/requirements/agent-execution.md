# Agent execution

These evaluator requirements govern reusable infrastructure. Checks identify verification methods. Evidence of agent compliance depends on the individual run and assessment.

## E4

When a case finishes or raises, the suite shall remove its temporary workspace.

**Checks.** [`engine/tests/test_smoke.py`](../tests/test_smoke.py), integrated tests for CLI execution policy

## E7

When launching a case, the suite shall require ChatGPT authentication, exclude API-key overrides and personal configuration, and explicitly select model, effort, noninteractive approvals, and a native agent-command permission profile permitting workspace reads/writes, Codex-defined minimal runtime reads, and, on macOS only, read-only access to `/Library/Developer/CommandLineTools`, while denying unrelated filesystem access and command networking.

**Checks.** integrated tests for command construction and execution, [`engine/tests/runtime/test_codex.py`](../tests/runtime/test_codex.py), integrated tests for CLI execution policy, retained command/live run

## E10

If a launched evaluation subprocess times out or evaluation receives SIGINT or SIGTERM, then the suite shall stop the launched process group and retain available evidence under the execution boundaries ([`engine/docs/framework-design.md` § Execution and security boundaries](../docs/framework-design.md#execution-and-security-boundaries)).

**Checks.** integrated tests for CLI execution policy
