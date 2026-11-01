# AGENTS-spec internal engineering

`_internal/` holds the engineering work behind the [AGENTS.md](../AGENTS.md) specification: the design rationale that informs changes to the contract, and a local evaluation framework that exercises selected contract behaviors with a coding agent. The contract, its tool bridges, and the guides for people adopting it live at the repository root, starting with [README.md](../README.md).

The root [AGENTS.md](../AGENTS.md) governs engineering work here as everywhere else in the repository. This directory defines no separate operating contract; its documents explain, evaluate, and maintain that one.

This README is for orientation only. Each topic below links to the document that owns it; if this summary and a linked owner disagree, the owner is authoritative and this README needs correcting.

## Two areas of work

| Area | What it covers | Canonical documentation |
| --- | --- | --- |
| Specification design | Why the contract is designed as it is, and the constraints and review scenarios that apply when changing `AGENTS.md`. It is also the public technical guide linked from the root README. | [CONTRACT-DESIGN.md](CONTRACT-DESIGN.md) |
| Evaluation framework | A Python suite that runs Codex on each case in a fresh temporary workspace containing an unchanged copy of the root contract, then combines automated assertions with human review of selected behaviors. Results are evidence about those cases, not general compliance. | [EVALUATIONS.md](EVALUATIONS.md) |

The framework depends on the specification: it evaluates the current root `AGENTS.md`, and its cases and review criteria cite that contract's clauses. The specification does not depend on the framework.

## Directory layout

| Path | Role |
| --- | --- |
| `evals/` | The evaluation package and its command-line entry point: shared execution, workspace, evidence, and grading infrastructure, plus one module per evaluation case. [Responsibilities and dependency direction](EVALUATIONS.md#responsibilities-and-dependency-direction) assigns each module's role. |
| `tests/` | The offline unittest suite, a fake Codex executable and an offline smoke substitute that never contact OpenAI, and an opt-in probe of the installed Codex sandbox. See [offline checks](EVALUATIONS.md#run-offline-checks) and [functional-check execution](EVALUATIONS.md#functional-check-execution). |
| [requirements.txt](requirements.txt) | The suite's Python dependency range. |
| `.venv/` | Local virtual environment created during [setup](EVALUATIONS.md#install-prerequisites); ignored by Git. |
| `.eval-runs/` | Evidence directories created by evaluation runs and kept after later runs; ignored by Git. See [retained evidence](EVALUATIONS.md#retained-evidence). |
| [CONTRACT-DESIGN.md](CONTRACT-DESIGN.md), [EVALUATIONS.md](EVALUATIONS.md) | Technical documentation for the two areas above. |
| [DOCUMENTATION.md](DOCUMENTATION.md) | Documentation ownership and editorial guidance for the whole repository, including the root guides. |

## Where to find things

| To | Go to |
| --- | --- |
| Understand what the suite evaluates and the limits of its results | [Purpose and evaluation model](EVALUATIONS.md#purpose-and-evaluation-model) |
| Install prerequisites, authenticate, and run offline checks or cases | [Setup and running evaluations](EVALUATIONS.md#setup-and-running-evaluations) |
| Read outcomes, retained evidence, and investigate a failure | [Results, evidence, and failure investigation](EVALUATIONS.md#results-evidence-and-failure-investigation) |
| Look up a case's situation, assertions, and review interpretation | [Cases and interpretation](EVALUATIONS.md#cases-and-interpretation); each case links to the module that owns its exact prompt, fixture, checks, and any rubric |
| Understand isolation, credentials, deadlines, and cleanup | [Execution and security boundaries](EVALUATIONS.md#execution-and-security-boundaries) |
| Understand the framework's structure and how one run proceeds | [Architecture, extension, and maintenance](EVALUATIONS.md#architecture-extension-and-maintenance) |
| Find the suite's requirements (E1–E40) and how each is verified | [Verifiable requirements](EVALUATIONS.md#verifiable-requirements) |
| Change or add an evaluation case | [Modify or extend an evaluation](EVALUATIONS.md#modify-or-extend-an-evaluation), then [verify a behavior change](EVALUATIONS.md#verify-a-behavior-change) |
| Understand or assess a change to the contract's design | [CONTRACT-DESIGN.md](CONTRACT-DESIGN.md), especially [Evolving the contract](CONTRACT-DESIGN.md#evolving-the-contract) and [Assessing design changes](CONTRACT-DESIGN.md#assessing-design-changes) |
| Edit any documentation, including the root guides | [DOCUMENTATION.md](DOCUMENTATION.md) |

## Getting started

To understand or maintain the evaluation framework:

1. Read the root [README.md](../README.md) and [AGENTS.md](../AGENTS.md) to learn what is being evaluated.
2. Read the [purpose and evaluation model](EVALUATIONS.md#purpose-and-evaluation-model).
3. Follow [install prerequisites](EVALUATIONS.md#install-prerequisites) and [run the offline checks](EVALUATIONS.md#run-offline-checks). They need no login and use no subscription allowance; live runs do, as [Run a case or the suite](EVALUATIONS.md#run-a-case-or-the-suite) explains.
4. Read the [architecture](EVALUATIONS.md#architecture-extension-and-maintenance), then the [cases](EVALUATIONS.md#cases-and-interpretation) and modules relevant to your work.

To work on the contract itself, start with the reading guidance at the top of [CONTRACT-DESIGN.md](CONTRACT-DESIGN.md). Edits to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md` follow the contract's [protected-file rule](../AGENTS.md#38-instructions-protected-files-and-external-actions).

## Documentation ownership

Each kind of knowledge has one canonical owner. [Document ownership](DOCUMENTATION.md#document-ownership) states what each document owns, and [DOCUMENTATION.md](DOCUMENTATION.md) holds the editing workflow and checks for keeping documents consistent.
