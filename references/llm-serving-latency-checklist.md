# LLM Serving Latency Checklist

- [ ] vLLM PagedAttention backend configured
- [ ] GPU memory utilization set (default 0.90)
- [ ] Prefix caching enabled where applicable
- [ ] LMCache Redis host/port configured
- [ ] Readiness probe allows model warm-up time
- [ ] Load test p95 below threshold (default 5000ms)
- [ ] Autoscale min/max replicas defined
- [ ] Rollback manifest version tagged
