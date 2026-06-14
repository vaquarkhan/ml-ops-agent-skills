---
name: responsible-ai-and-model-governance
description: Implements Fairlearn fairness metrics, automated Model Cards, and CI/CD gates for demographic parity. Use for governance reviews before model promotion.
---

# Responsible AI and Model Governance

## Overview

Calculate Demographic Parity and Equalized Odds with Fairlearn, generate Model Cards in markdown, and fail CI when fairness thresholds are exceeded.

## When to Use

- evaluating model fairness across sensitive cohorts
- generating Model Cards with lineage and intended use
- implementing CI gates for demographic parity (default 0.05 margin)
- blocking promotion when governance checks fail

## Workflow

1. Compute metrics in `governance/fairness.py` via `GovernancePipeline`.
2. Enforce gate with `enforce_fairness_gate` — raises `FairnessGateError` on breach.
3. Generate Model Card markdown with `generate_model_card`.
4. Run tests: `pytest tests/test_governance.py -v`.

## Verification

- [ ] Demographic parity difference computed per sensitive feature
- [ ] Equalized odds difference logged
- [ ] Model Card includes metrics, lineage, and intended use
- [ ] CI test fails when DP difference exceeds 0.05
