# MLOps Agent Entry Point

Use this file as the generic entry point for agents that support `AGENTS.md`-style repository instructions.

## Start Here

1. Load `skills/using-mlops-agent-skills/SKILL.md`
2. Load the platform preset from `presets/` that matches the environment
3. Load only the workflow skills needed for the current task
4. Pull in references, templates, and examples only when they improve decisions or proof

## Lifecycle Commands

- `/spec` → define model contract, feature schema, SLA, lineage, ownership
- `/plan` → break ML platform changes into atomic tasks
- `/build` → implement pipeline, model, feature, or serving changes incrementally
- `/validate` → prove data quality, drift checks, fairness gates, and test coverage
- `/review` → review reliability, cost, governance, and operability
- `/retrain` → run safe retraining and feature backfill workflows
- `/ship` → deploy, observe, rollback-safe release

## Default Routing

- unclear request → classify via `using-mlops-agent-skills`
- upstream data validation → `data-validation-and-contract-testing`
- feature store work → `feast-feature-store-engineering`
- GPU K8s training → `distributed-gpu-training-and-scheduling`
- MLflow / Unity Catalog → `mlflow-model-registry-and-continuous-training`
- LLM serving → `llm-serving-and-inference-optimization`
- drift monitoring → `model-monitoring-and-drift-detection`
- zkML proofs → `verifiable-ai-and-zkml`
- fairness / Model Cards → `responsible-ai-and-model-governance`

## Runnable Platform Code

This repository includes a full implementation at the repository root:

| Module | Path |
|--------|------|
| Data validation | `data/` |
| Feature store | `feature_store/` |
| Training | `training/` |
| Serving | `serving/` |
| Monitoring | `monitoring/` |
| zkML | `zkml/` |
| Governance | `governance/` |
| Kubernetes | `k8s/` |
| Tests | `tests/` |

## Guardrails

- prefer specification before implementation
- do not skip point-in-time feature correctness
- treat drift, fairness, and serving latency as release gates
- prefer a small set of active skills over loading the whole repository
- run hooks from `hooks/` before risky operations when possible

## High-Value References

- `skills-index.md`
- `registry/assets.json`
- `references/feast-pit-join-checklist.md`
- `references/volcano-gang-scheduling-checklist.md`
- `references/llm-serving-latency-checklist.md`
- `references/drift-detection-checklist.md`
- `references/fairness-gate-checklist.md`
- `examples/README.md`
- `tutorials/installing-vscode-and-jetbrains-plugins.md`
