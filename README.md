# AGENTS-spec

AGENTS-spec develops a reusable operating contract for collaboration with coding agents. To install or use it in your project, start with the consumer adoption guide in [`04-candidate/pre_README.md`](04-candidate/pre_README.md).

## Development pipeline

Read the stages in numerical order for an overview. For a specific edit, the change guide ([`docs/changing-the-contract.md` § Find the owner and the decision](docs/changing-the-contract.md#find-the-owner-and-the-decision)) identifies where to start, who can authorize it and what to verify.

| Stage | What it owns |
| --- | --- |
| [`01-discovery/README.md`](01-discovery/README.md) | Product objectives and their rationale, proposed examples and questions for the requester. |
| [`02-formulation/README.md`](02-formulation/README.md) | Accepted requirements, their conditions and constraints, and any expressly accepted defining examples. |
| [`03-design/README.md`](03-design/README.md) | The selected mechanisms for meeting the requirements and the reasons for choosing them. The shared clause index ([`docs/contract-traces.md` § Contract clause index](docs/contract-traces.md#contract-clause-index)) maps these choices to the instructions. |
| [`04-candidate/`](04-candidate/) | The five staged consumer files. For an instruction edit, start with [`docs/changing-the-contract.md` § Clarify Candidate wording](docs/changing-the-contract.md#clarify-candidate-wording). For a bridge or guide, check the installed paths ([`docs/architecture.md` § Staged sources and release-relative references](docs/architecture.md#staged-sources-and-release-relative-references)). |
| [`05-evaluations/README.md`](05-evaluations/README.md) | Case definitions, executable checks and evidence about what happened with an identified Candidate. |

The stages implement three behavior-driven development (BDD) practices. Discovery explores intent, Formulation records agreement, and Design, Candidate and Evaluations share Automation. For a requirements-led change, an evaluation expectation derived from accepted intent guides implementation. A feasibility finding or an unexpected result can reopen an earlier question. [`docs/architecture.md` § Stage interfaces](docs/architecture.md#stage-interfaces) · [`docs/pipeline.md` § Test-first iteration](docs/pipeline.md#test-first-iteration) · [`docs/README.md`](docs/README.md)

The established objectives put **O1 (control token consumption)** ahead of **O2 (requester awareness and consequential control)**. See [`01-discovery/deliverables/objectives-and-rationale.md` § Established objectives](01-discovery/deliverables/objectives-and-rationale.md#established-objectives). Durable project knowledge supports both. Evidence of savings or compliance requires separate assessment.
