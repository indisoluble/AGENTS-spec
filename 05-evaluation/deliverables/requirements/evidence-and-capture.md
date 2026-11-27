# Evidence retention and capture

These requirements cover final-response capture, assertion results and reasons, workspace differences, and retention when evidence writes fail. The retained evidence guide ([`05-evaluation/docs/running-and-reviewing.md` § Retained evidence](../../docs/running-and-reviewing.md#retained-evidence)) identifies the artifacts available for review.

These requirements govern evaluator behavior. The product baseline ([`02.0-formulation/deliverables/baseline.md`](../../../02.0-formulation/deliverables/baseline.md)) owns AGENTS-spec product requirements. Checks identify verification methods. Evidence of agent compliance depends on what an individual run and its assessment establish.

## E8

When execution ends, the suite shall attempt to retain the listed evidence ([`05-evaluation/docs/running-and-reviewing.md` § Retained evidence](../../docs/running-and-reviewing.md#retained-evidence)) outside the temporary workspace.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/runtime/test_codex.py`](../evaluation/tests/runtime/test_codex.py), [`engine/tests/runtime/test_codex.py`](../../../engine/tests/runtime/test_codex.py), live run

## E21

When reporting behavioral assertions, the suite shall retain boolean assertion values and Pydantic Evals assertion reasons separately in JSON and show specific violations in the terminal report.

**Checks.** [`05-evaluation/deliverables/evaluation/tests/scenarios/test_scope.py`](../evaluation/tests/scenarios/test_scope.py), [`03.1-conformance/deliverables/conformance/tests/test_scope.py`](../../../03.1-conformance/deliverables/conformance/tests/test_scope.py), [`05-evaluation/deliverables/evaluation/tests/scenarios/test_permissions.py`](../evaluation/tests/scenarios/test_permissions.py), [`03.1-conformance/deliverables/conformance/tests/test_permissions.py`](../../../03.1-conformance/deliverables/conformance/tests/test_permissions.py)
