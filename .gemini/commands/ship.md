# MLOps lifecycle: deploy with rollback path.

## Pre-ship

- Run `hooks/release-guard.sh`
- Confirm Model Card generated
- Confirm KServe manifest probes configured
- Tag MLflow artifact for target stage

## Post-ship

- Monitor drift service alerts for 24h
- Record release evidence in `templates/training-release-gate.yaml`
