# Documentation maintenance for AGENTS-spec

This file contains editorial instructions for people and agents maintaining the repository's documentation. It sits outside the ordinary reading path for learning about or using `AGENTS.md`.

The product is [AGENTS.md](AGENTS.md). Its bridges enable discovery and application; its guides explain adoption, use, and design. Editorial procedures belong here so those guides remain focused on the contract. This file adds no operating obligations to the reusable contract.

## Document responsibilities

Keep the three guides and this editorial file at the repository root.

| File | Responsibility | What belongs elsewhere |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | The self-contained operating contract: definitions, workflow, requirements, conditions, and exceptions. | Project-specific facts and commands belong in the adopting project's code and documentation. |
| [CLAUDE.md](CLAUDE.md) and [.github/copilot-instructions.md](.github/copilot-instructions.md) | Discovering and applying the contract, with permitted non-policy titles and provenance. | Independent or duplicated collaboration policy. |
| [README.md](README.md) | A truthful, inviting basic guide: what the contract offers, installation, a useful first task, and the expectations needed to make an informed adoption decision. | Detailed usage scenarios, engineering rationale, and editorial instructions. |
| [README-powerusers.md](README-powerusers.md) | Fuller practical explanations and examples that develop what the basic guide introduces. Includes alignment, continuation, and tool compatibility. | A second operating contract, exhaustive engineering rationale, or documentation-maintenance advice. |
| [README-maintainers.md](README-maintainers.md) | Technical documentation of the contract: attributes, opinionated choices, reasons, source assignments, trade-offs, and constraints supporting repair, improvement, or redesign. | Instructions about maintaining the READMEs or packaging documentation. |
| `META-README.md` | Documentation ownership, permitted overlap, editorial procedures, and verification. | Product behavior or information users need to adopt and use the contract. |

The ordinary reading path starts at the basic README and branches by interest: fuller use or technical understanding. Both interests concern `AGENTS.md`. Keep editorial navigation out of that path; contributors can discover this root file directly.

The name “power users” describes interest in getting more from the contract, not a required technical background. Its guide should remain accessible to readers seeking practical depth. The technical guide is documentation of the artifact itself, rather than a contributor onboarding manual.

## Single source of truth

Give each fact, procedure, rule, or detailed explanation one authoritative owner. Reuse it through links and purposeful summaries. Reader-appropriate introductions are useful; independently maintained competing definitions are not.

| Information | Authoritative owner | Treatment elsewhere |
| --- | --- | --- |
| Agent obligations, permissions, triggers, exceptions, and exact contract definitions | `AGENTS.md` | Explain the practical effect or design reason and link to the relevant rule. |
| Basic installation procedure and a first task | `README.md` | Link back when detailed guidance needs setup context. |
| Detailed practical application, examples, alignment, and continuation | `README-powerusers.md` | Use brief orientation in the basic guide; technical explanations may point to practical examples. |
| Tool compatibility, adoption diagnostics, and recorded provider-documentation check dates | `README-powerusers.md` | Keep basic setup concise; link technical integration claims to the relevant guidance and evidence dates. |
| Design rationale, exact source assignments, engineering trade-offs, and portability criteria | `README-maintainers.md` | Mention methods briefly when explaining usage; link to the deeper account. |
| Documentation responsibilities and maintenance procedures | `META-README.md` | Apply them in the other files without reproducing them in user-facing guides. |

“Authoritative owner” concerns the repository's documentation. Provider documentation remains the source for provider behavior; method references clarify their assigned practices. `AGENTS.md` remains authoritative for the combined collaboration policy. A guide or external source must not silently strengthen, weaken, or extend that policy.

The contract's design constraints, such as its portability criteria, are documented in the technical guide. They describe the artifact and inform changes to it; they do not add hidden duties to ordinary agent tasks.

### Permitted overlap

A summary may introduce a concept that another guide explains fully. Keep the summary proportionate to its reader's immediate decision and link to the detailed owner. Preserve consequential conditions and exceptions when omitting them would mislead.

For example, the basic guide can explain that unexpectedly larger work causes a pause. The power-user guide explains the trigger and gives practical examples. The technical guide explains why scope authorization alone is insufficient to control unexpected effort. All three derive the actual obligation from the contract's scope and interaction rule.

Likewise, a brief PDSA explanation can make a usage example understandable while the technical guide owns the full design rationale. An example illustrates the rule; it cannot establish a new threshold or required artifact.

