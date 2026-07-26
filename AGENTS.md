# AGENTS.md
**Release date:** 2026-07-26 - **Canonical source:** https://github.com/indisoluble/AGENTS-spec

## 1. Canonical status
`AGENTS.md` is the canonical repository agent contract for planning, implementation, refactoring, review, validation, and documentation; it governs agent behavior when repository instructions overlap or conflict. `.github/copilot-instructions.md` is its compatibility bridge only, never an independent policy source.

## 2. Operational protocol
Use this protocol for every task, scaling it to complexity; for trivial tasks, collapse it without elaborate plans. Planning selects an approach before editing; use a tool-specific Plan mode only if the user explicitly asks or the current tool workflow requires it. Its output is this contract's planning artifact; then follow user instructions and the tool approval model.
1. Classify the task as trivial or non-trivial.
2. Identify protected files, affected artifacts, relevant documentation, and applicable validation.
3. Inspect the required repository context.
4. Identify material assumptions, conflicts, missing context, and risks.
5. Before non-trivial edits, form and state a concise implementation plan; if section 9.3 is active, use its increment sequence.
6. Outside planning-only workflow, apply the smallest coherent, behaviorally complete change authorized by the request or selected increment.
7. Keep affected artifacts synchronized when required.
8. Run relevant available validation.
9. Report the outcome as section 15 requires.

## 3. Protected contract files
`AGENTS.md` and `.github/copilot-instructions.md` are protected. Modify either only when the user explicitly asks to change that file, contract, or bridge, or to apply prior recommendations specific to it.
If only one is requested, do not modify the other unless required or explicitly included. Do not bundle protected-file changes with unrelated code, documentation, formatting, dependencies, cleanup, or maintenance; propose unrequested changes separately.

## 4. Terminology and task classification
- **Affected artifacts**: affected code, tests, configuration, and documentation. A **behaviorally complete change** includes all of them and required validation for requested behavior, with no unstated follow-up.
- A task is **non-trivial** if it involves changes to behavior or documentation meaning; public APIs, interfaces, schemas, protocols, or data formats; security, authentication, authorization, secrets, permissions, privacy, concurrency, async behavior, lifecycle, cleanup, error handling, tests, CI, build, packaging, deployment, runtime configuration, or dependencies; multiple logical files, components, or documentation areas; or unclear requirements, missing context, or material risk.
- A task is **trivial** only if local, mechanical, low-risk, and changing no behavior, interface, configuration, dependency, test, documentation meaning, or repository structure.
- A **reviewable change/increment** is one unit a reviewer can understand and verify: intent, rationale, resulting behavior, risks, and validation. Judge size—lines, files, components—and tracing burden; interacting concerns, modules, control flow, state transitions, concurrency, migrations, or new abstractions reduce reviewability. Line count alone is insufficient.
- A change's **decision basis** is the user request and any most-specific relevant repository requirements, invariants, principles, conventions, current patterns, tests, configuration, or observable constraints.
- **Tests as Documentation** are automated tests that verify and communicate the expected contract through their name, setup, action, and assertions.
- A **documentation normalization pass** covers affected documents and direct cross-references only, unless the user explicitly requests repository-wide cleanup. Documentation is **significant** if it creates a baseline document, changes a document's primary responsibility, moves content, or changes project-level requirements, architecture, workflow, or engineering rules.
- A **design invariant** is a documented constraint that must hold unless the task explicitly changes its contract and updates all affected artifacts. A **current pattern** is a documented implementation shape or convention that should be followed by default; it may change when scoped, justified, tested, documented, and compatible with higher-level requirements.
- An **example** illustrates one valid use or implementation. Do not treat it as exclusive unless surrounding documentation makes it required.
- **Single Source of Truth** gives each shared value, logic, schema, rule, requirement, or definition one role-appropriate canonical owner. Code and documentation must reuse, reference, derive, generate, or extract from it, not maintain parallel authorities. Duplicate only when required for generated files, migrations, compatibility layers, test fixtures, snapshots, examples, external protocol boundaries, or concise documentation summaries; preserve intentional duplication unless the task requires changing it.

