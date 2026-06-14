"""PyTorch training loop with Feast features and MLflow Unity Catalog registration."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mlflow
import mlflow.pytorch
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

from feature_store.retrieval import build_training_dataset, get_feature_store

logger = logging.getLogger(__name__)


@dataclass
class TrainingConfig:
    """Configuration for the continuous training loop."""

    experiment_name: str = "mlops_continuous_training"
    model_name: str = "user_classifier"
    registry_uri: str = field(
        default_factory=lambda: os.getenv(
            "DATABRICKS_UC_REGISTRY_URI", "databricks-uc"
        )
    )
    tracking_uri: str = field(
        default_factory=lambda: os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    )
    unity_catalog_model: str = field(
        default_factory=lambda: os.getenv(
            "UC_MODEL_NAME", "main.mlops.user_classifier"
        )
    )
    epochs: int = 10
    batch_size: int = 32
    learning_rate: float = 0.001
    hidden_dim: int = 64
    staging_tag: str = "staging"
    seed: int = 42


class UserClassifier(nn.Module):
    """Simple feed-forward classifier for user event prediction."""

    def __init__(self, input_dim: int, hidden_dim: int = 64) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


class TrainingPipeline:
    """
    Automated continuous training pipeline.

    Pulls point-in-time features from Feast, trains a PyTorch model,
    autologs metrics via MLflow, and registers artifacts to Unity Catalog.
    """

    FEATURE_COLUMNS = ["feature_a", "feature_b", "feature_c", "session_count"]

    def __init__(self, config: TrainingConfig | None = None) -> None:
        self.config = config or TrainingConfig()
        self.scaler = StandardScaler()
        self.model: UserClassifier | None = None

    def _configure_mlflow(self) -> None:
        """Set MLflow tracking and registry URIs."""
        mlflow.set_tracking_uri(self.config.tracking_uri)
        mlflow.set_registry_uri(self.config.registry_uri)
        mlflow.set_experiment(self.config.experiment_name)
        mlflow.pytorch.autolog(log_models=True, log_datasets=True)

    def prepare_data(self, entity_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Build training dataset from Feast and split into train/validation.

        Args:
            entity_df: Entity DataFrame with user_id and event_timestamp.

        Returns:
            Tuple of (X_train, X_val, y_train, y_val) numpy arrays.
        """
        feature_store = get_feature_store()
        training_df = build_training_dataset(entity_df, feature_store)

        available_features = [c for c in self.FEATURE_COLUMNS if c in training_df.columns]
        if not available_features:
            raise ValueError(f"No feature columns found. Expected: {self.FEATURE_COLUMNS}")

        if "label" not in training_df.columns:
            raise ValueError("Training dataset missing 'label' column.")

        X = training_df[available_features].fillna(0.0).values.astype(np.float32)
        y = training_df["label"].values.astype(np.float32)

        return train_test_split(X, y, test_size=0.2, random_state=self.config.seed)

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
    ) -> dict[str, float]:
        """
        Train the PyTorch classifier and return final metrics.

        Args:
            X_train: Training feature matrix.
            y_train: Training labels.
            X_val: Validation feature matrix.
            y_val: Validation labels.

        Returns:
            Dictionary of final training and validation metrics.
        """
        torch.manual_seed(self.config.seed)
        input_dim = X_train.shape[1]

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)

        train_loader = DataLoader(
            TensorDataset(
                torch.tensor(X_train_scaled, dtype=torch.float32),
                torch.tensor(y_train.reshape(-1, 1), dtype=torch.float32),
            ),
            batch_size=self.config.batch_size,
            shuffle=True,
        )

        self.model = UserClassifier(input_dim, self.config.hidden_dim)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.config.learning_rate)
        criterion = nn.BCELoss()

        final_metrics: dict[str, float] = {}

        for epoch in range(self.config.epochs):
            self.model.train()
            epoch_loss = 0.0
            for batch_x, batch_y in train_loader:
                optimizer.zero_grad()
                outputs = self.model(batch_x)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()

            val_loss, val_acc = self._evaluate(X_val_scaled, y_val, criterion)
            avg_loss = epoch_loss / max(len(train_loader), 1)
            final_metrics = {
                "train_loss": avg_loss,
                "val_loss": val_loss,
                "val_accuracy": val_acc,
                "epoch": float(epoch + 1),
            }
            logger.info("Epoch %d: train_loss=%.4f val_loss=%.4f val_acc=%.4f",
                        epoch + 1, avg_loss, val_loss, val_acc)

        return final_metrics

    def _evaluate(
        self,
        X_val: np.ndarray,
        y_val: np.ndarray,
        criterion: nn.Module,
    ) -> tuple[float, float]:
        """Compute validation loss and accuracy."""
        assert self.model is not None
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.tensor(X_val, dtype=torch.float32)
            y_tensor = torch.tensor(y_val.reshape(-1, 1), dtype=torch.float32)
            outputs = self.model(X_tensor)
            val_loss = criterion(outputs, y_tensor).item()
            predictions = (outputs >= 0.5).float()
            val_acc = (predictions == y_tensor).float().mean().item()
        return val_loss, val_acc

    def run(self, entity_df: pd.DataFrame) -> dict[str, Any]:
        """
        Execute the full training loop with MLflow logging and UC registration.

        Args:
            entity_df: Entity DataFrame for point-in-time feature retrieval.

        Returns:
            Run metadata including run_id, metrics, and model URI.
        """
        self._configure_mlflow()
        X_train, X_val, y_train, y_val = self.prepare_data(entity_df)

        with mlflow.start_run(run_name=f"train_{self.config.model_name}") as run:
            mlflow.log_params(
                {
                    "epochs": self.config.epochs,
                    "batch_size": self.config.batch_size,
                    "learning_rate": self.config.learning_rate,
                    "hidden_dim": self.config.hidden_dim,
                    "input_dim": X_train.shape[1],
                }
            )

            metrics = self.train(X_train, y_train, X_val, y_val)
            for key, value in metrics.items():
                mlflow.log_metric(key, value)

            assert self.model is not None
            model_info = mlflow.pytorch.log_model(
                pytorch_model=self.model,
                artifact_path="model",
                registered_model_name=self.config.unity_catalog_model,
            )

            mlflow.set_tag("stage", self.config.staging_tag)
            mlflow.set_tag("framework", "pytorch")
            mlflow.set_tag("feature_store", "feast")

            logger.info("Model registered: %s (run_id=%s)", model_info.model_uri, run.info.run_id)

            return {
                "run_id": run.info.run_id,
                "metrics": metrics,
                "model_uri": model_info.model_uri,
                "registered_model_name": self.config.unity_catalog_model,
                "stage_tag": self.config.staging_tag,
            }
