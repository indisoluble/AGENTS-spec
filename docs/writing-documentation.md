# Writing engineering documentation

## Start with the reader's missing knowledge

Name a task and the point where the reader would have to guess. A designer might know which outcome to support but lack the constraint that ruled out a mechanism. A reviewer might know which check passed but lack the observation needed to interpret it. Start at the responsible stage entry point listed in [`docs/architecture.md` § Stage interfaces](architecture.md#stage-interfaces) and try to find that answer.

If the existing material still lets that reader complete the task correctly, it needs no edit for this purpose. If the answer exists but readers miss it, improve the route or the wording. If knowledge is missing, write the smallest addition that lets the reader proceed correctly. A new rule, interface, assumption, risk, or operating procedure can justify an update. Keep task-specific notes in working records. Preserve a finding in engineering documentation when it changes what a future reader needs to know.

## Choose a form that fits the task

Ask whether the reader needs to **do** something or **understand** something, then whether they are learning a skill or putting it to use. Apply the same questions to an existing passage that feels hard to follow. This is the [Diátaxis compass](https://diataxis.fr/compass/).

| Reader's need | Form | What to write |
| --- | --- | --- |
| Act while learning a skill | Tutorial | Guide a newcomer through a manageable first task. Give them a result they can recognize at each important step. |
| Act using an existing skill | How-to guide | Start from the maintainer's situation. Give the steps and choices needed to reach the intended result. |
| Look up facts to apply a skill | Reference | Give precise definitions, inputs, outputs, conditions, or exceptions where the reader can find them individually. |
| Build understanding while learning | Explanation | Connect the parts a reader already recognizes. Explain why they interact as they do and which trade-offs follow. |

A reader changing a scenario may need a short explanation at a decision point in a how-to. Keep it there if the reasoning is essential to the next step. Link to a separate explanation when its depth would interrupt the task. Improve the passage at hand before considering a broader reorganization. [Diátaxis workflow](https://diataxis.fr/how-to-use-diataxis/)

## Select the architectural concerns that matter

For an architectural question, identify the component or system in scope. Use the [arc42 overview](https://arc42.org/overview/) to look for a concern whose omission could lead to a wrong design, use, or assessment.

| What could the reader misunderstand? | Concerns to examine |
| --- | --- |
| Whom the system serves, what it must achieve, or which option is feasible | Goals, quality requirements and scenarios, constraints, solution strategy, and consequential decisions |
| Who is responsible for a result or where information crosses a boundary | Context and scope, building blocks and their interfaces, shared concepts, and terminology |
| What happens during use or failure, or where the software runs | Runtime interactions and deployment conditions |
| What could fail or become costly to maintain | Evidenced risks, technical debt, and the limits of accepted trade-offs |

For example, a maintainer changing an evaluator component may need its responsibility and dependencies ([`05-evaluation/docs/framework-design.md` § Responsibilities and dependency direction](../05-evaluation/docs/framework-design.md#responsibilities-and-dependency-direction)) plus the order of interactions during a run. If the framework already describes the interaction, point there. If a component-specific exception changes the order, document it at its owner. A component with no distinct deployment conditions needs no deployment section of its own. If a relevant condition is unknown, keep the uncertainty visible. The arc42 guidance distinguishes [component structure](https://docs.arc42.org/section-5/) from [runtime interactions](https://docs.arc42.org/section-6/).

## Choose the document boundary

Use the ownership and rationale conventions ([`docs/documentation.md` § Choosing the owner](documentation.md#choosing-the-owner)) before choosing a filename.

- Extend the existing owner when the reader, task, and reasons to update the material coincide. Create a focused document when a distinct task has no suitable owner. Split a document when parts serve independent tasks or change for different reasons.
- If accurate material is hard to locate, add or improve a question or task link in the nearest README. An index can route different audiences to the same owner.
- If two passages independently define the same thing, keep the qualified definition with its owner and replace the other with a link or a reader-specific summary. Remove obsolete material after preserving its current knowledge and decision history ([`docs/documentation.md` § Retaining decisions and current knowledge](documentation.md#retaining-decisions-and-current-knowledge)).

Use verification appropriate to the document ([`docs/maintaining-documentation.md` § Verify the reader task](maintaining-documentation.md#verify-the-reader-task)) to judge whether the change resolves the original difficulty.

## When the repository leaves a question open

Use the primary practice that addresses the uncertainty. arc42 helps identify architectural content and Diátaxis helps shape it for a reader. For a lasting choice, consult the ADR convention and its source ([`docs/documentation.md` § Architecture, decisions, and guides](documentation.md#architecture-decisions-and-guides)). For intended behavior, use [Cucumber's BDD practices](https://cucumber.io/docs/bdd/) to explore examples, express agreed rules precisely, and guide automation. The project pipeline ([`docs/pipeline.md` § Test-first iteration](pipeline.md#test-first-iteration)) connects those activities to work on the contract. Discovery's current examples ([`01-discovery/deliverables/example-coverage.md` § Reading a proposed example](../01-discovery/deliverables/example-coverage.md#reading-a-proposed-example)) are proposals. Acceptance derives expectations from the accepted specification. Design explains the mechanism, Conformance defines complementary checks, Candidate instructs the agent, and Evaluation assesses observations from the identified Candidate.

AGENTS-spec combines these references for its own engineering work. Placement follows the stage interfaces, status follows decision authority ([`docs/authority.md` § Development decisions](authority.md#development-decisions)), and dependencies follow [`docs/traceability.md` § Reading a reference](traceability.md#reading-a-reference). If the relevant source leaves a question open, use applicable engineering practice and resolve the local choice within that authority. A genuine departure from BDD follows the existing departure guidance ([`docs/pipeline.md` § Unresolved methodological questions](pipeline.md#unresolved-methodological-questions)).
