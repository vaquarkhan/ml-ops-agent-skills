---
name: llm-serving-and-inference-optimization
description: Deploys high-performance LLM inference with KServe, vLLM PagedAttention, and LMCache distributed KV caching. Use when authoring InferenceService manifests, tuning GPU memory, or load testing p95 latency under concurrent requests.
---

# LLM Serving and Inference Optimization

## Overview

Deploy large language models via KServe with vLLM backend leveraging **PagedAttention**, prefix caching, and **LMCache** Redis-backed distributed KV cache sharing across replicas. Validate p95 latency under concurrent load before promotion.

## When to Use

- authoring KServe InferenceService YAML manifests
- configuring vLLM memory utilization and attention backend
- setting up LMCache for cross-instance KV cache hit rate
- load testing inference endpoints (`serving/load_test.py`)
- tuning autoscale min/max replicas for LLM workloads
- investigating inference latency regressions

## Decision Framework

| Tuning knob | Starting point |
|-------------|----------------|
| GPU memory | `VLLM_GPU_MEMORY_UTILIZATION=0.90` |
| Max context | `VLLM_MAX_MODEL_LEN=4096` |
| Prefix caching | `VLLM_ENABLE_PREFIX_CACHING=true` |
| LMCache | Redis at `lmcache-redis.mlops.svc.cluster.local:6379` |
| p95 gate | Default 5000ms (`P95_LATENCY_THRESHOLD_MS`) |
| Concurrency | Load test 50 concurrent, 200 total requests |

## Workflow

1. Review manifest: `serving/kserve/inference-service.yaml`.
2. Configure vLLM args: dtype, max-model-len, prefix caching, KV cache dtype.
3. Deploy LMCache Redis sidecar and wire env vars (`LMCACHE_*`).
4. Set readiness/liveness probes with adequate warm-up delay (120s+).
5. Run load test: `python serving/load_test.py --endpoint <url> --concurrent 50`.
6. Assert `LoadTestResult.passed` — p95 below threshold, zero failures.
7. Unit test async client: `pytest tests/test_serving.py -v`.

## Anti-Patterns

- Deploying without readiness probes (premature traffic)
- Disabling prefix caching for repeated prompt patterns
- No LMCache when running multiple vLLM replicas
- Load testing with sequential requests only
- Promoting on mean latency while p95 fails SLA

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "It works on one GPU locally." | Production needs gang-aware autoscale, probes, and concurrent load proof. |
| "LMCache adds complexity." | Cross-replica KV sharing dramatically cuts tail latency. |
| "5000ms p95 is loose." | Tune threshold per SLA; gate must exist and be enforced. |
| "We can skip load tests in CI." | Async load test mocks prove harness; run live test pre-ship. |

## Red Flags

- InferenceService without resource limits
- missing LMCache Redis dependency
- no autoscale bounds defined
- load test failures ignored before `/ship`
- vLLM OOM kills under concurrent load

## Verification

- [ ] InferenceService uses vLLM backend with realistic CPU/memory/GPU limits
- [ ] LMCache enabled with Redis host/port configured
- [ ] Prefix caching and PagedAttention args present
- [ ] Load test passes p95 threshold under concurrent requests
- [ ] Readiness/liveness probes configured with warm-up time
- [ ] Checklist: `references/llm-serving-latency-checklist.md` complete

## Implementation References

- Manifest: `serving/kserve/inference-service.yaml`
- Load test: `serving/load_test.py`
- Example: `examples/kserve-vllm-lmcache-blueprint/`
