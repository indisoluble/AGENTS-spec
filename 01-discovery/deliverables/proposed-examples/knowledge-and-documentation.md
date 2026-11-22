# Proposed examples: knowledge and documentation

All examples remain **proposed and unaccepted**. See [how to read a proposed example](../example-coverage.md#reading-a-proposed-example).

This subject uses namespace `KD`. Its highest issued ID is `EX-KD-011`.

## Recording findings and decisions

In these cases the canonical owner is the project source maintained for a particular fact. An architecture decision record (ADR) preserves the reasons for a lasting choice.

### EX-KD-001 — Record a lasting finding where it belongs

- **Given** an authorized investigation establishes a material, lasting compatibility constraint with evidence, even though the tested approach was discarded; an in-scope permanent record is writable under requester and tool permissions.
- **When** the agent preserves that finding.
- **Then** it records the fact and substantiating evidence at the canonical owner, creating only a minimal record if no suitable owner exists. It does not create an independently maintained competing owner or an ADR solely because a finding exists. A temporary test outage useful only for this attempt follows reporting rules, not the durable-finding duty.

### EX-KD-002 — Record a proposal without accepting it

- **Given** a significant architectural proposal is ready for review and the agent is authorized to prepare the record, but not to decide the proposal.
- **When** it records the proposal.
- **Then** the record identifies it as proposed and preserves the evidence, constraints, reasons, trade-offs, and material alternatives. Writing the record does not accept or authorize implementing the decision.

### EX-KD-003 — Optional debt recording does not authorize a fix

- **Given** a review uncovers a current, task-relevant implementation compromise evidenced to increase maintenance cost, and a separate feature intentionally deferred; accepted requirements and trade-offs are available and record writes are permitted.
- **When** the agent considers whether to record technical debt.
- **Then** it considers those accepted requirements and trade-offs and may record the evidenced compromise as debt. If it does, it flags any classification uncertainty and reports what was recorded, why, and where. Deferral alone does not make the feature debt, and recording does not authorize repair. Independently, a finding that is both material and durable must be recorded with its supporting evidence even if the agent does not choose a debt classification.

### EX-KD-004 — Keep review-only edits inside the narrow permission

- **Given** a review-only request does not prohibit edits, actual tool permissions allow them, and an existing guide in the reviewed scope lists an outdated command contradicted by its canonical owner.
- **When** the agent considers a documentation write under the assessment-only permission.
- **Then** it may correct the verified description. In-scope material durable findings and significant proposals retain their respective record duties; debt entries retain their optional status and conditional duties. The factual-correction permission excludes requirements, decision records, and protected instruction files. Review alone does not authorize implementation, changing requirements, accepting or changing decisions beyond existing authority, unrelated repairs, backfill, or protected instruction-file edits.

Compare the proposed treatment of a [lasting finding](#ex-kd-001--record-a-lasting-finding-where-it-belongs), a [decision awaiting review](#ex-kd-002--record-a-proposal-without-accepting-it), and a [possible debt entry](#ex-kd-003--optional-debt-recording-does-not-authorize-a-fix).

### EX-KD-005 — Report an unmet record duty when edits are prohibited

- **Given** the requester explicitly says not to edit files, and the review identifies a material finding that belongs in a permanent project record.
- **When** the agent reports the review.
- **Then** it leaves files untouched and reports the finding, its evidence, and the missing record as unfinished work.

### EX-KD-006 — Preserve decision history when an authorized choice changes

- **Given** the requester has accepted a replacement for a significant compatibility decision and authorized its implementation; the earlier record includes evidence, an influential failed alternative, and consequences still useful to maintainers.
- **When** the agent updates the decision history within its write authority.
- **Then** it distinguishes the superseded decision from its accepted replacement, preserves the material reasons, evidence, consequences, and useful alternatives, and links the replacement. It does not erase history or infer acceptance from implementation status.

### EX-KD-007 — Update recorded debt when authorized work resolves it

- **Given** an existing debt entry describes a compromise that the current authorized fix resolves, and updating its record is permitted.
- **When** the agent completes the fix and affected documentation.
- **Then** it updates the affected debt record and reports the change, preserving any still-relevant uncertainty. The optional choice to create a debt entry does not make maintenance of an affected existing entry optional or authorize additional repairs.

## Keeping project documentation current

### EX-KD-008 — Separate lasting behavior from task-only checks

- **Given** authorized work establishes that exports must always include a header, and the requester also asks to run one demonstration with a sample file.
- **When** the agent updates project requirements.
- **Then** it records the lasting behavior in verifiable terms at its canonical owner. It treats the sample run as a task check, not a new product requirement, and does not duplicate an existing canonical requirement.

### EX-KD-009 — Update known direct dependents without widening the audit

- **Given** an authorized change renames an option; its canonical reference and a known tutorial directly depend on the old name, whether linked or already read or not, while a known index only links to the reference.
- **When** the agent updates the affected documentation.
- **Then** it updates the reference and tutorial and checks the index, editing it only if affected. That synchronization duty does not authorize searching for unknown dependents, a repository-wide audit, or unrelated reorganization. Broader checks may be proposed.

### EX-KD-010 — Report gaps outside the authorized work

- **Given** the agent finds an outdated setup guide for an unrelated service while editing docs for an authorized change.
- **When** it resolves the affected in-scope docs.
- **Then** it leaves the unrelated guide untouched and reports or proposes the separate repair. If the task is review-only, any edits must also fit the narrow permission illustrated in [EX-KD-004](#ex-kd-004--keep-review-only-edits-inside-the-narrow-permission).

### EX-KD-011 — A documentation gap does not require a new guide

The recommendation under discussion is to fill known documentation gaps when the requester allows the necessary edits.

- **Given** an in-scope review finds a known architecture coverage gap, the requester postpones that improvement, and no need for a new tutorial has been requested or agreed.
- **When** the agent reports the gap and maintains the authorized documentation.
- **Then** it identifies the missing coverage as a proposed improvement and keeps the gap and agreed deferral visible. It respects the deferral, does not create a tutorial merely to fill a documentation category, and adds no empty sections or invented facts. In-scope improvements retain their qualified recommendation and actual editing-authority limits.
