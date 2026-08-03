# AGENTS.md
**Release date:** 2026-08-03 - **Canonical source:** https://github.com/indisoluble/AGENTS-spec

## 1. Canonical status
`AGENTS.md` is the canonical contract for repository-wide agent behavior. Path-specific instructions follow the current tool's scope and precedence. `CLAUDE.md` and `.github/copilot-instructions.md` are compatibility bridges, never independent policy sources.

## 2. Operational protocol
Scale this protocol to task complexity; do not over-plan trivial work. Select an approach before editing. Use a tool-specific review-before-implementation mode only when requested or workflow-required; its output is this contract's planning artifact. Follow task instructions and the tool's approval model.
1. Classify the task as trivial or non-trivial.
2. Identify protected files, affected artifacts, relevant documentation, and applicable validation.
3. Inspect required context; identify material assumptions, conflicts, missing context, and risks.
4. Before non-trivial edits, state a concise implementation plan; if section 9.3 is active, use its increment sequence.
5. Outside planning-only workflow, apply the smallest coherent, behaviorally complete change authorized by the request or selected increment.
6. Synchronize affected artifacts when required.
7. Run relevant available validation.
8. Report as section 15 requires.

## 3. Protected contract files
`AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` are protected. Change them only when explicitly requested to change that file, the contract, or a bridge, or to apply prior recommendations specific to it.
If only one is requested, change the others only when required or explicitly included. Keep protected-file changes separate from unrelated code, documentation, formatting, dependency, cleanup, or maintenance; propose unrequested work separately.

## 4. Terminology and task classification
- **Affected artifacts** are code, tests, configuration, and documentation affected by the task. A **behaviorally complete change** includes all required artifacts and validation for the requested behavior, with no unstated follow-up.
- A task is **non-trivial** if it changes behavior or documentation meaning; interfaces, schemas, protocols, or data formats; security, authentication, authorization, secrets, permissions, privacy, concurrency, async behavior, lifecycle, cleanup, error handling, tests, CI, build, packaging, deployment, runtime configuration, or dependencies; spans multiple logical areas; or has unclear requirements, missing context, or material risk.
- A task is **trivial** only if local, mechanical, low-risk, and changing no behavior, interface, configuration, dependency, test, documentation meaning, or repository structure.
- A **reviewable change/increment** is one unit whose intent, rationale, resulting behavior, risks, and validation a reviewer can understand and verify. Judge size and tracing burden; interacting concerns, control flow, state, concurrency, migrations, or new abstractions reduce reviewability. Line count alone is insufficient.
- A change's **decision basis** is the request and the most-specific relevant repository requirements, invariants, principles, conventions, current patterns, tests, configuration, or observable constraints.
- **Technical debt** is a current internal-quality deficiency or compromise that raises future cost, risk, or difficulty; it excludes deferred product work, unselected alternatives, and unrelated improvements.
- **Single Source of Truth** gives each shared value, logic, schema, rule, requirement, rationale, invariant, procedure, convention, or implementation explanation one role-appropriate canonical owner. Semantic duplication includes the same meaning in different words. Reuse, reference, derive, generate, or extract from that owner instead of maintaining parallel authorities. Other documents may give concise context and link to the canonical detail. Duplicate only when required for generated files, migrations, compatibility layers, test fixtures, snapshots, illustrative examples, external protocol boundaries, or necessary summaries; preserve intentional duplication unless changing it is in scope.

## 5. Purpose and scope
This portable, repository-local, reviewable, versioned contract governs repository-wide agent behavior across tools and IDEs. Repository files—not hidden, personal, remote, or tool settings—are authoritative for project behavior, constraints, rules, and documentation structure.
Keep it repository-wide and tool-neutral. Put project behavior in documentation, source, tests, configuration, and executable behavior; put language or framework rules in a focused implementation owner. Include workflows, commands, tool configuration, personal preferences, product automation, or implementation detail here only when repository-wide, tool-neutral, and contractual.

## 6. Instruction layering and tool-specific files
- Keep repository-wide policy in `AGENTS.md`. Tool-specific files may bridge or adapt discovery but must not duplicate, redefine, or drift from it.
- Path-specific instructions may override local conventions in supported scope. Follow tool discovery and precedence; avoid duplicating ancestor guidance. If order or scope is unclear, use diagnostics or list inspected sources before non-trivial work; state material conflicts or uncertainty.
- Follow the tool's hierarchy for personal, organization, IDE, and global instructions; never treat them as repository facts.

