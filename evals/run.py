#!/usr/bin/env python3
"""Benchmark skill routing coverage against MLOps task scenarios."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Task scenario -> expected skill name
BENCHMARK_TASKS: dict[str, str] = {
    "schema drift in raw ingestion": "data-validation-and-contract-testing",
    "point-in-time feature join for training": "feast-feature-store-engineering",
    "volcano gang scheduling for GPU job": "distributed-gpu-training-and-scheduling",
    "register model to unity catalog": "mlflow-model-registry-and-continuous-training",
    "kserve vllm inference latency": "llm-serving-and-inference-optimization",
    "production drift PSI alert": "model-monitoring-and-drift-detection",
    "zero knowledge proof for model inference": "verifiable-ai-and-zkml",
    "demographic parity fairness gate": "responsible-ai-and-model-governance",
    "new mlops session triage": "using-mlops-agent-skills",
    "dbt contract for validated events": "data-validation-and-contract-testing",
    "lmcache redis kv cache config": "llm-serving-and-inference-optimization",
    "ezkl onnx circuit compile": "verifiable-ai-and-zkml",
}


def load_skill_keywords() -> dict[str, set[str]]:
    keywords: dict[str, set[str]] = {}
    for skill_file in ROOT.glob("skills/*/SKILL.md"):
        name = skill_file.parent.name
        text = skill_file.read_text(encoding="utf-8").lower()
        tokens = set(name.replace("-", " ").split())
        tokens.update(w for w in text.split() if len(w) > 4)
        keywords[name] = tokens
    return keywords


def route_task(task: str, keywords: dict[str, set[str]]) -> str | None:
    task_tokens = set(task.lower().replace("-", " ").split())
    best_name: str | None = None
    best_score = 0
    for name, tokens in keywords.items():
        score = len(task_tokens & tokens)
        if score > best_score:
            best_score = score
            best_name = name
    return best_name


def main() -> int:
    keywords = load_skill_keywords()
    hits = 0
    results: list[dict[str, str]] = []

    for task, expected in BENCHMARK_TASKS.items():
        routed = route_task(task, keywords)
        success = routed == expected
        if success:
            hits += 1
        results.append({"task": task, "expected": expected, "routed": routed or "none", "hit": success})

    coverage = hits / len(BENCHMARK_TASKS) * 100
    report = {"coverage_pct": coverage, "hits": hits, "total": len(BENCHMARK_TASKS), "results": results}
    out = ROOT / "evals" / "last-run.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Skill routing benchmark: {hits}/{len(BENCHMARK_TASKS)} ({coverage:.1f}%)")
    if coverage < 70:
        print("Benchmark FAILED: coverage below 70% threshold")
        return 1
    print("Benchmark PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
