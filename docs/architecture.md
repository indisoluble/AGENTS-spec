# AGENTS-spec engineering architecture

AGENTS-spec develops a reusable, self-contained [operating contract](../04-candidate/pre_AGENTS.md) for coding agents. Each engineering stage maintains its own deliverables. The [shared documentation index](README.md) locates knowledge used across stages.

## Purpose and scope

Engineering documentation supports understanding, changing, and verifying the product. The consumer package is designed for use without the engineering tree. Delivered `AGENTS.md` contains the complete runtime instructions, the bridges load or direct tools to it, and the two consumer guides explain adoption and use. Consumer artifacts have no references or dependencies back into engineering documentation.

## Stage interfaces

The mapping uses [Cucumber's three BDD practices](https://cucumber.io/docs/bdd/#three-practices). BDD leaves repository layout to the project. AGENTS-spec gives Discovery and Formulation distinct owners and divides Automation into mechanism selection, operational realization, and evaluation. The five stage directories are siblings. The grouping by practice is conceptual.

| BDD practice | Stage | Principal inputs | Principal outputs |
| --- | --- | --- | --- |
| Discovery | [`01-discovery/`](../01-discovery/README.md) | Requester needs, feedback, observations, existing knowledge | Objectives, rationale, proposals, exploratory examples, open questions |
| Formulation | [`02-formulation/`](../02-formulation/README.md) | Discovery deliverables and requester decisions | Precise accepted requirements, applicable constraints, any expressly accepted defining examples |
| Automation | [`03-design/`](../03-design/README.md) | Accepted requirements and applicable constraints | Selected mechanisms, specifications, decisions and rationale |
| Automation | [`04-candidate/`](../04-candidate/) | Selected mechanisms and delivery constraints | Staged operational contract and supporting consumer artifacts |
| Automation | [`05-evaluations/`](../05-evaluations/README.md) | Behavioral specifications, evaluation criteria, identified candidate | Evaluation definitions, executable checks, observations, assessments and evidence |

Keep each interface limited to what the stage needs from its direct dependencies. A deliverable's location confers no [acceptance status](authority.md#status-of-engineering-records). Formulation supplies accepted intent to both Design and Evaluations. Design selects the mechanism that Candidate expresses as operational instructions. For requirements-led work, Evaluations derives the expectation from accepted intent and compares observed behavior against it. The [traceability model](traceability.md#tracing-a-requirement-and-its-evaluation) connects these paths.

Read stages in numerical order to learn the pipeline. Explain each stage’s work using its own terms, shared definitions and earlier outputs. Links to later stages can trace a realization or a finding. Feedback can reopen an earlier question. The [test-first iteration](pipeline.md#test-first-iteration) shows how work moves among the stages. Each engineering stage owns its procedures and supporting knowledge under the [documentation conventions](documentation.md#choosing-the-owner).

## Staged sources and release-relative references

[`04-candidate/`](../04-candidate/) contains exactly the five files below. Engineering links target their staged sources. Display names and adopting-project examples use their intended consumer locations. Design owns the delivery rationale, and the [runtime authority rules](authority.md#runtime-authority) explain what governs the installed product.

| Staged source in `04-candidate/` | Intended consumer location |
| --- | --- |
| `pre_AGENTS.md` | `AGENTS.md` |
| `pre_CLAUDE.md` | `CLAUDE.md` |
| `pre_copilot-instructions.md` | `.github/copilot-instructions.md` |
| `pre_README.md` | `README.md` |
| `pre_README-powerusers.md` | `README-powerusers.md` |

References to standard instruction and documentation filenames describe adopting projects. Copilot’s `../AGENTS.md` resolves from the installed `.github/` directory. Both guides contain links to `pre_*` files that resolve in staging and break after installation. The adoption guide’s `../LICENSE` reaches the [repository license](../LICENSE) in staging and points outside the installed package. Design explains [bridge behavior](../03-design/deliverables/delivery-and-portability.md#why-the-bridges-differ) and [provider-specific instruction discovery](../03-design/deliverables/delivery-and-portability.md#installed-paths-and-provider-discovery).

## Architecture decisions

The [system-wide decision record](decisions.md#architecture-decisions) explains choices affecting multiple stages. [Design decisions and alternatives](../03-design/docs/decisions.md#architecture-decisions) and [evaluation framework decisions](../05-evaluations/docs/framework-design.md#architecture-decisions) retain their domain-specific reasons, alternatives, and successors. The [engineering authority and runtime contract decision](decisions.md#engineering-authority-and-the-runtime-contract) explains the basis for engineering ownership of requirements and design and the scope of the delivered contract's authority.

## Risks and technical debt

- Design records the [interpretation risks of accepted wording compromises](../03-design/deliverables/delivery-and-portability.md#current-wording-trade-offs).
- [Traceability gaps](traceability.md#current-traceability-gaps) and [evaluation coverage limits](../05-evaluations/docs/evaluation-model.md#purpose-and-evaluation-model) bound claims about requirements-derived acceptance.
- Evaluation evidence is specific to the environment exercised. The framework records the [limits of isolation and integration evidence](../05-evaluations/docs/framework-design.md#agent-execution).
