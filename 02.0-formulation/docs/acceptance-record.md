# Acceptance sources for the product baseline

## Behavioral acceptance and editorial provenance

The owner reported acceptance of **BR1–BR10 and five clarifications**. PR1 was already established and no BR11 was needed. The owner’s account is the source for behavioral acceptance. The original verbatim approvals and their dates have not been independently verified.

[`02.0-formulation/deliverables/baseline.md`](../deliverables/baseline.md) expresses the accepted outcomes editorially, preserving obligations, qualifications and exceptions. The five clarifications concern BR1 (coherence and recovery), BR3 (unauthorized consequential choices), BR7 (handoff and consumed allowances), BR8 (assessment-only writes) and BR10 (out-of-scope documentation gaps). BR4 also incorporates the accepted clarification to reassess learning after an inconclusive step before deciding whether another step is justified. It establishes neither a default numerical budget nor an automatic approval checkpoint. The earlier RC1–RC10 IDs identified provisional proposals with no one-to-one correspondence to the accepted rules.

The requester established PR1 through the requirements-led engineering decision ([`docs/decisions.md` § Requirements-led engineering and product/internal separation](../../docs/decisions.md#requirements-led-engineering-and-productinternal-separation)) and directed that the method-selection and portability constraints be preserved. For bridges and references, PR1 covers self-containment and BR3 and BR8 govern authorization. No separate provider-policy requirement was established.

## Limits of the decisions

- The requester left the example draft ([`01-discovery/deliverables/example-coverage.md` § Sources and decision scope](../../01-discovery/deliverables/example-coverage.md#sources-and-decision-scope)) unaccepted. All examples remain proposed, including examples of accepted clarifications.
- Acceptance covers the outcomes and their essential qualifications. It does not extend to every method or wording choice used to express them. The migration-fidelity review ([`docs/decisions.md` § Engineering authority and the runtime contract](../../docs/decisions.md#engineering-authority-and-the-runtime-contract)) had its own authorization and scope.

For a subsequent decision, follow [`02.0-formulation/docs/maintaining-formulation.md` § Establish what the decision covers](maintaining-formulation.md#establish-what-the-decision-covers) to record the scope, source and any expressly accepted defining example.
