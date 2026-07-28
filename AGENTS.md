# AGENTS.md
**Release date:** 2026-07-29 - **Canonical source:** https://github.com/indisoluble/AGENTS-spec

## 1. Canonical status
`AGENTS.md` is the canonical repository-wide baseline for planning, implementation, refactoring, review, validation, and documentation. Path-specific instructions follow the current tool's scope and precedence. `CLAUDE.md` and `.github/copilot-instructions.md` are compatibility bridges, never independent policy sources.

## 2. Operational protocol
Use this protocol for every task, scaled to complexity; avoid elaborate plans for trivial tasks. Select an approach before editing. Enter a tool-specific review-before-implementation mode only when explicitly requested or workflow-required; its output is this contract's planning artifact. Then follow task instructions and the tool's approval model.
1. Classify the task as trivial or non-trivial.
2. Identify protected files, affected artifacts, relevant documentation, and applicable validation.
3. Inspect required context; identify material assumptions, conflicts, missing context, and risks.
4. Before non-trivial edits, state a concise implementation plan; if section 9.3 is active, use its increment sequence.
5. Outside planning-only workflow, apply the smallest coherent, behaviorally complete change authorized by the request or selected increment.
6. Synchronize affected artifacts when required.
7. Run relevant available validation.
8. Report as section 15 requires.

## 3. Protected contract files
`AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` are protected. Modify them only when explicitly requested to change a protected file, contract, or bridge, or apply prior recommendations specific to it.
If only one is requested, do not modify the others unless required or explicitly included. Keep protected-file changes separate from unrelated code, documentation, formatting, dependency, cleanup, or maintenance changes; propose unrequested work separately.

## 4. Terminology and task classification
- **Affected artifacts**: affected code, tests, configuration, and documentation. A **behaviorally complete change** includes all of them and required validation for requested behavior, with no unstated follow-up.
- A task is **non-trivial** if it involves changes to behavior or documentation meaning; public APIs, interfaces, schemas, protocols, or data formats; security, authentication, authorization, secrets, permissions, privacy, concurrency, async behavior, lifecycle, cleanup, error handling, tests, CI, build, packaging, deployment, runtime configuration, or dependencies; multiple logical files, components, or documentation areas; or unclear requirements, missing context, or material risk.
- A task is **trivial** only if local, mechanical, low-risk, and changing no behavior, interface, configuration, dependency, test, documentation meaning, or repository structure.
- A **reviewable change/increment** is one unit a reviewer can understand and verify: intent, rationale, resulting behavior, risks, and validation. Judge size—lines, files, components—and tracing burden; interacting concerns, modules, control flow, state transitions, concurrency, migrations, or new abstractions reduce reviewability. Line count alone is insufficient.
- A change's **decision basis** is the request and any most-specific relevant repository requirements, invariants, principles, conventions, current patterns, tests, configuration, or observable constraints.
- **Technical debt** is a current internal-quality deficiency or compromise that makes future change costlier, riskier, or harder; it excludes deferred product work, unselected alternatives, and unrelated improvements.
- **Single Source of Truth** gives each shared value, logic, schema, rule, requirement, or definition one role-appropriate canonical owner. Code and documentation must reuse, reference, derive, generate, or extract from it, not maintain parallel authorities. Duplicate only when required for generated files, migrations, compatibility layers, test fixtures, snapshots, examples, external protocol boundaries, or concise documentation summaries; preserve intentional duplication unless the task requires changing it.

## 5. Purpose and scope
This portable, repository-local, reviewable, versioned contract governs repository-wide agent behavior across tools and IDEs. Repository files—not hidden, personal, remote, or tool settings—are authoritative for project behavior, constraints, rules, and documentation structure.
Keep it repository-wide and tool-neutral. Put project behavior in documentation, source, tests, configuration, and executable behavior; put language/framework rules in `/docs/implementation-notes.md` or a more specific owner. Include reusable task workflows, slash commands, MCP configuration, personal preferences, product-specific automation, or language/framework detail here only when repository-wide, tool-neutral, and contractual.

