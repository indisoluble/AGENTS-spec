# AGENTS.md Specification

This repository hosts a reusable `AGENTS.md` for AI coding agents.

## What it defines

A repo-level contract for how agents should work inside a project, including:

- docs-first analysis,
- small, reviewable changes,
- explicit traceability,
- reuse before new files,
- engineering rules for clean, maintainable code.

## Scope

This repository only contains:

- `AGENTS.md` — the canonical specification
- `.github/copilot-instructions.md` — a minimal bridge pointing to it

## Intended use

Use it as a reference or starting point for repositories that want a repo-only, tool-agnostic agent contract.

## Documentation bootstrap

This `AGENTS.md` can bootstrap documentation in an existing project with implemented code but missing or weak docs, generating and refining the documentation one file at a time.

Example prompt:

`Align this repository with AGENTS.md and bootstrap the documentation for the existing codebase.`
