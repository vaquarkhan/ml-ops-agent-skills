---
name: responsible-ai-and-model-governance
description: Implements Fairlearn fairness metrics, automated Model Cards, and CI/CD gates for demographic parity. Use when evaluating fairness across sensitive cohorts, generating Model Cards, or blocking promotion when parity thresholds are exceeded.
---

# Responsible AI and Model Governance

## Overview

Calculate **Demographic Parity Difference** and **Equalized Odds Difference** with Fairlearn, auto-generate **Model Cards** in markdown summarizing metrics, lineage, and intended use, and **fail CI** when demographic parity exceeds the configured margin (default 0.05).

## When to Use

- evaluating model fairness across sensitive attributes (gender, age cohort, region)
- generating Model Cards before staging/production promotion
- implementing CI gates that block biased models
- documenting intended use, limitations, and training lineage
- responding to governance or compliance review requests
- pairing with drift monitoring for holistic model health

## Decision Framework

| Metric | Gate |
|--------|------|
| Demographic parity diff | Must be ≤ 0.05 (configurable `FAIRNESS_DP_THRESHOLD`) |
| Equalized odds diff | Logged; document in Model Card |
| Sensitive feature | Must be named and monitored |
| Model Card | Required before `/ship` |
| Failure action | Raise `FairnessGateError` — pipeline stops |

## Workflow

1. Compute metrics: `GovernancePipeline.compute_fairness_metrics(y_true, y_pred, sensitive)`.
2. Evaluate gate: `metrics.evaluate_gate()` — sets `passed` boolean.
3. Enforce in CI: `enforce_fairness_gate(metrics)` raises on breach.
4. Generate Model Card: `generate_model_card(model_name, version, metrics)`.
5. Verify markdown includes DP/EO tables, lineage, intended use, gate status.
6. Test biased dataset fails gate: `pytest tests/test_governance.py -v`.

## Anti-Patterns

- Reporting accuracy only without cohort breakdown
- Model Card as afterthought post-deployment
- Moving fairness threshold after seeing results
- Using proxy features to encode sensitive attributes unnoticed
- Skipping governance for "internal only" models

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "Dataset is balanced." | Production cohorts drift; measure parity on predictions. |
| "0.05 threshold is too strict." | Document approved threshold; do not silently widen. |
| "Model Card is paperwork." | Model Card is the audit artifact regulators expect. |
| "Fairness slows delivery." | Fairness gate is cheaper than post-hoc remediation. |

## Red Flags

- no sensitive feature documented
- Model Card missing intended use section
- CI passes with intentionally biased test data
- demographic parity not logged to MLflow
- agent bypasses `FairnessGateError` to force ship

## Verification

- [ ] Demographic parity difference computed via Fairlearn
- [ ] Equalized odds difference logged in Model Card
- [ ] CI test fails when DP diff > 0.05 (`test_fairness_gate_fails_on_bias`)
- [ ] Model Card markdown generated with metrics and lineage
- [ ] Gate status (PASSED/FAILED) visible in Model Card
- [ ] Checklist: `references/fairness-gate-checklist.md` complete

## Implementation References

- Pipeline: `governance/fairness.py`
- Tests: `tests/test_governance.py`
- Starter: `starter-packs/responsible-ai-starter.yaml`

## Related Skills

- Pairs with: `model-monitoring-and-drift-detection`
- See: `starter-packs/responsible-ai-starter.yaml`
