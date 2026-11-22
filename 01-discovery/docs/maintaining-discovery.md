# Maintaining Discovery

## Investigate a behavioral question

1. Describe a situation in which the answer matters. Who is acting, what decision do they face, and what would the requester experience? Identify the [affected objective](../deliverables/objectives-and-rationale.md) and where the question came from. For feedback from later work, record what was tried, under which conditions, and what was observed or found infeasible.
2. Try a concrete example, then vary a condition that could change the answer. Consider the requester’s desired result, what an implementer would have to know, and what an evaluator could observe that distinguishes success from failure. Try a counterexample or exceptional case where two interpretations predict different results. One requester can examine all three perspectives, with an agent helping identify assumptions or alternatives.
3. Check the cases against the scope, permissions and exceptions in the requester’s recorded direction. If plausible answers still differ, describe the distinguishing condition, consequences of each answer, and the missing fact or decision in the [question record](../deliverables/open-questions.md).

For example, compare reading a record with running a benchmark to settle a blocker. The [reading decision](../deliverables/open-questions.md#reading-existing-project-documentation) settles the former. Varying the purpose of the benchmark gives the requester a different distinction to consider.

When several rules or cases emerge, use Example Mapping to pair each proposed rule with cases that illustrate or challenge it. Keep unanswered questions alongside them. A conversation or short notes can suffice. For an unfamiliar methodological issue, start with Cucumber and follow the project's fallback and departure policy. [Cucumber Discovery](https://cucumber.io/docs/bdd/discovery-workshop/) · [Concrete examples](https://cucumber.io/docs/bdd/examples/) · [Example Mapping](https://cucumber.io/docs/bdd/example-mapping/) · [Project methodology](../../docs/pipeline.md#unresolved-methodological-questions)

## Revise an objective or its rationale

Identify the requester need and the authorized direction for the desired outcome or its priority. Feedback, observed costs, and constraints help explain why an outcome matters and what limits it. An observation about one attempt can motivate a proposal. Establishing a new priority requires a decision about that priority. If the decision is missing, keep the proposed change open.

In [objectives and rationale](../deliverables/objectives-and-rationale.md), state the outcome, its qualifications, and the source and scope of the direction. Check that each affected reason still explains the desired outcome and preserves its qualifications and priority. A different way to achieve the same outcome need not change the objective.

## Add or revise a proposed example

1. Choose a [subject file](../deliverables/example-coverage.md#proposed-example-suites) or start one if the situation introduces a new subject. A concrete proposal about an undecided outcome is enough to add a case.
2. For a new example, add one to the highest EX number already assigned in any subject file. Write it with at least three digits, as in `EX-001`, followed by a descriptive title in the heading. Keep the ID when revising or moving a case. Retain retired IDs with their history so they cannot be reused.
3. State the starting facts, action and proposed observable result in Given/When/Then form. Explain any assumed project terms or permissions the reader needs. Keep conditions and exceptions with the outcome. If the [decision record](../deliverables/open-questions.md) contains a relevant conclusion or open question, link the case and that entry in both directions.
4. Update the subject’s IDs and count and the catalog total. Extend a range only for a consecutive ID. List a nonconsecutive ID separately. Check that the ID appears on exactly one case heading and that links reach any moved or retitled case.

## Record a requester decision

Record who decided, when, the reviewed proposal or version, the scope, conditions, exceptions, affected examples and any remaining uncertainty. Keep the original ID traceable. Move a settled distinction out of the unresolved list even if requirements review is pending. Identify any example the requester expressly accepted as defining. Agreement on an outcome alone leaves its examples proposed.
