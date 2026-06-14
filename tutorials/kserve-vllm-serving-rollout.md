# KServe vLLM Serving Rollout

## Goal

Deploy LLM inference with p95 latency gate.

## Steps

1. Apply `serving/kserve/inference-service.yaml`.
2. Configure LMCache Redis env vars.
3. Load test: `python serving/load_test.py`.

Skill: `skills/llm-serving-and-inference-optimization/SKILL.md`
