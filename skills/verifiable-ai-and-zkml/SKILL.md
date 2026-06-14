---
name: verifiable-ai-and-zkml
description: Generates zero-knowledge proofs for ML inference using EZKL, ONNX export, and Halo2 circuits. Use for zk-SNARK proof generation and cryptographic verification.
---

# Verifiable AI and zkML

## Overview

Export PyTorch models to ONNX, compile into Halo2 circuits via EZKL, generate zk-SNARK proofs, and verify execution without revealing weights.

## When to Use

- implementing zkML proof pipelines
- exporting neural networks to ONNX for EZKL
- generating and verifying proof receipts
- testing cryptographic validation in milliseconds

## Workflow

1. Define model in `zkml/generate_proof.py` (`SimpleNN`).
2. Export ONNX → compile circuit → generate witness → prove.
3. Verify proof with `verify_proof` (EZKL CLI or mock fallback).
4. Run tests: `pytest tests/test_zkml.py -v`.
5. CLI entry: `python zkml/generate_proof.py`.

## Verification

- [ ] ONNX export succeeds with deterministic sample input
- [ ] Proof artifact generated and persisted
- [ ] Verifier validates proof receipt
- [ ] Tests cover mock fallback when EZKL CLI unavailable
