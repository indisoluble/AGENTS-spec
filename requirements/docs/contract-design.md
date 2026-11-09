# Product requirements and design of AGENTS.md

**Engineering-only document.** This file is a temporary consolidation document within the requirements project at `requirements/docs/contract-design.md` and remains excluded from the intended consumer release. It is not a runtime instruction file, provider bridge, or adoption guide, and creates no additional consumer operating duties.

This document is the authoritative design source for the reusable, opinionated [AGENTS.md](../../contract/prerelease_AGENTS.md) contract's remaining currently binding design prescriptions and their semantics, selected mechanisms, rationale, trade-offs, significant design history, and subsequent engineering evolution. [Contract architecture](architecture.md) owns the transferred design overview, goals and boundaries, three-layer interaction and continuation, bounded-work design, PDSA learning design, completion and prediction distinctions, bounded-inquiry design, authorization and requester decisions, reporting and continued execution, Simple Design, DRY, component boundaries, refactoring, validation, focused techniques, arc42 documentation design, EARS requirements-writing design, ADR-writing design, technical-debt recording, Diátaxis documentation design, worked task example, and shared current-semantics vocabulary and contract-clause coverage index. [Product requirements](product-requirements.md) owns the established objectives, PR1, and product constraints; [requirement candidates](requirement-candidates.md) owns provisional RC1–RC10 and their unresolved acceptance questions. [Classification and evidence](#classification-and-evidence) remains here alongside the remaining design explanations and historical alternatives. Internal requirements and explanations add no runtime duties: `AGENTS.md` remains the independently self-contained normative runtime contract delivered to consuming agents.

