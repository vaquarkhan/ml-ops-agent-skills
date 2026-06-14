#!/usr/bin/env bash
# Pre-retrain guard: verify feature store and data validation tests pass.
set -euo pipefail
echo "[retrain-guard] Validating data pipeline..."
python -m pytest tests/test_data_validation.py tests/test_feature_store.py -q
echo "[retrain-guard] PASS"
