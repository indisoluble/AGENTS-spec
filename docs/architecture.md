# AGENTS-spec engineering architecture

AGENTS-spec develops a reusable, self-contained [operating contract](../03-candidate/pre_AGENTS.md) for coding agents. Behavior establishes product intent, Design selects its realization, Candidate stages the consumer files, and Evaluations assess the candidate. This overview maps stage boundaries and owners. See [authority and change](authority-and-change.md) for change guidance and [system-wide engineering decisions](decisions.md) for rationale.

## Purpose and scope

Engineering documentation supports understanding, changing, and verifying the product. Consumer artifacts contain no references or dependencies back into it. The delivered `AGENTS.md` contains the complete runtime instructions; the bridges load or direct tools to it, and the two consumer guides explain adoption and use.

### Current BDD-first organization

**Objectives → Requirements → Mechanisms → AGENTS.md → Evaluations** spans four stages. Use the stage entry points for their deliverables and supporting documentation.

| Stage | Responsibility |
| --- | --- |
| [01 — Behavior](../01-behavior/README.md) | Owns objectives and their rationale, accepted requirements and constraints, and discovery of proposed examples. |
| [02 — Design](../02-design/README.md) | Selects mechanisms that realize accepted intent and records their rationale and relationship to contract clauses. |
| [03 — Candidate](../03-candidate/pre_AGENTS.md) | Stages the self-contained runtime instructions, two bridges, and two consumer guides. The [adoption guide](../03-candidate/pre_README.md) explains installation. |
| [04 — Evaluations](../04-evaluations/README.md) | Owns cases, evaluator requirements, and the framework that exercises a staged candidate and produces observations and evidence for review. |

Behavior, Design, and Evaluations each have three immediate entries: `README.md` for orientation, `docs/` for supporting explanations and maintenance knowledge, and `deliverables/` for substantive artifacts. Candidate is the exception: exactly five consumer files at its root, with no engineering README or container directories. Design prescriptions stay with their necessary rationale rather than being split by normative status.

Numbers show conceptual progression, not mandatory sequential gates. BDD Discovery, Formulation, and Automation iterate across these responsibility owners; knowledge maintenance spans them all. Directory ownership identifies where knowledge is maintained, not who can accept or authorize a change.

## Principal boundaries

Accepted intent guides both design and evaluation expectations. Design relates selected mechanisms to the staged contract; evaluations exercise an identified candidate and return findings for review. These are separate paths: implementation wording alone cannot establish intended behavior or an independent expected result. The [traceability model](authority-and-change.md#cross-domain-traceability-and-feedback) explains their links, feedback, and remaining coverage gaps.

The dependency runs from Evaluations to Candidate. Consumers can use the contract independently of the evaluator. A contract edit can affect both what the next run exercises and how its results should be assessed. See the shared [authority model](authority-and-change.md#development-time-and-runtime-authority) and [change-impact guidance](authority-and-change.md#change-impact).

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
