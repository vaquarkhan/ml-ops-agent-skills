# MLOps lifecycle: prove quality before promotion.

## Required checks

```bash
python scripts/validate-skills.py
python scripts/validate-assets.py
pytest tests/ -v
python training/validate_k8s.py
```

## Gates

- Drift PSI threshold (default 0.2)
- Fairness demographic parity (default 0.05)
- Serving p95 latency threshold

Do not promote if any gate fails.
