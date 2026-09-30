# AGENTS.md Specification

A ready-made [AGENTS.md](AGENTS.md) for working with coding agents in new or established projects. Give your agent standing instructions for planning, implementation, validation, and documentation, so you can spend less time repeating how you want work handled.

Describe the outcome you want. From that request, the agent plans the next **small, complete step**, performs it, studies the result, and uses what it learns to decide what follows. This repeating Plan–Do–Study–Act (PDSA) workflow aims to keep effort manageable while giving each step the reasoning and validation it needs.

## Get started

1. **Copy [AGENTS.md](AGENTS.md) into your repository root.** If you already have instruction files, first preserve useful project facts found only there—such as build commands or system constraints—in appropriate project documentation. Check that those facts are still accurate before replacing the old files.
2. **Add the bridge for your tool, if applicable.** Use the supplied files at the paths below, replacing existing copies after preserving their useful project facts.

   | Tool | Files to use |
   | --- | --- |
   | Codex | Root `AGENTS.md` |
   | Claude Code | Root `AGENTS.md` and [CLAUDE.md](CLAUDE.md) |
   | GitHub Copilot | Root `AGENTS.md` and [.github/copilot-instructions.md](.github/copilot-instructions.md) |

3. **Keep the files in version control and check adoption.** In your tool, ask which repository instructions it loaded and check available instruction diagnostics. Then try a representative task: finding a file alone does not show that the agent follows it.

The supplied contract normally needs no project-specific customization. Keep project facts, build commands, and architecture in your project's documentation and code. Bridge files direct the tool to the contract.

Loading depends on the interface and settings. For verification, troubleshooting, and use with ChatGPT or Claude Projects, see [tool compatibility](README-powerusers.md#tool-compatibility).

## Try a first task

Ask for the result you need, as you normally would. For example:

> Fix the incorrect setup command in the README.

The agent is responsible for inspecting the relevant context, making the correction, checking it, and reporting the result. Those steps are already part of its standing instructions.

You can also give it a larger objective:

> Add CSV imports that report invalid rows and continue processing valid rows.

During Plan, the agent considers your overall objective and project context, chooses the next small, useful increment, and establishes its acceptance conditions. Later work stays at outline level. Results from Do and Study inform Act and the next Plan, so findings can reshape the approach as work progresses. The agent asks about consequential gaps, validates authorized work, and reports progress. You do not need to prescribe the steps or repeat the workflow.

Further increments can proceed under existing authorization. The agent pauses when the contract, your instructions, or the tool's rules require direction—for example, before taking on unexpectedly greater work. A pause after every increment is optional; you can request [additional review checkpoints](README-powerusers.md#optional-controls-you-can-add).

## What to expect

- **Focused progress.** Planning and learning stay connected: the agent chooses the next useful step in light of your objective and what earlier work established.
- **Coherent results.** Affected tests and documentation stay consistent with changes. Unrelated cleanup and speculative features stay outside the task.
- **Visible decisions.** The agent brings consequential unresolved questions to you and reports checks, assumptions, and unfinished work.
- **Project knowledge that develops with the work.** Adoption includes architecture documentation aligned with arc42, clearly expressed requirements, and records of significant decisions. You can limit or defer proposed documentation improvements. Installing the contract does not authorize a project-wide audit or rewrite.

This is an opinionated engineering baseline. Your instructions take priority within the tool's actual instruction hierarchy and permissions. You remain responsible for reviewing and accepting the work.

Effort control is best effort: the contract provides no token meter, hard quota, or guarantee of savings. Instruction files also cannot guarantee compliance; the tool's own controls still govern permissions and approvals.

## Get more from it

- **[Getting more from AGENTS.md](README-powerusers.md)** — fuller explanations, practical examples, existing-project alignment, and continuing unfinished work. No technical background is required to follow the collaboration guidance.
- **[The design of AGENTS.md](README-maintainers.md)** — its attributes, engineering choices, principles, and trade-offs.
- **[AGENTS.md](AGENTS.md)** — the complete operating rules, conditions, and exceptions.
