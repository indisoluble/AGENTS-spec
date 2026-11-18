# Evaluation framework design

This document explains execution/security boundaries, runtime architecture, maintenance, and engineering decisions. [Running and reviewing](running-and-reviewing.md) covers operations and evidence; the [evaluation model](evaluation-model.md) defines scope and limits. [Cases and E1–E40](../deliverables/cases-and-requirements.md) specify assessment responsibilities; scenario modules own exact policy and rubrics.

## Execution and security boundaries

### Agent execution

The native restrictive permission profile is the [accepted design](#restrictive-evaluation-agent-command-permissions) for [E7](../deliverables/cases-and-requirements.md#verifiable-requirements). Design acceptance does not establish runtime enforcement or authenticated `codex exec` integration; those require the separate validation described below.

The exact invocation is owned by [codex.py](../deliverables/runtime/codex.py). It selects `agents-spec-eval` through `default_permissions` and supplies the named profile entirely through repeatable `--config` arguments. The configured boundary permits reads/writes inside the disposable workspace, retaining Codex's protected-subpath safeguards through `extends=":workspace"`. It denies unrelated filesystem reads/writes through `:root="deny"`, with Codex-defined `:minimal="read"` runtime access outside the workspace. Explicit `:tmpdir="deny"` and `:slash_tmp="deny"` overrides remove inherited temporary-directory access, and `network.enabled=false` disables command networking. These are configured restrictions, not evidence that every access path has been verified. See the official [permission-profile documentation](https://learn.chatgpt.com/docs/permissions).

On macOS (`sys.platform == "darwin"`), the command additionally grants read access throughout Apple's [standard Command Line Tools directory](https://developer.apple.com/library/archive/technotes/tn2339/_index.html), `/Library/Developer/CommandLineTools`, so Python can start under the restrictive profile. This exception permits no writes there and leaves root denial, temporary-directory denials, and disabled command networking unchanged. Other platforms receive no CLT override. Full Xcode installations and other toolchain arrangements may need separate investigation.

This profile targets sandboxed commands executed by the evaluated agent. The parent Codex client uses the dedicated authentication profile, communicates with the provider, and writes final-response output. The Python evaluator creates and removes workspaces, manages subprocesses, retains evidence outside the workspace, and grades captured observations. Neither the parent client nor the Python evaluator runs inside this agent-command sandbox; it does not provide comprehensive host isolation.

The command omits legacy `--sandbox` and `sandbox_workspace_write` settings, which conflict with native profiles. It emits unquoted filesystem selector names in dotted CLI keys, for example `--config 'permissions.agents-spec-eval.filesystem.:minimal="read"'`, with TOML-serialized values. `exec` selects the profile via configuration, without the sandbox helper's `--permission-profile` flag. The [CLI reference](https://learn.chatgpt.com/docs/cli/reference) documents inline overrides and `--ignore-user-config`, which skips the user configuration file while authentication still uses `CODEX_HOME`; see also the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

Execution uses explicit model/effort settings, `approval_policy="never"` (no permission escalation), environment filtering, ignored user configuration/rules, disabled extensions and host skill discovery, output capture, and managed subprocess lifetimes. Permission configuration is supplied inline rather than persisted in user settings. Ephemeral execution suppresses session persistence, not the saved login.

Verification has separate scopes:

- **Offline configuration and orchestration.** [test_codex.py](../deliverables/tests/runtime/test_codex.py) checks profile selection, override keys and values, execution controls, and arguments received by a fake CLI. The [offline suite](running-and-reviewing.md#run-offline-checks) checks execution orchestration with substitutes. These tests do not run real Codex or establish runtime sandbox enforcement.
- **Runtime enforcement.** Credential-free macOS `codex sandbox` checks with the CLT exception covered conventional Python unit-test discovery, source edits with failing-then-passing tests, `tracemalloc`, denied synthetic reads/writes outside the workspace, and rejected connections to a verified loopback listener. Nonfatal cache-file write errors occurred in per-user macOS temporary/cache locations without affecting those workflows; they do not justify relaxing temporary-directory denials. These bounded checks do not establish complete sandbox enforcement or full evaluation-suite compatibility. Filesystem and network restrictions still need environment-specific verification. The repository's [functional-check sandbox probe](#functional-check-execution) covers only the separate evaluator-owned check sandbox; it does not verify the evaluated-agent profile.
- **Authenticated integration and platform behavior.** The complete `codex exec` path, including authentication, provider communication, sandboxed commands, and output capture, requires separately authorized validation. Offline tests and the functional-check probe do not establish this integration or portability across environments, including Linux and GitHub Actions.

Built-in prompts, platform enforcement, and managed configuration/requirements/instructions may affect a run. Model behavior and service availability remain nondeterministic even though grading is deterministic.

### Observation and capture boundaries

All behavioral cases capture initial workspace state before execution and final state after agent process-group cleanup, before temporary-directory removal. Snapshots stay in evaluator-owned memory outside the writable workspace. Filesystem-state assertions use captured observations rather than reopening agent-controlled paths or inferring state from a text summary. The [durable-finding-review setup validation](../deliverables/cases-and-requirements.md#durable-finding-review) additionally uses the current repository contract as evaluator-owned reference data.

A workspace snapshot includes relative paths, entry types, exact regular-file bytes, symbolic-link targets, and POSIX permission and special mode bits (`stat.S_IMODE`). It covers the root (`.`), hidden entries, nested paths, and empty directories. Links are inspected without following them; special files are recorded without reading their contents. Comparisons report created, deleted, type-changed, permission-changed, link-target-changed, and content-changed entries in sorted path order, with only the exemptions defined by the selected case.

Inspection of an existing tree either produces a complete snapshot or raises an inspection error; partial snapshots are never used to establish preservation. An absent observation (`None`) means inspection did not complete. An empty snapshot instead records a missing workspace root. Initial/final comparison cannot detect reverted edits or outside-workspace activity. Timestamps, ownership, inode identity, and other metadata are excluded. Inspections are sequential, not atomic filesystem transactions; logs can inform review but cannot prove the absence of unobserved actions.

Human-review cases capture `final-response.txt` outside the writable fixture, separately from progress messages. UTF-8 text is preserved without stripping whitespace or normalizing newlines, including empty text. Missing, unreadable, non-regular, or invalid UTF-8 capture files cause infrastructure errors; a pre-existing response is rejected to prevent stale evidence reuse. Available response text is retained after execution failure without making that execution successful. Smoke and scope-discipline keep their raw event logs without separate final-response capture.

The rubric also stays outside the writable fixture, so it does not coach the agent. See [retained evidence](running-and-reviewing.md#retained-evidence) for the manifests, exact-byte copies, and independent write guarantees.

### Deadlines and cleanup

| Operation | Bound |
| --- | --- |
| Agent execution (`codex exec`) | `--timeout` seconds per case; defaults to 180 and must be positive and finite. |
| CLI version and authentication checks | Separate 15-second timeout for each. |
| Each independent-execution or contract-change-followthrough functional check | Five seconds by default; a supplied check timeout must be positive and finite. |
| Functional-check launcher | Check timeout plus five seconds for startup and the adapter response. |
| Process-group cleanup | SIGTERM, up to two seconds waiting for the parent, then SIGKILL to the group, including children that outlive the parent. |

Waiting processes are checked for cancellation at intervals of at most 0.1 seconds. Main-thread SIGINT/Ctrl-C and SIGTERM handlers signal the process owners and are restored afterward. Cleanup completes before the next selected case; the interrupted sequence stops rather than starting another case.

Startup, filesystem operations, reporting, and cleanup add time. Neither `--timeout` nor the functional-check deadline is a hard limit for the entire Python command. Interactive authentication is outside these evaluation deadlines.

Cleanup covers descendants in the launched process group. It cannot guarantee cleanup after SIGKILL of the Python runner, machine failure, or descendants escaping into another process group. These limits apply to agent execution and functional checks.

### Functional-check execution

Independent-execution and contract-change-followthrough run agent-edited fixture code through evaluator-owned Python checks before grading. The scenarios supply ordered check sources, required files, and timeouts to [functional_checks.py](../deliverables/runtime/functional_checks.py), which validates observations, selects eligible checks, retains their evidence, and calls [functional.py](../deliverables/runtime/functional.py)'s `run_python_check(source, workspace, *, timeout=5, cancelled=None)` sequentially. The other cases grade observations without that subprocess.

The helper uses Codex's read-only, network-disabled command sandbox with fresh temporary `HOME` and `CODEX_HOME`, without credentials, personal configuration, inherited API keys, or a model session. Sandbox setup starts outside the fixture so fixture-local configuration cannot influence it; only the check subprocess enters the workspace. The Python adapter and check use isolated mode, disable bytecode generation, and skip site initialization. Fixture imports are explicit. The helper owns and removes its temporary profile; `evaluation.py` manages the workspace lifetime through `workspace.py`, and `functional_checks.py` retains check evidence. There is no retry or unsandboxed fallback.

A `FunctionalCheckResult` with `status="completed"` means the check returned, including a nonzero exit. It carries the return code, exact stdout/stderr bytes, an optional error, and separate launcher diagnostics; the shared functional-check module interprets these observations as generic assertions, and the scenario applies any additional acceptance criteria. Missing CLI, startup failure, malformed adapter responses, timeout, or cancellation produces `status="error"`. The [trusted adapter](../deliverables/runtime/_check_process.py) keeps check output separate from its result response.

A check timeout retains output captured before its deadline. Interruption or failure before the adapter replies can leave check output unavailable; output is buffered in memory. Checks are not run after an agent execution error, and skipped checks retain explicit reasons. Their scripts, results, output, and launcher diagnostics are saved independently from `execution.json`, which continues to describe agent execution. A failed evidence write does not stop remaining independent writes or hide the primary execution/check error.

The offline suite exercises this path using a fake sandbox command and cannot establish OS policy enforcement. From `04-evaluations/`, verify the installed CLI separately with the opt-in probe:

```sh
python -m deliverables.tests.probe_functional_sandbox -v
```

The probe runs trusted local code through the actual helper, checking readable fixture contents and denied fixture writes, outside-workspace writes, and loopback network access. It needs no login or subscription usage and may need to run outside an enclosing agent sandbox. The sandbox still permits host reads: a fresh profile does not make other host credentials unreadable or provide complete host isolation.

## Framework architecture

### Directory layout and ownership

Paths below are relative to `04-evaluations/`, where evaluator commands run. `deliverables/` is the Python package; generated evidence stays outside it in `.eval-runs/`. The [hierarchy decision](#evaluation-framework-package-and-verification-hierarchy) explains code and test ownership. The [stage layout decision](../../docs/decisions.md#stage-deliverables-and-the-contract-staging-exception) records the package name, placement, and import compatibility boundary.

| Path | Owns |
| --- | --- |
| `deliverables/__main__.py` | Composition and the command line: the ordered `CASES` collection, `run_case()`, and `write_report()`. It decides which scenarios exist, which shared stages each uses, and how results become exit codes. |
| `deliverables/runtime/` | Shared execution machinery used by every case: workspaces and observations, Codex launching, authentication, subprocesses, evaluation orchestration, and functional checks. It imports no scenario. |
| `deliverables/scenarios/` | One module per case with its prompt, fixture, dataset, evaluators, and any functional checks and review rubric. |
| `deliverables/tests/runtime/` | Offline tests of the shared machinery, plus `test_cli.py` for CLI guarantees spanning scenarios: case order, exit-code precedence, authentication, timeouts, signals, cleanup, and the functional-check lifecycle. |
| `deliverables/tests/scenarios/` | One `test_<module>.py` per scenario module, containing its grading tests and its CLI tests (`<Name>CLITests`). |
| `deliverables/tests/support/` | Test-only substitutes: `fake_codex.py`, a fake `codex` executable with scripted per-case responses, and `cli_harness.py`, whose `FakeCodexCLI` mixin runs the real CLI against it in a child process. |
| `deliverables/tests/offline_smoke.py`, `deliverables/tests/probe_functional_sandbox.py` | Standalone entry points with documented commands: an offline smoke demonstration and the opt-in [sandbox probe](#functional-check-execution). |

A component becomes a directory only when several independently meaningful files justify that boundary, for example if a scenario's evaluators and fixture grew large enough to be reviewed and changed separately. Until then a scenario stays one module with one test module. Production and test layouts correspond by responsibility, not file for file.

### Pydantic Evals concepts used here

The framework uses a small part of Pydantic Evals; the [technical references](#technical-references) link its documentation.

- **`Case`**: one named input, here the prompt, with an optional `expected_output`. Each scenario defines one case.
- **`Dataset`**: the cases and the evaluators that grade them. Scenarios expose a factory, such as `scope_dataset()`, so every run builds a fresh dataset.
- **Task**: the function Pydantic calls for each case. [evaluation.py](../deliverables/runtime/evaluation.py)'s `evaluate()` builds it around the execution callable: it prepares the workspace, calls the callable, and returns its `ExecutionResult` as the case's output, raising `ExecutionError` when execution failed.
- **`Evaluator` and `EvaluatorContext`**: an evaluator's `evaluate(ctx)` reads `ctx.output` (the `ExecutionResult`) and `ctx.expected_output`, then returns a Boolean or an `EvaluationReason` holding a value and a reason. Each evaluator class yields one named assertion. An exception raised inside an evaluator is an evaluator error, not a false assertion.
- **`EvaluationReport`**: graded cases with their assertions, task failures, and evaluator failures. `write_report()` derives the outcome and exit code from it.

Pydantic Evals runs the task and the evaluators. It does not launch Codex, inspect workspaces, or retain evidence; the runtime modules do.

### Evaluating an agent versus testing the evaluator

The two activities share code but answer different questions:

- **Evaluating an agent:** `python -m deliverables` runs the real Codex CLI on a scenario's fixture, consumes subscription allowance, and produces evidence about that run. The [evaluation model](evaluation-model.md#purpose-and-evaluation-model) bounds what that evidence establishes.
- **Testing the evaluator:** the offline suite never runs a model. Grading tests call `evaluate()` with test-authored execution functions that edit the fixture as a hypothetical agent would. CLI tests run the real command against `deliverables/tests/support/fake_codex.py`. Passing tests show that grading, evidence, and failure handling behave as specified, not that any agent complies with the contract.
- **Checking the functional-check sandbox:** the opt-in probe exercises that sandbox's filesystem and network restrictions using the installed Codex CLI. It does not verify the evaluated-agent permission profile; see [agent execution](#agent-execution) for the separate verification scopes.

### Responsibilities and dependency direction

The CLI composes a selected scenario with shared execution and evaluation mechanisms. Shared infrastructure has no dependency on individual scenarios. Scenario modules use the common interfaces while retaining their prompts, fixtures, assessment policy, and scenario-specific interpretation.

| Responsibility | Owner and boundary |
| --- | --- |
| Case composition and reporting | [__main__.py](../deliverables/__main__.py): one ordered `CASES` collection selects lazy dataset factories, fixtures, observation, rubrics, and optional functional checks. Rubric presence determines response capture and pending-review reporting. |
| Evaluation orchestration and results | [evaluation.py](../deliverables/runtime/evaluation.py): runs an injected execution callable in fresh workspaces and hands results to Pydantic Evals. Owns shared result/error semantics, observation-completeness validation, and response-presence assessment, without scenario policy. |
| Workspace lifecycle and observations | [workspace.py](../deliverables/runtime/workspace.py): prepares and removes fixtures, injects the root contract, safely reads regular files, and captures/compares state. Scenarios supply the meaning of permitted content changes. |
| Controlled agent execution and evidence | [codex.py](../deliverables/runtime/codex.py): launches Codex, captures observations, and retains evidence. [auth.py](../deliverables/runtime/auth.py) owns profile/authentication operations; [process.py](../deliverables/runtime/process.py) owns subprocess lifetimes and cancellation. |
| Individual functional-check execution | [functional.py](../deliverables/runtime/functional.py): runs one evaluator-owned check in a disposable unauthenticated sandbox profile and returns its status, exact output bytes, and launcher diagnostics. Owns subprocess lifetime, timeout, and cancellation. |
| Functional-check orchestration and interpretation | [functional_checks.py](../deliverables/runtime/functional_checks.py): validates required observations, selects and runs eligible checks sequentially, retains evidence, accumulates infrastructure errors, and interprets generic results as assertion values and reasons. Reuses `ExecutionResult`, workspace observations, the individual check runner, and `codex.save_json`; imports no scenario. |
| Scenario behavior | The modules linked in the [catalogue](../deliverables/cases-and-requirements.md#cases-and-interpretation) own their datasets, exact prompts/fixtures, ordered check scripts, required-file definitions, check timeouts, acceptance criteria, additional assertions, and rubrics. Common mechanisms are reused where their semantics match; scenario-specific policy stays local. |

One evaluation passes through these owners in the following order. Optional stages apply only when the selected case configures them; `smoke`, for example, has no workspace observation, functional checks, response capture, or human review.

1. **Selection and composition.** `main()` validates the arguments and selects entries from `CASES`. Each `CaseConfig` supplies a lazy dataset factory, fixture files, a workspace-observation setting, an optional human-review rubric, and an optional post-agent `check_execution` step. A rubric's presence also enables final-response capture and pending-review reporting. The scenario module behind the entry owns the behavioral policy: its prompt, fixture, evaluators, check scripts, and rubric. The stages below are shared mechanisms.
2. **Invocation.** `run_case()` creates the case's evidence directory, writes `review.md` when a rubric exists, and defines the execution callback: a function that accepts a prompt and a workspace path and returns an `ExecutionResult`. That result carries the execution status and error, plus any captured observations, final response, and functional-check results that grading later reads. `run_case()` passes the callback, a freshly built Pydantic `Dataset` (its `Case` holds the prompt; the dataset holds the evaluators), and the fixture mapping to `evaluate()`. `evaluate()` wraps the callback in a task and has Pydantic Evals run that task for one case at a time.
3. **Workspace preparation and agent execution.** Inside the task, `prepare_workspace()` creates the temporary directory, writes the unchanged root contract and then the fixture files, and yields the path to the callback. The callback calls `run_codex()`, which takes the initial snapshot when observation is enabled, saves the contract, prompt, and any initial `message.txt` as evidence, checks prerequisites, and launches Codex through `run_process()`, streaming raw events and diagnostics to the evidence directory. Whether the agent finishes, fails, times out, or is interrupted, `run_process()` stops its process group before returning or raising. `run_codex()` then captures the final response when requested, takes the final snapshot when observing, and writes the execution and workspace evidence. Three things remain distinct: the live workspace, which is disposable; the observations held in the returned `ExecutionResult`; and the evidence files written outside the workspace.
4. **Optional functional checks.** Only cases with a `check_execution` step, currently independent-execution and contract-change-followthrough, continue here. The callback invokes that step after `run_codex()` returns, so agent cleanup has finished while the workspace still exists. In independent-execution, for example, the scenario binds its check sources, required files, and timeout to `functional_checks.run_checks`. That function validates the required files from the captured final observation, runs eligible checks sequentially, records skipped checks with reasons, and retains `checks/` and `functional-checks.json` before returning the result with the check results attached. After an agent execution error, it runs no checks and records that reason. The scenario modules and [functional-check execution](#functional-check-execution) own the scripts, isolation, and meaning of the results.
5. **Workspace disposal and grading.** If the returned result has error status, the task raises an execution error inside the workspace context: the workspace is removed and the case is not graded (see [Outcomes and exit codes](running-and-reviewing.md#outcomes-and-exit-codes)). Otherwise the task returns the result, and leaving the context removes the workspace. Pydantic Evals then applies the dataset's evaluators to that returned result. Grading uses the captured data in memory—workspace observations, functional-check results, the final response, `file_contents`, and the status and error—alongside evaluator-owned reference data such as [durable-finding-review's current-contract validation](../deliverables/cases-and-requirements.md#durable-finding-review); it does not reopen the disposed workspace. Separately, the evidence files written in stages 2–4 remain on disk for later inspection.
6. **Reports and human review.** `evaluate()` returns Pydantic's report. `write_report()` derives the outcome and exit code, prints the result, and attempts `report.txt` and `report.json` independently. Completed execution does not imply passing assertions, and automated assertions cover only their defined technical conditions. A human-review rubric remains outside automated grading; its pending flag never overrides error or assertion-failure precedence. [Outcomes and exit codes](running-and-reviewing.md#outcomes-and-exit-codes) explains the classification, and [Retained evidence](running-and-reviewing.md#retained-evidence) lists the files.

**Cancellation and threading.** Pydantic runs the synchronous task in a worker thread, but Python runs signal handlers only on the main thread, where raising `KeyboardInterrupt` would not stop the worker. `main()` therefore wraps the case sequence in `cancellation_signals()` from [process.py](../deliverables/runtime/process.py), whose SIGINT and SIGTERM handlers only set a shared cancellation event and are restored afterward. `run_case()` passes that event to `run_codex()` and the functional-check step. Each launcher (`codex.py` and `auth.py` for Codex and its prerequisite checks, `functional.py` for each check) runs its subprocess through `run_process()`, which observes the event while waiting and stops that process group. Other operations, such as snapshots, evidence writes, and grading, are not interrupted midway. An interruption noticed after evaluation, including during reporting, still makes the case an execution failure, and no further case starts. [Deadlines and cleanup](#deadlines-and-cleanup) gives the polling interval, termination sequence, and cleanup limits.

Pydantic owns assertion results/reasons and terminal formatting; the custom code supplies observations and assessment policy. Standard-library filesystem facilities preserve the required byte, permission, and link semantics.

### Walkthrough: scope-discipline

This case shows each owner in a run without optional stages: no functional checks, response capture, or human review.

1. **Definition.** [scope.py](../deliverables/scenarios/scope.py) holds `PROMPT`, which asks for the greeting in `message.txt` to change, and `INITIAL_CONTENTS`, the fixture's exact bytes. `scope_dataset()` returns a `Dataset` with one `Case`, `edit-greeting-only`, whose `expected_output` is the single permitted edit, and two evaluators. `RequestedChange` compares the first line of the captured final `message.txt` with that expectation. `ScopePreserved` calls `scope_violations()`, which delegates to the shared `workspace_violations()` and supplies the one permitted content change. Both call `require_observation()` first, so missing snapshots become evaluator errors rather than verdicts.
2. **Registration.** [__main__.py](../deliverables/__main__.py) registers `CaseConfig("scope-discipline", scope.scope_dataset, {"message.txt": scope.INITIAL_CONTENTS})`. Workspace observation is on by default; with no rubric there is no response capture or pending review, and with no `check_execution` there are no functional checks.
3. **Run.** `python -m deliverables --case scope-discipline --model ID --reasoning-effort VALUE` follows the [lifecycle above](#responsibilities-and-dependency-direction). `prepare_workspace()` writes `AGENTS.md` and `message.txt`; `run_codex()` snapshots the workspace, runs Codex, and snapshots it again; the task returns an `ExecutionResult` holding both snapshots; the workspace is removed; Pydantic applies the two evaluators; `write_report()` prints the outcome.
4. **Result.** `report.json` records `RequestedChange` and `ScopePreserved` with separate reasons. The evidence directory keeps both workspace manifests and `workspace-changes.txt`. The command exits 0 if both pass, 1 if either fails, and 2 on an infrastructure error.
5. **Verification.** [test_scope.py](../deliverables/tests/scenarios/test_scope.py) holds all of this case's offline tests. `ScopeEvaluationTests` grade test-authored edits through `evaluate()`. `ScopeWorkspaceComparisonTests` exercise `scope_violations()` directly. `ScopeCLITests` run the command against the fake executable, whose `scope-discipline` responses are in [fake_codex.py](../deliverables/tests/support/fake_codex.py). Run them with `python -m unittest deliverables.tests.scenarios.test_scope -v`. The shared behavior they rely on, such as snapshots, evidence, and exit-code precedence, is tested under `deliverables/tests/runtime/`.

Scope-discipline grades only captured observations. Independent-execution and contract-change-followthrough also run evaluator-owned checks on the edited fixture through their `check_execution` entries; their evaluators turn the attached results into assertions with `functional_checks.check_assertion`. [Functional-check execution](#functional-check-execution) explains that path.

## Interfaces used by scenarios and substitutes

The shared evaluation runner accepts an explicit dataset, a `fixture_files` mapping, and an execution callable `(prompt, workspace) -> ExecutionResult`. Both the Codex launcher and offline substitutes use that callable boundary.

Scenario `check_execution` wrappers bind their sources, required files, timeout, artifacts directory, and cancellation event to `functional_checks.run_checks`, which returns the updated `ExecutionResult`. `check_assertion` accepts a result, check name, and required paths and returns the generic `EvaluationReason`. Additional policy, such as requiring changed regression-test bytes or preserving the root contract, stays in the scenario evaluator.

[ExecutionResult](../deliverables/runtime/evaluation.py) preserves `status`, `file_contents`, and `error`, with optional `workspace_observation`, `final_response`, and `functional_checks`. Completed execution does not imply passing assertions. Execution errors are reported separately from grading; observations and functional-check results are not themselves semantic verdicts. Skipped checks for non-regular required files have retained reasons rather than invented process results. `evaluation.require_observation` raises a workspace inspection error unless both initial and final snapshots are present, so an observed empty workspace is not confused with a missing observation; functional checks and scenario evaluators call it before applying their own fixture or content rules.

Fixture mappings use relative paths and exact bytes. Workspace preparation creates their parent directories and separately injects the unchanged root contract; absolute paths, parent traversal, and root-contract overrides are rejected. An explicit mapping replaces the default fixture, and an empty mapping adds no files beyond the contract. The documented [smoke convenience](../deliverables/scenarios/smoke.py), `smoke.evaluate`, retains its optional dataset, `initial_contents`, and `fixture_files` arguments: without a mapping it supplies `message.txt` using the selected initial contents; shared workspace preparation itself requires an explicit mapping.

Internal module locations and imports are implementation details unless a documented contract or demonstrated external consumer requires compatibility. Preserve the documented CLI, execution callable/result semantics, and smoke convenience when changing internal ownership; do not add aliases solely to retain accidental internal interfaces.

## Framework maintenance

### Modify or extend an evaluation

Begin with the scenario's intended behavior, its source module, linked tests, and [acceptance definitions](../deliverables/cases-and-requirements.md#cases-and-interpretation). A scenario change should normally involve those local owners, one `CASES` entry where configuration changes, and affected documentation.

1. **Keep policy with the scenario.** Its module owns the task, fixture, dataset/evaluators, and optional human rubric. Reuse shared execution, workspace observation, response capture, and evidence mechanisms; do not reproduce them inside a case. A common mechanism belongs with a cohesive owner, not in a generic utility collection merely because two callers use it.
2. **Compose through the existing CLI entry.** Register a dataset factory, not an eagerly constructed dataset. Select the existing observation/review settings and, only where needed, the post-execution functional check. Keep that check after agent cleanup and before fixture removal.
3. **Test observable contracts at the affected boundary.** Use the existing substitutes and fake CLI to verify outcomes, independent assertions, error classification, evidence, and resource cleanup. Preserve meaningful negative cases and independent expected results; do not mirror production grading or configuration logic in tests. Keep scenario-specific expectations local, sharing setup only when it clarifies the tests.
4. **Synchronize the knowledge owners.** Update the catalogue and affected acceptance/interpretation definitions when behavior changes; update [E1–E40](../deliverables/cases-and-requirements.md#verifiable-requirements) only through an authorized requirement change. Source remains canonical for exact fixture bytes, prompts, check scripts, and rubric text. Check direct documentation links and retain run-specific findings in evidence rather than turning this guide into a record of individual runs.

To add a scenario, apply those principles in these places:

1. Create `deliverables/scenarios/<module>.py` with `PROMPT`, the fixture bytes, its evaluators, and a dataset factory returning a one-case `Dataset`. Add `REVIEW_RUBRIC` and a `check_execution` wrapper over `functional_checks.run_checks` only if the case needs them. Import shared mechanisms from `deliverables.runtime`.
2. Add a `CaseConfig` entry to `CASES` in `deliverables/__main__.py` at its catalogue position. The `--case` choices and the `all` order come from that collection.
3. Teach `deliverables/tests/support/fake_codex.py` to recognize the case from its prompt or fixture and to produce the scripted responses its tests need.
4. Add `deliverables/tests/scenarios/test_<module>.py` with grading tests through `evaluate()` and a `<Name>CLITests(FakeCodexCLI, unittest.TestCase)` class for CLI composition, evidence, and failure classification.
5. Update the tests in `deliverables/tests/runtime/test_cli.py` that enumerate every case: the all-cases order and evidence, late-case precedence, and aggregate exit codes.
6. Add the case to the [catalogue](../deliverables/cases-and-requirements.md#cases-and-interpretation) with a case section linking its module and test module. The case lists in [E12 and E15](../deliverables/cases-and-requirements.md#verifiable-requirements) are requirements, so adding a case also needs an authorized requirement change.
7. Run the [offline checks](running-and-reviewing.md#run-offline-checks).

When applied in a consuming project, the candidate contract's [engineering rules](../../03-contract/prerelease_AGENTS.md#12-do--perform-the-authorized-work) and [validation rules](../../03-contract/prerelease_AGENTS.md#13-study--assess-completion-and-learning) cover production modules, tests, fixtures, and testing utilities alike. The staged candidate is source material, not development instructions for this repository. Use ordinary functions and existing typed result records for composition, `Path` for filesystem boundaries, and bytes where exact fixture/evidence preservation matters. Supply execution dependencies at the existing callable boundary for offline tests. Keep missing observations distinct from empty state and infrastructure errors distinct from false assertions.

### Verify a behavior change

For a case change, run the [offline checks](running-and-reviewing.md#run-offline-checks). The [case and requirement tables](../deliverables/cases-and-requirements.md) link the relevant regression tests; shared-infrastructure tests cover authentication, cancellation, filesystem observation, and evidence failures. For human-rubric changes, also compare the revised criteria with the applicable contract provisions, preserving rule strengths, triggers, exceptions, evidence limits, and unaffected technical checks. Offline tests verify infrastructure and technical assertions; they do not establish rubric semantic validity or live contractual compliance.

Live verification requires inspecting one separately authorized run. If authorization covers only offline work, stop after that verification and report live assessment as pending. The [functional-check sandbox probe](#functional-check-execution) checks that separate boundary's runtime enforcement. Verification of the evaluated-agent permission profile and authenticated integration follows the distinct scopes in [agent execution](#agent-execution).

Inspect the live run's selected case, assertions and reasons, initial/final bytes and available manifests, contract hash, model settings, and cleaned workspace path. For human-review cases, also inspect response capture, readable differences, the retained rubric, and pending-review reporting, and assess the rubric with the requester. For independent-execution and contract-change-followthrough, include functional-check evidence. Each executed case should produce a distinct workspace and evidence directory. Keep run-specific results with that evidence rather than duplicating them here.

## Architecture decisions

These records explain the evaluation-specific decisions and their scope. The [system-wide decision record](../../docs/decisions.md#architecture-decisions) covers choices across stages.

### Restrictive evaluation-agent command permissions

**Status:** Accepted. Authenticated `codex exec` integration and environment-specific enforcement still require validation.

**Context.** Evaluation-agent commands need workspace reads/writes while denying unrelated host access and shell networking. Pydantic Evals manages execution and grading; Codex runs the evaluated agent using a dedicated authentication profile. Evaluator-owned functional checks use a separate sandbox. [Agent execution](#agent-execution) owns the configured command boundary, official references, and verification limits.

**Decision.** Configure evaluated-agent commands through one restrictive native permission profile passed inline to `codex exec`, as required by [E7](../deliverables/cases-and-requirements.md#verifiable-requirements). The parent Codex client's authentication and provider communication and the Python evaluator operate outside that command sandbox.

**Consequences.** The configured profile limits command access to the workspace and the runtime reads documented under [agent execution](#agent-execution), with command networking disabled. Tools needing broader access may be unavailable. CLI support, runtime enforcement, and authenticated integration require environment-specific validation; offline tests establish configuration and orchestration only. The profile neither confines the parent client or Python evaluator nor establishes complete host isolation. Inline permission configuration requires no persistent user settings.

### Evaluation framework package and verification hierarchy

**The requester accepted the code and test hierarchy** on the basis of the alternatives and incremental implementation plan. The [stage layout decision](../../docs/decisions.md#stage-deliverables-and-the-contract-staging-exception) separately authorizes the `deliverables` package name and placement.

The CLI composes cases. Shared runtime machinery imports no scenario. Each scenario owns its prompt, fixture, assessment policy, and any functional checks or rubric. Reuse between scenarios is explicit, as when independent-execution uses the requester-guidance fixture. The [directory layout](#directory-layout-and-ownership) gives each scenario one module and a corresponding offline test module. Runtime tests cover shared guarantees, including cross-scenario CLI behavior. Test substitutes have their own owner outside production code.

Flat production and test trees obscure those responsibilities. Organizing just one tree leaves the other ambiguous, and naming only the test side `infrastructure/` obscures its relationship to runtime. A directory for a single-file scenario adds a level without a second responsibility. Test modules importing one another caused discovery to load some modules under two names even though each test ran once. Absolute package-qualified imports and [discovery from the stage import root](running-and-reviewing.md#run-offline-checks) avoid duplicate loading. Scenario tests locate the fake executable directly without depending on the CLI harness or a shared path constant.

Package-qualified imports, mock targets, and subprocess working directories must resolve the same package. The hierarchy deliberately omits compatibility aliases and re-exports because they would hide stale imports. Keep the documented CLI, callable and result contracts, smoke convenience, and standalone offline-smoke and sandbox-probe entry points. `_check_process.py` must stay beside `functional.py`, which locates it by position. Contract lookup must resolve the [staged source](../../docs/architecture.md#staged-sources-and-release-relative-references) from the runtime package.

Adding a scenario affects its module, registration, tests, fake responses, and cross-scenario case lists. Changes to code ownership preserve E1–E40 and grading semantics. [Offline tests](#evaluating-an-agent-versus-testing-the-evaluator) verify the machinery. Behavioral evidence requires a live run.

### Evaluation documentation by maintenance responsibility

**The requester accepted this structure and authorized organizing the documentation by maintenance responsibility.** It superseded the [earlier choice to keep evaluation documentation in one guide](../../docs/decisions.md#integrated-engineering-architecture-with-focused-detailed-owners). The shared architecture and its division of ownership continue to apply. The documentation decision grants no authority to change evaluator semantics, E1–E40, case order or criteria, rubric ownership, security behavior, product intent, or contract design.

The [evaluation model](evaluation-model.md) explains what a run can establish. [Operations](running-and-reviewing.md) covers execution, review, and retained evidence. The [case catalogue](../deliverables/cases-and-requirements.md) keeps the ten definitions together with E1–E40. This document owns framework boundaries, architecture, maintenance, decisions, and technical references. The [stage README](../README.md) connects those entry points under the [numbered stage decision](../../docs/decisions.md#four-numbered-stages-and-their-responsibilities).

An integrated guide keeps case criteria, requirements, lifecycle, and evidence close together but mixes the tasks of operators, case maintainers, and framework maintainers. Separate owners give each reader a direct entry point. Length alone would not justify the cost of maintaining links or the risk of overlooking a qualification. Review affected case, requirement, lifecycle, and evidence owners together. Keep direct reciprocal links to the observation boundaries, rubrics, checks, review procedures, and outcomes needed to interpret each case. When a section moves, update incoming links to its owner. The [shared architecture](../../docs/architecture.md#where-detailed-knowledge-lives) locates these owners. Historical runs retain the interpretation supported by their own contract, fixtures, rubrics, and captured evidence.

## Technical references

The repository source owns the actual commands, interfaces, and dependency constraints. External references support installation, compatibility investigation, and use of the existing libraries:

- Codex: [CLI installation](https://learn.chatgpt.com/docs/codex/cli), [authentication](https://learn.chatgpt.com/docs/auth), [non-interactive execution](https://learn.chatgpt.com/docs/non-interactive-mode), and the [CLI reference](https://learn.chatgpt.com/docs/cli/reference), including [command sandboxing](https://learn.chatgpt.com/docs/cli/reference#codex-sandbox).
- Pydantic Evals: [built-in comparisons](https://pydantic.dev/docs/ai/evals/evaluators/built-in/) compare supplied outputs rather than capturing workspaces; [custom evaluator explanations](https://pydantic.dev/docs/ai/evals/evaluators/custom/#with-reasons) supply assertion reasons.
