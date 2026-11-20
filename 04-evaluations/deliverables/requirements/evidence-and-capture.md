# Evidence retention and capture

These requirements cover final-response capture, assertion results and reasons, workspace differences, and retention when evidence writes fail. The [retained evidence guide](../../docs/running-and-reviewing.md#retained-evidence) identifies the artifacts available for review.

These requirements govern evaluator behavior. The [product baseline](../../../01-behavior/deliverables/baseline.md) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E8

When execution ends, the suite shall attempt to retain the [listed evidence](../../docs/running-and-reviewing.md#retained-evidence) outside the temporary workspace.

**Checks.** [test_codex.py](../tests/runtime/test_codex.py), live run

## E9

If an initial evidence write (`AGENTS.md`, optional `message.txt`, or `prompt.txt`) fails, then the suite shall stop normal setup before agent launch and preserve and report the primary infrastructure error through cleanup and available evidence retention, without requiring further initial writes. If a subsequent evidence-retention write fails, then the suite shall preserve primary execution/check errors, attempt remaining independent writes, and report write errors in the terminal.

**Checks.** [test_evidence.py](../tests/runtime/test_evidence.py)

## E21

When reporting behavioral assertions, the suite shall retain boolean assertion values and Pydantic Evals assertion reasons separately in JSON and show specific violations in the terminal report.

**Checks.** [test_scope.py](../tests/scenarios/test_scope.py), [test_permissions.py](../tests/scenarios/test_permissions.py)

## E23

When final-response capture is enabled, the launcher shall capture the CLI's final message separately from progress outside the agent workspace, preserve its text exactly including empty text, and report capture/read failures as infrastructure errors while preserving any primary execution error and available evidence.

**Checks.** [test_capture.py](../tests/runtime/test_capture.py)

## E24

When retaining workspace observations, the suite shall independently attempt each snapshot manifest and regular-file copy, using captured bytes without following links or recreating special files.

**Checks.** [test_capture.py](../tests/runtime/test_capture.py), [test_evidence.py](../tests/runtime/test_evidence.py)

## E27

When retaining workspace observations, the suite shall attempt to save a readable report of all observed entry/content differences independently of other evidence writes, distinguishing incomplete inspection from an unchanged workspace and assigning no behavioral verdict to those differences.

**Checks.** [test_guidance.py](../tests/scenarios/test_guidance.py), [test_workspace.py](../tests/runtime/test_workspace.py), [test_evidence.py](../tests/runtime/test_evidence.py)
