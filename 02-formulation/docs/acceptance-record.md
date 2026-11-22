# Acceptance sources for the product baseline

## Behavioral acceptance and editorial provenance

The owner reported acceptance of **BR1–BR10 and five clarifications**. PR1 was already established and no BR11 was needed. The owner’s account is the source for behavioral acceptance. The original verbatim approvals and their dates have not been independently verified.

The [baseline](../deliverables/baseline.md) expresses the accepted outcomes editorially, using the contract and design accounts to preserve obligations, qualifications and exceptions. The five clarifications concern BR1 (coherence and recovery), BR3 (unauthorized consequential choices), BR7 (handoff and consumed allowances), BR8 (assessment-only writes) and BR10 (out-of-scope documentation gaps). BR4 also incorporates the accepted clarification to reassess learning after an inconclusive step before deciding whether another step is justified. It establishes neither a default numerical budget nor an automatic approval checkpoint. The earlier RC1–RC10 IDs identified provisional proposals with no one-to-one correspondence to the accepted rules.

The requester established PR1 through the [requirements-led engineering decision](../../docs/decisions.md#requirements-led-engineering-and-productinternal-separation) and directed that the method-selection and portability constraints be preserved. For bridges and references, PR1 covers self-containment and BR3 and BR8 govern authorization. No separate provider-policy requirement was established. Design owns the [bridge behavior](../../03-design/deliverables/delivery-and-portability.md#why-the-bridges-differ) and [reference consultation rules](../../03-design/deliverables/methods-and-references.md#principles-and-reference-boundaries).

## Limits of the decisions

- The requester left the [example draft](../../01-discovery/deliverables/example-coverage.md#sources-and-decision-scope) unaccepted. All examples remain proposed, including examples of accepted clarifications.
- Selected methods, including PDSA, EARS, ADRs, arc42 and Diátaxis, retain their current strength. Design records the [selections, wording compromises and superseded controls](../../03-design/docs/decisions.md#selected-design-and-retained-decisions). The [migration-fidelity review](../../docs/decisions.md#engineering-authority-and-the-runtime-contract) had its own authorization and scope.
- The [28 Design illustrations](../../03-design/docs/design-illustrations.md) explain mechanisms. Existing evaluation expectations and observations retain their own [evidence limits](../../docs/traceability.md#what-evidence-can-establish).

For a subsequent decision, follow [Maintaining Formulation](maintaining-formulation.md#establish-what-the-decision-covers) to record the scope, source and any expressly accepted defining example.
