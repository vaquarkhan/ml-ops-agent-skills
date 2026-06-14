---
name: mlflow-model-registry-and-continuous-training
description: Implements PyTorch continuous training with MLflow autolog and Databricks Unity Catalog registration. Use for training loops, experiment tracking, and staging model artifacts.
---

# MLflow Model Registry and Continuous Training

## Overview

Pull point-in-time features from Feast, train PyTorch models, autolog metrics via MLflow, and register artifacts to Unity Catalog.

## When to Use

- building or modifying the training loop
- integrating MLflow tracking and registry URIs
- registering models to Databricks Unity Catalog
- testing that metrics, hyperparameters, and weights are logged

## Workflow

1. Configure `TrainingConfig` in `training/train.py` (registry URI, UC model name).
2. Pull features via `build_training_dataset` before training.
3. Enable `mlflow.pytorch.autolog()` and register with `databricks-uc` backend.
4. Tag artifacts for staging (`stage=staging`).
5. Run tests: `pytest tests/test_training.py -v`.

## Verification

- [ ] Training pulls from Feast with PIT correctness
- [ ] MLflow logs metrics, params, and model weights
- [ ] Artifact registered to Unity Catalog model name
- [ ] Staging tag applied to registered model
