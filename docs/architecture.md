# AGENTS-spec engineering architecture

**Structural migration status.** Five-stage descriptions on this page record the prior allocation where they differ from the [current ownership and transition record](migration-inventory.md). Detailed reconciliation is pending. Accepted product intent, design decisions and recorded evidence limits retain their existing authority.

AGENTS-spec develops a reusable, self-contained operating contract ([`04-candidate/pre_AGENTS.md`](../04-candidate/pre_AGENTS.md)) for coding agents. Each engineering stage maintains its own deliverables. The shared documentation index ([`docs/README.md`](README.md)) locates knowledge used across stages.

## Purpose and scope

Engineering documentation supports understanding, changing, and verifying the product. The consumer package is designed for use without the engineering tree. Delivered `AGENTS.md` contains the complete runtime instructions, the bridges load or direct tools to it, and the two consumer guides explain adoption and use. Consumer artifacts have no references or dependencies back into engineering documentation.

## Stage interfaces

The mapping uses [Cucumber's three BDD practices](https://cucumber.io/docs/bdd/#three-practices). BDD leaves repository layout to the project. AGENTS-spec gives Discovery and Formulation distinct owners and divides Automation into mechanism selection, operational realization, and evaluation. The five stage directories are siblings. The grouping by practice is conceptual.

| BDD practice | Stage | Principal inputs | Principal outputs |
| --- | --- | --- | --- |
| Discovery | [`01-discovery/README.md`](../01-discovery/README.md) | Requester needs, feedback, observations, existing knowledge | Objectives, rationale, proposals, exploratory examples, unresolved questions and requester conclusions |
| Formulation | [`02.0-formulation/README.md`](../02.0-formulation/README.md) | Discovery deliverables and requester decisions | Precise accepted requirements, applicable constraints, any expressly accepted defining examples |
| Automation | [`03.0-design/README.md`](../03.0-design/README.md) | Accepted requirements and applicable constraints | Selected mechanisms, specifications, decisions and rationale |
| Automation | [`04-candidate/`](../04-candidate) | Selected mechanisms and delivery constraints | Staged operational contract and supporting consumer artifacts |
| Automation | [`05-evaluation/README.md`](../05-evaluation/README.md) | Behavioral specifications, evaluation criteria, identified candidate | Evaluation definitions, executable checks, observations, assessments and evidence |

Keep each interface limited to what the stage needs from its direct dependencies. A deliverable's location confers no acceptance status ([`docs/authority.md` § Status of engineering records](authority.md#status-of-engineering-records)). Formulation supplies accepted intent to both Design and Evaluations. Design selects the mechanism that Candidate expresses as operational instructions. For requirements-led work, Evaluations derives the expectation from accepted intent and compares observed behavior against it. The traceability model ([`docs/traceability.md` § Tracing a requirement and its evaluation](traceability.md#tracing-a-requirement-and-its-evaluation)) connects these paths.

### Direction of stage references

Every Markdown file in a numbered stage may refer to its own contents, shared foundational knowledge and lower-numbered stages only. This applies to links, written paths and instructions that assume knowledge of another artifact. A maintainer must be able to understand and revise a stage’s outputs with those sources alone. Routing the reader through a shared page to required material in a higher-numbered stage still creates a forward dependency.

Keep a dependency with the artifact that relies on the source. Root `docs/` owns cross-stage navigation, traceability indexes and change-propagation procedures. Consumer files retain their installed meanings and independence from engineering documentation. See how to check stage references ([`docs/maintaining-documentation.md` § Check stage references](maintaining-documentation.md#check-stage-references)).

The numbering governs documentation dependencies. In a test-first iteration ([`docs/pipeline.md` § Test-first iteration](pipeline.md#test-first-iteration)), activities may overlap and any finding may reopen an earlier decision. Record the relevant conditions and observation at the earlier owner so its reader can evaluate the question there.

## Staged sources and release-relative references

[`04-candidate/`](../04-candidate) contains exactly the five files below. Engineering links to these files show their staged paths. Consumer link labels and adopting-project examples use the intended installed locations. Design owns the delivery rationale, and the runtime authority rules ([`docs/authority.md` § Runtime authority](authority.md#runtime-authority)) explain what governs the installed product.

| Staged source in `04-candidate/` | Intended consumer location |
| --- | --- |
| `pre_AGENTS.md` | `AGENTS.md` |
| `pre_CLAUDE.md` | `CLAUDE.md` |
| `pre_copilot-instructions.md` | `.github/copilot-instructions.md` |
| `pre_README.md` | `README.md` |
| `pre_README-powerusers.md` | `README-powerusers.md` |

References to standard instruction and documentation filenames describe adopting projects. Copilot’s `../AGENTS.md` resolves from the installed `.github/` directory. Both guides contain links to `pre_*` files that resolve in staging and break after installation. The adoption guide’s `../LICENSE` reaches the repository license ([`LICENSE`](../LICENSE)) in staging and points outside the installed package. Design explains bridge behavior ([`03.0-design/deliverables/delivery-and-portability.md` § Why the bridges differ](../03.0-design/deliverables/delivery-and-portability.md#why-the-bridges-differ)) and provider-specific instruction discovery ([`03.0-design/deliverables/delivery-and-portability.md` § Installed paths and provider discovery](../03.0-design/deliverables/delivery-and-portability.md#installed-paths-and-provider-discovery)).

## Architecture decisions

The system-wide decision record ([`docs/decisions.md` § Architecture decisions](decisions.md#architecture-decisions)) explains choices affecting multiple stages. Design decisions and alternatives ([`03.0-design/docs/decisions.md` § Architecture decisions](../03.0-design/docs/decisions.md#architecture-decisions)) and evaluation framework decisions ([`05-evaluation/docs/framework-design.md` § Architecture decisions](../05-evaluation/docs/framework-design.md#architecture-decisions)) retain their domain-specific reasons, alternatives, and successors. The engineering authority and runtime contract decision ([`docs/decisions.md` § Engineering authority and the runtime contract](decisions.md#engineering-authority-and-the-runtime-contract)) explains the basis for engineering ownership of requirements and design and the scope of the delivered contract's authority.

## Risks and technical debt

- Design records the interpretation risks of accepted wording compromises ([`03.0-design/deliverables/delivery-and-portability.md` § Current wording trade-offs](../03.0-design/deliverables/delivery-and-portability.md#current-wording-trade-offs)).
- Traceability gaps ([`docs/traceability.md` § Current traceability gaps](traceability.md#current-traceability-gaps)) and evaluation coverage limits ([`05-evaluation/docs/evaluation-model.md` § Purpose and evaluation model](../05-evaluation/docs/evaluation-model.md#purpose-and-evaluation-model)) bound claims about requirements-derived acceptance.
- Evaluation evidence is specific to the environment exercised. The framework records the limits of isolation and integration evidence ([`engine/docs/framework-design.md` § Agent execution](../engine/docs/framework-design.md#agent-execution)).
