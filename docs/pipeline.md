# Developing the contract with BDD

Behavior-driven development (BDD) uses concrete examples and short feedback cycles to establish shared intent and guide implementation. AGENTS-spec adapts [Cucumber’s three iterative practices](https://cucumber.io/docs/bdd/#three-practices) to seven engineering stages. The directory layout is a project decision. Their responsibilities, inputs, and outputs are defined in [`docs/architecture.md` § Stage interfaces](architecture.md#stage-interfaces).

## Applying the three practices

- **Discovery (01).** Explore examples, counterexamples, assumptions, and material unknowns from requester, implementation, and evaluation perspectives. One person may represent several perspectives. Consider the affected actors, normal and exceptional conditions, conflicts, feasibility, and missing evidence. Discovery links proposed examples by subject ([`01-discovery/deliverables/example-coverage.md`](../01-discovery/deliverables/example-coverage.md)) to the questions and requester conclusions ([`01-discovery/deliverables/open-questions.md`](../01-discovery/deliverables/open-questions.md)).
- **Formulation (02.0).** Express agreed behavior as precise rules and distinguishing examples suitable for automation. Proposals remain open until the requester or authorized delegate accepts them. The Formulation baseline ([`02.0-formulation/deliverables/baseline.md`](../02.0-formulation/deliverables/baseline.md)) identifies accepted wording and any examples expressly accepted as defining.
- **Automation (02.1, 03.0, 03.1, 04 and 05).** In reference BDD, agreed examples become executable tests that guide implementation. Here Automation spans requirements checks, mechanism selection and checking, realization in the Candidate, and evaluation of the evidence.

Deriving a deliverable takes judgment. Several formulations can fit an objective, and several mechanisms can satisfy a requirement. Compare them against the relevant intent and constraints. Design retains consequential choices, reasons, alternatives, trade-offs, status, and successors. BDD itself establishes neither completeness nor decision authority ([`docs/authority.md`](authority.md)).

## Test-first iteration

The conceptual order gives contributors two opportunities to establish a check before the work it will assess.

1. Discovery explores desired outcomes and the conditions that distinguish them.
2. Formulation records the requirements, constraints and defining examples the requester has accepted.
3. Acceptance derives a distinguishing expectation from that accepted intent before Design selects a mechanism.
4. Design selects a mechanism under the applicable requirements and authorized design decisions.
5. Conformance identifies what Acceptance can already establish and defines complementary criteria for the selected mechanism before Candidate realizes it.
6. Candidate expresses the approved mechanism in the operating instructions and companion artifacts.
7. Evaluation runs applicable checks on an identified Candidate, assesses the evidence and records conclusions, including what remains inconclusive.

Write the expectation first. Implement executable checks as soon as technically feasible and use them during iterations. Existing behavior can already pass a new check. A written criterion followed by qualified human assessment is test-first in the sense of fixing the expectation in advance. Only an executable check exercised during implementation provides executable test feedback.

Activities can overlap, repeat and reopen as their inputs change. A trial can expose an observation failure, an unworkable mechanism or an unresolved product distinction. Take each finding to the owner with authority to resolve it. The traceability relationships ([`docs/traceability.md`](traceability.md)) connect findings to deliverables and bound what today's clause-based cases establish.

When automation cannot reliably distinguish satisfying from violating an obligation, report the gap and review the evidence. The requester-guidance case ([`03.1-conformance/deliverables/cases/requester-guidance.md` § Human review and interpretation](../03.1-conformance/deliverables/cases/requester-guidance.md#human-review-and-interpretation)) illustrates the difference between detecting a response and judging its content. Future accepted examples remain subject to Automation.

## Unresolved methodological questions

Stage boundaries, repository layout, decision authority, documentation conventions, and tooling are project decisions. Where the project leaves a methodological question open, use [Cucumber's reference BDD practice](https://cucumber.io/docs/bdd/). Where it offers no applicable guidance, draw on established engineering practice and resolve the remaining choice proportionately with the responsible owner.

For a genuine departure from reference BDD, record the affected practice, scope and conditions, reason, closer alternatives considered and why they are inadequate, and consequences with the affected owner. That owner decides adoption within their authority. For a verification departure, also identify the reviewer, evidence, judgment method, and inconclusive scope. Record a standing change to the shared methodology here. There is no standing exception to Automation.