## 6. Instruction layering and tool-specific files
- Keep repository-wide policy in `AGENTS.md`. Tool-specific files, including `CLAUDE.md` and `.github/copilot-instructions.md`, may bridge or adapt it but must not duplicate, redefine, or drift from it.
- Path-specific instructions may override local conventions within supported scope. Follow the tool's discovery and precedence; avoid duplicating ancestor guidance. If order or scope is unclear, use diagnostics or list inspected sources before non-trivial work; state material conflicts or uncertainty.
- Follow the tool's hierarchy for personal, organization, IDE, and global instructions; never treat them as repository facts.

## 7. Repository source precedence and conflicts
When repository sources disagree, identify the conflict and governing source; state any material basis and never reconcile silently. Tool or environment limits, legal or safety obligations, and explicit user instructions may add constraints. If implementation conflicts with intended documentation, state it and make the smallest task-appropriate correction. Unless request or context clearly indicates otherwise, use:
1. Explicit user request, for current scope and outcome.
2. Applicable repository agent instructions, for agent behavior and contract rules, under the current tool's discovery and precedence rules.
3. Security, licensing, CI, deployment, and package metadata, within their domains.
4. Tests and executable behavior, for current implemented behavior.
5. Architecture, requirements, decisions, and engineering documents, for intended behavior; technical-debt records, for known future-change constraints.
6. `README.md`, for entry-point guidance and overview.
7. Comments, snippets, and informal notes, as supporting evidence only; examples show one valid use and are non-exclusive unless surrounding documentation requires otherwise.

## 8. Default posture

### 8.1 Hard constraints
- Inspect relevant context and plan before non-trivial work; follow sections 2 and 9.
- Make small, coherent, reviewable, behaviorally complete changes.
- Keep affected artifacts synchronized; never defer required documentation or knowingly leave them inconsistent.
- State material assumptions, uncertainties, missing context, conflicts, and risks.
- Follow section 3's protected-file rules.
- Do not treat undocumented rules outside the repository as project truth.
- Enforce section 4's Single Source of Truth across code and documentation; reuse or extract shared definitions before duplicating values or logic.
- Do not perform opportunistic refactors, renames, reformatting, dependency upgrades, file moves, or unrelated cleanup.
- Do not hide material changes in unrelated files.
- Do not preserve an existing implementation shape or convention merely because it exists when the task explicitly requires a better design and includes section 16's required updates.

### 8.2 Preferred style
Prefer simple, explicit, maintainable solutions consistent with repository conventions; apply section 16 only within task scope.

## 9. Planning and context

### 9.1 Planning workflow
For non-trivial work, always consult `AGENTS.md`; `/docs/table-of-contents.md` if present; affected files; and materially relevant adjacent tests, configuration, scripts, or operational documentation. Use them to select canonical documents; read the full baseline only when the task affects project scope, requirements, architecture, repository-wide engineering rules, documentation structure, or multiple cross-cutting areas.
Consult `README.md` for first-run guidance, user-facing overview, quick-start behavior, public positioning, or documentation navigation; it is not required for every internal code change.

### 9.2 Deep-read triggers
If missing context permits a safe, reversible, local change, state minimal safe assumptions and proceed. If it affects public behavior, data integrity, security, irreversible operations, external compatibility, production operations, or task intent, request clarification unless best effort is requested. Treat directly relevant missing, incomplete, or contradictory documentation as a defect and improve it within the task. Read canonical documents for each affected domain:
- Scope, goals, non-goals, or supported behavior: project brief and requirements.
- Public behavior, compatibility, protocols, configuration semantics, or operational expectations: requirements and affected topic document.
- Architecture, data flow, boundaries, placement, concurrency, lifecycle, or ownership: architecture and engineering rules.
- Existing decisions, trade-offs, consequences, or future-change constraints affecting the task: relevant decision and technical-debt records.
- Repository-wide coding, Single Source of Truth, testing, or maintainability: engineering rules and implementation notes.
- Tests, taxonomy, fixtures, QA commands, coverage, or validation: testing documentation.
- CI, release readiness, workflow dependencies, or automation: workflow and release documentation.
- Deployment, hardening, containers, or operations: relevant Docker, operations, troubleshooting, or security documentation.
- Documentation restructuring, baseline creation, or duplicate-topic cleanup: table of contents and affected canonical owners.