## 5. Purpose and scope
This portable, repository-local, reviewable, versioned contract governs repository-wide agent behavior across tools and IDEs. Repository files—not hidden, personal, remote, or tool-specific settings—are authoritative for project behavior, constraints, rules, and documentation structure. Put project behavior in documentation, source, tests, configuration, and executable behavior.
Exclude reusable task workflows, slash commands, MCP server configuration, local personal preferences, product-specific automation, and language/framework detail unless repository-wide, tool-neutral, and contractual. Put language/framework rules in repository documentation, usually `/docs/implementation-notes.md` or a more specific owner; include them here only for language-specific repositories.

## 6. Instruction layering and tool-specific files
- Keep repository-wide policy in `AGENTS.md`; tool-specific instructions, including `.github/copilot-instructions.md`, should be bridges or adapters and must not duplicate, redefine, or drift from it.
- Path-specific instructions may add local conventions where supported but must not contradict this contract; state conflicts and follow `AGENTS.md` unless the user explicitly directs otherwise. Personal, organization, IDE, or tool-global instructions may add preferences but must not override repository-local facts, protected-file rules, validation requirements, or explicit task instructions.
- If a tool combines sources in an unclear order, preserve this contract's intent, avoid duplication, and state material uncertainty. Use available diagnostics or explicitly list repository instruction sources inspected before non-trivial work.

## 7. Repository source precedence and conflicts
When repository sources disagree, identify the conflict and source governing the task; state the basis if material and never reconcile silently. Tool or environment limits, legal or safety obligations, and explicit user instructions may add constraints. If implementation conflicts with intended documentation, state it and make the smallest task-appropriate correction. Unless request or context clearly indicates otherwise, use:
1. Explicit user request, for current scope and outcome.
2. `AGENTS.md`, for agent behavior and contract rules.
3. Security, licensing, CI, deployment, and package metadata, within their domains.
4. Tests and executable behavior, for current implemented behavior.
5. Architecture, requirements, decisions, and engineering documents, for intended behavior.
6. `README.md`, for entry-point guidance and overview.
7. Comments, examples, snippets, and informal notes, as supporting evidence only.

## 8. Default posture

### 8.1 Hard constraints
- Inspect relevant context and plan before non-trivial work; follow sections 2 and 9.
- Make small, coherent, reviewable, behaviorally complete changes.
- Keep affected artifacts synchronized.
- State material assumptions, uncertainties, missing context, conflicts, and risks.
- Follow section 3's protected-file rules.
- Do not treat undocumented rules outside the repository as project truth.
- Enforce Single Source of Truth across code and documentation as defined in section 4.
- Reuse or extract shared definitions before duplicating values or logic.
- Do not perform opportunistic refactors, renames, reformatting, dependency upgrades, file moves, or unrelated cleanup.
- Do not hide material changes in unrelated files.
- Do not defer documentation required by section 12.
- Do not knowingly leave affected artifacts inconsistent.
- Do not preserve a current pattern merely because it exists when the task explicitly requires a better design and includes section 16's required updates.

### 8.2 Preferred style
Prefer simple, explicit, maintainable solutions consistent with repository conventions; apply section 16 only within task scope.

## 9. Planning and context

### 9.1 Planning workflow
Use section 2 for every task. For non-trivial work, always consult `AGENTS.md`; `/docs/table-of-contents.md` if present; affected files; and materially relevant adjacent tests, configuration, scripts, or operational documentation. Use these to select canonical documents. Do not read the full baseline by default unless the task affects project scope, requirements, architecture, repository-wide engineering rules, documentation structure, or multiple cross-cutting areas.
`README.md` should be consulted for first-run guidance, user-facing overview, quick-start behavior, public positioning, or documentation navigation; it is not mandatory for every internal code change.

