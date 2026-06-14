# End-to-End MLOps Lifecycle

Runnable walkthrough using the platform modules in this repository.

## Prerequisites

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Steps

### 1. Validate upstream data

```bash
pytest tests/test_data_validation.py -v
```

### 2. Build point-in-time training features

```bash
python feature_store/feature_repo/generate_sample_data.py
pytest tests/test_feature_store.py -v
```

### 3. Validate Kubernetes manifests

```bash
python training/validate_k8s.py
```

### 4. Run drift and governance gates

```bash
pytest tests/test_monitoring.py tests/test_governance.py -v
```

### 5. Load test serving (mock endpoint)

```bash
pytest tests/test_serving.py -v
```

## Skills

- `skills/using-mlops-agent-skills/SKILL.md`
- `starter-packs/full-ml-lifecycle-starter.yaml`
