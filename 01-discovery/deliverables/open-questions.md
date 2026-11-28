# Product questions and requester conclusions

## Unresolved outcomes

### Prescribed benchmarks

One inquiry question extends beyond reading documents. Suppose a material uncertainty still blocks the choice of an approach and the requester has not been told. Should running a prescribed benchmark to resolve that blocker call for notice when running the same benchmark to validate a settled limit would not? [`01-discovery/deliverables/proposed-examples/bounded-inquiry.md` § EX-BI-006 — A prescribed procedure can still be inquiry](proposed-examples/bounded-inquiry.md#ex-bi-006--a-prescribed-procedure-can-still-be-inquiry) illustrates the proposed boundary. The decision about reading documentation covers neither use of the benchmark.

### Routine local choices

Suppose the requester has settled the consequential choices, and an easily reversible implementation detail falls within the agreed limits. The agent has permission to choose it. Under what conditions, if any, would proceeding without asking also be a recommendation or an obligation? Would asking for approval in those circumstances fall short of the intended behavior even if the agent completes the work correctly?

### When no safe step is possible

Suppose activating a requested change would exceed an agreed limit, but the agent can still investigate safely or prepare a reversible draft. At what point does the duty to present alternatives and seek direction apply? Does it turn on the blocked operational change, the usefulness of the remaining authorized steps, or another condition?

## Requester conclusions awaiting requirements review

Both conclusions are requester direction given on November 22, 2026. Explicit incorporation into accepted requirements is pending. The requester did not accept any example as defining or authorize implementation changes in giving these clarifications.

### Reading existing project documentation

Reading existing project documentation is context gathering regardless of why the agent reads it. This includes reading an architecture record to answer an already identified blocking question. Authorization and limits still apply. If material uncertainty remains after relevant context gathering and blocks progress, the agent must promptly communicate the uncertainty and its significance unless both were already communicated. Any investigation must stay bounded and within existing authority and limits. Notification grants no authority.

[`01-discovery/deliverables/proposed-examples/bounded-inquiry.md` § EX-BI-007 — Reading existing project documents remains context gathering](proposed-examples/bounded-inquiry.md#ex-bi-007--reading-existing-project-documents-remains-context-gathering) illustrates this distinction. [`01-discovery/deliverables/proposed-examples/bounded-inquiry.md` § EX-BI-004 — Ordinary checking does not require an inquiry notice](proposed-examples/bounded-inquiry.md#ex-bi-004--ordinary-checking-does-not-require-an-inquiry-notice) illustrates routine checking.

### A request for a small correction

A requester asking for a “small correction” wants a succinct, focused code change. Substantial research may be justified to identify the correct solution. If the agent determines that implementing the correction requires a materially broader code change than the requester indicated, it must consult the requester before proceeding with that broader implementation. The distinction turns on the scope of the code change. The requester set no line count, effort threshold or automatic checkpoint for each additional edit.

Compare [`01-discovery/deliverables/proposed-examples/authorization-and-communication.md` § EX-AC-008 — Distinguish an expectation from a binding limit](proposed-examples/authorization-and-communication.md#ex-ac-008--distinguish-an-expectation-from-a-binding-limit), which assumes an otherwise authorized local correction, with [`01-discovery/deliverables/proposed-examples/authorization-and-communication.md` § EX-AC-004 — Do not pass a checkpoint or enlarge a limit on your own](proposed-examples/authorization-and-communication.md#ex-ac-004--do-not-pass-a-checkpoint-or-enlarge-a-limit-on-your-own), where the requester expressly imposed a limit.

Use the Discovery decision procedure ([`01-discovery/docs/maintaining-discovery.md` § Record a requester decision](../docs/maintaining-discovery.md#record-a-requester-decision)) to retain the scope and provenance of subsequent decisions.