### 9.2 Deep-read triggers
If missing context permits a safe, reversible, local change, state minimal safe assumptions and proceed. If it affects public behavior, data integrity, security, irreversible operations, external compatibility, production operations, or user intent, stop and ask unless best effort was requested. Treat directly relevant missing, incomplete, or contradictory documentation as debt and improve it within the task. Read each affected domain's canonical documents:
- Scope, goals, non-goals, or supported behavior: project brief and requirements.
- Public behavior, compatibility, protocols, configuration semantics, or operational expectations: requirements and affected topic document.
- Architecture, data flow, boundaries, placement, concurrency, lifecycle, or ownership: architecture and engineering rules.
- Repository-wide coding, Single Source of Truth, testing, or maintainability: engineering rules and implementation notes.
- Tests, taxonomy, fixtures, QA commands, coverage, or validation: testing documentation.
- CI, release readiness, workflow dependencies, or automation: workflow and release documentation.
- Deployment, hardening, containers, or operations: relevant Docker, operations, troubleshooting, or security documentation.
- Documentation restructuring, baseline creation, or duplicate-topic cleanup: table of contents and affected canonical owners.

### 9.3 Plan-mode reviewable increments
When Plan mode or equivalent review-before-implementation workflow is active or selected, present every non-trivial outcome before implementation as the smallest ordered sequence of independently reviewable increments (section 4). Use one increment only if the whole outcome is reviewable; never merge verifiable behaviors, rollout stages, or compatibility phases for a shared goal.
State end state, key risks/trade-offs. For each: goal, behavior, files/components, validation, docs impact, dependencies, working state/compatibility. Prefer functional, validated, behaviorally complete increments remaining buildable/startable/usable through documented workflow; preserve unaffected behavior/compatibility where practical; isolate breaking steps.
- Present all increments and await selection.
- After planning permits edits, implement only the increment the user selects.
- For an unavoidable non-working increment, state why, what remains usable/testable, minimized scope/duration, and restoring increment.
- If no division avoids an invalid, unsafe, or misleading state, change nothing; explain, give staging/atomic options and trade-offs, and ask for direction.
After each, sync affected artifacts; validate/report; leave commit-ready; never commit without authorization.
Otherwise it imposes no decomposition, approval checkpoint, or per-turn boundary; follow section 2 unless the user requests staging.

## 10. Execution paths
Section 15 applies; section 9.3 only during its workflow.

### 10.1 Tools that can modify repository files
Outside planning-only workflow, apply the smallest coherent, reviewable change; preserve conventions unless the task changes them; sync relevant documentation; avoid churn; follow section 3.
Do not ask permission for clearly scoped edits unless the user, tool, environment, or active workflow requires it. The tool or environment controls approvals, sandbox limits, confirmations, and security boundaries; this contract does not override them.

### 10.2 Tools that cannot modify repository files
Outside planning-only workflow, provide exact file edits, focused snippets, or a concrete patch with paths and replacement locations. Keep them reviewable and preserve all planning, quality, validation, documentation, rationale, and protected-file obligations; do not stop at abstractions when concrete edits are possible.

## 11. Code change discipline
Code changes must be minimal, coherent, and behaviorally complete. Before editing, inspect relevant implementation, nearby conventions, callers, callees, tests, configuration, documentation, and the smallest safe option. Do not make code appear cleaner by moving complexity into undocumented conventions, hidden coupling, duplication, or implicit behavior.

