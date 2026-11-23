# Maintaining engineering documentation

## Identify what changed

Locate the canonical owner ([`docs/documentation.md` § Choosing the owner](documentation.md#choosing-the-owner)) and compare the old and new meaning. What would the reader now believe, do, or verify differently? A clearer sentence or a corrected destination can be an editorial repair. A change to an actor, obligation, condition, exception, interface, or expected result can alter meaning even if only one word changed. For a substantive change, establish its authority. Use the cross-stage change guide ([`docs/changing-the-contract.md` § Find the owner and the decision](changing-the-contract.md#find-the-owner-and-the-decision)) if the change affects what another stage relies on. If the owner is accurate and only a summary is misleading, correct the summary.

## Inspect the dependents that use the changed knowledge

Start with the changed identifier, heading, clause, or path. Look at the known direct dependents in scope, including a summary, example, instruction, or procedure that repeats an assumption without linking to it. Use the kind of relationship ([`docs/traceability.md` § Reading a reference](traceability.md#reading-a-reference)) to decide what to compare.

| Why the dependent refers to the owner | What to check |
| --- | --- |
| Authority | Does the dependent still respect the accepted scope, conditions, exceptions, and decision status? If a decision has been replaced, retain its reasons, identify the successor and which provisions it supersedes, and direct current guidance to the applicable choice. |
| Traceability | Does the relationship still connect the right versions of intent, mechanism, instructions, evaluation expectation, or evidence? Inspect any affected interface, example, or claim. A wording edit cannot by itself authorize a new expected verdict. Use [`docs/traceability.md` § Specification-to-evaluation dependencies](traceability.md#specification-to-evaluation-dependencies) when a contract clause changes. |
| Navigation | Does the label follow the internal reference convention? Resolve the destination and heading fragment from the referring file and compare them with the displayed path and heading. Correct affected links, labels, and plain-text paths directly, including incoming references when a heading or file moves. |

Edit a dependent when its meaning, evidence qualification, or route has become stale. An inspected reference can remain correct. Continue beyond it only if something the next owner relies on has changed. For substantial rewrites, apply the retention convention ([`docs/documentation.md` § Retaining decisions and current knowledge](documentation.md#retaining-decisions-and-current-knowledge)). Report out-of-scope gaps separately. Review uses the existing decision authority and adds no central editorial approval. A local documentation change grants no authority for a search for unknown dependents, an audit, or a backfill.

## Verify the reader task

Start where the intended reader would start. Follow the affected path and see whether the reader can reach and use the answer, including its conditions and limits. Choose the check that exercises the purpose of the edit.

| If the reader needs to… | Try this check |
| --- | --- |
| Look up a fact or interface | Compare the reference with its authoritative source. Check inputs, outputs, strengths, exceptions, and status where relevant. A summary should lead to the maintained detail. |
| Carry out a procedure | Follow the steps from the stated prerequisites with the permissions the task allows. Can the maintainer make each choice and recognize completion? If only a walkthrough is possible, distinguish it from execution. |
| Learn by doing | Try the exercise from the learner's starting knowledge. Check that instructions introduce what each step needs and yield a recognizable result. |
| Understand a design or decision | Trace the explanation to the upstream intent, selected mechanism, and reasons. Can the reader explain why it applies here, where it stops applying, and where to find any decision that replaced it? |

Check affected links and anchors as well as the names a reader would copy or search for. Where two accounts cover the same fact, verify that only one needs to maintain its definition.

For a consumer link, first resolve the path and heading from the staged source. To check installation, copy the five files into an empty temporary directory using the installed paths ([`docs/architecture.md` § Staged sources and release-relative references](architecture.md#staged-sources-and-release-relative-references)). Keep their contents intact and follow the same reference from its installed file. For a failure, record the layout, referring file, literal target, and whether the path is missing, leaves the package, or reaches a file without the requested heading.

Limit conclusions to the evidence the check supplies. Text comparison can establish agreement with a specification. Claims about agent behavior require observations of the identified candidate, evaluator correctness needs corresponding machinery checks, and causal claims need comparative evidence. See [`docs/traceability.md` § What evidence can establish](traceability.md#what-evidence-can-establish).

## Check stage references

Resolve each changed local Markdown link from the referring file. Check that its destination is in the same stage, an earlier stage or shared foundational documentation. For consumer files, use the intended installation layout.

For link labels, use the convention in [`docs/documentation.md` § Internal references](documentation.md#internal-references). Also inspect written paths, clause numbers, instructions to consult another artifact, and links through shared pages. Try the maintenance task with just the current stage, earlier stages and shared definitions. Move a relationship needed only for cross-stage review to its dependent or the shared traceability indexes ([`docs/contract-traces.md`](contract-traces.md)). Validate changed link paths and fragments separately.
