# MLOps Agent Skills — Copilot Instructions

Follow the agent skill workflows in this repository.

## Start Here

1. Read `skills/using-mlops-agent-skills/SKILL.md`
2. Load the matching preset from `presets/`
3. Load task-specific skills only when needed

## Lifecycle

- `/spec` — contracts, schemas, SLAs
- `/validate` — pytest, drift, fairness gates
- `/ship` — serving manifests with rollback

## Platform Code

Runnable modules: `data/`, `feature_store/`, `training/`, `serving/`, `monitoring/`, `zkml/`, `governance/`, `k8s/`, `tests/`.

See `AGENTS.md` and `skills-index.md` for full routing.