- Preserve public behavior, APIs, file structure, naming, and conventions unless the task requires change.
- Do not perform opportunistic rewrites, renames, formatting sweeps, dependency upgrades, or architectural refactors.
- Do not introduce a parallel implementation when an existing one can be corrected or extended.
- Keep related affected artifacts in one coherent change.
- Change one behavioral concern at a time unless concerns are inseparable.
- Fix root causes rather than symptoms.
- Apply Single Source of Truth (sections 4 and 8) to business and domain rules, schemas, constants, and shared logic.
- Preserve or improve error handling, logging, resource lifecycle, concurrency behavior, and security properties.
- Avoid broad generated-file, vendored-file, or formatting-only changes unless directly required.
- Update lock files when dependency changes require it; do not update them incidentally.
- Add or update tests when behavior changes, defects are fixed, or edge cases are clarified.
- Prefer Tests as Documentation; unit tests should usually use clear Given/When/Then around public behavior and observable results.
- Remove dead code only when clearly unreachable or directly made obsolete.
- Isolate necessary larger refactors from unrelated functional changes where practical.

## 12. Documentation synchronization and normalization
Documentation is part of the change. Update it in the same cycle as changed behavior, interfaces, architecture, configuration, operations, workflows, or constraints.
Document every new repository-wide or reusable rationale, principle, convention, or pattern canonically in the same change. If scope or tool limits prevent it, give the exact edit and report it as follow-up; never establish repository policy through implementation alone.
Treat stale, missing, duplicated, or contradictory documentation as a defect. When it conflicts with implementation, inspect implementation and tests, determine authority, correct the wrong source, and state remaining uncertainty.
Apply Single Source of Truth: avoid duplicated long-form content; prefer links and concise summaries; preserve concise summaries that intentionally repeat canonical facts for readability.
After significant documentation creation or refactoring, run section 4's normalization pass. Within scope, reconcile `README.md` and relevant `/docs` cross-references; check consistency with `AGENTS.md`; remove contradictions and obsolete placeholders; reduce unnecessary duplication; keep `README.md` concise; move long-form detail to focused documents; verify names, links, cross-references, document roles, and separation of requirements, architecture, rules, and workflow guidance.

## 13. Bootstrap workflow for under-documented repositories
Use only for insufficient baseline documentation or user-requested bootstrapping, reorganization, or expansion. Establish section 14's baseline first; add its table of contents for a non-trivial set and specialized documents only to prevent overload. In sparse repositories, derive documentation from observable code, configuration, tests, scripts, and comments; distinguish confirmed facts from inferred intent. In empty ones, keep claims narrow and invent no architecture, requirements, workflows, or rules. Normalization is mandatory after bootstrapping or substantial reorganization.

- Create or refactor one document per small, reviewable step; move non-entry-point content from `README.md` into focused `/docs` files.
- Prefer useful minimal documentation to speculative completeness; mark unknowns explicitly, never invent project facts, and create specialized documents only with enough content.
- After creating or substantially refactoring a document, stop for human review unless explicitly authorized to continue.

## 14. Documentation map and placement
`README.md` is the concise entry point for project identity, setup, and deeper links; it must not own requirements, architecture, decisions, engineering or workflow rules, operations, or implementation notes. This section places documentation only; non-documentation files must follow current architecture, repository conventions, and relevant architecture or implementation documents. Move outgrown content to an appropriate owner. Baseline `/docs` documents:

- `/docs/project-brief.md`: purpose, scope, goals, non-goals, users or operators, high-level capabilities.
- `/docs/requirements.md`: functional, operational, quality, compatibility, security, performance, reliability, and constraints.
- `/docs/architecture.md`: system structure, runtime model, boundaries, data flows, integrations, deployment architecture.
- `/docs/engineering-rules.md`: repository-specific engineering principles, coding standards, testing expectations, design constraints, naming rules, and maintainability rules.
- `/docs/table-of-contents.md`: navigation index when the documentation set is non-trivial.

Specialized documents:

