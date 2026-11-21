# AGENTS-spec engineering architecture

AGENTS-spec develops a reusable, self-contained [operating contract](../03-candidate/pre_AGENTS.md) for coding agents. This overview defines the pipeline and the interfaces between its stages. Each stage maintains the substance of its own deliverables. See [authority and change](authority-and-change.md) for change guidance and [system-wide engineering decisions](decisions.md) for rationale.

## Purpose and scope

Engineering documentation supports understanding, changing, and verifying the product. Consumer artifacts contain no references or dependencies back into it. The delivered `AGENTS.md` contains the complete runtime instructions; the bridges load or direct tools to it, and the two consumer guides explain adoption and use.

## Current BDD-first organization

**Objectives → Requirements → Mechanisms → Candidate AGENTS.md → Evaluations** spans four stages. Behavior owns the first two steps. Contributors can start at any stage and revisit another when a finding calls its premises into question. Knowledge maintenance spans all four.

Behavior, Design, and Evaluations place their outputs in `deliverables/`. Their READMEs locate those outputs and the supporting knowledge in each stage's `docs/`. Candidate contains only the five [staged consumer artifacts](#staged-sources-and-release-relative-references). The [stage layout decision](decisions.md#stage-deliverables-and-the-candidate-staging-exception) explains why.

### Stage interfaces

Use the row for the stage you are working in. Its inputs can constrain a decision or supply evidence for one. The [authority and status of each source](authority-and-change.md#development-time-and-runtime-authority) determine which choices are open.

| Stage | Inputs used | Outputs owned here | What others use |
| --- | --- | --- | --- |
| [Behavior](../01-behavior/README.md) | Requester direction, established constraints, proposals, and feedback about unclear or unmet intent | [Objectives and rationale](../01-behavior/deliverables/objectives-and-rationale.md), [requirements baseline](../01-behavior/deliverables/baseline.md), and [Discovery proposals and questions](../01-behavior/deliverables/discovery.md) | Design and Evaluations use accepted intent and applicable constraints. Discovery exposes open questions and examples for review with their proposal status. |
| [Design](../02-design/README.md) | Accepted intent, applicable constraints, and existing design decisions | Mechanism specifications with their rationale and limits, and [records of decisions and alternatives](../02-design/docs/decisions.md) | Candidate uses the selected mechanisms. The [contract clause index](../02-design/deliverables/contract-design.md#contract-clause-index) connects clauses to their specifications and supported intent. |
| [Candidate](../03-candidate/) | Selected design, delivery constraints, and the existing staged text | The [staged contract](../03-candidate/pre_AGENTS.md), two bridges, and two consumer guides | Consumers use the delivered package. The evaluator exercises an identified version of the contract. Engineering trace links stay outside the package. |
| [Evaluations](../04-evaluations/README.md) | The candidate under test, case conditions, and the basis for the expected result | [Case specifications and evaluator requirements](../04-evaluations/README.md#case-specifications), the framework, and the evidence it produces | Reviewers compare [observations and results](../04-evaluations/docs/running-and-reviewing.md#results-evidence-and-failure-investigation) with the case criteria to identify what was exercised and which owner can address a finding. |

In requirements-led evaluation, Behavior supplies accepted intent for the independent expectation. Candidate supplies the instructions given to the agent under observation. The [traceability and feedback model](authority-and-change.md#cross-domain-traceability-and-feedback) explains how to retain both paths and how to interpret the current clause-based cases. Consumers can use the contract independently of the evaluator.

### Staged sources and release-relative references

Engineering links target the staged sources. Display names and adopting-project examples use the intended consumer filenames:

| Staged source in `03-candidate/` | Intended consumer location |
| --- | --- |
| `pre_AGENTS.md` | `AGENTS.md` |
| `pre_CLAUDE.md` | `CLAUDE.md` |
| `pre_copilot-instructions.md` | `.github/copilot-instructions.md` |
| `pre_README.md` | `README.md` |
| `pre_README-powerusers.md` | `README-powerusers.md` |

References to standard instruction and documentation filenames describe adopting projects. A bridge reference that fails from a staged file can resolve correctly at its installed location. The consumer README's license link targets the repository-root `LICENSE`. Check links against their intended locations. Design explains [bridge behavior](../02-design/deliverables/delivery-and-portability.md#why-the-bridges-differ) and [provider-specific instruction discovery](../02-design/deliverables/delivery-and-portability.md#discovery-of-staged-instruction-files).

## Architecture decisions

The [system-wide decision record](decisions.md#architecture-decisions) explains choices affecting multiple stages. [Design decisions and alternatives](../02-design/docs/decisions.md#architecture-decisions) and [evaluation framework decisions](../04-evaluations/docs/framework-design.md#architecture-decisions) retain their domain-specific reasons, alternatives, and successors. The [engineering authority and runtime contract decision](decisions.md#engineering-authority-and-the-runtime-contract) explains the basis for engineering ownership of requirements and design and the scope of the delivered contract's authority.

## Risks and technical debt

- Design records the [interpretation risks of accepted wording compromises](../02-design/deliverables/delivery-and-portability.md#current-wording-trade-offs).
- [Traceability gaps](authority-and-change.md#cross-domain-traceability-and-feedback) and [evaluation coverage limits](../04-evaluations/docs/evaluation-model.md#purpose-and-evaluation-model) bound claims about requirements-derived acceptance.
- Evaluation evidence is specific to the environment exercised. The framework records the [limits of isolation and integration evidence](../04-evaluations/docs/framework-design.md#agent-execution).
