# Drift Detection Checklist

Use when configuring production drift monitoring, PSI alerts, and retraining triggers.

> **Provenance:** Evidently AI drift detection guides; PSI threshold literature (credit scoring); Wasserstein distance monitoring patterns.

- [ ] Reference dataset frozen from training window
- [ ] Production sample collected from inference logs
- [ ] PSI threshold configured (default 0.2)
- [ ] Wasserstein distance computed per numeric column
- [ ] Alert fires when any column PSI exceeds threshold
- [ ] Synthetic drift tests pass in CI
- [ ] Runbook linked for drift incidents

## Sources

| Source | URL | Last reviewed |
|--------|-----|---------------|
| Evidently AI — Data drift | https://docs.evidentlyai.com/metrics/explainer_drift | 2026-06-14 |
| Evidently AI — PSI metric | https://docs.evidentlyai.com/metrics/customize_metric | 2026-06-14 |
| Basel Committee — Model risk (PSI thresholds in credit) | https://www.bis.org/basel_framework | 2026-06-14 |
| SciPy — Wasserstein distance | https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wasserstein_distance.html | 2026-06-14 |
| Runnable reference | `monitoring/drift_service.py` | 2026-06-14 |
