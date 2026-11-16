# Engineering history and decisions

These records retain system-wide decisions whose reasons or consequences still guide maintenance. [Architecture](architecture.md) describes the current system; [authority and change](authority-and-change.md) defines current maintenance guidance. Earlier layouts, full migration records, and intermediate ownership transfers remain in [the pre-extraction architecture at `62a407e`](https://github.com/indisoluble/AGENTS-spec/blob/62a407ea4d4177c67c39d7a761645f6d3bbd1abc/docs/architecture.md) and Git history.

## Temporary migration authority

During the source-of-truth migration, a frozen root `AGENTS.md` fixed current operating semantics; transfer required byte preservation and independent semantic and cross-document verification. After independent verification reported **READY FOR TRANSFER DECISION**, the requester explicitly replied **“Authorized”** on **8 November 2026**, transferring engineering authority to `contract-design.md`. The transfer is recorded in [`809e231`](https://github.com/indisoluble/AGENTS-spec/commit/809e231919c349b1ec3039ad3669dc88cf8b6e35).

The temporary freeze ended; it was not a permanent prohibition on separately authorized evolution. The transfer neither redesigned behavior nor accepted provisional product requirements or design alternatives. Delivered `AGENTS.md` retained self-contained runtime authority. The [current authority model](authority-and-change.md#development-time-and-runtime-authority) maintains that distinction.

## Decisions

Design-specific decisions remain in [decisions and alternatives](../02-design/docs/decisions-and-alternatives.md#architecture-decisions); evaluator decisions remain in [framework design](../04-evaluations/docs/framework-design.md#engineering-decisions). Structural implementation authorization below does not itself establish independent acceptance of the completed migration.

### Integrated engineering architecture with focused detailed owners

**Status: accepted.** Separate documents explained contract design and evaluation, but none explained the engineering project as a whole. A system overview was added for relationships, boundaries, and dependencies, with focused owners for design, evaluation, and knowledge maintenance. The README remained orientation, avoiding a second architecture there. Adding folders alone would not explain those relationships and would disrupt existing links.

Evaluation documentation was initially kept integrated so case criteria, evaluator requirements, lifecycle, and evidence stayed connected; length alone did not justify splitting them. The later [evaluation-documentation decision](../04-evaluations/docs/framework-design.md#evaluation-documentation-by-maintenance-responsibility-15-november-2026) separates maintenance responsibilities while preserving those connections. Moving detailed evaluator lifecycle material into shared architecture remains inappropriate because its execution and evidence context belongs with evaluations.

### Requirements-led engineering and product/internal separation

**Status: accepted.** Cases and rubrics referred to implemented clauses without separately identifying product intent. The decision made product requirements the basis for development and intended evaluation expectations, distinguished from design, runtime instructions, observations, and evaluator verification. Treating implemented wording wholesale as accepted intent was rejected. Requirements were initially colocated with design; later transfers established the current Behavior and Design owners.

Consumer artifacts must remain independently usable, with no references or dependencies into engineering documentation, including optional navigation. Internal requirements cannot supply hidden runtime policy. The scoped interpretation of contract §3.6 gives each audience its own navigation: consumer READMEs locate product documentation, while engineering entry points locate engineering knowledge. The clause's reference to `README.md` does not require a single root entry for both audiences. This interpretation adds no consumer duties.

### BDD-first reorganization (13 November 2026)

**Status: architecture and Phase 1 implementation approved; Phase 1 later recorded as complete and accepted.** The owner's 13 November assignment adopted *AGENTS-spec · BDD-first development with files grouped by responsibility* against [`4e44bd2`](https://github.com/indisoluble/AGENTS-spec/commit/4e44bd2c03d2e708654f5060705398e630d0dace). The 14 November Phase 2 assignment records Phase 1 acceptance; [baseline provenance](../01-behavior/deliverables/baseline.md#phase-2-acceptance-and-editorial-provenance) records its separately accepted BR formalization.

Group files by durable responsibility while using iterative BDD activities to develop behavior. A directory per activity would scatter subjects and encourage stage handoffs or competing definitions. A purely knowledge-oriented tree would preserve owners but obscure where a behavioral question starts. Responsibility owners with a short BDD entry path address both concerns. The organization supports iteration without imposing BDD on consumers or granting acceptance through passing checks.

The evaluator initially stayed in its existing package to avoid disturbing fixture, package, and evidence relationships merely to create an `automation/` stage. The numbered and uniform-stage decisions below later changed placement deliberately.

### Shared engineering documentation extraction (15 November 2026)

**Status: structure accepted and local implementation authorized; completion and independent review recorded by the later navigation assignment.** The requester approved extraction against [`62a407e`](https://github.com/indisoluble/AGENTS-spec/commit/62a407ea4d4177c67c39d7a761645f6d3bbd1abc).

Separate three reading tasks: current architecture, authority/change guidance, and useful history. Keeping them together reduced links but made returning maintainers read unrelated material. The split retains one canonical explanation per concept, at the cost of maintaining direct references; it refines physical ownership rather than product or runtime authority.

The subsequent *Remove Unnecessary HTML Anchors* assignment records documentation Steps 1 and 2 as complete and independently reviewed. It superseded the original compatibility-path and fragment-preservation constraint: navigation uses ordinary Markdown headings and direct canonical links, without requiring compatibility forwarding.

### Numbered pipeline and documentation ownership (15 November 2026)

**Status: structure accepted; local implementation authorized** against [`2104f19`](https://github.com/indisoluble/AGENTS-spec/commit/2104f19c9e45d44127beee4584e9d4c3e661d34c).

Number Behavior, Design, Contract, and Evaluations to expose conceptual progression while retaining iterative feedback. Concise root and stage READMEs orient readers; supporting metadata is separated from substantive artifacts. This improves entry paths at the cost of path and working-directory updates. Shared editing guidance belongs with cross-stage authority, rather than Behavior alone.

The evaluator was nested under `04-evaluations/` with its original `evaluations` namespace to preserve its import interface without compatibility packages or launchers. That namespace choice was explicitly superseded by the uniform-stage decision below; it is not a current compatibility constraint.

### Uniform stage structure and deliverables (15 November 2026)

**Status: structure accepted; local implementation and package rename authorized** against [`71f1cf4`](https://github.com/indisoluble/AGENTS-spec/commit/71f1cf4ebb13c5214fb884524e47cc78f0afaa16).

Give engineering stages a README, supporting `docs/`, and substantive `deliverables/`, as shown in [current architecture](architecture.md#current-bdd-first-organization). Keep prescriptions with their necessary rationale. Contract remains the five-file exception: engineering navigation or container directories would obscure its consumer staging boundary.

Rename the evaluation package to `deliverables`, superseding namespace preservation above. Wrapping an unchanged inner package would add a hierarchy level without a separate responsibility; compatibility packages, launchers, aliases, and symlinks were not introduced. The package stayed at the same depth, preserving parent calculations for contract lookup, subprocess working directories, and evidence. Commands run from `04-evaluations/`; new evidence stays outside the package in `.eval-runs/`, and historical evidence remains in place. [Operations](../04-evaluations/docs/running-and-reviewing.md#setup-and-running-evaluations) owns current commands, including `python -m deliverables`.
