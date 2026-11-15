# Methods and references

This document owns method selection and replacement rationale, reference semantics, exact source assignments and exclusions, and consultation boundaries. The linked mechanism documents own the selected methods’ detailed application.

**Status: current binding design, with rationale distinguished from accepted product requirements.** The [shared status and evidence boundaries](../docs/authority-and-change.md#status-and-evidence-boundaries) retain authority and revision qualifications. These explanations add no operating duties beyond the delivered contract.

Return to [contract architecture](contract-design.md) and its [shared vocabulary and clause-to-requirement index](contract-design.md#current-semantics-vocabulary-and-coverage). See the [selected-design index](docs/decisions-and-alternatives.md#selected-design-and-retained-decisions) and [superseded reference-consultation exemption](docs/decisions-and-alternatives.md#superseded-method-reference-inquiry-exemption) for decision status and history.

## Choosing or replacing methods

The method set was selected under the established [method-selection qualifications](../01-behavior/baseline.md#method-selection-qualifications), which own the criteria for additions and replacements and their revision conditions. Selected mechanisms are distinct from independently accepted enduring product requirements: [authorized redesign may reconsider them without making current prescriptions optional](../docs/authority-and-change.md#status-and-evidence-boundaries).

[PDSA](mechanisms/work-cycle-and-inquiry.md#learning-throughout-the-work) and [Simple Design](mechanisms/engineering-and-validation.md#simple-design-choosing-what-the-current-solution-needs) were judged sufficient for the agreed design alongside the [focused engineering references](mechanisms/engineering-and-validation.md#focused-techniques-and-how-they-work-together), [documentation conventions](mechanisms/knowledge-and-documentation.md#documentation-choices), and [explicit collaboration rules](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions). Additional umbrella frameworks were not needed to supply those responsibilities.

## Principles and reference boundaries

The delivered `AGENTS.md` remains the normative runtime authority. This section explains the current contract's method-reference semantics and source assignments; it adds no operating obligations and does not expand the practices adopted for AGENTS-spec development under the [development authority model](../docs/authority-and-change.md#development-time-and-runtime-authority).

Method references are linked sources explaining methods or practices named in the contract; they clarify those methods without adding rules. The accounts linked in this guide provide interpretive material within those conditions. The design draws on specific accounts rather than requiring whole frameworks or access to a paid book. The [Pragmatic Programmer book](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) is paid; its assigned public tips and extracts are freely available.

The exact [public-tip assignments](https://pragprog.com/tips/) are maintained here because the contract's links do not carry per-rule tip numbers:

| Concern | Assigned tips |
| --- | --- |
| Documentation synchronization | 13 |
| Components, boundaries, and coupling | 17, 44–45, 47–48 |
| Failures and contracts | 36–37 |
| Resources and mutation scope | 40–41 |
| Root causes | 65 |
| Attack surface | 72 |
| Naming | 74 |
| Regression checks | 94 |

The coupling assignment excludes tip 46. The DRY, inheritance, and shared-state extracts linked from their respective design explanations supply fuller accounts for their respective concerns. Attribution identifies supporting material, without claiming that one reference states the contract's combined preservation duties verbatim.

[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) supply requirement-keyword semantics. They concern the strength of agent obligations, while EARS expresses system requirements and ADRs record choices and reasons. Supporting explanations include [IHI's testing-changes guidance](https://www.ihi.org/library/model-for-improvement/testing-changes) and [arc42's debt FAQ](https://faq.arc42.org/questions/C-11-1/); they add no operating obligations.

The contract should normally suffice for ordinary cases. Under the [method-reference rules](../03-contract/prerelease_AGENTS.md#39-method-references), an agent may consult a linked source when the contract leaves a material ambiguity in applying that method, reading only enough to resolve it. The ambiguity, consulted reference, and resulting interpretation must be reported, and no other practices are imported. Research stays bounded by §§1.1 and 2.4: if the consultation is inquiry into material uncertainty blocking the next decision, its notification and conduct requirements apply, including the exception for uncertainty and significance already communicated in the request or task framing. Clear rules must not be researched. Before broader research, the agent must explain the unresolved uncertainty and ask the requester. Technical research for a task follows its scope, authorization, and applicable inquiry rules. This distinction prevents an explanatory link from becoming an open-ended research assignment or importing a reference's stronger rhetoric as policy.
