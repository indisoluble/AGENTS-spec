# Contract design review

Use these editorial checks to review how the current design is explained. The [design illustrations](design-illustrations.md) supply situations to read against the explanation. Use [Maintaining Design](maintaining-design.md) when the change concerns the mechanism itself. Editorial review adds no runtime duties, accepted requirements, evaluator criteria, or approval step. [Shared authority](../../docs/authority.md#status-of-engineering-records)

## Reviewing contract explanations

Use the [cross-stage change guide](../../docs/changing-the-contract.md#change-the-owner-and-verify-its-dependents) for maintenance boundaries and [contract design](../deliverables/contract-design.md) for mechanisms and rationale. The checks below concern explanation and comprehension, not behavioral evidence.

### Reader paths

The reference reader knows Git and coding agents. A junior developer should be able to adopt the contract without studying its methods first; “power users” seek practical depth rather than possessing method expertise.

| Document | Reader task |
| --- | --- |
| [README.md](../../04-candidate/pre_README.md) | Understand the offering, ordered objectives (token control, then requester awareness/control), benefits and limits; install with replacement precautions, check adoption, and try a first task. It should enable adoption alone, concisely and accessibly, without exaggerated claims. |
| [README-powerusers.md](../../04-candidate/pre_README-powerusers.md) | Evaluate/use the contract through formal, detailed practical guidance. Start with an ordinary outcome-oriented request and show agent handling, then situations, conditions, limitations, exceptions, and examples. Reference detail must be findable without preceding the first example; this remains user documentation. |
| [Contract architecture](../deliverables/contract-design.md) | Understand selected mechanisms, interactions, reasons, trade-offs, and decision status. [Formulation](../../02-formulation/README.md) locates accepted intent and [Discovery](../../01-discovery/README.md) locates proposals; [shared architecture](../../docs/architecture.md) explains engineering relationships. |

Use plain Markdown, descriptive headings, direct links, and comparison tables. Introduce terms before use and methods where they explain action or choice. Present default behavior before optional requester controls, and the workflow before its activities. Connect request, decision trigger, context/evidence, action, result, and next step; phase names and definition links alone do not explain that path. Read examples without relying on the editing conversation.

Neither guide nor Design documentation has a numeric length target or limit. Detail and useful repetition serve understanding; assess navigation and the combined impression of headings/examples, keeping consequential qualifications near claims. Avoid empty categories, obligatory templates, and formalism without explanatory value. The contract's [standing-context constraint](../../02-formulation/deliverables/baseline.md#portability-and-standing-context-qualifications) applies separately to `AGENTS.md`.

### Explanatory ownership and evidence

Guides and design can explain the same subject at different depths for distinct reader needs under the [summary boundary](../../docs/documentation.md#choosing-the-owner). Link to canonical detail rather than copying complete procedures, reference-assignment tables, or lifecycles; necessary copies retain owners/update relationships. The practical guide owns requester-facing explanations; mechanism documents own design rationale.

The [practical CSV walkthrough](../../04-candidate/pre_README-powerusers.md#from-a-request-to-a-result) owns shared scenario facts; the [technical walkthrough](../deliverables/mechanisms/work-cycle.md#how-the-design-works-in-a-task) uses them to explain design choices and stays aligned. Alternative paths state their assumptions. Illustrative choices and editorial checks cannot become policy.

Match claims to their sources:

- Intended outcomes and accepted behavior are recorded in the [established objectives](../../01-discovery/deliverables/objectives-and-rationale.md#established-objectives) and the [requirements baseline](../../02-formulation/deliverables/baseline.md). Keep candidates and proposals distinct.
- Current operating rules: [delivered contract](../../04-candidate/pre_AGENTS.md), with the [clause index](../deliverables/contract-design.md#contract-clause-index) for detail/rationale. Current design remains binding without detailed product acceptance, and authorized redesign may replace it.
- Methods: operational contract meaning and [reference assignments/consultation boundaries](../deliverables/methods-and-references.md#principles-and-reference-boundaries), without importing whole frameworks or stronger source rhetoric. Clear rules need no routine method research.
- Evaluator claims: [E1–E40](../../05-evaluations/README.md#evaluator-requirements), applicable case interpretation, and captured contract/rubric.
- When a change depends on how a provider [discovers instruction files](../deliverables/delivery-and-portability.md#installed-paths-and-provider-discovery) or loads them, assess those claims against the applicable official documentation and the behavior observed in the target environment.

Do not imply that contract text overrides higher-priority instructions, grants permissions, bypasses approvals, or technically guarantees compliance.

### Meaning and evidence checks

Review the complete reader task, including headings and walkthroughs. For [PR1](../../02-formulation/deliverables/baseline.md#r5), read the contract on its own to check whether its operating instructions are complete.

1. **Purpose:** fulfill the audience's task, explain ordered objectives and knowledge continuity, and preserve unique explanations at useful depth without promoting selected methods into product requirements.
2. **Semantics:** preserve actor, modality, trigger, timing, scope, authorization, conditions, exceptions, permissions versus obligations, and cross-clause interactions. Check limits versus expectations, autonomy versus consequential direction, notification versus consultation, and context/execution/validation versus inquiry. Preserve bounded conduct, evidence sufficiency, reassessment, and the already-communicated notification exception without inventing allowances or approval gates.
3. **Examples:** identify assumed facts, illustrative choices, expected outcomes, and observations. Explain why the evidence supports a choice, what completes the step, and what could change the next decision. Additional work alone does not trigger approval; absent architecture grants no unrestricted design authority. Organizing an explanation creates no additional process.
4. **Continuity:** retain distinct framing, notification, advance-disclosure, and consolidation timings. Routine-report recommendations are neither a ban nor a per-increment duty. Handoffs transfer results, authorization/limits including consumed allowances, direction, next-step bounds/conditions, evidence, and uncertainty rather than activity logs.
5. **Evidence/delivery:** distinguish intended effects from demonstrated results; text consistency proves neither comprehension, behavioral equivalence, nor savings. Check Markdown, paths, anchors, incoming references, and [release-relative meanings](../../docs/architecture.md#staged-sources-and-release-relative-references). Consumer artifacts retain no engineering dependencies, including navigation. Apply artifact-specific criteria and keep transient measurements/validation records in working or review records.

### Reader comprehension questions

| After reading | The reader should explain |
| --- | --- |
| [README.md](../../04-candidate/pre_README.md) | Objectives, files to install, adoption checks, and token-control limits. |
| [From a request to a result](../../04-candidate/pre_README-powerusers.md#from-a-request-to-a-result) | Initial framing, why that increment, completion evidence, and findings informing the next authorized step. |
| [Pausing or continuing](../../04-candidate/pre_README-powerusers.md#when-the-agent-pauses-or-continues) | Informing/consulting/reporting, prior-direction triggers, binding limits, useful updates without per-increment reports, and handoff state. |
| [Investigation](../../04-candidate/pre_README-powerusers.md#when-an-investigation-is-needed) | Inquiry versus context/validation, already-communicated uncertainty, bounds without announced allowances, evidence sufficiency/reassessment, and notification versus consultation. |
| [Requirements and documentation](../../04-candidate/pre_README-powerusers.md#use-requirements-and-documentation) | Canonical knowledge, record triggers, and why recording cannot authorize decisions. |

For reader testing, ask members of the reference audience to perform/explain these tasks in their own words. Distinguish inability to find an answer from misunderstanding it, and observed comprehension from editorial prediction. Keep observations in working/review records; editorial review alone does not establish usability.
