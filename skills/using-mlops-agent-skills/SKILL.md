---
name: using-mlops-agent-skills
description: Helps agents classify MLOps work, choose the right preset and skill bundle, and pick the safest next command. Use when starting a session, triaging an ambiguous ML platform request, or deciding how to proceed.
---

# Using MLOps Agent Skills

## Overview

Start here before changing training code, feature definitions, serving manifests, monitoring pipelines, or governance gates. This skill maps the user request to the right MLOps workflow so the agent does not skip validation, point-in-time correctness, reproducibility, or release proof.

## When to Use

- starting a new MLOps session
- deciding which skill should lead execution
- translating a vague request into the right workflow
- choosing the best preset, starter pack, or runnable example
- deciding the safest next command

Do not stop here once the task has been classified. Load the actual execution skill after triage.

## Workflow

1. Classify the task type.
   - Raw data ingestion or schema drift: use `data-validation-and-contract-testing`
   - Feature definitions, offline/online parity, PIT joins: use `feast-feature-store-engineering`
   - GPU training, Volcano/K8s jobs, distributed PyTorch: use `distributed-gpu-training-and-scheduling`
   - MLflow logging, Unity Catalog registration, CT loops: use `mlflow-model-registry-and-continuous-training`
   - KServe, vLLM, LMCache, inference latency: use `llm-serving-and-inference-optimization`
   - Production drift, PSI, Evidently monitoring: use `model-monitoring-and-drift-detection`
   - zk-SNARK proofs, ONNX→EZKL circuits: use `verifiable-ai-and-zkml`
   - Fairlearn gates, Model Cards, demographic parity: use `responsible-ai-and-model-governance`

2. Choose the platform preset.
   - Kubernetes + Volcano GPU stack: `kubernetes-gpu-mlops`
   - Databricks Unity Catalog + MLflow: `databricks-unity-catalog-mlops`
   - AWS SageMaker-style stack: `aws-sagemaker-mlops`
   - GCP Vertex-style stack: `gcp-vertex-mlops`

3. Recommend the fastest bootstrap asset.
   - New pipeline: `templates/model-contract.yaml` or `templates/feature-contract.yaml`
   - Training release: `templates/training-release-gate.yaml`
   - Serving rollout: `templates/inference-service-checklist.yaml`
   - Drift incident: `templates/drift-incident-runbook.md`
   - Greenfield platform: `starter-packs/full-ml-lifecycle-starter.yaml`

4. Recommend an example when concrete context helps.
   - Runnable platform code: repository root (`data/`, `feature_store/`, `training/`, etc.)
   - End-to-end walkthrough: `examples/end-to-end-ml-lifecycle/`
   - LLM serving blueprint: `examples/kserve-vllm-lmcache-blueprint/`

5. Choose the safe next command.
   - unclear intent or missing contracts: `/spec`
   - approved scope but ambiguous sequencing: `/plan`
   - implementation with clear acceptance criteria: `/build`
   - quality, drift, fairness, or release gating: `/validate`
   - reliability, cost, or governance review: `/review`
   - retrain, backfill features, or replay training: `/retrain`
   - deployment or publish readiness: `/ship`

6. Pull supporting references only when needed.
   - feature store: `references/feast-pit-join-checklist.md`
   - GPU scheduling: `references/volcano-gang-scheduling-checklist.md`
   - serving: `references/llm-serving-latency-checklist.md`
   - monitoring: `references/drift-detection-checklist.md`
   - governance: `references/fairness-gate-checklist.md`

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "It is only a small model tweak." | Small changes can break serving skew, drift baselines, or fairness gates. |
| "We already have MLflow." | Tracking does not replace contract validation, PIT joins, or release proof. |
| "Inference works locally." | Production serving needs load tests, KV cache config, and rollback paths. |

## Red Flags

- agent starts coding before choosing a workflow skill
- training-serving skew not considered for feature changes
- drift or fairness gates skipped before promotion
- no named next command for the current task

## Verification

- [ ] Task type mapped to the correct workflow skill
- [ ] Platform preset chosen where relevant
- [ ] Starter template, pack, or example recommended when useful
- [ ] Safest next command identified
- [ ] Validation, monitoring, and governance risks not skipped during triage
