# Documentation maintenance for AGENTS-spec

Use this file when editing the repository's documentation. It defines ownership, a short editing workflow, and the checks needed to preserve meaning. It sits outside the ordinary path for learning about or using [AGENTS.md](AGENTS.md) and adds no operating obligations to that contract.

## Document ownership

Keep the three reader-facing guides and this editorial file at the repository root.

| File | Owns |
| --- | --- |
| Root [AGENTS.md](AGENTS.md) | The self-contained repository-wide operating contract: exact definitions, requirements, permissions, triggers, conditions, and exceptions. Project facts and commands belong in the adopting project's code and documentation. |
| Root [CLAUDE.md](CLAUDE.md) and root-relative [.github/copilot-instructions.md](.github/copilot-instructions.md) | Discovery and application of the local contract, with permitted non-policy titles and provenance. No independent or duplicated collaboration policy in these bridges; directory instruction files follow the contract's separate scope rules. |
| [README.md](README.md) | Basic adoption: the offering, installation, replacement precautions, adoption checks, a first task, and essential expectations. |
| [README-powerusers.md](README-powerusers.md) | Detailed practical explanations and examples, alignment, tool compatibility, adoption diagnostics, and recorded provider-documentation check dates. |
| [README-maintainers.md](README-maintainers.md) | The contract's design: attributes, reasons, engineering choices, exact reference assignments, trade-offs, portability criteria, and constraints on evolution. |
| `META-README.md` | Documentation responsibilities, permitted overlap, editing procedures, and verification. |

The ordinary reading path starts at `README.md` and branches into practical use or technical understanding. Keep editorial navigation out of that path; contributors can discover this root file directly. “Power users” means readers seeking practical depth, without requiring technical expertise. The maintainer guide documents the contract itself; it is not a contributor onboarding manual.

### Check the authority or evidence for each kind of statement

When editing a guide, check each statement against the authority, reference, or evidence that governs that kind of statement:

