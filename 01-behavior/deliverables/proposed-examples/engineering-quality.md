# Proposed examples: engineering quality

These examples cover engineering quality under BR9. All remain **proposed and unaccepted**; [classification definitions and shared qualifications](../discovery.md#formulation-questions-and-evidence-limits) govern their interpretation.

Return to [Discovery](../discovery.md) and its [coverage matrix](../discovery.md#requirement-to-scenario-coverage). [Historical qualification sources](../../docs/candidate-and-example-history.md#scenario-qualification-provenance) and [draft corrections](../../docs/candidate-and-example-history.md#changes-from-the-supplied-draft) retain their provenance.

## BR9 — Engineering quality and preservation

Requirement: [BR9](../baseline.md#br9--engineering-quality-and-preservation). Current qualification evidence: [design explanation](../../../02-design/deliverables/mechanisms/engineering-and-validation.md#component-boundaries-refactoring-and-validation), [contract](../../../03-contract/prerelease_AGENTS.md) §§1.2–1.3.

### BR9.1 — Refactor without changing observable behavior

**Direct — proposed.**

- **Given** a refactor is authorized and existing callers rely on an error response, a required log entry, and timely cleanup.
- **When** the agent changes the internal structure.
- **Then** those guarantees remain unchanged and relevant checks cover them. A changed error, missing required log entry, or skipped cleanup is not an acceptable side effect of the refactor.

### BR9.2 — Change behavior only as intended and authorized

**Direct — proposed.**

- **Given** the requester authorizes a specific change to a public error response but not to other errors or compatibility guarantees.
- **When** the agent implements the change.
- **Then** it changes only the intended behavior and updates the affected requirements, tests, and docs consistently. The authorization does not extend to changing other responses.

### BR9.3 — Do not build for a hypothetical need alone

**Direct — proposed.**

- **Given** a straightforward change meets the current requirement, and a proposed plug-in layer would serve only a hypothetical future extension.
- **When** the agent chooses an implementation.
- **Then** speculation alone does not justify the layer. Clarity, canonical ownership, and reversibility should guide the choice among workable solutions; fewer parts alone do not establish quality. Current requirements or evidence may justify complexity, subject to authorization.

### BR9.4 — Current requirements can justify complexity

**Direct — proposed.**

- **Given** an accepted hard memory constraint cannot be met by the existing whole-file approach, measured evidence supports streaming, and the requester has specifically authorized the necessary architectural choice.
- **When** the agent implements and validates that change.
- **Then** streaming complexity is justified by the current requirement and evidence, with material trade-offs explained and lasting rationale recorded. Other contracts and invariants remain preserved unless their changes are also intended and authorized; fewer lines would not excuse violating the memory constraint.

### BR9.5 — No textual caller is not proof of dead code

**Detail review — proposed.** The exact dead-code evidence test remains current design under the accepted focused-change and preservation outcomes.

- **Given** a cleanup adjacent to an authorized fix finds no textual calls to a handler, but dynamic registration may still reach it; removal of live functionality is not authorized.
- **When** the agent considers deleting the handler as dead code.
- **Then** the missing textual calls do not establish clear unreachability or direct obsolescence from the authorized change. It leaves the handler unless the required evidence and scope support removal; speculative cleanup is not added.
