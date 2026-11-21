# System-wide engineering decisions and rationale

These records explain system-wide choices and their history. [Architecture](architecture.md) distinguishes the implemented layout from the approved target. [Authority and change](authority-and-change.md) defines decision authority and change guidance.

## Architecture decisions

Design-specific decisions remain in [decisions and alternatives](../02-design/docs/decisions.md#architecture-decisions). Evaluator decisions remain in [framework design](../04-evaluations/docs/framework-design.md#architecture-decisions).

### Five-stage BDD-aligned engineering pipeline

**The requester approved the target architecture and authorized this documentation increment.** The [approved target](architecture.md#approved-five-stage-target) establishes five sibling stages at the repository root. The [implemented four-stage layout](architecture.md#implemented-four-stage-architecture) remains in use. [Migration and its verification](architecture.md#migration-from-the-implemented-layout) are future implementation work requiring separate authorization. Acceptance of the completed migration is a separate decision based on that work. Product acceptance, redesign, evaluator changes, and release remain outside this authorization.

The requester chose five stages to make the relationship to [reference BDD](https://cucumber.io/docs/bdd/) explicit and give discovering intent and formulating accepted requirements distinct owners. Clear starting points and limited interfaces make outputs easier to find and reduce what contributors need to know for a local change. Keeping Design, Candidate, and Evaluations distinct preserves the separation of mechanism selection, realization in instructions, and assessment. Sibling directories avoid additional nesting and a new Automation owner or technical handoff. Accepted intent continues to lead development and supply independent evaluation expectations in the [test-first iteration](authority-and-change.md#test-first-iteration).

The following changes apply to the target. The earlier records retain their original scope and status.

| Earlier decision | Effect of this decision |
| --- | --- |
| [Responsibility-based BDD organization](#responsibility-based-bdd-organization) | Replaces shared stage ownership for Discovery and Formulation. Retains organization by durable responsibility, iterative BDD across owners, and the rejection of a dedicated `automation/` directory. That alternative would add no distinct responsibility and would disrupt evaluator relationships. |
| [Four numbered stages and their responsibilities](#four-numbered-stages-and-their-responsibilities) | Supersedes the four-stage target and numbering, including combined Behavior ownership. Retains conceptual progression, feedback across owners, and the Design, Candidate, and Evaluations responsibilities. |
| [Stage deliverables and the Candidate staging exception](#stage-deliverables-and-the-candidate-staging-exception) | Replaces the stage names and placement to which the layout applies. Retains the documentation roles, rationale needed to interpret a specification, the five-file Candidate exception, and `deliverables` as the evaluator's Python package. |
| [Requirements-led engineering and product/internal separation](#requirements-led-engineering-and-productinternal-separation) and [engineering authority and the runtime contract](#engineering-authority-and-the-runtime-contract) | Reassigns the combined Behavior ownership in the target interfaces. Retains established intent as the basis of development, requirements and design as engineering authorities within their scopes, the self-contained runtime contract and consumer package, and all recorded acceptance and transfer history. The earlier document split within Behavior continues to describe the implemented layout. |
| [Separate owners for architecture, authority, and decision rationale](#separate-owners-for-architecture-authority-and-decision-rationale) and [documentation conventions within existing owners](#documentation-conventions-within-existing-owners) | Both decisions continue to apply. Architecture owns pipeline and interfaces, authority and change owns authority and traceability, and this record owns decision rationale. Existing documentation conventions apply to the target owners. |

### Engineering authority and the runtime contract

Under the [current authority model](authority-and-change.md#development-time-and-runtime-authority), Behavior owns the [established objectives and rationale](../01-behavior/deliverables/objectives-and-rationale.md) and the [accepted requirements and constraints](../01-behavior/deliverables/baseline.md). [Contract design](../02-design/deliverables/contract-design.md) owns their selected realization. The delivered `AGENTS.md` retains self-contained runtime authority within the consuming tool's instruction hierarchy and permissions.

The requester authorized the transfer of engineering authority from the frozen contract to `contract-design.md` after an independent migration-fidelity review. The requester-supplied review checked byte-for-byte preservation of the contract, preservation of its operating semantics in the specification, and consistency across documents, including evaluation relationships. It reported **READY FOR TRANSFER DECISION**, with all eight criteria passing and no corrective findings. The requester's explicit reply, **“Authorized”**, covered the transfer alone. Its scope excluded product redesign, acceptance of provisional requirements, and selection of design alternatives. Live-agent compliance and token savings require evidence beyond either the review or the authorization.

The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) separates the combined Behavior ownership in the target. The authority distinctions and the scope of the historical transfer continue to apply.

### Integrated engineering architecture with focused detailed owners

**Accepted.** The shared architecture explains relationships, boundaries, and dependencies across the project. The root README orients readers and links to that overview. Design, evaluation, and knowledge maintenance each need a focused owner for their detail. A directory listing alone cannot explain how changes in one domain affect another, and rearranging directories solely for navigation disrupts links.

The evaluator lifecycle belongs with the cases, requirements, and evidence needed to interpret a run. The original decision kept them in one guide. The later [evaluation documentation decision](../04-evaluations/docs/framework-design.md#evaluation-documentation-by-maintenance-responsibility) keeps those connections through direct links between the responsible owners.

### Requirements-led engineering and product/internal separation

**Accepted.** The requester established product requirements as the basis for development and intended evaluation expectations. Inferring accepted intent from implemented clauses or their rubrics would bypass review of the individual requirements. [Behavior](../01-behavior/README.md) owns accepted outcomes, [Discovery](../01-behavior/deliverables/discovery.md) keeps proposals explicit, and [Design](../02-design/deliverables/contract-design.md) owns selected mechanisms. The requester authorized separate ownership of established requirements and provisional candidates without changing their decision status. Observations of agent behavior and checks of evaluator correctness answer different questions.

Consumer artifacts must remain independently usable, with no references or dependencies into engineering documentation, including optional navigation. Internal requirements cannot supply hidden runtime policy. Under contract §3.6, consumer READMEs locate product documentation and engineering entry points locate engineering knowledge. Each audience can find its own material without a common root entry point or additional consumer duties.

The owner subsequently authorized a documentation split within Behavior. [Objectives and rationale](../01-behavior/deliverables/objectives-and-rationale.md) records the established objectives, their priorities and qualifications, and R1–R5. The [baseline](../01-behavior/deliverables/baseline.md) retains BR1–BR10, PR1, established constraints, and their acceptance and editorial provenance. The authorization covers documentation ownership and preserves the existing product decisions.

The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) replaces the combined Behavior ownership in the target. Requirements-led development and the product/internal separation continue to apply.

### Responsibility-based BDD organization

**The owner approved the architecture, authorized local implementation, and recorded the completed reorganization as accepted.** Product acceptance has its own [owner-reported scope](../01-behavior/deliverables/baseline.md#behavioral-acceptance-and-editorial-provenance).

Files are grouped by durable responsibility. Discovery, Formulation, and Automation iterate across those owners. One directory per activity would scatter each subject across handoffs and invite competing definitions. A tree organized solely by subject would leave readers without a clear starting point for a behavioral question. The [BDD entry path](authority-and-change.md#bdd-activities-and-complementary-responsibilities) provides that starting point. Passing checks does not confer acceptance, and consumers have no obligation to adopt BDD.

The dedicated `automation/` stage was a rejected alternative. Moving the evaluator to mirror one BDD activity would disrupt its package, fixture, and evidence relationships without improving ownership.

The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) supersedes the earlier shared placement of Discovery and Formulation for the target. The rationale for organizing by durable responsibility and the rejection of a dedicated Automation directory still apply.

### Separate owners for architecture, authority, and decision rationale

**The requester accepted the structure and authorized local implementation.** The requester's navigation decision records the shared and [contract-design documentation](../02-design/docs/decisions.md#ownership-of-contract-design-documentation) structures as complete and independently reviewed. The review concerned documentation organization.

[Architecture](architecture.md) explains how the system fits together. [Authority and change](authority-and-change.md) identifies who may decide a change and which owners it affects. This record explains why system-wide choices were made. A single document would reduce cross-references but mix those reading tasks. The requester selected direct links to canonical owners through ordinary Markdown headings. When material moves, maintainers update incoming links without preserving obsolete paths or fragments through forwarding references.

### Four numbered stages and their responsibilities

**The requester accepted the structure and authorized local implementation of stage placement and documentation ownership.** Independent acceptance of the finished implementation is unverified.

Behavior owns accepted intent, discovery, and proposed examples. Design selects mechanisms and explains their rationale. Candidate stages the five consumer files. Evaluations exercise an identified candidate and supply observations, assessments, and evidence. Numbering makes that progression visible while allowing findings to reopen questions in any stage.

Root and engineering stage READMEs orient readers. A flat structure would save navigation steps but obscure which artifacts are deliverables and which support their maintenance. Editing guidance that affects multiple stages belongs with shared change authority.

The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) supersedes the count, numbering, and combined Behavior ownership for the target. This record still describes the current stage placement. The earlier concern about distinguishing deliverables from supporting knowledge still applies within the target's sibling stage directories.

### Stage deliverables and the Candidate staging exception

**The requester accepted the structure and authorized local implementation, including the evaluation package rename.** Separate acceptance of the completed implementation is unverified.

Behavior, Design, and Evaluations each have a README for orientation, `docs/` for supporting explanations, and `deliverables/` for substantive artifacts. Prescriptions stay with the rationale needed to apply them. Candidate stages exactly five consumer files at its root. Engineering navigation or an extra container there would obscure the delivery boundary. See the [implemented stage layout](architecture.md#implemented-four-stage-architecture).

The evaluation package itself is `deliverables`. Wrapping a package named `evaluations` in a `deliverables/` directory would add a level with no distinct responsibility. The requester explicitly authorized the import-interface change from `evaluations.*` to `deliverables.*` without compatibility packages, launchers, aliases, or symlinks. Callers must use the current name. Keeping package depth stable preserves relative lookups for the contract, subprocess working directories, and evidence. The operations guide documents the [invocation](../04-evaluations/docs/running-and-reviewing.md#setup-and-running-evaluations) and [retained evidence locations](../04-evaluations/docs/running-and-reviewing.md#retained-evidence).

The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) replaces stage placement in the target. The documentation roles, Candidate exception, and Python package decision continue to apply.

### Documentation conventions within existing owners

The requester authorized local implementation of the [engineering documentation convention](authority-and-change.md#engineering-documentation-convention) after the documentation audit and architectural review. AGENTS-spec adopts this convention for its own engineering documentation under the existing stage and authority decisions.

Predictable names and topic headings give each README a direct route to an architecture, decision, or guide. A central collection would separate stage-specific decisions from the artifacts they explain. A fixed set of architecture files or guide categories would split coherent tasks and could create competing specifications. Keeping canonical details with their owners requires maintaining incoming references when a document moves.
