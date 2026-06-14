# Using MLOps Agent Skills

Start every session with `skills/using-mlops-agent-skills/SKILL.md`.

## Install

```bash
scripts/install.sh --tool all --target .
```

## Workflow

1. Classify the request (validation, features, training, serving, monitoring, governance, zkML).
2. Load matching preset from `presets/`.
3. Load one execution skill — not the entire catalog.
4. Pick lifecycle command: `/spec` → `/plan` → `/build` → `/validate` → `/ship`.

## Validate

```bash
python scripts/validate-skills.py
python evals/run.py
pytest tests/ -q
```
