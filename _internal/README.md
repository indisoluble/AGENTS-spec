# AGENTS-spec internal engineering

`_internal/` holds engineering navigation and documentation governance behind the [AGENTS.md](../contract/prerelease_AGENTS.md) specification. Root `docs/` holds system-wide engineering documentation. The `requirements/` project owns the established product requirements and provisional requirement candidates and holds the temporary contract-design consolidation document. The `evaluations/` project holds behavioral evaluation, verification of its machinery, dependencies, and evaluation documentation. The contract, its tool bridges, and the guides for people adopting it are the five consumer artifacts staged exclusively at the `contract/` root with `prerelease_` filenames, starting with [README.md](../contract/prerelease_README.md).

[requirements/docs/product-requirements.md](../requirements/docs/product-requirements.md) owns the established objectives, PR1, and product constraints with their qualifications and provenance. [requirements/docs/requirement-candidates.md](../requirements/docs/requirement-candidates.md) owns provisional RC1–RC10 and their unresolved acceptance questions. [requirements/docs/architecture.md](../requirements/docs/architecture.md#current-semantics-vocabulary-and-coverage) owns the shared current-semantics vocabulary and contract-clause coverage index. [contract-design.md](../requirements/docs/contract-design.md) retains the remaining current binding design prescriptions, mechanisms, rationale, decisions, history, and classification and evidence. [requirements/](../requirements/README.md) provides domain navigation. The staged [AGENTS.md](../contract/prerelease_AGENTS.md) remains the self-contained normative runtime contract for consumers, not development instructions for this repository. [architecture.md](../docs/architecture.md#development-time-and-runtime-authority) explains authority boundaries and system relationships; [documentation-maintenance.md](docs/documentation-maintenance.md) owns editorial guidance.

This README is for orientation only. Each topic below links to the document that owns it; if this summary and a linked owner disagree, the owner is authoritative and this README needs correcting.

## Engineering responsibilities

| Responsibility | What it covers | Canonical documentation |
| --- | --- | --- |
| Product requirements | Desired collaboration outcomes and their reasons, applicable product constraints, and established versus provisional status. RC1–RC10 await developer acceptance. | [requirements/README.md](../requirements/README.md) is the domain entry point; [product-requirements.md](../requirements/docs/product-requirements.md) owns the established items; [requirement-candidates.md](../requirements/docs/requirement-candidates.md) owns provisional candidates |
| Specification design | How contract instructions express intended outcomes: current semantics, distinguishable rationale, design decisions, trade-offs, historical alternatives, and review scenarios. | [requirements/docs/architecture.md](../requirements/docs/architecture.md#current-semantics-vocabulary-and-coverage) owns shared vocabulary and the contract-clause coverage index; [requirements/docs/contract-design.md](../requirements/docs/contract-design.md) owns the remaining design |
| Behavioral evaluation and evaluator verification | A Python suite runs Codex in fresh workspaces with the unchanged current contract; automated assertions and human review assess selected behaviors. Offline tests verify the machinery; E1–E40 specify evaluator behavior, distinct from product requirements. Results are evidence about the exercised cases, not general compliance. | [evaluations/docs/evaluations.md](../evaluations/docs/evaluations.md) |
| Engineering architecture | Authority, responsibilities, boundaries, cross-domain dependencies, and system-wide decisions with an index of narrower decision records. | [docs/architecture.md](../docs/architecture.md) |
| Documentation maintenance | Canonical ownership and editorial guidance for all repository documentation, including the consumer guides. | [docs/documentation-maintenance.md](docs/documentation-maintenance.md) |

The current framework evaluates `contract/prerelease_AGENTS.md`, injected as workspace-root `AGENTS.md`, and its cases and review criteria cite contract clauses. Established product requirements guide development and intended evaluation expectations; explicit traceability is later work. The adopted contract depends on no internal engineering document or framework. Results enter human review and do not authorize changes to requirements, implementation, or expectations. [docs/architecture.md](../docs/architecture.md) owns these relationships; the documents above own their detail.

## Directory layout

| Path | Role |
| --- | --- |
| `../docs/` | System-wide engineering documentation: [architecture.md](../docs/architecture.md) owns authority, cross-domain relationships, principal boundaries, and system-wide engineering decisions. |
| `docs/` | [documentation-maintenance.md](docs/documentation-maintenance.md) remains the canonical owner of documentation ownership and editorial guidance across the whole repository, including the consumer guides. |
| `../contract/` | Exclusively the five staged consumer artifacts: the runtime contract, two provider bridges, and adoption and practical guides, all with `prerelease_` filenames. |
| `../requirements/` | The product-requirements home. Its [README.md](../requirements/README.md) provides responsibility boundaries, navigation, and remaining migration work; [docs/product-requirements.md](../requirements/docs/product-requirements.md) owns established objectives, PR1, and product constraints; [docs/requirement-candidates.md](../requirements/docs/requirement-candidates.md) owns provisional RC1–RC10 and unresolved acceptance questions; [docs/architecture.md](../requirements/docs/architecture.md#current-semantics-vocabulary-and-coverage) owns shared vocabulary and the contract-clause coverage index; [docs/contract-design.md](../requirements/docs/contract-design.md) is the temporary consolidation document retaining the remaining specification design, excluded from the intended consumer release. |
| `../evaluations/docs/` | Evaluation documentation: [evaluations.md](../evaluations/docs/evaluations.md) owns the evaluation framework guide, evaluator requirements E1–E40, and evaluation-specific engineering decisions. |
| `../evaluations/` | The evaluation project and Python package: its command-line entry point and case composition (`__main__.py`), shared execution, workspace, evidence, and grading infrastructure in `runtime/`, and one module per evaluation case in `scenarios/`. Run `python -m evaluations` from the repository root. [Responsibilities and dependency direction](../evaluations/docs/evaluations.md#responsibilities-and-dependency-direction) assigns each module's role. |
| `../evaluations/tests/` | The offline unittest suite, grouped by responsibility: `runtime/` for the shared machinery and cross-scenario CLI guarantees, `scenarios/` for one module per evaluation case, and `support/` for a fake Codex executable and CLI test harness that never contact OpenAI. The test root keeps an offline smoke substitute and an opt-in probe of the evaluator-owned functional-check sandbox, separate from the evaluated-agent permission profile. See [offline checks](../evaluations/docs/evaluations.md#run-offline-checks) and [functional-check execution](../evaluations/docs/evaluations.md#functional-check-execution). |
| [../evaluations/requirements.txt](../evaluations/requirements.txt) | The suite's Python dependency range. |
| `../.venv/` | Local virtual environment created during [setup](../evaluations/docs/evaluations.md#install-prerequisites); ignored by Git. Existing environments are not moved. |
| `../evaluations/.eval-runs/` | Evidence directories created by evaluation runs and kept after later runs; ignored by Git. Historical evidence under `_internal/.eval-runs/` remains in place. See [retained evidence](../evaluations/docs/evaluations.md#retained-evidence). |

## Where to find things

| To | Go to |
| --- | --- |
| Understand how specification design, evaluation, and documentation maintenance fit together, and how a contract change can affect evaluation | [architecture.md](../docs/architecture.md) |
| Distinguish intended requirements from runtime rules and find decision ownership | [Development-time and runtime authority](../docs/architecture.md#development-time-and-runtime-authority) and [Decisions](../docs/architecture.md#decisions) |
| Find established objectives, requirements and constraints, provisional candidates, and remaining requirements migration work | [Requirements entry point](../requirements/README.md) |
| Find the specification of current operating semantics | [Current-semantics vocabulary and coverage](../requirements/docs/architecture.md#current-semantics-vocabulary-and-coverage) |
| Understand what the suite evaluates and the limits of its results | [Purpose and evaluation model](../evaluations/docs/evaluations.md#purpose-and-evaluation-model) |
| Install prerequisites, authenticate, and run offline checks or cases | [Setup and running evaluations](../evaluations/docs/evaluations.md#setup-and-running-evaluations) |
| Read outcomes, retained evidence, and investigate a failure | [Results, evidence, and failure investigation](../evaluations/docs/evaluations.md#results-evidence-and-failure-investigation) |
| Look up a case's situation, assertions, and review interpretation | [Cases and interpretation](../evaluations/docs/evaluations.md#cases-and-interpretation); each case links to the module that owns its exact prompt, fixture, checks, and any rubric |
| Understand isolation, credentials, deadlines, and cleanup | [Execution and security boundaries](../evaluations/docs/evaluations.md#execution-and-security-boundaries) |
| Understand the framework's structure and how one run proceeds | [Architecture, extension, and maintenance](../evaluations/docs/evaluations.md#architecture-extension-and-maintenance) |
| Find accepted evaluation-specific decisions and their history | [Engineering decisions](../evaluations/docs/evaluations.md#engineering-decisions) |
| Learn how a scenario is built, run, and tested, starting from the Pydantic Evals concepts used | [Walkthrough: scope-discipline](../evaluations/docs/evaluations.md#walkthrough-scope-discipline) and [Pydantic Evals concepts used here](../evaluations/docs/evaluations.md#pydantic-evals-concepts-used-here) |
| Find the suite's requirements (E1–E40) and how each is verified | [Verifiable requirements](../evaluations/docs/evaluations.md#verifiable-requirements) |
| Change or add an evaluation case | [Modify or extend an evaluation](../evaluations/docs/evaluations.md#modify-or-extend-an-evaluation), then [verify a behavior change](../evaluations/docs/evaluations.md#verify-a-behavior-change) |
| Understand or assess a change to the contract's design | [contract-design.md](../requirements/docs/contract-design.md), especially [Evolving the contract](../requirements/docs/contract-design.md#evolving-the-contract) and [Assessing design changes](../requirements/docs/contract-design.md#assessing-design-changes) |
| Edit any documentation, including the consumer guides | [documentation-maintenance.md](docs/documentation-maintenance.md) |

## Getting started

To understand or maintain the evaluation framework:

1. Read the staged [README.md](../contract/prerelease_README.md) and [AGENTS.md](../contract/prerelease_AGENTS.md) to learn what is being evaluated, and [architecture.md](../docs/architecture.md) for how the framework relates to the specification.
2. Read the [purpose and evaluation model](../evaluations/docs/evaluations.md#purpose-and-evaluation-model).
3. Follow [install prerequisites](../evaluations/docs/evaluations.md#install-prerequisites) and [run the offline checks](../evaluations/docs/evaluations.md#run-offline-checks). They need no login and use no subscription allowance; live runs do, as [Run a case or the suite](../evaluations/docs/evaluations.md#run-a-case-or-the-suite) explains.
4. Read the [architecture](../evaluations/docs/evaluations.md#architecture-extension-and-maintenance), then the [cases](../evaluations/docs/evaluations.md#cases-and-interpretation) and modules relevant to your work.

To work on the contract itself, read the [authority model](../docs/architecture.md#development-time-and-runtime-authority), then the reading guidance at the top of [contract-design.md](../requirements/docs/contract-design.md). For the published semantics of edits to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`, see the candidate contract's [protected-file rule](../contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions).

## Documentation ownership

Each kind of knowledge has one canonical owner. [Document ownership](docs/documentation-maintenance.md#document-ownership) states what each document owns, and [documentation-maintenance.md](docs/documentation-maintenance.md) holds the editing workflow and checks for keeping documents consistent.

This README is the engineering entry point. Staged consumer files at the `contract/` root contain no references or dependencies into engineering documentation, including optional navigation; engineering documents may reference those staged files. The [accepted boundary decision](../docs/architecture.md#requirements-led-engineering-and-productinternal-separation) records the scoped application of §3.6, with each README identifying documentation for its own audience.

The staged [README.md](../contract/prerelease_README.md) (an accessible introduction for potential adopters) and [README-powerusers.md](../contract/prerelease_README-powerusers.md) (detailed practical guidance for users) are user-facing. They may intentionally explain some of the same concepts at different depths, provided both stay consistent with `AGENTS.md` and neither defines competing rules. Internal engineering documents, including this README, apply ownership strictly: each detailed technical fact, requirement, procedure, or decision has one owner, and other documents summarize and link. [Public guides and internal engineering documents](docs/documentation-maintenance.md#public-guides-and-internal-engineering-documents) owns this distinction.
