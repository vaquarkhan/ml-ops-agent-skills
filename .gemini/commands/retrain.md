# MLOps lifecycle: safe retrain and feature backfill.

## Guardrails

- Run `hooks/retrain-guard.sh` before retraining
- Verify point-in-time feature correctness after backfill
- Compare drift metrics pre/post retrain
- Register new MLflow run; do not overwrite production alias without review

## Skills

- `feast-feature-store-engineering`
- `mlflow-model-registry-and-continuous-training`
