---
name: verifiable-ai-and-zkml
description: Generates zero-knowledge proofs for ML inference using EZKL, ONNX export, and Halo2 circuits. Use when implementing zk-SNARK proof pipelines, exporting PyTorch to ONNX, or verifying model execution without revealing weights.
---

# Verifiable AI and zkML

## Overview

Export PyTorch models to ONNX, compile into Halo2 cryptographic circuits via **EZKL**, generate zk-SNARK proofs validating inference execution over sample inputs **without revealing model weights**, and verify proofs in milliseconds.

## When to Use

- implementing verifiable inference pipelines
- exporting neural networks to ONNX for EZKL compilation
- generating and verifying zk-SNARK proof receipts
- demonstrating trustless ML execution to auditors
- testing cryptographic verification in CI (mock fallback when EZKL CLI absent)
- exploring zero-knowledge ML differentiators for regulated domains

## Decision Framework

| Stage | Tool |
|-------|------|
| Model | PyTorch `SimpleNN` in `zkml/generate_proof.py` |
| Export | `torch.onnx.export` opset 17 |
| Compile | `ezkl compile-circuit` |
| Prove | `ezkl prove` with witness + pk |
| Verify | `ezkl verify` or `_mock_verify` fallback |
| CI without EZKL | Mock artifacts — tests still pass |

## Workflow

1. Instantiate model: `ZKMLPipeline.create_model()`.
2. Export ONNX: `export_onnx(model)` → `artifacts/model.onnx`.
3. Compile circuit: `compile_circuit(onnx_path)` → settings + compiled circuit.
4. Generate witness from sample input JSON.
5. Run setup → prove → write `proof.json`.
6. Verify: `verify_proof(artifacts)` — must return True.
7. CLI: `python zkml/generate_proof.py`.
8. Test: `pytest tests/test_zkml.py -v` (requires torch).

## Anti-Patterns

- Shipping mock proofs as production verification
- Exposing model weights in public inputs
- Skipping verification step after proof generation
- Using unsupported ONNX ops without EZKL compatibility check
- Claiming zkML coverage without test verification path

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "zkML is academic only." | Regulated AI and audit trails benefit from verifiable execution. |
| "Mock fallback makes tests meaningless." | Mock proves pipeline wiring; real EZKL required for production proofs. |
| "ONNX export is enough." | Proof requires compile + witness + verify chain. |
| "Any neural net works." | Start with SimpleNN; validate EZKL support per architecture. |

## Red Flags

- proof.json without verification step
- EZKL CLI errors ignored in production path
- weights included in public inputs
- no test for verify_proof success
- agent claims zkML without running pipeline

## Verification

- [ ] ONNX export succeeds with deterministic sample input
- [ ] Proof artifact generated and persisted under `artifacts/`
- [ ] Verifier returns True (EZKL or documented mock fallback)
- [ ] `pytest tests/test_zkml.py` passes when torch available
- [ ] Proof receipt does not expose model weights
- [ ] Unique differentiator documented in Model Card intended use

## Implementation References

- Pipeline: `zkml/generate_proof.py`
- Tests: `tests/test_zkml.py`
- Unique capability: no other agent skills repo ships EZKL integration
