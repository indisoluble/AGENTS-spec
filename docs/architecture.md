# AGENTS-spec engineering architecture

AGENTS-spec develops a reusable, self-contained [operating contract](../03-candidate/pre_AGENTS.md) for coding agents. This overview defines the implemented pipeline and the approved target, which is pending migration. Each stage maintains the substance of its own deliverables. See [authority and change](authority-and-change.md) for change guidance and [system-wide engineering decisions](decisions.md) for rationale.

## Purpose and scope

Engineering documentation supports understanding, changing, and verifying the product. Consumer artifacts contain no references or dependencies back into it. The delivered `AGENTS.md` contains the complete runtime instructions; the bridges load or direct tools to it, and the two consumer guides explain adoption and use.

## Implemented four-stage architecture

**Objectives → Requirements → Mechanisms → Candidate AGENTS.md → Evaluations** spans four stages. Behavior owns the first two steps and houses both Discovery and Formulation. Contributors can start at any stage and revisit another when a finding calls its premises into question. Knowledge maintenance spans all four.

Behavior, Design, and Evaluations place their outputs in `deliverables/`. Their READMEs locate those outputs and the supporting knowledge in each stage's `docs/`. Candidate contains only the five [staged consumer artifacts](#staged-sources-and-release-relative-references). The [stage layout decision](decisions.md#stage-deliverables-and-the-candidate-staging-exception) explains why.

### Stage interfaces

