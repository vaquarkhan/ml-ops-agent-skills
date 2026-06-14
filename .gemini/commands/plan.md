# MLOps lifecycle: break approved scope into atomic, verifiable tasks.

## Steps

1. Load the execution skill for the task domain.
2. Sequence: validation → features → training → registry → serving → monitoring → governance.
3. Identify dependencies (Feast materialization before training, etc.).
4. Assign verification command per task (`pytest`, `validate_k8s.py`, load test).

## Exit criteria

- Each task has acceptance criteria and a verification command
