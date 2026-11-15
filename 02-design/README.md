# 02 — Design

Design determines how the operating contract expresses [accepted behavioral intent and product constraints](../01-behavior/baseline.md). It owns selected mechanisms and their rationale; design selection and independent product acceptance retain distinct authority.

- [contract-design.md](contract-design.md) is the central specification: design goals and boundaries, layer composition, shared vocabulary, and the [clause-to-requirement index](contract-design.md#current-semantics-vocabulary-and-coverage).
- Its four [mechanism documents](contract-design.md#crosscutting-concepts) keep current binding prescriptions together with their necessary explanations.
- [delivery-and-portability.md](delivery-and-portability.md) owns provider integration, portability, and wording trade-offs; [methods-and-references.md](methods-and-references.md) owns method selection, reference semantics, and source assignments.
- Local `docs/` contains [design-review guidance and 28 non-normative illustrations](docs/design-review.md), plus [decisions, historical alternatives, and their status](docs/decisions-and-alternatives.md).

The [staged contract](../03-contract/prerelease_AGENTS.md) remains the self-contained normative runtime text. This README provides navigation without redefining mechanisms or accepted requirements. [Shared interfaces and authority](../docs/authority-and-change.md#cross-domain-traceability-and-feedback) and [editing guidance](../docs/authority-and-change.md#working-with-requirements-and-design-documentation) govern cross-stage maintenance; the [project README](../README.md) locates the other stages.
