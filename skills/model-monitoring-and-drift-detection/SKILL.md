---
name: model-monitoring-and-drift-detection
description: Implements continuous drift monitoring with Evidently AI, PSI, and Wasserstein metrics. Use when comparing reference training data against production inference distributions or wiring drift alerts into CI/CD gates.
---

# Model Monitoring and Drift Detection

## Overview

Compare reference (training) datasets against current production inference data using Evidently `DataDriftPreset` with **Population Stability Index (PSI)** and **Wasserstein distance**, triggering `Drift Detected` alerts when PSI exceeds configurable thresholds (default 0.2).

## When to Use

- building continuous monitoring services
- configuring PSI and Wasserstein thresholds per feature
- generating synthetic drifted data for test coverage
- wiring drift alerts into CI/CD promotion gates
- investigating model quality degradation in production
- comparing pre/post retrain distributions

## Decision Framework

| Metric | Use |
|--------|-----|
| PSI | Primary gate — threshold default 0.2 |
| Wasserstein | Secondary distribution distance signal |
| Evidently | Preferred when importable; PSI fallback always available |
| Reference window | Frozen training snapshot — never rolling production |
| Alert | `DriftReport.drift_detected == True` blocks promotion |

## Workflow

1. Implement service in `monitoring/drift_service.py` with lazy Evidently import.
2. Set `PSI_DRIFT_THRESHOLD` via environment (default 0.2).
3. Run `DriftDetectionService.detect_drift(reference, current)`.
4. Extract per-column PSI via `_extract_psi` with fallback computation.
5. Generate synthetic drift: `generate_synthetic_drifted_data(reference, drift_magnitude=5.0)`.
6. Assert drift alert in tests when PSI > 0.2: `pytest tests/test_monitoring.py -v`.
7. Integrate into `/validate` and release gate template.

## Anti-Patterns

- Using production data as reference baseline
- Alerting on mean shift only without PSI
- Ignoring drift on low-cardinality features
- No synthetic drift tests in CI
- Silent fallback without logging when Evidently unavailable

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "Accuracy hasn't dropped yet." | Drift precedes accuracy collapse — detect early. |
| "PSI 0.2 is arbitrary." | Calibrate per feature; document threshold in Model Card. |
| "We check dashboards manually." | Automated gate prevents silent promotion during drift. |
| "One feature drifted — ship anyway." | Any column over threshold triggers alert by design. |

## Red Flags

- no reference dataset versioning
- drift service never run in CI
- PSI threshold undocumented
- production monitoring disconnected from training window
- agent dismisses drift without retrain plan

## Verification

- [ ] PSI computed per numeric column
- [ ] Wasserstein distance calculated for distribution shifts
- [ ] `drift_detected=True` when synthetic shift PSI > 0.2
- [ ] Evidently lazy import with PSI fallback logged
- [ ] `pytest tests/test_monitoring.py` passes
- [ ] Checklist: `references/drift-detection-checklist.md` complete

## Implementation References

- Service: `monitoring/drift_service.py`
- Tests: `tests/test_monitoring.py`
- Starter: `starter-packs/drift-monitoring-starter.yaml`

## Related Skills

- Pairs with: `responsible-ai-and-model-governance`
- See: `starter-packs/drift-monitoring-starter.yaml`
