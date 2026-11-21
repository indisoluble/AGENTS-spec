# Engineering documentation

## Choosing the owner

Give each fact, rule, interface, procedure, explanation, or decision one owner according to its responsibility and scope. Another document can summarize it for a different reader if it preserves the relevant qualifications and links to the detail. A copy that readers could treat as authoritative or that needs independent maintenance creates a second owner. When navigation disagrees with its source, correct the navigation.

| Location | What belongs there |
| --- | --- |
| Repository `README.md` | Project purpose, consumer adoption entry point, the five stages, and a route to shared engineering knowledge. |
| Root `docs/` | Engineering knowledge shared across stages. The [index](README.md) points to the owner for each question. |
| Engineering stage `README.md` | The stage's purpose and interfaces, with routes to its deliverables, decisions, and procedures. The shared [stage interfaces](architecture.md#stage-interfaces) define the boundaries. |
| Stage `deliverables/` | Substantive stage outputs with their individual status and authority. Keep rationale essential to interpreting a specification with the specification. |
| Stage `docs/` | Supporting architecture, decisions, rationale, guidance on deriving deliverables, and stage-specific procedures and maintenance knowledge. |

Discovery, Formulation, Design, and Evaluations use the stage layout. Candidate contains only its [five consumer files](architecture.md#staged-sources-and-release-relative-references) at the directory root. Its technical rationale belongs primarily in Design, and engineering navigation stays outside the package.

The two consumer guides can explain the same subject at different depths. Preserve each guide's practical value and the contract's strengths, conditions, and exceptions. Keep essential explanations self-contained or refer to product documentation, the contract, or external sources. Design owns the [audience and comprehension checks](../03-design/docs/design-review.md#reviewing-contract-explanations).

## Architecture, decisions, and guides

- **Architecture.** Use recognizable headings for applicable [arc42 concerns](https://arc42.org/overview/). Prefer `architecture.md` when a scope needs a standalone overview. If a deliverable already owns the architecture, link to it from the scope README. Document relevant concerns within existing owners. Omit empty sections and avoid a parallel hierarchy or a file per arc42 topic. Link to evidenced risks and technical debt, retaining the responsible owner's classification and detail.
- **Decision records.** Link significant decisions from the scope README. Use `docs/decisions.md` by default for a dedicated collection, or link directly to the `Architecture decisions` section of a canonical architecture document. Preserve the choice, context, scope, rationale, material alternatives, consequences, status, and known successors to the extent documented. Attribute dates and acceptance only where the record supports them. Related choices can share a record. See [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
- **Guides and names.** Choose descriptive headings and filenames for the reader's purpose. Use the [Diátaxis](https://diataxis.fr/) distinction between tutorials, how-to guides, reference, and explanation where it helps. Keep material together when it serves one reading or maintenance task. Create categories or directories only for an actual need. Use lowercase hyphenated Markdown filenames, preserving established special names and staged consumer filenames. Rename an existing file only for a concrete navigation or maintenance benefit.

## Maintaining documentation after a change

Follow known direct dependents within the authorized scope, including summaries that repeat changed knowledge. Inspect each [reference's role](traceability.md#reading-a-reference). When material moves, update affected links, labels, heading fragments, and plain-text references to point directly to its new owner. Report out-of-scope gaps separately. The conventions add no central editorial approval and grant no authority to search for unknown dependents, audit, or backfill.

For a substantial rewrite, use a temporary old-to-new content map with reasons for removals. Preserve unique current explanations, accepted requirements, constraints, interpretation-essential rationale, decision attribution and scope, and evidence limits. Retain ADRs, including superseded choices, their rationale, influential rejected alternatives, status, and successor links. Keep an event or date when it establishes authority, provenance, compatibility, or the validity of evidence.

Use Git history for obsolete descriptions of earlier development states. Temporary maps, progress reports, validation logs, measurements, fingerprints, and authorization exchanges belong in working or delivery records. Preserve the resulting decision and its scope where they govern subsequent work.