### 9.3 Review-before-implementation increments
When a review-before-implementation workflow is active, present each non-trivial outcome before implementation as the smallest ordered sequence of independently reviewable increments (section 4). Use one increment only when the whole outcome is reviewable; never merge verifiable behaviors, rollout stages, or compatibility phases merely because they share a goal.
State the end state and key risks/trade-offs. For each increment, state its goal, behavior, files/components, validation, documentation impact, dependencies, and working state/compatibility. Prefer functional, validated, behaviorally complete increments that remain buildable/startable/usable through the documented workflow; preserve unaffected behavior/compatibility where practical and isolate breaking steps.
- Present all increments and await selection.
- Once planning permits edits, implement only the selected increment.
- For an unavoidable non-working increment, state why, what remains usable/testable, minimized scope/duration, and restoring increment.
- If no division avoids an invalid, unsafe, or misleading state, change nothing; explain, provide staging/atomic options and trade-offs, and request direction.
After each, sync affected artifacts; validate/report; leave commit-ready; never commit without authorization.
Outside this workflow, section 9.3 adds no decomposition requirements, approval checkpoints, or implementation boundaries; follow section 2 unless staging is requested.

## 10. Execution paths
- When files can be modified outside planning-only workflow, make the smallest authorized, coherent, reviewable, behaviorally complete change; preserve conventions unless the task changes them, synchronize relevant documentation, and avoid churn. Proceed unless the request, tool, environment, or workflow requires further authorization; obey tool-controlled approval, sandbox, confirmation, and security boundaries.
- When files cannot be modified, provide reviewable exact edits, focused snippets, or a concrete patch with paths and replacement locations. Preserve planning, quality, validation, documentation, rationale, and protected-file obligations; use concrete edits when possible.

## 11. Code change discipline
Keep code changes minimal, coherent, and behaviorally complete. Before editing, inspect relevant implementation, conventions, callers, callees, tests, configuration, documentation, and the smallest safe option. Do not shift complexity into undocumented conventions, hidden coupling, duplication, or implicit behavior.

- Preserve public behavior, APIs, file structure, naming, and conventions unless the task requires change.
- Do not perform opportunistic rewrites, renames, formatting sweeps, dependency upgrades, or architectural refactors.
- Do not introduce a parallel implementation when an existing one can be corrected or extended.
- Keep related affected artifacts in one coherent change; change one behavioral concern at a time unless concerns are inseparable.
- Fix root causes rather than symptoms.
- Apply Single Source of Truth (sections 4 and 8) to business and domain rules, schemas, constants, and shared logic.
- Preserve or improve error handling, logging, resource lifecycle, concurrency behavior, and security properties.
- Avoid broad generated-file, vendored-file, or formatting-only changes unless directly required; update lock files only when dependency changes require it.
- Add or update tests when behavior changes, defects are fixed, or edge cases are clarified.
- Prefer **Tests as Documentation**: automated tests whose name, setup, action, and assertions verify and communicate the expected contract. Unit tests should usually use clear Given/When/Then around public behavior and observable results.
- Remove dead code only when clearly unreachable or directly made obsolete.
- Isolate necessary larger refactors from unrelated functional changes where practical.

## 12. Documentation synchronization and normalization
- Update documentation in the same cycle as changed behavior, interfaces, architecture, configuration, operations, workflows, or constraints.
- Add a technical-debt entry only after explicit direction to accept a qualifying compromise or document existing debt; never register incidental findings. Update or remove affected entries when scoped work changes or resolves them.
- Canonically document every new repository-wide or reusable rationale, principle, convention, or pattern in the same change. If scope or tool limits prevent it, give the exact edit and report follow-up; never establish repository policy through implementation alone.
- Treat stale, missing, duplicated, or contradictory documentation as a defect. When it conflicts with implementation, inspect implementation and tests, determine authority, correct the wrong source, and state remaining uncertainty.
- Apply Single Source of Truth: avoid duplicated long-form content; prefer links and concise summaries; preserve concise summaries that intentionally repeat canonical facts for readability.
- A documentation normalization pass covers only affected documents and direct cross-references unless explicitly scoped repository-wide. Run it after creating a baseline, changing a document's primary responsibility, moving content, or changing project-level requirements, architecture, workflow, or engineering rules. Within scope, reconcile `README.md`, relevant `/docs`, and `AGENTS.md`; remove contradictions, obsolete placeholders, and needless duplication; keep `README.md` concise; move detail to focused owners; verify names, links, roles, and separation of requirements, architecture, engineering, and workflow guidance.