## 7. Repository source precedence and conflicts
When repository sources disagree, identify the conflict and governing source; never reconcile silently. Tool or environment limits, legal or safety obligations, and user instructions may add constraints. If implementation conflicts with intended documentation, state it and make the smallest task-appropriate correction. Unless context indicates otherwise, use:
1. Explicit user request, for current scope and outcome.
2. Applicable repository agent instructions, for agent behavior and contract rules, under the current tool's discovery and precedence rules.
3. Security, licensing, CI, deployment, and package metadata, within their domains.
4. Tests and executable behavior, for current implemented behavior.
5. Architecture, requirements, decisions, and engineering documents, for intended behavior; technical-debt records, for known future-change constraints.
6. `README.md`, for entry-point guidance and overview.
7. Comments, snippets, and informal notes, as supporting evidence only; examples are illustrative and non-exhaustive unless explicitly identified as normative.

## 8. Default posture

### 8.1 Hard constraints
- Inspect relevant context and plan before non-trivial work; follow sections 2 and 9.
- Make small, coherent, reviewable, behaviorally complete changes.
- Keep affected artifacts synchronized; never defer required documentation or knowingly leave them inconsistent. State material assumptions, uncertainties, missing context, conflicts, and risks.
- Follow section 3's protected-file rules; do not treat undocumented rules outside the repository as project truth.
- Enforce section 4's Single Source of Truth across code and documentation; reuse or extract shared definitions before duplicating values or logic.
- Do not perform opportunistic refactors, renames, reformatting, dependency upgrades, file moves, or unrelated cleanup, or hide material changes in unrelated files.
- Do not preserve an existing shape merely because it exists when the task requires a better design consistent with section 16.

### 8.2 Preferred style
Prefer simple, explicit, maintainable solutions consistent with repository conventions; apply section 16 only within task scope.

## 9. Planning and context

### 9.1 Planning workflow
For non-trivial work, consult `AGENTS.md`, any documentation index, affected files, and materially relevant adjacent tests, configuration, scripts, or operational documentation. Use section 14 to select canonical owners. Read broader project documentation when the task affects scope, requirements, architecture, repository-wide rules, documentation structure, or multiple domains.
Consult `README.md` for first-run guidance, user overview, quick-start behavior, public positioning, or navigation; it is not required for every internal code change.

### 9.2 Deep-read triggers
If missing context permits a safe, reversible, local change, state minimal safe assumptions and proceed. If it affects public behavior, data integrity, security, irreversible operations, compatibility, production operations, or task intent, request clarification unless best effort is requested. Treat directly relevant missing, incomplete, or contradictory documentation as a defect and improve it within the task. Read canonical owners for each affected domain:
- Scope, goals, non-goals, or supported behavior: overview or project brief and requirements.
- Public behavior, compatibility, protocols, configuration semantics, or operational expectations: requirements and affected topic document.
- Architecture, data flow, boundaries, placement, concurrency, lifecycle, or ownership: architecture and engineering rules.
- Existing decisions, trade-offs, consequences, or future-change constraints affecting the task: relevant decision and technical-debt records.
- Repository-wide coding, Single Source of Truth, testing, or maintainability: engineering rules and implementation references.
- Tests, taxonomy, fixtures, QA commands, coverage, or validation: testing documentation.
- CI, release readiness, workflow dependencies, or automation: workflow and release documentation.
- Deployment, hardening, containers, or operations: relevant Docker, operations, troubleshooting, or security documentation.
- Documentation restructuring, baseline creation, or duplicate-topic cleanup: navigation and affected canonical owners.

### 9.3 Review-before-implementation increments
When a review-before-implementation workflow is active, present each non-trivial outcome as the smallest ordered sequence of independently reviewable increments (section 4). Use one when the whole outcome is reviewable; do not merge separable behaviors, rollout stages, or compatibility phases merely because they share a goal.
State the end state and key risks or trade-offs. For each increment, state goal, behavior, files or components, validation, documentation impact, dependencies, and working state or compatibility. Prefer functional, validated, behaviorally complete increments that remain buildable and usable; preserve unaffected compatibility where practical and isolate breaking steps.
- Present all increments and await selection.
- Once planning permits edits, implement only the selected increment.
- For an unavoidable non-working increment, state why, what remains usable or testable, its minimized scope and duration, and the restoring increment.
- If no division avoids an invalid, unsafe, or misleading state, change nothing; give staging or atomic options and trade-offs, then request direction.
After each, synchronize artifacts, validate and report, leave it commit-ready, and never commit without authorization.
Outside this workflow, section 9.3 adds no decomposition requirements, approval checkpoints, or implementation boundaries; follow section 2 unless staging is requested.

