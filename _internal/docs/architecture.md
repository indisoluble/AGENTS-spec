# AGENTS-spec engineering architecture

This document explains how the internal engineering project behind [AGENTS.md](../../AGENTS.md) fits together: why it exists, how its responsibilities relate, where its principal boundaries lie, and through which dependencies a change in one area affects another. It owns those system-level relationships. Detailed knowledge stays with the documents listed in [where detailed knowledge lives](#where-detailed-knowledge-lives); this document summarizes them only as far as the relationships require.

## Purpose and scope

The repository delivers a specification: the root `AGENTS.md` contract and two instruction bridges, `CLAUDE.md` and `.github/copilot-instructions.md`, which adopters copy into their own repositories following the [installation steps](../../README.md#get-started). The root [README.md](../../README.md) and [README-powerusers.md](../../README-powerusers.md) explain that specification to its users.

`_internal/` holds the engineering work used to develop and assess the specification. Adopters do not install it, and it adds no operating duties to the delivered contract. The [authority model below](#development-time-and-runtime-authority) distinguishes engineering authority from the instructions currently governing maintenance work. The engineering project has three related responsibilities:

1. **Product requirements, design, and evolution.** Defining intended agent behavior and product constraints, and explaining the mechanisms, decisions, and trade-offs selected to realize them. [contract-design.md](contract-design.md) is the authoritative engineering source for product requirements, current binding design prescriptions, constraints, rationale, significant design history, and subsequent engineering evolution. RC1–RC10 remain provisional enduring product-requirement candidates; their acceptance is separate from preserving the current binding semantics.
2. **Behavioral evaluation and evaluator verification.** A local Python framework runs Codex on finite cases against the current contract and produces evidence about those cases. Offline tests verify the evaluation machinery. [evaluations.md](evaluations.md) owns the subsystem documentation, including evaluator requirements E1–E40, which are distinct from product requirements.
3. **Knowledge maintenance.** Keeping each fact, rule, explanation, and decision with one canonical owner and keeping its dependents consistent, across the whole repository including the root guides. [documentation-maintenance.md](documentation-maintenance.md) owns the ownership map and editorial guidance.

Its readers are people who engineer, evaluate, evolve, operate, and maintain the specification and its evaluation framework. This document explains the engineering relationships; it does not supply runtime operating rules, adopting-project facts or architecture, or provider-owned instruction-loading behavior. Everything outside `_internal/` belongs to the user-facing product or its adoption and usage material. Root files neither reference nor depend on `_internal/`, including optional further-reading links. Internal documentation may reference root files, and engineering navigation starts at [_internal/README.md](../README.md).

### Development-time and runtime authority

**Engineering authority.** [contract-design.md](contract-design.md) is the authoritative engineering source for product requirements, currently binding design prescriptions, constraints, rationale, significant design history, and subsequent engineering evolution. Product objectives, established product requirements and constraints, accepted engineering decisions, and requester direction govern that evolution and its acceptance criteria, including intended evaluation expectations. Design rationale explains why selected mechanisms realize that intent. Existing `AGENTS.md` wording is implementation evidence, not an independent justification for preserving every mechanism or automatic proof of accepted product intent. Inferred requirement candidates remain separate from established requirements and await review and acceptance by coherent topic; a complete independently accepted product-requirements baseline is not yet established. The [historical record below](#temporary-migration-authority) preserves the authority-transition provenance.

**Runtime normative authority.** `AGENTS.md` is the complete, self-contained normative operating contract delivered to consuming agents, within the applicable instruction hierarchy and tool permissions. Requirements and rationale in internal documentation create no additional operating duties or runtime dependencies. A mismatch between intended requirements and contract wording calls for human review and authorized correction, not an implicit change to the rules applied to an agent. Existing runs remain interpreted under their captured contract and rubric until approved changes are implemented; revised criteria do not silently revise historical conclusions. Neither source automatically grants permission to edit protected files or make consequential decisions beyond existing authorization; requester authority and tool permissions continue to apply.

**Currently loaded operating instructions.** Agents maintaining this repository may receive the repository-root `AGENTS.md` through provider-specific instruction-loading mechanisms. While loaded, its applicable instructions govern the agent's conduct, subject to higher-priority instructions, tool permissions, and requester authority. This is an operational fact about the current development arrangement, not a permanent architectural requirement that the contract govern its own evolution.

An authorized redesign may reconsider or replace an existing mechanism, including PDSA or another method currently prescribed by the contract. Authorization to reconsider a mechanism does not itself suspend applicable loaded instructions. If changing the engineering process itself becomes necessary, that change must be addressed explicitly through an authorized and technically effective mechanism; editing or evaluating the contract creates no exemption from the instructions governing the agent.

The contract prescribes intended conduct; it does not independently enforce or guarantee compliance. Technical enforcement depends on the tool's actual controls, and observed behavior requires evidence.

Verifying the contract against intended requirements examines whether its text expresses the intended obligations, permissions, conditions, exceptions, and constraints. Behavioral evaluation instead examines what agents receiving that text actually do. Evaluator tests verify the machinery's own specified execution, observation, grading, reporting, and failure behavior; they do not establish agent compliance or the semantic validity of the expectations. These are separate evidence relationships. The [current-semantic specification](contract-design.md#current-semantics-vocabulary-and-coverage) records the current clauses and their interactions; traceability from independently accepted product requirements to the contract and evaluations remains pending.

#### Temporary migration authority

**Historical boundary — concluded November 8, 2026.** Throughout the source-of-truth migration, the frozen root `AGENTS.md` governed **all current operating semantics**, within the actual instruction hierarchy, permissions, and requester authority. The verified baseline is historical evidence:

| Identity | Value |
| --- | --- |
| `AGENTS.md` Git blob | `289a31a644d7ab1b816c873f244566ab632a330f` |
| File SHA-256 | `3d7b6c240e0f4b02713d166662d7d95ec74985b9939b23838863acd596407e81` |
| Reference commit on `refactor` | `184c7d5b26bfa78762c77e72381df9e408ac370b` |

Transfer required byte-for-byte preservation of `AGENTS.md`, semantic preservation in `contract-design.md`, and independent semantic and cross-document verification. The engineering specification had to preserve every obligation, prohibition, permission, recommendation, trigger, condition, exception, and relevant semantic interaction without weakening, strengthening, extending, or omitting them; other documentation had to remain consistent with the frozen contract.

Final requester-supplied independent verification against `66e63a443ac73712b4af8a54f5bc6fac3cb4fdff` returned **READY FOR TRANSFER DECISION**, with acceptance criteria A–H **PASS** and no corrective findings. Verification supplied evidence for the transfer decision; it did not itself transfer authority.

On **November 8, 2026**, after reviewing that verification, the requester explicitly replied **“Authorized”**, transferring engineering authority to `contract-design.md`. The transfer was documented in [`809e231`](https://github.com/indisoluble/AGENTS-spec/commit/809e231919c349b1ec3039ad3669dc88cf8b6e35). `AGENTS.md` retains self-contained normative runtime authority; internal documents create no runtime dependencies. The temporary byte-for-byte migration freeze concluded. The baseline is not a permanent prohibition on future separately authorized evolution under the [current authority model](#development-time-and-runtime-authority) and protected-file rules.

The transfer changes no existing agent operating behavior, amends no runtime contract, accepts none of RC1–RC10 as enduring product requirements, and selects or approves none of D1–D10. It authorizes no product redesign. Current methods, including PDSA, explicit increment predictions, EARS, and the other preserved prescriptions, retain their existing normative force until separately authorized change. The migration reviews establish neither comprehensive live-agent compliance nor measured token savings.

## Context and relationships

```mermaid
flowchart LR
  subgraph Root["Repository root: the specification and its user guides"]
    A["AGENTS.md<br/>normative runtime contract"]
    BR["CLAUDE.md,<br/>.github/copilot-instructions.md"]
    G["README.md,<br/>README-powerusers.md"]
  end
  subgraph Internal["_internal/: engineering"]
    subgraph CD["docs/contract-design.md: engineering authority"]
      PR["Product requirements<br/>RC1–RC10 provisional"]
      DR["Current binding semantics, constraints,<br/>rationale and design history"]
    end
    EV["docs/evaluations.md<br/>evaluation expectations and framework;<br/>evaluator requirements E1–E40"]
    DM["docs/documentation-maintenance.md"]
    PKG["evals/<br/>CLI composition, runtime/, and scenarios/"]
    T["tests/<br/>runtime/, scenarios/, and support/;<br/>offline smoke and functional-check sandbox probe"]
    RUNS[".eval-runs/<br/>retained evidence (git-ignored)"]
  end
  BR -->|direct tools to| A
  G -->|explain| A
  PR -.->|guide development| A
  PR -.->|guide intended expectations;<br/>traceability pending| EV
  DR -.->|guides engineering changes;<br/>explains mechanisms and trade-offs| A
  PKG -->|copies current bytes into each run;<br/>cases and rubrics cite clauses| A
  EV -->|specifies and explains| PKG
  T -->|verifies offline| PKG
  PKG -->|writes| RUNS
  RUNS -.->|read in human review| H["Maintainers and requester"]
  H -.->|may propose changes| PR
  H -.->|may propose changes| DR
  H -.->|"may propose; edits need §3.8 authorization"| A
  H -.->|may propose changes| EV
  DM -.->|governs editing of| PR
  DM -.->|governs editing of| DR
  DM -.->|governs editing of| EV
  DM -.->|governs editing of| G
```

Solid arrows are current references or mechanisms; dashed arrows are engineering responsibilities and human activities, including the requirements relationships, with candidate acceptance and traceability still pending. The internal-to-root editing relationships create no reference or dependency from product files back into engineering documentation. No automated path leads from evaluation results to changes in requirements, design, the contract, or evaluation expectations.

- **Contract and bridges.** `AGENTS.md` is the only operating contract. The bridges apply it through different mechanisms: `CLAUDE.md` uses Claude Code's import syntax, while the Copilot file links to the contract and directs the tool to read and follow it. Neither adds policy, and actual loading still depends on the tool, interface, and settings; [why the bridges differ](contract-design.md#why-the-bridges-differ) explains them.
- **Product requirements, current semantics, and design rationale.** `contract-design.md` is the authoritative engineering source described under [development-time and runtime authority](#development-time-and-runtime-authority). It specifies current binding semantics alongside rationale and evolution constraints, while acceptance of RC1–RC10 remains separate and pending. Internal intent and explanation cannot change the delivered contract's operating rules; a future authorized behavioral change must be reflected consistently in `AGENTS.md` and affected canonical engineering documentation, within the protected-file rules.
- **Evaluation framework.** The framework depends on the specification; the specification does not depend on the framework. Evaluation workspaces contain the root contract and the case fixture, with no bridge files, and the framework runs only Codex, so it exercises neither bridge nor any other tool.
- **Offline tests.** The unittest suite, a fake Codex executable, and an offline smoke substitute verify infrastructure and technical assertions without contacting OpenAI. A separate opt-in probe checks the evaluator-owned functional-check sandbox using the installed Codex CLI; it does not verify the evaluated-agent permission profile. Neither establishes live agent behavior or the semantic validity of a rubric.
- **Evidence and human review.** Each run retains its evidence outside the disposable workspace. Human reviewers assess rubric criteria outside the CLI, which collects no verdicts.
- **Documentation maintenance.** This concern spans all of the above: it assigns owners and governs how dependent documents are kept consistent.

### What evaluation evidence can establish

Results are evidence about the specific cases run, not about general contract compliance. The cases are finite and present designed conditions; automated assertions answer defined technical questions, while semantic criteria remain with human reviewers; model behavior is nondeterministic, so one run is not repeated evidence; and showing that the contract caused an observed behavior requires comparative evidence. [Purpose and evaluation model](evaluations.md#purpose-and-evaluation-model) owns these limits and the current coverage gaps. Human review distinguishes evaluator faults, unsuitable expectations or scenarios, contract wording that fails intended requirements, agent behavior, and unresolved product intent. Findings can inform proposals about requirements, design, implementation, or evaluation expectations; they authorize none of those changes. Contract edits retain the [protected-file rule](../../AGENTS.md#38-instructions-protected-files-and-external-actions) and the [evolution constraints](contract-design.md#evolving-the-contract).

## Principal boundaries

| Boundary | What it separates | Detail |
| --- | --- | --- |
| Product intent and runtime implementation | Product requirements guide development; rationale explains design choices. `AGENTS.md` implements the intended behavior as the complete runtime contract. RC1–RC10 remain provisional; guides and examples cannot enact behavior. | [Development-time and runtime authority](#development-time-and-runtime-authority) |
| Product requirements and evaluator requirements | Product requirements concern intended agent behavior and product constraints. E1–E40 specify the suite's required behavior, including how cases are executed and assessed; they do not independently establish product intent. Fictional application requirements in fixtures concern those applications. | [Verifiable requirements](evaluations.md#verifiable-requirements), [contract-design.md](contract-design.md) |
| Shared evaluation infrastructure and scenarios | Shared modules in `evals/runtime/` have no dependency on individual scenarios. Each scenario module in `evals/scenarios/` owns its prompt, fixture, assertions, any functional checks, and any human-review rubric. The CLI in `evals/__main__.py` composes the two. | [Responsibilities and dependency direction](evaluations.md#responsibilities-and-dependency-direction) |
| Execution, observation, grading, and human assessment | Agent commands use the restrictive permission profile for a disposable workspace. The parent Codex client and Python evaluator operate outside that command sandbox. Observations are captured outside the workspace; automated grading reads those observations, and human assessment uses the retained rubric and evidence. | [Purpose and evaluation model](evaluations.md#purpose-and-evaluation-model), [execution and security boundaries](evaluations.md#execution-and-security-boundaries) |
| Implementation and verification | The offline suite verifies configuration and orchestration with substitutes. The repository's sandbox probe checks only the evaluator-owned functional-check boundary. Agent-command enforcement and authenticated integration need separate environment-specific validation. | [Agent execution](evaluations.md#agent-execution), [verify a behavior change](evaluations.md#verify-a-behavior-change) |
| Evidence retention and interpretation | Evidence directories record what happened. Reports classify execution failures, assertion failures, and pending review separately. Interpretation stays tied to the captured contract and rubric. | [Results, evidence, and failure investigation](evaluations.md#results-evidence-and-failure-investigation) |
| Product and internal engineering documentation | Root files remain independent of internal engineering documentation. Internal documents give each detailed fact one owner; the user-facing root guides may overlap intentionally. | [Public guides and internal engineering documents](documentation-maintenance.md#public-guides-and-internal-engineering-documents) |

## Specification-to-evaluation dependencies

The framework currently exercises the root contract, and the dependencies below describe that implementation. The agreed requirements-led model guides future development without claiming that product-requirement traceability already exists. These are the known direct dependents to inspect under the contract's [canonical-knowledge rule](../../AGENTS.md#35-canonical-knowledge-and-affected-documentation) when `AGENTS.md` changes; they add no procedure or approval step.

| Dependency | Mechanism | Consequence |
| --- | --- | --- |
| Runtime contract injection | `CONTRACT_PATH` in [workspace.py](../evals/runtime/workspace.py) resolves to the repository-root `AGENTS.md`. Workspace preparation copies its current bytes into every workspace, and fixtures cannot override it (E1, E22). | Every run evaluates the contract as it stands at run time; no version is pinned. A contract edit reaches the next run whether or not affected cases and rubrics were reviewed. Offline tests compare against the same current bytes rather than fixed contents, so they neither depend on nor detect contract wording. |
| Clause references | The [case catalogue](evaluations.md#cases-and-interpretation) and case sections cite contract sections and link their heading anchors. Rubrics in [assumptions.py](../evals/scenarios/assumptions.py), [inquiry.py](../evals/scenarios/inquiry.py), and [findings.py](../evals/scenarios/findings.py) cite section numbers and rule strengths. Other rubrics direct reviewers to the retained contract's strengths and triggers without numbering. Automated assertions encode scenario expectations derived from contract behavior, such as `ScopePreserved` for §1.2's restriction on unrelated cleanup. | Renumbered sections, renamed headings, or changed rule meaning can leave case descriptions, assertions, or rubrics stale. No automated check in the repository detects such staleness. |
| Contract identity in evidence | [codex.py](../evals/runtime/codex.py) records `contract_sha256` in `execution.json` and saves the injected `AGENTS.md` with each run's evidence. Each human-review run also retains its rubric as `review.md`. | Results stay tied to the contract and rubric they used. A later contract change neither revises earlier conclusions nor carries them over to the new text. |

Other documents also link `AGENTS.md` heading anchors, including `contract-design.md` and the root guides. Their synchronization follows ordinary [documentation maintenance](documentation-maintenance.md#editing-workflow).

### Change impact

A contract change does not necessarily require an evaluation change. Established product requirements guide intended behavior and expectations; existing clauses and rubrics describe the current implementation and assessment baseline. Compare the changed clauses with the behavior each case exercises, using the catalogue's contract references and the rubric citations above, without treating contract edits alone as authority to redefine expected behavior:

- **Behavior an evaluated case exercises.** If a rule's strength, trigger, condition, exception, or scope changes where a case's assertions or rubric criteria depend on it, the scenario module and its catalogue entry are affected owners. Assess whether the case still presents its intended condition and whether its assertions and rubric still match the contract. An E1–E40 requirement changes only if the framework's own required behavior changes, through authorized requirement work.
- **Structure or wording without changed behavior.** Renumbering, renamed headings, or moved clauses need reference corrections in rubrics, the catalogue, and linking documents. Rubric meaning is unchanged.
- **No demonstrated evaluation impact.** A change to behavior that no case exercises needs no case change; [Purpose and evaluation model](evaluations.md#purpose-and-evaluation-model) lists known coverage gaps. Proposing new coverage is a separate decision, not an obligation created by the change.

Changes in the other direction never alter the contract. Editing a case or rubric changes what is assessed and how; it does not change what `AGENTS.md` requires.

## Where detailed knowledge lives

This architecture refines into the existing owners rather than replacing them:

- **Runtime normative behavior:** [AGENTS.md](../../AGENTS.md), the complete operating contract.
- **Product requirements, current-semantic specification, rationale, and evolution:** [contract-design.md](contract-design.md), the authoritative engineering source for intended requirements and constraints alongside current binding design prescriptions, trade-offs, significant specification decisions and design history, evolution constraints, design scenarios, and reference assignments. RC1–RC10 remain provisional.
- **Evaluation framework:** [evaluations.md](evaluations.md): evaluation model, operations and authentication, evidence and failure investigation, cases, execution boundaries, framework architecture and lifecycle, and E1–E40. Scenario modules own exact prompts, fixtures, checks, and rubrics.
- **Documentation ownership and editorial guidance:** [documentation-maintenance.md](documentation-maintenance.md), including the [per-document ownership table](documentation-maintenance.md#document-ownership) and the [public/internal distinction](documentation-maintenance.md#public-guides-and-internal-engineering-documents).

[_internal/README.md](../README.md) provides orientation and task-based navigation into these documents.

## Decisions

This section holds engineering-system-wide decisions and indexes decisions owned at narrower scopes. Specification-design decisions belong with requirements and rationale in `contract-design.md`; evaluation-subsystem decisions belong in `evaluations.md`. The two existing evaluation-specific records below remain canonical here, with their complete history preserved, until a separately authorized relocation. Documentation maintenance owns the ownership map and editing guidance, not duplicate decision records.

| Decision | Scope and canonical record |
| --- | --- |
| [Restrictive evaluation-agent command permissions](#restrictive-evaluation-agent-command-permissions) | Evaluation subsystem; retained here, intended future location `evaluations.md`. |
| [Integrated engineering architecture with focused detailed owners](#integrated-engineering-architecture-with-focused-detailed-owners) | Engineering system; retained here with the refinements recorded below. |
| [Evaluation framework package and verification hierarchy](#evaluation-framework-package-and-verification-hierarchy) | Evaluation subsystem; retained here, intended future location `evaluations.md`. |
| [Requirements-led engineering and product/internal separation](#requirements-led-engineering-and-productinternal-separation) | Engineering system; authority, ownership, and navigation boundaries. |

### Restrictive evaluation-agent command permissions

**Status:** Accepted. Authenticated `codex exec` integration and environment-specific enforcement still require validation.

**Context.** Evaluation-agent commands need workspace reads/writes while denying unrelated host access and shell networking. Pydantic Evals manages execution and grading; Codex runs the evaluated agent using a dedicated authentication profile. Evaluator-owned functional checks use a separate sandbox. [Agent execution](evaluations.md#agent-execution) owns the configured command boundary, official references, and verification limits.

**Decision.** Configure evaluated-agent commands through one restrictive native permission profile passed inline to `codex exec`, as required by [E7](evaluations.md#verifiable-requirements). The parent Codex client's authentication and provider communication and the Python evaluator operate outside that command sandbox.

**Consequences.** The configured profile limits command access to the workspace and the runtime reads documented under [agent execution](evaluations.md#agent-execution), with command networking disabled. Tools needing broader access may be unavailable. CLI support, runtime enforcement, and authenticated integration require environment-specific validation; offline tests establish configuration and orchestration only. The profile neither confines the parent client or Python evaluator nor establishes complete host isolation. Inline permission configuration requires no persistent user settings.

### Integrated engineering architecture with focused detailed owners

**Status:** Accepted. The requester accepted this direction after reviewing a read-only assessment of alternatives.

**Context.** The internal documents each had clear owners, but no document explained the engineering project as a whole. The internal README described two areas and a one-sentence dependency, while documentation maintenance appeared only as a file. `contract-design.md` does not refer to the evaluation framework, and `evaluations.md` links to contract clauses but not to the design rationale. The [dependencies above](#specification-to-evaluation-dependencies) were undocumented as relationships. Constraints: the README is orientation only; `contract-design.md` is also the public technical guide, not contributor onboarding; root-guide links into `_internal/docs/` and module docstrings referencing `docs/evaluations.md` should stay valid; and the contract's [architecture rule](../../AGENTS.md#36-architecture-guides-and-code-documentation) recommends starting architecture in one document, splitting sections as readability or maintenance warrants.

**Decision.** Add this document as the owner of system-level relationships, context, boundaries, and cross-domain dependencies. Keep `contract-design.md`, `evaluations.md`, and `documentation-maintenance.md` as the detailed owners, with `evaluations.md` intact as the framework's integrated documentation. The README keeps orientation and navigation. No paths or existing anchors change.

**Consequences.** One owner explains how specification design, evaluation, and documentation maintenance relate, without breaking external or docstring links. Maintainers keep one more document consistent, and must keep its summaries at the level of relationships so that it does not become a second owner of framework, rationale, or ownership detail.

**Rejected alternatives.**

- *Strengthen the existing documents only:* the README would have to own architecture, contrary to its role, and `contract-design.md` serves contract readers rather than the engineering project.
- *Subdirectories such as `specification/` and `evaluation/`:* folders do not explain relationships, and moving files would break root-guide links, docstrings, and anchors for a small document set.
- *Separate `evaluation-architecture.md` or `evaluation-cases.md`, extracted E1–E40, or another split of `evaluations.md`:* these would present evaluation as an independent subsystem and separate requirements from the case acceptance definitions and evidence they reference. Length alone did not justify a split.
- *Moving the framework lifecycle into this document:* it would separate that lifecycle from the outcome, evidence, and functional-check sections it explains.

**Later navigation change.** The context and rejected alternatives above record root-guide links into `_internal/docs/` as they existed when this decision was made. A later editorial decision, owned by [documentation-maintenance.md](documentation-maintenance.md#public-guides-and-internal-engineering-documents), replaced those links with one pointer from each root guide to `_internal/README.md`. It changes navigation only; this decision, its paths, and the remaining link constraints from docstrings and external references are unaffected.

That pointer arrangement is historical. [Requirements-led engineering and product/internal separation](#requirements-led-engineering-and-productinternal-separation) supersedes it and refines the earlier rationale-only description of specification design, while retaining the integrated architecture and focused detailed owners.

### Evaluation framework package and verification hierarchy

**Status:** Accepted. The requester selected this hierarchy after reviewing read-only assessments of alternatives and an incremental migration plan. The migration proceeds in separately reviewed increments; until each one lands, source and test paths elsewhere in this document and in [evaluations.md](evaluations.md) describe the layout that currently exists.

**Context.** `evals/` held the command-line entry point, eight shared execution modules, and ten scenario modules side by side, so its listing did not distinguish what is evaluated from how a case runs. `tests/` was equally flat: shared-mechanism tests, scenario tests, the fake Codex executable, the CLI test harness, and two standalone entry points. `test_codex_failures.py` combined 13 cross-scenario CLI guarantees with 24 tests belonging to individual scenarios, two of which imported values from other test modules; discovery therefore loaded `test_followthrough.py` and `test_inquiry.py` under two module names each, although no test ran twice. A developer unfamiliar with Pydantic Evals could not tell from the tree where a scenario is defined, where it is verified, or which code runs every case. Constraints: keep `python -m evals`, `python -m unittest discover -s tests -v`, `python -m tests.offline_smoke`, and `python -m tests.probe_functional_sandbox` working; preserve E1–E40, grading semantics, and the documented smoke convenience; add no aliases for incidental internal module paths, as [interfaces used by scenarios](evaluations.md#interfaces-used-by-scenarios-and-substitutes) states; keep `_check_process.py` beside `functional.py`, which locates it by file position; and keep `CONTRACT_PATH` resolving to the root `AGENTS.md`.

**Decision.**

- `evals/__main__.py` remains the command-line entry point and composes the scenarios (`CASES`); `python -m evals` requires it at that path.
- `evals/runtime/` owns the shared execution machinery: `evaluation`, `workspace`, `codex`, `auth`, `process`, `functional`, `functional_checks`, and `_check_process`. It imports no scenario.
- `evals/scenarios/` owns evaluation definitions and grading policy: one module per scenario with its prompt, fixture, dataset, evaluators, any functional checks, and any review rubric. Scenarios depend on runtime; reuse between scenarios stays explicit, as when independent-execution reuses the requester-guidance fixture.
- `tests/runtime/` verifies shared mechanisms and cross-scenario CLI guarantees in `test_cli.py`, which is `test_codex_failures.py` after its scenario-specific tests move out.
- `tests/scenarios/` verifies individual scenarios: each `test_<module>.py` holds that scenario's grading tests and its CLI tests.
- `tests/support/` holds the fake Codex executable and the CLI test harness. `tests/offline_smoke.py` and `tests/probe_functional_sandbox.py` stay at the `tests/` root so their documented commands are unchanged.
- A component becomes a directory only when several independently meaningful files justify it; otherwise it stays one module. Test layout corresponds to production by responsibility, not file for file.
- Internal imports are absolute and package-qualified, and moved modules leave no compatibility re-exports.
- Live evaluation, which runs Codex through `python -m evals`, stays separate from offline verification under `tests/`, which uses substitutes and the fake CLI to establish evaluator correctness rather than agent behavior.

**Consequences.** The tree separates composition, shared machinery, scenario policy, and verification by responsibility. A scenario's definition and its complete offline verification are each one file, and with no imports between test modules, no module is loaded under two names. Costs are a one-time update of imports, string mock-patch targets, child-process import strings, and documentation links, and path calculations one level deeper: `CONTRACT_PATH`, the CLI harness's working directory, and the fake-executable path in scenario tests. Discovery reports test IDs relative to `tests/`, such as `scenarios.test_scope…`, which differ from the package-qualified names used to run one module, such as `python -m unittest tests.scenarios.test_scope`; during discovery `runtime`, `scenarios`, and `support` are importable as top-level names, as test modules already are. Adding a scenario touches its module, its `CASES` entry, its test module, the fake executable's responses, and the case lists in the cross-scenario CLI tests. Requirement wording is unaffected; only source links and verification references move.

**Rejected alternatives.**

- *Keep both trees flat and explain them in documentation:* least churn, but the listings would still mix shared machinery with scenarios, and scenario-specific CLI tests would stay combined with cross-scenario ones.
- *Scenarios package only, with flat tests:* fewer moves, but tests would remain distinguishable only by file name.
- *Shared modules left at the `evals/` root, with tests grouped under `tests/infrastructure/`:* groups tests by responsibility, but leaves shared modules interleaved with the entry point and gives production and verification different names for the same responsibility.
- *One directory per scenario, such as `evals/scenarios/scope/scenario.py`:* adds a level with no second substantive file to hold.
- *Compatibility modules at the old paths:* no documented contract or demonstrated consumer depends on internal module paths; aliases would preserve accidental interfaces and hide stale imports that otherwise fail loudly.
- *Moving `offline_smoke.py` and the sandbox probe into subdirectories:* would change their documented commands.
- *Test substitutes in runtime, or a shared path constant for the fake executable:* test-only code does not belong in production modules, and scenario tests that install the fake as a sandbox locate it directly instead of depending on the CLI harness.

**Relation to the earlier decision.** The subdirectories rejected in [Integrated engineering architecture with focused detailed owners](#integrated-engineering-architecture-with-focused-detailed-owners) concerned the documents under `_internal/docs/`. This decision concerns code and test packages and leaves the documentation layout unchanged.

### Requirements-led engineering and product/internal separation

**Status:** Accepted. The requester approved this engineering direction and authorized its documentation in Stage 1; requirements extraction, design-document restructuring, evaluation traceability, and directory reorganization remain outside this stage.

**Context.** The project now develops and evaluates a reusable contract, with separate evaluation code and offline tests. Earlier ownership described `contract-design.md` as rationale, while cases and rubrics referred to the implemented contract. That arrangement did not separately identify product intent as the basis for development. Root guides also pointed into `_internal/`, following the historical navigation change above. The requester established independent product documentation, requirements-led development, preservation of existing knowledge, and unchanged paths as the constraints for this correction.

**Decision.** Product requirements define intended agent behavior and product constraints and guide contract development and evaluation expectations. `contract-design.md` is their canonical owner alongside clearly distinguishable design rationale and specification-design decisions, in one document. Existing clauses are not automatically accepted requirements; inferred candidates remain separate for later review by coherent topic. `AGENTS.md` remains the complete runtime normative contract, and current runs retain their captured contract and rubric interpretation. E1–E40 remain evaluator requirements. Evaluation results provide evidence for human review, without automatically authorizing changes to any of these artifacts.

Everything outside `_internal/` belongs to the user-facing product or its adoption and usage material. Root product files contain no references or dependencies into `_internal/`; internal documentation may reference them. Apply [§3.6](../../AGENTS.md#36-architecture-guides-and-code-documentation) by scope: the root README identifies user-facing documentation, while `_internal/README.md` identifies engineering documentation and serves as its entry point. The clause names `README.md` without explicitly assigning all documentation locations to one root entry point. This records the approved repository interpretation without changing that clause or adding consumer duties.

This architecture owns engineering-system-wide decisions and their index. Specification-specific records belong in `contract-design.md`, and evaluation-specific records belong in `evaluations.md`; the existing evaluation records remain here until separately authorized relocation. Keep the current paths for this stage. The [ownership map](documentation-maintenance.md#document-ownership) and [navigation guidance](documentation-maintenance.md#public-guides-and-internal-engineering-documents) apply these boundaries without duplicating decision records.

**Consequences.** Product documentation remains independently usable, with no internal runtime dependency. Maintainers distinguish intended requirements, design reasoning, implemented instructions, observed agent behavior, and verification of the evaluator. The requirements inventory is not yet extracted or accepted, and evaluation traceability is not yet established. Later work preserves significant rationale, constraints, accepted decisions, and useful alternatives; the historical PDSA guide informs that work without overriding current decisions or implementation. No code, grading policy, contract behavior, or directory layout changes in this stage. The earlier integrated-architecture decision remains accepted, with its rationale-only ownership description refined and its root-guide pointer arrangement superseded.

**Rejected alternatives.**

- *Accept current implementation wording wholesale as product requirements:* would infer intent from implementation without topic-level review.
- *Retain optional root-guide pointers into internal engineering documentation:* would violate the approved product/internal boundary.
- *Make internal requirements or rationale additional runtime instructions:* would make the adopted contract incomplete and create hidden dependencies.

Splitting requirements from rationale into separate files, relocating existing decision records, and reorganizing directories are deferred; this decision does not perform or authorize them.
