# AGENTS-spec engineering architecture

This document explains how the internal engineering project behind [AGENTS.md](../03-contract/prerelease_AGENTS.md) fits together: why it exists, how its responsibilities relate, and where its principal boundaries lie. It owns the current system overview. [Authority and change propagation](authority-and-change.md) owns the detailed cross-domain authority, evidence, and dependency guidance; [engineering history](engineering-history.md) owns previous arrangements and system-wide decision records. Detailed knowledge stays with the documents listed in [where detailed knowledge lives](#where-detailed-knowledge-lives); this overview summarizes them only as far as the relationships require.

## Purpose and scope

The repository stages consumer artifacts at the `03-contract/` root with `prerelease_` filenames: the `AGENTS.md` contract and two instruction bridges, `CLAUDE.md` and `.github/copilot-instructions.md`, whose intended consumer locations are described in the [installation steps](../03-contract/prerelease_README.md#get-started). The staged [README.md](../03-contract/prerelease_README.md) and [README-powerusers.md](../03-contract/prerelease_README-powerusers.md) explain that specification to its users. These five files are the only contents of `03-contract/`; engineering documentation is excluded from this staging area.

### Current BDD-first organization

The [13 November 2026 architecture decision](engineering-history.md#bdd-first-reorganization-13-november-2026) organizes files by durable responsibility; the [numbered-pipeline successor](engineering-history.md#numbered-pipeline-and-documentation-ownership-15-november-2026) refines their placement and entry points. Numbering indicates conceptual progression, not mandatory sequential gates. BDD activities can revisit the same topic and cross several owners. An information owner is the canonical place to maintain a subject. Acceptance and change authority belong to the requester or an explicitly authorized delegate, not to a directory, activity, or evaluation result.

```text
/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── authority-and-change.md
│   └── engineering-history.md
├── 01-behavior/
│   ├── README.md
│   ├── baseline.md
│   ├── discovery.md
│   ├── docs/
│   │   └── candidate-and-example-history.md
│   └── proposed-examples/
│       ├── planning-and-scope.md
│       ├── authorization-and-communication.md
│       ├── bounded-inquiry.md
│       ├── validation-and-learning.md
│       ├── knowledge-and-documentation.md
│       ├── engineering-quality.md
│       └── self-contained-delivery.md
├── 02-design/
│   ├── README.md
│   ├── contract-design.md
│   ├── delivery-and-portability.md
│   ├── methods-and-references.md
│   ├── mechanisms/
│   │   ├── work-cycle-and-inquiry.md
│   │   ├── requester-decisions-and-reporting.md
│   │   ├── engineering-and-validation.md
│   │   └── knowledge-and-documentation.md
│   └── docs/
│       ├── design-review.md
│       └── decisions-and-alternatives.md
├── 03-contract/
│   ├── prerelease_AGENTS.md
│   ├── prerelease_CLAUDE.md
│   ├── prerelease_copilot-instructions.md
│   ├── prerelease_README.md
│   └── prerelease_README-powerusers.md
└── 04-evaluations/
    ├── README.md
    ├── requirements.txt
    ├── cases-and-requirements.md
    ├── docs/
    │   ├── evaluations.md
    │   ├── running-and-reviewing.md
    │   └── framework-design.md
    └── evaluations/
        ├── __init__.py
        ├── __main__.py
        ├── runtime/
        ├── scenarios/
        └── tests/
```

| Owner | Durable responsibility and entry point |
| --- | --- |
| `01-behavior/` | [Stage navigation](../01-behavior/README.md); [established objectives, PR1, constraints, and accepted behavior](../01-behavior/baseline.md); [proposal status, coverage, and open formulation questions](../01-behavior/discovery.md); [proposed example suites](../01-behavior/discovery.md#proposed-example-suites); [candidate and example history](../01-behavior/docs/candidate-and-example-history.md). Established intent and proposals keep separate status. |
| `02-design/` | [Stage navigation](../02-design/README.md); [contract architecture, vocabulary, and clause coverage](../02-design/contract-design.md), with [detailed mechanisms](../02-design/contract-design.md#crosscutting-concepts), [delivery](../02-design/delivery-and-portability.md), [methods and references](../02-design/methods-and-references.md), and [decisions and history](../02-design/docs/decisions-and-alternatives.md); [editorial guidance and the 28 non-normative design illustrations](../02-design/docs/design-review.md). Selected design authority is distinct from independent product acceptance. |
| `03-contract/` | Five staged consumer artifacts: the self-contained instructions, provider bridges, and adoption guides. Their [release-relative meanings](#staged-sources-and-release-relative-references) remain intact. |
| `04-evaluations/` | [Stage navigation](../04-evaluations/README.md); [evaluation model and navigation](../04-evaluations/docs/evaluations.md), with separate owners for [operations and evidence](../04-evaluations/docs/running-and-reviewing.md), [cases and evaluator requirements](../04-evaluations/cases-and-requirements.md), and [framework design](../04-evaluations/docs/framework-design.md). Scenario policy, runtime machinery, and offline tests live in the nested `evaluations/` package. Commands run from `04-evaluations/`; new evidence goes to its `.eval-runs/`. Retained evidence stays in its [documented locations](../04-evaluations/docs/running-and-reviewing.md#retained-evidence). |
| `docs/` | This current system overview; [shared authority, ownership, BDD interfaces, traceability, and change guidance](authority-and-change.md); [engineering history and system decisions](engineering-history.md). Detailed definitions remain with their domain owners. |

Start with the [project README](../README.md), then the relevant stage or the shared [BDD activities and authority](authority-and-change.md#bdd-activities-and-complementary-responsibilities). Knowledge maintenance remains cross-cutting. Consumer artifacts acquire no dependency on this engineering organization or on BDD.

## Current relationships and change guidance

Accepted product intent in `01-behavior/` guides contract design and intended evaluation expectations. `02-design/` explains the mechanisms implemented by the staged contract; `04-evaluations/` exercises that candidate and retains evidence for human review. The [traceability account](authority-and-change.md#cross-domain-traceability-and-feedback) distinguishes these relationships, their reverse paths, and the remaining requirements-to-evaluation gaps. Consumer artifacts remain independent of engineering documentation.

The following links lead to the canonical authority and change guidance:

- [BDD activities and complementary responsibilities](authority-and-change.md#bdd-activities-and-complementary-responsibilities)
- [Cross-domain traceability and feedback](authority-and-change.md#cross-domain-traceability-and-feedback)
- [Development-time and runtime authority](authority-and-change.md#development-time-and-runtime-authority)
- [Status and evidence boundaries](authority-and-change.md#status-and-evidence-boundaries)
- [What evaluation evidence can establish](authority-and-change.md#what-evaluation-evidence-can-establish)
- [Documentation ownership boundaries](authority-and-change.md#documentation-ownership-boundaries)
- [Specification-to-evaluation dependencies](authority-and-change.md#specification-to-evaluation-dependencies)
- [Change impact](authority-and-change.md#change-impact)

## Principal boundaries

| Boundary | What it separates | Detail |
| --- | --- | --- |
| Product intent and runtime implementation | Product requirements guide development; rationale explains design choices. `AGENTS.md` implements the intended behavior as the complete runtime contract. BR1–BR10 are accepted; their proposed examples and residual candidate detail retain separate status. Guides and examples cannot enact behavior. | [Development-time and runtime authority](authority-and-change.md#development-time-and-runtime-authority) |
| Product requirements and evaluator requirements | Product requirements concern intended agent behavior and product constraints. E1–E40 specify the suite's required behavior, including how cases are executed and assessed; they do not independently establish product intent. Fictional application requirements in fixtures concern those applications. | [Established product requirements](../01-behavior/baseline.md), [candidate history and disposition](../01-behavior/docs/candidate-and-example-history.md#disposition-of-the-earlier-candidates), [verifiable requirements](../04-evaluations/cases-and-requirements.md#verifiable-requirements) |
| Shared evaluation infrastructure and scenarios | Shared modules in `04-evaluations/evaluations/runtime/` have no dependency on individual scenarios. Each scenario module in `04-evaluations/evaluations/scenarios/` owns its prompt, fixture, assertions, any functional checks, and any human-review rubric. The CLI in `04-evaluations/evaluations/__main__.py` composes the two. | [Responsibilities and dependency direction](../04-evaluations/docs/framework-design.md#responsibilities-and-dependency-direction) |
| Execution, observation, grading, and human assessment | Agent commands use the restrictive permission profile for a disposable workspace. The parent Codex client and Python evaluator operate outside that command sandbox. Observations are captured outside the workspace; automated grading reads those observations, and human assessment uses the retained rubric and evidence. | [Purpose and evaluation model](../04-evaluations/docs/evaluations.md#purpose-and-evaluation-model), [execution and security boundaries](../04-evaluations/docs/framework-design.md#execution-and-security-boundaries) |
| Implementation and verification | The offline suite verifies configuration and orchestration with substitutes. The repository's sandbox probe checks only the evaluator-owned functional-check boundary. Agent-command enforcement and authenticated integration need separate environment-specific validation. | [Agent execution](../04-evaluations/docs/framework-design.md#agent-execution), [verify a behavior change](../04-evaluations/docs/framework-design.md#verify-a-behavior-change) |
| Evidence retention and interpretation | Evidence directories record what happened. Reports classify execution failures, assertion failures, and pending review separately. Interpretation stays tied to the captured contract and rubric. | [Results, evidence, and failure investigation](../04-evaluations/docs/running-and-reviewing.md#results-evidence-and-failure-investigation) |
| Product and internal engineering documentation | Staged consumer files remain independent of internal engineering documentation. Engineering documents give each detailed fact one owner; the consumer guides may overlap intentionally. | [Documentation ownership boundaries](authority-and-change.md#documentation-ownership-boundaries) |

### Staged sources and release-relative references

Engineering links to consumer sources target the staged files. Display names and adopting-project examples retain the intended published filenames:

| Staged source | Intended consumer location |
| --- | --- |
| `03-contract/prerelease_AGENTS.md` | `AGENTS.md` |
| `03-contract/prerelease_CLAUDE.md` | `CLAUDE.md` |
| `03-contract/prerelease_copilot-instructions.md` | `.github/copilot-instructions.md` |
| `03-contract/prerelease_README.md` | `README.md` |
| `03-contract/prerelease_README-powerusers.md` | `README-powerusers.md` |

The contract's standard instruction and documentation filenames describe adopting projects. Claude's `@AGENTS.md` import targets the eventual root contract, and Copilot's `../AGENTS.md` link resolves from the eventual `.github/` directory. These deliberate exceptions do not resolve from the staged files; they preserve release semantics rather than importing development instructions. The consumer README's license link points to the repository-root `LICENSE`.

The recorded provider check for nonstandard staging names is **November 8, 2026** ([Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code](https://code.claude.com/docs/en/memory), [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)); moving this guidance does not refresh that evidence. No repository instruction bridge imports the candidate for development. Explicit source reading and injection as `AGENTS.md` into isolated evaluation workspaces are separate uses, as the [authority model](authority-and-change.md#development-time-and-runtime-authority) explains.

## Where detailed knowledge lives

This architecture refines into the existing owners rather than replacing them:

- **Runtime normative behavior:** [AGENTS.md](../03-contract/prerelease_AGENTS.md), the complete operating contract.
- **Product intent and contract design:** [Behavior](../01-behavior/README.md) navigates accepted requirements, proposed examples, coverage, and remaining work; [Design](../02-design/README.md) navigates the selected contract specification and its supporting documents. Definitions and detailed rationale stay with their [behavior](../01-behavior/baseline.md), [design](../02-design/contract-design.md), and [design-review](../02-design/docs/design-review.md) owners.
- **Evaluation framework:** the [stage README](../04-evaluations/README.md) provides orientation; [evaluations.md](../04-evaluations/docs/evaluations.md) owns the evaluation model and entry navigation; [running and reviewing](../04-evaluations/docs/running-and-reviewing.md) owns operations, authentication, evidence, and failure investigation; [cases and requirements](../04-evaluations/cases-and-requirements.md) keeps the ten case definitions with E1–E40; [framework design](../04-evaluations/docs/framework-design.md) owns execution boundaries, architecture and lifecycle, maintenance, and decisions. Scenario modules own exact prompts, fixtures, assertions, checks, and rubrics.
- **Cross-domain authority and ownership:** [Authority and change propagation](authority-and-change.md) owns the [authority model](authority-and-change.md#development-time-and-runtime-authority), [documentation boundaries](authority-and-change.md#documentation-ownership-boundaries), and dependencies; [engineering history](engineering-history.md#decisions) owns system-wide decisions. [Shared editing guidance](authority-and-change.md#working-with-requirements-and-design-documentation) stays with authority and change; domain-specific review and maintenance guidance stays with the owners above.

## Historical context

For the arrangement preceding BDD-first organization, read the [Phase 1 responsibility account](engineering-history.md#historical-responsibility-arrangement-at-the-phase-1-baseline) and its [historical context graph and relationships](engineering-history.md#historical-context-graph-at-the-phase-1-baseline). These describe the former `requirements/` organization, not today's tree.

The [temporary migration-authority record](engineering-history.md#temporary-migration-authority) preserves the frozen-contract baseline, independent verification, and the requester's 8 November authority-transfer decision.

## Decisions

This index links complete records at their canonical owners. [Engineering history](engineering-history.md#decisions) owns system-wide records and their historical qualifications; [contract-design decisions and alternatives](../02-design/docs/decisions-and-alternatives.md#architecture-decisions) owns specification-design decisions and historical alternatives; [evaluation framework design](../04-evaluations/docs/framework-design.md#engineering-decisions) owns evaluation-subsystem decisions. Domain documentation links to those records rather than duplicating them.

| Decision | Scope and canonical record |
| --- | --- |
| [Restrictive evaluation-agent command permissions](../04-evaluations/docs/framework-design.md#restrictive-evaluation-agent-command-permissions) | Evaluation project. |
| [Integrated engineering architecture with focused detailed owners](engineering-history.md#integrated-engineering-architecture-with-focused-detailed-owners) | Engineering system; original rationale and subsequent refinements. |
| [Evaluation documentation by maintenance responsibility (15 November 2026)](../04-evaluations/docs/framework-design.md#evaluation-documentation-by-maintenance-responsibility-15-november-2026) | Narrow successor to the integrated evaluation-documentation layout; preserves case/requirement/evidence relationships and changes documentation layout only. |
| [Evaluation framework package and verification hierarchy](../04-evaluations/docs/framework-design.md#evaluation-framework-package-and-verification-hierarchy) | Evaluation project. |
| [Requirements-led engineering and product/internal separation](engineering-history.md#requirements-led-engineering-and-productinternal-separation) | Engineering system; authority, ownership, and product/internal separation. |
| [BDD-first reorganization (13 November 2026)](engineering-history.md#bdd-first-reorganization-13-november-2026) | Engineering system; approved responsibility owners, BDD interfaces, and Phase 1 preservation boundary. |
| [Shared engineering documentation extraction (15 November 2026)](engineering-history.md#shared-engineering-documentation-extraction-15-november-2026) | Structural successor for this three-document arrangement; remaining migrations are outside this step. |
| [Numbered pipeline and documentation ownership (15 November 2026)](engineering-history.md#numbered-pipeline-and-documentation-ownership-15-november-2026) | Engineering system; numbered responsibilities, concise entry points, local metadata, artifact-only Contract, and nested evaluation package. |
