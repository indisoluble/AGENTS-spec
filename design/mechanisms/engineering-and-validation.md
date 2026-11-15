# Engineering and validation

This document owns engineering scope boundaries, Simple Design, component and refactoring practices, validation and test evidence, and the focused engineering techniques with their interactions.

**Status: current binding design, with rationale distinguished from accepted product requirements.** The [shared status and evidence boundaries](../../docs/authority-and-change.md#status-and-evidence-boundaries) retain authority and revision qualifications. These explanations add no operating duties beyond the delivered contract.

Return to [contract architecture](../contract-design.md) and its [shared vocabulary and clause-to-requirement index](../contract-design.md#current-semantics-vocabulary-and-coverage). Related owners: [completion, predictions, and inquiry](work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation), [authorization and reporting](requester-decisions-and-reporting.md), [DRY and documentation](knowledge-and-documentation.md), and [method assignments and consultation limits](../methods-and-references.md#principles-and-reference-boundaries).

## Engineering scope boundaries

**Current scope boundary (§1.2).** The agent MUST NOT add unrelated cleanup, renaming, reformatting, dependency changes, file moves, or speculative refactoring. It MUST NOT delete code as dead unless the code is clearly unreachable or directly made obsolete by the authorized change. Necessary larger refactors SHOULD stay distinct from behavior changes. These boundaries apply to the practices below; method selection does not authorize unrelated work.

## Simple Design: choosing what the current solution needs

Beck's [Simple Design, explained by Fowler](https://martinfowler.com/bliki/BeckDesignRules.html), supplies four criteria: meet requirements and pass tests, express intent, avoid duplicated knowledge, and retain only necessary elements. They assess the current solution; fewer classes or lines alone cannot establish simplicity.

Code SHOULD be clear and maintainable, reusing suitable code and project patterns. Names and structure SHOULD explain implementation; tests SHOULD explain behavior; comments and documentation SHOULD explain reasons or limits code cannot express, with links for detail. These recommendations assign complementary explanatory roles rather than requiring comments to repeat the code.

Current requirements MAY justify complexity; speculation alone MUST NOT justify abstractions, parallel implementations, configuration, or optimization. Optimization SHOULD have requirements or evidence and explain material complexity and trade-offs. The documented strategy SHOULD be followed unless the task conflicts with or materially extends it; the authority and consultation guards still apply.

Hard memory, latency, throughput, concurrency, cost, or scale requirements may justify complexity. An imagined future extension does not provide equivalent evidence. Supporting one agreed input format can be complete without a framework for unspecified formats, while still including its necessary error handling and checks. A documented optimization strategy supplies project context and is a strong default; a task that conflicts with or materially extends it remains subject to the consultation rules. Material trade-offs remain visible.

## Component boundaries, refactoring, and validation

The agent SHOULD fix root causes, use descriptive names, and favor independent components, clear boundaries, small public interfaces, visible side effects, encapsulation, and low coupling. Resource acquisition, use, and release, and shared-resource synchronization and transactions SHOULD have explicit owners; concurrent coordination SHOULD stay separate from sequential logic where practical. These properties make the effects of a change easier to understand. The [public tips](https://pragprog.com/tips/) and [shared-state extract](https://media.pragprog.com/titles/tpp20/shared-state.pdf) support these concerns; their exact assignments appear in [Principles and reference boundaries](../methods-and-references.md#principles-and-reference-boundaries). Practical separation supports clear ownership without prescribing a universal asynchronous architecture.

The current preservation duties are explicit:

| Concern | Current prescription |
| --- | --- |
| Protected behavior and guarantees | The agent MUST preserve public contracts, compatibility, error handling, required logging, resource lifecycles, concurrency guarantees, and security unless intended and authorized otherwise. It SHOULD make failure handling and contracts explicit and minimize unnecessary attack exposure. |
| Refactoring and behavior changes | [Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) MUST preserve observable behavior. Intended behavior changes MUST update affected requirements, tests, and documentation. The authorization exception for intended behavior changes does not redefine refactoring. |
| Invariants and patterns | Documented design invariants (promised properties) MUST hold unless authorized work updates their contract and affected files. Patterns MAY change through scoped, justified, validated improvements; material lasting rationale MUST be recorded. |

Neither preservation distinction requires retaining a defect when changing it is intended and authorized. Lasting rationale is retained under the applicable record rules, not discarded simply because a pattern was improved.

The dead-code condition matters because registration, reflection, or external callers may make apparently unused code reachable. Clear unreachability or direct obsolescence from the authorized change is needed for removal *as dead code*. Explicitly authorized removal of live functionality is a different case.

## Validation and test evidence

Completion MUST require correctness, consistency, and validation across affected artifacts; required stops MAY leave work incomplete. Before completing an increment, the agent MUST run relevant available acceptance checks, independently of whether a report is produced then. Checks MUST cover affected behavior, risk, and hard performance and operational limits. Passing tests MUST NOT replace requirements or necessary checks. Failed, unavailable, and omitted checks MUST be disclosed under the [reporting rule](requester-decisions-and-reporting.md#reporting-and-continued-execution); any need for requester involvement still follows the [progression guards](../../contract/prerelease_AGENTS.md#2-progression-guards).

Behavior changes, defect repairs, and clarified edge cases SHOULD have appropriate tests, including regression checks. Their names, examples, setup, actions, and assertions should explain the expected observable behavior as part of that recommendation. This does not require code or unit tests for their own sake during documentation-only work; the acceptance checks appropriate to that work still apply.

Distinguishing check availability from acceptance prevents a tooling limitation from being treated as successful validation. It also allows sufficient alternative evidence to establish a condition when the contract's substitution rules permit it.

Sufficient alternative evidence MAY substitute only when the original check is unavailable and is not specifically required. A check is available if runnable under current authorization, tool access, permissions, credentials or resources, and prerequisites with ordinary expected setup. An easier alternative MUST NOT make it unavailable: a relevant available acceptance check still runs even if an alternative could provide equally sufficient evidence. If a check needs missing authority, access, or resources, or materially more work, the agent MUST disclose this rather than silently obtain or absorb it, applying the authorization, limit, and reassessment rules. More work alone does not create a checkpoint.

Conditions lacking sufficient evidence MUST be reported unverified, and validation incomplete, unless validly revised under existing authority. Disclosure alone cannot establish them. A pre-existing failure is assessed for relevance and disclosed, without automatically blocking unrelated work. The [practical validation examples](../../contract/prerelease_README-powerusers.md#assess-the-result) distinguish available checks, equivalent local checks, insufficient mocked evidence, and a specifically required CI result.

Unit tests SHOULD use [Given/When/Then](https://martinfowler.com/bliki/GivenWhenThen.html): starting conditions, action under test, and expected result. For a quoted field containing a comma, those parts are the sample, the parser call, and the intact-field assertion. The contract prescribes neither literal labels nor a testing framework. The agent MUST NOT weaken tests just to pass.

## Focused techniques and how they work together

These techniques support Simple Design when their benefits justify their costs. Their selection grants no authority for unrelated restructuring or new dependencies.

**Gross's [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/)**

Behavior SHOULD be understandable near its implementation; the agent MUST balance this with separate responsibilities and canonical ownership. A clearly named validation call can keep the control flow readable while the rule stays in its canonical owner. The contract does not require inlining everything or adopting htmx.

**The [Law of Demeter](https://www2.ccs.neu.edu/research/demeter/demeter-method/LawOfDemeter/general-formulation.html)**

The agent SHOULD use direct collaborators' interfaces, avoiding reach-through when this reduces coupling and weighing clarity and interface costs; it MUST NOT ban all chained access. The trade-off is reduced coupling versus interface complexity: forwarding methods that add no useful boundary can make the code harder to follow. The contract therefore weighs coupling and clarity rather than imposing a blanket ban on chained access or requiring an aspect-oriented solution.

**Fowler's [Value Object](https://martinfowler.com/bliki/ValueObject.html)**

Value objects (equal by contents) or other domain structures SHOULD replace primitives when they clarify meaning or validation. The agent SHOULD favor immutability where practical, preserving required identity and state changes. The contract makes this a conditional design recommendation; it requires neither wrapping every primitive nor adopting Domain-Driven Design.

**The [inheritance extract](https://media.pragprog.com/titles/tpp20/inheritance-tax.pdf)**

The agent SHOULD prefer interfaces, protocols, and composition when they reduce coupling, and polymorphism over complex conditional dispatch when clearer, without banning justified inheritance. The conditions matter: these preferences do not justify abstractions based on speculation alone or prohibit suitable inheritance.

**Fowler's [dependency injection](https://martinfowler.com/articles/injection.html), “Separating Configuration from Use”**

The agent SHOULD supply dependencies externally when this improves separation, clarity, or testing. Configuration SHOULD stay at assembly, initialization, or external-system boundaries. Supplying a clock as a parameter can suffice; no container or new dependency is required.
