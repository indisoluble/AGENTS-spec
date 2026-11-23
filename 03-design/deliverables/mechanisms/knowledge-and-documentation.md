# Knowledge and documentation

Contract architecture ([`03-design/deliverables/contract-design.md`](../contract-design.md)) supplies status and vocabulary. This document explains knowledge ownership and documentation methods. Authorization ([`03-design/deliverables/mechanisms/requester-decisions-and-reporting.md` § Authorization and requester decisions](requester-decisions-and-reporting.md#authorization-and-requester-decisions)) determines assessment-write permissions and durable-finding duties; reporting ([`03-design/deliverables/mechanisms/requester-decisions-and-reporting.md` § Reporting and continued execution](requester-decisions-and-reporting.md#reporting-and-continued-execution)) determines disclosure timing.

## DRY: keeping knowledge consistent as work progresses

The [Pragmatic Programmer's DRY account](https://media.pragprog.com/titles/tpp20/dry.pdf) concerns knowledge otherwise requiring independent maintenance in several places. Writing for maintainers and users, the agent MUST give each project fact, rule, or explanation one canonical owner (file/section) and MUST prefer reuse, links, derivation, generation, or extraction over independent copies. This reduces the risk of divergence.

A setting can own a retry limit while a guide explains its purpose and links to it. Two unrelated limits with the same value need not represent shared knowledge. Resemblance alone MUST NOT require abstraction: similar code MAY encode different rules. Necessary generated, protocol, migration, compatibility, test, example, or summary copies MAY remain with a clear owner and update process.

## Documentation choices

Project artifacts have role-specific owners rather than a global precedence order:

| Artifact | Knowledge role |
| --- | --- |
| Requirements | Intended behavior |
| Accepted decisions | Choices and reasons |
| Architecture | Boundaries and guarantees |
| Schemas/package metadata | Declared constraints |
| Code/tests/execution | Evidence of implemented behavior |
| Examples/notes | Rules only when explicitly labeled as such |

A total ordering was rejected because different artifacts own different knowledge. Implemented behavior can contradict a requirement without authorizing its revision. The agent MUST report contradictions, distinguish evidence from inference, and follow the relevant owner. Consequential conflicts unresolved by ownership MUST go to the requester. Instruction files govern conduct rather than proving project facts; requester-stated facts, requirements, and constraints remain task context.

Documentation preserves knowledge for maintainers, users, and future agents. Reading it supports Plan; writing it can be Do work; Study validates it and Act retains learning. Record and documentation triggers can arise in any phase without expanding authority.

Affected documentation comprises canonical owners of changed knowledge and known direct dependents, linked or not, read or not. It MUST track code, tests, configuration, interfaces, architecture, and operations. A README repeating a changed value is affected even without a link. Dependents are known through the task, inspected artifacts, references, ownership, or source/update relationships; links alone warrant checks, not necessarily edits.

Documentation work MUST remain bounded and within that set unless broader work is authorized. Dependents and target coverage MUST NOT authorize searches for unknown dependents, repository-wide audits, backfills, or reorganization; wider checks MAY be proposed. Documentation-only work follows the same increment, validation, and review rules.

At review boundaries, the agent MUST fix stale, conflicting, duplicated, or misplaced content and links within authorized scope; assessment-only writes retain their narrower permission. Current-system documents MUST describe what exists and label proposed/unfinished work. Out-of-scope gaps do not override editing scope or instruction-file protection.

## arc42: shared architectural context as the project grows

[arc42](https://arc42.org/overview/) supplies twelve topics; applicable topics set target coverage rather than a mandatory empty template:

| Topic | Subject |
| --- | --- |
| 1 | Goals, stakeholders, fundamental requirements |
| 2 | Design/implementation constraints |
| 3 | Context and scope |
| 4 | Solution strategy |
| 5 | Building blocks |
| 6 | Runtime behavior |
| 7 | Deployment |
| 8 | Crosscutting concepts |
| 9 | Decisions |
| 10 | Quality goals/scenarios |
| 11 | Risks and technical debt under its own qualifications |
| 12 | Glossary |

Shared coverage aims to reduce reinvention and relearning, giving new projects questions to answer as evidence develops. Content MUST use known facts, detailed requirement links, and no empty sections or invention. For known gaps, the agent MUST propose improvements and SHOULD make them within authorized scope; conventions MUST NOT excuse gaps. The requester MAY decline, postpone, or limit changes; material unknowns/gaps MUST remain visible. A partial architecture can therefore comply. [Incremental documentation](https://faq.arc42.org/questions/B-14/) and [appropriate depth](https://faq.arc42.org/questions/B-4/) support this approach; [quality scenarios](https://docs.arc42.org/section-10/) make goals assessable—“imports should be fast” needs an agreed workload and measure.

`README.md` MUST concisely give purpose, getting started, and documentation locations other than root `docs/`. Architecture SHOULD start in one document in the existing documentation folder (README-stated, otherwise root `docs/`); sections MAY split for readability/maintenance and names/layout MAY vary. This keeps early information together while permitting adequate existing arrangements. A new document in default root `docs/` needs no README location update solely for that reason. Summaries link to canonical requirements/ADRs; implementation detail stays near code/tests. AGENTS-spec's product/internal separation ([`docs/decisions.md` § Requirements-led engineering and product/internal separation](../../../docs/decisions.md#requirements-led-engineering-and-productinternal-separation)) assigns consumer and engineering navigation to their respective audiences without adding consumer duties.

Topic 11 includes known risks beyond internal-quality compromises: external dependencies or operations can create risks without technical debt. Preserve that [risks/debt distinction](https://docs.arc42.org/section-11/) without inventing a risk-management procedure.

## EARS: making required behavior explicit

[EARS (Easy Approach to Requirements Syntax)](https://alistairmavin.com/ears/) gives natural-language requirements consistent condition/response patterns. For example:

> If an input row has a different number of fields from the header, then the importer shall reject that row and report its line number.

The pattern exposes behavior to implement/check; it cannot decide row versus file rejection or the line-number convention. Those remain project decisions. New/revised in-scope system requirements MUST have canonical owners and consistently express verifiable behavior as `<prefix> the <system> shall <response>.` Unchanged requirements need no automatic conversion; restating a canonical requirement MUST NOT duplicate it.

| Pattern | Prefix |
| --- | --- |
| Unconditional | None |
| State | `While <state>,` |
| Event | `When <event>,` |
| Optional feature | `Where <feature is included>,` |
| Unwanted condition | `If <unwanted condition>, then` |

Conditions MAY combine, state before event: `While <state>, when <event>, the <system> shall <response>.` The requirement boundary ([`03-design/deliverables/mechanisms/work-cycle.md` § Requirements, acceptance conditions, and predictions](work-cycle.md#requirements-acceptance-conditions-and-predictions)) and revision authority ([`03-design/deliverables/mechanisms/engineering-and-validation.md` § Validation and test evidence](engineering-and-validation.md#validation-and-test-evidence)) determine applicability and permitted change. EARS adds no mandatory rationale field; significant choices retain their reasons under the decision rule.

## ADRs: preserving the reasons for lasting choices

[Architecture Decision Records (ADRs)](https://docs.arc42.org/section-9/) retain reasons code may not reveal. A streaming-parser choice can connect memory constraints and experiment evidence with error-reporting consequences, allowing later reassessment rather than reconstruction.

For significant architectural, optimization, compatibility, or other lasting choices in scope, the agent MUST create an ADR when a concrete proposal is ready for decision/review, in or linked from arc42 section 9. It MUST retain decision-shaping evidence, requirements, and constraints through: **title**; **status**; **context** (situation/constraints); **decision** (choice/reasons); and **consequences** (benefits/costs/risks).

This timing preserves developed proposals before acceptance without recording every exploratory idea; routine local choices SHOULD NOT create ADRs. The agent MUST distinguish proposed, accepted, rejected, and superseded status. Accepted MUST reflect existing decision authority/consultation, not implementation status or an additional ADR approval. Records cannot replace prior requester direction. Material history, influential failures, useful [rejected alternatives](https://docs.arc42.org/tips/9-6/), and replacement links MUST be preserved, without an exhaustive alternative search or out-of-scope backfill.

## Recording technical debt

The agent MAY record current, task-relevant, evidenced design/implementation compromises increasing maintenance cost or risk in [arc42 section 11](https://docs.arc42.org/section-11/). It MUST consider accepted requirements/trade-offs: deferred features, rejected options, or preferences alone are not debt. Intended behavior is not automatically a defect, though an accepted compromise can carry debt.

This permission makes concerns visible, including during assessment within its write limits, without separate permission for each entry or an obligation to fix it. The agent MUST flag uncertain classifications and report recorded debt in chat (what, why, where, uncertainty); nonblocking disclosures SHOULD normally join the next consolidated report. Records MUST be updated when in-scope work changes/resolves debt. Recording MUST NOT authorize fixes or override decisions; protected-file rules still apply. A separate material-and-durable finding trigger can require a record although debt recording itself is optional.

## Diátaxis: choosing content for the reader's need

[Diátaxis](https://diataxis.fr/) separates four needs: tutorials teach by guided practice, how-tos solve tasks, reference supplies facts/interfaces, and explanation builds understanding. A guide to correcting rejected rows can focus on that task and link to maintained format rules and rationale.

New guides/tutorials MAY serve only an explicitly requested or agreed need; some software needs none. In-scope guides MUST apply Diátaxis. The agent MUST NOT create empty categories for ceremony. Existing affected guides stay current through synchronization. [Incremental application](https://diataxis.fr/how-to-use-diataxis/) requires no four-document set. Comments, docstrings, and generated API docs SHOULD follow suitable existing language/tool conventions; the agent SHOULD offer requester choices for new conventions materially affecting public documentation or maintenance. The [Diátaxis introduction](https://diataxis.fr/start-here/) explains the forms.
