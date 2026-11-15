# Proposed examples: planning and scope

These examples cover planning and scope under BR1, BR2. All remain **proposed and unaccepted**; [classification definitions and shared qualifications](../discovery.md#formulation-questions-and-evidence-limits) govern their interpretation.

Return to [Discovery](../discovery.md) and its [coverage matrix](../discovery.md#requirement-to-scenario-coverage). [Historical qualification sources](../docs/candidate-and-example-history.md#scenario-qualification-provenance) and [draft corrections](../docs/candidate-and-example-history.md#changes-from-the-supplied-draft) retain their provenance.

## BR1 — Focused, proportionate, authorized work

Requirement: [BR1](../baseline.md#br1--focused-proportionate-authorized-work). Current qualification evidence: [design explanation](../../02-design/mechanisms/work-cycle-and-inquiry.md#small-commitments-with-sufficient-depth), [contract](../../03-contract/prerelease_AGENTS.md) §§1.1, 2.3, 2.5.

### BR1.1 — Fix the defect and its necessary dependents

**Direct — proposed.**

- **Given** the requester authorizes fixing a parser defect, a directly affected caller needs a matching change, and an adjacent file has unrelated formatting issues.
- **When** the agent plans and implements the fix.
- **Then** it includes the necessary caller change and relevant checks, leaves the unrelated formatting alone, and does not claim that a smaller patch excuses leaving the defect partly fixed.

### BR1.2 — Reassess before extending the work

**Direct — proposed.**

- **Given** a completed increment fixed one case and its regression check exposed a second case covered by the same requirement and authorization.
- **When** the agent considers another increment.
- **Then** it checks what has been done, what remains, the agreed direction and limits, and why the new evidence justifies the next step. If those conditions support continuing, it proceeds without a new approval checkpoint.

### BR1.3 — Explain a step that cannot stand alone before starting it

**Direct — proposed.**

- **Given** an authorized interface change has an intermediate step that cannot stand alone because a dependent adapter is still on the old interface, and tool permissions allow the work.
- **When** the agent is about to start that step.
- **Then** it explains why the step cannot stand alone, what will remain usable or testable, how to undo it, and material reversal limits. At review, handoff, or a deliberate pause after a meaningful step, it leaves a coherent state with the unfinished dependency identified. This does not require every intermediate edit to be independently complete or permit passing a required stop.

### BR1.4 — Stop at the end of the authorized task

**Direct — proposed.**

- **Given** the agent completed the requested fix and the relevant checks passed, and the agent spotted a useful but unrelated improvement.
- **When** it considers the improvement as a next increment.
- **Then** it reports the requested work complete and leaves the unrelated work untouched. It may propose the improvement, but completing the fix did not authorize it.

### BR1.5 — Honor a required stop with unfinished work

**Direct — proposed.**

- **Given** a requester checkpoint requires stopping after a meaningful migration step, and a dependent adapter remains unfinished as disclosed before the step.
- **When** the checkpoint is reached.
- **Then** the agent stops and leaves a coherent reviewable state, identifies what is usable or testable, explains recovery and material reversal limits, and hands off the unfinished dependency. It neither continues solely to claim completeness nor labels the overall migration complete.

### BR1.6 — Match planning depth to the next decision

**Direct — proposed.**

- **Given** a broad authorized task includes a consequential interface decision now and low-risk implementation details that cannot be settled until that decision is made.
- **When** the agent plans its next useful commitment.
- **Then** it investigates enough at the interface level to support that decision, includes necessary dependencies and checks, and keeps distant implementation detail at outline level. Small scope does not excuse omitting evidence needed for the decision or authorize unrelated planning.

## BR2 — Evidence-based planning and knowledge ownership

Requirement: [BR2](../baseline.md#br2--evidence-based-planning-and-knowledge-ownership). Current qualification evidence: [design explanation](../../02-design/mechanisms/knowledge-and-documentation.md#documentation-choices), [contract](../../03-contract/prerelease_AGENTS.md) §1.1.

### BR2.1 — Inspect what matters before choosing the fix

**Direct — proposed.**

- **Given** a failing import has a documented required outcome, an affected caller and test, and a setting that selects the import path.
- **When** the agent prepares its next step.
- **Then** it checks those sources before choosing a fix or refining the checks. It identifies the authorized objective and what would demonstrate success, and distinguishes the required result from its prediction about how the proposed fix will work.

### BR2.2 — A passing test does not settle what the product should do

**Direct — proposed.**

- **Given** the canonical requirement says to reject blank identifiers, while the current code and a passing test accept them.
- **When** the agent assesses the discrepancy.
- **Then** it reports the conflict and treats the requirement as evidence of intended behavior and the code and test as evidence of current behavior. It does not silently change the requirement to match the implementation.

### BR2.3 — Ask when the sources cannot settle a consequential choice

**Direct — proposed.**

- **Given** two applicable, authoritative requirements prescribe incompatible handling of the same customer data and their ownership does not resolve the conflict.
- **When** the next implementation choice depends on which one applies.
- **Then** the agent reports the conflict, separates confirmed facts from assumptions, and seeks direction before making the dependent choice.

### BR2.4 — Use instruction files for conduct, not proof of project facts

**Detail review — proposed.** The exact artifact-role assignment is current design; the accepted outcome is evidence ownership without invented precedence.

- **Given** an instruction file mentions an old package command as background, authoritative package configuration declares the current command, and no requester instruction requires using the old command.
- **When** the agent establishes the project command before planning a check.
- **Then** it uses the configuration as the owner of that fact and reports the discrepancy. It continues to follow applicable conduct instructions; it does not invent a universal ranking that makes instructions, code, or tests authoritative for every kind of knowledge.
