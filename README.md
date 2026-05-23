# AGENTS.md Specification

This repository provides a reusable instruction framework for making AI coding agents operate against explicit, version-controlled project rules.

It is intended for projects that use AI coding assistants such as GitHub Copilot, ChatGPT, Codex-style agents, or other IDE-integrated tools.

The purpose is to replace repeated, informal prompting with a repository-local development contract that is reviewable, maintainable, and portable across tools.

## 1. What this repository provides

This repository contains 2 files:

- `AGENTS.md`
- `.github/copilot-instructions.md`

`AGENTS.md` is the canonical operating contract for coding agents. It defines how agents should inspect context, plan changes, modify code, update documentation, check work, and preserve small, reviewable diffs.

`.github/copilot-instructions.md` is a GitHub Copilot compatibility bridge. It points Copilot back to `AGENTS.md` so the project does not maintain a second, competing instruction source.

## 2. Intended use and customization

`AGENTS.md` is a drop-in canonical baseline for repository-local agent behavior.

It is intended to be copied into a repository as-is and treated as the repository's agent contract. `AGENTS.md` guides agent behavior; it does not replace project-specific documentation or guarantee identical behavior across all tools, IDEs, models, or sessions.

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

- inspect relevant repository context before non-trivial work;
- plan before making non-trivial changes;
- keep changes small, coherent, and reviewable;
- avoid unrelated refactors, formatting churn, dependency upgrades, file moves, and cleanup;
- preserve protected contract files unless explicitly asked to change them;
- keep code, tests, configuration, and documentation synchronized;
- update relevant documentation when behavior, interfaces, architecture, configuration, operations, workflow, or constraints change;
- prefer tests that both verify behavior and communicate expected behavior;
- disclose material assumptions, conflicts, missing context, risks, and unresolved follow-up items.

## 5. Documentation bootstrap behavior

A destination project does not need complete documentation before adopting this setup.

If documentation is missing or insufficient, agents should bootstrap it incrementally according to the rules in `AGENTS.md`. This allows the same setup to work for new projects, existing projects with limited documentation, and mature projects whose documentation needs restructuring or normalization.

## 6. Tool compatibility

`AGENTS.md` is the canonical agent contract for the repository, but different coding agents discover and apply repository instructions differently. Some tools can read `AGENTS.md` directly. Others use tool-specific instruction files or configuration.

This repository includes `.github/copilot-instructions.md` as a GitHub Copilot bridge. When adding support for another tool, prefer a small bridge file that refers to `AGENTS.md` rather than duplicating the contract.

This keeps `AGENTS.md` as the single source of truth while allowing tool-specific instruction discovery.