- `/docs/decisions.md` or `/docs/adr/`: decisions, rationale, alternatives, consequences.
- `/docs/workflow.md`: development workflow, branching, review, CI, release readiness, and collaboration rules.
- `/docs/implementation-notes.md`: language, framework, runtime, module, or integration guidance.
- `/docs/operations.md`: deployment, runtime operations, monitoring, incidents, backup, recovery, production support.
- `/docs/security.md`: threat model, assumptions, secrets, authentication, authorization, vulnerability management.
- `/docs/testing.md`: test strategy, taxonomy, commands, fixtures, coverage expectations, validation rules.
- `/docs/release.md`: versioning, changelog, publication, migrations, compatibility policy.

## 15. Output and validation expectations
When reporting analysis, plans, proposed or applied changes, validation, or unresolved items, include review-relevant assumptions, uncertainties, affected files, approach, decision basis, documentation status and impact, validation, risks, trade-offs, and follow-up.
For each coherent proposed or applied change, give its decision basis (section 4). Distinguish documented rules from implementation evidence or inference; never invent documentary support. Related edits may share one basis.
For documented support, link only the most specific canonical locations; restate only if applicability is ambiguous, sources conflict, or the user asks. If links are unavailable, give exact path and heading.
For an unsupported material choice, label its rationale, principle, convention, or pattern as new; state where documented, give section 12's exact proposed edit, or explain why it is intentionally local and needs no canonical rule.
For trivial tasks, be brief but retain outcome and validation status. Run relevant available tests, linters, type checks, formatters, builds, documentation-link checks, example commands, or manual inspection. Format only touched files; avoid repository-wide churn unless requested or required. Report unavailable or failed validation; never claim full validation after failure or invent results.
Provide complete copyable file content unless a patch or excerpt was requested. When helpful for review, use:

- Summary: what changed, was concluded, or is proposed.
- Files changed or affected: paths and purposes.
- Rationale and documentation basis: canonical links; new bases and documentation status.
- Validation: checks run, omitted, or failed, and manual inspection.
- Assumptions and risks: material assumptions, uncertainties, conflicts, or trade-offs.
- Follow-up: unresolved items only; do not invent future work.

## 16. Code and engineering preferences
Apply these preferences only when relevant to requested code, design, refactoring, or maintainability; they authorize no unrelated refactoring, redesign, renaming, reformatting, dependency or architecture changes. Prefer clear, maintainable designs consistent with documented architecture, rules, and established repository conventions.

- Keep implementations simple; fix root causes; avoid unnecessary indirection, abstraction, configurability, or parallel implementations.
- Prefer explicit boundaries, descriptive names, small public interfaces, visible side effects, and encapsulated boundary conditions and edge cases.
- Prefer Locality of Behaviour: make a unit's behavior apparent from it and its immediate context. Keep behavior-controlling declarations or calls near affected code without needless inlining; balance locality with separation of concerns and Single Source of Truth.
- Prefer automated tests that document behavior without replacing required project documentation.
- Avoid hidden coupling and logical dependencies between unrelated modules; follow the Law of Demeter when it materially reduces coupling.
- Prefer value objects or explicit domain structures to primitive-heavy designs when appropriate.
- Favor immutability where practical.
- Prefer dependency injection when it improves separation, clarity, or testability.
- Prefer protocols or interfaces over inheritance-heavy designs when appropriate.
- Prefer polymorphism over complex conditional dispatch when it makes the design clearer.
- Keep configuration at explicit composition, initialization, or boundary layers rather than burying configurable values in low-level implementation code.
- Separate concurrent, asynchronous, or multi-threaded code from ordinary sequential logic when practical.
- Favor existing repository patterns unless they are the problem.
- If a current pattern is the problem, improve it within task scope. Such changes must identify the affected invariant or pattern, preserve required behavior, update tests and canonical documentation, and state the rationale.

## 17. Tool and IDE caveat
This contract guides agent and chat workflows; tools, editors, hosted agents, integrations, or review surfaces may apply it unevenly. Preserve its intent; do not duplicate policy in tool-specific files unless the user explicitly requests that trade-off.
If a tool cannot edit, follow section 10.2; cannot validate, follow section 15; cannot confirm loaded instructions, state material uncertainty.