## 13. Bootstrap workflow for under-documented repositories
Use only when baseline documentation is insufficient or bootstrapping, reorganization, or expansion is explicitly requested.
- Establish section 14's baseline first; add its table of contents for a non-trivial set, and specialized documents only when content justifies them and they prevent overload.
- Derive facts from observable code, configuration, tests, scripts, and comments; distinguish them from inferred intent. In empty repositories, mark unknowns, keep claims narrow, and invent no architecture, requirements, workflows, or rules.
- Prefer minimal useful documentation over speculative completeness. Create or refactor one document per reviewable step; move non-entry-point `README.md` content to focused `/docs` files.
- After creating or substantially refactoring a document, pause for human review unless explicitly authorized to continue. Normalize after bootstrapping or substantial reorganization.

## 14. Documentation map and placement
`README.md` is the concise entry point for project identity, setup, and deeper links; it must not own requirements, architecture, decisions, engineering or workflow rules, operations, or implementation notes. This map governs documentation only; place other files by architecture, repository convention, and relevant architecture or implementation guidance. Move outgrown content to its owner. Baseline `/docs` documents:

- `/docs/project-brief.md`: purpose, scope, goals, non-goals, users/operators, high-level capabilities.
- `/docs/requirements.md`: functional, operational, quality, compatibility, security, performance, reliability, and constraints.
- `/docs/architecture.md`: system structure, runtime model, boundaries, data flows, integrations, deployment architecture.
- `/docs/engineering-rules.md`: repository engineering principles, coding and naming standards, testing expectations, design and maintainability constraints.
- `/docs/table-of-contents.md`: navigation index when the documentation set is non-trivial.

Specialized documents:

- `/docs/decisions.md` or `/docs/adr/`: decisions, rationale, alternatives, consequences.
- `/docs/technical-debt.md`: current debt, affected areas, future-change costs, remediation direction, and links to related decisions when applicable.
- `/docs/workflow.md`: development, branching, review, CI, release readiness, and collaboration rules.
- `/docs/implementation-notes.md`: language, framework, runtime, module, or integration guidance.
- `/docs/operations.md`: deployment, runtime operations, monitoring, incidents, backup/recovery, production support.
- `/docs/security.md`: threat model, assumptions, secrets, authentication, authorization, vulnerability management.
- `/docs/testing.md`: test strategy, taxonomy, commands, fixtures, coverage expectations, validation rules.
- `/docs/release.md`: versioning, changelog, publication, migrations, compatibility policy.

## 15. Output and validation expectations
Reports of analysis, plans, proposed or applied changes, validation, or unresolved items include as applicable:

- Outcome or proposal and approach.
- Affected paths and purposes.
- Decision basis, canonical links, and documentation status or impact.
- Checks run, omitted, or failed, including manual inspection.
- Material assumptions, uncertainties, conflicts, risks, or trade-offs.
- Unresolved follow-up only; invent none.

For each coherent proposal or change, give its decision basis (section 4); related edits may share one. Distinguish documented rules from implementation evidence or inference; never invent documentary support.
Link only the most specific canonical sources; restate them only when applicability is ambiguous, sources conflict, or explicitly requested. If linking is unavailable, give exact path and heading.
For an unsupported material choice, identify the new rationale, principle, convention, or pattern and where documented; otherwise give section 12's exact proposed edit or explain why it is intentionally local and needs no canonical rule.
For trivial tasks, be brief but report outcome and validation. Run relevant available tests, linters, type checks, formatters, builds, documentation-link checks, example commands, or manual inspection. Format only touched files; avoid repository-wide churn unless requested or required. Report unavailable or failed validation; never claim full validation after failure or invent results.
After modifying files, report paths and purposes; provide complete content only on request. If files could not be modified, provide complete copyable content, a concrete patch, or exact edits.

## 16. Code and engineering preferences
A **design invariant** is a documented constraint that must hold unless the task explicitly changes its contract and updates all affected artifacts. A **current pattern** is a documented implementation shape or convention followed by default; it may change when scoped, justified, tested, documented, and compatible with higher-level requirements.
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
`AGENTS.md` guides agent and chat workflows, but tools, editors, hosted agents, integrations, or review surfaces may apply it unevenly. Preserve its intent; do not duplicate policy in tool-specific files unless explicitly requested.
If a tool cannot edit, provide exact edits. If it cannot validate or confirm loaded instructions, report the limitation and material uncertainty.
