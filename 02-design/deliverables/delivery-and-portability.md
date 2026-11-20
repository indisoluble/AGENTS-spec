# Delivery and portability

[Contract architecture](contract-design.md) supplies design status and clause traceability. The baseline owns [PR1 self-containment](../../01-behavior/deliverables/baseline.md#established-product-requirement) and the [portability constraint](../../01-behavior/deliverables/baseline.md#portability-and-standing-context-qualifications); this document explains their integration and wording trade-offs.

## Context and Scope

These are consumer-contract loading and instruction rules (§3.8). [Development authority](../../docs/authority-and-change.md#development-time-and-runtime-authority) determines their applicability to this repository. Engineering links use [staged sources](../../docs/architecture.md#staged-sources-and-release-relative-references); consumer paths below describe installed files.

Provider claims retain their [recorded evidence dates](../../03-contract/prerelease_README-powerusers.md#evidence-dates); editorial work does not refresh them. Actual support depends on the provider and adopting environment.

### Discovery of staged instruction files

The `prerelease_*` filenames in `03-contract/` are engineering staging names. Install each instruction file using the consumer filename and location in the [staged-to-installed mapping](../../docs/architecture.md#staged-sources-and-release-relative-references).

Automatic discovery depends on the provider, interface, and configuration. See the discovery rules for [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code](https://code.claude.com/docs/en/memory), and [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions).

### Why the bridges differ

Both bridges apply the same local contract. [CLAUDE.md](../../03-contract/prerelease_CLAUDE.md) uses Claude Code's [native `@AGENTS.md` import](https://code.claude.com/docs/en/memory#import-additional-files), so one line can perform its loading role. [Copilot support](https://docs.github.com/en/copilot/reference/custom-instructions-support) varies by interface; a Markdown link identifies a file without universally importing it. Its bridge therefore explicitly directs reading/following the contract within the actual hierarchy and permissions. Claude's import and Copilot's `../AGENTS.md` link resolve from their installed locations.

Neither bridge adds a failure-to-load policy: an unloaded contract cannot govern the failure. The package defines no common bootstrap stop/report/resume protocol; actual tool and requester instructions apply. [Compatibility guidance](../../03-contract/prerelease_README-powerusers.md#tool-compatibility) supplies diagnostics without adding fallback policy.

The [instruction rule](../../03-contract/prerelease_AGENTS.md#38-instructions-protected-files-and-external-actions) distinguishes canonical ownership, bridge content, and edit protection:

| Scope | Current prescription |
| --- | --- |
| Canonical contract | Root `AGENTS.md` MUST own the repository-wide contract. |
| Two bridges | Root `CLAUDE.md` and root-relative `.github/copilot-instructions.md` MUST only discover/apply it, optionally with non-policy titles/provenance. `AGENTS.md` is not a bridge. |
| Three protected files | These three root-relative files MUST be edited only on explicit request for the file/instructions; applying file-specific recommendations counts. Necessary edits to the other two MAY accompany that request. Other affected documents follow ordinary synchronization rules. Instruction-file edits MUST stay separate from unrelated work. |

Directory instructions MAY add subtree rules only if contract-compatible. The tool sets discovery, scope, and precedence; precedence never makes conflicting policy acceptable, and conflicts MUST be reported. Compatibility constrains content rather than inventing precedence. Adoption therefore needs human validation of existing practices/workflows under the [installation precautions](../../03-contract/prerelease_README.md#get-started), without adding runtime duties or treating instructions as owners of project facts.

If loading/scope/precedence uncertainty could affect the task, the agent SHOULD inspect available diagnostics and relevant instruction files; it MUST report checks and remaining material uncertainty. Tool limits blocking loading require [disclosure](mechanisms/requester-decisions-and-reporting.md#reporting-and-continued-execution). Diagnostics and demonstrated application are different evidence.

Discovery, inclusion, precedence, and application are distinct: [VS Code conflict guidance](https://code.visualstudio.com/docs/agent-customization/custom-instructions#_resolve-conflicting-instructions), [instruction settings](https://code.visualstudio.com/docs/agents/reference/ai-settings#_custom-instructions-settings), and [GitHub.com precedence](https://docs.github.com/en/copilot/concepts/prompting/response-customization#precedence-of-custom-instructions) address different aspects. File order or a link cannot establish all four; use the [adoption checks](../../03-contract/prerelease_README-powerusers.md#check-adoption) for the actual environment.

Copilot's title/header identify the release and upstream origin; its date/source URL match `AGENTS.md`. Metadata adds no policy authority, and optional provenance does not require a Claude header. Minimality preserves each bridge's loading/application role.

External actions—commits, publishing/sending, or remote/shared-state changes—MUST be authorized. Read-only access follows task scope and tool permissions. Documentation duties and instruction-file edit requests do not independently authorize external actions.

### Keeping the contract portable

The [baseline qualifications](../../01-behavior/deliverables/baseline.md#portability-and-standing-context-qualifications) define the strongly preferred target of about 24,000 LF-normalized UTF-8 bytes, its measurement, exceptional excess, compression review, fidelity priority, and required loading headroom.

The **2026-10-04** provider check covered [Codex's documented default 32 KiB combined instruction limit](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance), Anthropic's [guidance on concise, human-readable instruction files](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md), and the context cost of [loading the contract through a Claude import](https://code.claude.com/docs/en/memory#import-additional-files). The approximate 24,000-byte project target leaves room for directory instructions and other loaded context. These sources explain the choice rather than establishing a universal ceiling or actual compatibility; delivered files, other instructions, and tool configuration still matter.

### Current wording trade-offs

Compact instructions reduce standing text but can require inferred relationships, clarification, consultation, or rework; smaller text does not establish lower total token use. Preserve these distinctions when editing:

| Treatment | Interpretation risk and review focus |
| --- | --- |
| Implicit agent subjects, short labels, slash groups | Keep actors, every duty, and relationships between grouped actions clear. |
| Broad knowledge-ownership and permitted-copy categories | Keep facts, schemas, requirements, rationale, invariants, procedures, conventions, tests, and examples recognizable under their rules. |
| Concise definitions, architecture topics, record fields, reports | Preserve distinguishing meaning and conditions; keyword matches alone do not suffice. |
| Layers and section references | Each passage needs enough local meaning; forward references may supply detail, but must not force lookahead just to understand it. Useful brief repetition is acceptable (`permitted work (§2.1)` is one example). Guards/triggers apply across phases; placement must not confine applicability or imply extra phases. |
| Initial outline and first increment | Preserve advance visibility of overall direction and next objective/bounds after preliminary context. Later work stays at outline level; framing is not approval. |
| Requester limits and consequential direction | Keep informal expectations distinct from binding limits, material ambiguity subject to clarification, and new consequential direction/material departures subject to prior consultation unless specifically authorized. Routine corrections remain autonomous. |
| Purpose-based inquiry and awareness | Keep context, execution, validation, and inquiry distinct; unknown output or a prescribed procedure alone cannot classify them. Prompt uncertainty/significance notification differs from consultation and needs no duplicate when already communicated. No declared allowance is required; announcing one cannot replace bounds, sufficient evidence, or reassessment before justified continuation. |
| Intermediate communication | Minimizing routine reports and keeping updates concise/useful are recommendations, not a ban or effort-audit duty. Consolidation, framing, inquiry notification, and advance disclosures retain distinct triggers/strengths. |
| References without per-rule numeric locators | Preserve [exact assignments](methods-and-references.md#principles-and-reference-boundaries) and narrow consultation limits so links do not become open-ended research. |

These are interpretation risks rather than added operating rules or measured outcomes. Acceptance covers only the identified wording compromises. Any new trade-off, including reduced explicitness without intended rule change, is a design decision for requester review: record what becomes less explicit, where operative meaning remains, and likely interpretation/effort consequences. Prior acceptance and matching counts establish neither losslessness nor behavioral equivalence for further reductions.
