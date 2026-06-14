# MLOps lifecycle: define model contract, feature schema, SLA, and lineage.

Load `skills/using-mlops-agent-skills/SKILL.md` and the task-specific skill after triage.

## Steps

1. Identify model type (batch classifier, LLM, zkML-verified model).
2. Draft contract using `templates/model-contract.yaml`.
3. Define upstream data contract in `data/dbt/models/schema.yml`.
4. Document fairness and drift thresholds.
5. Output `/plan` task breakdown — do not implement yet.

## Exit criteria

- Named owner, SLA, and rollback path documented
- Feature schema and label definition unambiguous
