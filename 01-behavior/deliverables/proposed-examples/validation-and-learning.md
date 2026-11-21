# Proposed examples: validation and learning

All examples remain **proposed and unaccepted**. See [classifications and shared qualifications](../discovery.md#formulation-questions-and-evidence-limits) and the [coverage matrix](../discovery.md#requirement-to-scenario-coverage).

## BR5 — Completion supported by validation

Requirement: [BR5](../baseline.md#br5--completion-supported-by-validation). Current qualification evidence: [design explanation](../../../02-design/deliverables/mechanisms/engineering-and-validation.md#validation-and-test-evidence), [contract](../../../03-candidate/pre_AGENTS.md) §1.3.

### BR5.1 — Run relevant checks that are available

**Direct — proposed.**

- **Given** a fix changes error handling and an applicable acceptance check is runnable with ordinary setup under current authorization.
- **When** the agent validates the fix.
- **Then** it runs the applicable check and checks the affected behavior and constraints. A quicker smoke test does not make the applicable check unavailable.

### BR5.2 — Substitute evidence only when the missing check was not required

**Direct — proposed.**

- **Given** an integration check cannot run under current access and was not specifically required; an authorized replay is available as possible evidence for the same acceptance condition.
- **When** the agent assesses what the replay demonstrates.
- **Then** it may use the replay only if it supplies sufficient evidence for that condition, explaining the unavailable check and substitute. If the replay does not establish part of the condition, it reports that part unverified and validation incomplete. It does not silently acquire extra access.

### BR5.3 — A required check remains required when it is unavailable

**Direct — proposed.**

- **Given** the requester explicitly requires a staging check and the agent has no authorized staging access.
- **When** local checks pass.
- **Then** the agent reports the staging check as unavailable, validation as incomplete, and what is needed to finish. It neither obtains access on its own nor claims the required check was satisfied locally.

### BR5.4 — Failure is not permission to lower the bar

**Direct — proposed.**

- **Given** an acceptance test fails because the implementation mishandles a required edge case.
- **When** the agent reviews the failure.
- **Then** it fixes the issue within scope or reports the failure and unfinished work. It does not weaken requirements, acceptance conditions, or tests, or reinterpret them merely to claim completion.

**Current design:** [Validation and test evidence](../../../02-design/deliverables/mechanisms/engineering-and-validation.md#validation-and-test-evidence) retains the qualified recommendations for appropriate tests, regression checks, and test-writing conventions. [Reporting and continued execution](../../../02-design/deliverables/mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution) retains the mechanics for reporting material departures from recommendations. These selected design details remain outside this example's proposed defining outcome.

### BR5.5 — Validate research against its own objective

**Direct — proposed.**

- **Given** the requester authorizes only an investigation into why a check fails.
- **When** the agent confirms the cause with evidence but makes no fix.
- **Then** it may report the investigation complete if the evidence meets the research objective, while making clear that the defect has not been fixed or validated as fixed.

### BR5.6 — A passing smoke check does not establish a hard limit

**Direct — proposed.**

- **Given** an authorized change must satisfy an existing hard memory limit, its smoke check passes, and no evidence yet establishes memory use under the required workload.
- **When** the agent assesses completion.
- **Then** it runs the relevant available check for that limit; if the condition cannot be sufficiently verified within authority, it reports it unverified and validation incomplete. The smoke result alone cannot establish the hard limit or replace the requirement.

## BR6 — Learning from observed results

Requirement: [BR6](../baseline.md#br6--learning-from-observed-results). Current qualification evidence: [design explanation](../../../02-design/deliverables/mechanisms/work-cycle.md#learning-throughout-the-work), [contract](../../../03-candidate/pre_AGENTS.md) §§1, 1.3–1.4.

### BR6.1 — Change the approach without changing the goal

**Direct — proposed.**

- **Given** an authorized trial was expected to avoid a duplicate call, but the observed result disproves that prediction.
- **When** the agent plans its next step.
- **Then** it uses the observation to revise or discard the approach. It keeps the acceptance condition and authority unchanged, and undertakes another trial only if it remains justified and authorized.

### BR6.2 — Keep useful learning without creating paperwork for its own sake

**Direct — proposed.**

- **Given** a discarded approach reveals both a lasting compatibility constraint and a one-off local setup issue.
- **When** the agent decides what to retain.
- **Then** it uses the relevant findings in its next decision and handles the material, durable constraint under BR8. It does not create a separate learning artifact merely because it ran a trial.

### BR6.3 — Retain an approach that the evidence supports

**Direct — proposed.**

- **Given** an authorized experiment meets the acceptance conditions and its observations support the approach, with no material contrary evidence.
- **When** the agent uses the result to decide what follows.
- **Then** it may retain the approach and uses the findings in the next authorized decision. Learning does not require changing a successful approach, inventing a failure, producing a worksheet, or starting more work after the task is complete.
