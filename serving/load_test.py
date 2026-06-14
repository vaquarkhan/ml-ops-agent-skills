"""Async load testing for KServe vLLM inference endpoints."""

from __future__ import annotations

import argparse
import asyncio
import logging
import statistics
import time
from dataclasses import dataclass, field

import aiohttp

logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT = "http://localhost:8080/v1/completions"
DEFAULT_P95_THRESHOLD_MS = 5000.0


@dataclass
class LoadTestConfig:
    """Configuration for inference endpoint load testing."""

    endpoint_url: str = DEFAULT_ENDPOINT
    concurrent_requests: int = 50
    total_requests: int = 200
    p95_latency_threshold_ms: float = DEFAULT_P95_THRESHOLD_MS
    request_timeout_seconds: float = 30.0
    prompt: str = "Explain the importance of MLOps in production AI systems."


@dataclass
class LoadTestResult:
    """Aggregated load test metrics."""

    total_requests: int
    successful_requests: int
    failed_requests: int
    latencies_ms: list[float] = field(default_factory=list)
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    mean_latency_ms: float = 0.0
    requests_per_second: float = 0.0
    passed: bool = False

    def compute(self, threshold_ms: float) -> None:
        """Compute percentile metrics and pass/fail determination."""
        if self.latencies_ms:
            sorted_latencies = sorted(self.latencies_ms)
            self.mean_latency_ms = statistics.mean(sorted_latencies)
            self.p50_latency_ms = _percentile(sorted_latencies, 50)
            self.p95_latency_ms = _percentile(sorted_latencies, 95)
            self.p99_latency_ms = _percentile(sorted_latencies, 99)
        self.passed = (
            self.failed_requests == 0
            and self.p95_latency_ms <= threshold_ms
            and self.successful_requests > 0
        )


def _percentile(sorted_data: list[float], pct: float) -> float:
    """Calculate percentile from pre-sorted data."""
    if not sorted_data:
        return 0.0
    idx = int(len(sorted_data) * pct / 100)
    idx = min(idx, len(sorted_data) - 1)
    return sorted_data[idx]


async def _send_request(
    session: aiohttp.ClientSession,
    config: LoadTestConfig,
    semaphore: asyncio.Semaphore,
) -> tuple[bool, float]:
    """Send a single inference request and return success flag and latency."""
    payload = {
        "model": "llm-vllm-serving",
        "prompt": config.prompt,
        "max_tokens": 64,
        "temperature": 0.7,
    }
    async with semaphore:
        start = time.perf_counter()
        try:
            async with session.post(
                config.endpoint_url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=config.request_timeout_seconds),
            ) as response:
                await response.read()
                latency_ms = (time.perf_counter() - start) * 1000
                return response.status == 200, latency_ms
        except (aiohttp.ClientError, asyncio.TimeoutError):
            latency_ms = (time.perf_counter() - start) * 1000
            return False, latency_ms


async def run_load_test(config: LoadTestConfig) -> LoadTestResult:
    """
    Bombard the inference endpoint with concurrent requests.

    Args:
        config: Load test configuration parameters.

    Returns:
        LoadTestResult with percentile latencies and pass/fail status.
    """
    semaphore = asyncio.Semaphore(config.concurrent_requests)
    result = LoadTestResult(
        total_requests=config.total_requests,
        successful_requests=0,
        failed_requests=0,
    )

    start_time = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [
            _send_request(session, config, semaphore)
            for _ in range(config.total_requests)
        ]
        outcomes = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start_time

    for success, latency_ms in outcomes:
        result.latencies_ms.append(latency_ms)
        if success:
            result.successful_requests += 1
        else:
            result.failed_requests += 1

    result.requests_per_second = result.total_requests / max(elapsed, 0.001)
    result.compute(config.p95_latency_threshold_ms)

    logger.info(
        "Load test complete: %d/%d success, p95=%.1fms, rps=%.1f, passed=%s",
        result.successful_requests,
        result.total_requests,
        result.p95_latency_ms,
        result.requests_per_second,
        result.passed,
    )
    return result


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for load testing."""
    parser = argparse.ArgumentParser(description="KServe vLLM load tester")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--concurrent", type=int, default=50)
    parser.add_argument("--total", type=int, default=200)
    parser.add_argument("--p95-threshold-ms", type=float, default=DEFAULT_P95_THRESHOLD_MS)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO)
    config = LoadTestConfig(
        endpoint_url=args.endpoint,
        concurrent_requests=args.concurrent,
        total_requests=args.total,
        p95_latency_threshold_ms=args.p95_threshold_ms,
    )
    result = asyncio.run(run_load_test(config))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
