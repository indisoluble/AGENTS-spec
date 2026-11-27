# AGENTS-spec

AGENTS-spec develops a reusable `AGENTS.md` file that tells coding agents how to work with the people requesting changes.

Suppose an agent pauses to ask a question when the requester expected it to keep working. Before rewriting the instruction, a contributor can use the pipeline to compare what people wanted, what the instruction said, and what the agent actually did.

## Development pipeline

The numbered stages show the conceptual order of work. The arrows show what each owner uses. A requirement can survive a change of mechanism, so checking the required outcome and checking the selected mechanism answer different questions.

```mermaid
---
title: How AGENTS-spec develops AGENTS.md for coding agents
config:
  flowchart:
    wrappingWidth: 280
    rankSpacing: 32
    nodeSpacing: 28
---
flowchart TD
    D["<b>01 Discovery</b><br/>Explore needs and questions"] -->|proposals| F["<b>02.0 Formulation</b><br/>Record the requirements<br/>the requester accepts"]
    F -->|required outcomes| A["<b>02.1 Acceptance</b><br/>How will we tell if a<br/>requirement is met?"]
    F -->|requirements and constraints| M["<b>03.0 Design</b><br/>Select and specify mechanisms"]
    M -->|mechanism prescriptions| C["<b>03.1 Conformance</b><br/>What else must we check<br/>about the selected mechanism?"]
    A -->|coverage to consider| C
    M -->|mechanisms to realize| K["<b>04 Candidate</b><br/>Stage AGENTS.md<br/>and companion files"]
    A -->|requirements checks| E["<b>05 Evaluation</b><br/>Run checks, assess evidence<br/>and draw conclusions"]
    C -->|mechanism checks| E
    K -->|artifact under evaluation| E
    X(["<b>Shared engine</b><br/>Reusable evaluation infrastructure"]) -->|execution and evidence capture| E
```

**Current coverage.** One registered smoke case checks the infrastructure. Nine behavioral cases exercise existing Candidate clauses, and eight require human judgment. There are zero independently derived requirements-Acceptance cases. The nine cases have provisional Conformance ownership pending review of their basis in Design and their complementary coverage.

## Where to start

| What are you looking for? | Where to start |
| --- | --- |
| Use the instructions and install the companion files | [`04-candidate/pre_README.md`](04-candidate/pre_README.md) · [`docs/architecture.md` § Staged sources and release-relative references](docs/architecture.md#staged-sources-and-release-relative-references) |
| Find the need, the accepted rule or the design choice | [`01-discovery/README.md`](01-discovery/README.md) · [`02.0-formulation/README.md`](02.0-formulation/README.md) · [`03.0-design/README.md`](03.0-design/README.md) |
| Trace an instruction to a decision | [`04-candidate/pre_AGENTS.md`](04-candidate/pre_AGENTS.md) · [`docs/contract-traces.md` § Contract clause index](docs/contract-traces.md#contract-clause-index) |
| See what the checks cover and how results are assessed | [`02.1-acceptance/deliverables/coverage.md`](02.1-acceptance/deliverables/coverage.md) · [`03.1-conformance/deliverables/coverage.md`](03.1-conformance/deliverables/coverage.md) · [`05-evaluation/README.md`](05-evaluation/README.md) |
| Understand how the stages fit together or change the contract | [`docs/architecture.md` § Stage interfaces](docs/architecture.md#stage-interfaces) · [`docs/pipeline.md` § Test-first iteration](docs/pipeline.md#test-first-iteration) · [`docs/README.md`](docs/README.md) |
