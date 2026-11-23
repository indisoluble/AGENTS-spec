# Proposed examples: engineering quality

All examples remain **proposed and unaccepted**. See [`01-discovery/deliverables/example-coverage.md` § Reading a proposed example](../example-coverage.md#reading-a-proposed-example).

This subject uses namespace `EQ`. Its highest issued ID is `EX-EQ-005`.

## EX-EQ-001 — Refactor without changing observable behavior

- **Given** a refactor is authorized and existing callers rely on an error response, a required log entry, and timely cleanup.
- **When** the agent changes the internal structure.
- **Then** those guarantees remain unchanged and relevant checks cover them. A changed error, missing required log entry, or skipped cleanup is not an acceptable side effect of the refactor.

## EX-EQ-002 — Change behavior only as intended and authorized

- **Given** the requester authorizes a specific change to a public error response but not to other errors or compatibility guarantees.
- **When** the agent implements the change.
- **Then** it changes only the intended behavior and updates the affected requirements, tests, and docs consistently. The authorization does not extend to changing other responses.

## EX-EQ-003 — Do not build for a hypothetical need alone

- **Given** a straightforward change meets the current requirement, and a proposed plug-in layer would serve only a hypothetical future extension.
- **When** the agent chooses an implementation.
- **Then** speculation alone does not justify the layer. Clarity, canonical ownership, and reversibility should guide the choice among workable solutions; fewer parts alone do not establish quality. Current requirements or evidence may justify complexity, subject to authorization.

## EX-EQ-004 — Current requirements can justify complexity

- **Given** an accepted hard memory constraint cannot be met by the existing whole-file approach, measured evidence supports streaming, and the requester has specifically authorized the necessary architectural choice.
- **When** the agent implements and validates that change.
- **Then** streaming complexity is justified by the current requirement and evidence, with material trade-offs explained and lasting rationale recorded. Other contracts and invariants remain preserved unless their changes are also intended and authorized; fewer lines would not excuse violating the memory constraint.

## EX-EQ-005 — No textual caller is not proof of dead code

- **Given** a cleanup adjacent to an authorized fix finds no textual calls to a handler, but dynamic registration may still reach it; removal of live functionality is not authorized.
- **When** the agent considers deleting the handler as dead code.
- **Then** the missing textual calls do not establish clear unreachability or direct obsolescence from the authorized change. It leaves the handler unless the required evidence and scope support removal; speculative cleanup is not added.
