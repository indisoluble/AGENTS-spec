# Maintaining Formulation

## Establish what the decision covers

Start with the [Discovery decision record](../../01-discovery/deliverables/open-questions.md). Read the proposal and its distinguishing cases alongside the relevant [objective and rationale](../../01-discovery/deliverables/objectives-and-rationale.md), the [existing requirement and constraints](../deliverables/baseline.md), and the cited evidence or open question. Product acceptance requires a decision about the outcome.

Identify the requester or authorized delegate, the version they reviewed, and the outcome, conditions, exceptions, and examples their decision covers. Make the decision traceable from the entry. Several rules can share one source, as BR1–BR10 share the [owner-reported acceptance account](acceptance-record.md#behavioral-acceptance-and-editorial-provenance). Distinguish the editor’s interpretation from what the source establishes about the decision maker’s reasons.

For a partial decision, formulate the settled outcome and link the remaining choice to its [Discovery question](../../01-discovery/deliverables/open-questions.md). New evidence may reopen a question. Revising accepted intent takes a decision under the same [product authority](../../docs/authority.md#development-decisions).

## Write or amend the rule

1. Identify the actor or artifact, the circumstances that trigger the rule, and an outcome a reader could observe. Ask what a satisfying response and a violation would look like under the same conditions. Vary a condition to expose a permission or exception. If the decision leaves it unclear whether a response is allowed, take that distinction back to Discovery.
2. State the rule in the vocabulary of the task. The baseline uses EARS (Easy Approach to Requirements Syntax) to connect conditions to required responses. For an event-driven duty, the form is “When [event], the [actor] shall [response].” A state can qualify when the duty applies. Keep exceptions close and use additional sentences when needed. Preserve the difference between a duty, a permissible choice, and a recommendation with justified departures. EARS is the project’s specification technique. BDD uses concrete examples to establish shared understanding. [Cucumber on Formulation](https://cucumber.io/docs/bdd/#formulation-what-it-should-do)
3. Keep the requirement’s ID when amending it. Give a newly accepted outcome its own baseline entry and ID if no existing requirement covers it. Compare what the decision and the proposed wording require, recommend, permit, or prohibit, for whom and when. Check interacting rules, priorities, and applicable constraints, including their measurement and exceptions. An editorial clarification preserves what would satisfy or violate the existing rule. A newly required response, an earlier deadline, or a lost exception needs authority for that change.

For example, read [BR3](../deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction) against two actions by an agent considering a new consequential architectural direction. Obtaining direction before adopting it satisfies the consultation duty when the specific choice lacks prior authorization. Disclosing the choice afterwards addresses a separate duty and cannot supply prior authorization. Extending that same mandatory timing to *every* unsettled material choice would also change BR3, which gives other choices a qualified ask-first recommendation. The [R2 rationale](../../01-discovery/deliverables/objectives-and-rationale.md#r2) explains the interest in requester control.

Keep essential qualifications with the rule. Link its rationale and acceptance source from the baseline. Ask whether a different mechanism could yield the same permitted outcomes under the same constraints. For example, [BR6](../deliverables/baseline.md#br6--learning-from-observed-results) requires the agent to use observed results in subsequent work. It leaves room for more than one way to learn from them.

## Determine whether an example defines the rule

A useful example gives the relevant starting facts, an event or action, and a visible result. Include the fact that distinguishes two plausible responses. For a permission, allow the choices the rule permits. Given/When/Then can make that distinction readable. The wording alone establishes neither agreement, executability, nor coverage. [Cucumber on concrete examples](https://cucumber.io/docs/bdd/examples/)

| What you have | How to use it |
| --- | --- |
| An exploratory Discovery example | Follow its ID to the proposed facts and outcome. Both Direct and Detail review are proposal classifications. |
| An expressly accepted defining example | Record the agreed version and its conditions beside the requirement in Formulation. Cite the decision that accepted that example as defining. Link the resulting entry back to the Discovery ID so its origin and any outstanding parts remain traceable. Acceptance of the rule alone leaves the example proposed. |

## Verify the rule and its coverage

Compare the baseline with the decision and the previous version, including adjacent qualifications, interacting rules and constraints. Check that a reader can distinguish permitted outcomes from violations using the baseline alone. Report a missing decision or an ambiguity with the conditions that expose it.

Use the [coverage matrix](../deliverables/example-coverage.md) to connect a requirement to the Discovery cases that illustrate it. Index each case once under its primary requirement in the column matching its Discovery classification. Record a secondary interaction only when the case exercises it. Reconcile IDs, links, classifications and totals with the [subject suites](../../01-discovery/deliverables/example-coverage.md#proposed-example-suites). A matrix entry does not accept a case as defining.
