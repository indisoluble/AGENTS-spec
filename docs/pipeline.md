# Developing the contract with BDD

Behavior-driven development (BDD) uses concrete examples and short feedback cycles to establish shared intent and guide implementation. Cucumber describes three iterative practices. AGENTS-spec assigns the work to five technical stages. Their responsibilities, inputs, and outputs are defined in the [stage interfaces](architecture.md#stage-interfaces).

## Applying the three practices

- **Discovery.** Explore examples, counterexamples, assumptions, and material unknowns from requester, implementation, and evaluation perspectives. One person may represent several perspectives. Consider the affected actors, normal and exceptional conditions, conflicts, feasibility, and missing evidence. The [Discovery deliverable](../01-discovery/deliverables/discovery.md) and its example suites keep sources, proposal coverage, and unresolved questions visible.
- **Formulation.** Express agreed behavior as precise rules and distinguishing examples suitable for automation. Proposals remain open until the requester or authorized delegate accepts them. The [Formulation baseline](../02-formulation/deliverables/baseline.md) identifies accepted wording and any examples expressly accepted as defining.
- **Automation.** In reference BDD, agreed examples become executable tests that guide implementation. Here Evaluations defines and runs checks, Design selects mechanisms, and Candidate realizes them as operational instructions.

Deriving a deliverable takes judgment. Several formulations can fit an objective, and several mechanisms can satisfy a requirement. Compare them against the relevant intent and constraints. Design retains consequential choices, reasons, alternatives, trade-offs, status, and successors. BDD itself establishes neither completeness nor [decision authority](authority.md).

## Test-first iteration

For a requirements-led change, one iteration can proceed as follows.

1. Discovery explores the question and Formulation records the accepted behavior.
2. Evaluations derives an expectation from the accepted requirement or an expressly accepted defining example. Establish a check that can distinguish satisfying the condition from violating it before claiming coverage.
3. The check guides authorized work in Design and Candidate. Existing behavior that already satisfies the condition can pass without an implementation edit.
4. Evaluations runs the check against the identified candidate and assesses the evidence. Both evaluation activities belong to the same stage and framework.

Stage numbers express conceptual progression. Activities can overlap wherever their dependencies permit. Technical feasibility can reopen Discovery or Formulation, and observations can send a question back to any responsible owner. The [traceability relationships](traceability.md) connect those findings to the affected deliverables and explain the limits of today's clause-based cases.

When automation cannot reliably distinguish satisfying from violating an obligation, report the gap and review the evidence. The [requester-guidance case](../05-evaluations/deliverables/cases/requester-guidance.md#human-review-and-interpretation) illustrates the difference between detecting a response and judging its content. Future accepted examples remain subject to Automation.

## Unresolved methodological questions

Stage boundaries, repository layout, decision authority, documentation conventions, and tooling are project decisions. Where the project leaves a methodological question open, use [Cucumber's reference BDD practice](https://cucumber.io/docs/bdd/). Where it offers no applicable guidance, draw on established engineering practice and resolve the remaining choice proportionately with the responsible owner.

For a genuine departure from reference BDD, record the affected practice, scope and conditions, reason, closer alternatives considered and why they are inadequate, and consequences with the affected owner. That owner decides adoption within their authority. For a verification departure, also identify the reviewer, evidence, judgment method, and inconclusive scope. Record a standing change to the shared methodology here. There is no standing exception to Automation.
