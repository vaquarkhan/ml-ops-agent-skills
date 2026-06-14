# MLflow Unity Catalog Registration

## Goal

Register PyTorch models to Unity Catalog with staging tags.

## Steps

1. Set `DATABRICKS_UC_REGISTRY_URI=databricks-uc`.
2. Run `TrainingPipeline.run(entity_df)`.
3. Verify MLflow tags include `stage=staging`.

Skill: `skills/mlflow-model-registry-and-continuous-training/SKILL.md`