Avoid copying full procedures, source-assignment tables, or detailed lifecycle accounts between guides. Necessary examples and summaries should have a clear source and an identifiable update relationship. Different wording alone does not create a different responsibility.

## Make a documentation change

1. **Establish the intended change and its owner.** Distinguish an editorial clarification from a change to operating behavior. If behavior would change, identify it explicitly and follow the [contract-file authorization rule](AGENTS.md#53-instructions-contract-files-and-external-actions); do not enact it indirectly in a README.
2. **Update the authoritative content first.** Preserve the strength, trigger, scope, exception, and meaning of the rules being explained. For a clarification, use the relevant contract clauses and current rationale.
3. **Trace the affected dependencies.** Check summaries, examples, cross-references, and bridge explanations that derive from the changed content. Update only the relevant dependents; avoid creating a duplicate detailed owner.
4. **Check the reader's path.** Keep installation and a useful first task available in the basic guide. Keep practical depth in the power-user guide and construction details in the technical guide. Move editorial instructions here.
5. **Verify the resulting files.** Check coverage, consistency, Markdown, paths, and section anchors. When the contract itself changes, also assess it against the [technical review scenarios](README-maintainers.md#assessing-design-changes) and [portability criteria](README-maintainers.md#keeping-the-contract-portable).

For a substantial move or rewrite, keep a temporary content map showing where necessary information went. Use it to detect accidental loss or duplication, then retain only enduring ownership guidance here. A short entry point must not be achieved by quietly removing necessary explanations from the repository.

When headings or paths change, inspect incoming references throughout the repository. Where a known external reference warrants compatibility, consider a brief forwarding anchor or link rather than maintaining two full explanations.

## Preserve meaning and evidence

- Preserve the primary purpose in each guide's framing: preventing unconstrained token consumption, including unexpectedly heavy use within one increment, through intentionally small, complete steps. Explain progressive detail, bounded inquiry, material-growth reassessment, and visible results as supporting controls. PDSA organizes work and learning; engineering and documentation practices support quality and retained knowledge. Their prominence must not obscure why the contract combines them. The contract's introduction owns the purpose; the technical guide owns its rationale, and the practical guide develops its use.
- Keep adequate analysis, coherent completeness, and necessary validation explicit alongside effort control. Small scope must not imply shallow reasoning or omission of relevant dependencies. Inquiry may pause with missing evidence; neither the limit nor useful learning establishes completion. Explain token visibility and the absence of quotas or guarantees after introducing the positive purpose; a remaining caveat about tokens does not preserve that purpose by itself.
- Keep `MUST`, `SHOULD`, and `MAY` distinct when explaining the contract. A strong recommendation has justified exceptions; a mandatory checkpoint does not become optional through paraphrase.
- Preserve the distinction between task and increment completion, acceptance conditions and predictions, and investigation stopping limits and successful completion.
- Explain investigation limits as allowances the agent must establish and state before investigating blocking uncertainty, together with the question, scope, objective, and needed evidence. The contract supplies no universal value, unit, or formula. Keep the trigger, timing, and agent responsibility explicit; do not imply that a limit is only needed when the requester asks for one, or that every limit needs requester approval. Concrete bounds in examples illustrate the rule without creating defaults. The detailed practical explanation belongs in `README-powerusers.md`; summaries elsewhere should link to it.
- Keep the agent responsible for decomposition, establishing acceptance conditions, bounding blocking inquiries, validation, effort assessment, and recognizing when requester involvement is needed. Do not imply that a requester must repeat these standing instructions in each prompt.
- Present PDSA as starting with the request. Place context gathering, outlining the approach, and increment selection within Plan, and connect Study and Act to subsequent planning. Do not imply that the agent first fixes a complete sequence of increments outside PDSA or that the contract requires a separate hierarchy of outer and inner cycles.
- Distinguish an increment, a report, and an approval checkpoint. Do not imply that every increment requires fresh approval or that a completed increment grants permission.
- Keep documentation coverage expectations separate from permission to audit, backfill, or reorganize an entire project.
- Do not turn a mentioned method into a mandatory deliverable for every task. Preserve the conditions on tests, ADRs, guides, continuation records, and engineering techniques.
- Keep the known limits visible: token control is best effort, instruction compliance is not guaranteed, and tool permissions retain their authority. Do not claim measured benefits or compatibility that the evidence does not establish.
- Preserve primary-source links and exact attribution. Use the technical guide's [source assignments](README-maintainers.md#principles-and-reference-boundaries) rather than importing an entire framework or treating all source rhetoric as contractual policy.
- Keep the original evidence dates when moving existing provider guidance. If a claim is newly verified or changed, record the actual check date with the affected guidance. Editorial work alone does not refresh external evidence.

The READMEs describe the current contract and its use. Include background only when it explains a current choice. Keep revision narratives, obsolete editing alternatives, draft measurements, and package fingerprints out of them. Temporary working notes may retain editing history; move useful lasting rationale to its proper owner before retiring those notes.

## Write for the reader

Use plain Markdown, descriptive headings, direct links, and tables where they aid comparison. Introduce a term before using it and explain methods where they illuminate a practical action or design choice.

The basic guide should lead with the primary benefit sought: controlled token consumption through small, complete increments that preserve necessary depth and quality. Explain how visible results support requester direction, then provide an actionable starting point. Keep claims truthful and conditions proportionate. A newcomer should be able to understand the offering, install it, and begin a useful task using that guide alone.

Explain default behavior before optional controls. Lead with ordinary outcome-oriented requests and show the agent selecting increments, establishing checks, and applying the contract's consultation rules. Place requester-selected steps, requester-supplied investigation limits, and extra review checkpoints in a clearly optional context; distinguish those choices from the agent's mandatory framing of a blocking inquiry. Review the combined impression of headings and examples: accurate individual sentences do not compensate for a reading path that teaches the requester to manage the agent's workflow.

Introduce the complete PDSA workflow before developing its individual activities. Show increment selection as part of Plan and include a practical example in which findings influence the next Plan or the broader approach. Describe effort factors as assessments under the contract; do not invent numerical scores or imply that all future increments must be measured and settled before work starts.

The power-user guide should answer the questions that arise afterward. Use realistic examples and concise references to relevant standards and principles. Link deeper design rationale instead of requiring technical background to follow the practical guidance.

The technical guide should explain what the contract is and why it is constructed that way. Its analysis should be sufficient to inform changes to `AGENTS.md`; it should not require readers to switch roles into editing the surrounding documentation.

There is no numeric length limit for the READMEs. Judge length by purpose, necessary detail, repetition, and navigation. Keep conditions close to the explanations they qualify. Avoid empty categories, obligatory templates, promotional guarantees, and formalism that adds no understanding.

## Review the complete result

Before delivering a documentation change, verify:

- **Purpose and emphasis:** each guide identifies token-consumption control as the driving goal and connects the methods to it. The reading path explains small commitments, sufficient depth, complete results, and requester visibility before developing supporting practices or limitations. It introduces no new quota, automatic accounting duty, or mandatory pause after every increment.
- **Basic use:** purpose, files, placement, essential replacement precautions, adoption checks, and a useful first task are understandable from `README.md`.
- **Default responsibilities:** the examples work with an ordinary request for an outcome; the agent supplies the process. Optional requester controls are clearly distinguished from required consultation and the ability to continue under existing authorization.
- **Investigation limits:** the explanation identifies who states the limit and when, provides a concrete illustrative bound, and distinguishes obtaining the evidence from exhausting the allowance. Incomplete work is reported when acceptance conditions remain unmet; no arbitrary default, automatic completion claim, or blanket approval checkpoint is introduced.
- **Workflow continuity:** the reading order places planning inside PDSA from the request onward. Examples connect the overall objective, selection of the next increment, observed results, and subsequent planning without introducing an unsupported process hierarchy.
- **Practical depth:** necessary detailed usage guidance remains available and discoverable; method references support the explanations.
- **Technical depth:** attributes, rationale, sources, constraints, and trade-offs remain sufficient to assess changes to the contract.
- **Editorial separation:** the three reader-facing guides stay focused on `AGENTS.md`; instructions for keeping the READMEs synchronized remain here.
- **Ownership:** detailed knowledge has one owner; permitted summaries agree with it and direct readers to it.
- **Links and packaging:** relative paths match the intended repository layout, section anchors resolve, moved topics have updated incoming links, and delivered files contain the intended versions.

Measure `AGENTS.md` itself if it changes, using the technical guide's criteria. Counts can support review; automated enforcement is not required. Do not preserve transient size snapshots or remaining-space claims in the READMEs. Documentation consistency and textual review do not establish equivalent agent behavior or token savings.
