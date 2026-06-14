#!/usr/bin/env python3
"""Benchmark skill routing coverage against MLOps task scenarios."""

from __future__ import annotations

import json
import re
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

# Multi-token triggers checked before fuzzy overlap (resolves ambiguous scenarios).
ROUTING_TRIGGERS: list[tuple[frozenset[str], str]] = [
    (frozenset({"point", "time"}), "feast-feature-store-engineering"),
    (frozenset({"zero", "knowledge"}), "verifiable-ai-and-zkml"),
    (frozenset({"ezkl"}), "verifiable-ai-and-zkml"),
    (frozenset({"demographic", "parity"}), "responsible-ai-and-model-governance"),
    (frozenset({"volcano", "gang"}), "distributed-gpu-training-and-scheduling"),
    (frozenset({"unity", "catalog"}), "mlflow-model-registry-and-continuous-training"),
    (frozenset({"lmcache"}), "llm-serving-and-inference-optimization"),
    (frozenset({"kserve", "vllm"}), "llm-serving-and-inference-optimization"),
]

STOPWORDS = {
    "for",
    "in",
    "the",
    "a",
    "an",
    "to",
    "and",
    "or",
    "with",
    "when",
    "use",
    "before",
    "after",
    "this",
    "that",
    "from",
}


def tokenize(text: str) -> set[str]:
    """Normalize punctuation/hyphens and drop short stopwords."""
    normalized = re.sub(r"[^\w\s]", " ", text.lower())
    return {word for word in normalized.split() if len(word) > 2 and word not in STOPWORDS}


def _parse_frontmatter_description(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("---", 3)
    if end == -1:
        return ""
    block = text[3:end]
    for line in block.splitlines():
        if line.strip().startswith("description:"):
            return line.split(":", 1)[1].strip()
    return ""


def load_skill_keywords() -> dict[str, set[str]]:
    keywords: dict[str, set[str]] = {}
    for skill_file in ROOT.glob("skills/*/SKILL.md"):
        name = skill_file.parent.name
        text = skill_file.read_text(encoding="utf-8")
        tokens = tokenize(name.replace("-", " "))
        tokens.update(tokenize(_parse_frontmatter_description(text)))
        tokens.update(tokenize(text))
        keywords[name] = tokens
    return keywords


def route_task(task: str, keywords: dict[str, set[str]]) -> str | None:
    task_tokens = tokenize(task)

    best_trigger: tuple[frozenset[str], str] | None = None
    for trigger_tokens, skill in ROUTING_TRIGGERS:
        if trigger_tokens <= task_tokens:
            if best_trigger is None or len(trigger_tokens) > len(best_trigger[0]):
                best_trigger = (trigger_tokens, skill)
    if best_trigger is not None:
        return best_trigger[1]

    best_name: str | None = None
    best_score = 0
    for name, tokens in keywords.items():
        slug_tokens = tokenize(name.replace("-", " "))
        score = len(task_tokens & tokens)
        score += 2 * len(task_tokens & slug_tokens)
        if score > best_score:
            best_score = score
            best_name = name
    return best_name


def main() -> int:
    keywords = load_skill_keywords()
    hits = 0
    results: list[dict[str, str | bool]] = []

    for task, expected in BENCHMARK_TASKS.items():
        routed = route_task(task, keywords)
        success = routed == expected
        if success:
            hits += 1
        results.append(
            {"task": task, "expected": expected, "routed": routed or "none", "hit": success}
        )

    coverage = hits / len(BENCHMARK_TASKS) * 100
    report = {
        "coverage_pct": coverage,
        "hits": hits,
        "total": len(BENCHMARK_TASKS),
        "results": results,
    }
    out = ROOT / "evals" / "last-run.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Skill routing benchmark: {hits}/{len(BENCHMARK_TASKS)} ({coverage:.1f}%)")
    if coverage < 100:
        misses = [r for r in results if not r["hit"]]
        for miss in misses:
            print(f"  MISS: {miss['task']!r} -> {miss['routed']} (expected {miss['expected']})")
    if coverage < 100:
        print("Benchmark FAILED: expected 100% routing coverage")
        return 1
    print("Benchmark PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
