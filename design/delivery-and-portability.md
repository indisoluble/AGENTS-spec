# Delivery and portability

This document owns provider integration and bridge rationale, portability evidence, standing-context trade-offs, and wording/compression risks.

**Status: current binding design, with rationale distinguished from accepted product requirements.** The [shared status and evidence boundaries](../docs/authority-and-change.md#status-and-evidence-boundaries) retain authority and revision qualifications. These explanations add no operating duties beyond the delivered contract.

Return to [contract architecture](contract-design.md) and its [clause-to-requirement index](contract-design.md#current-semantics-vocabulary-and-coverage). The accepted [PR1 self-containment requirement](../behavior/baseline.md#established-product-requirement) and [portability qualifications](../behavior/baseline.md#portability-and-standing-context-qualifications) remain owned by the baseline. See [consumer-artifact boundaries and release-relative references](../docs/architecture.md#staged-sources-and-release-relative-references), [reference consultation limits](methods-and-references.md#principles-and-reference-boundaries), and [decision status and rationale](decisions-and-alternatives.md#selected-design-and-retained-decisions). Provider evidence below retains its original dates; this extraction does not refresh it.

## Context and Scope

This view describes provider integration and instruction-loading boundaries for the delivered consumer contract. AGENTS-spec development authority, instruction loading, and the scoped adoption of engineering practices remain defined by the [engineering-system architecture](../docs/authority-and-change.md#development-time-and-runtime-authority); these consumer-contract rules are not automatically adopted for repository development.

### Why the bridges differ

The provider explanations here retain their existing source provenance; the [recorded evidence dates](../contract/prerelease_README-powerusers.md#evidence-dates) still apply, and this restructuring does not refresh them. Actual support needs checking in the adopting environment.

Both bridges apply the same local contract through their tool's instruction mechanisms. [CLAUDE.md](../contract/prerelease_CLAUDE.md) uses `@AGENTS.md`, Claude Code's [native import syntax](https://code.claude.com/docs/en/memory#import-additional-files), to include the referenced content. The single line can therefore perform its loading role.

[Copilot support](https://docs.github.com/en/copilot/reference/custom-instructions-support) varies by interface. A Markdown link identifies a file but is not a universal import mechanism. The supplied bridge explicitly directs reading and following the local contract within the actual hierarchy and permissions. Neither supplied bridge defines independent behavior for a failure to load the contract. The contract cannot govern an agent that never received it, so the package supplies no common stop/report/resume protocol for that case. Actual tool and requester instructions govern the situation. The [practical compatibility guidance](../contract/prerelease_README-powerusers.md#tool-compatibility) explains this limitation and adoption diagnostics; it adds no fallback operating policy.

The [current instruction rule](../contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions) assigns **two different scopes**:

| Scope | Current prescription |
| --- | --- |
| Canonical contract | Root `AGENTS.md` MUST own the canonical repository-wide contract. |
| Two bridges only | Root `CLAUDE.md` and root-relative `.github/copilot-instructions.md` MUST only discover and apply that contract, optionally with non-policy titles or provenance. `AGENTS.md` is not a bridge. |
| Three protected files | `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` MUST be edited only on explicit request for the file or instructions; applying file-specific recommendations counts. Necessary edits to the other two MAY accompany that request. Other affected documents follow the ordinary canonical-knowledge and synchronization rules. These instruction-file edits MUST stay separate from unrelated work. |

Directory instructions MAY add subtree rules only if contract-compatible. The actual tool sets discovery, scope, and precedence; that precedence never makes conflicting policy acceptable, and the agent MUST report conflicts. Compatibility is a content rule, not an invented precedence mechanism. Adoption guidance therefore calls for human validation of which existing practices, conventions, and workflows persist, following the [basic installation precautions](../contract/prerelease_README.md#get-started); that guidance is not an extra runtime rule. Project facts and operating rules have different owners.

If uncertainty about loading, scope, or precedence could affect the task, the agent SHOULD check available diagnostics and relevant instruction files; it MUST report what was checked and remaining material uncertainty. Tool limits blocking instruction loading also require the [tool-limit disclosure](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution). Diagnostic inspection and demonstrated application are different evidence, and these rules add no bootstrap protocol for a contract that was never loaded.

External actions—commits, publishing or sending, or changes to remote or shared state—MUST be authorized. Read-only access follows task scope and tool permissions. Neither documentation duties nor an instruction-file edit request independently authorizes an external action.

Discovery, inclusion, precedence, and application are distinct. [VS Code's conflict guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#_resolve-conflicting-instructions), its [instruction settings](https://code.visualstudio.com/docs/agents/reference/ai-settings#_custom-instructions-settings), and [GitHub.com's precedence guidance](https://docs.github.com/en/copilot/concepts/prompting/response-customization#precedence-of-custom-instructions) describe different aspects. File order or a link alone cannot establish all four. The [adoption checks](../contract/prerelease_README-powerusers.md#check-adoption) and [recorded evidence dates](../contract/prerelease_README-powerusers.md#evidence-dates) qualify the integration guidance; exact settings and support depend on the provider's documentation and the actual environment.

The Copilot title and header identify the associated release and upstream origin. Its release date and source URL match `AGENTS.md`. Metadata adds no policy authority, and the adopted local contract remains canonical. Permitting provenance does not require a header on the one-line Claude import. Minimality preserves each bridge's loading and application role.

### Keeping the contract portable

The established [portability and standing-context qualifications](../behavior/baseline.md#portability-and-standing-context-qualifications) own the size target and its operative conditions. This section explains the design rationale and supporting provider evidence rather than independently defining those constraints.

The provider evidence supporting the choice below retains its recorded **2026-10-04** check date in the [evidence-date owner](../contract/prerelease_README-powerusers.md#evidence-dates). It has not been newly verified by this restructuring; applicable limits still depend on the actual provider and environment.

The target was informed by [Codex's documented default 32 KiB combined instruction limit](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance) and Anthropic's [guidance to keep `CLAUDE.md` concise and human-readable](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md). The approximate 24,000-byte figure is a project choice: it leaves room below Codex's default for directory instructions and other loaded instruction or configuration context, and reflects Claude Code's guidance on limiting standing context. Importing the contract through `CLAUDE.md` still [loads its contents into context](https://code.claude.com/docs/en/memory#import-additional-files). These sources are provider evidence for the design choice, not a universal ceiling or proof of actual provider compatibility; the canonical qualifications retain the distinctions concerning delivered files, other loaded instructions, tool configuration, clarity, and precision.

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
| Reference links without per-rule numeric locators | The [exact assignments](methods-and-references.md#principles-and-reference-boundaries) preserve attribution; narrow consultation limits prevent the links from becoming open-ended research. |

These are interpretation risks, not additional operating rules or measured agent outcomes. The [canonical portability qualifications](../behavior/baseline.md#portability-and-standing-context-qualifications) retain the fidelity and self-containment constraints governing compression.

Acceptance of the current wording compromises covers only the identified trade-offs. It does not authorize further loss of precision. Any new trade-off, including reduced explicitness without an intended rule change, is a design decision to identify for requester review. Its rationale needs to record what becomes less explicit, where the operative meaning remains, and the likely interpretation or effort consequences. Previous acceptance and matching counts do not establish that a further reduction is lossless or behaviorally equivalent.
