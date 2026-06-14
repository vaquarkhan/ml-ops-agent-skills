# Drift Detection Production Gates

## Goal

Block promotion when PSI exceeds 0.2.

## Steps

1. Configure `PSI_DRIFT_THRESHOLD=0.2`.
2. Run `DriftDetectionService.detect_drift(ref, current)`.
3. Assert `drift_detected` in CI: `pytest tests/test_monitoring.py`.

Skill: `skills/model-monitoring-and-drift-detection/SKILL.md`
