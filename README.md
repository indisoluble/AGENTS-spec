# AGENTS.md Specification

## 1. What this repository is
This repository provides the agent-facing files used to establish a repo-local development contract in another repository.

## 2. What problem it solves
It keeps agent behavior and project rules inside the destination repository so they remain reviewable, versioned, and portable across tools and IDEs.

## 3. What this repository contains
This repository contains `AGENTS.md`, `.github/copilot-instructions.md`, and `README.md`.

## 4. What gets copied to the destination repository
The files intended for reuse in the destination repository are `AGENTS.md` and `.github/copilot-instructions.md`.

## 5. How to use it
Copy the two agent-facing files into the destination repository, preserve their metadata, and use them as-is or adapt them to the target project as needed.

## 6. Canonical source of truth
`AGENTS.md` is the canonical agent contract, and `.github/copilot-instructions.md` is a minimal compatibility bridge.

## 7. Bootstrap behavior when documentation is missing
No documentation is required in advance; if documentation is missing or insufficient, agents should bootstrap it incrementally according to `AGENTS.md`.

## 8. Portability and tool compatibility
This setup is designed to work with normal development workflows, remain especially compatible with VS Code and GitHub Copilot, and stay broadly portable across other IDEs and coding agents.