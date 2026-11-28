# Proposed examples: bounded inquiry

All examples remain **proposed and unaccepted**. See [`01-discovery/deliverables/example-coverage.md` § Reading a proposed example](../example-coverage.md#reading-a-proposed-example).

This subject uses namespace `BI`. Its highest issued ID is `EX-BI-008`.

## EX-BI-001 — Tell the requester what is blocking progress

- **Given** reading the relevant code and docs leaves a material uncertainty about whether a retry can create a duplicate charge, and the requester has not already been told.
- **When** that uncertainty blocks the choice of fix.
- **Then** the agent promptly explains the uncertainty and why it matters, and may start a narrow investigation that is already authorized. It does not ask for approval solely because it announced the investigation.

## EX-BI-002 — Stop when there is enough evidence

- **Given** a bounded, authorized check shows whether the retry reuses the same transaction identifier, which answers the question that blocked the decision.
- **When** that evidence is sufficient to choose the next authorized step.
- **Then** the agent ends the inquiry. At completion, handoff, or when asking for input, it reports the conclusion, supporting evidence, and any material uncertainty that remains.

## EX-BI-003 — Review an inconclusive step before doing more

- **Given** an authorized bounded local reproduction has finished without enough evidence to answer the blocking question.
- **When** the agent considers further investigation.
- **Then** it reassesses what the preceding step taught it before deciding whether another bounded step is justified. It may continue only on that evidence within existing authorization and requester limits; the unfinished answer alone is not justification. If the useful next step requires access outside that authority, it reports the missing evidence and asks before accessing it. No default numerical budget, newly announced allowance, or automatic approval checkpoint follows from the inconclusive result.

## EX-BI-004 — Ordinary checking does not require an inquiry notice

- **Given** the next action is to read the affected module or run an ordinary regression check, and no material uncertainty about how to proceed blocks the next decision.
- **When** the agent does that work within authorization.
- **Then** it treats the actions as context gathering and validation respectively. Not knowing the check result does not itself require a separate inquiry notice. A useful update is still permitted under the communication rules.

For an example of a useful update, see [`01-discovery/deliverables/proposed-examples/authorization-and-communication.md` § EX-AC-014 — Useful updates are permitted without a report per increment](authorization-and-communication.md#ex-ac-014--useful-updates-are-permitted-without-a-report-per-increment). The requester separately clarified the scope of reading existing documentation ([`01-discovery/deliverables/open-questions.md` § Reading existing project documentation](../open-questions.md#reading-existing-project-documentation)).

## EX-BI-005 — A notice already given need not be repeated

- **Given** the requester already identified the blocking uncertainty and why it matters, and authorized a narrow investigation.
- **When** the agent starts that investigation.
- **Then** it need not send a second notice about the same uncertainty. The work still stays within the authorized bounds.

## EX-BI-006 — A prescribed procedure can still be inquiry

- **Given** context gathering leaves a material uncertainty about which storage approach is viable, a documented benchmark can resolve it, the bounded benchmark is authorized, and the uncertainty has not been communicated.
- **When** the agent uses that benchmark to choose how to proceed.
- **Then** it promptly explains the uncertainty and its significance and conducts a bounded inquiry subject to evidence sufficiency and reassessment. Being a documented procedure does not exempt it. Running the same benchmark solely to validate a settled limit would not be inquiry merely because its output is unknown.

Whether the benchmark’s purpose should change the need for notice is an open question for the requester ([`01-discovery/deliverables/open-questions.md` § Prescribed benchmarks](../open-questions.md#prescribed-benchmarks)).

## EX-BI-007 — Reading existing project documents remains context gathering

The requester clarified how to treat reading ([`01-discovery/deliverables/open-questions.md` § Reading existing project documentation](../open-questions.md#reading-existing-project-documentation)). This particular example remains proposed.

- **Given** a material question blocks the next decision and an existing project architecture record may answer it; reading that record is within scope.
- **When** the agent reads that record and directly relevant project documentation.
- **Then** the reading remains context gathering, even for that blocking question, without an inspection-by-inspection inquiry notice. Authorization, proportionate effort, and cumulative reassessment still apply. This does not exempt subsequent empirical inquiry or required decision disclosures.

## EX-BI-008 — An unanswered question is not evidence for another attempt

- **Given** a bounded inquiry ends inconclusively, its findings justify no further useful authorized step, and the next decision still depends on the missing evidence.
- **When** the agent reassesses the result.
- **Then** it reports the missing evidence, uncertainty, unfinished work, and available alternatives and seeks direction. It does not repeat attempts solely because the question is unanswered or claim that reaching the step boundary satisfied the objective.
