# MLOps Agent Skills Index

Grouped catalog of workflow skills in this repository.

## Start Here

| Skill | Description |
|-------|-------------|
| [using-mlops-agent-skills](skills/using-mlops-agent-skills/SKILL.md) | Classify work, choose preset, pick next command |

## Data & Features

| Skill | Description |
|-------|-------------|
| [data-validation-and-contract-testing](skills/data-validation-and-contract-testing/SKILL.md) | Great Expectations + dbt upstream validation |
| [feast-feature-store-engineering](skills/feast-feature-store-engineering/SKILL.md) | Feast offline/online, PIT joins |

## Training & Registry

| Skill | Description |
|-------|-------------|
| [distributed-gpu-training-and-scheduling](skills/distributed-gpu-training-and-scheduling/SKILL.md) | Volcano gang scheduling, fractional GPU |
| [mlflow-model-registry-and-continuous-training](skills/mlflow-model-registry-and-continuous-training/SKILL.md) | PyTorch CT + MLflow Unity Catalog |

## Serving & Monitoring

| Skill | Description |
|-------|-------------|
| [llm-serving-and-inference-optimization](skills/llm-serving-and-inference-optimization/SKILL.md) | KServe + vLLM + LMCache |
| [model-monitoring-and-drift-detection](skills/model-monitoring-and-drift-detection/SKILL.md) | Evidently PSI/Wasserstein drift |

## Trust & Governance

| Skill | Description |
|-------|-------------|
| [verifiable-ai-and-zkml](skills/verifiable-ai-and-zkml/SKILL.md) | EZKL zero-knowledge proofs |
| [responsible-ai-and-model-governance](skills/responsible-ai-and-model-governance/SKILL.md) | Fairlearn + Model Cards |

## Platform Presets

| Preset | Stack |
|--------|-------|
| [kubernetes-gpu-mlops](presets/kubernetes-gpu-mlops.yaml) | K8s, Volcano, KServe, Feast |
| [databricks-unity-catalog-mlops](presets/databricks-unity-catalog-mlops.yaml) | Databricks UC, MLflow, Feast |
| [aws-sagemaker-mlops](presets/aws-sagemaker-mlops.yaml) | SageMaker, S3, GX |
| [gcp-vertex-mlops](presets/gcp-vertex-mlops.yaml) | Vertex AI, BigQuery, Feast |

## By Lifecycle Command

| Command | Primary Skills |
|---------|----------------|
| `/spec` | using-mlops-agent-skills, data-validation-and-contract-testing |
| `/plan` | using-mlops-agent-skills + task-specific skill |
| `/build` | All implementation skills |
| `/validate` | data-validation, monitoring, governance, tests/ |
| `/review` | governance, monitoring, serving |
| `/retrain` | feast-feature-store, mlflow-model-registry, distributed-gpu |
| `/ship` | llm-serving, distributed-gpu, governance |
