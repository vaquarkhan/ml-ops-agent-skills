---
name: model-monitoring-and-drift-detection
description: Implements continuous drift monitoring with Evidently AI, PSI, and Wasserstein metrics. Use for comparing reference training data against production inference distributions.
---

# Model Monitoring and Drift Detection

## Overview

Compare reference (training) datasets against current production inference data using Evidently DataDriftPreset with PSI threshold alerts.

## When to Use

- building drift detection services
- configuring PSI and Wasserstein thresholds
- generating synthetic drifted data for tests
- wiring "Drift Detected" alerts into CI/CD

## Workflow

1. Implement monitoring in `monitoring/drift_service.py`.
2. Set `PSI_DRIFT_THRESHOLD` (default 0.2) via environment.
3. Compare reference vs current with `DriftDetectionService.detect_drift`.
4. Generate synthetic drift for tests with `generate_synthetic_drifted_data`.
5. Run tests: `pytest tests/test_monitoring.py -v`.

## Verification

- [ ] PSI computed per numeric column
- [ ] Wasserstein distance calculated for distribution shifts
- [ ] Drift alert triggers when PSI exceeds 0.2
- [ ] Evidently fallback to native PSI when library unavailable
