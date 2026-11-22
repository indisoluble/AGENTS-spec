# Product questions and requester conclusions

## Unresolved outcomes

One inquiry question extends beyond reading documents. Suppose a material uncertainty still blocks the choice of an approach and the requester has not been told. Should running a prescribed benchmark to resolve that blocker call for notice when running the same benchmark to validate a settled limit would not? [EX-BI-006](proposed-examples/bounded-inquiry.md#ex-bi-006--a-prescribed-procedure-can-still-be-inquiry) illustrates the proposed boundary. The decision about reading documentation covers neither use of the benchmark.

## Requester conclusions awaiting requirements review

Both conclusions are requester direction given on November 22, 2026. Explicit incorporation into accepted requirements is pending. The requester did not accept any example as defining or authorize implementation changes in giving these clarifications.

### Reading existing project documentation

Reading existing project documentation is context gathering regardless of why the agent reads it. This includes reading an architecture record to answer an already identified blocking question. Authorization and limits still apply. If material uncertainty remains after relevant context gathering and blocks progress, the agent must promptly communicate the uncertainty and its significance unless both were already communicated. Any investigation must stay bounded and within existing authority and limits. Notification grants no authority.

[EX-BI-007](proposed-examples/bounded-inquiry.md#ex-bi-007--reading-existing-project-documents-remains-context-gathering) illustrates this distinction. [EX-BI-004](proposed-examples/bounded-inquiry.md#ex-bi-004--ordinary-checking-does-not-require-an-inquiry-notice) illustrates routine checking.

### A request for a small correction

A requester asking for a “small correction” wants a succinct, focused code change. Substantial research may be justified to identify the correct solution. If the agent determines that implementing the correction requires a materially broader code change than the requester indicated, it must consult the requester before proceeding with that broader implementation. The distinction turns on the scope of the code change. The requester set no line count, effort threshold or automatic checkpoint for each additional edit.

Compare [EX-AC-008](proposed-examples/authorization-and-communication.md#ex-ac-008--distinguish-an-expectation-from-a-binding-limit), which assumes an otherwise authorized local correction, with [EX-AC-004](proposed-examples/authorization-and-communication.md#ex-ac-004--do-not-pass-a-checkpoint-or-enlarge-a-limit-on-your-own), where the requester expressly imposed a limit.

Use the [Discovery decision procedure](../docs/maintaining-discovery.md#record-a-requester-decision) to retain the scope and provenance of subsequent decisions.
