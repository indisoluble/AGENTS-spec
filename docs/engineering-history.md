# Engineering history and decisions

These records explain the system-wide decisions that still guide maintenance. [Architecture](architecture.md) describes the current system, and [authority and change](authority-and-change.md) defines the responsibilities of its owners.

## Temporary migration authority

The frozen root `AGENTS.md` governed operating semantics during the transfer to an engineering specification. Transfer required byte-for-byte preservation of the contract and independent verification of semantic coverage and cross-document consistency, including evaluation relationships. The requester-supplied independent review reported **READY FOR TRANSFER DECISION**. On **8 November 2026**, after that review, the requester explicitly replied **“Authorized”**, transferring engineering authority to `contract-design.md`.

That authorization ended the freeze. Its scope excluded product redesign, acceptance of provisional requirements, and selection of design alternatives. The review assessed preservation of the existing contract and its engineering description. The delivered `AGENTS.md` retained self-contained runtime authority. The [current authority model](authority-and-change.md#development-time-and-runtime-authority) identifies the owners of product intent and design and the authority needed for changes.

## Decisions

Design-specific decisions remain in [decisions and alternatives](../02-design/docs/decisions-and-alternatives.md#architecture-decisions). Evaluator decisions remain in [framework design](../04-evaluations/docs/framework-design.md#engineering-decisions). Each status below identifies what the requester approved and any separately recorded review or acceptance of the implementation.

### Integrated engineering architecture with focused detailed owners

**Status: accepted.** Separate documents explained contract design and evaluation, but none explained the engineering project as a whole. A system overview was added for relationships, boundaries, and dependencies, with focused owners for design, evaluation, and knowledge maintenance. The README remained orientation, avoiding a second architecture there. Adding folders alone would not explain those relationships and would disrupt existing links.

Evaluation documentation was initially kept integrated so case criteria, evaluator requirements, lifecycle, and evidence stayed connected; length alone did not justify splitting them. The later [evaluation-documentation decision](../04-evaluations/docs/framework-design.md#evaluation-documentation-by-maintenance-responsibility-15-november-2026) separates maintenance responsibilities while preserving those connections. Moving detailed evaluator lifecycle material into shared architecture remains inappropriate because its execution and evidence context belongs with evaluations.

### Requirements-led engineering and product/internal separation

**Status: accepted.** Cases and rubrics referred to implemented clauses without separately identifying product intent. The requester established product requirements as the basis for development and intended evaluation expectations. Treating implemented wording wholesale as accepted intent was rejected because it would bypass review of the individual requirements. [Behavior](../01-behavior/deliverables/baseline.md) owns accepted intent, and [Design](../02-design/deliverables/contract-design.md) owns the selected mechanisms. Observing agent behavior and verifying the evaluator answer separate questions.

Consumer artifacts must remain independently usable, with no references or dependencies into engineering documentation, including optional navigation. Internal requirements cannot supply hidden runtime policy. The scoped interpretation of contract §3.6 gives each audience its own navigation: consumer READMEs locate product documentation, while engineering entry points locate engineering knowledge. The clause's reference to `README.md` does not require a single root entry for both audiences. This interpretation adds no consumer duties.

### BDD-first reorganization (13 November 2026)

**Architecture approved and local implementation authorized.** On 13 November the owner adopted BDD-first development with files grouped by responsibility. On 14 November the owner recorded that this reorganization was complete and accepted. The separate [behavioral acceptance summary](../01-behavior/deliverables/baseline.md#behavioral-acceptance-and-editorial-provenance) identifies the product outcomes the owner reported as accepted.

Group files by durable responsibility while using iterative BDD activities to develop behavior. A directory per activity would scatter subjects and encourage stage handoffs or competing definitions. A purely knowledge-oriented tree would preserve owners but obscure where a behavioral question starts. Responsibility owners with a short BDD entry path address both concerns. The organization supports iteration without imposing BDD on consumers or granting acceptance through passing checks.

A dedicated `automation/` stage was considered. Moving the evaluator solely to mirror a BDD activity would disrupt package, fixture, and evidence relationships without improving ownership.

### Shared engineering documentation extraction (15 November 2026)

**Structure accepted and local implementation authorized.** The requester's navigation decision subsequently recorded both the shared engineering split and the [contract-design split](../02-design/docs/decisions-and-alternatives.md#contract-design-documentation-extraction-15-november-2026) as complete and independently reviewed.

The shared documents serve three reading tasks. Maintainers can look up the current system, determine who can authorize a change and which owners it affects, or recover the reasons for a decision. One document reduced links but mixed reading tasks. The split gives each subject a canonical home at the cost of maintaining direct references.

The requester also superseded the requirement to preserve obsolete paths and fragments through forwarding links. Navigation uses ordinary Markdown headings and links directly to canonical owners.

### Numbered pipeline and documentation ownership (15 November 2026)

**Structure accepted and local implementation authorized by the requester.** The authorization covers stage placement and documentation ownership. It does not record independent acceptance of the finished implementation.

Numbering Behavior, Design, Contract, and Evaluations makes conceptual progression visible while allowing iterative feedback. Concise root and stage READMEs orient readers. Keeping all documents at the same level would save navigation steps but obscure the distinction between deliverables and supporting guidance. Shared editing guidance belongs with cross-stage authority because changes can affect several owners.

The decision retained the `evaluations` package name to preserve imports without a compatibility package. The [uniform stage decision](#uniform-stage-structure-and-deliverables-15-november-2026) superseded that part of the design.

### Uniform stage structure and deliverables (15 November 2026)

**Structure accepted and local implementation authorized, including the package rename.** The requester explicitly authorized changing the import interface. The decision record establishes no separate acceptance of the completed implementation.

Give engineering stages a README, supporting `docs/`, and substantive `deliverables/`, as shown in [current architecture](architecture.md#current-bdd-first-organization). Keep prescriptions with their necessary rationale. Contract remains the five-file exception: engineering navigation or container directories would obscure its consumer staging boundary.

The evaluation package itself is named `deliverables`. Wrapping the old package in a directory of that name would add a level without a distinct responsibility. The approved rename dispensed with compatibility packages, launchers, aliases, and symlinks. Keeping the same package depth preserves relative lookups for the contract, subprocess working directories, and evidence. [Operations](../04-evaluations/docs/running-and-reviewing.md#setup-and-running-evaluations) owns the current commands and [locations of retained evidence](../04-evaluations/docs/running-and-reviewing.md#retained-evidence).
