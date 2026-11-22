# Methods and references

[Contract architecture](contract-design.md) supplies design status and clause traceability. This document explains method selection and reference semantics (§3.9), including exact source assignments and consultation limits.

## Choosing or replacing methods

[Method-selection qualifications](../../02-formulation/deliverables/baseline.md#method-selection-qualifications) constrain additions/replacements: recognized practices, freely accessible interpretive material sufficient for the assigned role, and distinct responsibilities unless explicitly revised. They permit authorized replacement without making current prescriptions optional.

[PDSA](mechanisms/work-cycle.md#learning-throughout-the-work) and [Simple Design](mechanisms/engineering-and-validation.md#simple-design-choosing-what-the-current-solution-needs) were judged sufficient for the agreed design alongside the [focused engineering references](mechanisms/engineering-and-validation.md#focused-techniques-and-how-they-work-together), [documentation conventions](mechanisms/knowledge-and-documentation.md#documentation-choices), and [explicit collaboration rules](mechanisms/requester-decisions-and-reporting.md#authorization-and-requester-decisions). Additional umbrella frameworks were not needed to supply those responsibilities.

In this design, PDSA connects a prediction and the observed result to the next decision. Simple Design guides choices about the solution within the increment. The recorded selection names no competing learning cycle. For a prospective replacement, see the [worked comparison against BR6](../docs/maintaining-design.md#compare-mechanisms-in-use).

## Principles and reference boundaries

Method references explain named practices without adding rules. The design adopts specific accounts rather than whole frameworks or access to a paid book. The [Pragmatic Programmer book](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) is paid; its assigned public tips/extracts are freely available.

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

The contract should normally suffice. Under the [method-reference rules](../../04-candidate/pre_AGENTS.md#39-method-references), an agent may consult a linked source when the contract leaves a material ambiguity in applying that method, reading only enough to resolve it. The ambiguity, consulted reference, and resulting interpretation must be reported, and no other practices are imported. Research stays bounded by §§1.1 and 2.4: if the consultation is inquiry into material uncertainty blocking the next decision, its notification and conduct requirements apply, including the exception for uncertainty and significance already communicated in the request or task framing. Clear rules must not be researched. Before broader research, the agent must explain the unresolved uncertainty and ask the requester. Technical research for a task follows its scope, authorization, and applicable inquiry rules. This distinction prevents an explanatory link from becoming an open-ended research assignment or importing a reference's stronger rhetoric as policy.
