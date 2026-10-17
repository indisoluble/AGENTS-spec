# Local evaluation smoke test

This suite checks that Python can prepare a workspace, launch Codex, grade its actual output with Pydantic Evals, and retain evidence. One case asks Codex to replace `before\n` with exactly `after\n` in `message.txt`, alongside an unchanged copy of the current root [AGENTS.md](AGENTS.md).

A pass demonstrates that the infrastructure works. It does not establish scope discipline, PDSA compliance, human guidance, effort escalation, or other behavioral compliance. Those evaluations, containers, and CI remain deferred.

## Setup and commands

Run commands from the repository root. Use Python 3.11 or newer and a POSIX system; verification so far uses macOS with Python 3.14. Windows is not supported by the process-group and file-opening implementation.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt
```

[requirements.txt](requirements.txt) owns the dependency range. It allows Pydantic Evals minor and patch upgrades within major version 2. Dependencies are not locked, so installations can resolve different versions; rerun the offline checks after upgrading.

**Codex is a separate prerequisite.** Installing Python dependencies does not install it. Follow the [official Codex CLI installation instructions](https://learn.chatgpt.com/docs/codex/cli), then check it in the same terminal that will run the suite:

```sh
command -v codex
codex --version
```

The runner finds `codex` on `PATH`. An editor can provide its own executable without making it available in your terminal; add that executable's directory to `PATH` or install the CLI separately. `--codex-home` selects credential/configuration storage, not the executable. The verified CLI build is `0.162.0-alpha.17.2`; another build must support the flags and features in [execution_command](evals/codex.py), including `skip_host_skill_discovery`.

Check the infrastructure without signing in or using your subscription:

```sh
python -m unittest discover -s tests -v
python -m tests.offline_smoke
```

The tests use substitutes or fake CLI processes with dummy credentials in temporary directories. They never launch real Codex or contact OpenAI. The failure tests send signals to their own child processes and use `/bin/ps` to check cleanup; an enclosing agent sandbox may require permission to perform that inspection.

Sign in once, then run one live case:

```sh
python -m evals --login
python -m evals --model gpt-6.1-sol --reasoning-effort medium
```

Use model and effort values supported by your subscription and installed CLI. `--timeout SECONDS` accepts a positive finite number and defaults to 180. Each command runs one case in one fresh session, with no automatic retries or concurrent cases. A live run uses your ChatGPT subscription allowance; the suite rejects API authentication and removes API-key environment overrides instead of falling back to API billing.

| Exit code | Meaning |
| --- | --- |
| `0` | Execution completed and exact-content grading passed. |
| `1` | Execution completed, but the content assertion failed. |
| `2` | Setup, execution, interruption, evaluation, or evidence writing failed. |

## Authentication and credential lifetime

The default dedicated profile is `~/.codex-evals`. To choose another directory, supply `--codex-home PATH` consistently with login, runs, and logout. Use a dedicated directory outside the repository; personal instructions or a different configuration cause the runner to reject the profile.

Login launches `codex login --device-auth` with that directory as `CODEX_HOME`, forcing ChatGPT authentication and file storage. Enable device-code sign-in in your ChatGPT security settings if requested. Codex writes plaintext credentials to `auth.json` there and manages token refresh. The suite does not read or copy the credential contents. See [Codex authentication](https://learn.chatgpt.com/docs/auth).

**Credentials are retained until explicit logout.** A test finishing, failing, or timing out does not remove them. There is no suite-defined expiration period; provider expiry or revocation may require signing in again. To remove the saved login:

```sh
python -m evals --logout
```

Logout delegates to Codex for the selected profile and preserves its configuration and evaluation evidence. Local deletion does not guarantee server-side revocation. The suite creates new profile directories with owner-only permissions; it does not repair permissions on an existing directory. Interactive login/logout are separate from automated evaluation and its timeout.

## Execution and evidence

[smoke.py](evals/smoke.py) owns the case, temporary workspace, `ExecutionResult`, and exact-content evaluator. Its injected execution function accepts `(prompt, workspace)` and returns `ExecutionResult(status, file_contents, error)`. A future container launcher can preserve this interface without changing the case or evaluator.

[auth.py](evals/auth.py) owns profile/authentication operations; [codex.py](evals/codex.py) owns the controlled command and evidence; [process.py](evals/process.py) owns subprocess lifetimes; [__main__.py](evals/__main__.py) assembles these and reports the outcome. Pydantic runs the synchronous task in a worker thread. Main-thread SIGINT (Ctrl-C) and SIGTERM handlers set a cancellation event that the process owner observes, then restore the original handlers on exit.

The execution timeout covers `codex exec`. Version and authentication checks each have a separate 15-second timeout. Processes are checked for cancellation at intervals of at most 0.1 seconds while waiting. Cleanup sends SIGTERM to the launched process group, waits up to two seconds for its parent, then sends SIGKILL to the group, including children that outlive the parent. Startup, filesystem operations, reporting, and cleanup add time: `--timeout` is not a hard deadline for the entire Python command.

Each run prints a git-ignored `.eval-runs/<timestamp>-<id>/` evidence directory:

| File | Contents |
| --- | --- |
| `prompt.txt`, `AGENTS.md` | Submitted prompt and initial contract snapshot. |
| `execution.json` | Contract SHA-256, CLI version when available, command/settings, paths, status, errors, duration, and exit status when available. |
| `events.jsonl`, `stderr.txt` | Raw CLI events and diagnostics once execution starts. |
| `workspace/AGENTS.md`, `workspace/message.txt` | Final regular fixture files, when present and readable. |
| `report.txt`, `report.json` | Human-readable and machine-readable grading/error results. |

The runner reads the actual output file; an agent's claim of success is insufficient. Missing output fails grading; unreadable, non-regular, or symbolic-link fixtures produce execution errors. Available evidence is saved before the temporary workspace is removed. Failed writes are reported independently and retain the original execution error; early setup failures can leave only partial evidence. Runs do not delete earlier evidence.

The profile and credentials are not copied to the evidence directory. Raw events and stderr are not automatically redacted; inspect them before sharing.

## Execution boundaries

Codex receives explicit model/effort settings, `workspace-write` sandboxing, no interactive approvals, and no shell network access. The model connection still requires network access. The runner ignores user configuration and rules, disables personal extensions and host skill discovery, and uses an ephemeral session. Ephemeral execution suppresses session persistence, not the saved login. See [non-interactive Codex execution](https://learn.chatgpt.com/docs/non-interactive-mode).

Built-in prompts, platform enforcement, and managed requirements/instructions may still apply. Temporary workspaces and sandboxing are not complete host isolation: code and grading live outside the writable fixture, but host reads and tool/platform behavior remain relevant. Cleanup covers descendants in the launched process group; it cannot guarantee cleanup after SIGKILL of the Python runner, a machine failure, or descendants escaping into a different process group. Model behavior and service availability are nondeterministic even though grading is deterministic.

## Verifiable requirements

This section owns the suite's requirements; the linked code/tests provide implementation evidence.

| ID | Requirement | Checks |
| --- | --- | --- |
| E1 | When a case starts, the suite shall provide a fresh temporary workspace containing the initial fixture and an unchanged copy of the current root contract. | [test_smoke.py](tests/test_smoke.py), live run |
| E2 | When execution completes, the suite shall compare the returned file contents exactly with the expected contents, including whitespace, treating missing output as a failed assertion. | [test_smoke.py](tests/test_smoke.py) |
| E3 | If execution reports an error or raises an exception, then the suite shall report an execution failure separately from content assertions. | [test_smoke.py](tests/test_smoke.py), [test_codex_failures.py](tests/test_codex_failures.py) |
| E4 | When a case finishes or raises, the suite shall remove its temporary workspace. | [test_smoke.py](tests/test_smoke.py), [test_codex_failures.py](tests/test_codex_failures.py) |
| E5 | If a fixture is a symbolic link or non-regular file, then the suite shall reject it without reading its contents. | [test_evidence.py](tests/test_evidence.py) |
| E6 | The suite shall use `~/.codex-evals` by default, or the selected `--codex-home`, for login, logout, and evaluation, retaining credentials until explicit logout and delegating credential removal to Codex for that profile only. | [test_auth.py](tests/test_auth.py) |
| E7 | When launching a case, the suite shall require ChatGPT authentication, exclude API-key overrides and personal configuration, and explicitly select model, effort, workspace-write sandboxing, and noninteractive approvals. | [test_codex.py](tests/test_codex.py), [test_codex_failures.py](tests/test_codex_failures.py), retained command/live run |
| E8 | When execution ends, the suite shall attempt to retain the evidence listed above outside the temporary workspace. | [test_codex.py](tests/test_codex.py), live run |
| E9 | If evidence writing fails, then the suite shall preserve the execution error, attempt remaining independent writes, and report write errors in the terminal. | [test_evidence.py](tests/test_evidence.py) |
| E10 | If a launched evaluation subprocess times out or evaluation receives SIGINT or SIGTERM, then the suite shall stop the launched process group and retain available evidence under the execution boundaries above. | [test_codex_failures.py](tests/test_codex_failures.py) |
| E11 | The suite shall return exit code 0 for success, 1 for assertion failure, and 2 for setup, execution, interruption, evaluation, or evidence-write failure. | [test_auth.py](tests/test_auth.py), [test_codex.py](tests/test_codex.py), [test_codex_failures.py](tests/test_codex_failures.py), [test_evidence.py](tests/test_evidence.py) |

For release verification, run the offline checks and inspect a live run's report, actual retained file bytes, contract hash, model settings, and cleaned workspace path. Repeating the live command should produce a distinct workspace and evidence directory. Keep those run-specific results in the evidence, rather than duplicating them here.
