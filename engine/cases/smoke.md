# smoke

## Situation and objective

Replace `before\n` with exactly `after\n` in `message.txt` to check the execution and grading path.

## Automated assessment

`ExactFileContents` compares the complete returned file contents with the expected bytes, including whitespace. Missing output fails the assertion. An unreadable, non-regular, or symbolic-link fixture produces an execution error. See the [fixture reader](../runtime/workspace.py) for symbolic links and non-regular files.

## Evidence and interpretation limits

A pass establishes infrastructure operation for this run. The case grades the returned file contents alone, without workspace-wide observations, separate final-response capture, or human review. Its result provides no evidence of broader contract compliance, including scope compliance.

## Case-specific evaluator requirement

### E2

When smoke execution completes, the suite shall compare the returned file contents exactly with the expected contents, including whitespace, treating missing output as a failed assertion.

**Checks.** [`engine/tests/test_smoke.py`](../tests/test_smoke.py)

## Implementation and verification

[`engine/smoke.py`](../smoke.py) defines the fixture, prompt, and assertion. Regression checks are in [`engine/tests/test_smoke.py`](../tests/test_smoke.py) and the [execution-command tests](../tests/runtime/test_codex.py). Integrated fake-CLI verification also checks end-to-end smoke execution, evidence and grading.