For adoption, use [README.md](../../contract/prerelease_README.md); for practical guidance, use [Getting more from AGENTS.md](../../contract/prerelease_README-powerusers.md). For engineering-system relationships and authority, use [architecture.md](../../docs/architecture.md#development-time-and-runtime-authority); for editorial procedures and canonical ownership, use [documentation-maintenance.md](../../_internal/docs/documentation-maintenance.md#document-ownership). This reference explains product intent and design, rather than supplying a complete product-development process, branching strategy, workflow engine, or framework tutorial.

Read by question:

| Question | Start here |
| --- | --- |
| What is intended and established? | [Established product requirements](product-requirements.md), including their qualifications and provenance |
| What remains provisional, and how is evidence classified? | [Requirement candidates](requirement-candidates.md) and [classification and evidence](#classification-and-evidence) |
| What does the current contract prescribe? | [Current-semantics vocabulary and coverage](architecture.md#current-semantics-vocabulary-and-coverage), then the indexed topic sections here and in the [contract architecture](architecture.md); essential operating detail is specified in these engineering sources, without requiring a guide or contract link to fill gaps. |
| Why these mechanisms, and how do they interact? | [Contract architecture](architecture.md), including the [worked task](architecture.md#how-the-design-works-in-a-task), then the remaining [design choices](#design-choices) |
| Which decisions and older alternatives affect interpretation? | [Decision status and historical alternatives](#decision-status-and-historical-alternatives) |
| How should the contract evolve? | [Evolving the contract](#evolving-the-contract) |
| What distinctions and sources matter in review? | [Design reference](#design-reference) |

## Product objectives, requirements, and constraints

### Classification and evidence

This document governs engineering design evolution within the established requirements and constraints now owned by [product-requirements.md](product-requirements.md), applicable accepted decisions, and requester authority under the [engineering authority model](../../docs/architecture.md#development-time-and-runtime-authority). This section continues to own classification and evidence for the material retained here and the shared status distinctions; the requirements documents preserve [established-item provenance](product-requirements.md#status-and-provenance) and [candidate status and provenance](requirement-candidates.md#status-and-provenance). Runtime obligations remain those delivered through the complete, self-contained `AGENTS.md`, within the consuming tool's instruction hierarchy and permissions. Protected-file rules and authority limits continue to apply. The [authority-transition history](../../docs/architecture.md#temporary-migration-authority) retains the transfer provenance.

Currently mandatory methods and other prescribed mechanisms retain their present normative force, including PDSA, explicit increment predictions, decomposition rules, and EARS. Future revisability makes none of these optional now and changes neither recommendations nor permissions. Prospective RC proposals and D1–D10 alternatives must not redefine the current specification; future requirements acceptance and authorized redesign are separate work. RC1–RC10 and the earlier 30 RCx-Py proposals remain non-authoritative unless separately accepted. Earlier in-principle acceptance of nine proposals and selection of D2-A/D3-A for planning do not replace or reinterpret current behavior or authorize design changes here.

The classification concerns engineering intent, not whether a currently loaded instruction applies to an agent. Existing clauses prove what the runtime contract presently specifies; they do not independently prove that every behavior or selected method is an accepted product requirement. An authorized redesign can reconsider mechanisms, including PDSA and the three-layer organization. The engineering architecture is provider-neutral; the candidate contract is staged and does not automatically govern development. It remains normative for consuming agents and explicitly isolated evaluations; historical loading during repository maintenance is not a permanent self-governance requirement. [Development-time and runtime authority](../../docs/architecture.md#development-time-and-runtime-authority) owns that distinction.

| Status | Evidence and interpretation in this document |
| --- | --- |
| **Established objective or product requirement** | Supported by explicit requester direction or accepted project records beyond the implemented clause alone. Objectives state desired outcomes; [PR1](product-requirements.md#established-product-requirement) states a verifiable product constraint. |
| **Established constraint** | A retained, documented compatibility, portability, or design boundary. Its original strength, exceptions, measurement, and revision conditions remain attached; a preferred target is not a hard ceiling. |
| **Design rationale or selected decision** | Reasons for a mechanism, its interactions, costs, and alternatives. Selection in the current design does not make the mechanism a permanent product requirement. Explicit acceptance and supersession are distinguished in the [decision index](#decision-status-and-historical-alternatives). |
| **Current binding design prescription** | An operative mechanism recorded here and delivered through `AGENTS.md`, with its present modality, actor, trigger, timing, scope, conditions, and exceptions. The detailed [design choices](#design-choices) specify these semantics alongside distinguishable rationale; the [assessment scenarios](#assessing-design-changes) illustrate interactions. Binding now does not imply independently accepted enduring product status. |
| **Requirement candidate — provisional** | Intended behavior inferred from rationale, examples, or clauses without independently established acceptance. The [candidate inventory](requirement-candidates.md#requirement-candidates) identifies topics and acceptance decisions still needed. |
| **Historical or superseded reasoning** | Significant earlier mechanisms and reasons, with source context and current replacement links. These explain evolution; they are not current policy or accepted requirements. |

The [requirements owner's provenance section](product-requirements.md#status-and-provenance) preserves why the ordered objectives, PR1, and constraints are established, including the earlier reader guidance, adoption guide, accepted requirements-led engineering decision, and requester preservation direction. Accepted product intent does not accept every implemented clause. Detailed behavioral acceptance cannot be reconstructed merely from an “accepted contract” commit title or normative wording, so it remains provisional where no separate evidence is available.

### Established objectives

The canonical [established objectives](product-requirements.md#established-objectives) are O1 (control token consumption, first), O2 (requester awareness and consequential control, second), and supporting knowledge continuity. Their complete definitions, qualifications, and evidence limits now belong to `requirements/docs/product-requirements.md`; the design sections below explain the current mechanisms.

### Established product requirement

The canonical [PR1 — Self-contained operating contract](product-requirements.md#established-product-requirement), its complete EARS statement, and its distinctions between completeness, provider loading, adopting-project information, and behavioral evidence now belong to `requirements/docs/product-requirements.md`.

### Established constraints

The canonical [established constraints](product-requirements.md#established-constraints) now belong to `requirements/docs/product-requirements.md`: authority and capability boundaries, method selection, and portability and standing context, with their original strengths, qualifications, exceptions, and revision conditions. [Design boundaries](architecture.md#design-goals-and-boundaries), [method selection](#choosing-or-replacing-methods), [portability](#keeping-the-contract-portable), and [wording trade-offs](#current-wording-trade-offs) retain the full engineering explanations and current design consequences; they are not independent definitions of the transferred constraints.

### Requirement candidates

The canonical [provisional RC1–RC10 inventory and unresolved acceptance questions](requirement-candidates.md#requirement-candidates) now belong to `requirements/docs/requirement-candidates.md`, with their [status and provenance](requirement-candidates.md#status-and-provenance). All entries remain provisional; their complete linked design explanations and current semantics remain in the [contract architecture](architecture.md) and this document, with historical alternatives retained here.

## Design choices

**Status: current binding design, with rationale and historical context distinguished.** The sections here and in the [contract architecture](architecture.md) specify the present operating behavior and preserve its reasons, interactions, and qualifications. Statements about what an agent MUST, SHOULD, or MAY do explain `AGENTS.md` at its current strength; they are not an additional operating contract or acceptance of the provisional RC topics. The named methods and exact three-layer arrangement can be reconsidered only through future authorized change under the established objectives and constraints; they remain binding at their current strengths now.

### Current-semantics vocabulary and coverage

See the requirements-domain [contract architecture — Current-semantics vocabulary and coverage](architecture.md#current-semantics-vocabulary-and-coverage) for the canonical vocabulary and current contract-clause coverage index.

### Design overview

See the requirements-domain [contract architecture — Design overview](architecture.md#design-overview).

#### Design goals and boundaries

The canonical [design goals and boundaries](architecture.md#design-goals-and-boundaries) now belong to `requirements/docs/architecture.md`.

### Workflow design choices

See the requirements-domain [contract architecture — Workflow design choices](architecture.md#workflow-design-choices) for layer interaction and continuation within [Solution Strategy](architecture.md#solution-strategy), and [Crosscutting Concepts](architecture.md#crosscutting-concepts) for the reusable rules and mechanisms, including bounded-work design. The remaining detailed workflow mechanisms below stay here.

#### Three interacting layers

The canonical [three interacting layers](architecture.md#three-interacting-layers), their composition, four continuation outcomes, authorization qualifications, and evidence limits now belong to `requirements/docs/architecture.md`.

#### Small commitments with sufficient depth

See the requirements-domain [contract architecture — Small commitments with sufficient depth](architecture.md#small-commitments-with-sufficient-depth) for the canonical bounded-work design.

#### Learning throughout the work

See the requirements-domain [contract architecture — Learning throughout the work](architecture.md#learning-throughout-the-work) for the canonical PDSA learning design.

#### Completion, predictions, and bounded investigation

See the requirements-domain [contract architecture — Completion, predictions, and bounded investigation](architecture.md#completion-predictions-and-bounded-investigation) for the canonical design.

#### Authorization and requester decisions

See the requirements-domain [contract architecture — Authorization and requester decisions](architecture.md#authorization-and-requester-decisions) for the canonical design.

#### Reporting and continued execution

See the requirements-domain [contract architecture — Reporting and continued execution](architecture.md#reporting-and-continued-execution) for the canonical design.

### How the design works in a task

See the requirements-domain [contract architecture — How the design works in a task](architecture.md#how-the-design-works-in-a-task) for the canonical worked example.

### Engineering choices

**Current scope boundary (§1.2).** The agent MUST NOT add unrelated cleanup, renaming, reformatting, dependency changes, file moves, or speculative refactoring. It MUST NOT delete code as dead unless the code is clearly unreachable or directly made obsolete by the authorized change. Necessary larger refactors SHOULD stay distinct from behavior changes. These boundaries apply to the practices below; method selection does not authorize unrelated work.

#### Simple Design: choosing what the current solution needs

See the requirements-domain [contract architecture — Simple Design: choosing what the current solution needs](architecture.md#simple-design-choosing-what-the-current-solution-needs) for the canonical current-design explanation.

#### DRY: keeping knowledge consistent as work progresses

See the requirements-domain [contract architecture — DRY: keeping knowledge consistent as work progresses](architecture.md#dry-keeping-knowledge-consistent-as-work-progresses) for the canonical current-design explanation.

#### Component boundaries, refactoring, and validation

See the requirements-domain [contract architecture — Component boundaries, refactoring, and validation](architecture.md#component-boundaries-refactoring-and-validation) for the canonical current-design explanation.

#### Validation and test evidence

See the requirements-domain [contract architecture — Validation and test evidence](architecture.md#validation-and-test-evidence) for the canonical current-design explanation.

#### Focused techniques and how they work together

See the requirements-domain [contract architecture — Focused techniques and how they work together](architecture.md#focused-techniques-and-how-they-work-together) for the canonical current-design explanation.

### Documentation choices

See the requirements-domain [contract architecture — Documentation choices](architecture.md#documentation-choices) for the canonical documentation ownership and synchronization design.

#### arc42: shared architectural context as the project grows

See the requirements-domain [contract architecture — arc42: shared architectural context as the project grows](architecture.md#arc42-shared-architectural-context-as-the-project-grows) for the canonical current-design explanation.

#### EARS: making required behavior explicit

See the requirements-domain [contract architecture — EARS: making required behavior explicit](architecture.md#ears-making-required-behavior-explicit) for the canonical current-design explanation.

#### ADRs: preserving the reasons for lasting choices

See the requirements-domain [contract architecture — ADRs: preserving the reasons for lasting choices](architecture.md#adrs-preserving-the-reasons-for-lasting-choices) for the canonical current-design explanation.

#### Recording technical debt

See the requirements-domain [contract architecture — Recording technical debt](architecture.md#recording-technical-debt) for the canonical current-design explanation.

#### Diátaxis: choosing content for the reader's need

See the requirements-domain [contract architecture — Diátaxis: choosing content for the reader's need](architecture.md#diátaxis-choosing-content-for-the-readers-need) for the canonical current-design explanation.

### Why the bridges differ

The provider explanations here retain their existing source provenance; the [recorded evidence dates](../../contract/prerelease_README-powerusers.md#evidence-dates) still apply, and this restructuring does not refresh them. Actual support needs checking in the adopting environment.

Both bridges apply the same local contract through their tool's instruction mechanisms. [CLAUDE.md](../../contract/prerelease_CLAUDE.md) uses `@AGENTS.md`, Claude Code's [native import syntax](https://code.claude.com/docs/en/memory#import-additional-files), to include the referenced content. The single line can therefore perform its loading role.

[Copilot support](https://docs.github.com/en/copilot/reference/custom-instructions-support) varies by interface. A Markdown link identifies a file but is not a universal import mechanism. The supplied bridge explicitly directs reading and following the local contract within the actual hierarchy and permissions. Neither supplied bridge defines independent behavior for a failure to load the contract. The contract cannot govern an agent that never received it, so the package supplies no common stop/report/resume protocol for that case. Actual tool and requester instructions govern the situation. The [practical compatibility guidance](../../contract/prerelease_README-powerusers.md#tool-compatibility) explains this limitation and adoption diagnostics; it adds no fallback operating policy.

The [current instruction rule](../../contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions) assigns **two different scopes**:

| Scope | Current prescription |
| --- | --- |
| Canonical contract | Root `AGENTS.md` MUST own the canonical repository-wide contract. |
| Two bridges only | Root `CLAUDE.md` and root-relative `.github/copilot-instructions.md` MUST only discover and apply that contract, optionally with non-policy titles or provenance. `AGENTS.md` is not a bridge. |
| Three protected files | `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` MUST be edited only on explicit request for the file or instructions; applying file-specific recommendations counts. Necessary edits to the other two MAY accompany that request. Other affected documents follow the ordinary canonical-knowledge and synchronization rules. These instruction-file edits MUST stay separate from unrelated work. |

Directory instructions MAY add subtree rules only if contract-compatible. The actual tool sets discovery, scope, and precedence; that precedence never makes conflicting policy acceptable, and the agent MUST report conflicts. Compatibility is a content rule, not an invented precedence mechanism. Adoption guidance therefore calls for human validation of which existing practices, conventions, and workflows persist, following the [basic installation precautions](../../contract/prerelease_README.md#get-started); that guidance is not an extra runtime rule. Project facts and operating rules have different owners.

If uncertainty about loading, scope, or precedence could affect the task, the agent SHOULD check available diagnostics and relevant instruction files; it MUST report what was checked and remaining material uncertainty. Tool limits blocking instruction loading also require the [tool-limit disclosure](architecture.md#reporting-and-continued-execution). Diagnostic inspection and demonstrated application are different evidence, and these rules add no bootstrap protocol for a contract that was never loaded.

External actions—commits, publishing or sending, or changes to remote or shared state—MUST be authorized. Read-only access follows task scope and tool permissions. Neither documentation duties nor an instruction-file edit request independently authorizes an external action.

Discovery, inclusion, precedence, and application are distinct. [VS Code's conflict guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#_resolve-conflicting-instructions), its [instruction settings](https://code.visualstudio.com/docs/agents/reference/ai-settings#_custom-instructions-settings), and [GitHub.com's precedence guidance](https://docs.github.com/en/copilot/concepts/prompting/response-customization#precedence-of-custom-instructions) describe different aspects. File order or a link alone cannot establish all four. The [adoption checks](../../contract/prerelease_README-powerusers.md#check-adoption) and [recorded evidence dates](../../contract/prerelease_README-powerusers.md#evidence-dates) qualify the integration guidance; exact settings and support depend on the provider's documentation and the actual environment.

The Copilot title and header identify the associated release and upstream origin. Its release date and source URL match `AGENTS.md`. Metadata adds no policy authority, and the adopted local contract remains canonical. Permitting provenance does not require a header on the one-line Claude import. Minimality preserves each bridge's loading and application role.

## Decision status and historical alternatives

### Selected design and retained decisions

This index identifies status and points to the reasons and consequences already owned here. It does not turn each explanation into an ADR or independently accept a product requirement. Engineering-system and evaluation-specific decisions stay with the [architecture decision index](../../docs/architecture.md#decisions) and [evaluation documentation](../../evaluations/docs/evaluations.md); they are not copied here.

| Choice | Status and rationale location |
| --- | --- |
| Separate work cycle, progression guards, and triggered rules | **Selected current design.** [Three interacting layers](architecture.md#three-interacting-layers) explains cross-phase concerns, composition, and the rejected implication that placement confines a duty to a phase. No measured benefit or permanent three-layer requirement is claimed. |
| Bounded commitments with PDSA and focused practices | **Selected current design; recorded as sufficient for the agreed design.** [Learning](architecture.md#learning-throughout-the-work), [engineering choices](#engineering-choices), and [method selection](#choosing-or-replacing-methods) explain complementary roles. Additional umbrella frameworks were not needed; future replacement is possible under the selection criteria. |
| Role-specific knowledge ownership | **Selected current design; earlier total ordering rejected/superseded.** [Documentation choices](architecture.md#documentation-choices) retains why no global artifact precedence fits different knowledge owners, and how unresolved consequential conflicts are handled. |
| Provider-specific instruction bridges | **Selected current integration design.** [Why the bridges differ](#why-the-bridges-differ) retains native import versus explicit read/follow, provenance, no common bootstrap policy, and actual-provider limits. A link is not treated as a universal import. |
| Qualified size target and compact wording | **Retained established constraint; identified wording compromises recorded as accepted in the existing design account.** [Portability](#keeping-the-contract-portable) and [wording trade-offs](#current-wording-trade-offs) retain the exception, review conditions, and limited acceptance. This does not extend acceptance to further precision loss. |
| Effort baselines, mandatory inquiry framing, and routine-report suppression | **Historical/superseded.** The alternatives below preserve their control and visibility rationale; current §§2.3–2.4 and 3.7 describe different mechanisms. |

### Historical source and interpretation

The historical source is [`README-maintainers.md` on PDSA at `9a078b3`](https://github.com/indisoluble/AGENTS-spec/blob/9a078b3833297ca33357391bb60e6d469bceeff4/README-maintainers.md). The current guide descends from it through accepted-contract alignment and later moves; relevant records include [`c4bc519`](https://github.com/indisoluble/AGENTS-spec/commit/c4bc51938ef7a4890f1f353e46e764f226c3b42f) and [`96947a8`](https://github.com/indisoluble/AGENTS-spec/commit/96947a8a8644e744525c0209dcc2a5b290f3589f). These identify repository evidence, not new external-source verification. Historical explanations below preserve significant mechanisms and reasons without restoring their operative force. The current explanations linked beside them own present interpretation.

### Superseded effort-baseline checkpoint

**Historical mechanism.** The PDSA version established both an increment baseline when planning that increment and a cumulative-task baseline at task start, using requester direction where supplied and otherwise agent judgment without routine notification. Baselines could be qualitative; they were working state rather than token quotas, worksheets, or required project records. New evidence changed current estimates, but growth was assessed against the established baselines rather than the latest estimate. A material increase required reassessment, an explanation of what changed, unfinished work and uncertainty, and the smallest useful complete next step, followed by requester direction before taking on the added work, even within an unchanged broad objective and authorization.

Only requester direction could revise a baseline. Approval of disclosed growth revised the affected baselines to include only that commitment, avoiding repeated consultation for already approved effort while leaving later growth detectable. A new increment baseline could not absorb growth already discovered without direction, and new increments, attempts, and handoffs could not reset the task baseline. Handoffs transferred the task baseline, any unfinished increment's baseline, and still-relevant approved revisions. A continuing agent missing them recovered the state or obtained direction before further effort-bearing work rather than setting fresh baselines.

**Reason and trade-off.** A scope boundary alone did not prevent unexpectedly heavy work within one increment or cumulative growth through many small additions. Keeping original comparison points made those changes visible across attempts and contexts. The mechanism required judgment about qualitative baselines and material growth; it supplied no automatically enforced quota. The historical CSV walkthrough's unexpectedly larger shared-parser redesign therefore triggered a growth checkpoint in whichever phase it was found.

**Current replacement.** [Authorization and requester decisions](architecture.md#authorization-and-requester-decisions) explains requester-imposed limits, evidence-based cumulative reassessment, and consequential-direction consultation. Current §2.3 does not require agent-created increment/task baselines or consultation solely because an agent estimate grows. The current parser example distinguishes a routine correction from a new consequential direction or material departure. The old baseline state and automatic material-growth checkpoint are not current handoff or continuation requirements.

### Superseded inquiry announcement and stopping rule

**Historical mechanism.** Beyond exempt context gathering, inquiry required advance framing before starting or continuing: question, scope, objective, effort limit, and needed evidence. The agent could choose a useful bound without requester approval of every limit; there was no default amount, unit, or formula. Obtaining the evidence or reaching the declared limit ended that inquiry even if the answer remained unknown. A report then identified unmet acceptance conditions, missing evidence, uncertainty, and any need for broader research or design direction. The report itself was not an approval checkpoint.

Existing scope and authority could permit a newly framed bounded attempt, but requester caps, checkpoints, unresolved consequential intent, missing evidence blocking safe continuation, and the historical material-growth rules still controlled it. Neither an exhausted allowance nor a negative finding granted authority. The declaration made commitment visible before consumption, but judgment about the bound supplied neither a tool-enforced timeout nor a token quota. Context gathering, including reading existing project documentation for a blocking question, remained exempt from that inquiry framing while still subject to scope and effort controls.

**Current replacement.** [Completion, predictions, and bounded investigation](architecture.md#completion-predictions-and-bounded-investigation) preserves the purpose-based boundary while explaining timely uncertainty/significance notification, including the already-communicated exception, and actual bounded conduct without a five-element announcement or declared allowance. Sufficient evidence ends inquiry; insufficient evidence at an increment's bounds requires reassessment before justified further investigation. There is no automatic inquiry-end report or new announcement per attempt. Optional requester limits remain binding. Removing the older framing mechanism establishes no behavioral equivalence or token-efficiency result.

### Superseded report suppression and consultation strength

**Historical report choice.** Routine report drafting as well as output was prohibited unless requested or required. Suppressing drafting aimed to avoid consuming effort preparing narration merely to withhold it. Reporting consolidated work at completion, handoff, or input requests, with advance disclosures affecting authorization or the next decision and an explicit inquiry-end report. Other disclosures had to join the next consolidated report unless earlier timing was explicit; this was mandatory, unlike the current recommendation that other information should normally join that report. Record maintenance retained its own timing. The trade-off described in that version was less routine visibility while authorized work continued; fewer reports were not measured token savings and reserved no review opportunity.

**Current replacement.** [Reporting and continued execution](architecture.md#reporting-and-continued-execution) explains the recommendation to minimize routine reports and keep intermediate communication concise and useful, with specific mandatory timings for consolidation, initial framing, inquiry notification, and advance disclosures affecting authorization or a decision requiring input. Useful intermediate updates are possible; the older categorical drafting/output ban and inquiry-end timing are superseded.

**Historical consultation strength.** The PDSA account treated asking before unsettled consequential choices as a SHOULD, while material unresolved intent or permission and the baseline-growth checkpoint had their own mandatory force. The current [requester-interaction account](architecture.md#authorization-and-requester-decisions) distinguishes the MUST for a new consequential architectural or lasting design direction or material departure unless specifically authorized, from the SHOULD for other unsettled material choices. Historical strength must not be substituted for the current clause. In both designs, a report or ADR could not retroactively authorize a choice.

### Superseded method-reference inquiry exemption

The historical reference account exempted narrow consultation to clarify a material method ambiguity from §2.4 inquiry framing, while requiring disclosure of the ambiguity, source, and interpretation and forbidding imported obligations. This kept a clarification link from becoming a full research assignment.

The current [reference boundaries](#principles-and-reference-boundaries) retain limited consultation and no imported rules, but qualifying consultation now follows the purpose-based context/inquiry distinction and notification/conduct requirements, including the already-communicated exception. Clear rules must not be researched, and broader research needs explanation and requester direction. The former blanket inquiry exemption is historical only.

## Evolving the contract

These sections constrain repairs, improvements, or redesign of `AGENTS.md`: how methods are chosen or replaced, how the contract stays portable, and which current wording trade-offs need review when editing. They guide the contract's evolution and add no operating duties to ordinary project tasks.

### Choosing or replacing methods

The established [method-selection constraint and qualifications](product-requirements.md#method-selection-qualifications) are owned by the requirements document. The retained discussion below explains their design application and the reasons for the current method set; it does not independently redefine the constraint.

The method set was selected for recognized practices, freely accessible material sufficient to interpret their assigned roles, and distinct responsibilities. PDSA and Simple Design were judged sufficient for the agreed design alongside the focused engineering references, documentation conventions, and explicit collaboration rules. Additional umbrella frameworks were not needed to supply those responsibilities.

These selection criteria remain constraints on future additions or replacements unless explicitly revised. A proposed method change should explain the need it addresses, the accessibility of its required interpretive material, and any overlap or expansion of obligations. Changing a selection criterion is itself a design decision to identify explicitly; these constraints on the contract's evolution add no operating duties to ordinary project tasks.

### Keeping the contract portable

The established [portability and standing-context constraint and qualifications](product-requirements.md#portability-and-standing-context-qualifications) are owned by the requirements document. The retained discussion below explains the measurement, provider evidence, engineering rationale, and current design application under that constraint; it does not independently redefine it.

The provider evidence supporting the choice below retains its recorded **2026-10-04** check date in the [evidence-date owner](../../contract/prerelease_README-powerusers.md#evidence-dates). It has not been newly verified by this restructuring; applicable limits still depend on the actual provider and environment.

The entire `AGENTS.md` has a **strongly preferred target of about 24,000 UTF-8 bytes after normalizing line endings to LF**. Replace each CRLF pair and any remaining CR with LF before counting the whole file's UTF-8 bytes; do not otherwise trim or reformat its contents. LF and CRLF copies of the same content therefore have the same count. Normalized UTF-8 bytes remain the project's canonical measurement.

This target is informed by [Codex's default 32 KiB combined instruction limit](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance) and Anthropic's [guidance to keep `CLAUDE.md` concise and human-readable](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md). The approximate 24,000-byte figure is a project choice: it leaves room below Codex's default for directory instructions and other loaded instruction or configuration context, and reflects Claude Code's guidance on limiting standing context. Importing the contract through `CLAUDE.md` still [loads its contents into context](https://code.claude.com/docs/en/memory#import-additional-files).

Exceeding the target is exceptional but acceptable when further reduction would materially compromise normative fidelity or human comprehensibility. Before such excess is accepted, the contract receives a deliberate compression review. That review removes genuine redundancy and low-value explanatory detail before it compresses core control semantics, such as authorization, requester limits, cumulative reassessment, consultation, inquiry, and continuation. Even over target, the contract keeps meaningful headroom below applicable provider and project combined instruction-loading limits, such as Codex's default above, so directory instructions and other context can coexist. The project defines no separate provider-independent ceiling; those applicable combined limits bound the acceptable excess.

Check the normalized byte count after edits. Automated counts can help; automated enforcement is not required. Normalization defines this project's measurement; provider compatibility still depends on the actual delivered files, other loaded instructions, and tool configuration. Preserve useful spacing and headings. Meeting the target does not establish clarity, compatibility, equivalent behavior, agent adherence, or token savings. Vendor changes can prompt a review but do not automatically change the project policy.

The size target concerns the standing contract itself, not the reasoning or work allowed for a task. Operational meaning remains self-contained in `AGENTS.md`; necessary operating semantics must not move into a README to satisfy the target, because that would undermine portability even if the resulting file were smaller. Compactness is therefore subordinate to normative fidelity and usable comprehension, while standing instruction context remains a constrained resource.

### Current wording trade-offs

Compact instructions reduce standing text while increasing the risk that readers must infer relationships. Ambiguity can cause clarification, reference consultation, or rework; a smaller contract does not establish lower total token use. Review these current treatments when editing:

| Treatment | Interpretation risk and review focus |
| --- | --- |
| Implicit agent subjects, short labels, and slash groups | Keep the actor, every duty, and the relationship between grouped actions clear. |
| Broad knowledge-ownership and permitted-copy categories | Ensure readers can recognize facts, schemas, requirements, rationale, invariants, procedures, conventions, tests, and examples under the appropriate rule. |
| Concise definitions, architecture topics, record fields, and reports | Preserve distinguishing meaning and conditions; matching a name or keyword alone is insufficient. |
| Layered organization with section cross-references | Each passage should make sense where it appears. A reference can point forward to details when the surrounding text explains the relevant concept or constraint; `permitted work (§2.1)` is one example. Where a bare reference would force readers to look ahead just to understand the current passage, supply enough local explanation, accepting useful brief repetition. Keep consequential conditions explicit; guards and triggered rules apply across phases, and placement must not restrict a rule to one phase or imply an extra phase. |
| Initial task outline and first increment | Preserve advance visibility of the overall direction and next objective and bounds after proportionate preliminary context gathering. Keep later work at outline level and distinguish the statement from an approval request. |
| Requester limits and consequential direction | Distinguish informal expectations from binding requester constraints. Material ambiguity needs clarification; new consequential design direction and material departures need prior consultation unless the specific choice is already authorized. Routine local corrections remain autonomous. |
| Purpose-based inquiry, awareness, and bounded conduct | Unknown data and prescribed procedures do not decide classification alone. Preserve context gathering, execution, validation, and inquiry as distinct activities. Promptly explaining material uncertainty and its significance differs from consulting on a consequential choice. No duplicate notification is needed when the request or task framing already communicates it. A declared allowance is not required, and announcing one cannot replace actual bounded work, evidence sufficiency, or reassessment before justified continuation. |
| Proportionate intermediate communication | Minimizing routine reports and keeping updates concise and useful are recommendations, not a categorical ban or a requirement for effort-audit messages. Consolidated reporting, initial framing, prompt inquiry notification, and disclosures before affected work retain their own triggers and strengths. |
| Reference links without per-rule numeric locators | The [exact assignments](#principles-and-reference-boundaries) preserve attribution; narrow consultation limits prevent the links from becoming open-ended research. |

These are interpretation risks, not additional operating rules or measured agent outcomes. Do not approach the size target by removing essential conditions or transferring them into a README.

Acceptance of the current wording compromises covers only the identified trade-offs. It does not authorize further loss of precision. Any new trade-off, including reduced explicitness without an intended rule change, is a design decision to identify for requester review. Its rationale needs to record what becomes less explicit, where the operative meaning remains, and the likely interpretation or effort consequences. Previous acceptance and matching counts do not establish that a further reduction is lossless or behaviorally equivalent.

## Design reference

Use this material when reviewing a proposed change or an explanation of the contract: the design scenarios check combinations of rules against their intended distinctions, and the reference assignments preserve attribution and consultation limits.

### Assessing design changes

**Status: design-assessment scenarios against the current implementation, not independently accepted product requirements or evaluation results.** The rows preserve interpretation distinctions for textual review. The [candidate inventory](requirement-candidates.md#requirement-candidates) identifies where independent product acceptance remains unresolved. [Architecture](../../docs/architecture.md#what-evaluation-evidence-can-establish) owns the relationship to behavioral evidence; [evaluations.md](../../evaluations/docs/evaluations.md#purpose-and-evaluation-model) owns evaluation strategy and limits. These scenarios establish neither comprehensive coverage nor a new evaluation procedure.

The design can be assessed at two levels: whether the contract works as a self-contained set of instructions, and whether a proposed change preserves or deliberately alters the meaning of its clauses. A standalone reading tests the first; comparison of strength, trigger, scope, exception, and meaning tests the second. The detailed patterns, fields, and obligations are specified in the [current-semantic topic sections](#current-semantics-vocabulary-and-coverage); `AGENTS.md` remains the normative runtime authority.

| Scenario | Design distinction to assess |
| --- | --- |
| Broad objective, including a new project | The agent limits its next commitment and keeps later work at outline level until detail is needed for the next decision. Necessary depth, affected dependencies, and validation remain within scope; the breadth of the goal does not justify an unconstrained first increment. |
| Starting a task | After proportionate preliminary context gathering, assess whether the agent briefly communicates the task outline and first increment's objective and bounds before substantial work. The statement creates no approval checkpoint. It can also communicate material inquiry uncertainty and its significance, satisfying that notification without a second message. |
| Requester expectation or binding limit | “I expect a small fix” is not automatically a budget; “consult before a second increment” is a checkpoint. Material ambiguity about the intended force needs clarification. Only requester direction can revise requester-imposed limits or checkpoints; subdivision and retries do not reset them. |
| Ordinary authorized change | The agent selects a small increment and completes its checks before completing the increment, even without a chat report. Completion grants no additional permission or automatic documentation artifact; another increment can proceed under existing authorization unless a checkpoint requires a pause. |
| Completed exploration without a record trigger | Without durable material findings or significant lasting choices, no record is required merely to log the discussion. Transient task facts, such as a temporary CI outage or a failed experiment relevant only to the current attempt, follow the reporting rules only. |
| Material findings or significant proposals during review | A [finding](../../contract/prerelease_AGENTS.md#32-durable-findings-and-permanent-records) needs a permanent record only when it is both material and durable, even if it comes from a discarded approach; a missing owner leads to the minimum record rather than backfill, and a prohibited write is reported as unfinished work. A concrete significant proposal ready for decision or review requires an [ADR](../../contract/prerelease_AGENTS.md#33-significant-decisions-adrs) retaining the evidence that materially shaped it rather than routine PDSA history; brainstorming or a finding alone does not. Status reflects existing decision authority. Recording supplies no implementation authority or new approval checkpoint. |
| Verified factual documentation error during assessment | The agent may make an existing description of current project facts within the assessed scope match the canonical owner of that kind of knowledge, subject to scope, requester restrictions, §3.8, and tool permissions. Requirements, decision records, and protected instruction files are excluded. A verified mismatch with authoritative package configuration can justify correcting a README command; it does not authorize changing implementation, intended requirements, accepted decisions, or protected instruction files. |
| Task-relevant debt found during assessment | Evidenced debt may be recorded after considering accepted requirements and trade-offs. Any entry triggers classification-uncertainty and chat-disclosure duties. The general material-findings requirement still applies; neither classification nor recording authorizes a fix. |
| Requester or tool prohibits writes | Assessment permissions remain subject to requester restrictions (§2.1) and §3.8. An explicit ban on creating, modifying, or deleting files covers records and factual documentation corrections; tool restrictions also remain binding. Findings and proposed text can be supplied in chat within those limits, but chat does not satisfy a permanent-record obligation; the unmade record is reported as unfinished work. |
| Continued execution and reporting | Several increments can complete without a report for each one. At task completion, handoff, or when seeking input, the agent consolidates unreported work. Routine progress reports should be minimized and intermediate communication should be concise and useful. Assess a routine update against those recommendations and any requester or tool instructions; its presence alone is not an automatic violation. Required findings and records are maintained throughout. |
| Requested or required disclosures | Disclosures affecting authorization or a decision requiring requester input must precede affected work. Other information, including inquiry outcomes, should normally join the next consolidated report. Initial task framing precedes substantial work, and material inquiry uncertainty and its significance must be made clear promptly unless already communicated in the request or task framing. Reporting or notification alone creates no approval checkpoint and cannot replace required consultation. |
| Selecting and revisiting work | Plan connects the requested outcome, permission, relevant context, and evidence to a useful next increment from the first request. Assess whether that connection is understandable, including when missing evidence or consequential constraints change the next step. Study and Act inform later planning; later work stays at outline level until detail is needed and revisions stay within authorization. |
| Investigation contradicts its prediction | An evidenced answer can complete the investigation while disproving the prediction; unmet implementation behavior remains incomplete. |
| Reading existing project documentation | Reading remains context gathering without inspection-by-inspection announcements, even for a material blocking question. Inspecting relevant code, callers, tests, configuration, and directly related dependencies to establish context is also context gathering. Scope, requester limits, proportionate work, and cumulative reassessment apply to all of it. |
| Prescribed empirical operation or acceptance check | Unknown output alone does not establish inquiry. Contrast executing a settled measurement/calculation or checking acceptance with using the same procedure to investigate an unsettled approach. Classify purpose before assessing inquiry duties; a procedure neither automatically triggers nor exempts inquiry. |
| Material uncertainty about how to proceed blocks the next decision after context gathering | Promptly make the uncertainty and its significance clear unless already communicated in the request or task framing. Private planning or a retrospective report cannot replace a required timely notification. Assess actual bounded, proportionate investigation; the absence of a five-element announcement or declared effort allowance is not itself a violation. |
| The request already communicates inquiry uncertainty and its significance | No duplicate inquiry notification is required. Initial task framing, bounded conduct, sufficient evidence, cumulative reassessment, and any required consultation still apply. Coverage by the request does not authorize every consequential direction that the inquiry might suggest. |
| Inquiry exposes an unsettled consequential direction | Narrow investigation may establish facts for consultation within existing authorization. Obtain requester direction before adopting or implementing a choice requiring consultation under §2.2; merely notifying the requester or presenting evidence does not satisfy that requirement. |
| Investigation obtains sufficient evidence or reaches an increment's bounds | End inquiry when evidence is sufficient. At an increment's bounds with insufficient evidence, reassess before further investigation without claiming completion. Further attempts need justification from preceding findings and must respect authorization, limits, and checkpoints; a new advance announcement is not automatic. Report outcomes at §3.7's occasions and seek required direction before affected work. Neither an exhausted attempt nor a new increment supplies authority or resets a requester limit. |
| Acceptance-critical verification is unavailable | Sufficient alternative evidence can establish the same condition unless a specific check is required. Otherwise the condition remains unverified and validation incomplete unless validly revised. Disclosure alone does not satisfy it. |
| Equivalent evidence exists for an available acceptance check | The relevant available check must run. Equivalence alone does not permit substitution; the unavailable-check exception does not apply. |
| Known risk without an internal-quality compromise | Preserve the known risk under topic 11 without inventing a technical-debt classification. |
| Documentation-only work | Applicable methods and validation apply without requiring code or unit tests for their own sake. |
| Additional work | Reassess cumulative progress, remaining work, direction, and limits before expanding planned work or starting another increment/attempt. Each next increment needs evidence supporting its contribution and must remain within existing authorization, direction, and limits. |
| New consequential design direction or material departure | Obtain requester direction before adoption or implementation unless the specific choice is already authorized, including in a new project without established architecture. A Proposed ADR can prepare the decision; recording it or reporting later cannot supply prior authorization. |
| Handoff and resumption | Transfer meaningful results and continuation state: task objective and established direction; applicable limits/checkpoints and consumed allowances; next or unfinished increment objective/bounds/acceptance conditions; and relevant inquiry conclusions, supporting evidence, and unresolved uncertainty. A chronological activity log is insufficient. Use that state on resumption; recover missing authorization or limit state or obtain direction before dependent work. |
| Any tool fails to load the contract | The package defines no separate bootstrap stop/report/resume policy. Neither a bridge nor a README supplies one, and an unloaded contract cannot govern the failure. Use actual tool and requester instructions and distinguish loading diagnostics from demonstrated application. |
| Root and directory instruction files | Only the three root-relative contract/bridge paths receive special edit protection. Subtree rules may be added only when compatible with the root contract; the tool decides discovery, scope, and precedence, which never makes conflicting policy acceptable; encountered conflicts are reported. |

The relevant dependencies span [engineering](../../contract/prerelease_AGENTS.md#12-do--perform-the-authorized-work), [validation](../../contract/prerelease_AGENTS.md#13-study--assess-completion-and-learning), the [progression guards](../../contract/prerelease_AGENTS.md#2-progression-guards), the [triggered rules](../../contract/prerelease_AGENTS.md#3-triggered-rules) for knowledge retention and documentation, and [how the layers compose](../../contract/prerelease_AGENTS.md#4-how-the-layers-compose). Method conditions, appropriate-test recommendations, required validation, documentation scope, and requester authority all contribute to the resulting behavior.

Changes to protected instruction files follow [their authorization rule](../../contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions), including file-specific recommendations and necessary companion edits to the other two listed files; other affected documentation follows the ordinary synchronization rules. Substantive policy changes need explicit identification. An explanation or review checklist cannot substitute for the actual clauses, and a shorter contract does not by itself establish equivalent agent behavior or token savings.

### Principles and reference boundaries

Method references are linked sources explaining methods or practices named in the contract; they clarify those methods without adding rules. The accounts linked in this guide provide interpretive material within those conditions. The design draws on specific accounts rather than requiring whole frameworks or access to a paid book. The [Pragmatic Programmer book](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) is paid; its assigned public tips and extracts are freely available.

The exact [public-tip assignments](https://pragprog.com/tips/) are maintained here because the contract's links do not carry per-rule tip numbers:

| Concern | Assigned tips |
| --- | --- |
| Documentation synchronization | 13 |
| Components, boundaries, and coupling | 17, 44–45, 47–48 |
| Failures and contracts | 36–37 |
| Resources and mutation scope | 40–41 |
| Root causes | 65 |
| Attack surface | 72 |
| Naming | 74 |
| Regression checks | 94 |

The coupling assignment excludes tip 46. The DRY, inheritance, and shared-state extracts linked from their respective design explanations supply fuller accounts for their respective concerns. Attribution identifies supporting material, without claiming that one reference states the contract's combined preservation duties verbatim.

[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) supply requirement-keyword semantics. They concern the strength of agent obligations, while EARS expresses system requirements and ADRs record choices and reasons. Supporting explanations include [IHI's testing-changes guidance](https://www.ihi.org/library/model-for-improvement/testing-changes) and [arc42's debt FAQ](https://faq.arc42.org/questions/C-11-1/); they add no operating obligations.

The contract should normally suffice for ordinary cases. Under the [method-reference rules](../../contract/prerelease_AGENTS.md#39-method-references), an agent may consult a linked source when the contract leaves a material ambiguity in applying that method, reading only enough to resolve it. The ambiguity, consulted reference, and resulting interpretation must be reported, and no other practices are imported. Research stays bounded by §§1.1 and 2.4: if the consultation is inquiry into material uncertainty blocking the next decision, its notification and conduct requirements apply, including the exception for uncertainty and significance already communicated in the request or task framing. Clear rules must not be researched. Before broader research, the agent must explain the unresolved uncertainty and ask the requester. Technical research for a task follows its scope, authorization, and applicable inquiry rules. This distinction prevents an explanatory link from becoming an open-ended research assignment or importing a reference's stronger rhetoric as policy.
