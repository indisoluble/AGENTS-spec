# Engineering history and decisions

These records explain the system-wide decisions that still guide maintenance. [Architecture](architecture.md) describes the current system, and [authority and change](authority-and-change.md) defines the responsibilities of its owners.

## Engineering authority and the runtime contract

Under the [current authority model](authority-and-change.md#development-time-and-runtime-authority), the [behavioral baseline](../01-behavior/deliverables/baseline.md) owns accepted product intent and constraints, and [contract design](../02-design/deliverables/contract-design.md) owns their selected realization. The delivered `AGENTS.md` retains self-contained runtime authority within the consuming tool's instruction hierarchy and permissions.

The requester authorized the transfer of engineering authority from the frozen contract to `contract-design.md` after an independent migration-fidelity review. The requester-supplied review checked byte-for-byte preservation of the contract, preservation of its operating semantics in the specification, and consistency across documents, including evaluation relationships. It reported **READY FOR TRANSFER DECISION**, with all eight criteria passing and no corrective findings. The requester's explicit reply, **“Authorized”**, covered the transfer alone. Its scope excluded product redesign, acceptance of provisional requirements, and selection of design alternatives. Live-agent compliance and token savings require evidence beyond either the review or the authorization.

## Decisions

Design-specific decisions remain in [decisions and alternatives](../02-design/docs/decisions-and-alternatives.md#architecture-decisions). Evaluator decisions remain in [framework design](../04-evaluations/docs/framework-design.md#engineering-decisions).

### Integrated engineering architecture with focused detailed owners

**Accepted.** The shared architecture explains relationships, boundaries, and dependencies across the project. The root README orients readers and links to that overview. Design, evaluation, and knowledge maintenance each need a focused owner for their detail. A directory listing alone cannot explain how changes in one domain affect another, and rearranging directories solely for navigation disrupts links.

The evaluator lifecycle belongs with the cases, requirements, and evidence needed to interpret a run. [Evaluation documentation ownership](../04-evaluations/docs/framework-design.md#evaluation-documentation-by-maintenance-responsibility) explains how those connections are maintained across operator and maintainer entry points.

### Requirements-led engineering and product/internal separation

**Accepted.** The requester established product requirements as the basis for development and intended evaluation expectations. Inferring accepted intent from implemented clauses or their rubrics would bypass review of the individual requirements. [Behavior](../01-behavior/deliverables/baseline.md) owns accepted outcomes, [Discovery](../01-behavior/deliverables/discovery.md) keeps proposals explicit, and [Design](../02-design/deliverables/contract-design.md) owns selected mechanisms. The requester authorized separate ownership of established requirements and provisional candidates without changing their decision status. Observations of agent behavior and checks of evaluator correctness answer different questions.

Consumer artifacts must remain independently usable, with no references or dependencies into engineering documentation, including optional navigation. Internal requirements cannot supply hidden runtime policy. Under contract §3.6, consumer READMEs locate product documentation and engineering entry points locate engineering knowledge. Each audience can find its own material without a common root entry point or additional consumer duties.

### Responsibility-based BDD organization

**The owner approved the architecture, authorized local implementation, and recorded the completed reorganization as accepted.** Product acceptance has its own [owner-reported scope](../01-behavior/deliverables/baseline.md#behavioral-acceptance-and-editorial-provenance).

Files are grouped by durable responsibility. Discovery, Formulation, and Automation iterate across those owners. One directory per activity would scatter each subject across handoffs and invite competing definitions. A tree organized solely by subject would leave readers without a clear starting point for a behavioral question. The [BDD entry path](authority-and-change.md#bdd-activities-and-complementary-responsibilities) provides that starting point. Passing checks does not confer acceptance, and consumers have no obligation to adopt BDD.

The dedicated `automation/` stage was a rejected alternative. Moving the evaluator to mirror one BDD activity would disrupt its package, fixture, and evidence relationships without improving ownership.

### Separate owners for architecture, authority, and decision rationale

**The requester accepted the structure and authorized local implementation.** The requester's navigation decision records the shared and [contract-design documentation](../02-design/docs/decisions-and-alternatives.md#ownership-of-contract-design-documentation) structures as complete and independently reviewed. The review concerned documentation organization.

[Architecture](architecture.md) explains how the system fits together. [Authority and change](authority-and-change.md) identifies who may decide a change and which owners it affects. This record explains why system-wide choices were made. A single document would reduce cross-references but mix those reading tasks. The requester selected direct links to canonical owners through ordinary Markdown headings. When material moves, maintainers update incoming links without preserving obsolete paths or fragments through forwarding references.

### Four numbered stages and their responsibilities

**The requester accepted the structure and authorized local implementation of stage placement and documentation ownership.** Independent acceptance of the finished implementation is unverified.

Behavior owns accepted intent, discovery, and proposed examples. Design selects mechanisms and explains their rationale. Contract stages the five consumer files. Evaluations exercise an identified candidate and supply observations, assessments, and evidence. Numbering makes that progression visible while allowing findings to reopen questions in any stage.

Root and engineering stage READMEs orient readers. A flat structure would save navigation steps but obscure which artifacts are deliverables and which support their maintenance. Editing guidance that affects multiple stages belongs with shared change authority.

### Stage deliverables and the Contract staging exception

**The requester accepted the structure and authorized local implementation, including the evaluation package rename.** Separate acceptance of the completed implementation is unverified.

Behavior, Design, and Evaluations each have a README for orientation, `docs/` for supporting explanations, and `deliverables/` for substantive artifacts. Prescriptions stay with the rationale needed to apply them. Contract stages exactly five consumer files at its root. Engineering navigation or an extra container there would obscure the delivery boundary. See the [stage layout](architecture.md#current-bdd-first-organization).

The evaluation package itself is `deliverables`. Wrapping a package named `evaluations` in a `deliverables/` directory would add a level with no distinct responsibility. The requester explicitly authorized the import-interface change from `evaluations.*` to `deliverables.*` without compatibility packages, launchers, aliases, or symlinks. Callers must use the current name. Keeping package depth stable preserves relative lookups for the contract, subprocess working directories, and evidence. The operations guide documents the [invocation](../04-evaluations/docs/running-and-reviewing.md#setup-and-running-evaluations) and [retained evidence locations](../04-evaluations/docs/running-and-reviewing.md#retained-evidence).
