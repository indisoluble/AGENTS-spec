# Proposed examples: bounded inquiry

These examples cover bounded inquiry under BR4. All remain **proposed and unaccepted**; [classification definitions and shared qualifications](../discovery.md#formulation-questions-and-evidence-limits) govern their interpretation.

Return to [Discovery](../discovery.md) and its [coverage matrix](../discovery.md#requirement-to-scenario-coverage). [Historical qualification sources](../../docs/candidate-and-example-history.md#scenario-qualification-provenance) and [draft corrections](../../docs/candidate-and-example-history.md#changes-from-the-supplied-draft) retain their provenance.

## BR4 — Bounded investigation and timely reassessment

Requirement: [BR4](../baseline.md#br4--bounded-investigation-and-timely-reassessment). Current qualification evidence: [design explanation](../../../02-design/deliverables/mechanisms/work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation), [contract](../../../03-contract/prerelease_AGENTS.md) §2.4; §§1.1, 2.3.

### BR4.1 — Tell the requester what is blocking progress

**Direct — proposed.**

- **Given** reading the relevant code and docs leaves a material uncertainty about whether a retry can create a duplicate charge, and the requester has not already been told.
- **When** that uncertainty blocks the choice of fix.
- **Then** the agent promptly explains the uncertainty and why it matters, and may start a narrow investigation that is already authorized. It does not ask for approval solely because it announced the investigation.

### BR4.2 — Stop when there is enough evidence

**Direct — proposed.**

- **Given** a bounded, authorized check shows whether the retry reuses the same transaction identifier, which answers the question that blocked the decision.
- **When** that evidence is sufficient to choose the next authorized step.
- **Then** the agent ends the inquiry. At completion, handoff, or when asking for input, it reports the conclusion, supporting evidence, and any material uncertainty that remains.

### BR4.3 — Review an inconclusive step before doing more

**Direct — proposed.**

- **Given** an authorized bounded local reproduction has finished without enough evidence to answer the blocking question.
- **When** the agent considers further investigation.
- **Then** it reassesses what the preceding step taught it before deciding whether another bounded step is justified. It may continue only on that evidence within existing authorization and requester limits; the unfinished answer alone is not justification. If the useful next step requires access outside that authority, it reports the missing evidence and asks before accessing it. No default numerical budget, newly announced allowance, or automatic approval checkpoint follows from the inconclusive result.

### BR4.4 — Ordinary checking does not require an inquiry notice

**Detail review — proposed.** The detailed context/validation exclusion is current design, beyond the broad accepted inquiry outcome.

- **Given** the next action is to read the affected module or run an ordinary regression check, and no material uncertainty about how to proceed blocks the next decision.
- **When** the agent does that work within authorization.
- **Then** it treats the actions as context gathering and validation respectively. Not knowing the check result does not itself require a separate inquiry notice. A useful update is still permitted under the communication rules.

### BR4.5 — A notice already given need not be repeated

**Direct — proposed.**

- **Given** the requester already identified the blocking uncertainty and why it matters, and authorized a narrow investigation.
- **When** the agent starts that investigation.
- **Then** it need not send a second notice about the same uncertainty. The work still stays within the authorized bounds.

### BR4.6 — A prescribed procedure can still be inquiry

**Detail review — proposed.** The purpose-based classification of this prescribed procedure needs review as a defining product example, not as a change to current §2.4.

- **Given** context gathering leaves a material uncertainty about which storage approach is viable, a documented benchmark can resolve it, the bounded benchmark is authorized, and the uncertainty has not been communicated.
- **When** the agent uses that benchmark to choose how to proceed.
- **Then** it promptly explains the uncertainty and its significance and conducts a bounded inquiry subject to evidence sufficiency and reassessment. Being a documented procedure does not exempt it. Running the same benchmark solely to validate a settled limit would not be inquiry merely because its output is unknown.

### BR4.7 — Reading existing project documents remains context gathering

**Detail review — proposed.** The blanket exclusion for reading existing project documents is precise current design, not independently spelled out in the acceptance summary.

- **Given** a material question blocks the next decision and an existing project architecture record may answer it; reading that record is within scope.
- **When** the agent reads that record and directly relevant project documentation.
- **Then** the reading remains context gathering, even for that blocking question, without an inspection-by-inspection inquiry notice. Authorization, proportionate effort, and cumulative reassessment still apply. This does not exempt subsequent empirical inquiry or required decision disclosures.

### BR4.8 — An unanswered question is not evidence for another attempt

**Direct — proposed.**

- **Given** a bounded inquiry ends inconclusively, its findings justify no further useful authorized step, and the next decision still depends on the missing evidence.
- **When** the agent reassesses the result.
- **Then** it reports the missing evidence, uncertainty, unfinished work, and available alternatives and seeks direction. It does not repeat attempts solely because the question is unanswered or claim that reaching the step boundary satisfied the objective.
