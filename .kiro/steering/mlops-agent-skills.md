---
inclusion: always
---

# MLOps Agent Skills Steering

## Entry Point

Load `skills/using-mlops-agent-skills/SKILL.md` at session start.

## Lifecycle Commands

| Command | Purpose |
|---------|---------|
| /spec | Contracts, schemas, SLAs |
| /plan | Task breakdown |
| /build | Incremental implementation |
| /validate | Tests, drift, fairness gates |
| /review | Reliability and governance |
| /retrain | Safe retraining |
| /ship | Deploy with rollback |

## Guardrails

- Classify work before coding
- Load platform preset from `presets/`
- Enforce PIT feature correctness and fairness/drift gates
- No placeholder implementations
- Prefer `references/` checklists during review

## Runnable Platform

Code modules at repo root: `data/`, `feature_store/`, `training/`, `serving/`, `monitoring/`, `zkml/`, `governance/`, `k8s/`, `tests/`.

## Validation

```bash
python scripts/validate-skills.py
python scripts/validate-assets.py
pytest tests/ -v
```
