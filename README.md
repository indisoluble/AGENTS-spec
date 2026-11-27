# AGENTS-spec

AGENTS-spec develops a reusable `AGENTS.md` file that tells coding agents how to work with the people requesting changes.

Suppose an agent pauses to ask a question when the requester expected it to keep working. Before rewriting the instruction, a contributor can use the pipeline to compare what people wanted, what the instruction said, and what the agent actually did.

## Development pipeline

The structural migration introduces seven stages. The sequence below describes engineering activities that can overlap or reopen. Authoritative requirements come from Formulation and mechanism prescriptions from Design.

1. Discovery explores needs and proposals.
2. Formulation records accepted intent and constraints.
3. [Acceptance](02.1-acceptance/README.md) defines how to assess accepted intent.
4. Design selects mechanisms.
5. [Conformance](03.1-conformance/README.md) defines complementary mechanism checks.
6. Candidate supplies the consumer artifacts.
7. [Evaluation](05-evaluation/README.md) executes the integrated suite and assesses evidence.

This project's BDD adaptation maps Discovery and Formulation to the first two activities and Automation to the remaining five. Shared methodology and the overview diagram await the documentation alignment increment. The [migration record](docs/migration-inventory.md) identifies the earlier allocation and preserved rationale.

Today's behavioral cases exercise selected Candidate clauses. The suite has no acceptance check derived directly from a Formulation requirement. [`05-evaluation/docs/maintaining-evaluations.md` § Establish the expectation](05-evaluation/docs/maintaining-evaluations.md#establish-the-expectation) · [`05-evaluation/docs/evaluation-model.md` § Purpose and evaluation model](05-evaluation/docs/evaluation-model.md#purpose-and-evaluation-model)

## Where to start

| What are you looking for? | Where to start |
| --- | --- |
| The need behind a proposal | [`01-discovery/README.md`](01-discovery/README.md) · [`01-discovery/deliverables/objectives-and-rationale.md` § Established objectives](01-discovery/deliverables/objectives-and-rationale.md#established-objectives) |
| The behavior people agreed on | [`02.0-formulation/README.md`](02.0-formulation/README.md) |
| The reason for a design choice | [`03.0-design/README.md`](03.0-design/README.md) |
| An instruction and the decisions behind it | [`04-candidate/pre_AGENTS.md`](04-candidate/pre_AGENTS.md) · [`docs/contract-traces.md` § Contract clause index](docs/contract-traces.md#contract-clause-index) |
| How to use the instructions in your project | [`04-candidate/pre_README.md`](04-candidate/pre_README.md) |
| The companion files and where to install them | [`04-candidate/`](04-candidate) · [`docs/architecture.md` § Staged sources and release-relative references](docs/architecture.md#staged-sources-and-release-relative-references) |
| What the checks cover and where the gaps are | [`05-evaluation/README.md`](05-evaluation/README.md) · [`docs/traceability.md` § Current traceability gaps](docs/traceability.md#current-traceability-gaps) |
| How the stages fit together and where to find shared guidance | [`docs/architecture.md` § Stage interfaces](docs/architecture.md#stage-interfaces) · [`docs/README.md`](docs/README.md) |
| How to clarify an instruction while keeping its meaning | [`docs/changing-the-contract.md` § Clarify Candidate wording](docs/changing-the-contract.md#clarify-candidate-wording) |
| Who can authorize a change to the expected behavior | [`docs/changing-the-contract.md` § Find the owner and the decision](docs/changing-the-contract.md#find-the-owner-and-the-decision) |
