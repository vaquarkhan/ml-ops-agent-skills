"""Tests for Fairlearn governance gates and Model Card generation."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from governance.fairness import (
    FairnessGateError,
    FairnessMetrics,
    GovernancePipeline,
    ModelCard,
)


class TestGovernancePipeline:
    """Fairlearn fairness evaluation and CI/CD gating tests."""

    def test_fairness_metrics_pass_gate(
        self, fairness_data: tuple[np.ndarray, np.ndarray, pd.Series]
    ) -> None:
        y_true, y_pred, sensitive = fairness_data
        pipeline = GovernancePipeline(dp_threshold=0.05)
        metrics = pipeline.compute_fairness_metrics(y_true, y_pred, sensitive)
        assert metrics.passed is True
        assert abs(metrics.demographic_parity_difference) <= 0.05

    def test_fairness_gate_fails_on_bias(
        self, biased_fairness_data: tuple[np.ndarray, np.ndarray, pd.Series]
    ) -> None:
        y_true, y_pred, sensitive = biased_fairness_data
        pipeline = GovernancePipeline(dp_threshold=0.05)
        metrics = pipeline.compute_fairness_metrics(y_true, y_pred, sensitive)
        assert metrics.passed is False

        with pytest.raises(FairnessGateError, match="Fairness gate FAILED"):
            pipeline.enforce_fairness_gate(metrics)

    def test_enforce_gate_passes(
        self, fairness_data: tuple[np.ndarray, np.ndarray, pd.Series]
    ) -> None:
        y_true, y_pred, sensitive = fairness_data
        pipeline = GovernancePipeline(dp_threshold=0.05)
        metrics = pipeline.compute_fairness_metrics(y_true, y_pred, sensitive)
        pipeline.enforce_fairness_gate(metrics)

    def test_generate_model_card(
        self,
        fairness_data: tuple[np.ndarray, np.ndarray, pd.Series],
        tmp_path: Path,
    ) -> None:
        y_true, y_pred, sensitive = fairness_data
        pipeline = GovernancePipeline()
        metrics = pipeline.compute_fairness_metrics(y_true, y_pred, sensitive)
        card = pipeline.generate_model_card(
            model_name="user_classifier",
            version="1.0.0",
            fairness_metrics=metrics,
            output_dir=tmp_path,
        )
        assert card.markdown_path is not None
        assert card.markdown_path.exists()
        content = card.markdown_path.read_text(encoding="utf-8")
        assert "Model Card" in content
        assert "Demographic Parity" in content
        assert "Fairlearn" in content

    def test_model_card_failed_gate_markdown(
        self, biased_fairness_data: tuple[np.ndarray, np.ndarray, pd.Series], tmp_path: Path
    ) -> None:
        y_true, y_pred, sensitive = biased_fairness_data
        pipeline = GovernancePipeline(dp_threshold=0.05)
        metrics = pipeline.compute_fairness_metrics(y_true, y_pred, sensitive)
        card = pipeline.generate_model_card(
            model_name="biased_model",
            version="0.1.0",
            fairness_metrics=metrics,
            output_dir=tmp_path,
        )
        content = card.markdown_path.read_text(encoding="utf-8")
        assert "FAILED" in content

    def test_fairness_metrics_evaluate_gate(self) -> None:
        metrics = FairnessMetrics(
            demographic_parity_difference=0.03,
            equalized_odds_difference=0.02,
            dp_threshold=0.05,
        )
        metrics.evaluate_gate()
        assert metrics.passed is True

        metrics.demographic_parity_difference = 0.10
        metrics.evaluate_gate()
        assert metrics.passed is False

    def test_fairness_gate_error_is_exception(self) -> None:
        assert issubclass(FairnessGateError, Exception)

    def test_model_card_dataclass(self) -> None:
        metrics = FairnessMetrics(
            demographic_parity_difference=0.01,
            equalized_odds_difference=0.02,
        )
        metrics.evaluate_gate()
        card = ModelCard(
            model_name="test",
            version="1",
            description="test model",
            intended_use="testing",
            training_data_lineage="test data",
            fairness_metrics=metrics,
        )
        assert card.model_name == "test"
        assert card.generated_at is not None

    def test_equalized_odds_computed(
        self, fairness_data: tuple[np.ndarray, np.ndarray, pd.Series]
    ) -> None:
        y_true, y_pred, sensitive = fairness_data
        pipeline = GovernancePipeline()
        metrics = pipeline.compute_fairness_metrics(y_true, y_pred, sensitive)
        assert isinstance(metrics.equalized_odds_difference, float)
