# AGENTS-spec internal engineering

`_internal/` holds the engineering work behind the [AGENTS.md](../AGENTS.md) specification: product requirements and design rationale, behavioral evaluation and verification of its machinery, engineering architecture, and documentation governance. The contract, its tool bridges, and the guides for people adopting it live at the repository root, starting with [README.md](../README.md).

Stage 2 restructuring and classification, Remediation Step 1, and the [current-semantic specification](docs/contract-design.md#current-semantics-vocabulary-and-coverage) in Remediation Step 2 are complete. The independent Step 2 semantic review returned PASS. Step 3 cross-document reconciliation is the present stage, with its independent review and Step 4 final migration verification, including evaluation relationship checks, still pending. The [temporary migration authority](docs/architecture.md#temporary-migration-authority) records these milestones: frozen `AGENTS.md` authority remains active, and explicit engineering authority transfer is pending. Future product-requirement acceptance and authorized redesign remain separate work.

The root [AGENTS.md](../AGENTS.md) is the self-contained normative product contract. Product requirements, accepted engineering decisions, and requester direction guide its evolution. Agents maintaining this repository may receive it through provider-specific instruction-loading mechanisms; when loaded, its applicable instructions govern their conduct within the actual instruction hierarchy and tool permissions. This current arrangement is not a permanent architectural requirement. [Development-time and runtime authority](docs/architecture.md#development-time-and-runtime-authority) owns these distinctions and their operational limits.

This README is for orientation only. Each topic below links to the document that owns it; if this summary and a linked owner disagree, the owner is authoritative and this README needs correcting.

## Engineering responsibilities

| Responsibility | What it covers | Canonical documentation |
| --- | --- | --- |
| Product requirements and specification design | The complete engineering specification of current frozen semantics alongside intended agent behavior, product constraints, distinguishable rationale, design decisions, trade-offs, and review scenarios. RC1–RC10 remain provisional enduring product-requirement candidates awaiting acceptance. | [docs/contract-design.md](docs/contract-design.md), the designated future authoritative engineering source |
| Behavioral evaluation and evaluator verification | A Python suite runs Codex in fresh workspaces with the unchanged current contract; automated assertions and human review assess selected behaviors. Offline tests verify the machinery; E1–E40 specify evaluator behavior, distinct from product requirements. Results are evidence about the exercised cases, not general compliance. | [docs/evaluations.md](docs/evaluations.md) |
| Engineering architecture | Authority, responsibilities, boundaries, cross-domain dependencies, and system-wide decisions with an index of narrower decision records. | [docs/architecture.md](docs/architecture.md) |
| Documentation maintenance | Canonical ownership and editorial guidance for all repository documentation, including the root guides. | [docs/documentation-maintenance.md](docs/documentation-maintenance.md) |

The current framework evaluates the root `AGENTS.md`, and its cases and review criteria cite contract clauses. Established product requirements guide development and intended evaluation expectations; explicit traceability is later work. The adopted contract depends on no internal engineering document or framework. Results enter human review and do not authorize changes to requirements, implementation, or expectations. [docs/architecture.md](docs/architecture.md) owns these relationships; the documents above own their detail.

## Directory layout

| Path | Role |
| --- | --- |
| `docs/` | Internal engineering documentation: [architecture.md](docs/architecture.md) for the integrated engineering architecture, [contract-design.md](docs/contract-design.md) and [evaluations.md](docs/evaluations.md) for specification design and the evaluation framework, and [documentation-maintenance.md](docs/documentation-maintenance.md) for documentation ownership and editorial guidance across the whole repository, including the root guides. |
| `evals/` | The evaluation package: its command-line entry point and case composition (`__main__.py`), shared execution, workspace, evidence, and grading infrastructure in `runtime/`, and one module per evaluation case in `scenarios/`. [Responsibilities and dependency direction](docs/evaluations.md#responsibilities-and-dependency-direction) assigns each module's role. |
| `tests/` | The offline unittest suite, grouped by responsibility: `runtime/` for the shared machinery and cross-scenario CLI guarantees, `scenarios/` for one module per evaluation case, and `support/` for a fake Codex executable and CLI test harness that never contact OpenAI. The root keeps an offline smoke substitute and an opt-in probe of the evaluator-owned functional-check sandbox, separate from the evaluated-agent permission profile. See [offline checks](docs/evaluations.md#run-offline-checks) and [functional-check execution](docs/evaluations.md#functional-check-execution). |
| [requirements.txt](requirements.txt) | The suite's Python dependency range. |
| `.venv/` | Local virtual environment created during [setup](docs/evaluations.md#install-prerequisites); ignored by Git. |
| `.eval-runs/` | Evidence directories created by evaluation runs and kept after later runs; ignored by Git. See [retained evidence](docs/evaluations.md#retained-evidence). |

## Where to find things

| To | Go to |
| --- | --- |
| Understand how specification design, evaluation, and documentation maintenance fit together, and how a contract change can affect evaluation | [architecture.md](docs/architecture.md) |
| Distinguish intended requirements from runtime rules and find decision ownership | [Development-time and runtime authority](docs/architecture.md#development-time-and-runtime-authority) and [Decisions](docs/architecture.md#decisions) |
| Find the migration status and the completed specification of current operating semantics | [Temporary migration authority](docs/architecture.md#temporary-migration-authority) and [Current-semantics vocabulary and coverage](docs/contract-design.md#current-semantics-vocabulary-and-coverage) |
| Understand what the suite evaluates and the limits of its results | [Purpose and evaluation model](docs/evaluations.md#purpose-and-evaluation-model) |
| Install prerequisites, authenticate, and run offline checks or cases | [Setup and running evaluations](docs/evaluations.md#setup-and-running-evaluations) |
| Read outcomes, retained evidence, and investigate a failure | [Results, evidence, and failure investigation](docs/evaluations.md#results-evidence-and-failure-investigation) |
| Look up a case's situation, assertions, and review interpretation | [Cases and interpretation](docs/evaluations.md#cases-and-interpretation); each case links to the module that owns its exact prompt, fixture, checks, and any rubric |
| Understand isolation, credentials, deadlines, and cleanup | [Execution and security boundaries](docs/evaluations.md#execution-and-security-boundaries) |
| Understand the framework's structure and how one run proceeds | [Architecture, extension, and maintenance](docs/evaluations.md#architecture-extension-and-maintenance) |
| Learn how a scenario is built, run, and tested, starting from the Pydantic Evals concepts used | [Walkthrough: scope-discipline](docs/evaluations.md#walkthrough-scope-discipline) and [Pydantic Evals concepts used here](docs/evaluations.md#pydantic-evals-concepts-used-here) |
| Find the suite's requirements (E1–E40) and how each is verified | [Verifiable requirements](docs/evaluations.md#verifiable-requirements) |
| Change or add an evaluation case | [Modify or extend an evaluation](docs/evaluations.md#modify-or-extend-an-evaluation), then [verify a behavior change](docs/evaluations.md#verify-a-behavior-change) |
| Understand or assess a change to the contract's design | [contract-design.md](docs/contract-design.md), especially [Evolving the contract](docs/contract-design.md#evolving-the-contract) and [Assessing design changes](docs/contract-design.md#assessing-design-changes) |
| Edit any documentation, including the root guides | [documentation-maintenance.md](docs/documentation-maintenance.md) |

## Getting started

To understand or maintain the evaluation framework:

1. Read the root [README.md](../README.md) and [AGENTS.md](../AGENTS.md) to learn what is being evaluated, and [architecture.md](docs/architecture.md) for how the framework relates to the specification.
2. Read the [purpose and evaluation model](docs/evaluations.md#purpose-and-evaluation-model).
3. Follow [install prerequisites](docs/evaluations.md#install-prerequisites) and [run the offline checks](docs/evaluations.md#run-offline-checks). They need no login and use no subscription allowance; live runs do, as [Run a case or the suite](docs/evaluations.md#run-a-case-or-the-suite) explains.
4. Read the [architecture](docs/evaluations.md#architecture-extension-and-maintenance), then the [cases](docs/evaluations.md#cases-and-interpretation) and modules relevant to your work.

To work on the contract itself, read the [authority model](docs/architecture.md#development-time-and-runtime-authority) and [temporary migration authority](docs/architecture.md#temporary-migration-authority), then the reading guidance at the top of [contract-design.md](docs/contract-design.md). Its completed current-semantic specification retains the design rationale; reviewing and accepting RC1–RC10 by coherent topic is later work. The migration freeze keeps `AGENTS.md` byte-for-byte unchanged; future authorized edits to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md` also follow the contract's [protected-file rule](../AGENTS.md#38-instructions-protected-files-and-external-actions).

## Documentation ownership

Each kind of knowledge has one canonical owner. [Document ownership](docs/documentation-maintenance.md#document-ownership) states what each document owns, and [documentation-maintenance.md](docs/documentation-maintenance.md) holds the editing workflow and checks for keeping documents consistent.

This README is the engineering entry point. Root product files contain no references or dependencies into `_internal/`, including optional navigation; internal documents may reference root files. The [accepted boundary decision](docs/architecture.md#requirements-led-engineering-and-productinternal-separation) records the scoped application of §3.6, with each README identifying documentation for its own audience.

The root [README.md](../README.md) (an accessible introduction for potential adopters) and [README-powerusers.md](../README-powerusers.md) (detailed practical guidance for users) are user-facing. They may intentionally explain some of the same concepts at different depths, provided both stay consistent with `AGENTS.md` and neither defines competing rules. Internal engineering documents, including this README, apply ownership strictly: each detailed technical fact, requirement, procedure, or decision has one owner, and other documents summarize and link. [Public guides and internal engineering documents](docs/documentation-maintenance.md#public-guides-and-internal-engineering-documents) owns this distinction.
