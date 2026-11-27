# Evaluation engine

The engine wraps Pydantic Evals for coding-agent trials with a contract supplied by its caller. It creates disposable workspaces, launches and cleans up processes, captures observations and evidence, and runs evaluator-owned functional checks. The caller supplies the dataset, fixtures, optional checks and execution configuration. The [interfaces and execution boundaries](docs/framework-design.md) describe the results a caller can interpret. The [maintenance guide](docs/maintaining-engine.md) covers changes to shared behavior.

Use Python 3.11 or newer on POSIX. From the directory containing this package, with the intended Python environment active, run:

```sh
python -m pip install -r engine/requirements.txt
python -m unittest discover -s engine/tests -t . -v
python -m engine.tests.offline_smoke
```

The [standalone smoke](cases/smoke.md) uses synthetic contract bytes and a test-authored edit. Engine verification requires no product checkout or authenticated agent. The optional [functional sandbox probe](docs/framework-design.md#functional-check-execution) separately exercises an installed Codex sandbox. Engine requirements cover [agent execution](requirements/agent-execution.md), [workspaces](requirements/workspace-and-observation.md), [evidence](requirements/evidence-and-capture.md), [functional checks](requirements/functional-checks.md) and [smoke grading](cases/smoke.md#e2).
