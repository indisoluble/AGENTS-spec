# Proposed examples: self-contained delivery

All examples remain **proposed and unaccepted**. See [`01-discovery/deliverables/example-coverage.md` § Reading a proposed example](../example-coverage.md#reading-a-proposed-example).

This subject uses namespace `SD`. Its highest issued ID is `EX-SD-003`.

In these cases, `AGENTS.md` is the file of instructions delivered to a project. A provider bridge is a tool-specific file that directs a coding agent to those instructions. The reviewer asks what the agent could learn by reading the delivered file alone.

## EX-SD-001 — Check the delivered file against the full duty set

- **Given** the delivered `AGENTS.md` and an inventory of all generic operating duties intended for that release, including all binding procedures as well as general behavioral duties.
- **When** a reviewer checks the delivered file without relying on the companion guides, provider bridge, or internal engineering docs to supply instructions.
- **Then** every operative duty, including its applicable trigger, force, and exceptions, can be recovered from the delivered file. The result establishes textual self-containment only, not provider loading or agent adherence.

## EX-SD-002 — Fail when a companion supplies missing policy

- **Given** a mandatory consultation trigger is defined only in an internal guide or provider bridge, and the delivered file omits it or points elsewhere for the operative rule.
- **When** a reviewer checks the delivered file for self-containment.
- **Then** the file lacks a required operating instruction even if a provider loads both files and an agent could follow their combined instructions.

## EX-SD-003 — Allow loading aids and adopting-project facts

- **Given** a provider bridge only locates and loads `AGENTS.md`, a guide explains a method without adding duties, and an adopting project supplies its own build commands and requirements.
- **When** a reviewer checks the delivered contract for generic operating duties.
- **Then** those external materials are compatible with self-containment if the contract contains all its operative instructions. Whether the provider successfully loads it is a separate check.
