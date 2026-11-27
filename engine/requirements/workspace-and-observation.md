# Workspace preparation and observation

These evaluator requirements govern reusable infrastructure. Checks identify verification methods. Evidence of agent compliance depends on the individual run and assessment.

## E1

When a case starts, the suite shall provide a fresh temporary workspace containing that case's initial fixture and an unchanged copy of the current root contract.

**Checks.** [`engine/tests/test_smoke.py`](../tests/test_smoke.py), integrated tests for scope comparisons and grading, fixture and grading tests for scope comparisons and grading, integrated tests for requester-guidance, live run

## E16

When capturing a workspace snapshot, the inspector shall record relative paths, entry types, POSIX permission and special mode bits, exact regular-file bytes, and symbolic-link targets, without following links or opening special-file contents.

**Checks.** [`engine/tests/runtime/test_workspace.py`](../tests/runtime/test_workspace.py)

## E17

If inspection of an existing workspace tree fails, then the inspector shall raise an inspection error instead of returning a partial snapshot.

**Checks.** [`engine/tests/runtime/test_workspace.py`](../tests/runtime/test_workspace.py)

## E22

When given a fixture mapping, workspace preparation shall create exactly those regular files and their parent directories alongside the unchanged root contract, adding no default fixture when the mapping is empty. If a fixture path would escape the workspace or override the root contract, then workspace preparation shall reject it. When called without a fixture mapping, the smoke convenience helper shall supply the default `message.txt` fixture with the selected initial contents. When called with a fixture mapping, including an empty one, the smoke convenience helper shall use that mapping instead of the default.

**Checks.** [`engine/tests/runtime/test_capture.py`](../tests/runtime/test_capture.py), [`engine/tests/test_smoke.py`](../tests/test_smoke.py)
