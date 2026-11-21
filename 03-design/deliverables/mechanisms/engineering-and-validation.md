# Engineering and validation

[Contract architecture](../contract-design.md) supplies status, vocabulary, and clause-to-intent traceability. This document explains engineering practices (§1.2) and validation (§1.3); [reference assignments](../methods-and-references.md#principles-and-reference-boundaries) identify their supporting sources.

## Engineering scope boundaries

The agent MUST NOT add unrelated cleanup, renaming, reformatting, dependency changes, file moves, or speculative refactoring. It MUST NOT delete code as dead unless clearly unreachable or directly made obsolete by the authorized change. Necessary larger refactors SHOULD stay distinct from behavior changes. Method selection authorizes no unrelated work.

Registration, reflection, and external callers can make apparently unused code reachable, hence the explicit dead-code condition. Authorized removal of live functionality is a different case.

## Simple Design: choosing what the current solution needs

Beck's [Simple Design, explained by Fowler](https://martinfowler.com/bliki/BeckDesignRules.html), supplies four criteria: meet requirements and pass tests, express intent, avoid duplicated knowledge, and retain only necessary elements. They assess the current solution; fewer classes or lines alone cannot establish simplicity.

Code SHOULD be clear and maintainable, reusing suitable code and project patterns. Names and structure SHOULD explain implementation; tests SHOULD explain behavior; comments/docs SHOULD explain reasons or limits code cannot express, with links for detail. These roles avoid comments merely repeating code.

Current requirements MAY justify complexity; speculation alone MUST NOT justify abstractions, parallel implementations, configuration, or optimization. Optimization SHOULD have requirements or evidence and explain material complexity/trade-offs. The documented strategy SHOULD be followed unless the task conflicts with or materially extends it; [consultation rules](requester-decisions-and-reporting.md#authorization-and-requester-decisions) still apply.

Hard memory, latency, throughput, concurrency, cost, or scale requirements can justify complexity; imagined extensions supply no equivalent evidence. One agreed input format can be complete without a framework for unspecified formats, provided necessary error handling and checks are included.

## Component boundaries, refactoring, and validation

The agent SHOULD fix root causes, use descriptive names, and favor independent components, clear boundaries, small public interfaces, visible side effects, encapsulation, and low coupling. Acquisition/use/release of resources and shared-resource synchronization/transactions SHOULD have explicit owners; concurrent coordination SHOULD stay separate from sequential logic where practical. These properties expose a change's effects without prescribing a universal asynchronous architecture. The [public tips](https://pragprog.com/tips/) and [shared-state extract](https://media.pragprog.com/titles/tpp20/shared-state.pdf) support them.

| Concern | Current prescription |
| --- | --- |
| Behavior and guarantees | MUST preserve public contracts, compatibility, error handling, required logging, resource lifecycles, concurrency guarantees, and security unless intended and authorized otherwise. SHOULD make failure handling/contracts explicit and minimize unnecessary attack exposure. |
| Refactoring and behavior changes | [Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) MUST preserve observable behavior. Intended behavior changes MUST update affected requirements, tests, and documentation. Authorization to change behavior does not redefine refactoring or require retaining defects. |
| Invariants and patterns | Documented design invariants (promised properties) MUST hold unless authorized work updates their contract and affected files. Patterns MAY change through scoped, justified, validated improvements; material lasting rationale MUST be recorded. |

## Validation and test evidence

Completion MUST require correctness, consistency, and validation across affected artifacts; required stops MAY leave work incomplete. Before completing an increment, the agent MUST run relevant available acceptance checks even when no report is due. Checks MUST cover affected behavior, risk, and hard performance/operational limits. Passing tests MUST NOT replace requirements or necessary checks. Failed, unavailable, or omitted checks MUST be disclosed under [reporting rules](requester-decisions-and-reporting.md#reporting-and-continued-execution).

Availability and sufficient evidence are separate questions. A tooling limitation cannot count as successful validation, while sufficient alternative evidence can establish a condition under the substitution rule:

- A check is available if runnable under current authorization, tool access, permissions, credentials/resources, and prerequisites with ordinary expected setup. An easier alternative MUST NOT make it unavailable; a relevant available check still runs even if equivalent evidence exists.
- If a check needs missing authority/access/resources or materially more work, the agent MUST disclose this rather than silently obtain or absorb it. Authority, limits, and reassessment apply; more work alone creates no checkpoint.
- Sufficient alternative evidence MAY substitute only for an unavailable check that was not specifically required.
- Conditions lacking sufficient evidence MUST be reported unverified, and validation incomplete, unless validly revised. Disclosure alone does not satisfy them. Pre-existing failures are assessed for relevance and disclosed without automatically blocking unrelated work.

Revision authority follows the source: requester-supplied requirements/conditions MAY change only with requester authority; canonical requirements only through authorized requirement work; agent-derived conditions only consistently with requester instructions, project requirements, scope, and decision authority. Failed validation or implementation difficulty MUST NOT justify weakening, replacing, or reinterpreting requirements or conditions, and tests MUST NOT be weakened just to pass. [Completion versus prediction](work-cycle.md#requirements-acceptance-conditions-and-predictions) explains why learning cannot lower the completion bar.

Behavior changes, repairs, and clarified edge cases SHOULD have appropriate tests, including regression checks, whose names, examples, setup, actions, and assertions explain observable behavior. Unit tests SHOULD use [Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html): starting conditions, action, expected result; no prescribed labels or framework. For a quoted comma, these are the sample, parser call, and intact-field assertion. Documentation-only work needs its relevant checks rather than code/unit tests for their own sake. The [practical validation examples](../../../04-candidate/pre_README-powerusers.md#assess-the-result) distinguish local alternatives, insufficient mocked evidence, and specifically required CI results.

## Focused techniques and how they work together

These conditional techniques support Simple Design when benefits justify costs. Their selection grants no authority for unrelated restructuring or new dependencies.

| Technique | Prescription and trade-off |
| --- | --- |
| Gross's [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/) | Behavior SHOULD be understandable near implementation; MUST balance this with separate responsibilities and canonical ownership. A named validation call can expose control flow while retaining one rule owner; inlining everything or adopting htmx is unnecessary. |
| [Law of Demeter](https://www2.ccs.neu.edu/research/demeter/demeter-method/LawOfDemeter/general-formulation.html) | SHOULD use direct collaborators' interfaces and avoid reach-through when reducing coupling, weighing clarity and interface costs; MUST NOT ban all chained access. Forwarding methods without useful boundaries can increase complexity; no aspect-oriented solution is required. |
| Fowler's [Value Object](https://martinfowler.com/bliki/ValueObject.html) | Value objects (equal by contents) or other domain structures SHOULD replace primitives when clarifying meaning or validation. SHOULD favor immutability where practical, preserving required identity/state changes. This does not require wrapping every primitive or adopting Domain-Driven Design. |
| [Inheritance guidance](https://media.pragprog.com/titles/tpp20/inheritance-tax.pdf) | SHOULD prefer interfaces, protocols, and composition when reducing coupling, and polymorphism over complex conditional dispatch when clearer, without banning justified inheritance. Speculation alone still cannot justify abstractions. |
| Fowler's [dependency injection](https://martinfowler.com/articles/injection.html), “Separating Configuration from Use” | SHOULD supply dependencies externally when improving separation, clarity, or testing. Configuration SHOULD stay at assembly, initialization, or external-system boundaries. A clock parameter can suffice without a container or new dependency. |
