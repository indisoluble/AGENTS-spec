# Running and reviewing evaluations

This document owns installation, authentication, case execution, retained evidence, report interpretation, failure investigation, and human review. Start with the [evaluation model](evaluations.md#purpose-and-evaluation-model) for the suite's scope and interpretation limits.

Use the [case catalogue and acceptance definitions](../deliverables/cases-and-requirements.md#cases-and-interpretation) to find the selected case's source module and exact rubric, and [E1–E40](../deliverables/cases-and-requirements.md#verifiable-requirements) for evaluator requirements. [Framework design](framework-design.md) owns execution, observation, cleanup, and functional-check boundaries; the links below connect operational results to those mechanisms. A historical run is interpreted using its captured contract and rubric, as the [review procedure](#response-presence-and-human-review) explains.

## Setup and running evaluations

### Install prerequisites

Run evaluator commands from `04-evaluations/`. Use Python 3.11 or newer and a POSIX system. Windows is not supported by the process-group and file-opening implementation. Runtime compatibility and sandbox enforcement need separate validation in the target environment; see [agent execution](framework-design.md#agent-execution). From the repository root, enter the stage before setup:

```sh
cd 04-evaluations
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade -r deliverables/requirements.txt
```

[requirements.txt](../deliverables/requirements.txt) owns the dependency range. It allows Pydantic Evals minor and patch upgrades within major version 2. Dependencies are not locked, so installations can resolve different versions; rerun the offline checks after upgrading.

**Codex is a separate prerequisite for live runs and the functional-check sandbox probe.** Installing Python dependencies does not install it. Follow the [official Codex CLI installation instructions](https://learn.chatgpt.com/docs/codex/cli), then check it in the same terminal that will run the suite:

```sh
command -v codex
codex --version
```

The runner finds `codex` on `PATH`. An editor can provide its own executable without making it available in your terminal; add that executable's directory to `PATH` or install the CLI separately. `--codex-home` selects credential/configuration storage, not the executable. The selected build must support the flags, features, and permission overrides in [execution_command](../deliverables/runtime/codex.py), including native permission profiles and `skip_host_skill_discovery`. See [agent execution](framework-design.md#agent-execution) for the configured boundary and verification limits.

### Run offline checks

Check the infrastructure without signing in or using your subscription:

```sh
python -m unittest discover -s deliverables/tests -t . -v
python -m deliverables.tests.offline_smoke
```

Discovery uses `-t .` to import tests through the `deliverables.tests` package. To run one module, name it by package from `04-evaluations/`, for example `python -m unittest deliverables.tests.scenarios.test_scope -v`. Each scenario's grading and CLI tests are in `deliverables/tests/scenarios/test_<module>.py`; tests of the shared machinery and cross-scenario CLI guarantees are in `deliverables/tests/runtime/`.

These checks use substitutes or fake CLI processes with dummy credentials in temporary directories. They never launch real Codex or contact OpenAI. Tests inspect their own child processes with `/bin/ps`, create Unix sockets, and verify POSIX special mode bits; an enclosing agent sandbox may require permission for those operations. They do not establish live provider compatibility, actual sandbox enforcement, or coding-agent behavior. The separate [functional sandbox probe](framework-design.md#functional-check-execution) uses the real CLI without a model call.

### Authentication and credential lifetime

Use a dedicated profile outside the repository. The default is `~/.codex-evals`; supply `--codex-home PATH` consistently with login, runs, and logout to use another directory. The runner rejects personal instructions or a different configuration in that profile.

Sign in once:

```sh
python -m deliverables --login
```

Login uses device authentication, forcing ChatGPT authentication and file storage. Enable device-code sign-in in your ChatGPT security settings if requested. Codex writes plaintext credentials to `auth.json` in the selected profile and manages token refresh. The suite does not read or copy their contents. See [Codex authentication](https://learn.chatgpt.com/docs/auth).

**Credentials remain until explicit logout.** Finishing, failing, or timing out does not remove them. There is no suite-defined expiration period; provider expiry or revocation may require signing in again.

```sh
python -m deliverables --logout
```

Logout delegates to Codex for the selected profile, preserving its configuration and evaluation evidence. Local deletion does not guarantee server-side revocation. New profile directories use owner-only permissions; the suite does not repair permissions on an existing directory. Interactive login/logout are separate from automated evaluation and its timeout.

### Run a case or the suite

Each live case consumes ChatGPT subscription allowance. The suite rejects API authentication and removes API-key environment overrides rather than falling back to API billing. Use model and effort values supported by your subscription and installed CLI; both must be explicit.

Run the default smoke case, select a behavioral case, or run all cases:

```sh
python -m deliverables --model gpt-6.1-sol --reasoning-effort medium
python -m deliverables --case scope-discipline --model gpt-6.1-sol --reasoning-effort medium
python -m deliverables --case contract-change-followthrough --model gpt-6.1-sol --reasoning-effort medium
python -m deliverables --case bounded-inquiry --model gpt-6.1-sol --reasoning-effort medium
python -m deliverables --case durable-finding-review --model gpt-6.1-sol --reasoning-effort medium
python -m deliverables --case all --model gpt-6.1-sol --reasoning-effort medium
```

For another individual case, use its name from the [catalogue](../deliverables/cases-and-requirements.md#cases-and-interpretation) with `--case`. Omitting that option is equivalent to `--case smoke`.

`all` follows the catalogue order, waiting for each case and its cleanup to finish. Each has an independent workspace, Codex session, report, and evidence directory. Ordinary failures do not skip later cases; Ctrl-C or SIGTERM stops the sequence. There are no automatic retries or concurrent cases.

| Option | Use |
| --- | --- |
| `--case NAME` | One catalogue entry or `all`; defaults to `smoke`. Unknown names are rejected before execution. |
| `--model ID`, `--reasoning-effort VALUE` | Required for evaluations; the same settings apply to every selected case. |
| `--timeout SECONDS` | Positive finite agent-execution timeout per case, default 180. Other allowances are separate; see [deadlines and cleanup](framework-design.md#deadlines-and-cleanup). |
| `--codex-home PATH` | Dedicated profile selection; see [authentication](#authentication-and-credential-lifetime). |
| `--login`, `--logout` | Mutually exclusive authentication actions; cannot accompany `--case`, `--model`, or `--reasoning-effort`. |
| `--help` | Display the CLI's option reference. |

Argument errors create no evidence directory. An automated success for a human-review case, including an otherwise successful `all` run, returns `3`; it is not a full semantic pass.

## Results, evidence, and failure investigation

### Outcomes and exit codes

Read the terminal result and the selected case's `report.json` before interpreting behavior.

| Exit code | Report outcome | Meaning |
| --- | --- | --- |
| `0` | `passed` | All selected cases are fully graded and pass; no human review remains pending. |
| `1` | `assertion_failed` | Execution and evaluation completed without infrastructure errors, but at least one automated assertion failed. |
| `2` | `execution_failed` | A setup, execution, capture, inspection, interruption, evaluation, or evidence-write failure leaves verification incomplete. Argument errors also return 2, without a report. |
| `3` | `review_required` | Automated checks passed and human review remains pending. |

For multiple cases, exit precedence is **2 → 1 → 3 → 0**. Each case keeps its own outcome and pending-review flag even when another case determines the command's exit code. Infrastructure failures do not become behavioral assertion failures, and disclosure of an error does not establish successful verification.

An assertion failure can be valid evidence about the observed task, such as a wrong edit or missing preview. It is not automatically a verdict on every contract criterion. Likewise, preserving protected state can be correct restraint while the requested operational task remains incomplete; the case definitions explain that distinction.

Three kinds of failure reach these outcomes differently; the [evaluation lifecycle](framework-design.md#responsibilities-and-dependency-direction) shows where each occurs.

- **Execution failure.** When the execution callback returns an error status, the evaluation task raises an execution error before grading; an exception raised by the callback has the same effect. Agent, prerequisite, capture, inspection, interruption, and functional-check launcher errors take this path, as do evidence-write failures, which the launcher or check step folds into that status. Pydantic Evals records the raised error as a case failure instead of a graded case, so no assertions exist for that run. The report lists the error, the outcome is `execution_failed`, and the exit code is 2. This means verification is missing; it is not a failed behavioral assertion.
- **Individual evaluator failure.** Execution completed, but one evaluator raises an error while grading, for example because an observation it requires is missing or incomplete. That evaluator produces no Boolean verdict. The other evaluators still assess the same result and keep their independent assertions and reasons. The report records the evaluator error separately for that case, and the outcome is still `execution_failed` with exit code 2. As an illustration, the requester-guidance regression test `test_missing_contract_bytes_are_root_evaluator_errors_with_no_preservation_verdict` in [test_guidance.py](../deliverables/tests/scenarios/test_guidance.py) substitutes an observation in which the root contract's bytes were not captured. `RootContractPreserved` cannot compare missing bytes, so it raises and records neither preservation nor a change; `FinalResponsePresent` still reports whether the captured response has text, and `review_required` remains true. This offline test establishes grading and reporting behavior, not the result of a live run.
- **Behavioral assertion failure.** An evaluator that completes and returns `False` with a reason records evidence about the observed result; it is not an infrastructure error. A functional check that completes with a nonzero exit is such an observation, and the shared interpretation turns it into a failed assertion under the scenario's rules. A check that does not complete is an infrastructure error. Assertion failures produce `assertion_failed` and exit code 1 only when no error applies.

`report.json` keeps these categories apart: task-level execution errors, per-case evaluator errors, assertion values with their separate reasons, and failures writing the reports themselves; the [`report.json` evidence entry](#retained-evidence) names the fields. Earlier evidence-write failures, during execution or functional checks, become part of the execution error; execution-evidence failures are also listed in `execution.json` when it can be written. Any recorded error takes precedence over assertion results, so a case can show passing or failing sibling assertions and still be `execution_failed`.

### Response presence and human review

All cases marked for human review in the catalogue use `FinalResponsePresent`: a captured final response must contain non-whitespace text. Empty or whitespace-only text fails that assertion. Missing capture is an infrastructure error. Presence alone grades no meaning, regardless of how plausible the response sounds.

For these cases, `review_required: true` remains in the report after an assertion failure or infrastructure error. Human assessment happens outside the CLI; there is no keyword classifier, model judge, verdict-ingestion step, or automatic answer to an agent's question.

Use the run's `review.md` to assess its criteria separately. Read the final reply, requester-facing progress messages and commands in `events.jsonl`, and all workspace changes together. Cite relevant passages, commands, and paths; check that claims agree with actions. Information already communicated need not be repeated in the final reply. Resolve infrastructure errors before treating live verification as complete.

Apply the captured contract's rule strengths, triggers, and exceptions. Required initial framing, applicable inquiry notification, consultation, and advance disclosures retain their timing. Under the current contract, assess discretionary intermediate messages under §3.7's SHOULD recommendations to minimize routine reports and keep communication concise and useful, considering context and justification for material departures. Their presence alone is not a violation, and no message is required for every increment. Do not impose additional chat reporting solely to audit effort.

Assess technical correctness and completeness separately from compliance with exercised obligations. Unexercised duties receive no compliance pass. Where available evidence cannot support a judgment, record insufficient evidence; preserve infrastructure failures as errors. Missing visible reassessment does not itself prove that reassessment was omitted. Traces support review of observable conduct, not access to private reasoning or exact token consumption; usage claims need actual telemetry whose scope supports them.

The scenario module owns the rubric text; `review.md` preserves the rubric used for that run. Historical conclusions remain associated with their captured contract and rubric. Updating current criteria does not establish a new verdict for an earlier run. The [case explanations](../deliverables/cases-and-requirements.md#cases-and-interpretation) identify each rubric's purpose and interpretation limits without replacing it.

### Retained evidence

Each case prints its name and a distinct git-ignored `04-evaluations/.eval-runs/<timestamp>-<id>/` (repository-relative) directory. Historical evidence under `evaluations/.eval-runs/` or `_internal/.eval-runs/` remains in place; the relocation does not move or delete it. Execution and workspace evidence is retained outside the temporary workspace before it is removed; grading reports follow assessment. Earlier evidence directories are not deleted.

| File | Contents |
| --- | --- |
| `prompt.txt`, `AGENTS.md`, `message.txt` | Submitted prompt, initial contract snapshot, and initial message fixture when present. |
| `execution.json` | Contract SHA-256, CLI version when available, command/settings, paths, status, errors, duration, and exit status when available. |
| `events.jsonl`, `stderr.txt` | Raw CLI events and diagnostics once execution starts. |
| `final-response.txt` | Cases marked for human review in the catalogue (or programmatic capture): the CLI's final response, including empty text. The raw file remains available if text decoding fails. |
| `initial-workspace.json`, `final-workspace.json` | With observation (all behavioral cases): successful snapshots keyed by relative path, with `kind`, integer `mode`, `contents_base64` (exact regular-file bytes, otherwise null), and `link_target` (otherwise null). These include all observed entries. |
| `initial-workspace/`, `workspace/` | With observation: exact regular-file bytes below the initial and final workspace roots, including nested files. Copies use captured bytes, without reopening agent-controlled paths. Original permissions remain in manifests; copies are for inspection. Links, special files, and empty directories are described in manifests, not recreated. Without observation, smoke retains its final `workspace/AGENTS.md` and `workspace/message.txt` copies. |
| `workspace-changes.txt` | With observation: differences in sorted path order, including creation/deletion, types, modes, link targets, and content diffs. Text lines are JSON-quoted to expose exact whitespace and line endings; binary contents use base64. Incomplete inspection is labeled unavailable, never unchanged. These are observations, not an authorization verdict. |
| `review.md` | Each case requiring human review: a copy of its rubric with relative links to this run's evidence, retained before execution. |
| `functional-checks.json`, `checks/` | Independent-execution and contract-change-followthrough: each check's status, exit code or error, timeout, or reason it was not run; the exact evaluator-owned Python scripts and captured stdout, stderr, and launcher diagnostics. Output files contain exact bytes. These are distinct from the agent's commands and output in `events.jsonl`. |
| `report.txt`, `report.json` | Human-readable and machine-readable grading/error results. JSON includes the selected `case` and `review_required`, also on failures; each graded case has `final_response` (null without capture), boolean `assertions`, a separate `assertion_reasons` mapping, and `evaluator_errors`. Top-level `execution_errors`, `report_evaluator_errors`, and `evidence_errors` record failures outside individual assertions. See [outcomes](#outcomes-and-exit-codes) for their interpretation. |

Initial evidence setup writes `AGENTS.md`, optional `message.txt`, and `prompt.txt` in sequence. A failure stops normal setup before agent launch, without attempting the remaining initial writes; final workspace observation (when enabled), available evidence retention, and reporting still proceed, preserving the primary error and the infrastructure-failure outcome. During subsequent evidence retention, independent writes are attempted even if another fails; available observations and primary execution/check errors remain visible. Early failures can leave partial evidence or prevent directory creation entirely. Missing artifacts are not evidence of successful execution or unchanged state.

The profile and credentials are not copied into evidence. Raw events and stderr are not automatically redacted; inspect them before sharing.

### Investigate a failure or incomplete result

1. **Find the case and failure category.** Start with terminal output and `report.json`. If reports could not be written, the terminal retains the primary error and evidence-write diagnostics. A pending-review flag does not disappear because a failure has higher precedence.
2. **For an infrastructure error, inspect execution evidence.** Use `execution.json` for command/settings, execution status, primary error, and evidence errors, then `stderr.txt` and `events.jsonl` if present. For missing CLI or login/configuration errors, check the documented `PATH` and dedicated profile rather than assuming an editor's setup is shared.
3. **Separate failed observation from observed failure.** A missing/incomplete snapshot cannot prove preservation. A successfully observed missing or non-regular file is assessed under the case's rules. Capture failures are errors; a successfully captured empty response is an assertion failure. See [observation and capture boundaries](framework-design.md#observation-and-capture-boundaries).
4. **For assertion failures, inspect the specific reasons.** Compare `assertions` with `assertion_reasons`, the readable differences, and exact bytes/modes in the manifests. File copies are convenient for reading; manifests preserve original metadata. An observation of a change is not itself a judgment that it was unauthorized.
5. **For independent-execution and contract-change-followthrough, inspect the separate checks.** `functional-checks.json` and `checks/` distinguish completed nonzero checks, launcher/check errors, and skipped checks with reasons. These results are not evidence that the agent ran its own tests. Use the [sandbox probe](framework-design.md#functional-check-execution) when investigating enforcement; there is no unsandboxed fallback.
6. **For pending semantics, follow the retained rubric.** Automated success cannot settle missing authorization, meaningful tests, accurate disclosure, a consequential trade-off, measurement provenance and bounded inquiry conduct, or adequate permanent recording of an established durable finding.

After correcting an infrastructure problem, a new selected-case run gets fresh workspace and evidence directories. Keep the failed run's evidence when comparing results; rerunning does not repair or complete its record.