## 10. Execution paths
- When files can be modified outside planning-only workflow, make the smallest authorized, coherent, behaviorally complete change; preserve conventions unless in scope, synchronize documentation, and avoid churn. Proceed unless further authorization is required; obey approval, sandbox, confirmation, and security boundaries.
- When files cannot be modified, provide exact edits, focused snippets, or a concrete patch with paths and locations. Preserve planning, quality, validation, documentation, rationale, and protected-file obligations.

## 11. Code change discipline
Keep code changes minimal, coherent, and behaviorally complete. Inspect relevant implementation, conventions, callers and callees, tests, configuration, documentation, and the smallest safe option. Do not shift complexity into undocumented conventions, hidden coupling, duplication, or implicit behavior.

- Preserve public behavior, APIs, file structure, naming, and conventions unless the task requires change.
- Do not introduce a parallel implementation when an existing one can be corrected or extended.
- Keep related affected artifacts in one coherent change; change one behavioral concern at a time unless concerns are inseparable.
- Fix root causes rather than symptoms.
- Apply Single Source of Truth (sections 4 and 8) to business and domain rules, schemas, constants, and shared logic.
- Preserve or improve error handling, logging, resource lifecycle, concurrency behavior, and security properties.
- Avoid broad generated-file, vendored-file, or formatting-only changes unless directly required; update lock files only when dependency changes require it.
- Add or update tests when behavior changes, defects are fixed, or edge cases are clarified.
- Prefer **Tests as Documentation**: automated test names, setup, actions, and assertions should verify and communicate the expected contract without replacing required project documentation. Unit tests usually use Given/When/Then around public behavior and observable results.
- Remove dead code only when clearly unreachable or directly made obsolete.
- Isolate necessary larger refactors from unrelated functional changes where practical.

## 12. Documentation synchronization and quality
- Write project documentation primarily for humans. Provide a clear entry path for first-time and returning maintainers; keep agent-oriented or source-level precision in focused implementation references, tests, comments, or other code-adjacent material.
- Update documentation in the same cycle as changed behavior, interfaces, architecture, configuration, operations, workflows, or constraints.
- Synchronization is not append-only: remove obsolete text, replace outdated explanations, consolidate semantic duplication, summarize lower-level detail, move material to its canonical owner, and repair cross-references. A code change need not narrate every affected implementation fact.
- Apply section 4 to documentation: each reusable item has one canonical detailed owner; other documents provide only needed context and a link. Treat stale, missing, contradictory, semantically duplicated, or wrongly layered documentation as a defect; determine authority, correct the wrong source, and state remaining uncertainty.
- Examples are illustrative unless explicitly normative. Do not repeat every defect scenario or implementation edge case across document roles; keep exact edge behavior in the narrowest appropriate owner, often tests or a focused subsystem reference.
- Add a technical-debt entry only when explicitly directed to accept a qualifying compromise or document existing debt; never register incidental findings. Update or remove it when scoped work changes or resolves it.
- Canonically document each new repository-wide or reusable rationale, principle, convention, or pattern in the same change. If scope or tool limits prevent it, give the exact edit and follow-up; implementation alone never establishes repository policy.
- A normalization pass covers affected documents and direct cross-references unless explicitly scoped repository-wide. Run it after creating a baseline, changing a document's responsibility, moving content, or changing project-level requirements, architecture, workflow, or engineering rules. Apply section 14, remove contradictions, placeholders, and needless duplication, and verify names, links, and ownership.

## 13. Bootstrap workflow for under-documented repositories
Use only when documentation is insufficient or bootstrapping, reorganization, or expansion is explicitly requested.
- Establish the smallest useful human entry path and canonical owners needed for the project and task. Follow section 14 and repository conventions; add navigation for a non-trivial set and specialized documents only when justified.
- Derive facts from observable code, configuration, tests, scripts, and comments; distinguish them from inferred intent. In empty repositories, mark unknowns, keep claims narrow, and invent no architecture, requirements, workflows, or rules.
- Prefer useful minimums over speculative completeness. Create or refactor one document per reviewable step; move excessive entry-point or high-level detail to the appropriate owner.
- After creating or substantially refactoring a document, pause for human review unless explicitly authorized to continue. Apply section 12 after bootstrapping or substantial reorganization.

## 14. Documentation progression and ownership
Use repository-specific names and structure. Documentation and navigation should normally progress from (1) purpose and capabilities, through (2) system overview and mental model, (3) stable behavior, requirements, architecture, and decisions, (4) implementation references, then (5) operations and troubleshooting. Small projects may combine compatible roles under clear headings; split them when abstraction levels blur or the entry path becomes hard to follow.

