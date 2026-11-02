# AGENTS-spec internal engineering

`_internal/` holds the engineering work behind the [AGENTS.md](../AGENTS.md) specification: the design rationale that informs changes to the contract, a local evaluation framework that exercises selected contract behaviors with a coding agent, and the guidance that keeps the repository's documentation canonically owned. The contract, its tool bridges, and the guides for people adopting it live at the repository root, starting with [README.md](../README.md).

The root [AGENTS.md](../AGENTS.md) governs engineering work here as everywhere else in the repository. This directory defines no separate operating contract; its documents explain, evaluate, and maintain that one.

This README is for orientation only. Each topic below links to the document that owns it; if this summary and a linked owner disagree, the owner is authoritative and this README needs correcting.

## Engineering responsibilities

| Responsibility | What it covers | Canonical documentation |
| --- | --- | --- |
| Specification design | Why the contract is designed as it is, and the constraints and review scenarios that apply when changing `AGENTS.md`. It remains publicly readable for anyone interested in the specification's rationale; the root guides reach it through this README rather than linking to it directly. | [docs/contract-design.md](docs/contract-design.md) |
| Evaluation framework | A Python suite that runs Codex on each case in a fresh temporary workspace containing an unchanged copy of the root contract, then combines automated assertions with human review of selected behaviors. Results are evidence about those cases, not general compliance. | [docs/evaluations.md](docs/evaluations.md) |
| Documentation maintenance | Canonical ownership and editorial guidance for all repository documentation, including the root guides. | [docs/documentation-maintenance.md](docs/documentation-maintenance.md) |

The framework depends on the specification: it evaluates the current root `AGENTS.md`, and its cases and review criteria cite that contract's clauses. The specification does not depend on the framework. [docs/architecture.md](docs/architecture.md) explains how these responsibilities fit together, their boundaries, and how a contract change can affect evaluation cases, rubrics, and documentation; the documents above own the detail.

## Directory layout

| Path | Role |
| --- | --- |
| `docs/` | Internal engineering documentation: [architecture.md](docs/architecture.md) for the integrated engineering architecture, [contract-design.md](docs/contract-design.md) and [evaluations.md](docs/evaluations.md) for specification design and the evaluation framework, and [documentation-maintenance.md](docs/documentation-maintenance.md) for documentation ownership and editorial guidance across the whole repository, including the root guides. |
| `evals/` | The evaluation package: its command-line entry point and case composition (`__main__.py`), shared execution, workspace, evidence, and grading infrastructure in `runtime/`, and one module per evaluation case in `scenarios/`. [Responsibilities and dependency direction](docs/evaluations.md#responsibilities-and-dependency-direction) assigns each module's role. |
| `tests/` | The offline unittest suite, grouped by responsibility: `runtime/` for the shared machinery and cross-scenario CLI guarantees, `scenarios/` for one module per evaluation case, and `support/` for a fake Codex executable and CLI test harness that never contact OpenAI. The root keeps an offline smoke substitute and an opt-in probe of the installed Codex sandbox. See [offline checks](docs/evaluations.md#run-offline-checks) and [functional-check execution](docs/evaluations.md#functional-check-execution). |
| [requirements.txt](requirements.txt) | The suite's Python dependency range. |
| `.venv/` | Local virtual environment created during [setup](docs/evaluations.md#install-prerequisites); ignored by Git. |
| `.eval-runs/` | Evidence directories created by evaluation runs and kept after later runs; ignored by Git. See [retained evidence](docs/evaluations.md#retained-evidence). |

## Where to find things

| To | Go to |
| --- | --- |
| Understand how specification design, evaluation, and documentation maintenance fit together, and how a contract change can affect evaluation | [architecture.md](docs/architecture.md) |
| Understand what the suite evaluates and the limits of its results | [Purpose and evaluation model](docs/evaluations.md#purpose-and-evaluation-model) |
| Install prerequisites, authenticate, and run offline checks or cases | [Setup and running evaluations](docs/evaluations.md#setup-and-running-evaluations) |
| Read outcomes, retained evidence, and investigate a failure | [Results, evidence, and failure investigation](docs/evaluations.md#results-evidence-and-failure-investigation) |
| Look up a case's situation, assertions, and review interpretation | [Cases and interpretation](docs/evaluations.md#cases-and-interpretation); each case links to the module that owns its exact prompt, fixture, checks, and any rubric |
| Understand isolation, credentials, deadlines, and cleanup | [Execution and security boundaries](docs/evaluations.md#execution-and-security-boundaries) |
| Understand the framework's structure and how one run proceeds | [Architecture, extension, and maintenance](docs/evaluations.md#architecture-extension-and-maintenance) |
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

To work on the contract itself, start with the reading guidance at the top of [contract-design.md](docs/contract-design.md). Edits to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md` follow the contract's [protected-file rule](../AGENTS.md#38-instructions-protected-files-and-external-actions).

## Documentation ownership

Each kind of knowledge has one canonical owner. [Document ownership](docs/documentation-maintenance.md#document-ownership) states what each document owns, and [documentation-maintenance.md](docs/documentation-maintenance.md) holds the editing workflow and checks for keeping documents consistent.

The root [README.md](../README.md) (an accessible introduction for potential adopters) and [README-powerusers.md](../README-powerusers.md) (detailed practical guidance for users) are user-facing. They may intentionally explain some of the same concepts at different depths, provided both stay consistent with `AGENTS.md` and neither defines competing rules. Internal engineering documents, including this README, apply ownership strictly: each detailed technical fact, requirement, procedure, or decision has one owner, and other documents summarize and link. [Public guides and internal engineering documents](docs/documentation-maintenance.md#public-guides-and-internal-engineering-documents) owns this distinction.
