# Running and reviewing evaluations

This document owns installation, authentication, case execution, retained evidence, report interpretation, failure investigation, and human review. Start with [`05-evaluation/docs/evaluation-model.md` § Purpose and evaluation model](evaluation-model.md#purpose-and-evaluation-model) for the suite's scope and interpretation limits.

Use [`05-evaluation/README.md` § Case specifications](../README.md#case-specifications) to find the selected case's source module and exact rubric. The stage README ([`05-evaluation/README.md` § Evaluator requirements](../README.md#evaluator-requirements)) links the case-specific and shared evaluator requirements. [`05-evaluation/docs/framework-design.md`](framework-design.md) owns execution, observation, cleanup, and functional-check boundaries; the links below connect operational results to those mechanisms. A historical run is interpreted using its captured contract and rubric, as the [review procedure](#response-presence-and-human-review) explains.

## Setup and running evaluations

### Install prerequisites

Run evaluator commands from the repository root. Use Python 3.11 or newer and a POSIX system. Windows is not supported by the process-group and file-opening implementation. Runtime compatibility and sandbox enforcement need separate validation in the target environment; see [`engine/docs/framework-design.md` § Agent execution](../../engine/docs/framework-design.md#agent-execution). From the repository root, set up the source import roots:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade -r engine/requirements.txt
export PYTHONPATH="$PWD:$PWD/03.1-conformance/deliverables:$PWD/05-evaluation/deliverables"
```

[`engine/requirements.txt`](../../engine/requirements.txt) owns the dependency range. It allows Pydantic Evals minor and patch upgrades within major version 2. Dependencies are not locked, so installations can resolve different versions; rerun the offline checks after upgrading.

**Codex is a separate prerequisite for live runs and the functional-check sandbox probe.** Installing Python dependencies does not install it. Follow the [official Codex CLI installation instructions](https://learn.chatgpt.com/docs/codex/cli), then check it in the same terminal that will run the suite:

```sh
command -v codex
codex --version
```

The runner finds `codex` on `PATH`. An editor can provide its own executable without making it available in your terminal; add that executable's directory to `PATH` or install the CLI separately. `--codex-home` selects credential/configuration storage, not the executable. The selected build must support the flags, features, and permission overrides in execution_command ([`engine/runtime/codex.py`](../../engine/runtime/codex.py)), including native permission profiles and `skip_host_skill_discovery`. See [`engine/docs/framework-design.md` § Agent execution](../../engine/docs/framework-design.md#agent-execution) for the configured boundary and verification limits.

### Run offline checks

Check the infrastructure without signing in or using your subscription:

```sh
python -m unittest discover -s engine/tests -t . -v
python -m unittest discover -s 03.1-conformance/deliverables/conformance/tests -t 03.1-conformance/deliverables -v
python -m unittest discover -s 05-evaluation/deliverables/evaluation/tests -t 05-evaluation/deliverables -v
python -m engine.tests.offline_smoke
```

Each discovery root imports its own package exactly once. For one integration module, use `python -m unittest -v evaluation.tests.runtime.test_cli`.

These checks use substitutes or fake CLI processes with dummy credentials in temporary directories. They never launch real Codex or contact OpenAI. Tests inspect their own child processes with `/bin/ps`, create Unix sockets, and verify POSIX special mode bits; an enclosing agent sandbox may require permission for those operations. They do not establish live provider compatibility, actual sandbox enforcement, or coding-agent behavior. The separate functional sandbox probe ([`engine/docs/framework-design.md` § Functional-check execution](../../engine/docs/framework-design.md#functional-check-execution)) uses the real CLI without a model call.

### Authentication and credential lifetime

Use a dedicated profile outside the repository. The default is `~/.codex-evals`; supply `--codex-home PATH` consistently with login, runs, and logout to use another directory. The runner rejects personal instructions or a different configuration in that profile.

Sign in once:

```sh
python -m evaluation --login
```

Login uses device authentication, forcing ChatGPT authentication and file storage. Enable device-code sign-in in your ChatGPT security settings if requested. Codex writes plaintext credentials to `auth.json` in the selected profile and manages token refresh. The suite does not read or copy their contents. See [Codex authentication](https://learn.chatgpt.com/docs/auth).

**Credentials remain until explicit logout.** Finishing, failing, or timing out does not remove them. There is no suite-defined expiration period; provider expiry or revocation may require signing in again.

```sh
python -m evaluation --logout
```

Logout delegates to Codex for the selected profile, preserving its configuration and evaluation evidence. Local deletion does not guarantee server-side revocation. New profile directories use owner-only permissions; the suite does not repair permissions on an existing directory. Interactive login/logout are separate from automated evaluation and its timeout.

### Run a case or the suite

Each live case consumes ChatGPT subscription allowance. The suite rejects API authentication and removes API-key environment overrides rather than falling back to API billing. Use model and effort values supported by your subscription and installed CLI; both must be explicit.

Run the default smoke case, select a behavioral case, or run all cases:

```sh
python -m evaluation --model gpt-6.1-sol --reasoning-effort medium
python -m evaluation --case scope-discipline --model gpt-6.1-sol --reasoning-effort medium
python -m evaluation --case contract-change-followthrough --model gpt-6.1-sol --reasoning-effort medium
python -m evaluation --case bounded-inquiry --model gpt-6.1-sol --reasoning-effort medium
python -m evaluation --case durable-finding-review --model gpt-6.1-sol --reasoning-effort medium
python -m evaluation --case all --model gpt-6.1-sol --reasoning-effort medium
```

For another individual case, use its name from the accepted case selections ([`05-evaluation/deliverables/requirements/suite-execution-and-results.md` § E12](../deliverables/requirements/suite-execution-and-results.md#e12)) with `--case`. Omitting that option is equivalent to `--case smoke`.

`all` follows the order defined by E15 ([`05-evaluation/deliverables/requirements/suite-execution-and-results.md` § E15](../deliverables/requirements/suite-execution-and-results.md#e15)), waiting for each case and its cleanup to finish. Each has an independent workspace, Codex session, report, and evidence directory. Ordinary failures do not skip later cases; Ctrl-C or SIGTERM stops the sequence. There are no automatic retries or concurrent cases.

| Option | Use |
| --- | --- |
| `--case NAME` | A registered case name or `all`. The default is `smoke`. Unknown names are rejected before execution. |
| `--model ID`, `--reasoning-effort VALUE` | Required for evaluations; the same settings apply to every selected case. |
| `--timeout SECONDS` | Positive finite agent-execution timeout per case, default 180. Other allowances are separate; see [`engine/docs/framework-design.md` § Deadlines and cleanup](../../engine/docs/framework-design.md#deadlines-and-cleanup). |
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

When grading proceeds, contract-change-followthrough reports its five assertions independently and durable-finding-review reports its two assertions independently. Bounded-inquiry and durable-finding-review report `review_required` on automated success when no infrastructure error takes precedence. [`05-evaluation/deliverables/requirements/suite-execution-and-results.md` § E38](../deliverables/requirements/suite-execution-and-results.md#e38) · [`05-evaluation/deliverables/requirements/suite-execution-and-results.md` § E39](../deliverables/requirements/suite-execution-and-results.md#e39) · [`05-evaluation/deliverables/requirements/suite-execution-and-results.md` § E40](../deliverables/requirements/suite-execution-and-results.md#e40)

An assertion failure can be valid evidence about the observed task, such as a wrong edit or missing preview. It is not automatically a verdict on every contract criterion. Likewise, preserving protected state can be correct restraint while the requested operational task remains incomplete; the case definitions explain that distinction.

To locate a failure in the evaluation lifecycle ([`05-evaluation/docs/framework-design.md` § Responsibilities and dependency direction](framework-design.md#responsibilities-and-dependency-direction)), read the fields for the individual case.

- **Execution failed before grading.** An execution callback error status or exception becomes a task failure in `execution_errors`. Prerequisite, agent, capture, inspection and functional-check launcher errors can take this path. No assertions were graded for that task.
- **An evaluator could not grade its criterion.** Look for `evaluator_errors` in the graded case. Other assertions keep their values and reasons. For example, when the capture lacks the root contract's bytes, `RootContractPreserved` has no verdict, but `FinalResponsePresent` can still succeed and review remains pending. The offline requester-guidance regression test ([`05-evaluation/deliverables/evaluation/tests/scenarios/test_guidance.py`](../deliverables/evaluation/tests/scenarios/test_guidance.py)) exercises this distinction.
- **An assertion returned false.** Read its entry in `assertion_reasons` against the case specification. A completed nonzero functional check can fail a behavioral assertion. Failure to complete the check is an infrastructure error.

Also inspect report-level evaluator and write errors in the [report fields](#retained-evidence). Write failures during execution or functional checks enter the execution error. When available, `execution.json` also lists errors retaining execution evidence. Any recorded error takes precedence when the CLI determines the outcome. Early failures may produce only a short report with an `error` field or a terminal diagnostic.

### Response presence and human review

Cases requiring human review use the reusable `FinalResponsePresent` assertion. Use the retained rubric to assess what the response means and whether it matches the observed conduct. [`engine/docs/framework-design.md` § Response-presence assessment](../../engine/docs/framework-design.md#response-presence-assessment)

Under [`05-evaluation/deliverables/requirements/suite-execution-and-results.md` § E26](../deliverables/requirements/suite-execution-and-results.md#e26), `review_required: true` remains in the report for these cases after an assertion failure or infrastructure error. Human assessment happens outside the CLI; there is no keyword classifier, model judge, verdict-ingestion step, or automatic answer to an agent's question.

Use the run's `review.md` to assess its criteria separately. Its presence means the rubric was supplied. To establish that a person actually reviewed the run, look for their assessment associated with that evidence directory. Read the final reply, requester-facing progress messages and commands in `events.jsonl`, and all workspace changes together. For requester-guidance, compare the documentation and code changes with what the agent told the requester. Cite relevant passages, commands, and paths. Check that claims agree with actions. Record the assessment with the evidence for that run. Information already communicated need not be repeated in the final reply. Resolve infrastructure errors before treating live verification as complete.

Apply the captured contract's rule strengths, triggers, and exceptions. Required initial framing, applicable inquiry notification, consultation, and advance disclosures retain their timing. Under the current contract, assess discretionary intermediate messages under §3.7's SHOULD recommendations to minimize routine reports and keep communication concise and useful, considering context and justification for material departures. Their presence alone is not a violation, and no message is required for every increment. Do not impose additional chat reporting solely to audit effort.

Assess technical correctness and completeness separately from compliance with exercised obligations. Unexercised duties receive no compliance pass. Where available evidence cannot support a judgment, record insufficient evidence; preserve infrastructure failures as errors. Missing visible reassessment does not itself prove that reassessment was omitted. Traces support review of observable conduct, not access to private reasoning or exact token consumption; usage claims need actual telemetry whose scope supports them.

The scenario module owns the rubric text; `review.md` preserves the rubric used for that run. Historical conclusions remain associated with their captured contract and rubric. Updating current criteria does not establish a new verdict for an earlier run. The case specifications ([`05-evaluation/README.md` § Case specifications](../README.md#case-specifications)) identify each rubric's purpose and interpretation limits without replacing it.

### Retained evidence

Each case prints its name and a distinct git-ignored `05-evaluation/.eval-runs/<timestamp>-<id>/` directory, relative to the repository root. For older local runs, also look under `05-evaluations/.eval-runs/`, `04-evaluations/.eval-runs/`, `evaluations/.eval-runs/` and `_internal/.eval-runs/`. Each run keeps its own evidence directory. Execution and workspace evidence is retained outside the temporary workspace before that workspace is removed. Grading reports follow assessment.

| File | Contents |
| --- | --- |
| `prompt.txt`, `AGENTS.md`, `message.txt` | Submitted prompt, initial contract snapshot, and initial message fixture when present. |
| `execution.json` | `contract_sha256` identifies the initial `AGENTS.md` snapshot saved by [`engine/runtime/codex.py`](../../engine/runtime/codex.py). Also records CLI version when available, command/settings, paths, status, errors, duration, and exit status when available. |
| `events.jsonl`, `stderr.txt` | Raw CLI events and diagnostics. The launcher opens these files before starting the agent process, so their presence alone cannot establish a completed turn. |
| `final-response.txt` | The CLI's final response, including empty text, for human-review cases or programmatic capture. The raw file remains available if text decoding fails. |
| `initial-workspace.json`, `final-workspace.json` | With observation (all behavioral cases): successful snapshots keyed by relative path, with `kind`, integer `mode`, `contents_base64` (exact regular-file bytes, otherwise null), and `link_target` (otherwise null). These include all observed entries. |
| `initial-workspace/`, `workspace/` | With observation: exact regular-file bytes below the initial and final workspace roots, including nested files. Copies use captured bytes, without reopening agent-controlled paths. Original permissions remain in manifests; copies are for inspection. Links, special files, and empty directories are described in manifests, not recreated. Without observation, smoke retains its final `workspace/AGENTS.md` and `workspace/message.txt` copies. |
| `workspace-changes.txt` | With observation: differences in sorted path order, including creation/deletion, types, modes, link targets, and content diffs. Text lines are JSON-quoted to expose exact whitespace and line endings; binary contents use base64. Incomplete inspection is labeled unavailable, never unchanged. These are observations, not an authorization verdict. |
| `review.md` | Each case requiring human review: a copy of its rubric with relative links to this run's evidence, retained before execution. |
| `functional-checks.json`, `checks/` | For independent-execution and contract-change-followthrough, each check's status, exit code or error, timeout, or reason it was skipped. The directory retains the evaluator-owned scripts, exact captured check stdout and stderr bytes, and separate launcher diagnostics. The agent's own commands and output appear in `events.jsonl`. |
| `report.txt`, `report.json` | Human-readable and machine-readable grading/error results. JSON includes the selected `case` and `review_required`, also on failures; each graded case has `final_response` (null without capture), boolean `assertions`, a separate `assertion_reasons` mapping, and `evaluator_errors`. Top-level `execution_errors`, `report_evaluator_errors`, and `evidence_errors` record failures outside individual assertions. See [outcomes](#outcomes-and-exit-codes) for their interpretation. |

Initial evidence setup writes `AGENTS.md`, optional `message.txt`, and `prompt.txt` in sequence. A failure stops normal setup before agent launch, without attempting the remaining initial writes; final workspace observation (when enabled), available evidence retention, and reporting still proceed, preserving the primary error and the infrastructure-failure outcome. During subsequent evidence retention, independent writes are attempted even if another fails; available observations and primary execution/check errors remain visible. Early failures can leave partial evidence or prevent directory creation entirely. Missing artifacts are not evidence of successful execution or unchanged state.

Use the evidence listed above with the retained rubric for bounded-inquiry and durable-finding-review. Durable-finding-review has no `functional-checks.json` or `checks/` artifacts. [`05-evaluation/deliverables/requirements/workspace-and-observation.md` § E19](../deliverables/requirements/workspace-and-observation.md#e19) · [`05-evaluation/deliverables/requirements/workspace-and-observation.md` § E20](../deliverables/requirements/workspace-and-observation.md#e20) · [`05-evaluation/deliverables/requirements/evidence-and-capture.md` § E21](../deliverables/requirements/evidence-and-capture.md#e21) · [`engine/requirements/evidence-and-capture.md` § E23](../../engine/requirements/evidence-and-capture.md#e23)

The profile and credentials are not copied into evidence. Raw events and stderr are not automatically redacted; inspect them before sharing.

### Identify the Candidate and evaluator used

Evaluation selects the staged Candidate on the first successful setup read and retains those immutable bytes for every case in the invocation. The evidence hash is calculated from the actual initial workspace file. For a completed capture, compare the SHA-256 of the run directory's `AGENTS.md` with `contract_sha256` in `execution.json`. To check a particular Candidate, hash the raw bytes of its `04-candidate/pre_AGENTS.md` the same way. The hash identifies the injected contract only. Use `report.json` for the case and `execution.json` for the recorded model, effort and Codex CLI version when available.

The run bundle has no automatic identifier for the evaluator source revision or installed Pydantic Evals version. For a version-sensitive comparison, identify the checkout and environment **at run time** in the associated review record. From the repository root with the evaluation environment active, use these commands to identify the revision, local evaluator changes and installed versions.

```sh
git rev-parse HEAD
git status --short --untracked-files=all -- engine/ 02.1-acceptance/ 03.1-conformance/ 05-evaluation/
python --version
python -m pip show pydantic-evals
```

If the evaluator has local edits, retain the relevant changes with that reference so the case and grading code can be identified. For an older run, use its own evidence and any contemporaneous review reference. A matching contract hash or case name alone cannot recover the evaluator revision. If its version is unknown, qualify comparisons accordingly. Run and expectation traceability ([`docs/traceability.md` § Tracing a requirement and its evaluation](../../docs/traceability.md#tracing-a-requirement-and-its-evaluation))

### Investigate a failure or incomplete result

1. **Find the case and failure category.** Start with terminal output and `report.json`. If reports could not be written, the terminal retains the primary error and evidence-write diagnostics. A pending-review flag does not disappear because a failure has higher precedence.
2. **For an infrastructure error, inspect execution evidence.** Read `execution.json` for the primary error, command/settings and evidence errors. A missing CLI, rejected profile or missing ChatGPT login can stop setup before a turn starts. Check the terminal's `PATH` and the selected authentication directory. If the command ran, inspect its return code, `stderr.txt` and `events.jsonl`. The launcher requires exit zero, a `turn.completed` event and no `turn.failed` event. Partial output can survive an incomplete turn.
3. **Separate failed observation from observed failure.** A missing/incomplete snapshot cannot prove preservation. A successfully observed missing or non-regular file is assessed under the case's rules. Capture failures are errors; a successfully captured empty response is an assertion failure. See [`engine/docs/framework-design.md` § Observation and capture boundaries](../../engine/docs/framework-design.md#observation-and-capture-boundaries).
4. **For assertion failures, inspect the specific reasons.** Compare `assertions` with `assertion_reasons`, the readable differences, and exact bytes/modes in the manifests. File copies are convenient for reading; manifests preserve original metadata. An observation of a change is not itself a judgment that it was unauthorized.
5. **For independent-execution and contract-change-followthrough, inspect the separate checks.** `functional-checks.json` and `checks/` distinguish completed nonzero checks, launcher/check errors, and skipped checks with reasons. These results are not evidence that the agent ran its own tests. Use the sandbox probe ([`engine/docs/framework-design.md` § Functional-check execution](../../engine/docs/framework-design.md#functional-check-execution)) when investigating enforcement; there is no unsandboxed fallback.
6. **For pending semantics, follow the retained rubric.** Automated success cannot settle missing authorization, meaningful tests, accurate disclosure, a consequential trade-off, measurement provenance and bounded inquiry conduct, or adequate permanent recording of an established durable finding.

After correcting an infrastructure problem, a new selected-case run gets fresh workspace and evidence directories. Keep the failed run's evidence when comparing results; rerunning does not repair or complete its record.