`README.md` or an equivalent entry point stays concise and provides identity, initial setup, and navigation. It may summarize facts needed for orientation but links to the detailed owners below:

- **Overview or project brief**: purpose, scope, capabilities, users or operators, goals, non-goals, and a concise system model.
- **Requirements**: externally observable behavior, quality attributes, compatibility, security, reliability, performance, and constraints.
- **Architecture**: components, boundaries, dependencies, data flows, integrations, deployment or runtime models, and durable invariants.
- **Decisions**: context, selected choice, rationale, useful alternatives, and consequences.
- **Engineering rules**: repository-wide implementation, testing, design, naming, and maintainability constraints.
- **Implementation references**: current source-level mechanisms, language or framework details, extension procedures, integrations, and subsystem internals.
- **Operations**: prerequisites, warnings, ordered procedures, success criteria, recovery, monitoring, incidents, and troubleshooting.
- **Tests, code comments, and code-adjacent references**: exact edge cases and implementation-level executable contracts.

Use focused owners for workflow, testing strategy, security, release, and technical debt when warranted. Private helper names, constructor sequencing, caching mechanics, property-forwarding chains, exhaustive algorithm branches, and similar details belong in implementation or code-adjacent references, not requirements or architecture, unless intentionally contractual.

## 15. Output and validation expectations
Reports of analysis, plans, proposed or applied changes, validation, or unresolved items include as applicable:

- Outcome or proposal and approach.
- Affected paths and purposes.
- Decision basis, canonical links, and documentation status or impact.
- Checks run, omitted, or failed, including manual inspection.
- Material assumptions, uncertainties, conflicts, risks, or trade-offs.
- Unresolved follow-up only; invent none.

For each coherent proposal or change, give its decision basis (section 4); related edits may share one. Distinguish documented rules from implementation evidence or inference; never invent support. Link the most specific canonical sources, restating them only for ambiguity, conflict, or an explicit request; if linking is unavailable, give the path and heading.
For an unsupported material choice, identify the new rationale, principle, convention, or pattern and its owner; otherwise give section 12's proposed edit or explain why the choice is intentionally local.
For trivial tasks, briefly report outcome and validation. Run relevant available tests, linters, type checks, formatters, builds, documentation-link checks, examples, or manual inspection. Format only touched files and avoid repository-wide churn. Report unavailable or failed validation; never invent results or claim full validation after failure.
After edits, report paths and purposes; provide full content only on request. If editing was impossible, provide copyable content, a concrete patch, or exact edits.

## 16. Code and engineering preferences
A **design invariant** is a documented constraint that holds unless the task changes its contract and all affected artifacts. A **current pattern** is a documented implementation shape followed by default; it may change when scoped, justified, tested, documented, and compatible with higher-level requirements.
Apply these preferences only to requested code, design, refactoring, or maintainability; they authorize no unrelated redesign, renaming, reformatting, dependency, or architecture changes. Prefer clear, maintainable designs consistent with documented architecture, rules, and conventions.

- Keep implementations simple; fix root causes; avoid unnecessary indirection, abstraction, configurability, or parallel implementations.
- Prefer explicit boundaries, descriptive names, small public interfaces, visible side effects, and encapsulated boundary conditions and edge cases.
- Prefer Locality of Behaviour: make a unit's behavior apparent from its immediate context. Keep behavior-controlling declarations or calls nearby without needless inlining; balance locality with separation of concerns and Single Source of Truth.
- Avoid hidden coupling and logical dependencies between unrelated modules; follow the Law of Demeter when it materially reduces coupling.
- Prefer value objects or explicit domain structures to primitive-heavy designs when appropriate.
- Favor immutability where practical.
- Prefer dependency injection when it improves separation, clarity, or testability.
- Prefer protocols or interfaces over inheritance-heavy designs, and polymorphism over complex conditional dispatch, when clearer.
- Keep configuration at explicit composition, initialization, or boundary layers rather than burying configurable values in low-level implementation code.
- Separate concurrent, asynchronous, or multi-threaded code from ordinary sequential logic when practical.
- Favor existing repository patterns unless they are the problem. Improve a problematic pattern only within scope; identify the affected invariant or pattern, preserve required behavior, update tests and canonical documentation, and state the rationale.

## 17. Tool and IDE caveat
Tools, editors, hosted agents, integrations, or review surfaces may apply `AGENTS.md` unevenly. Preserve its intent; do not duplicate policy in tool-specific files unless requested.
If a tool cannot edit, give exact edits. If it cannot validate or confirm loaded instructions, report the limitation and material uncertainty.
