# System-wide engineering decisions and rationale

These records explain the rationale and scope of choices that affect multiple stages. The current architecture in [`docs/architecture.md`](architecture.md) defines their interfaces. The authority rules ([`docs/authority.md`](authority.md)) identify who may decide changes.

## Architecture decisions

Design-specific decisions remain in decisions and alternatives ([`03.0-design/docs/decisions.md` § Architecture decisions](../03.0-design/docs/decisions.md#architecture-decisions)). Evaluator decisions remain in [`05-evaluation/docs/framework-design.md` § Architecture decisions](../05-evaluation/docs/framework-design.md#architecture-decisions).

### Seven-stage pipeline and shared evaluation engine

**Accepted.** The requester approved the seven-stage architecture after independent critical review of the proposal. Independent verification of the migration identified two findings. Corrective reverification closed both with the disposition **READY FOR MIGRATION ACCEPTANCE**. The requester formally accepted the completed structural migration and its documentation alignment at `a5f69fbc13c74cc301c126d60722bc59ca1a4173`. Acceptance covers the engineering architecture and its migration only. Product acceptance, release and subsequent engineering work each require separate authorization. The verification evidence and its limitations are recorded in [`docs/migration-inventory.md` § Final independent reverification](migration-inventory.md#final-independent-reverification).

**Context and choice.** The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) separated intent, design and realization, but assigned definition of checks, execution and assessment to one Evaluations stage. A requirement can outlast its mechanism. To make it clear which source governs a check, the requester chose independent Acceptance and Conformance stages and a separate integrated Evaluation owner. Clear responsibilities take precedence over minimizing stage count. Consolidation and further engine generalization are deferred.

| Earlier provision | Disposition under the approved successor |
| --- | --- |
| Stage numbering and BDD grouping | Seven sibling stages preserve conceptual progression and iterative feedback. The decimal numbers express proximity. Discovery and Formulation retain separate owners. Automation spans Acceptance, Design, Conformance, Candidate and Evaluation. |
| Combined evaluation owner | Acceptance owns requirements-derived definitions and feasible coverage. Conformance owns complementary mechanism definitions and sole responsibility for redundancy decisions. Evaluation owns suite policy, Candidate binding, execution, evidence, assessments and conclusions. Existing clause-based cases retain provisional placement and original provenance. |
| Evaluator package and shared runtime | The former `deliverables` Python package is superseded. Source-checkout imports use `engine`, `conformance` and `evaluation`. A stage's `deliverables/` remains a location for artifacts. Reusable facilities and their verification live in the root engine. There are no compatibility entry points. |
| Direction of dependencies | Keep the earlier-stage and shared-foundation rule. Apply it to executable and indirect dependencies as well as documentation. The engine is independent of every numbered stage. Inventoried legacy references retain their temporary status. |
| Product authority and delivery | Retain requester decisions, accepted intent, selected mechanisms and recorded trace gaps, historical rationale, and the self-contained five-file Candidate staging exception. Preserve evaluator obligations, case semantics, human-review requirements and historical evidence. |

The current interfaces and the limits of this project's BDD adaptation are maintained in [`docs/architecture.md` § Stage interfaces](architecture.md#stage-interfaces) and [`docs/pipeline.md` § Applying the three practices](pipeline.md#applying-the-three-practices).

### Integrated evaluator ownership correction

**Audit accepted and correction authorized by the requester.** Following the accepted structural migration, the requester accepted the independent semantic ownership audit and authorized Evaluation to take ownership of E13, E25 and E32–E40. These obligations govern integrated execution, named assertion reporting, response and workspace capture, or retention and application of review evidence. E33 and E34 govern named cases even where the engine implements the underlying capabilities.

E18 stays provisionally with scope-discipline because it specifies the specialized comparison, including the fixture-specific greeting-value exception. The nine behavioral definitions retain their qualified Candidate-clause basis. The authorization covers ownership of the eleven requirements and separable operating procedures. Permanent behavioral ownership and any changes to criteria, coverage or evaluator semantics require subsequent decisions. [`docs/migration-inventory.md` § Integrated evaluator ownership correction](migration-inventory.md#integrated-evaluator-ownership-correction)

### Shared guidance for writing and maintaining documentation

**The requester authorized local implementation and accepted the completed shared guidance.** The [shared documentation ownership decision](#focused-owners-for-shared-engineering-documentation) established a conventions reference. It answered where a specification belongs, but gave a contributor little help deciding what was missing or whether a revision was sufficient.

Keep placement, rationale, naming, and retention in the conventions reference ([`docs/documentation.md`](documentation.md)). The writing guide ([`docs/writing-documentation.md`](writing-documentation.md)) helps authors decide what a reader needs. The maintenance guide ([`docs/maintaining-documentation.md`](maintaining-documentation.md)) helps a contributor trace change impact and verify the result. One expanded reference would keep the guidance in a single file but make a local correction harder to look up. Organizing by methodology would scatter one task across several guides. The task split costs a link when a contributor moves from drafting to review. It allows both guides to use the same conventions and stage owners.

For questions the project leaves open, direct contributors to the relevant primary practice. This preserves the distinction between selecting architectural concerns, shaping material for a reader, recording a choice, and defining behavior. The shared guidance first applied those practices within the then-established five stages. Its ownership and authority principles continue under the [seven-stage successor](#seven-stage-pipeline-and-shared-evaluation-engine).

### Focused owners for shared engineering documentation

**The requester authorized local implementation and accepted the completed shared documentation refactoring.** This decision refines the earlier [separation of architecture, authority, and decision rationale](#separate-owners-for-architecture-authority-and-decision-rationale). A contributor tracing the impact of a requirement and one checking who can accept it previously had to navigate the same combined document. Its single entry point saved links but obscured which parts each task needed.

The shared documentation index ([`docs/README.md`](README.md)) provides separate routes to structural interfaces, BDD execution, authority, traceability and evidence, documentation conventions, contributor guidance, and system-wide decisions. Changes to a shared rule have one owner. Readers crossing concerns follow direct links, and stage-specific detail stays with its deliverable or local guide. The index is navigation only.

The requester clarified historical retention. Keep ADRs and their supersession links so a contributor can recover the reasoning behind a choice. Obsolete development narratives can be retired once their lasting knowledge is documented at its current owner. The retention convention ([`docs/documentation.md` § Retaining decisions and current knowledge](documentation.md#retaining-decisions-and-current-knowledge)) preserves the current knowledge, decision scope, and essential rationale those accounts may contain.

### Five-stage BDD-aligned engineering pipeline

**Historical decision.** The [seven-stage successor](#seven-stage-pipeline-and-shared-evaluation-engine) supersedes this numbering, the combined Evaluations owner and the evaluator package placement. The following rationale and table record what the five-stage decision established at the time.

**The requester approved the five-stage architecture, authorized implementation, and accepted that migration.** The decision covered the five-stage allocation and the path changes needed to preserve existing behavior. Product decisions and release authorization retained their separate scope. The current interfaces are maintained in [`docs/architecture.md` § Stage interfaces](architecture.md#stage-interfaces).

The requester chose five stages to make the relationship to [reference BDD](https://cucumber.io/docs/bdd/) explicit and give discovering intent and formulating accepted requirements distinct owners. Clear starting points and limited interfaces make outputs easier to find and reduce what contributors need to know for a local change. Keeping Design, Candidate, and Evaluations distinct preserves the separation of mechanism selection, realization in instructions, and assessment. Sibling directories avoid additional nesting and a new Automation owner or technical handoff. Accepted intent continues to lead development and supply independent evaluation expectations in [`docs/pipeline.md` § Test-first iteration](pipeline.md#test-first-iteration).

The earlier decisions retain their recorded authorization and acceptance status. The table describes their disposition at the five-stage transition.

| Earlier decision | Effect of this decision |
| --- | --- |
| [Responsibility-based BDD organization](#responsibility-based-bdd-organization) | Replaces shared stage ownership for Discovery and Formulation. Retains organization by durable responsibility, iterative BDD across owners, and the rejection of a dedicated `automation/` directory. That alternative would add no distinct responsibility and would disrupt evaluator relationships. |
| [Four numbered stages and their responsibilities](#four-numbered-stages-and-their-responsibilities) | Supersedes the four-stage target and numbering, including combined Behavior ownership. Retains conceptual progression, feedback across owners, and the Design, Candidate, and Evaluations responsibilities. |
| [Stage deliverables and the Candidate staging exception](#stage-deliverables-and-the-candidate-staging-exception) | Replaces the stage names and placement to which the layout applies. Retains the documentation roles, rationale needed to interpret a specification, the five-file Candidate exception, and `deliverables` as the evaluator's Python package. |
| [Requirements-led engineering and product/internal separation](#requirements-led-engineering-and-productinternal-separation) and [engineering authority and the runtime contract](#engineering-authority-and-the-runtime-contract) | Separates Discovery and Formulation ownership. Retains established intent as the basis of development, requirements and design as engineering authorities within their scopes, the self-contained runtime contract and consumer package, and all recorded acceptance and transfer history. |
| [Separate owners for architecture, authority, and decision rationale](#separate-owners-for-architecture-authority-and-decision-rationale) and [documentation conventions within existing owners](#documentation-conventions-within-existing-owners) | Retained the separation of architecture, authority, and rationale and applied the documentation conventions to all five stages. The [focused shared owners](#focused-owners-for-shared-engineering-documentation) refine the allocation of that material. |

### Engineering authority and the runtime contract

Under both the [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) and its [seven-stage successor](#seven-stage-pipeline-and-shared-evaluation-engine), the authority model ([`docs/authority.md` § Development decisions](authority.md#development-decisions)) assigns Discovery ownership of the established objectives and rationale ([`01-discovery/deliverables/objectives-and-rationale.md`](../01-discovery/deliverables/objectives-and-rationale.md)) and Formulation ownership of the accepted requirements and constraints ([`02.0-formulation/deliverables/baseline.md`](../02.0-formulation/deliverables/baseline.md)). [`03.0-design/deliverables/contract-design.md`](../03.0-design/deliverables/contract-design.md) owns their selected realization. The delivered `AGENTS.md` retains self-contained runtime authority within the consuming tool's instruction hierarchy and permissions.

The requester authorized the transfer of engineering authority from the frozen contract to `contract-design.md` after an independent migration-fidelity review. The requester-supplied review checked byte-for-byte preservation of the contract, preservation of its operating semantics in the specification, and consistency across documents, including evaluation relationships. It reported **READY FOR TRANSFER DECISION**, with all eight criteria passing and no corrective findings. The requester's explicit reply, **“Authorized”**, covered the transfer alone. Its scope excluded product redesign, acceptance of provisional requirements, and selection of design alternatives. Live-agent compliance and token savings require evidence beyond either the review or the authorization.

### Integrated engineering architecture with focused detailed owners

**Accepted.** The shared architecture explains relationships, boundaries, and dependencies across the project. The root README orients readers and links to that overview. Design, evaluation, and knowledge maintenance each need a focused owner for their detail. A directory listing alone cannot explain how changes in one domain affect another, and rearranging directories solely for navigation disrupts links.

The evaluator lifecycle belongs with the cases, requirements, and evidence needed to interpret a run. The original decision kept them in one guide. The later evaluation documentation decision ([`05-evaluation/docs/framework-design.md` § Evaluation documentation by maintenance responsibility](../05-evaluation/docs/framework-design.md#evaluation-documentation-by-maintenance-responsibility)) keeps those connections through direct links between the responsible owners.

### Requirements-led engineering and product/internal separation

**Accepted.** The requester established product requirements as the basis for development and intended evaluation expectations. Inferring accepted intent from implemented clauses or their rubrics would bypass review of the individual requirements. Formulation ([`02.0-formulation/README.md`](../02.0-formulation/README.md)) owns accepted outcomes, Discovery ([`01-discovery/deliverables/example-coverage.md`](../01-discovery/deliverables/example-coverage.md)) keeps proposals explicit, and Design ([`03.0-design/deliverables/contract-design.md`](../03.0-design/deliverables/contract-design.md)) owns selected mechanisms. The requester authorized separate ownership of established requirements and provisional candidates without changing their decision status. Observations of agent behavior and checks of evaluator correctness answer different questions.

Consumer artifacts must remain independently usable, with no references or dependencies into engineering documentation, including optional navigation. Internal requirements cannot supply hidden runtime policy. Under contract §3.6, consumer READMEs locate product documentation and engineering entry points locate engineering knowledge. Each audience can find its own material without a common root entry point or additional consumer duties.

The owner authorized separate documentation for objectives and their rationale and for accepted requirements, constraints, and acceptance provenance. The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) assigned those responsibilities to Discovery and Formulation while preserving the product decisions.

### Responsibility-based BDD organization

**The owner approved the original responsibility-based organization, authorized local implementation, and recorded that reorganization as accepted.** Product acceptance has its own owner-reported scope ([`02.0-formulation/docs/acceptance-record.md` § Behavioral acceptance and editorial provenance](../02.0-formulation/docs/acceptance-record.md#behavioral-acceptance-and-editorial-provenance)).

The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) retained grouping by durable responsibility while giving Discovery and Formulation distinct owners. Discovery, Formulation, and Automation iterate across those owners. One directory per activity would scatter each subject across handoffs and invite competing definitions. A tree organized solely by subject would leave readers without a clear starting point for a behavioral question. The BDD entry path ([`docs/pipeline.md` § Applying the three practices](pipeline.md#applying-the-three-practices)) provides that starting point. Passing checks does not confer acceptance, and consumers have no obligation to adopt BDD.

The dedicated `automation/` stage was a rejected alternative. Moving the evaluator to mirror one BDD activity would disrupt its package, fixture, and evidence relationships without improving ownership.

### Separate owners for architecture, authority, and decision rationale

**The requester accepted the structure and authorized local implementation.** The requester's navigation decision records the shared and contract-design documentation ([`03.0-design/docs/decisions.md` § Ownership of contract-design documentation](../03.0-design/docs/decisions.md#ownership-of-contract-design-documentation)) structures as complete and independently reviewed. The review concerned documentation organization.

In the original allocation, architecture described the structure of the system. A combined guide identified who could decide a change and which owners it affected. This record explained the rationale for system-wide choices. The [focused shared owners](#focused-owners-for-shared-engineering-documentation) supersede the combined guide while retaining the separation of reader tasks. A single document would reduce cross-references but mix those reading tasks. The requester selected direct links to canonical owners through ordinary Markdown headings. When material moves, maintainers update incoming links without preserving obsolete paths or fragments through forwarding references.

### Four numbered stages and their responsibilities

**The requester accepted the structure and authorized local implementation of stage placement and documentation ownership.** Independent acceptance of that four-stage implementation is unverified.

The four-stage decision placed intent, discovery, and proposed examples in Behavior. The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) superseded that placement and numbering. At that transition it retained Design ownership of mechanisms and rationale, Candidate staging of the five consumer files, and Evaluations ownership of observations, assessments, and evidence. Numbering expresses a progression that permits feedback to any stage.

Root and engineering stage READMEs orient readers. A flat structure would save navigation steps but obscure which artifacts are deliverables and which support their maintenance. This decision placed editing guidance that affects multiple stages with shared change authority. The cross-stage change guide ([`docs/changing-the-contract.md`](changing-the-contract.md)) now owns that guidance.

### Stage deliverables and the Candidate staging exception

**The requester accepted the structure and authorized local implementation, including the evaluation package rename.** Separate acceptance of that earlier package and directory change is unverified.

Under the original decision, Behavior, Design, and Evaluations each had a README for orientation, `docs/` for supporting explanations, and `deliverables/` for substantive artifacts. Prescriptions stay with the rationale needed to apply them. Candidate stages exactly five consumer files at its root. Engineering navigation or an extra container there would obscure the delivery boundary. The [five-stage decision](#five-stage-bdd-aligned-engineering-pipeline) extended these roles to Discovery and Formulation. See the documentation layout ([`docs/documentation.md` § Choosing the owner](documentation.md#choosing-the-owner)).

Under this earlier decision the evaluation package was named `deliverables`. At the time, wrapping a package named `evaluations` in a `deliverables/` directory would have added a level with no distinct responsibility. The requester explicitly authorized the import-interface change from `evaluations.*` to `deliverables.*` without compatibility packages, launchers, aliases, or symlinks. Callers then used the renamed package. Stable depth preserved relative contract lookups, subprocess working directories and evidence paths. The [seven-stage successor](#seven-stage-pipeline-and-shared-evaluation-engine) replaced that package and its lookup arrangement while retaining the five-file staging exception. The operations guide documents the invocation ([`05-evaluation/docs/running-and-reviewing.md` § Setup and running evaluations](../05-evaluation/docs/running-and-reviewing.md#setup-and-running-evaluations)) and retained evidence locations ([`05-evaluation/docs/running-and-reviewing.md` § Retained evidence](../05-evaluation/docs/running-and-reviewing.md#retained-evidence)).

### Documentation conventions within existing owners

The requester authorized local implementation of the engineering documentation convention ([`docs/documentation.md` § Architecture, decisions, and guides](documentation.md#architecture-decisions-and-guides)) after the documentation audit and architectural review. AGENTS-spec adopts this convention for its own engineering documentation under the existing stage and authority decisions.

Predictable names and topic headings give each README a direct route to an architecture, decision, or guide. A central collection would separate stage-specific decisions from the artifacts they explain. A fixed set of architecture files or guide categories would split coherent tasks and could create competing specifications. Keeping canonical details with their owners requires maintaining incoming references when a document moves.
