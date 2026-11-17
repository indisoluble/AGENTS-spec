# Local coding-agent evaluations

This document explains what the suite assesses and what its evidence can establish. Use the [stage README](../README.md) for routes to case definitions, operations, and framework maintenance.

## Purpose and evaluation model

The suite examines coding-agent behavior in small, controlled situations drawn from [AGENTS.md](../../03-contract/prerelease_AGENTS.md). The contract prioritizes token control through bounded, proportionate work, then informed requester control of consequential direction, supported by durable project knowledge. Every case receives a fresh temporary workspace with its fixture and an unchanged copy of `03-contract/prerelease_AGENTS.md` as workspace-root `AGENTS.md`. Ten cases are registered: the smoke case checks the infrastructure; the nine behavioral cases exercise specific contract decisions rather than general compliance.

A run connects four responsibilities:

1. **Execution:** Codex receives the case's task and works in the disposable fixture.
2. **Observation:** the launcher retains execution evidence and, for behavioral cases, initial/final workspace state. Cases requiring human review also capture the final response.
3. **Automated assessment:** Pydantic Evals applies the case's assertions to the observed result. Independent-execution and contract-change-followthrough first run their evaluator-owned functional checks after agent cleanup and before workspace removal.
4. **Human assessment:** a reviewer uses the retained rubric, messages, commands, and workspace evidence to assess criteria automation cannot establish.

An agent's completion claim is not proof of success. Automated assertions, infrastructure health, task completion, and human judgments answer different questions; [results](running-and-reviewing.md#results-evidence-and-failure-investigation) explains how they are reported. A successful observed behavior does not establish that AGENTS.md caused it. Causal attribution requires comparative evidence.

The [catalogue](../deliverables/cases-and-requirements.md#cases-and-interpretation) describes designed coverage and its limits. A case deliberately presents a condition and defines its assessment; this does not mean an agent has passed. Executed evidence requires a run, reviewed results require assessment, and broader confidence requires repeated, varied evidence. There are no dedicated scenarios for initial planning communication, cumulative reassessment, requester limits across increments, consequential architectural consultation, or handoff/resumption continuity. Conditional rubric criteria do not ensure those situations occur; the [bounded-inquiry interpretation](../deliverables/cases-and-requirements.md#bounded-inquiry) also identifies notification and retry coverage limits. Full PDSA assessment, containers, and CI remain deferred. The CLI does not collect human verdicts or resume an agent with an answer.

The [product baseline](../../01-behavior/deliverables/baseline.md) records accepted intent. The [60 behavioral examples](../../01-behavior/deliverables/discovery.md#proposed-example-suites) remain proposed, and [E1–E40](../deliverables/cases-and-requirements.md#verifiable-requirements) specify evaluator behavior. The cases exercise contract clauses. Requirements-derived acceptance tests would need independently established expectations and traceability to accepted intent. Complete BR1–BR10 coverage has not been established. Results provide evidence for human review. Authority to change intent, design, or evaluation criteria follows the [cross-domain traceability and feedback model](../../docs/authority-and-change.md#cross-domain-traceability-and-feedback).