Use the row for the stage you are working in. Its inputs can constrain a decision or supply evidence for one. The [authority and status of each source](authority-and-change.md#development-time-and-runtime-authority) determine which choices are open.

| Stage | Inputs used | Outputs owned here | What others use |
| --- | --- | --- | --- |
| [Behavior](../01-behavior/README.md) | Requester direction, established constraints, proposals, and feedback about unclear or unmet intent | [Objectives and rationale](../01-behavior/deliverables/objectives-and-rationale.md), [requirements baseline](../01-behavior/deliverables/baseline.md), and [Discovery proposals and questions](../01-behavior/deliverables/discovery.md) | Design and Evaluations use accepted intent and applicable constraints. Discovery exposes open questions and examples for review with their proposal status. |
| [Design](../02-design/README.md) | Accepted intent, applicable constraints, and existing design decisions | Mechanism specifications with their rationale and limits, and [records of decisions and alternatives](../02-design/docs/decisions.md) | Candidate uses the selected mechanisms. The [contract clause index](../02-design/deliverables/contract-design.md#contract-clause-index) connects clauses to their specifications and supported intent. |
| [Candidate](../03-candidate/) | Selected design, delivery constraints, and the existing staged text | The [staged contract](../03-candidate/pre_AGENTS.md), two bridges, and two consumer guides | Consumers use the delivered package. The evaluator exercises an identified version of the contract. Engineering trace links stay outside the package. |
| [Evaluations](../04-evaluations/README.md) | The candidate under test, case conditions, and the basis for the expected result | [Case specifications and evaluator requirements](../04-evaluations/README.md#case-specifications), the framework, and the evidence it produces | Reviewers compare [observations and results](../04-evaluations/docs/running-and-reviewing.md#results-evidence-and-failure-investigation) with the case criteria to identify what was exercised and which owner can address a finding. |

In requirements-led evaluation, the accepted baseline in Behavior supplies intent for the independent expectation. Candidate supplies the instructions given to the agent under observation. The [traceability and feedback model](authority-and-change.md#cross-domain-traceability-and-feedback) explains how to retain both paths and how to interpret the current clause-based cases. Consumers can use the contract independently of the evaluator.

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

## Approved five-stage target

The requester approved this architecture and authorized documenting it. The [decision record](decisions.md#five-stage-bdd-aligned-engineering-pipeline) gives the scope of that approval. Use the [implemented interfaces](#stage-interfaces) for current navigation and operations.

```text
/
├── README.md
├── docs/
├── 01-discovery/
├── 02-formulation/
├── 03-design/
├── 04-candidate/
└── 05-evaluations/
```

### Target stage interfaces

The mapping uses [Cucumber's three BDD practices](https://cucumber.io/docs/bdd/#three-practices). BDD leaves repository layout to the project. AGENTS-spec gives Discovery and Formulation distinct owners and divides Automation into mechanism selection, operational realization, and evaluation. The five stage directories are siblings. The grouping by practice is conceptual.

| BDD practice | Target stage | Principal inputs | Principal outputs |
| --- | --- | --- | --- |
| Discovery | `01-discovery/` | Requester needs, feedback, observations, existing knowledge | Objectives, rationale, proposals, exploratory examples, open questions |
| Formulation | `02-formulation/` | Discovery deliverables and requester decisions | Precise accepted requirements, applicable constraints, defining behavioral examples |
| Automation | `03-design/` | Accepted requirements and applicable constraints | Selected mechanisms, specifications, decisions and rationale |
| Automation | `04-candidate/` | Selected mechanisms and delivery constraints | Staged operational contract and supporting consumer artifacts |
| Automation | `05-evaluations/` | Behavioral specifications, evaluation criteria, identified candidate | Evaluation definitions, executable checks, observations, assessments and evidence |

Keep these interfaces explicit and limited to what each stage needs from its direct dependencies. The table defines responsibilities and leaves individual artifact allocation to migration analysis. Location confers no [acceptance status](authority-and-change.md#status-and-evidence-boundaries). Requirements define desired behavior. Design selects mechanisms to realize it, Candidate expresses those mechanisms as operational instructions, and Evaluations assesses resulting behavior. Delivered `AGENTS.md` retains its [normative, self-contained runtime authority](authority-and-change.md#development-time-and-runtime-authority) within the consumer tool's instruction hierarchy and permissions. During development it realizes intent established independently of the contract.

Numbers show conceptual progression. The [test-first iteration](authority-and-change.md#test-first-iteration) illustrates how Evaluations participates before and after realization, and how feedback can reopen work in any relevant stage.

### Target documentation layout

Discovery, Formulation, Design, and Evaluations normally use this layout.

```text
<stage>/
├── README.md
├── deliverables/
└── docs/
```

The stage `README.md` explains purpose and interfaces and provides navigation. `deliverables/` holds canonical substantive outputs with their individual authority and status. `docs/` holds supporting architecture, rationale, decisions, transformation guidance, and maintenance knowledge. Rationale essential to interpreting a specification may stay with the specification. Root `docs/` owns shared engineering knowledge, including the pipeline, cross-stage interfaces, authority, traceability, and documentation conventions. The [existing conventions](authority-and-change.md#engineering-documentation-convention) govern arc42, Diátaxis, and ADRs, together with [canonical ownership and proportionate cross-references](authority-and-change.md#documentation-ownership-boundaries).

The target `04-candidate/` contains exactly `pre_AGENTS.md`, `pre_CLAUDE.md`, `pre_copilot-instructions.md`, `pre_README.md`, and `pre_README-powerusers.md`. The five files occupy the directory directly, with no engineering README, `docs/`, or `deliverables/`. Consumer artifacts remain independent of engineering documentation, including its navigation. Their technical rationale belongs primarily in Design.

## Migration from the implemented layout

| Implemented directory | Target directory |
| --- | --- |
| `01-behavior/` | `01-discovery/` and `02-formulation/` |
| `02-design/` | `03-design/` |
| `03-candidate/` | `04-candidate/` |
| `04-evaluations/` | `05-evaluations/` |

The Discovery/Formulation split is the only substantial new ownership boundary. The other three stages retain their technical responsibilities. Migration and verification remain future work under the [scope of the decision](decisions.md#five-stage-bdd-aligned-engineering-pipeline).

- **Behavior allocation.** Review the objectives and rationale map, the accepted baseline, the proposed examples and coverage matrix, and the candidate and example history by substantive ownership. Mixed material includes requirement rationale and links to both provisional proposals and accepted outcomes. The file boundaries and locations of shared provenance remain to be settled. Preserve IDs, source relationships, and acceptance status.
- **Repository references.** Follow affected Markdown links, heading fragments, navigation labels, and plain-text paths, including Python docstrings. Update documented commands and working-directory assumptions for the renamed evaluator stage. Check consumer references in the [intended installed context](#staged-sources-and-release-relative-references) and verify all five staged files byte for byte.
- **Evaluator paths.** Keep the `deliverables` [Python package](decisions.md#stage-deliverables-and-the-candidate-staging-exception). Verify `python -m deliverables`, package-qualified imports and mock targets, offline test discovery, and subprocess working directories from the new stage root. The [runtime candidate lookup](../04-evaluations/deliverables/runtime/workspace.py) and [smoke-test assertion](../04-evaluations/deliverables/tests/scenarios/test_smoke.py) name `03-candidate/` directly. Check fixture setup, candidate injection, and path resolution for test helpers without changing evaluator behavior or fixture contents.
- **Evidence paths.** The [runner](../04-evaluations/deliverables/__main__.py) derives `.eval-runs/` from its stage root, so new runs would use `05-evaluations/.eval-runs/` after migration. Account for existing local bundles and [documented historical locations](../04-evaluations/docs/running-and-reviewing.md#retained-evidence). The inventory and handling of retained bundles across checkouts remain migration questions. Preserve their recorded paths, candidate identity, criteria, and interpretation.

## Architecture decisions

The [system-wide decision record](decisions.md#architecture-decisions) explains choices affecting multiple stages. [Design decisions and alternatives](../02-design/docs/decisions.md#architecture-decisions) and [evaluation framework decisions](../04-evaluations/docs/framework-design.md#architecture-decisions) retain their domain-specific reasons, alternatives, and successors. The [engineering authority and runtime contract decision](decisions.md#engineering-authority-and-the-runtime-contract) explains the basis for engineering ownership of requirements and design and the scope of the delivered contract's authority.

## Risks and technical debt

- Design records the [interpretation risks of accepted wording compromises](../02-design/deliverables/delivery-and-portability.md#current-wording-trade-offs).
- [Traceability gaps](authority-and-change.md#cross-domain-traceability-and-feedback) and [evaluation coverage limits](../04-evaluations/docs/evaluation-model.md#purpose-and-evaluation-model) bound claims about requirements-derived acceptance.
- Evaluation evidence is specific to the environment exercised. The framework records the [limits of isolation and integration evidence](../04-evaluations/docs/framework-design.md#agent-execution).
