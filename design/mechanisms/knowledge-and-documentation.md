# Knowledge and documentation

This document owns DRY and canonical knowledge, documentation roles and synchronization, EARS, arc42, ADRs, technical debt, Diátaxis, and code-documentation choices.

**Status: current binding design, with rationale distinguished from accepted product requirements.** The [shared status and evidence boundaries](../../docs/authority-and-change.md#status-and-evidence-boundaries) retain authority and revision qualifications. These explanations add no operating duties beyond the delivered contract.

Return to [contract architecture](../contract-design.md) and its [shared vocabulary and clause-to-requirement index](../contract-design.md#current-semantics-vocabulary-and-coverage). Recording permissions, durable-finding duties, and decision authority remain in [authorization and requester decisions](requester-decisions-and-reporting.md#authorization-and-requester-decisions); disclosure timing remains in [reporting](requester-decisions-and-reporting.md#reporting-and-continued-execution). Follow [BR8](../../behavior/baseline.md#br8--durable-knowledge-without-expanded-editing-authority), [BR10](../../behavior/baseline.md#br10--affected-requirements-and-documentation), and the [decision-status and historical rationale index](../decisions-and-alternatives.md#selected-design-and-retained-decisions).

## DRY: keeping knowledge consistent as work progresses

The [Pragmatic Programmer's DRY account](https://media.pragprog.com/titles/tpp20/dry.pdf) concerns knowledge that would otherwise need independent maintenance in several places. Writing for maintainers and users, the agent MUST give each project fact, rule, or explanation one canonical owner (a file or section) and MUST prefer reuse, links, derivation, generation, or extraction over independent copies. Canonical ownership reduces the risk of divergent facts, rules, or explanations across code and documents.

A setting can own a retry limit while a guide explains its purpose and links to it. Two unrelated limits may have the same value without representing shared knowledge. Necessary generated, protocol, migration, compatibility, test, example, or summary copies MAY remain with a clear canonical owner and update process. Resemblance alone MUST NOT require abstraction: similar code MAY encode different rules.

## Documentation choices

Different project artifacts answer different questions. Requirements describe intended behavior. Accepted decisions retain choices and reasons. Architecture describes boundaries and guarantees. Schemas and package metadata declare their own constraints. Code, tests, and execution provide evidence of implemented behavior. Examples and notes govern only when explicitly labeled as rules.

These roles explain why executable behavior does not automatically overrule a requirement. If an implementation behaves differently from a required format, that disagreement is evidence to assess. The existence of the implementation does not by itself authorize changing the requirement. The contract intentionally has no global precedence ladder among these artifacts. An earlier total ordering was removed because a single ranking cannot fit artifacts that own different kinds of knowledge.

The agent MUST report contradictions, distinguish evidence from inference, and follow the knowledge's owner. If ownership leaves a consequential conflict unresolved, it MUST take that conflict to the requester under the requester-interaction rules instead of inventing a fallback order. Instruction files govern agent conduct rather than proving project facts. Requirements, constraints, and facts stated by the requester remain legitimate task context.

Documentation preserves a shared account of the project for maintainers, users, and future agents. Reading canonical facts and reasons supports Plan; producing a guide or updating affected documentation is Do work. Study checks acceptance; Act uses the findings and retains relevant learning. Requirement, record, decision, debt, documentation, and architecture duties are [triggered rules](../../contract/prerelease_AGENTS.md#3-triggered-rules) because their conditions can arise in any phase. They preserve knowledge as it emerges without authorizing work beyond their terms.

Updates follow **affected documentation**: the canonical owners of changed knowledge and the known documents that directly depend on it, whether linked or not and read or not. These documents MUST track code, tests, configuration, interfaces, architecture, and operations. A README repeating a changed value is affected even if it has no link to the owner and has not yet been read. Such dependents are typically known from the task, artifacts being inspected, explicit references, ownership, or established source/update relationships. Links alone warrant checks, not necessarily edits.

Documentation work MUST stay bounded under the increment and inquiry rules and within that affected set unless broader work is authorized. Dependents and coverage expectations MUST NOT authorize searches for unknown dependents, repository-wide audits, backfills, or reorganization; wider checks MAY be proposed. This defines the required synchronization work without making every edit a repository-wide documentation project. Documentation-only work uses the same increment, validation, and review rules as other work.

At review boundaries, the agent MUST fix stale, conflicting, duplicated, or misplaced content and links within authorized scope; analysis or review alone remains limited to the [permitted assessment writes](requester-decisions-and-reporting.md#authorization-and-requester-decisions). Current-system documents MUST describe what exists and label unfinished or proposed work. Finding an out-of-scope gap does not override scope or protected-file limits.

## arc42: shared architectural context as the project grows

[arc42](https://arc42.org/overview/) supplies the following twelve topics. Applicable topics set target coverage, rather than a mandatory empty template:

| Topic | Target subject |
| --- | --- |
| 1 | Goals, stakeholders, and fundamental requirements |
| 2 | Design and implementation constraints |
| 3 | Context and scope |
| 4 | Solution strategy |
| 5 | Building blocks |
| 6 | Runtime behavior |
| 7 | Deployment |
| 8 | Crosscutting concepts |
| 9 | Decisions |
| 10 | Quality goals and scenarios |
| 11 | Risks and technical debt, under the debt rule's qualifications |
| 12 | Glossary |

Shared content expectations aim to reduce reinvention and relearning across repositories. They give an empty project questions to answer as evidence develops, without requiring the entire design to be settled first.

Content MUST use known facts, not empty sections or invention, and detailed requirement links. For known gaps, the agent MUST propose improvements and SHOULD make them within authorized scope; conventions MUST NOT excuse gaps. The requester MAY decline, postpone, or limit changes, and material unknowns and gaps MUST stay visible. A partial or minimal architecture document does not itself breach the contract when these qualifications are respected. [Incremental documentation](https://faq.arc42.org/questions/B-14/) and [appropriate depth](https://faq.arc42.org/questions/B-4/) support keeping content useful as the system develops. [Quality scenarios](https://docs.arc42.org/section-10/) make goals assessable: “imports should be fast” still needs an agreed workload and measure.

`README.md` MUST concisely give purpose, getting started, and any documentation locations other than root `docs/`. Architecture SHOULD start in one document in the existing documentation folder (the README-stated location, otherwise root `docs/`); sections MAY split for readability or maintenance, and names and layout MAY vary. Because root `docs/` is the standard default, creating a document there requires no README location update solely for that reason. This keeps early information together. The accepted [product/internal separation decision](../../docs/engineering-history.md#requirements-led-engineering-and-productinternal-separation) owns the scoped README interpretation for this repository: consumer README navigation concerns user-facing documentation, while engineering navigation stays with the [behavior entry point](../../behavior/README.md), [evaluation guide](../../evaluations/docs/evaluations.md), and [engineering-system architecture](../../docs/architecture.md). That is a compatible engineering boundary, not an extra operating duty for adopting projects. An adequate existing arrangement can remain. Known coverage gaps still require proposals and warrant improvements within authorized scope, subject to requester limits or deferral. Summaries link to canonical requirements and ADRs, while implementation detail stays near code and tests.

Topic 11 covers known risks as well as technical debt under the contract's definition. The risk category is not restricted to internal-quality compromises: external dependencies and operational circumstances can create known risks even when implementation quality is adequate. The distinction preserves the scope of [arc42's risks and debt topic](https://docs.arc42.org/section-11/) without classifying every risk as debt or importing an additional risk-management procedure.

## EARS: making required behavior explicit

[EARS (Easy Approach to Requirements Syntax)](https://alistairmavin.com/ears/) gives natural-language requirements consistent condition-and-response patterns. The [practical guide's CSV example](../../contract/prerelease_README-powerusers.md#make-expected-behavior-explicit) illustrates this:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

The pattern exposes behavior to implement and check. It cannot decide whether to reject one row or the whole file, or define a row's line number for a particular format. Those remain project decisions. EARS applies to new or revised in-scope system requirements; unchanged requirements need no automatic conversion. Under the [current rule](../../contract/prerelease_AGENTS.md#31-new-or-revised-system-requirements), new or revised in-scope requirements MUST have canonical owners and consistently express verifiable behavior in the form `<prefix> the <system> shall <response>.` Restating a canonical requirement MUST NOT create a duplicate. The five prefixes and their applicability are:

| Pattern | Prefix before `the <system> shall <response>.` |
| --- | --- |
| Unconditional behavior | None |
| State | `While <state>,` |
| Event | `When <event>,` |
| Optional feature | `Where <feature is included>,` |
| Unwanted condition | `If <unwanted condition>, then` |

Conditions MAY combine, with state before event: `While <state>, when <event>, the <system> shall <response>.` The [system-requirement boundary and revision rules](work-cycle-and-inquiry.md#completion-predictions-and-bounded-investigation) determine what needs this form and who may change it. Rationale belongs with significant choices; EARS adds no mandatory rationale field to each requirement.

## ADRs: preserving the reasons for lasting choices

[Architecture Decision Records](https://docs.arc42.org/section-9/) retain reasons that code alone may not reveal. A streaming-parser decision can connect a memory constraint and experiment evidence with consequences for error reporting. Later work can assess that reasoning against new evidence instead of reconstructing it.

For significant architectural, optimization, compatibility, or other lasting choices in scope, the agent MUST create an ADR when a concrete proposal is ready for decision or review, in or linked from arc42 section 9. It MUST retain the decision-shaping evidence, requirements, and constraints through these fields:

| Field | Required information |
| --- | --- |
| Title | The decision's title |
| Status | Proposed, accepted, rejected, or superseded, as applicable |
| Context | Situation and constraints |
| Decision | Choice and reasons |
| Consequences | Benefits, costs, and risks |

This timing preserves developed proposals before acceptance without requiring an ADR for every exploratory idea; routine local choices SHOULD NOT create ADRs. The agent MUST distinguish proposed, accepted, rejected, and superseded decisions. Accepted MUST reflect a decision under existing authority and consultation rules, not implementation status or a new ADR-specific approval. A record cannot replace required prior requester direction for a new consequential design direction or material departure. The agent MUST preserve material history, influential failures, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links, explaining the basis and applicability of decisions. No exhaustive alternative search or out-of-scope backfill is required.

## Recording technical debt

The agent MAY record current, task-relevant, evidenced design or implementation compromises increasing maintenance cost or risk in arc42 section 11. It MUST consider accepted requirements and trade-offs. A deferred feature, rejected option, or different preference alone does not establish debt. Intended behavior is not automatically a defect, although an accepted compromise can carry debt.

Permission to record evidenced, task-relevant debt makes concerns visible without requiring separate authorization for each entry or an in-scope fix. It applies to assessment-only work too, within its write limits. The agent MUST flag uncertain classifications and report recorded debt in chat—what, why, where, and uncertainty—making the classification assessable; nonblocking disclosures SHOULD normally join the next consolidated report under the [reporting rule](requester-decisions-and-reporting.md#reporting-and-continued-execution). When in-scope work changes or resolves debt, its records in [arc42's risks and debt section](https://docs.arc42.org/section-11/) MUST be updated. Recording MUST NOT authorize fixes or override an accepted decision; contract-file protection still applies. A separate material-and-durable finding trigger can require a record even though debt recording itself is a MAY.

## Diátaxis: choosing content for the reader's need

[Diátaxis](https://diataxis.fr/) separates four needs: tutorials teach through guided practice, how-to guides help complete a task, reference supplies precise facts and interfaces, and explanation develops understanding. The [introductory guide](https://diataxis.fr/start-here/) explains these forms. A guide for correcting rejected rows can focus on the task and link to maintained format rules and background rationale.

New guides and tutorials MAY serve only an explicitly requested or agreed need; simple or low-level software may need none. In-scope guides MUST apply Diátaxis: tutorials teach by guided practice, how-tos solve tasks, reference gives facts and interfaces, and explanation builds understanding. The agent MUST NOT create empty categories for ceremony. Affected existing guides stay current under the synchronization rules. [Applying Diátaxis incrementally](https://diataxis.fr/how-to-use-diataxis/) supports this without a four-document requirement. Comments, docstrings, and generated API documentation SHOULD follow suitable existing language and tool conventions; the agent SHOULD offer requester choices for new conventions materially affecting public documentation or maintenance.
