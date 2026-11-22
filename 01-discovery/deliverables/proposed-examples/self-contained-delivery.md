# Proposed examples: self-contained delivery

All examples remain **proposed and unaccepted**. See [classifications and shared qualifications](../example-coverage.md#reading-a-proposed-example).

## PR1 — Self-contained operating contract

### PR1.1 — Check the delivered file against the full duty set

**Direct — proposed.**

- **Given** the delivered `AGENTS.md` and an inventory of all generic operating duties intended for that release, including all binding procedures as well as general behavioral duties.
- **When** a reviewer checks the delivered file without relying on the companion guides, provider bridge, or internal engineering docs to supply instructions.
- **Then** every operative duty, including its applicable trigger, force, and exceptions, can be recovered from the delivered file. The result establishes textual self-containment only, not provider loading or agent adherence.

### PR1.2 — Fail when a companion supplies missing policy

**Direct — proposed.**

- **Given** a mandatory consultation trigger is defined only in an internal guide or provider bridge, and the delivered file omits it or points elsewhere for the operative rule.
- **When** a reviewer checks the delivered file for self-containment.
- **Then** the file lacks a required operating instruction even if a provider loads both files and an agent could follow their combined instructions.

### PR1.3 — Allow loading aids and adopting-project facts

**Direct — proposed.**

- **Given** a provider bridge only locates and loads `AGENTS.md`, a guide explains a method without adding duties, and an adopting project supplies its own build commands and requirements.
- **When** a reviewer checks the delivered contract for generic operating duties.
- **Then** those external materials are compatible with self-containment if the contract contains all its operative instructions. Whether the provider successfully loads it is a separate check.
