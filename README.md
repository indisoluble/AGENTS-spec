# AGENTS.md Specification

This repository provides a reusable instruction framework for making AI coding agents operate against explicit, version-controlled project rules.

It is intended for projects that use AI coding assistants such as GitHub Copilot, ChatGPT, Codex-style agents, or other IDE-integrated tools.

The purpose is to replace repeated, informal prompting with a repository-local development contract that is reviewable, maintainable, portable across tools, and optimized for agent consumption.

## 1. What this repository provides

This repository contains 2 contract files:

- `AGENTS.md`
- `.github/copilot-instructions.md`

`AGENTS.md` is the canonical operating contract for coding agents. It defines how agents should inspect context, classify tasks, plan changes, modify code, update documentation, validate work, and deliver coherent, reviewable changes whose decision basis and documentation status are traceable.

`.github/copilot-instructions.md` is a GitHub Copilot compatibility bridge. It points Copilot-compatible surfaces back to the repository-root `AGENTS.md` so the project does not maintain a second, competing instruction source.

## 2. Intended use and customization

`AGENTS.md` is a drop-in canonical baseline for repository-local agent behavior.

It is intended to be copied into a repository as-is and treated as the repository's agent contract. `AGENTS.md` guides agent behavior; it does not replace project-specific documentation, executable behavior, tests, configuration, or human review.

Most repositories should not edit `AGENTS.md` during normal adoption. Instead, keep `AGENTS.md` generic and put project-specific facts in focused repository documentation.

For documentation placement, baseline documents, and specialized documents, use the documentation map and placement rules defined in `AGENTS.md`.

Edit `AGENTS.md` directly only when the repository needs to change agent behavior or repository-wide agent policy.

## 3. How to use it

Copy these files into the destination repository:

- `AGENTS.md`
- `.github/copilot-instructions.md`

Then commit both files so the agent contract becomes part of the project history.

No direct edits to `AGENTS.md` are required for normal adoption.

## 4. What changes after adding `AGENTS.md`

Adding `AGENTS.md` gives coding agents an explicit repository-local operating contract.

After adding it, agents should be expected to:

- classify tasks as trivial or non-trivial;
- inspect relevant repository context before non-trivial work;
- plan proportionally before non-trivial edits;
- when Plan mode or an equivalent review-before-implementation workflow is active, present non-trivial outcomes as ordered reviewable increments and implement only the selected increment;
- keep changes small, coherent, reviewable, and behaviorally complete;
- make each coherent change traceable to its decision basis and documentation status;
- preserve Single Source of Truth across code and documentation;
- avoid unrelated refactors, formatting churn, dependency upgrades, file moves, and cleanup;
- preserve protected contract files unless explicitly asked to change them;
- keep code, tests, configuration, and documentation synchronized;
- update relevant documentation when behavior, interfaces, architecture, configuration, operations, workflow, or constraints change;
- prefer tests that both verify behavior and communicate expected behavior;
- disclose material assumptions, conflicts, missing context, risks, validation status, and unresolved follow-up items.

## 5. Tool-specific instruction files

`AGENTS.md` is the canonical source for repository-wide agent behavior.

Tool-specific instruction files should be thin compatibility bridges or narrow adapters. They should not duplicate, redefine, or drift from the repository-wide policy in `AGENTS.md`.

This repository includes `.github/copilot-instructions.md` as a GitHub Copilot bridge. When adding support for another tool, prefer a small bridge file that refers to `AGENTS.md` rather than copying the full contract.

This keeps `AGENTS.md` as the single source of truth while allowing tool-specific instruction discovery.

## 6. Tool-specific modes and approvals

Some tools provide explicit planning modes, approval modes, autonomous modes, hooks, custom agents, skills, or other workflow mechanisms.

`AGENTS.md` does not require a specific product mode. Its ordinary planning rules mean that agents should choose an appropriate implementation approach before non-trivial edits. When a user invokes Plan mode, or the current workflow provides an equivalent review-before-implementation stage, non-trivial outcomes must be presented as ordered reviewable increments before implementation; once edits are permitted, only the selected increment is implemented.

Tool approval prompts, sandbox limits, file-edit confirmations, terminal confirmations, and security boundaries are controlled by the current tool or environment. `AGENTS.md` does not override them.

## 7. Documentation bootstrap behavior

A destination project does not need complete documentation before adopting this setup.

If documentation is missing or insufficient, agents should bootstrap it incrementally according to the rules in `AGENTS.md`. This allows the same setup to work for new projects, existing projects with limited documentation, and mature projects whose documentation needs restructuring or normalization.

## 8. Tool compatibility

Different coding agents discover and apply repository instructions differently. Some tools can read `AGENTS.md` directly. Others use tool-specific instruction files, settings, chat modes, skills, hooks, or configuration.

This repository is designed around a conservative rule:

- keep repository-wide agent behavior in `AGENTS.md`;
- keep tool-specific bridges small;
- avoid duplicating policy across instruction files;
- preserve the intent of `AGENTS.md` when a tool cannot apply every instruction uniformly.

When instruction application is uncertain, use the current tool's diagnostics or ask the agent to state which repository instruction sources it used before starting non-trivial work.
