# LLM Serving Latency Checklist

Use when rolling out KServe InferenceServices with vLLM and LMCache.

> **Provenance:** vLLM documentation (PagedAttention); KServe InferenceService spec; LMCache project documentation.

- [ ] vLLM PagedAttention backend configured
- [ ] GPU memory utilization set (default 0.90)
- [ ] Prefix caching enabled where applicable
- [ ] LMCache Redis host/port configured
- [ ] Readiness probe allows model warm-up time
- [ ] Load test p95 below threshold (default 5000ms)
- [ ] Autoscale min/max replicas defined
- [ ] Rollback manifest version tagged

## Sources

| Source | URL | Last reviewed |
|--------|-----|---------------|
| vLLM — PagedAttention | https://docs.vllm.ai/en/latest/ | 2026-06-14 |
| KServe — InferenceService API | https://kserve.github.io/website/latest/modelserving/v1beta1/inference_service/ | 2026-06-14 |
| LMCache — KV cache reuse | https://github.com/LMCache/LMCache | 2026-06-14 |
| Runnable reference | `serving/kserve-vllm.yaml` | 2026-06-14 |
| Runnable reference | `serving/load_test.py` | 2026-06-14 |
