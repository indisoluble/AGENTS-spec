# AGENTS.md Specification

This repository provides a reusable instruction framework for making AI coding agents operate against explicit, version-controlled project rules.

It is intended for projects that use AI coding assistants such as GitHub Copilot, ChatGPT, Codex-style agents, or other IDE-integrated tools.

The purpose is to replace repeated, informal prompting with a repository-local development contract that is reviewable, maintainable, and portable across tools.

## 1. What this repository provides

This repository contains the files needed to add an agent-facing development contract to another repository:

- `AGENTS.md`
- `.github/copilot-instructions.md`

`AGENTS.md` is the canonical operating contract for coding agents. It defines how agents should inspect context, plan changes, modify code, update documentation, validate work, and preserve small, reviewable diffs.

`.github/copilot-instructions.md` is a GitHub Copilot compatibility bridge. It directs Copilot back to `AGENTS.md` so the project does not maintain a second, competing instruction source.

Together, these files make agent guidance part of the repository itself instead of leaving it in prompts, chat history, IDE state, or tool-specific configuration.

## 2. What a project gains from this

A destination project gains:

- a single, version-controlled source of truth for agent instructions;
- more consistent agent behavior across tools and sessions;
- clearer rules for code, documentation, testing, and validation;
- visible project guidance that can be reviewed through normal Git workflows;
- documentation bootstrap rules for projects with missing or incomplete documentation;
- reduced risk of instruction drift across prompts, tools, and contributors.

## 3. How to use it

Copy these files into the destination repository:

- `AGENTS.md`
- `.github/copilot-instructions.md`

Then review and adapt `AGENTS.md` to the target project’s architecture, workflow, documentation rules, coding standards, and review expectations.

A typical adoption flow is:

1. Copy `AGENTS.md` to the repository root.
2. Copy `.github/copilot-instructions.md` to `.github/copilot-instructions.md`.
3. Adapt `AGENTS.md` for the destination project.
4. Commit both files so the agent contract becomes part of the project history.

Once committed, coding agents can use these files as stable project context before proposing or applying changes.

## 4. Documentation bootstrap behavior

A destination project does not need complete documentation before adopting this setup.

If documentation is missing or insufficient, agents should bootstrap it incrementally according to the rules in `AGENTS.md`. This allows the same setup to work for new projects, existing projects with limited documentation, and mature projects whose documentation needs restructuring or normalization.

## 5. Portability and tool compatibility

This setup is designed for normal repository-based development workflows.

It is especially compatible with VS Code and GitHub Copilot, while remaining broadly portable across other IDEs, coding agents, and AI-assisted development tools.