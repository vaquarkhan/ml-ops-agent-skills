---
name: llm-serving-and-inference-optimization
description: Deploys high-performance LLM inference with KServe, vLLM PagedAttention, and LMCache distributed KV caching. Use for InferenceService manifests and async load testing.
---

# LLM Serving and Inference Optimization

## Overview

Deploy LLMs via KServe with vLLM backend, enable prefix caching and LMCache Redis-backed KV sharing, and validate p95 latency under concurrent load.

## When to Use

- authoring KServe InferenceService YAML
- configuring vLLM memory utilization and attention backend
- setting up LMCache for cross-instance KV cache
- load testing inference endpoints

## Workflow

1. Review manifest in `serving/kserve/inference-service.yaml`.
2. Configure vLLM args (PagedAttention, prefix caching, dtype).
3. Deploy LMCache Redis sidecar and env vars.
4. Run async load test: `python serving/load_test.py --endpoint <url>`.
5. Assert p95 latency below threshold (default 5000ms).

## Verification

- [ ] InferenceService uses vLLM backend with realistic resource limits
- [ ] LMCache enabled with Redis connection configured
- [ ] Load test passes p95 threshold under concurrent requests
- [ ] Readiness/liveness probes configured
