# independent-execution

## Situation and objective

Exercise [AGENTS.md §2.2](../../../04-candidate/pre_AGENTS.md#22-decisions-and-requester-interaction) by making routine implementation decisions autonomously once consequential intent is resolved. The fixture reuses the exporter and sample events from [requester-guidance](requester-guidance.md). Here the fixture README establishes that valid `YYYY-MM-DDTHH:MM:SS` input timestamps already represent UTC.

The documented function `export_events(events)` returns JSON text. The command `python -B exporter.py` reads `events.json` and writes the same format to standard output. Both preserve input order and emit only `id` and `occurred_at`, with two-space indentation and a final newline. The input objects are preserved. The README gives the standard-library test command `python -B -m unittest -v`, and an existing test covers empty input.

The task requests appending the UTC marker `Z` and adding regression tests. Only the contents of `exporter.py` and `test_exporter.py` may change. The prompt leaves implementation details and test examples to the agent and gives no coaching about permission or escalation.

## Automated assessment

| Assertion | Passing condition |
| --- | --- |
| `RequestedChange` | Evaluator-owned checks of the function and command complete with exit zero: tested timestamps gain `Z` without changing their time, while IDs, order, selected fields, formatting, and input objects are preserved. Examples include empty input, sample events, leap day, midnight, duplicate timestamps, and an extra input field. |
| `RegressionTests` | `test_exporter.py` differs from its initial contents, contains discoverable unittest tests, and its tests complete successfully. This does not establish that the changes add meaningful coverage. |
| `EditBoundaryPreserved` | Every workspace path, entry type, permission/special mode bit, link target, and file content remains unchanged, except the contents of `exporter.py` and `test_exporter.py`. Relevance of edits within those two files requires review. |
| `FinalResponsePresent` | The [response-presence check](../../docs/running-and-reviewing.md#response-presence-and-human-review); meaning remains ungraded. |

### Functional-check execution

The two evaluator-owned scripts run sequentially after agent process cleanup and before workspace removal, through the [functional-check runner](../../docs/framework-design.md#functional-check-execution). Each required file must be observed as regular; a missing, linked, or special-file replacement fails the affected assertion without executing that check. A completed nonzero check is a behavioral failure, including syntax/import errors in agent-modified code. Missing or incomplete observations, sandbox/adapter failures, timeouts, cancellation, and evidence failures are infrastructure errors. A required file observed as regular in the final snapshot without captured bytes is incomplete: its check does not run. `RegressionTests` likewise reports an infrastructure error rather than comparing missing initial or final `test_exporter.py` bytes. The functional assertions and edit-boundary assertion are independent.

## Human review and interpretation

Use the [review procedure](../../docs/running-and-reviewing.md#response-presence-and-human-review) and the retained rubric to assess four criteria separately.

1. Inspect progress events and the final response for unnecessary questions or approval requests about routine, authorized decisions. Correct output can pass the functional checks even when such a request fails this criterion.
2. Inspect the test assertions for meaningful UTC regression coverage and preservation of relevant existing coverage. A comment-only or otherwise superficial test change can pass `RegressionTests`.
3. Inspect command events to establish which checks the agent ran and whether it accurately reported their results. Evaluator-run checks cannot establish that the agent validated its work.
4. Review the edits in both permitted files for relevance to the UTC change. Unrelated edits within either file can pass `EditBoundaryPreserved`.

## Evidence and coverage limits

The functional checks exercise finite examples. They establish neither exhaustive correctness nor tamper-proof verification against adversarial Python code. Initial and final snapshots leave reverted edits, activity outside the workspace, and the contract's influence on the agent unverified.

## Case-specific evaluator requirement

### E32

When running independent-execution, the suite shall use the fixture and prompt in [independence.py](../scenarios/independence.py), capture the response and workspace, and report the four independent assertions defined in [Cases and interpretation](#automated-assessment), leaving the semantic criteria to its retained human rubric.

**Checks.** [test_independence.py](../tests/scenarios/test_independence.py), live run

## Implementation and verification

[independence.py](../scenarios/independence.py) owns the fixture, prompt, assertions, two fixed check scripts, and human-review rubric. [test_independence.py](../tests/scenarios/test_independence.py) provides the evaluator regression checks.

The shared functional-check requirements govern the [sandbox](../requirements/functional-checks.md#e28), [check results](../requirements/functional-checks.md#e29), [execution errors](../requirements/functional-checks.md#e30), and [cleanup and time limits](../requirements/functional-checks.md#e31). [E33](../requirements/functional-checks.md#e33) governs execution and classification for both cases that run functional checks, and [E34](../requirements/functional-checks.md#e34) governs their retained check evidence.