| Statement being edited | Where to check |
| --- | --- |
| What an agent is required or permitted to do under this contract | [AGENTS.md](AGENTS.md). Preserve its rule strengths, conditions, scope, and exceptions. |
| How this contract uses an adopted method, such as PDSA, Simple Design, DRY, EARS, arc42, or Diátaxis | [AGENTS.md](AGENTS.md), which is authoritative for the method's operational meaning under the contract. For deeper explanation of that role, use the technical guide's design sections, such as [Engineering choices](README-maintainers.md#engineering-choices) and [Documentation choices](README-maintainers.md#documentation-choices); they explain the contract without overriding it. |
| General background on a named method, or clarification of a material ambiguity in the contract's use of it | The external method reference already linked from `AGENTS.md` or `README-maintainers.md`, consulted only when needed. It supplies background, attribution, or clarification, not additional policy; import no other practices from it. The technical guide explains these [reference boundaries](README-maintainers.md#principles-and-reference-boundaries). |
| How a tool discovers or applies instructions | The tool's current official documentation, such as the documentation for OpenAI Codex, Anthropic Claude Code, or GitHub Copilot. This is evidence about external product behavior, not interpretation of the contract. [Tool compatibility](README-powerusers.md#tool-compatibility) links to this documentation and records when it was checked. |
| Why the contract chose a method, and the reasons and constraints for changing `AGENTS.md` | The [design rationale](README-maintainers.md#design-goals-and-boundaries), [method-selection criteria](README-maintainers.md#choosing-or-replacing-methods), and [portability constraints](README-maintainers.md#keeping-the-contract-portable) in the technical guide. These guide evolution of the contract; they add no duties to ordinary project tasks performed under it. |

When updating a guide, explain an adopted method from its operational meaning in `AGENTS.md`. Routine consultation of external method references is unnecessary when the contract is clear. If a material ambiguity remains about the contract's use of a method, read only enough of the linked reference to resolve it, consistent with the contract's [method-reference rule](AGENTS.md#39-method-references), and do not present the result as a new rule. If a reference recommends additional or stronger practices, do not describe them as requirements unless `AGENTS.md` requires them. A guide explains the contract; changing the contract requires an explicit update to `AGENTS.md`.

When explaining how an agent tool works, check its official documentation. Do not suggest that `AGENTS.md` overrides the tool’s higher-priority instructions, grants additional permissions, or bypasses required approvals. See [Authority and scope](AGENTS.md#21-authority-and-scope) and [Instructions, protected files, and external actions](AGENTS.md#38-instructions-protected-files-and-external-actions).

### Summaries and overlap

Give each fact, procedure, rule, or detailed explanation one authoritative owner. Elsewhere, use a reader-appropriate summary and a direct link. Preserve conditions and exceptions locally when their omission would make that summary misleading.

A brief introduction, a practical explanation, and a design rationale may discuss the same subject for different reader needs. Let each answer its reader's question, and link to the fuller treatment where useful. Avoid copying complete procedures, reference-assignment tables, or lifecycle descriptions between guides; necessary copies need a clear owner and update relationship. Different wording alone does not establish a separate responsibility.

Keep examples tied to the rules they illustrate. Make their assumptions visible and distinguish an illustrative choice from a general requirement. Neither an example nor an editorial checklist should become a second source of operating policy.

The [practical CSV walkthrough](README-powerusers.md#from-a-request-to-a-result) owns the shared scenario facts. The [technical walkthrough](README-maintainers.md#how-the-design-works-in-a-task) uses those facts to explain design choices; keep it aligned when the practical example changes. Alternative paths and additional examples state their own assumptions locally.

## Editing workflow

1. **Identify the change and its owner.** Separate editorial clarification from changed operating behavior. Any edit to `AGENTS.md` or a bridge, including an editorial edit, follows the [protected-file authorization rule](AGENTS.md#38-instructions-protected-files-and-external-actions). Identify behavior changes explicitly; a README cannot enact them.
2. **Update the authoritative explanation first.** For a clarification, identify the relevant contract clauses and current rationale, then edit the explanation in its owner. For a policy change, align explanations with the authorized contract change. Preserve each rule's meaning and qualifications.
3. **Follow its dependencies.** Update affected summaries, examples, references, and bridge explanations. Check incoming links throughout the repository when headings or paths move. If a known external link would break, consider retaining its Markdown heading with a brief link to the new location.
4. **Walk through the reader's task.** Use the paths below to check progression and discoverability. For a substantial rewrite, maintain a temporary map from old content to its new location, recording why any material is removed, so unique explanations do not disappear.
5. **Review the complete result.** Apply the checklist below. Use relevant [design scenarios](README-maintainers.md#assessing-design-changes) to check explanations against the contract. If the contract changes, also apply the technical guide's [portability criteria](README-maintainers.md#keeping-the-contract-portable).

Keep current descriptions and useful lasting rationale in their owners. Revision narratives, obsolete alternatives, draft measurements, package fingerprints, and temporary content maps belong in working notes or delivery records. Retain only enduring ownership guidance here. A shorter entry point must not be achieved by quietly dropping necessary explanations from the repository.

## Reader paths

- **[README.md](README.md) — basic guide:** explain the primary benefit sought, give actionable installation steps and a useful first task, then show essential expectations and further reading. A newcomer should be able to adopt the contract using this guide alone.
- **[README-powerusers.md](README-powerusers.md) — practical guide:** begin with an ordinary outcome-oriented request and show how the agent handles it. Then explain situations the user may encounter. Put detailed reference material where readers can find it without making it a prerequisite for the first example.
- **[README-maintainers.md](README-maintainers.md) — technical guide:** connect design problems with chosen approaches, reasons, trade-offs, and implications for future changes. Keep sufficient method and reference detail available for assessing the contract. Keep instructions for maintaining the READMEs in `META-README.md`.

Use plain Markdown only, descriptive headings, direct links, and tables for comparisons. Introduce terms before depending on them; explain methods where they clarify an action or design choice. Present default behavior before optional requester controls.

When explaining a workflow, give the overall path before developing individual activities. Show what prompts a decision, what context or evidence informs it, and how the result affects what follows. Naming phases or linking to their definitions does not by itself explain these connections. Read examples from the reader's starting point, without relying on knowledge from the editing conversation.

There is no numeric length limit for these guides. Assess necessary detail, repetition, navigation, and the combined impression of headings and examples. Accurate sentences still need a reading path that teaches the intended responsibilities. Keep consequential qualifications close to their claims; avoid empty categories, obligatory templates, and formalism that adds no understanding.

## Meaning and evidence checklist

Use these editorial checks for the complete change. The technical guide's [design scenarios](README-maintainers.md#assessing-design-changes) own the detailed review cases; the contract owns the behavior being explained.

1. **Purpose, coverage, and ownership.** Check that each guide fulfills its reader's purpose and preserves the contract's stated goal and limits. Confirm that necessary explanations remain available at the appropriate depth and that consolidation has not deleted unique knowledge. Keep editorial procedures here and design rationale in the technical guide.
2. **Fidelity to the contract.** Compare affected claims with the authoritative clauses. Preserve the actor, rule strength, trigger, timing, scope, conditions, and exceptions, including relevant shared rules. Check both individual sentences and their combined implication. A paraphrase, heading, or example must not introduce an obligation, permission, exception, or procedural requirement.
3. **Connected explanations.** Follow each walkthrough from its starting request through decisions, actions, evidence, and what follows. Can the reader understand how a choice was reached and what could change it? Use the [reader comprehension questions](#reader-comprehension-questions) to review progression and, when testing substantial rewrites with readers, identify what they can explain without coaching. Keep distinctions made by the contract visible; do not imply an extra process merely to organize the explanation.
4. **Examples and qualifications.** Identify assumed project facts, illustrative choices, expected outcomes, and observed results clearly. Keep conditions close enough to prevent examples from becoming apparent defaults or guarantees. Check alternative outcomes against the same rules as the successful path.
5. **References, attribution, and provider evidence.** Preserve links to primary references and exact attribution using the technical guide's [reference assignments](README-maintainers.md#principles-and-reference-boundaries). Do not import a whole framework or a reference's stronger rhetoric as policy. Retain original provider-check dates when moving guidance; record a new date only for a newly verified or changed claim. Editorial work does not refresh external evidence.
6. **Evidence for claims.** Match claims about benefits, limits, and compatibility to the available evidence. Distinguish intended effects from demonstrated outcomes. Textual consistency does not establish measured comprehension, equivalent agent behavior, or token savings.
7. **Links and delivery.** Check Markdown, relative paths, heading anchors, incoming links, and delivered file versions against the intended repository layout. Confirm that summaries agree with their owners. Apply artifact-specific criteria from their authoritative location when those artifacts change, and keep transient measurements and validation records out of the guides.

### Reader comprehension questions

Use these questions to assess whether the guides teach their intended responsibilities. They complement the technical guide's [design scenarios](README-maintainers.md#assessing-design-changes), which assess the contract's behavior and meaning; keep the detailed behavioral scenarios in the technical guide. These are editorial checks, not extra operating duties for agents using the contract.

| After reading | The reader should be able to explain |
| --- | --- |
| [README.md](README.md) | What the file is for, which files to install for their tool, how to check adoption, and what token control can and cannot promise. |
| [From a request to a result](README-powerusers.md#from-a-request-to-a-result) | Why the agent selected that increment, what would count as completion, and how the findings affect subsequent work. |
| [When the agent pauses or continues](README-powerusers.md#when-the-agent-pauses-or-continues) | Why completing an increment, reporting a result, and requesting approval are separate events; when existing authorization permits continuation and when direction is required. |
| [Use requirements and documentation](README-powerusers.md#use-requirements-and-documentation) | Which requirements or records may be created or updated, what triggers them, and why examples do not prescribe a document for every step. |

For reader testing, give representative newcomers the relevant guide and ask them to carry out or explain these tasks in their own words. A junior developer familiar with Git and a coding agent should be able to follow basic adoption without first studying the contract's engineering methods. Record where a reader cannot find an answer separately from where an explanation is misunderstood. Keep test observations in working or review records, and distinguish observed comprehension from an editor's prediction; an editorial review alone does not establish usability.
