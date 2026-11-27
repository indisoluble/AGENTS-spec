# Evidence retention and capture

These evaluator requirements govern reusable infrastructure. Checks identify verification methods. Evidence of agent compliance depends on the individual run and assessment.

## E9

If an initial evidence write (`AGENTS.md`, optional `message.txt`, or `prompt.txt`) fails, then the suite shall stop normal setup before agent launch and preserve and report the primary infrastructure error through cleanup and available evidence retention, without requiring further initial writes. If a subsequent evidence-retention write fails, then the suite shall preserve primary execution/check errors, attempt remaining independent writes, and report write errors in the terminal.

**Checks.** integrated tests for evidence retention

## E23

When final-response capture is enabled, the launcher shall capture the CLI's final message separately from progress outside the agent workspace, preserve its text exactly including empty text, and report capture/read failures as infrastructure errors while preserving any primary execution error and available evidence.

**Checks.** [`engine/tests/runtime/test_capture.py`](../tests/runtime/test_capture.py)

## E24

When retaining workspace observations, the suite shall independently attempt each snapshot manifest and regular-file copy, using captured bytes without following links or recreating special files.

**Checks.** [`engine/tests/runtime/test_capture.py`](../tests/runtime/test_capture.py), integrated tests for evidence retention

## E27

When retaining workspace observations, the suite shall attempt to save a readable report of all observed entry/content differences independently of other evidence writes, distinguishing incomplete inspection from an unchanged workspace and assigning no behavioral verdict to those differences.

**Checks.** integrated tests for requester-guidance, [`engine/tests/runtime/test_workspace.py`](../tests/runtime/test_workspace.py), integrated tests for evidence retention
