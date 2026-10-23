# AGENTS.md Specification

A ready-to-use [AGENTS.md](AGENTS.md) that gives coding agents a consistent way to work in new or established repositories.

Its primary aim is to prevent unconstrained token use: investigations that keep expanding, detailed planning for distant work, or unexpectedly heavy effort within a single step.

Describe the outcome you want. The agent selects a **small, useful step**, completes the necessary analysis, work, documentation, and checks, then uses the results to decide what follows. Later detail develops as evidence becomes available. The agent can continue within your authorization, but must ask for direction before undertaking substantially more work or investigation than expected.

Effort control is best effort. These instructions provide no token meter, hard quota, or guarantee of savings.

## Get started

1. **Review existing instructions, then copy [AGENTS.md](AGENTS.md) into your repository root.** If your project already has agent instructions, the person responsible for adoption must review and confirm which practices, conventions, and workflows will remain and which will be replaced before overwriting them.

   Verify and preserve project facts found only in the old instruction files—such as build commands and deployment constraints—in appropriate project documentation before replacement.

   Retained operating rules belong in authoritative instruction files. Keep compatible additions, or explicitly authorize an adaptation of the contract, following the [instruction-file rules](README-powerusers.md#instruction-files-and-external-actions).

2. **Add the bridge for your tool, if applicable.** The supplied bridges direct the tool to the shared root contract, keeping operating policy in `AGENTS.md`. Use the files at the paths below, applying the same review and preservation steps before replacing existing copies.

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

That is an illustration, not a required response template. If a check fails or cannot run, the agent must say so; saying so does not establish completion. See [validation and unavailable checks](README-powerusers.md#assess-the-result). You do not need to repeat these responsibilities in your request.

For a larger objective, use the same approach:

> Add CSV imports that report invalid rows and continue processing valid rows.

The agent chooses the next small, useful step—called an **increment**—from your request and the project context. It works through Plan–Do–Study–Act (PDSA): plan the step, do the work, assess the result, and use what it learned to decide what follows. Later work stays at outline level until it needs more detail. The [worked example](README-powerusers.md#from-a-request-to-a-result) shows this process from request to report.

The agent can complete several increments under your existing authorization before sending a report. It must combine unreported work into a report when the task is complete, when it hands unfinished work back to you or another person or agent, or when it seeks your input. It does not draft or send routine progress reports unless you request them or an applicable rule requires them. An earlier message is still required when a rule calls for one, such as the advance statement before an investigation described below.

A message and a request for approval serve different purposes. The agent pauses when the contract, your instructions, or the tool's rules require direction, including before substantially more work or investigation than expected. You can request status updates or [extra review checkpoints](README-powerusers.md#optional-controls-you-can-add) if you want to follow individual increments. [When the agent pauses or continues](README-powerusers.md#when-the-agent-pauses-or-continues) explains these distinctions in detail.

## What to expect

- **Focused progress.** The agent selects each step using your objective, relevant project evidence, and earlier findings. Unrelated cleanup and speculative features stay outside the task.
- **Complete work within each step.** Small scope still receives the necessary reasoning and validation. Affected code, tests, configuration, and documentation stay consistent. A required stop can leave a step unfinished; it cannot be reported as complete.
- **Decisions and consolidated results.** Consequential unresolved questions come to you. Reports identify completed work, checks, material assumptions, and unfinished work; one report can cover several increments.
- **Ordinary context gathering.** Reading relevant code, callers, tests, configuration, and directly related dependencies, along with existing project documentation, is part of normal work and needs no inquiry framing or inspection-by-inspection announcement. Running an agreed test or measurement also does not become an investigation merely because its result is not yet known.
- **Bounded investigations.** Sometimes the agent needs to investigate a material uncertainty about how to proceed before it can make the next decision. For example, it may need evidence to choose an approach that fits an agreed memory limit. This is an **inquiry**: before starting, the agent states its question and boundaries concisely in chat. That statement does not itself ask for approval. The inquiry ends when it has sufficient evidence or reaches its effort limit; outcomes join the normal report unless your input is needed sooner. Missing required evidence leaves work incomplete. Scope and effort-growth controls apply to ordinary work and inquiries alike. See the [investigation examples](README-powerusers.md#when-an-investigation-is-needed) for the distinction and the required framing.
- **Project knowledge that develops with the work.** Adoption includes architecture documentation organized around arc42, a set of topics for explaining a software system, along with clearly expressed requirements and records of significant decisions. These practices support quality and preserve knowledge for later steps. You can limit or defer proposed documentation improvements. Installation does not authorize a project-wide audit or rewrite.

This is an opinionated engineering baseline. Your instructions take priority within the tool's actual instruction hierarchy and permissions. You remain responsible for reviewing and accepting the work.

Instruction files cannot guarantee compliance. The tool's controls govern permissions and approvals.

## Get more from it

- **[Getting more from AGENTS.md](README-powerusers.md)** — practical examples, when the agent pauses, and existing-project alignment.
- **[The design of AGENTS.md](README-maintainers.md)** — design reasons, engineering choices, supporting references, constraints, and trade-offs that inform changes to the contract.
- **[AGENTS.md](AGENTS.md)** — the complete operating rules, conditions, and exceptions.

## Local evaluation suite

The local Python/Pydantic Evals suite runs Codex in temporary workspaces and combines automated checks with human review of selected contract behaviors. Results supply evidence about those cases, not general compliance. See the [case catalogue and interpretation limits](META-EVALUATIONS.md#cases-and-interpretation) and [evaluation setup, commands, and boundaries](META-EVALUATIONS.md).

## License

Licensed under [MIT No Attribution (MIT-0)](LICENSE).
