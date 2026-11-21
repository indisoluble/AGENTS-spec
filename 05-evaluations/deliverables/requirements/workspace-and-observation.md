# Workspace preparation and observation

These requirements cover the workspace each case receives, the fixture mappings used to prepare it, and the filesystem state available for grading. The [observation boundaries](../../docs/framework-design.md#observation-and-capture-boundaries) explain what a snapshot records and which changes it can reveal.

These requirements govern evaluator behavior. The [product baseline](../../../02-formulation/deliverables/baseline.md) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E1

When a case starts, the suite shall provide a fresh temporary workspace containing that case's initial fixture and an unchanged copy of the current root contract.

**Checks.** [test_smoke.py](../tests/scenarios/test_smoke.py), [test_scope.py](../tests/scenarios/test_scope.py), [test_guidance.py](../tests/scenarios/test_guidance.py), live run

## E5

If a fixture is a symbolic link or non-regular file, then the suite shall avoid reading its contents, treating it as an execution error for smoke and using its observed entry type for behavioral-case assessment.

**Checks.** [test_evidence.py](../tests/runtime/test_evidence.py), [test_scope.py](../tests/scenarios/test_scope.py), [test_assumptions.py](../tests/scenarios/test_assumptions.py)

## E16

When capturing a workspace snapshot, the inspector shall record relative paths, entry types, POSIX permission and special mode bits, exact regular-file bytes, and symbolic-link targets, without following links or opening special-file contents.

**Checks.** [test_workspace.py](../tests/runtime/test_workspace.py)

## E17

If inspection of an existing workspace tree fails, then the inspector shall raise an inspection error instead of returning a partial snapshot.

**Checks.** [test_workspace.py](../tests/runtime/test_workspace.py)

## E19

When running a behavioral case, the suite shall capture initial state before execution and final state after process cleanup, retain available [snapshot manifests and fixture bytes](../../docs/running-and-reviewing.md#retained-evidence), and grade the captured observations.

**Checks.** [test_scope.py](../tests/scenarios/test_scope.py), [test_evidence.py](../tests/runtime/test_evidence.py), [test_cli.py](../tests/runtime/test_cli.py), live run

## E20

If a required workspace observation is missing or inspection fails, then the suite shall report an error rather than successful scope preservation, preserving any primary execution error and available evidence.

**Checks.** [test_scope.py](../tests/scenarios/test_scope.py), [test_evidence.py](../tests/runtime/test_evidence.py)

## E22

When given a fixture mapping, workspace preparation shall create exactly those regular files and their parent directories alongside the unchanged root contract, adding no default fixture when the mapping is empty. If a fixture path would escape the workspace or override the root contract, then workspace preparation shall reject it. When called without a fixture mapping, the smoke convenience helper shall supply the default `message.txt` fixture with the selected initial contents. When called with a fixture mapping, including an empty one, the smoke convenience helper shall use that mapping instead of the default.

**Checks.** [test_capture.py](../tests/runtime/test_capture.py), [test_smoke.py](../tests/scenarios/test_smoke.py)
