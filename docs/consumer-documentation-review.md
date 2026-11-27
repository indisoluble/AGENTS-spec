# Reviewing consumer documentation

Use these checks to review the two guides against the operating contract and its design. Use the situations in [`03.0-design/docs/design-illustrations.md`](../03.0-design/docs/design-illustrations.md) to assess the explanation. Use the Design review checks ([`03.0-design/docs/design-review.md`](../03.0-design/docs/design-review.md)) for mechanism explanations. Editorial review adds no runtime duties, accepted requirements, evaluator criteria, or approval step. Shared authority ([`docs/authority.md` § Status of engineering records](authority.md#status-of-engineering-records))

## Reviewing contract explanations

Use the cross-stage change guide ([`docs/changing-the-contract.md` § Change the owner and verify its dependents](changing-the-contract.md#change-the-owner-and-verify-its-dependents)) for maintenance boundaries and [`03.0-design/deliverables/contract-design.md`](../03.0-design/deliverables/contract-design.md) for mechanisms and rationale. The checks below concern explanation and comprehension, not behavioral evidence.

### Reader paths

The reference reader knows Git and coding agents. A junior developer should be able to adopt the contract without studying its methods first; “power users” seek practical depth rather than possessing method expertise.

| Document | Reader task |
| --- | --- |
| [`04-candidate/pre_README.md`](../04-candidate/pre_README.md) | Understand the offering, ordered objectives (token control, then requester awareness/control), benefits and limits; install with replacement precautions, check adoption, and try a first task. It should enable adoption alone, concisely and accessibly, without exaggerated claims. |
| [`04-candidate/pre_README-powerusers.md`](../04-candidate/pre_README-powerusers.md) | Evaluate/use the contract through formal, detailed practical guidance. Start with an ordinary outcome-oriented request and show agent handling, then situations, conditions, limitations, exceptions, and examples. Reference detail must be findable without preceding the first example; this remains user documentation. |

Use plain Markdown, descriptive headings, direct links, and comparison tables. Introduce terms before use and methods where they explain action or choice. Present default behavior before optional requester controls, and the workflow before its activities. Connect request, decision trigger, context/evidence, action, result, and next step; phase names and definition links alone do not explain that path. Read examples without relying on the editing conversation.

Neither guide nor Design documentation has a numeric length target or limit. Detail and useful repetition serve understanding; assess navigation and the combined impression of headings/examples, keeping consequential qualifications near claims. Avoid empty categories, obligatory templates, and formalism without explanatory value. The contract's standing-context constraint ([`02.0-formulation/deliverables/baseline.md` § Portability and standing-context qualifications](../02.0-formulation/deliverables/baseline.md#portability-and-standing-context-qualifications)) applies separately to `AGENTS.md`.

### Explanatory ownership and evidence

Guides and design can explain the same subject at different depths for distinct reader needs under the summary boundary ([`docs/documentation.md` § Choosing the owner](documentation.md#choosing-the-owner)). Link to canonical detail rather than copying complete procedures, reference-assignment tables, or lifecycles; necessary copies retain owners/update relationships. The practical guide owns requester-facing explanations; mechanism documents own design rationale.

The practical CSV walkthrough ([`04-candidate/pre_README-powerusers.md` § From a request to a result](../04-candidate/pre_README-powerusers.md#from-a-request-to-a-result)) shows the requester experience. The technical walkthrough ([`03.0-design/deliverables/mechanisms/work-cycle.md` § How the design works in a task](../03.0-design/deliverables/mechanisms/work-cycle.md#how-the-design-works-in-a-task)) states the scenario assumptions and explains design choices. Check their shared assumptions when either walkthrough changes. Alternative paths state their assumptions. Illustrative choices and editorial checks cannot become policy.

For review-only work, compare the practical record examples ([`04-candidate/pre_README-powerusers.md` § Records during review and exploration](../04-candidate/pre_README-powerusers.md#records-during-review-and-exploration)) with the assessment-write mechanism ([`03.0-design/deliverables/mechanisms/requester-decisions-and-reporting.md` § Assessment writes and durable findings](../03.0-design/deliverables/mechanisms/requester-decisions-and-reporting.md#assessment-writes-and-durable-findings)). For validation, compare the guide’s evidence examples ([`04-candidate/pre_README-powerusers.md` § Assess the result](../04-candidate/pre_README-powerusers.md#assess-the-result)) with the conditions for substituting a check ([`03.0-design/deliverables/mechanisms/engineering-and-validation.md` § Validation and test evidence](../03.0-design/deliverables/mechanisms/engineering-and-validation.md#validation-and-test-evidence)). The guide’s provider evidence dates ([`04-candidate/pre_README-powerusers.md` § Evidence dates](../04-candidate/pre_README-powerusers.md#evidence-dates)) distinguish the checks behind its compatibility guidance ([`04-candidate/pre_README-powerusers.md` § Tool compatibility](../04-candidate/pre_README-powerusers.md#tool-compatibility)).

Match claims to their sources:

- Intended outcomes and accepted behavior are recorded in [`01-discovery/deliverables/objectives-and-rationale.md` § Established objectives](../01-discovery/deliverables/objectives-and-rationale.md#established-objectives) and the requirements baseline ([`02.0-formulation/deliverables/baseline.md`](../02.0-formulation/deliverables/baseline.md)). Keep candidates and proposals distinct.
- Current operating rules: delivered contract ([`04-candidate/pre_AGENTS.md`](../04-candidate/pre_AGENTS.md)), with the clause index ([`docs/contract-traces.md` § Contract clause index](contract-traces.md#contract-clause-index)) for detail/rationale. Current design remains binding without detailed product acceptance, and authorized redesign may replace it.
- Methods: operational contract meaning and reference assignments/consultation boundaries ([`03.0-design/deliverables/methods-and-references.md` § Principles and reference boundaries](../03.0-design/deliverables/methods-and-references.md#principles-and-reference-boundaries)), without importing whole frameworks or stronger source rhetoric. Clear rules need no routine method research.
- Evaluator claims: E1–E40 ([`05-evaluation/README.md` § Evaluator requirements](../05-evaluation/README.md#evaluator-requirements)), applicable case interpretation, and captured contract/rubric.
- When a change depends on how a provider discovers instruction files ([`03.0-design/deliverables/delivery-and-portability.md` § Installed paths and provider discovery](../03.0-design/deliverables/delivery-and-portability.md#installed-paths-and-provider-discovery)) or loads them, assess those claims against the applicable official documentation and the behavior observed in the target environment.

Do not imply that contract text overrides higher-priority instructions, grants permissions, bypasses approvals, or technically guarantees compliance.

### Meaning and evidence checks

Review the complete reader task, including headings and walkthroughs. For PR1 ([`02.0-formulation/deliverables/baseline.md` § R5](../02.0-formulation/deliverables/baseline.md#r5)), read the contract on its own to check whether its operating instructions are complete.

Apply the checks in [`03.0-design/docs/design-review.md` § Meaning and evidence checks](../03.0-design/docs/design-review.md#meaning-and-evidence-checks) to explanatory prose and examples. Check Markdown, paths, anchors, incoming references, and release-relative meanings ([`docs/architecture.md` § Staged sources and release-relative references](architecture.md#staged-sources-and-release-relative-references)). Consumer artifacts retain no engineering dependencies, including navigation. Apply artifact-specific criteria and keep transient measurements/validation records in working or review records.

### Reader comprehension questions

| After reading | The reader should explain |
| --- | --- |
| [`04-candidate/pre_README.md`](../04-candidate/pre_README.md) | Objectives, files to install, adoption checks, and token-control limits. |
| [`04-candidate/pre_README-powerusers.md` § From a request to a result](../04-candidate/pre_README-powerusers.md#from-a-request-to-a-result) | Initial framing, why that increment, completion evidence, and findings informing the next authorized step. |
| Pausing or continuing ([`04-candidate/pre_README-powerusers.md` § When the agent pauses or continues](../04-candidate/pre_README-powerusers.md#when-the-agent-pauses-or-continues)) | Informing/consulting/reporting, prior-direction triggers, binding limits, useful updates without per-increment reports, and handoff state. |
| Investigation ([`04-candidate/pre_README-powerusers.md` § When an investigation is needed](../04-candidate/pre_README-powerusers.md#when-an-investigation-is-needed)) | Inquiry versus context/validation, already-communicated uncertainty, bounds without announced allowances, evidence sufficiency/reassessment, and notification versus consultation. |
| Requirements and documentation ([`04-candidate/pre_README-powerusers.md` § Use requirements and documentation](../04-candidate/pre_README-powerusers.md#use-requirements-and-documentation)) | Canonical knowledge, record triggers, and why recording cannot authorize decisions. |

For reader testing, ask members of the reference audience to perform/explain these tasks in their own words. Distinguish inability to find an answer from misunderstanding it, and observed comprehension from editorial prediction. Keep observations in working/review records; editorial review alone does not establish usability.
