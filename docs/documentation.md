# Engineering documentation

Use this reference to place engineering knowledge and preserve its rationale. For a new or unclear deliverable, start with [writing engineering documentation](writing-documentation.md). For an existing change or a review, use [maintaining and verifying documentation](maintaining-documentation.md).

## Choosing the owner

Give each fact, rule, interface, procedure, explanation, or decision one owner according to its responsibility and scope. Another document can summarize it for a different reader if it preserves the relevant qualifications and links to the detail. A copy that readers could treat as authoritative or that needs independent maintenance creates a second owner. When navigation disagrees with its source, correct the navigation.

| Location | What belongs there |
| --- | --- |
| Repository `README.md` | Project purpose, consumer adoption entry point, the five stages, and a route to shared engineering knowledge. |
| Root `docs/` | Engineering knowledge shared across stages. The [index](README.md) points to the owner for each question. |
| Engineering stage `README.md` | The stage's purpose and interfaces, with routes to its deliverables, decisions, and procedures. The shared [stage interfaces](architecture.md#stage-interfaces) define the boundaries. |
| Stage `deliverables/` | Substantive stage outputs with their individual status and authority. Keep rationale essential to interpreting a specification with the specification. |
| Stage `docs/` | Supporting architecture, decisions, rationale, guidance on deriving deliverables, and stage-specific procedures and maintenance knowledge. |

Ask what the stage produces and what someone needs to know to maintain that output. A proposed example is a Discovery output while its status is still open. An accepted rule, its constraints, and any expressly accepted defining example belong in Formulation. A selected mechanism is a Design output. A case definition and the executable checks that exercise it are Evaluations outputs. A maintainer's explanation of how to revise those checks belongs in supporting documentation. The [stage interfaces](architecture.md#stage-interfaces) locate these outputs, and the [authority rules](authority.md#status-of-engineering-records) explain what their records establish.

When several stages use a definition, keep it with the stage responsible for changing it. Keep the cross-stage interface in shared architecture. At the dependent, identify the particular rule, decision, or version it relies on using the [traceability relationships](traceability.md#tracing-a-requirement-and-its-evaluation). Link to the detail a reader needs to continue the task.

Discovery, Formulation, Design, and Evaluations use the stage layout. Candidate contains only its [five consumer files](architecture.md#staged-sources-and-release-relative-references) at the directory root. Its technical rationale belongs primarily in Design, and engineering navigation stays outside the package.

The two consumer guides can explain the same subject at different depths. Preserve each guide's practical value and the contract's strengths, conditions, and exceptions. Keep essential explanations self-contained or refer to product documentation, the contract, or external sources. The shared [consumer documentation review](consumer-documentation-review.md#reviewing-contract-explanations) covers audience and comprehension checks.

## Where the rationale belongs

A maintainer should be able to tell why a significant deliverable has its present form. Start with the upstream intent, the premises and constraints on the choice, and how the author arrived at the result. For a choice with lasting consequences, make the reasons for selection, material alternatives considered, remaining trade-offs or limitations, and decision authority and status discoverable. Use the detail warranted by the consequences. Identify an unresolved premise as such.

- **Alongside the deliverable.** If removing a reason would change how someone interprets or applies a rule, keep it there. For example, Formulation keeps the [standalone inspection boundary for PR1](../02-formulation/deliverables/baseline.md#r5) with the requirement. A Design specification can likewise keep a constraint that explains when its mechanism applies.
- **With the upstream owner.** If the reader needs the reason for an accepted outcome, link to the relevant entry in [Discovery's rationale map](../01-discovery/deliverables/objectives-and-rationale.md#rationale-map). Explain locally what that outcome implies for this deliverable.
- **In supporting documentation.** If a reader can apply the specification but needs to understand its derivation, interactions, or maintenance, place that explanation with the responsible stage and link it from the deliverable. For the choice between consequential alternatives, link to the decision record. Existing prose and links can provide the whole justification.

## Architecture, decisions, and guides

- **Architecture.** Use recognizable headings for applicable [arc42 concerns](https://arc42.org/overview/). Prefer `architecture.md` when a scope needs a standalone overview. If a deliverable already owns the architecture, link to it from the scope README. Document relevant concerns within existing owners. Omit empty sections and avoid a parallel hierarchy or a file per arc42 topic. Link to evidenced risks and technical debt, retaining the responsible owner's classification and detail.
- **Decision records.** Use an architecture decision record (ADR) when a concrete choice would constrain future changes to structure, interfaces, dependencies, compatibility, quality, or another lasting engineering concern, and future maintainers need its reasoning. A proposal ready for decision can be recorded as proposed. Keep routine implementation details with their source, operational findings with their evidence, and explanations of settled behavior with the relevant specification. See [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
- **Decision placement and scope.** Keep a stage decision with the stage whose work it governs. Put a system-wide decision in the shared collection. Link significant decisions from the scope README. Use `docs/decisions.md` by default for a dedicated collection, or link directly to the `Architecture decisions` section of a canonical architecture document. Preserve context, choice, scope, reasons, material alternatives, consequences, status, and known successors to the extent documented. Attribute dates and acceptance only where the record supports them. Related choices can share a record.
- **Guides and names.** Choose descriptive headings and filenames for the reader's purpose. Use the [Diátaxis](https://diataxis.fr/) distinction between tutorials, how-to guides, reference, and explanation where it helps. Keep material together when it serves one reading or maintenance task. Create categories or directories only for an actual need. Use lowercase hyphenated Markdown filenames, preserving established special names and staged consumer filenames. Rename an existing file only for a concrete navigation or maintenance benefit.

## Retaining decisions and current knowledge

For a substantial rewrite, use a temporary old-to-new content map with reasons for removals. Preserve unique current explanations, accepted requirements, constraints, interpretation-essential rationale, decision attribution and scope, and evidence limits. Retain ADRs, including superseded choices, their rationale, influential rejected alternatives, status, and successor links. Keep an event or date when it establishes authority, provenance, compatibility, or the validity of evidence.

Maintained engineering documentation must be understandable from the current repository. Explain substantive choices at their canonical owners and link directly to those documents. Do not link to specific repository commits, trees, blobs, or obsolete file revisions. Git history serves as a development record and can lose intermediate revisions when commits are squashed. Remove obsolete development narratives once their lasting knowledge is preserved at its owner.

Temporary maps, progress reports, validation logs, measurements, fingerprints, and authorization exchanges belong in working or delivery records. Commit identifiers can be useful in those records, diagnostic output, and review discussions. Preserve the resulting decision and its scope where they govern subsequent work.
