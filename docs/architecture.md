# AGENTS-spec engineering architecture

AGENTS-spec develops a reusable, self-contained operating contract ([`04-candidate/pre_AGENTS.md`](../04-candidate/pre_AGENTS.md)) for coding agents. Each engineering stage maintains its own deliverables. The shared documentation index ([`docs/README.md`](README.md)) locates knowledge used across stages.

## Purpose and scope

Engineering documentation supports understanding, changing, and verifying the product. The consumer package is designed for use without the engineering tree. Delivered `AGENTS.md` contains the complete runtime instructions, the bridges load or direct tools to it, and the two consumer guides explain adoption and use. Consumer artifacts have no references or dependencies back into engineering documentation.

## Stage interfaces

AGENTS-spec has seven sibling stages. The numbers express conceptual progression and proximity. Each stage owns its work independently, including Acceptance and Conformance. The project maps these responsibilities to the three BDD practices in [`docs/pipeline.md` § Applying the three practices](pipeline.md#applying-the-three-practices).

| Stage and entry point | Principal inputs | What the stage owns |
| --- | --- | --- |
| **01 Discovery** · [`01-discovery/README.md`](../01-discovery/README.md) | Requester needs, feedback, observations and established knowledge | Objectives and rationale, proposals, exploratory examples, open questions and requester conclusions |
| **02.0 Formulation** · [`02.0-formulation/README.md`](../02.0-formulation/README.md) | Discovery and decisions by the requester or authorized delegate | Accepted product requirements, applicable constraints and expressly accepted defining examples |
| **02.1 Acceptance** · [`02.1-acceptance/README.md`](../02.1-acceptance/README.md) | Formulation supplies accepted intent. The engine supplies reusable facilities where needed. | Mechanism-independent evaluation definitions, including fixtures, assertions, qualitative criteria, coverage and gaps |
| **03.0 Design** · [`03.0-design/README.md`](../03.0-design/README.md) | Formulation and authorized design decisions | Selected mechanisms, specifications, decisions and rationale, including qualified or missing requirement traces |
| **03.1 Conformance** · [`03.1-conformance/README.md`](../03.1-conformance/README.md) | Design, applicable requirements and Acceptance coverage, with engine facilities where needed | Complementary mechanism-specific definitions, fixtures, assertions, qualitative criteria, coverage and reasons for omissions |
| **04 Candidate** · [`04-candidate/`](../04-candidate/) | Design and applicable delivery constraints | Staged operational instructions and supporting consumer artifacts |
| **05 Evaluation** · [`05-evaluation/README.md`](../05-evaluation/README.md) | Definition owners supply criteria. Execution uses the selected Candidate and engine. Assessment uses identified definitions and evidence. | Integrated evaluator contract and suite, run evidence and provenance, automated and qualitative assessments, consolidated findings and engineering conclusions |

Formulation supplies the authority for requirements and constraints. Design supplies the authority for a selected mechanism within its approved scope. Test-first work can expose an ambiguity early. Changing either source still requires a decision by its owner. [`docs/authority.md` § Development decisions](authority.md#development-decisions)

The shared engine sits outside the numbered stages. It provides workspace preparation, agent and process execution, observation, evidence capture, functional-check and reporting interfaces, and their verification. Product-specific expectations belong with the definition owners. Evaluation binds those definitions to one Candidate, selects the cases and execution order, retains evidence, and determines the aggregate outcome and pending review. [`engine/README.md`](../engine/README.md) · [`05-evaluation/docs/framework-design.md` § Contract injection and fixture inputs](../05-evaluation/docs/framework-design.md#contract-injection-and-fixture-inputs)

An Acceptance result needs the applicable Acceptance definition, an identified Candidate and execution or inspection evidence. A Conformance result needs the corresponding Conformance definition, Candidate and evidence. The Candidate is the subject of both assessments. Coverage records describe what the definitions can establish before any particular run. Findings from a run can reopen a decision at any stage. [`docs/traceability.md` § Tracing a requirement and its evaluation](traceability.md#tracing-a-requirement-and-its-evaluation)

### Direction of stage references

A numbered stage may depend on its own knowledge, shared foundational knowledge and earlier stages. This applies to Markdown links and displayed paths, executable imports, fixture and resource lookup, subprocess commands and working directories, test helpers and indirect dependencies. A required forward dependency remains a dependency if it is reached through a shared page, helper or launcher. The engine and its documentation and tests must work with all numbered stages absent.

Root `docs/` owns cross-stage navigation, traceability indexes and change-propagation procedures. Keep specific dependencies with the owner that uses them. Earlier owners can receive feedback by recording the relevant conditions and observation locally. Test-first activity creates no additional authoritative input to Design or Candidate. Consumer files retain their installed meanings and independence from engineering documentation. [`docs/maintaining-documentation.md` § Check stage references](maintaining-documentation.md#check-stage-references)

Some legacy Conformance definitions still rely on Candidate clauses and refer readers forward to integrated review procedures. These preserved exceptions remain open pending authorized owner review. Their provisional placement establishes neither Design derivation nor compliance with the dependency rule. The inventory distinguishes historical citations, operative criteria and documentation dependencies. [`docs/migration-inventory.md` § Case-level exceptions](migration-inventory.md#case-level-exceptions)

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
