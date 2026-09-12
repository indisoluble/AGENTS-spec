# AGENTS.md Specification

This repository provides a reusable instruction framework for making AI coding agents operate against explicit, version-controlled project rules.

It is intended for projects that use AI coding assistants such as GitHub Copilot, Claude Code, ChatGPT, Codex-style agents, or other IDE-integrated tools.

The purpose is to replace repeated, informal prompting with a repository-local development contract that is reviewable, maintainable, portable across tools, and optimized for agent consumption.

## 1. What this repository provides

This repository contains one canonical contract and two compatibility bridges:

- `AGENTS.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`

`AGENTS.md` is the canonical operating contract for coding agents. It defines how agents should inspect context, classify tasks, plan changes, modify code, update documentation, validate work, and deliver coherent, reviewable changes whose decision basis and documentation status are traceable.

`CLAUDE.md` is a Claude Code compatibility bridge. Its native `@AGENTS.md` import loads the canonical contract without duplicating it.

`.github/copilot-instructions.md` is a GitHub Copilot compatibility bridge. It points Copilot-compatible surfaces back to the repository-root `AGENTS.md` so the project does not maintain a second, competing instruction source.

## 2. Intended use and customization

`AGENTS.md` is a drop-in canonical baseline for repository-local agent behavior.

It is intended to be copied into a repository as-is and treated as the repository's agent contract. `AGENTS.md` guides agent behavior; it does not replace project-specific documentation, executable behavior, tests, configuration, or human review.

Most repositories should not edit `AGENTS.md` during normal adoption. Instead, keep `AGENTS.md` generic and put project-specific facts in focused repository documentation.

For documentation progression, role ownership, and placement, use the documentation rules defined in `AGENTS.md`.

Edit `AGENTS.md` directly only when the repository needs to change agent behavior or repository-wide agent policy.

## 3. How to use it

Copy these files into the destination repository:

- `AGENTS.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`

Then commit all three files so the agent contract becomes part of the project history.

No direct edits to `AGENTS.md` are required for normal adoption.

## 4. What changes after adding `AGENTS.md`

`AGENTS.md` encourages a consistent way of working:

- **Understand before acting.** Read relevant project context and plan in proportion to the task.
- **Respect the requested scope.** Distinguish analysis from implementation, avoid unrelated changes, and respect protected files and review checkpoints.
- **Deliver reviewable changes.** Keep changes small and complete; use selected increments when a review-before-implementation workflow is active.
- **Keep project knowledge consistent.** Synchronize code, tests, configuration, and documentation written for people, with one authoritative owner for each shared fact or rule.
- **Explain decisions.** Connect changes to project requirements, established decisions, and documented trade-offs.
- **Verify and report.** Run relevant checks, favor tests that explain behavior, and disclose results, material uncertainties, risks, and remaining work.

This overview is not exhaustive. [`AGENTS.md`](AGENTS.md) defines the full rules and exceptions. The [contract organization](#5-contract-organization) and [portability budget](#8-cross-tool-portability-budget) guide future contract updates.

## 5. Contract organization

Tool-specific files provide discovery or imports for the canonical `AGENTS.md` contract. When adding support for another tool, use a thin bridge or narrow adapter following the contract's rules for tool-specific files.

Some repetition inside `AGENTS.md` is intentional: a rule may recur where an agent must apply it, keeping its conditions visible without relying entirely on cross-references. Shorter wording is not assumed to provide equivalent guidance. Repository-wide agent instructions, conditions, exceptions, illustrative examples, and decision-relevant rationale remain together in `AGENTS.md`; explanations useful only to human developers maintaining the contract belong in this README.

## 6. Tool-specific modes and approvals

Some tools provide explicit planning modes, approval modes, autonomous modes, hooks, custom agents, skills, or other workflow mechanisms.

`AGENTS.md` does not require a specific product mode. Its ordinary planning rules mean that agents should choose an appropriate implementation approach before non-trivial edits. When a user invokes Plan mode, or the current workflow provides an equivalent review-before-implementation stage, non-trivial outcomes must be presented as ordered reviewable increments before implementation; once edits are permitted, only the selected increment is implemented.

Analysis or review alone does not authorize repository edits. For requested changes that cannot be applied in the current environment, agents provide exact proposed edits or a focused patch. Documentation work governed by the contract's bootstrap and reorganization workflow also retains its human review checkpoint unless continuation was explicitly authorized.

A selected increment's execution brief can also be used with sustained execution tools such as [Codex Goal mode](https://learn.chatgpt.com/use-cases/follow-goals). It states the outcome, scope, prerequisites, required artifacts, acceptance checks, and review or stop conditions. The agent should carry that increment through implementation, validation, and scoped corrections, reporting completion only after verifying every acceptance criterion. Existing review checkpoints still apply, and unselected increments remain outside the run's scope.

Tool approval prompts, sandbox limits, file-edit confirmations, terminal confirmations, and security boundaries are controlled by the current tool or environment. `AGENTS.md` does not override them.

## 7. Documentation bootstrap and reorganization

A destination project does not need complete documentation before adopting this setup.

When documentation is insufficient, misplaced, or wrongly layered, agents use the bootstrap and reorganization workflow in `AGENTS.md`. They establish or reorganize the smallest useful human entry path and canonical owners using the repository's names and structure.

Existing documentation is moved or refactored one document per reviewable step, with affected references repaired in that step. Creation or substantial refactoring is followed by human review unless continuation was explicitly authorized. Work covers affected documents and direct references unless repository-wide work is requested. The full workflow and ownership rules remain in `AGENTS.md`.

## 8. Cross-tool portability budget

`AGENTS.md` is intentionally concise and tool-neutral for use across multiple commercial coding-agent products rather than optimized for a single vendor.

The maintained portability targets are:

- fewer than 200 lines, adapting [Claude Code's recommendation that each `CLAUDE.md` target under 200 lines](https://code.claude.com/docs/en/memory#write-effective-instructions) to the imported contract;
- fewer than 24 KB (24,000 UTF-8 bytes), a conservative project budget below [Codex's default 32 KiB aggregate project-instruction limit](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

The 24 KB target is not a documented Claude Code limit. These are documentation-only maintenance targets, not requirements of the `AGENTS.md` format or universal compatibility guarantees. They are maintained through review rather than automated enforcement. Current vendor documentation remains authoritative because tools may change how they discover, combine, limit, and apply repository instructions.

## 9. Tool compatibility

Instruction loading, setup, and limits depend on the product and interface. Consult the provider's current documentation:

| Provider | Official guidance |
|---|---|
| OpenAI | [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [ChatGPT projects](https://learn.chatgpt.com/docs/projects) |
| Anthropic | [Claude Code](https://code.claude.com/docs/en/memory#agentsmd) · [Claude projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects) |
| GitHub | [Copilot support](https://docs.github.com/en/copilot/reference/custom-instructions-support) |

When instruction application is uncertain, use the current tool's diagnostics or ask the agent to state which repository instruction sources it used before starting non-trivial work.