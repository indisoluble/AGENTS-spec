# AGENTS-spec engineering architecture

AGENTS-spec develops a reusable, self-contained [operating contract](../04-candidate/pre_AGENTS.md) for coding agents. This overview defines the five-stage engineering pipeline. Each stage maintains the substance of its own deliverables. See [authority and change](authority-and-change.md) for change guidance and [system-wide engineering decisions](decisions.md) for rationale.

## Purpose and scope

Engineering documentation supports understanding, changing, and verifying the product. Consumer artifacts contain no references or dependencies back into it. The delivered `AGENTS.md` contains the complete runtime instructions; the bridges load or direct tools to it, and the two consumer guides explain adoption and use.

## Stage interfaces

The mapping uses [Cucumber's three BDD practices](https://cucumber.io/docs/bdd/#three-practices). BDD leaves repository layout to the project. AGENTS-spec gives Discovery and Formulation distinct owners and divides Automation into mechanism selection, operational realization, and evaluation. The five stage directories are siblings. The grouping by practice is conceptual.

| BDD practice | Stage | Principal inputs | Principal outputs |
| --- | --- | --- | --- |
| Discovery | [`01-discovery/`](../01-discovery/README.md) | Requester needs, feedback, observations, existing knowledge | Objectives, rationale, proposals, exploratory examples, open questions |
| Formulation | [`02-formulation/`](../02-formulation/README.md) | Discovery deliverables and requester decisions | Precise accepted requirements, applicable constraints, defining behavioral examples |
| Automation | [`03-design/`](../03-design/README.md) | Accepted requirements and applicable constraints | Selected mechanisms, specifications, decisions and rationale |
| Automation | [`04-candidate/`](../04-candidate/) | Selected mechanisms and delivery constraints | Staged operational contract and supporting consumer artifacts |
| Automation | [`05-evaluations/`](../05-evaluations/README.md) | Behavioral specifications, evaluation criteria, identified candidate | Evaluation definitions, executable checks, observations, assessments and evidence |

Keep these interfaces explicit and limited to what each stage needs from its direct dependencies. Location confers no [acceptance status](authority-and-change.md#status-and-evidence-boundaries). Requirements define desired behavior. Design selects mechanisms to realize it, Candidate expresses those mechanisms as operational instructions, and Evaluations assesses resulting behavior. Delivered `AGENTS.md` retains its [normative, self-contained runtime authority](authority-and-change.md#development-time-and-runtime-authority) within the consumer tool's instruction hierarchy and permissions. During development it realizes intent established independently of the contract.

Formulation supplies accepted intent for independent expectations. The identified candidate supplies the instructions exercised in a run. The [traceability model](authority-and-change.md#cross-domain-traceability-and-feedback) distinguishes these paths and explains the current clause-based cases.

Numbers show conceptual progression. The [test-first iteration](authority-and-change.md#test-first-iteration) illustrates how Evaluations participates before and after realization, and how feedback can reopen work in any relevant stage.

## Documentation layout

Discovery, Formulation, Design, and Evaluations normally use this layout.

```text
<stage>/
├── README.md
├── deliverables/
└── docs/
```

The stage `README.md` explains purpose and interfaces and provides navigation. `deliverables/` holds canonical substantive outputs with their individual authority and status. `docs/` holds supporting architecture, rationale, decisions, transformation guidance, and maintenance knowledge. Rationale essential to interpreting a specification may stay with the specification. Root `docs/` owns shared engineering knowledge, including the pipeline, cross-stage interfaces, authority, traceability, and documentation conventions. The [existing conventions](authority-and-change.md#engineering-documentation-convention) govern arc42, Diátaxis, and ADRs, together with [canonical ownership and proportionate cross-references](authority-and-change.md#documentation-ownership-boundaries).

The [Candidate directory](../04-candidate/) contains exactly `pre_AGENTS.md`, `pre_CLAUDE.md`, `pre_copilot-instructions.md`, `pre_README.md`, and `pre_README-powerusers.md`. The five files occupy the directory directly, with no engineering README, `docs/`, or `deliverables/`. Consumer artifacts remain independent of engineering documentation, including its navigation. Their technical rationale belongs primarily in Design.

### Staged sources and release-relative references

Engineering links target the staged sources. Display names and adopting-project examples use the intended consumer filenames:

| Staged source in `04-candidate/` | Intended consumer location |
| --- | --- |
| `pre_AGENTS.md` | `AGENTS.md` |
| `pre_CLAUDE.md` | `CLAUDE.md` |
| `pre_copilot-instructions.md` | `.github/copilot-instructions.md` |
| `pre_README.md` | `README.md` |
| `pre_README-powerusers.md` | `README-powerusers.md` |

References to standard instruction and documentation filenames describe adopting projects. A bridge reference that fails from a staged file can resolve correctly at its installed location. The consumer README's license link targets the repository-root `LICENSE`. Check links against their intended locations. Design explains [bridge behavior](../03-design/deliverables/delivery-and-portability.md#why-the-bridges-differ) and [provider-specific instruction discovery](../03-design/deliverables/delivery-and-portability.md#discovery-of-staged-instruction-files).

## Architecture decisions

The [system-wide decision record](decisions.md#architecture-decisions) explains choices affecting multiple stages. [Design decisions and alternatives](../03-design/docs/decisions.md#architecture-decisions) and [evaluation framework decisions](../05-evaluations/docs/framework-design.md#architecture-decisions) retain their domain-specific reasons, alternatives, and successors. The [engineering authority and runtime contract decision](decisions.md#engineering-authority-and-the-runtime-contract) explains the basis for engineering ownership of requirements and design and the scope of the delivered contract's authority.

## Risks and technical debt

- Design records the [interpretation risks of accepted wording compromises](../03-design/deliverables/delivery-and-portability.md#current-wording-trade-offs).
- [Traceability gaps](authority-and-change.md#cross-domain-traceability-and-feedback) and [evaluation coverage limits](../05-evaluations/docs/evaluation-model.md#purpose-and-evaluation-model) bound claims about requirements-derived acceptance.
- Evaluation evidence is specific to the environment exercised. The framework records the [limits of isolation and integration evidence](../05-evaluations/docs/framework-design.md#agent-execution).
