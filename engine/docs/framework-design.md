# Evaluation framework design

## Execution and security boundaries

### Agent execution

The native restrictive permission profile is the [accepted design](#restrictive-evaluation-agent-command-permissions) for [`engine/requirements/agent-execution.md` § E7](../requirements/agent-execution.md#e7). Design acceptance does not establish runtime enforcement or authenticated `codex exec` integration; those require the separate validation described below.

The word *profile* refers to two different things here. The authentication profile is a directory selected by `--codex-home`. [`engine/runtime/auth.py`](../runtime/auth.py) checks its configuration and ChatGPT login. The command-permission profile is a named set of access rules. [`engine/runtime/codex.py`](../runtime/codex.py) selects `agents-spec-eval` through `default_permissions` and supplies those rules through repeatable `--config` arguments.

The configured boundary permits reads/writes inside the disposable workspace, retaining Codex's protected-subpath safeguards through `extends=":workspace"`. It denies unrelated filesystem reads/writes through `:root="deny"`, with Codex-defined `:minimal="read"` runtime access outside the workspace. Explicit `:tmpdir="deny"` and `:slash_tmp="deny"` overrides remove inherited temporary-directory access, and `network.enabled=false` disables command networking. These are configured restrictions, not evidence that every access path has been verified. See the official [permission-profile documentation](https://learn.chatgpt.com/docs/permissions).

On macOS (`sys.platform == "darwin"`), the command additionally grants read access throughout Apple's [standard Command Line Tools directory](https://developer.apple.com/library/archive/technotes/tn2339/_index.html), `/Library/Developer/CommandLineTools`, so Python can start under the restrictive profile. This exception permits no writes there and leaves root denial, temporary-directory denials, and disabled command networking unchanged. Other platforms receive no CLT override. Full Xcode installations and other toolchain arrangements may need separate investigation.

This profile targets sandboxed commands executed by the evaluated agent. The parent Codex client uses the dedicated authentication profile, communicates with the provider, and writes final-response output. The Python evaluator creates and removes workspaces, manages subprocesses, retains evidence outside the workspace, and grades captured observations. Neither the parent client nor the Python evaluator runs inside this agent-command sandbox; it does not provide comprehensive host isolation.

The command omits legacy `--sandbox` and `sandbox_workspace_write` settings, which conflict with native profiles. It emits unquoted filesystem selector names in dotted CLI keys, for example `--config 'permissions.agents-spec-eval.filesystem.:minimal="read"'`, with TOML-serialized values. `exec` selects the profile via configuration, without the sandbox helper's `--permission-profile` flag. The [CLI reference](https://learn.chatgpt.com/docs/cli/reference) documents inline overrides and `--ignore-user-config`, which skips the user configuration file while authentication still uses `CODEX_HOME`; see also the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

Execution uses explicit model/effort settings, `approval_policy="never"` (no permission escalation), environment filtering, ignored user configuration/rules, disabled extensions and host skill discovery, output capture, and managed subprocess lifetimes. Permission configuration is supplied inline rather than persisted in user settings. Ephemeral execution suppresses session persistence, not the saved login.

Verification has separate scopes:

- **Offline configuration.** The [execution-command tests](../tests/runtime/test_codex.py) check profile selection, override keys, values and arguments. Offline substitutes verify orchestration. Actual CLI enforcement requires environment-specific evidence.
- **Runtime enforcement.** Credential-free macOS `codex sandbox` checks with the CLT exception covered conventional Python unit-test discovery, source edits with failing-then-passing tests, `tracemalloc`, denied synthetic reads/writes outside the workspace, and rejected connections to a verified loopback listener. Nonfatal cache-file write errors occurred in per-user macOS temporary/cache locations without affecting those workflows; they do not justify relaxing temporary-directory denials. These bounded checks do not establish complete sandbox enforcement or full evaluation-suite compatibility. Filesystem and network restrictions still need environment-specific verification. The repository's [functional-check sandbox probe](#functional-check-execution) covers only the separate evaluator-owned check sandbox; it does not verify the evaluated-agent profile.
- **Authenticated integration and platform behavior.** The complete `codex exec` path, including authentication, provider communication, sandboxed commands, and output capture, requires separately authorized validation. Offline tests and the functional-check probe do not establish this integration or portability across environments, including Linux and GitHub Actions.

Built-in prompts, platform enforcement, and managed configuration/requirements/instructions may affect a run. Model behavior and service availability remain nondeterministic even though grading is deterministic.

### Observation and capture boundaries

When observation is enabled, the launcher captures initial state before execution and final state after process-group cleanup. Snapshots remain in evaluator-owned memory outside the writable workspace. Grading can use these captured bytes after workspace removal.

A workspace snapshot ([`engine/requirements/workspace-and-observation.md` § E16](../requirements/workspace-and-observation.md#e16)) includes relative paths, entry types, exact regular-file bytes, symbolic-link targets, and POSIX permission and special mode bits (`stat.S_IMODE`). It covers the root (`.`), hidden entries, nested paths, and empty directories. Links are inspected without following them; special files are recorded without reading their contents. Comparisons report created, deleted, type-changed, permission-changed, link-target-changed, and content-changed entries in sorted path order, with only the exemptions defined by the selected case.

Inspection of an existing tree either produces a complete snapshot or raises an inspection error; partial snapshots are never used to establish preservation. An absent observation (`None`) means inspection did not complete. An empty snapshot instead records a missing workspace root. Initial/final comparison cannot detect reverted edits or outside-workspace activity. Timestamps, ownership, inode identity, and other metadata are excluded. Inspections are sequential, not atomic filesystem transactions; logs can inform review but cannot prove the absence of unobserved actions.

Human-review cases capture `final-response.txt` outside the writable fixture, separately from progress messages. UTF-8 text is preserved without stripping whitespace or normalizing newlines, including empty text. Missing, unreadable, non-regular, or invalid UTF-8 capture files cause infrastructure errors; a pre-existing response is rejected to prevent stale evidence reuse. Available response text is retained after execution failure without making that execution successful. When separate capture is disabled, the raw event log is still retained.

### Response-presence assessment

The reusable `FinalResponsePresent` assertion passes when a captured final response contains non-whitespace text. Empty or whitespace-only text fails. Missing capture is an error. The assertion grades presence alone. [`engine/runtime/evaluation.py`](../runtime/evaluation.py)

### Deadlines and cleanup

| Operation | Bound |
| --- | --- |
| Agent execution | Caller-supplied positive finite timeout. |
| CLI version and authentication checks | Separate 15-second timeout for each. |
| Each functional check | Five seconds by default; a supplied check timeout must be positive and finite. |
| Functional-check launcher | Check timeout plus five seconds for startup and the adapter response. |
| Process-group cleanup | SIGTERM, up to two seconds waiting for the parent, then SIGKILL to the group, including children that outlive the parent. |

Waiting processes are checked for cancellation at intervals of at most 0.1 seconds. Main-thread SIGINT/Ctrl-C and SIGTERM handlers signal the process owners and are restored afterward.

Startup, filesystem operations, reporting, and cleanup add time. Neither `--timeout` nor the functional-check deadline is a hard limit for the entire Python command. Interactive authentication is outside these evaluation deadlines.

Cleanup covers descendants in the launched process group. It cannot guarantee cleanup after SIGKILL of the Python runner, machine failure, or descendants escaping into another process group. These limits apply to agent execution and functional checks.

### Functional-check execution

The helper uses Codex's read-only, network-disabled command sandbox with fresh temporary `HOME` and `CODEX_HOME`, without credentials, personal configuration, inherited API keys, or a model session. Sandbox setup starts outside the fixture so fixture-local configuration cannot influence it; only the check subprocess enters the workspace. The Python adapter and check use isolated mode, disable bytecode generation, and skip site initialization. Fixture imports are explicit. The helper owns and removes its temporary profile; `evaluation.py` manages the workspace lifetime through `workspace.py`, and `functional_checks.py` retains check evidence. There is no retry or unsandboxed fallback.

A `FunctionalCheckResult` with `status="completed"` means the check returned, including a nonzero exit. It carries the return code, exact stdout/stderr bytes, an optional error, and separate launcher diagnostics; the shared functional-check module interprets these observations as generic assertions, and the scenario applies any additional acceptance criteria. Missing CLI, startup failure, malformed adapter responses, timeout, or cancellation produces `status="error"`. The trusted adapter ([`engine/runtime/_check_process.py`](../runtime/_check_process.py)) keeps check output separate from its result response.

A check timeout retains output captured before its deadline. Interruption or failure before the adapter replies can leave check output unavailable; output is buffered in memory. Checks are not run after an agent execution error, and skipped checks retain explicit reasons. Their scripts, results, output, and launcher diagnostics are saved independently from `execution.json`, which continues to describe agent execution. A failed evidence write does not stop remaining independent writes or hide the primary execution/check error.

The offline suite exercises this path using a fake sandbox command and cannot establish OS policy enforcement. From the source root, verify the installed CLI separately with the opt-in probe:

```sh
python -m engine.tests.probe_functional_sandbox -v
```

The probe runs trusted local code through the actual helper, checking readable fixture contents and denied fixture writes, outside-workspace writes, and loopback network access. It needs no login or subscription usage and may need to run outside an enclosing agent sandbox. The sandbox still permits host reads: a fresh profile does not make other host credentials unreadable or provide complete host isolation.

## Interfaces used by scenarios and substitutes

The shared evaluation runner accepts an explicit contract reader, dataset, a `fixture_files` mapping, and an execution callable `(prompt, workspace) -> ExecutionResult`. Both the Codex launcher and offline substitutes use that callable boundary.

Scenario `check_execution` wrappers bind their sources, required files, timeout, artifacts directory, and cancellation event to `functional_checks.run_checks`, which returns the updated `ExecutionResult`. `check_assertion` accepts a result, check name, and required paths and returns the generic `EvaluationReason`. Additional policy, such as requiring changed regression-test bytes or preserving the root contract, stays in the scenario evaluator.

ExecutionResult ([`engine/runtime/evaluation.py`](../runtime/evaluation.py)) preserves `status`, `file_contents`, and `error`, with optional `workspace_observation`, `final_response`, and `functional_checks`. Completed execution does not imply passing assertions. Execution errors are reported separately from grading; observations and functional-check results are not themselves semantic verdicts. Skipped checks for non-regular required files have retained reasons rather than invented process results. `evaluation.require_observation` raises a workspace inspection error unless both initial and final snapshots are present, so an observed empty workspace is not confused with a missing observation; functional checks and scenario evaluators call it before applying their own fixture or content rules.

### Contract injection and fixture inputs

The caller supplies a trusted contract reader. Each task injects the returned bytes before execution.

Fixture mappings use relative paths and exact bytes. Workspace preparation creates their parent directories and rejects absolute paths, parent traversal, and root-contract overrides. An explicit mapping replaces the default fixture, and an empty mapping adds no files beyond the contract. The documented smoke convenience ([`engine/smoke.py`](../smoke.py)), `smoke.evaluate`, retains its optional dataset, `initial_contents`, and `fixture_files` arguments: without a mapping it supplies `message.txt` using the selected initial contents; shared workspace preparation itself requires an explicit mapping.

## Architecture decisions

### Restrictive evaluation-agent command permissions

**Status:** Accepted. Authenticated `codex exec` integration and environment-specific enforcement still require validation.

**Context.** Evaluation-agent commands need workspace reads/writes while denying unrelated host access and shell networking. Pydantic Evals manages execution and grading; Codex runs the evaluated agent using a dedicated authentication profile. Evaluator-owned functional checks use a separate sandbox. [Agent execution](#agent-execution) owns the configured command boundary, official references, and verification limits.

**Decision.** Configure evaluated-agent commands through one restrictive native permission profile passed inline to `codex exec`, as required by [`engine/requirements/agent-execution.md` § E7](../requirements/agent-execution.md#e7). The parent Codex client's authentication and provider communication and the Python evaluator operate outside that command sandbox.

**Consequences.** The configured profile limits command access to the workspace and the runtime reads documented under [agent execution](#agent-execution), with command networking disabled. Tools needing broader access may be unavailable. CLI support, runtime enforcement, and authenticated integration require environment-specific validation; offline tests establish configuration and orchestration only. The profile neither confines the parent client or Python evaluator nor establishes complete host isolation. Inline permission configuration requires no persistent user settings.

## Technical references

The repository source owns the actual commands, interfaces, and dependency constraints. External references support installation, compatibility investigation, and use of the existing libraries:

- Codex: [CLI installation](https://learn.chatgpt.com/docs/codex/cli), [authentication](https://learn.chatgpt.com/docs/auth), [non-interactive execution](https://learn.chatgpt.com/docs/non-interactive-mode), and the [CLI reference](https://learn.chatgpt.com/docs/cli/reference), including [command sandboxing](https://learn.chatgpt.com/docs/cli/reference#codex-sandbox).
- Pydantic Evals: [built-in comparisons](https://pydantic.dev/docs/ai/evals/evaluators/built-in/) compare supplied outputs rather than capturing workspaces; [custom evaluator explanations](https://pydantic.dev/docs/ai/evals/evaluators/custom/#with-reasons) supply assertion reasons.
