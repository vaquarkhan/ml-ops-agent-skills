---
name: mlflow-model-registry-and-continuous-training
description: Implements PyTorch continuous training with MLflow autolog and Databricks Unity Catalog registration. Use when building training loops, experiment tracking, or registering staging model artifacts to Unity Catalog.
---

# MLflow Model Registry and Continuous Training

## Overview

Pull point-in-time features from Feast, train PyTorch classifiers, autolog metrics and artifacts via MLflow, and register models to **Databricks Unity Catalog** using the `databricks-uc` registry URI with explicit staging tags.

## When to Use

- building or modifying the continuous training loop
- integrating MLflow tracking and Unity Catalog registry URIs
- registering models with staging/production stage tags
- verifying metrics, hyperparameters, and weights are logged
- designing automated retraining pipelines
- connecting Feast features to PyTorch DataLoaders

## Decision Framework

| Decision | Recommendation |
|----------|----------------|
| Registry backend | `DATABRICKS_UC_REGISTRY_URI=databricks-uc` |
| Model naming | `UC_MODEL_NAME=main.mlops.user_classifier` |
| Feature source | Always `build_training_dataset` (PIT correct) |
| Autolog | `mlflow.pytorch.autolog(log_models=True)` |
| Local without MLflow server | Mock MLflow in tests; use tracking URI in prod |

## Workflow

1. Configure `TrainingConfig` in `training/train.py` (registry URI, UC model name, hyperparams).
2. **Prepare data** via `build_training_dataset(entity_df)` — never bypass PIT retrieval.
3. **Train** with `TrainingPipeline.train()` — BCELoss, Adam, dropout for regularization.
4. **Log** with `mlflow.start_run()` — params, metrics, `stage=staging` tag.
5. **Register** via `mlflow.pytorch.log_model(registered_model_name=...)`.
6. Test with mocked MLflow: `pytest tests/test_training.py -v` (requires torch).

## Anti-Patterns

- Training on latest features without timestamps (leakage)
- Manual weight saving without MLflow lineage
- Registering to local filesystem registry in production
- Skipping validation split metrics before registration
- Hardcoding model paths instead of UC registered name

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "We only need the .pt file." | Registry lineage is required for audit, rollback, and governance. |
| "Autolog is too verbose." | Selective logging is fine; core metrics and params are mandatory. |
| "Unity Catalog is optional." | Preset `databricks-unity-catalog-mlops` assumes UC as source of truth. |
| "Training loss looked good." | Validation metrics and fairness gates determine promotion. |

## Red Flags

- no MLflow run_id after training
- missing `stage` tag on registered artifact
- features pulled without Feast PIT join
- training script runs but nothing registered
- agent promotes model without `/validate` gate

## Verification

- [ ] Training pulls from Feast with PIT correctness
- [ ] MLflow logs params, metrics, and model artifacts
- [ ] Artifact registered to Unity Catalog model name
- [ ] Staging tag applied (`stage=staging`)
- [ ] `pytest tests/test_training.py` passes when torch available
- [ ] Release gate template filled: `templates/training-release-gate.yaml`

## Implementation References

- Training: `training/train.py`
- Preset: `presets/databricks-unity-catalog-mlops.yaml`
- Skill dependency: `feast-feature-store-engineering`

## Related Skills

- Requires: `feast-feature-store-engineering`
- Pairs with: `responsible-ai-and-model-governance`
