# Maintaining engineering documentation

## Identify what changed

Locate the [canonical owner](documentation.md#choosing-the-owner) and compare the old and new meaning. What would the reader now believe, do, or verify differently? A clearer sentence or a corrected destination can be an editorial repair. A change to an actor, obligation, condition, exception, interface, or expected result can alter meaning even if only one word changed. For a substantive change, establish its authority. Use the [cross-stage change guide](changing-the-contract.md#find-the-owner-and-the-decision) if the change affects what another stage relies on. If the owner is accurate and only a summary is misleading, correct the summary.

## Inspect the dependents that use the changed knowledge

Start with the changed identifier, heading, clause, or path. Look at the known direct dependents in scope, including a summary, example, instruction, or procedure that repeats an assumption without linking to it. Use the [kind of relationship](traceability.md#reading-a-reference) to decide what to compare.

| Why the dependent refers to the owner | What to check |
| --- | --- |
| Authority | Does the dependent still respect the accepted scope, conditions, exceptions, and decision status? If a decision has been replaced, retain its reasons, identify the successor and which provisions it supersedes, and direct current guidance to the applicable choice. |
| Traceability | Does the relationship still connect the right versions of intent, mechanism, instructions, evaluation expectation, or evidence? Inspect any affected interface, example, or claim. A wording edit cannot by itself authorize a new expected verdict. Use the [specification-to-evaluation dependencies](traceability.md#specification-to-evaluation-dependencies) when a contract clause changes. |
| Navigation | Does the label describe what the reader will find? Resolve the path and heading fragment from the referring file. Correct affected links, labels, and plain-text paths directly, including incoming references when a heading or file moves. |

Edit a dependent when its meaning, evidence qualification, or route has become stale. An inspected reference can remain correct. Continue beyond it only if something the next owner relies on has changed. For substantial rewrites, apply the [retention convention](documentation.md#retaining-decisions-and-current-knowledge). Report out-of-scope gaps separately. Review uses the existing decision authority and adds no central editorial approval. A local documentation change grants no authority for a search for unknown dependents, an audit, or a backfill.

## Verify the reader task

Start where the intended reader would start. Follow the affected path and see whether the reader can reach and use the answer, including its conditions and limits. Choose the check that exercises the purpose of the edit.

| If the reader needs to… | Try this check |
| --- | --- |
| Look up a fact or interface | Compare the reference with its authoritative source. Check inputs, outputs, strengths, exceptions, and status where relevant. A summary should lead to the maintained detail. |
| Carry out a procedure | Follow the steps from the stated prerequisites with the permissions the task allows. Can the maintainer make each choice and recognize completion? If only a walkthrough is possible, distinguish it from execution. |
| Learn by doing | Try the exercise from the learner's starting knowledge. Check that instructions introduce what each step needs and yield a recognizable result. |
| Understand a design or decision | Trace the explanation to the upstream intent, selected mechanism, and reasons. Can the reader explain why it applies here, where it stops applying, and where to find any decision that replaced it? |

Check affected links and anchors as well as the names a reader would copy or search for. Interpret consumer references at their [intended locations](architecture.md#staged-sources-and-release-relative-references). Where two accounts cover the same fact, verify that only one needs to maintain its definition.

Limit conclusions to the evidence the check supplies. Text comparison can establish agreement with a specification. Claims about agent behavior require observations of the identified candidate, evaluator correctness needs corresponding machinery checks, and causal claims need comparative evidence. See [what evidence can establish](traceability.md#what-evidence-can-establish).
