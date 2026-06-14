"""Tests for KServe vLLM load testing."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from serving.load_test import (
    LoadTestConfig,
    LoadTestResult,
    _percentile,
    _send_request,
    main,
    run_load_test,
)


def _make_async_response(status: int = 200) -> MagicMock:
    """Build a mock aiohttp response with async read."""
    response = MagicMock()
    response.status = status
    response.read = AsyncMock(return_value=b"ok")
    return response


def _make_async_session(response: MagicMock | None = None, post_error: Exception | None = None) -> MagicMock:
    """Build a mock ClientSession with async context manager for post()."""
    session = MagicMock()

    if post_error is not None:
        session.post = MagicMock(side_effect=post_error)
        return session

    response = response or _make_async_response()
    post_cm = MagicMock()
    post_cm.__aenter__ = AsyncMock(return_value=response)
    post_cm.__aexit__ = AsyncMock(return_value=None)
    session.post = MagicMock(return_value=post_cm)
    return session


class TestLoadTest:
    """Async load test for inference endpoints."""

    def test_percentile_calculation(self) -> None:
        data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        assert _percentile(data, 50) == 6.0
        assert _percentile(data, 95) == 10.0
        assert _percentile([], 50) == 0.0

    def test_load_test_result_compute_pass(self) -> None:
        result = LoadTestResult(
            total_requests=10,
            successful_requests=10,
            failed_requests=0,
            latencies_ms=[100.0, 200.0, 150.0, 180.0, 120.0],
        )
        result.compute(threshold_ms=5000.0)
        assert result.passed is True

    def test_load_test_result_compute_fail_high_latency(self) -> None:
        result = LoadTestResult(
            total_requests=5,
            successful_requests=5,
            failed_requests=0,
            latencies_ms=[6000.0, 7000.0, 8000.0],
        )
        result.compute(threshold_ms=5000.0)
        assert result.passed is False

    def test_load_test_result_compute_fail_errors(self) -> None:
        result = LoadTestResult(
            total_requests=5,
            successful_requests=3,
            failed_requests=2,
            latencies_ms=[100.0, 200.0, 300.0],
        )
        result.compute(threshold_ms=5000.0)
        assert result.passed is False

    def test_load_test_result_compute_fail_no_success(self) -> None:
        result = LoadTestResult(
            total_requests=1,
            successful_requests=0,
            failed_requests=1,
            latencies_ms=[100.0],
        )
        result.compute(threshold_ms=5000.0)
        assert result.passed is False

    @pytest.mark.asyncio
    async def test_send_request_success(self) -> None:
        config = LoadTestConfig()
        session = _make_async_session()
        success, latency = await _send_request(session, config, asyncio.Semaphore(10))
        assert success is True
        assert latency >= 0

    @pytest.mark.asyncio
    async def test_send_request_failure(self) -> None:
        config = LoadTestConfig()
        session = _make_async_session(post_error=aiohttp.ClientError("connection refused"))
        success, latency = await _send_request(session, config, asyncio.Semaphore(10))
        assert success is False

    @pytest.mark.asyncio
    async def test_send_request_non_200(self) -> None:
        config = LoadTestConfig()
        session = _make_async_session(_make_async_response(status=500))
        success, _ = await _send_request(session, config, asyncio.Semaphore(10))
        assert success is False

    @pytest.mark.asyncio
    async def test_send_request_timeout(self) -> None:
        config = LoadTestConfig()
        session = _make_async_session(post_error=asyncio.TimeoutError())
        success, _ = await _send_request(session, config, asyncio.Semaphore(10))
        assert success is False

    @pytest.mark.asyncio
    @patch("serving.load_test.aiohttp.ClientSession")
    async def test_run_load_test_all_success(self, mock_session_class: MagicMock) -> None:
        mock_session = _make_async_session()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        config = LoadTestConfig(total_requests=5, concurrent_requests=2)
        result = await run_load_test(config)
        assert result.successful_requests == 5
        assert result.passed is True

    @patch("serving.load_test.asyncio.run")
    def test_main_returns_zero_on_pass(self, mock_asyncio_run: MagicMock) -> None:
        passed_result = LoadTestResult(
            total_requests=1, successful_requests=1, failed_requests=0, latencies_ms=[50.0]
        )
        passed_result.compute(5000.0)
        mock_asyncio_run.return_value = passed_result
        assert main([]) == 0

    @patch("serving.load_test.asyncio.run")
    def test_main_returns_one_on_fail(self, mock_asyncio_run: MagicMock) -> None:
        failed_result = LoadTestResult(
            total_requests=1, successful_requests=0, failed_requests=1, latencies_ms=[9000.0]
        )
        failed_result.compute(5000.0)
        mock_asyncio_run.return_value = failed_result
        assert main([]) == 1
