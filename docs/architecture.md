# AGENTS-spec engineering architecture

This document explains how the internal engineering project behind [AGENTS.md](../contract/prerelease_AGENTS.md) fits together: why it exists, how its responsibilities relate, and where its principal boundaries lie. It owns the current system overview. [Authority and change propagation](authority-and-change.md) owns the detailed cross-domain authority, evidence, and dependency guidance; [engineering history](engineering-history.md) owns previous arrangements and system-wide decision records. Detailed knowledge stays with the documents listed in [where detailed knowledge lives](#where-detailed-knowledge-lives); this overview summarizes them only as far as the relationships require.

## Purpose and scope

The repository stages consumer artifacts at the `contract/` root with `prerelease_` filenames: the `AGENTS.md` contract and two instruction bridges, `CLAUDE.md` and `.github/copilot-instructions.md`, whose intended consumer locations are described in the [installation steps](../contract/prerelease_README.md#get-started). The staged [README.md](../contract/prerelease_README.md) and [README-powerusers.md](../contract/prerelease_README-powerusers.md) explain that specification to its users. These five files are the only contents of `contract/`; engineering documentation is excluded from this staging area.

### Current BDD-first organization

The [13 November 2026 architecture decision](engineering-history.md#bdd-first-reorganization-13-november-2026) organizes files by durable responsibility. BDD activities can revisit the same topic and cross several owners; directories are not sequential stage gates. An information owner is the canonical place to maintain a subject. Acceptance and change authority belong to the requester or an explicitly authorized delegate, not to a directory, activity, or evaluation result.

```text
/
├── .gitignore
├── LICENSE
├── behavior/
│   ├── README.md
│   ├── baseline.md
│   └── discovery.md
├── design/
│   ├── contract-design.md
│   ├── design-review.md
│   ├── delivery-and-portability.md
│   ├── methods-and-references.md
│   ├── decisions-and-alternatives.md
│   └── mechanisms/
│       ├── work-cycle-and-inquiry.md
│       ├── requester-decisions-and-reporting.md
│       ├── engineering-and-validation.md
│       └── knowledge-and-documentation.md
├── contract/
│   ├── prerelease_AGENTS.md
│   ├── prerelease_CLAUDE.md
│   ├── prerelease_copilot-instructions.md
│   ├── prerelease_README.md
│   └── prerelease_README-powerusers.md
├── docs/
│   ├── architecture.md
│   ├── authority-and-change.md
│   └── engineering-history.md
└── evaluations/
    ├── __init__.py
    ├── __main__.py
    ├── requirements.txt
    ├── docs/evaluations.md
    ├── runtime/
    ├── scenarios/
    └── tests/
```

| Owner | Durable responsibility and entry point |
| --- | --- |
| `behavior/` | [Navigation and editing](../behavior/README.md); [established objectives, PR1, constraints, and accepted behavior](../behavior/baseline.md); [proposed acceptance examples, coverage, historical candidates, and open formulation questions](../behavior/discovery.md). Established intent and proposals keep separate status. |
| `design/` | [Contract architecture, vocabulary, and clause coverage](../design/contract-design.md), with [detailed mechanisms](../design/contract-design.md#crosscutting-concepts), [delivery](../design/delivery-and-portability.md), [methods and references](../design/methods-and-references.md), and [decisions and history](../design/decisions-and-alternatives.md); [editorial guidance and the 28 non-normative design illustrations](../design/design-review.md). Selected design authority is distinct from independent product acceptance. |
| `contract/` | Five staged consumer artifacts: the self-contained instructions, provider bridges, and adoption guides. Their [release-relative meanings](#staged-sources-and-release-relative-references) remain intact. |
| `evaluations/` | [Evaluator requirements, operational expectations, cases, evidence interpretation, and operations](../evaluations/docs/evaluations.md), with scenario policy, runtime machinery, and offline tests at their existing paths. Retained evidence stays in its [documented locations](../evaluations/docs/evaluations.md#retained-evidence). |
| `docs/` | This current system overview; [shared authority, ownership, BDD interfaces, traceability, and change guidance](authority-and-change.md); [engineering history and system decisions](engineering-history.md). Detailed definitions remain with their domain owners. |

Start an objective, question, design concern, or evaluation finding through [behavior navigation](../behavior/README.md#starting-a-bdd-topic). Knowledge maintenance remains cross-cutting. Consumer artifacts acquire no dependency on this engineering organization or on BDD.

## Current relationships and change guidance

Accepted product intent in `behavior/` guides contract design and intended evaluation expectations. `design/` explains the mechanisms implemented by the staged contract; `evaluations/` exercises that candidate and retains evidence for human review. The [traceability account](authority-and-change.md#cross-domain-traceability-and-feedback) distinguishes these relationships, their reverse paths, and the remaining requirements-to-evaluation gaps. Consumer artifacts remain independent of engineering documentation.

The following links lead to the canonical guidance. Anchors retain known incoming references and the published specification-to-evaluation dependency entry without duplicating the moved explanations.

| Canonical guidance |
| --- |
| <a id="bdd-activities-and-complementary-responsibilities"></a>[BDD activities and complementary responsibilities](authority-and-change.md#bdd-activities-and-complementary-responsibilities) |
| <a id="cross-domain-traceability-and-feedback"></a>[Cross-domain traceability and feedback](authority-and-change.md#cross-domain-traceability-and-feedback) |
| <a id="development-time-and-runtime-authority"></a>[Development-time and runtime authority](authority-and-change.md#development-time-and-runtime-authority) |
| <a id="status-and-evidence-boundaries"></a>[Status and evidence boundaries](authority-and-change.md#status-and-evidence-boundaries) |
| <a id="what-evaluation-evidence-can-establish"></a>[What evaluation evidence can establish](authority-and-change.md#what-evaluation-evidence-can-establish) |
| <a id="documentation-ownership-boundaries"></a>[Documentation ownership boundaries](authority-and-change.md#documentation-ownership-boundaries) |
| <a id="specification-to-evaluation-dependencies"></a>[Specification-to-evaluation dependencies](authority-and-change.md#specification-to-evaluation-dependencies) |
| <a id="change-impact"></a>[Change impact](authority-and-change.md#change-impact) |

## Principal boundaries

| Boundary | What it separates | Detail |
| --- | --- | --- |
| Product intent and runtime implementation | Product requirements guide development; rationale explains design choices. `AGENTS.md` implements the intended behavior as the complete runtime contract. BR1–BR10 are accepted; their proposed examples and residual candidate detail retain separate status. Guides and examples cannot enact behavior. | [Development-time and runtime authority](authority-and-change.md#development-time-and-runtime-authority) |
| Product requirements and evaluator requirements | Product requirements concern intended agent behavior and product constraints. E1–E40 specify the suite's required behavior, including how cases are executed and assessed; they do not independently establish product intent. Fictional application requirements in fixtures concern those applications. | [Established product requirements](../behavior/baseline.md), [candidate history and disposition](../behavior/discovery.md#disposition-of-the-earlier-candidates), [verifiable requirements](../evaluations/docs/evaluations.md#verifiable-requirements) |
| Shared evaluation infrastructure and scenarios | Shared modules in `evaluations/runtime/` have no dependency on individual scenarios. Each scenario module in `evaluations/scenarios/` owns its prompt, fixture, assertions, any functional checks, and any human-review rubric. The CLI in `evaluations/__main__.py` composes the two. | [Responsibilities and dependency direction](../evaluations/docs/evaluations.md#responsibilities-and-dependency-direction) |
| Execution, observation, grading, and human assessment | Agent commands use the restrictive permission profile for a disposable workspace. The parent Codex client and Python evaluator operate outside that command sandbox. Observations are captured outside the workspace; automated grading reads those observations, and human assessment uses the retained rubric and evidence. | [Purpose and evaluation model](../evaluations/docs/evaluations.md#purpose-and-evaluation-model), [execution and security boundaries](../evaluations/docs/evaluations.md#execution-and-security-boundaries) |
| Implementation and verification | The offline suite verifies configuration and orchestration with substitutes. The repository's sandbox probe checks only the evaluator-owned functional-check boundary. Agent-command enforcement and authenticated integration need separate environment-specific validation. | [Agent execution](../evaluations/docs/evaluations.md#agent-execution), [verify a behavior change](../evaluations/docs/evaluations.md#verify-a-behavior-change) |
| Evidence retention and interpretation | Evidence directories record what happened. Reports classify execution failures, assertion failures, and pending review separately. Interpretation stays tied to the captured contract and rubric. | [Results, evidence, and failure investigation](../evaluations/docs/evaluations.md#results-evidence-and-failure-investigation) |
| Product and internal engineering documentation | Staged consumer files remain independent of internal engineering documentation. Engineering documents give each detailed fact one owner; the consumer guides may overlap intentionally. | [Documentation ownership boundaries](authority-and-change.md#documentation-ownership-boundaries) |

### Staged sources and release-relative references

Engineering links to consumer sources target the staged files. Display names and adopting-project examples retain the intended published filenames:

| Staged source | Intended consumer location |
| --- | --- |
| `contract/prerelease_AGENTS.md` | `AGENTS.md` |
| `contract/prerelease_CLAUDE.md` | `CLAUDE.md` |
| `contract/prerelease_copilot-instructions.md` | `.github/copilot-instructions.md` |
| `contract/prerelease_README.md` | `README.md` |
| `contract/prerelease_README-powerusers.md` | `README-powerusers.md` |

The contract's standard instruction and documentation filenames describe adopting projects. Claude's `@AGENTS.md` import targets the eventual root contract, and Copilot's `../AGENTS.md` link resolves from the eventual `.github/` directory. These deliberate exceptions do not resolve from the staged files; they preserve release semantics rather than importing development instructions. The consumer README's license link points to the repository-root `LICENSE`.

The recorded provider check for nonstandard staging names is **November 8, 2026** ([Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code](https://code.claude.com/docs/en/memory), [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)); moving this guidance does not refresh that evidence. No repository instruction bridge imports the candidate for development. Explicit source reading and injection as `AGENTS.md` into isolated evaluation workspaces are separate uses, as the [authority model](authority-and-change.md#development-time-and-runtime-authority) explains.

## Where detailed knowledge lives

This architecture refines into the existing owners rather than replacing them:

- **Runtime normative behavior:** [AGENTS.md](../contract/prerelease_AGENTS.md), the complete operating contract.
- **Product intent and contract design:** [behavior/README.md](../behavior/README.md) navigates accepted requirements, proposed examples and coverage, historical candidates, operating-contract architecture, design review, and remaining requirements work. Definitions, detailed rationale, and editorial checks stay with their [behavior](../behavior/baseline.md), [design](../design/contract-design.md), and [design-review](../design/design-review.md) owners.
- **Evaluation framework:** [evaluations.md](../evaluations/docs/evaluations.md): evaluation model, operations and authentication, evidence and failure investigation, cases, execution boundaries, framework architecture and lifecycle, and E1–E40. Scenario modules own exact prompts, fixtures, checks, and rubrics.
- **Cross-domain authority and ownership:** [Authority and change propagation](authority-and-change.md) owns the [authority model](authority-and-change.md#development-time-and-runtime-authority), [documentation boundaries](authority-and-change.md#documentation-ownership-boundaries), and dependencies; [engineering history](engineering-history.md#decisions) owns system-wide decisions. Detailed editorial guidance stays with the domains above.

## Historical context

For the arrangement preceding BDD-first organization, read the <a id="historical-responsibility-arrangement-at-the-phase-1-baseline"></a>[Phase 1 responsibility account](engineering-history.md#historical-responsibility-arrangement-at-the-phase-1-baseline) and its <a id="historical-context-graph-at-the-phase-1-baseline"></a>[historical context graph and relationships](engineering-history.md#historical-context-graph-at-the-phase-1-baseline). These describe the former `requirements/` organization, not today's tree.

<a id="temporary-migration-authority"></a>
The [temporary migration-authority record](engineering-history.md#temporary-migration-authority) preserves the frozen-contract baseline, independent verification, and the requester's 8 November authority-transfer decision.

## Decisions

This index links complete records at their canonical owners. [Engineering history](engineering-history.md#decisions) owns system-wide records and their historical qualifications; [contract-design decisions and alternatives](../design/decisions-and-alternatives.md#architecture-decisions) owns specification-design decisions and historical alternatives; [the evaluation guide](../evaluations/docs/evaluations.md#engineering-decisions) owns evaluation-subsystem decisions. Domain documentation links to those records rather than duplicating them. Named decision anchors, including the earlier evaluation-record forwarding anchors, remain available here.

| Decision | Scope and canonical record |
| --- | --- |
| <a id="restrictive-evaluation-agent-command-permissions"></a>[Restrictive evaluation-agent command permissions](../evaluations/docs/evaluations.md#restrictive-evaluation-agent-command-permissions) | Evaluation project. |
| <a id="integrated-engineering-architecture-with-focused-detailed-owners"></a>[Integrated engineering architecture with focused detailed owners](engineering-history.md#integrated-engineering-architecture-with-focused-detailed-owners) | Engineering system; original rationale and subsequent refinements. |
| <a id="evaluation-framework-package-and-verification-hierarchy"></a>[Evaluation framework package and verification hierarchy](../evaluations/docs/evaluations.md#evaluation-framework-package-and-verification-hierarchy) | Evaluation project. |
| <a id="requirements-led-engineering-and-productinternal-separation"></a>[Requirements-led engineering and product/internal separation](engineering-history.md#requirements-led-engineering-and-productinternal-separation) | Engineering system; authority, ownership, and product/internal separation. |
| <a id="bdd-first-reorganization-13-november-2026"></a>[BDD-first reorganization (13 November 2026)](engineering-history.md#bdd-first-reorganization-13-november-2026) | Engineering system; approved responsibility owners, BDD interfaces, and Phase 1 preservation boundary. |
| [Shared engineering documentation extraction (15 November 2026)](engineering-history.md#shared-engineering-documentation-extraction-15-november-2026) | Structural successor for this three-document arrangement; remaining migrations are outside this step. |
