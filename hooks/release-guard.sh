#!/usr/bin/env bash
# Pre-release guard: run tests and K8s validation before ship.
set -euo pipefail
echo "[release-guard] Running pytest..."
python -m pytest tests/ -q --ignore=tests/test_training.py --ignore=tests/test_zkml.py
echo "[release-guard] Validating K8s manifests..."
python training/validate_k8s.py
echo "[release-guard] PASS"
