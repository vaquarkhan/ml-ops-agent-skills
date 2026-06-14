# Examples

Example packs for MLOps agent workflows.

## Runnable Platform (this repository)

The full platform implementation is at the repository root:

| Module | Path | Run |
|--------|------|-----|
| Data validation | `data/` | `pytest tests/test_data_validation.py` |
| Feature store | `feature_store/` | `pytest tests/test_feature_store.py` |
| GPU K8s validate | `k8s/` | `python training/validate_k8s.py` |
| Training | `training/` | `pytest tests/test_training.py` |
| Serving load test | `serving/` | `python serving/load_test.py` |
| Drift detection | `monitoring/` | `pytest tests/test_monitoring.py` |
| zkML | `zkml/` | `python zkml/generate_proof.py` |
| Governance | `governance/` | `pytest tests/test_governance.py` |

## Example Packs

| Example | Type | Description |
|---------|------|-------------|
| [end-to-end-ml-lifecycle](end-to-end-ml-lifecycle/) | Runnable | Full lifecycle walkthrough README |
| [kserve-vllm-lmcache-blueprint](kserve-vllm-lmcache-blueprint/) | Blueprint | spec/plan for LLM serving rollout |
| [feast-pit-training-dataset](feast-pit-training-dataset/) | Runnable | PIT join smoke test script |
| [fairness-gate-ci](fairness-gate-ci/) | Runnable | Fairness CI gate demonstration |

## Selector

- Need executable proof → use repository root or **Runnable** examples
- Need `/spec` → `/plan` only → use **Blueprint** examples
