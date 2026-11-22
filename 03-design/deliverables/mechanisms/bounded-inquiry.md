# Bounded inquiry

[Contract §2.4](../../../04-candidate/pre_AGENTS.md#24-context-gathering-and-bounded-inquiry) sets the bounds on investigative increments and specifies when the requester needs notice, consultation, or findings. It supports [BR4, bounded investigation and timely reassessment](../../../02-formulation/deliverables/baseline.md#br4--bounded-investigation-and-timely-reassessment). The [contract architecture](../contract-design.md) supplies status, vocabulary, and clause-to-intent traceability.

## When inquiry applies

Inspecting relevant code, callers, tests, configuration, and directly related dependencies to establish context, and *all reading of existing project documentation*, are context gathering—even for a material blocking question. No inspection-by-inspection announcement is needed. Scope, limits, proportionality, and cumulative reassessment still apply.

Discovery’s proposed example [BR4.7](../../../01-discovery/deliverables/proposed-examples/bounded-inquiry.md#br47--reading-existing-project-documents-remains-context-gathering) illustrates the distinction using an architecture record. Whether every future contract must preserve this exclusion is an [open product question](../../../01-discovery/deliverables/open-questions.md#which-activities-count-as-inquiry).

Beyond context gathering, inquiry means investigating material uncertainty about how to proceed that blocks the next decision. Purpose distinguishes inquiry from settled execution and validation: unknown output alone does not trigger inquiry, and using a prescribed procedure does not exempt an investigation. The same measurement or test can serve any of these purposes.

The agent MUST promptly make the blocking uncertainty and its significance clear unless already communicated in the request or task framing. Notification requires no advance estimate or declared allowance. It neither grants authority nor creates an approval checkpoint. [Initial framing and reporting](requester-decisions-and-reporting.md#reporting-and-continued-execution) retain their separate timings.

## Evidence, reassessment, and consultation

Inquiry MUST focus on the blocking question through small, bounded, proportionate increments and end when evidence is sufficient. Sufficiency and bounds prevent different failures: treating any output as an answer, and continuing simply because the answer is unknown. At increment bounds with insufficient evidence, the agent MUST reassess before further investigation. Further attempts MUST be justified by preceding findings and remain within authorization, limits, and checkpoints. No numeric budget is required; announced bounds cannot substitute for disciplined conduct. The [practical example's](../../../04-candidate/pre_README-powerusers.md#when-an-investigation-is-needed) single sample illustrates a bounded experiment; its optional one-attempt checkpoint is a separate requester control. An inconclusive result alone establishes neither completion nor additional authority.

Narrow authorized investigation MAY establish facts for consultation. If it exposes a [decision requiring requester direction](requester-decisions-and-reporting.md#authorization-and-requester-decisions), consultation MUST precede adoption or implementation. Without evidence justifying the next increment, the agent MUST seek direction. Inquiry outcomes are reported at completion, handoff, or input requests; there is no automatic inquiry-end report or new announcement per attempt.

An investigative increment follows the same [planning rules](work-cycle.md#small-commitments-with-sufficient-depth) and [PDSA cycle](work-cycle.md#learning-throughout-the-work) as other work. The [quoted-comma example](work-cycle.md#requirements-acceptance-conditions-and-predictions) explains what a sample can establish about the investigation and the required behavior.

The [superseded announcement and stopping rule](../../docs/decisions.md#superseded-inquiry-announcement-and-stopping-rule) explains the earlier use of declared limits and the change in reporting occasions.
