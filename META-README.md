# Documentation maintenance for AGENTS-spec

Use this file when editing the repository's documentation. It defines ownership, a short editing workflow, and the checks needed to preserve meaning. It sits outside the ordinary path for learning about or using [AGENTS.md](AGENTS.md) and adds no operating obligations to that contract.

## Document ownership

Keep the three reader-facing guides and this editorial file at the repository root.

| File | Owns |
| --- | --- |
| [AGENTS.md](AGENTS.md) | The self-contained operating contract: exact definitions, requirements, permissions, triggers, conditions, and exceptions. Project facts and commands belong in the adopting project's code and documentation. |
| [CLAUDE.md](CLAUDE.md) and [.github/copilot-instructions.md](.github/copilot-instructions.md) | Discovery and application of the local contract, with permitted non-policy titles and provenance. No independent or duplicated collaboration policy. |
| [README.md](README.md) | Basic adoption: the offering, installation, replacement precautions, adoption checks, a first task, and essential expectations. |
| [README-powerusers.md](README-powerusers.md) | Detailed practical explanations and examples, alignment, continuation, tool compatibility, adoption diagnostics, and recorded provider-documentation check dates. |
| [README-maintainers.md](README-maintainers.md) | The contract's design: attributes, reasons, engineering choices, exact source assignments, trade-offs, portability criteria, and constraints on evolution. |
| `META-README.md` | Documentation responsibilities, permitted overlap, editing procedures, and verification. |

The ordinary reading path starts at `README.md` and branches into practical use or technical understanding. Keep editorial navigation out of that path; contributors can discover this root file directly. “Power users” means readers seeking practical depth, without requiring technical expertise. The maintainer guide documents the contract itself; it is not a contributor onboarding manual.

Provider documentation owns claims about provider behavior. Method references clarify their assigned practices. `AGENTS.md` remains authoritative for the combined collaboration policy; neither a guide nor an external source may silently strengthen, weaken, or extend it. Design constraints in the technical guide inform changes to the artifact and add no hidden duties to ordinary agent tasks.

### Summaries and overlap

Give each fact, procedure, rule, or detailed explanation one authoritative owner. Elsewhere, use a reader-appropriate summary and a direct link. Preserve conditions and exceptions locally when their omission would make that summary misleading.

For example, the basic guide explains that unexpectedly larger work causes a pause. The practical guide explains when this happens and illustrates it. The technical guide explains why authorization alone cannot control unexpected effort. Each serves its reader while deriving the obligation from the same contract clause.

A brief PDSA overview can similarly support a practical example without reproducing the full design rationale. Examples cannot create new thresholds or required artifacts. Avoid copying full procedures, source-assignment tables, or lifecycle descriptions between guides; necessary copies need a clear source and update relationship. Different wording alone does not establish a separate responsibility.

## Editing workflow

