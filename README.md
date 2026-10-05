# AGENTS.md Specification

A ready-to-use [AGENTS.md](AGENTS.md) that gives coding agents a consistent way to work in new or established repositories.

Its primary aim is to prevent unconstrained token use: investigations that keep expanding, detailed planning for distant work, or unexpectedly heavy effort within a single step.

Describe the outcome you want. The agent selects a **small, useful step**, completes the necessary analysis, work, documentation, and checks, then uses the results to decide what follows. Later detail develops as evidence becomes available. The agent can continue within your authorization, but must ask for direction before undertaking substantially more work or investigation than expected.

Effort control is best effort. These instructions provide no token meter, hard quota, or guarantee of savings.

## Get started

1. **Review existing instructions, then copy [AGENTS.md](AGENTS.md) into your repository root.** A person responsible for adoption must validate which existing practices, conventions, and workflows will persist and which will be replaced. Preserve useful project facts found only in the old files—such as build commands or system constraints—in appropriate project documentation after checking their accuracy. Retained operating rules belong in authoritative instruction files: use compatible additions or an explicitly authorized contract adaptation, following the [instruction-file rules](README-powerusers.md#instruction-files-and-external-actions).
2. **Add the bridge for your tool, if applicable.** Use the supplied files at the paths below, applying the same human review and fact-preservation precautions before replacing existing copies.

   | Tool | Files to use |
   | --- | --- |
   | Codex | Root `AGENTS.md` |
   | Claude Code | Root `AGENTS.md` and [CLAUDE.md](CLAUDE.md) |
   | GitHub Copilot | Root `AGENTS.md` and [.github/copilot-instructions.md](.github/copilot-instructions.md) |

3. **Keep the files in version control and check adoption.** Ask your tool which repository instructions it loaded and check available instruction diagnostics. Then try the [worked adoption check](README-powerusers.md#worked-adoption-check): it combines a loading check with a small assessment task. Finding a file alone does not show that the agent follows it.

The supplied contract normally needs no project-specific customization. Keep project facts, build commands, and architecture in your project's documentation and code. The bridges direct the tool to the contract.

Loading depends on the interface and settings. For verification, troubleshooting, and use with ChatGPT or Claude Projects, see [tool compatibility](README-powerusers.md#tool-compatibility).

## Try a first task

Ask for the result you need:

> Fix the incorrect setup command in the README.

For this one-step task, the agent inspects the relevant project files, makes the correction, checks it, and reports the completed task. For example, if the documented command disagreed with the project's package configuration and the corrected command ran successfully, a brief report could be:

> Corrected the setup command in `README.md` to match the package configuration. Ran the corrected command successfully.

That is an illustration, not a required response template. If a check fails or cannot run, the agent must say so. Disclosure alone does not establish completion: acceptance conditions still need sufficient evidence, and a specifically required check cannot be bypassed. See [validation and unavailable checks](README-powerusers.md#assess-the-result). You do not need to repeat these responsibilities in your request.

For a larger objective, use the same approach:

> Add CSV imports that report invalid rows and continue processing valid rows.

The agent chooses the next small, useful step—called an **increment**—from your request and the project context. It works through Plan–Do–Study–Act (PDSA): plan the step, do the work, assess the result, and use what it learned to decide what follows. Later work stays at outline level until it needs more detail. The [worked example](README-powerusers.md#from-a-request-to-a-result) shows this process from request to report.

Further increments can proceed under existing authorization. The agent combines unreported work into a report at task completion, at a handoff, or when asking for your input. While continuing, it must not draft or output routine progress reports unless requested or otherwise required.

Disclosures affecting authorization or the next decision come before the affected work; other disclosures join the next consolidated report unless an earlier time is specified. The agent pauses when the contract, your instructions, or the tool's rules require direction, including before unexpectedly greater work. It uses your effort expectations where supplied and otherwise establishes them without a routine announcement. You can request status updates or [extra review checkpoints](README-powerusers.md#optional-controls-you-can-add) if you want to follow individual increments.

## What to expect

- **Focused progress.** The agent selects each step using your objective, relevant project evidence, and earlier findings. Unrelated cleanup and speculative features stay outside the task.
- **Complete work within each step.** Small scope still receives the necessary reasoning and validation. Affected code, tests, configuration, and documentation stay consistent. A required stop can leave a step unfinished; it cannot be reported as complete.
- **Decisions and consolidated results.** Consequential unresolved questions come to you. Reports identify completed work, checks, material assumptions, and unfinished work; one report can cover several increments.
- **Bounded investigations.** Inspecting the relevant code, callers, tests, configuration, and directly related dependencies to establish starting context, and all reading of existing project documentation, are context gathering. Documentation reading remains exempt from inquiry framing even when answering a blocking question. Other activity aimed at resolving material uncertainty blocking the next decision, such as experiments or exploration beyond that context, is inquiry whatever it is called; it requires the question, scope, objective, needed evidence, and an effort limit before it starts or continues. The agent stops that inquiry when it obtains the evidence or reaches the limit; missing required evidence means incomplete work. Existing scope and authority can permit another bounded attempt, subject to requester limits, checkpoints, and reassessment of materially greater effort. All work, including context gathering, remains subject to scope and growth limits. See [investigation examples](README-powerusers.md#when-an-investigation-is-needed).
- **Project knowledge that develops with the work.** Adoption includes architecture documentation organized around arc42, a set of topics for explaining a software system, along with clearly expressed requirements and records of significant decisions. These practices support quality and preserve knowledge for later steps. You can limit or defer proposed documentation improvements. Installation does not authorize a project-wide audit or rewrite.

This is an opinionated engineering baseline. Your instructions take priority within the tool's actual instruction hierarchy and permissions. You remain responsible for reviewing and accepting the work.

Instruction files cannot guarantee compliance. The tool's controls govern permissions and approvals.

## Get more from it

- **[Getting more from AGENTS.md](README-powerusers.md)** — practical examples, when the agent pauses, and existing-project alignment. No technical background is required to follow the collaboration guidance.
- **[The design of AGENTS.md](README-maintainers.md)** — design reasons, engineering choices, sources, constraints, and trade-offs that inform changes to the contract.
- **[AGENTS.md](AGENTS.md)** — the complete operating rules, conditions, and exceptions.
