# Drift Detection Checklist

> **Provenance:** Evidently AI drift detection guides; PSI threshold literature (credit scoring); Wasserstein distance monitoring patterns.

- [ ] Reference dataset frozen from training window
- [ ] Production sample collected from inference logs
- [ ] PSI threshold configured (default 0.2)
- [ ] Wasserstein distance computed per numeric column
- [ ] Alert fires when any column PSI exceeds threshold
- [ ] Synthetic drift tests pass in CI
- [ ] Runbook linked for drift incidents
