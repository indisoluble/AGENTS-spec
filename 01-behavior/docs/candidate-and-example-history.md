# Candidate and example history

Accepted requirements are in the [baseline](../deliverables/baseline.md); current classifications, questions, and coverage are in [Discovery](../deliverables/discovery.md). This record maps proposal identifiers to accepted outcomes and identifies the limits of the acceptance evidence.

## Status and provenance

The proposal record identifies 30 RCx-Py proposals and reports in-principle acceptance for nine. Of the design alternatives D1–D10, it identifies D2-A and D3-A as selected for planning only. The record does not identify which nine proposals received that status or describe the selected alternatives in enough detail to implement them. Neither decision authorized a redesign. The owner's [behavioral acceptance summary](../deliverables/baseline.md#behavioral-acceptance-and-editorial-provenance) separately establishes the scope of BR approval.

## Disposition of the earlier candidates

RC1–RC10 identify provisional candidates. The linked baseline requirements give the accepted outcomes and point to their current design mechanisms. The identifiers do not correspond one-to-one. RC5 covers both validation (BR5) and learning (BR6), and RC10 maps to PR1 and the authorization boundaries in BR3 and BR8. Where a detail lacks acceptance evidence, its decision status remains unverified.

| Candidate | Accepted outcome in the baseline | Retained boundary |
| --- | --- | --- |
| RC1 — Bounded, complete commitments | [BR1](../deliverables/baseline.md#br1--focused-proportionate-authorized-work) | Coherence and recovery clarification included; exact decomposition remains selected design. |
| RC2 — Evidence-led planning and knowledge ownership | [BR2](../deliverables/baseline.md#br2--evidence-based-planning-and-knowledge-ownership) | Evidence and ownership accepted; the complete artifact taxonomy and planning mechanics are not automatically permanent. |
| RC3 — Authorization and consequential consultation | [BR3](../deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction) | Prior direction and retrospective-disclosure clarification included; precise current MUST/SHOULD/MAY distinctions remain intact. |
| RC4 — Purpose-based inquiry and timely awareness | [BR4](../deliverables/baseline.md#br4--bounded-investigation-and-timely-reassessment) | Reassessment after an inconclusive step is accepted. Further investigation needs justification from preceding findings and must respect authorization, limits, and checkpoints. |
| RC5 — Completion evidence and learning | [BR5](../deliverables/baseline.md#br5--completion-supported-by-validation) and [BR6](../deliverables/baseline.md#br6--learning-from-observed-results) | Completion and learning are distinct; PDSA and test-writing techniques retain current design status. |
| RC6 — Proportionate reports and continuity | [BR7](../deliverables/baseline.md#br7--proportionate-communication-and-actionable-handoffs) | Handoff limits, checkpoints, consumed allowances, and resumption clarification included. |
| RC7 — Durable knowledge and decision authority | [BR8](../deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority) | Assessment-write clarification included; record mechanisms and optional debt retain their own conditions. |
| RC8 — Engineering quality and preservation | [BR9](../deliverables/baseline.md#br9--engineering-quality-and-preservation) | Quality and preservation accepted without freezing every technique or strengthening recommendations. |
| RC9 — Requirements and documentation maintenance | [BR10](../deliverables/baseline.md#br10--affected-requirements-and-documentation) | Affected-document maintenance and out-of-scope-gap clarification included; documentation methods remain selected design. |
| RC10 — Reference and bridge behavior | [PR1](../deliverables/baseline.md#established-product-requirement), with applicable [BR3](../deliverables/baseline.md#br3--autonomy-within-authorization-and-prior-direction)/[BR8](../deliverables/baseline.md#br8--durable-knowledge-without-expanded-editing-authority) boundaries | Detailed bridge compatibility, provenance, diagnostics, [failure-to-load behavior](../../02-design/deliverables/delivery-and-portability.md#why-the-bridges-differ), and [narrow reference consultation](../../02-design/deliverables/methods-and-references.md#principles-and-reference-boundaries) retain their current design status. |

## Scenario qualification provenance

The [coverage matrix](../deliverables/discovery.md#requirement-to-scenario-coverage) includes all 44 identifiers from the owner-supplied, explicitly unaccepted `AGENTS-spec-BDD-scenarios.md` draft. The other 16 proposed examples are BR1.5–BR1.6, BR2.4, BR3.8–BR3.9, BR4.6–BR4.8, BR5.6, BR6.3, BR7.5, BR8.6–BR8.7, BR9.4–BR9.5, and BR10.4. Each suite cites the requirement and the contract or design detail used to qualify its examples. The [28 design illustrations](../../02-design/docs/design-review.md#assessing-design-changes) serve a separate editorial purpose.

For example, the inquiry and reporting proposals draw on [requester limits (§2.3)](../../03-contract/prerelease_AGENTS.md#23-effort-estimates-and-requester-limits), [notification and reassessment (§2.4)](../../03-contract/prerelease_AGENTS.md#24-context-gathering-and-bounded-inquiry), and [report timing (§3.7)](../../03-contract/prerelease_AGENTS.md#37-reporting). Contract detail qualifies a proposal without establishing its acceptance.

The examples preserve the following distinctions for acceptance review.

- **Permissions and recommendations.** BR3.1 preserves discretion over routine choices. BR3.7 preserves qualified consultation for other unsettled material choices. BR4.4–BR4.5 allow useful communication when an inquiry notice is unnecessary, and BR7.2 preserves the qualified recommendation on routine updates.
- **Disclosure and authority.** BR3.5 keeps reporting a material assumption separate from consulting about unresolved intent or permission and from seeking direction when no safe step remains. BR3.6 treats a consequential choice made without required direction as a failure even after disclosure. BR7.1 keeps initial framing distinct from an approval checkpoint. BR8.4 distinguishes narrow assessment-write permission from mandatory record triggers and optional debt recording.
- **Scope and evidence.** BR1.3 applies coherence at review boundaries and preserves advance recovery disclosure for work that cannot stand alone. BR5.2 permits substitution if the evidence is sufficient and the unavailable check was not specifically required. BR10.2 covers known direct dependents whether linked or read, with the need for an edit determined by the effect of the change.