1. **Identify the change and its owner.** Separate editorial clarification from changed operating behavior. Any edit to `AGENTS.md` or a bridge, including an editorial edit, follows the [protected-file authorization rule](AGENTS.md#53-instructions-contract-files-and-external-actions). Identify behavior changes explicitly; a README cannot enact them.
2. **Update the authoritative explanation first.** For a clarification, use the relevant contract clauses and current rationale. Preserve each rule's strength, trigger, scope, exception, and meaning.
3. **Follow its dependencies.** Update affected summaries, examples, references, and bridge explanations. Check incoming links throughout the repository when headings or paths move. For a known external reference, consider a forwarding anchor or link instead of retaining a duplicate explanation.
4. **Walk through the reader's task.** Use the paths below to check progression and discoverability. For a substantial rewrite, maintain a temporary map from old content to its new location so unique explanations do not disappear.
5. **Review the complete result.** Apply the checklist below. If the contract changes, also use the technical guide's [design scenarios](README-maintainers.md#assessing-design-changes) and [portability criteria](README-maintainers.md#keeping-the-contract-portable).

Keep current descriptions and useful lasting rationale in their owners. Revision narratives, obsolete alternatives, draft measurements, package fingerprints, and temporary content maps belong in working notes or delivery records. Retain only enduring ownership guidance here. A shorter entry point must not be achieved by quietly dropping necessary explanations from the repository.

## Reader paths

- **Basic guide:** explain the primary benefit sought, give actionable installation steps and a useful first task, then show essential expectations and further reading. A newcomer should be able to adopt the contract using this guide alone.
- **Practical guide:** begin with an ordinary outcome-oriented request and show how the agent handles it. Then explain situations the user may encounter. Put detailed reference material where readers can find it without making it a prerequisite for the first example.
- **Technical guide:** connect design problems with chosen approaches, reasons, trade-offs, and implications for future changes. Keep sufficient method and source detail available for assessing the contract. Keep instructions for maintaining the READMEs here.

Use plain Markdown, descriptive headings, direct links, and tables for comparisons. Introduce terms before depending on them; explain methods where they clarify an action or design choice. Present default behavior before optional requester controls. Introduce the complete PDSA cycle before developing individual activities, and include an example in which findings shape subsequent planning.

There is no numeric length limit for these guides. Assess necessary detail, repetition, navigation, and the combined impression of headings and examples. Accurate sentences still need a reading path that teaches the intended responsibilities. Keep consequential qualifications close to their claims; avoid empty categories, obligatory templates, and formalism that adds no understanding.

## Meaning and evidence checklist

Use this checklist to review the complete change, following the relevant links for detailed explanations.

1. **Purpose and quality.** Each guide's framing identifies prevention of unconstrained token consumption—including unexpectedly heavy use within one increment—as the driving goal. Small, complete commitments, progressive detail, bounded inquiry, material-growth reassessment, and visible results support it. PDSA organizes work and learning; engineering and documentation support quality and retained knowledge. Adequate analysis, relevant dependencies, consistency, and necessary validation remain explicit. Explain the purpose before its limits; a token caveat alone does not preserve it.
2. **Rule strength and authority.** Preserve `MUST`, `SHOULD`, and `MAY`: obligations, strong recommendations with justified exceptions, and permissions. A recommendation's exception cannot bypass a mandatory checkpoint. Distinguish an increment, its report, and approval: completion neither grants new permission nor requires a fresh instruction when existing authorization suffices. Material growth still requires direction before added effort, even under broad authorization. Keep tool hierarchy, permissions, and approval rules authoritative.
3. **Agent responsibilities and workflow.** The agent supplies decomposition, acceptance conditions, validation, effort assessment, and recognition of required requester involvement. Ordinary requests need not repeat these duties. PDSA starts with the request: context gathering, outlining, and increment selection belong to Plan; Study and Act inform later planning. Describe effort factors as assessments, without inventing a numerical scoring scheme or requiring every future increment to be measured and settled in advance. Introduce no unsupported outer/inner process hierarchy. Requester-selected steps, limits, and additional checkpoints remain optional controls.
4. **Completion and learning.** Keep the overall task distinct from its current increment, acceptance conditions distinct from predictions, and validation distinct from assessing the approach. Revising a prediction changes no requirements. Useful learning cannot make missing required behavior complete; a successful sample establishes only what its evidence supports.
5. **Blocking investigations.** Before starting, the agent must establish and state the question, scope, objective, effort limit, and evidence needed. Preserve the actor, trigger, and timing. The contract specifies no universal amount, unit, or formula and does not require approval of every limit. Examples illustrate concrete bounds without creating defaults. Obtaining the evidence and exhausting the allowance both stop inquiry; unmet acceptance conditions still require an incomplete-work report. Neither a limit nor a negative result grants additional permission. Keep broader-research and material-growth conditions visible. The [practical explanation](README-powerusers.md#when-an-investigation-is-needed) owns the full account.
6. **Conditional work and documentation scope.** Preserve the conditions on tests, ADRs, guides, continuation records, and engineering techniques. No method creates a deliverable for every task. Coverage expectations grant no permission for project-wide audits, backfills, or reorganization. Keep the difference between assessment and authorized edits clear.
7. **Coverage and audience.** Installation, file placement, replacement precautions, adoption checks, and a useful first task remain available in the basic guide. Practical detail remains discoverable in the power-user guide. Rationale, exact source assignments, constraints, and trade-offs remain sufficient to inform evolution of the contract. Unique human explanations must survive consolidation; editorial procedures stay here.
8. **Sources and evidence.** Preserve primary-source links and exact attribution using the technical guide's [source assignments](README-maintainers.md#principles-and-reference-boundaries). Do not import an entire framework or stronger source rhetoric as policy. Retain original provider-check dates when moving guidance; record a new date only for a newly verified or changed claim. Editorial work does not refresh external evidence.
9. **Limits of claims.** Keep token control best effort, instruction compliance uncertain, and tool controls authoritative. Introduce no quota, automatic token-accounting duty, mandatory pause after every increment, promotional guarantee, or unsupported compatibility claim. Textual consistency does not establish measured comprehension, equivalent agent behavior, or token savings.
10. **Links and delivery.** Check Markdown, relative paths, anchors, incoming links, and delivered file versions against the intended repository layout. Confirm detailed knowledge has one owner and summaries agree. If `AGENTS.md` changes, measure the whole file against its separate byte and line criteria. Counts can support review; automated enforcement is not required. Keep transient contract-size snapshots and remaining-space claims out of the READMEs.
