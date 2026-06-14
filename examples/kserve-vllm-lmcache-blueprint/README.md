# KServe + vLLM + LMCache Blueprint

Architecture blueprint for high-performance LLM serving (spec/plan only).

## Spec

- **Goal**: Deploy Llama-class model with p95 latency under 5s at 50 concurrent requests
- **Backend**: KServe InferenceService with vLLM PagedAttention
- **Cache**: LMCache Redis-backed distributed KV cache
- **Autoscale**: 2–8 replicas based on queue depth

## Plan

1. Apply `serving/kserve/inference-service.yaml`
2. Deploy LMCache Redis (`lmcache-redis` Service)
3. Configure env: `LMCACHE_ENABLED=true`, `VLLM_ENABLE_PREFIX_CACHING=true`
4. Run load test: `python serving/load_test.py --concurrent 50 --total 200`
5. Gate promotion on p95 < 5000ms

## Artifacts

- Manifest: `../../serving/kserve/inference-service.yaml`
- Load test: `../../serving/load_test.py`
- Skill: `../../skills/llm-serving-and-inference-optimization/SKILL.md`
