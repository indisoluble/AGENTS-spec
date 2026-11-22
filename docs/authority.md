# Engineering and runtime authority

## Development decisions

Product objectives, established requirements and constraints, accepted engineering decisions, and requester direction govern contract evolution and intended evaluation expectations. The requester or an explicitly authorized delegate decides outcomes, priorities, and product acceptance. Record the authorized scope, version, and decision authority. Requirement acceptance, design selection, implementation authorization, and release permission are distinct decisions. Agreement during BDD, documentation edits, and passing evaluations grant none automatically.

Discovery records the [established objectives](../01-discovery/deliverables/objectives-and-rationale.md#established-objectives). Formulation records the [accepted requirements and constraints](../02-formulation/deliverables/baseline.md). [Contract design](../03-design/deliverables/contract-design.md) specifies their selected realization.

## Status of engineering records

A record’s source and the scope of the decision determine its authority. Its directory or normative wording alone cannot establish product acceptance.

| Status | Meaning |
| --- | --- |
| **Established objective or product requirement** | Supported by requester direction or accepted records beyond implementation wording. The [objectives](../01-discovery/deliverables/objectives-and-rationale.md#established-objectives) state desired outcomes and record the sources for their priority. BR1–BR10 and PR1 have equal accepted product authority. BR1–BR10 concern agent behavior, and PR1 concerns self-contained contract delivery. [Formulation’s acceptance record](../02-formulation/docs/acceptance-record.md) records requirement sources and editorial limits. |
| **Established constraint** | A compatibility, portability, or design boundary retaining its original strength, exceptions, measurement, and revision conditions. Preserve the difference between a preferred target and a hard ceiling. |
| **Design rationale or selected decision** | A mechanism's reasons, interactions, costs, and alternatives. Selection does not make it a permanent product requirement. The [decision index](../03-design/docs/decisions.md#selected-design-and-retained-decisions) distinguishes acceptance and supersession. |
| **Current binding design prescription** | An operative mechanism specified by design and delivered through `AGENTS.md`, retaining modality, actor, trigger, timing, scope, conditions, and exceptions. Binding now does not imply enduring product acceptance. |
| **Provisional requirement candidate** | Intent inferred from rationale, examples, or clauses without independently established acceptance. The [acceptance sources and editorial limits](../02-formulation/docs/acceptance-record.md#behavioral-acceptance-and-editorial-provenance) identify which outcomes have supporting decisions. |
| **Proposed defining example** | An example awaiting acceptance, including a direct demonstration of an accepted requirement. Discovery's Direct and Detail review labels classify proposed examples. Neither establishes an accepted criterion or behavioral evidence. |
| **Historical or superseded reasoning** | Records why an earlier mechanism was considered or replaced. Source context and successor links identify the decision that now applies. |

Currently mandatory methods, including PDSA, explicit increment predictions, decomposition rules, and EARS, retain their force until authorized change. BR acceptance does not accept every clause, historical RC proposal, or design illustration. The [proposal source qualifications](../01-discovery/deliverables/example-coverage.md#sources-and-decision-scope) distinguish in-principle acceptance and selection for planning. Detailed product acceptance needs evidence of a decision by the requester or an authorized delegate. Normative wording establishes what the contract prescribes.

[E1–E40](../05-evaluations/README.md#evaluator-requirements) specify evaluator behavior. Fictional application requirements govern their fixtures. Neither source independently establishes product intent.

## Runtime authority

Delivered `AGENTS.md` is the complete normative operating contract within the consuming tool’s instruction hierarchy and permissions. Internal requirements and rationale add no operating duties. A mismatch requires human review and authorized correction. Requirements and contract wording grant no extra permission to edit protected files or make consequential decisions. The contract prescribes conduct. Enforcement depends on actual tool controls, and claims about behavior require [observational evidence](traceability.md#what-evidence-can-establish).

## Repository development and instruction loading

Established engineering direction adopts [bounded work with sufficient depth](../03-design/deliverables/mechanisms/work-cycle.md#small-commitments-with-sufficient-depth), [adequate validation](../03-design/deliverables/mechanisms/engineering-and-validation.md#validation-and-test-evidence), [behavior preservation](../03-design/deliverables/mechanisms/engineering-and-validation.md#component-boundaries-refactoring-and-validation), [canonical knowledge ownership](../03-design/deliverables/mechanisms/knowledge-and-documentation.md#dry-keeping-knowledge-consistent-as-work-progresses), and appropriate [documentation](../03-design/deliverables/mechanisms/knowledge-and-documentation.md#documentation-choices) and [decision records](../03-design/deliverables/mechanisms/knowledge-and-documentation.md#adrs-preserving-the-reasons-for-lasting-choices). This scoped adoption is subject to developer direction, higher-priority instructions, and actual permissions. It does not adopt the entire candidate or automatically apply consumer-specific loading or protected-file rules to this repository.

`04-candidate/pre_AGENTS.md` is staged source, not a standard automatic development instruction entry point. There is no root `AGENTS.md`, root `CLAUDE.md`, or active `.github/copilot-instructions.md` importing it. Agents may explicitly read the source, and Evaluations supplies it to the evaluated agent. Neither use activates it for repository development. See the [staged-source mapping](architecture.md#staged-sources-and-release-relative-references). Development instructions require an actual supported instruction or task mechanism. Documentation neither configures loading nor unloads instructions already present in a session.

Authorized redesign can reconsider PDSA, the three-layer organization, or another selected mechanism. Loaded instructions still apply. A necessary engineering-process change must be explicitly authorized and technically effective.
