"""Tests for PyTorch training pipeline with MLflow Unity Catalog integration."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("torch")
pytest.importorskip("mlflow")

import torch

from training.train import TrainingConfig, TrainingPipeline, UserClassifier


@pytest.fixture
def training_pipeline() -> TrainingPipeline:
    return TrainingPipeline(TrainingConfig(epochs=2, batch_size=16))


@pytest.fixture
def mock_training_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(42)
    X = rng.uniform(0, 1, (100, 4)).astype(np.float32)
    y = rng.choice([0, 1], 100).astype(np.float32)
    split = 80
    return X[:split], X[split:], y[:split], y[split:]


class TestUserClassifier:
    """Tests for the PyTorch model."""

    def test_forward_pass_shape(self) -> None:
        model = UserClassifier(input_dim=4, hidden_dim=64)
        x = torch.randn(8, 4)
        output = model(x)
        assert output.shape == (8, 1)

    def test_forward_pass_values_in_range(self) -> None:
        model = UserClassifier(input_dim=4)
        output = model(torch.randn(4, 4))
        assert (output >= 0).all() and (output <= 1).all()


class TestTrainingPipeline:
    """Tests for continuous training with MLflow."""

    def test_train_returns_metrics(
        self,
        training_pipeline: TrainingPipeline,
        mock_training_data: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    ) -> None:
        X_train, X_val, y_train, y_val = mock_training_data
        metrics = training_pipeline.train(X_train, y_train, X_val, y_val)
        assert "train_loss" in metrics
        assert "val_loss" in metrics
        assert "val_accuracy" in metrics
        assert training_pipeline.model is not None

    def test_prepare_data_with_mock_feast(
        self, training_pipeline: TrainingPipeline, entity_df: pd.DataFrame
    ) -> None:
        mock_df = pd.DataFrame(
            {
                "user_id": [1, 2, 3, 4, 5],
                "event_timestamp": entity_df["event_timestamp"],
                "feature_a": [1.0, 2.0, 3.0, 4.0, 5.0],
                "feature_b": [0.1, 0.2, 0.3, 0.4, 0.5],
                "feature_c": [0.5, 0.6, 0.7, 0.8, 0.9],
                "session_count": [1, 2, 3, 4, 5],
                "label": [0, 1, 0, 1, 0],
            }
        )
        with patch("training.train.build_training_dataset", return_value=mock_df):
            result = training_pipeline.prepare_data(entity_df)
        assert len(result) == 4

    def test_prepare_data_missing_label_raises(
        self, training_pipeline: TrainingPipeline, entity_df: pd.DataFrame
    ) -> None:
        mock_df = pd.DataFrame({"feature_a": [1.0], "feature_b": [2.0]})
        with patch("training.train.build_training_dataset", return_value=mock_df):
            with pytest.raises(ValueError, match="label"):
                training_pipeline.prepare_data(entity_df)

    def test_prepare_data_no_features_raises(
        self, training_pipeline: TrainingPipeline, entity_df: pd.DataFrame
    ) -> None:
        mock_df = pd.DataFrame({"label": [0, 1], "other": [1, 2]})
        with patch("training.train.build_training_dataset", return_value=mock_df):
            with pytest.raises(ValueError, match="No feature columns"):
                training_pipeline.prepare_data(entity_df)

    @patch("training.train.mlflow")
    def test_run_logs_and_registers(
        self,
        mock_mlflow: MagicMock,
        training_pipeline: TrainingPipeline,
        entity_df: pd.DataFrame,
        mock_training_data: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    ) -> None:
        mock_run = MagicMock()
        mock_run.info.run_id = "run_123"
        mock_mlflow.start_run.return_value.__enter__ = MagicMock(return_value=mock_run)
        mock_mlflow.start_run.return_value.__exit__ = MagicMock(return_value=False)

        mock_model_info = MagicMock()
        mock_model_info.model_uri = "models:/test/1"
        mock_mlflow.pytorch.log_model.return_value = mock_model_info

        with patch.object(training_pipeline, "prepare_data", return_value=mock_training_data):
            result = training_pipeline.run(entity_df)

        assert result["run_id"] == "run_123"
        assert result["stage_tag"] == "staging"
        mock_mlflow.set_tag.assert_any_call("stage", "staging")
        mock_mlflow.pytorch.autolog.assert_called_once()

    def test_training_config_defaults(self) -> None:
        config = TrainingConfig()
        assert config.epochs == 10
        assert config.registry_uri == "databricks-uc"

    def test_evaluate_computes_accuracy(
        self,
        training_pipeline: TrainingPipeline,
        mock_training_data: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    ) -> None:
        _, X_val, _, y_val = mock_training_data
        training_pipeline.model = UserClassifier(input_dim=4)
        criterion = torch.nn.BCELoss()
        val_loss, val_acc = training_pipeline._evaluate(X_val, y_val, criterion)
        assert val_loss >= 0
        assert 0 <= val_acc <= 1

    def test_configure_mlflow(self, training_pipeline: TrainingPipeline) -> None:
        with patch("training.train.mlflow") as mock_mlflow:
            training_pipeline._configure_mlflow()
            mock_mlflow.set_tracking_uri.assert_called_once()
            mock_mlflow.set_registry_uri.assert_called_once()
