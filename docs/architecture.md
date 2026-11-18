# AGENTS-spec engineering architecture

AGENTS-spec develops a reusable, self-contained [operating contract](../03-contract/prerelease_AGENTS.md) for coding agents. Behavior establishes product intent, Design selects its realization, Contract stages the consumer files, and Evaluations assess the candidate. This document explains that structure; [authority and change](authority-and-change.md) explains how to change it, and [engineering history](engineering-history.md) preserves consequential decisions and their reasons.

## Purpose and scope

Engineering documentation supports understanding, changing, and verifying the product. Consumer artifacts contain no references or dependencies back into it. The delivered `AGENTS.md` contains the complete runtime instructions; the bridges load or direct tools to it, and the two consumer guides explain adoption and use.

### Current BDD-first organization

```text
01-behavior/       accepted baseline, discovery, proposed examples
02-design/         contract design, mechanisms, rationale
03-contract/       five staged consumer artifacts
04-evaluations/    case definitions, evaluator requirements, Python package
docs/              shared architecture, authority/change guidance, decisions
```

Behavior, Design, and Evaluations each have three immediate entries: `README.md` for orientation, `docs/` for supporting explanations and maintenance knowledge, and `deliverables/` for substantive artifacts. Contract is the exception: exactly five consumer files at its root, with no engineering README or container directories. Design prescriptions stay with their necessary rationale rather than being split by normative status.

Numbers show conceptual progression, not mandatory sequential gates. BDD Discovery, Formulation, and Automation iterate across these responsibility owners; knowledge maintenance spans them all. Directory ownership identifies where knowledge is maintained, not who can accept or authorize a change.

## Current relationships and change guidance

Accepted intent guides both design and evaluation expectations. Design relates selected mechanisms to the staged contract; evaluations exercise an identified candidate and return findings for review. These are separate paths: implementation wording alone cannot establish intended behavior or an independent expected result. The [traceability model](authority-and-change.md#cross-domain-traceability-and-feedback) explains their links, feedback, and remaining coverage gaps.

For a change, use the shared [authority model](authority-and-change.md#development-time-and-runtime-authority) and [change-impact guidance](authority-and-change.md#change-impact). Detailed owners are listed below.

## Principal boundaries

- **Shared machinery and scenario policy:** `04-evaluations/deliverables/runtime/` has no dependency on individual scenarios. Scenario modules own prompts, fixtures, assertions, functional checks, and human rubrics; `deliverables/__main__.py` composes them. See [responsibilities and dependency direction](../04-evaluations/docs/framework-design.md#responsibilities-and-dependency-direction).
- **Execution and assessment:** the restrictive agent-command sandbox covers commands in the disposable workspace. The parent Codex client and Python evaluator operate outside it; observations are retained outside the writable fixture, then graded and reviewed. See [execution and security boundaries](../04-evaluations/docs/framework-design.md#execution-and-security-boundaries).
- **Contract and evaluator:** the evaluator consumes the contract; the contract has no dependency on the evaluator. Contract injection, clause references, and captured identity are the [direct dependencies to inspect](authority-and-change.md#specification-to-evaluation-dependencies).

### Staged sources and release-relative references

Engineering links target the staged sources. Display names and adopting-project examples use the intended consumer filenames:

| Staged source in `03-contract/` | Intended consumer location |
| --- | --- |
| `prerelease_AGENTS.md` | `AGENTS.md` |
| `prerelease_CLAUDE.md` | `CLAUDE.md` |
| `prerelease_copilot-instructions.md` | `.github/copilot-instructions.md` |
| `prerelease_README.md` | `README.md` |
| `prerelease_README-powerusers.md` | `README-powerusers.md` |

Standard instruction and documentation filenames in the contract describe adopting projects. Claude's `@AGENTS.md` import and Copilot's `../AGENTS.md` link resolve at their intended consumer locations, not from the staged files. The consumer README's license link targets the repository-root `LICENSE`. Preserve these release-relative meanings when editing or checking links.

These staged instruction filenames fall outside the default discovery paths documented for [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code](https://code.claude.com/docs/en/memory), and [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions), as checked on **8 November 2026**. The [authority model](authority-and-change.md#development-time-and-runtime-authority) distinguishes development instruction loading from explicit source reading and isolated evaluation injection.

## Where detailed knowledge lives

| Question | Canonical owner |
| --- | --- |
| What behavior is accepted, and why? | [Baseline](../01-behavior/deliverables/baseline.md): objectives, rationale, BR1–BR10, PR1, constraints, and acceptance provenance. |
| What remains proposed or unresolved? | [Discovery](../01-behavior/deliverables/discovery.md): example suites, classifications, coverage, formulation questions, and remaining work; [candidate history](../01-behavior/docs/candidate-and-example-history.md): earlier proposals and their disposition. |
| How does the contract realize intent? | [Contract design](../02-design/deliverables/contract-design.md): vocabulary, clause index, layer composition, and links to mechanisms, delivery, methods, and rationale. [Design review](../02-design/docs/design-review.md) supplies explanation checks and non-normative illustrations. |
| What instructions reach consumers? | [Staged AGENTS.md](../03-contract/prerelease_AGENTS.md); the [adoption guide](../03-contract/prerelease_README.md) explains installation. |
| What do evaluations assess, and how are they operated? | [Evaluation model](../04-evaluations/docs/evaluations.md), [cases and E1–E40](../04-evaluations/deliverables/cases-and-requirements.md), [operations and evidence](../04-evaluations/docs/running-and-reviewing.md), and [framework design](../04-evaluations/docs/framework-design.md). Exact case policy stays in scenario modules. Run commands from `04-evaluations/`; new evidence goes to its `.eval-runs/`, with older evidence in its [documented locations](../04-evaluations/docs/running-and-reviewing.md#retained-evidence). |
| What authority and maintenance rules cross stages? | [Authority and change](authority-and-change.md): BDD responsibilities, status, traceability, documentation ownership, and change impact. |

## Decisions

[Engineering history](engineering-history.md#decisions) records system-wide choices. [Design decisions and alternatives](../02-design/docs/decisions-and-alternatives.md#architecture-decisions) and [evaluation engineering decisions](../04-evaluations/docs/framework-design.md#engineering-decisions) retain their domain-specific reasons, alternatives, and successors. The [engineering authority and runtime contract decision](engineering-history.md#engineering-authority-and-the-runtime-contract) explains the basis for engineering ownership of requirements and design and the scope of the delivered contract's authority.
