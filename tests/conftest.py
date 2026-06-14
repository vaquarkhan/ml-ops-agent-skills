"""Shared pytest fixtures and optional dependency skip guards."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from tests._optional_deps import (
    FAIRLEARN_AVAILABLE,
    FEAST_AVAILABLE,
    GREAT_EXPECTATIONS_AVAILABLE,
    MLFLOW_AVAILABLE,
    TORCH_AVAILABLE,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "requires_torch: needs PyTorch installed")
    config.addinivalue_line("markers", "requires_gx: needs Great Expectations installed")
    config.addinivalue_line("markers", "requires_feast: needs Feast installed")
    config.addinivalue_line("markers", "requires_ezkl: needs ezkl CLI installed")
    config.addinivalue_line("markers", "requires_fairlearn: needs Fairlearn installed")
    config.addinivalue_line("markers", "requires_mlflow: needs MLflow installed")


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool | None:
    """Skip entire test modules when optional dependencies are missing."""
    name = collection_path.name
    if name == "test_training.py" and (not TORCH_AVAILABLE or not MLFLOW_AVAILABLE):
        return True
    if name == "test_zkml.py" and not TORCH_AVAILABLE:
        return True
    if name == "test_data_validation.py" and not GREAT_EXPECTATIONS_AVAILABLE:
        return True
    if name == "test_feature_store.py" and not FEAST_AVAILABLE:
        return True
    if name == "test_governance.py" and not FAIRLEARN_AVAILABLE:
        return True
    return None


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    for item in items:
        nodeid = item.nodeid
        if not TORCH_AVAILABLE and ("test_training" in nodeid or "test_zkml" in nodeid):
            item.add_marker(pytest.mark.skip(reason="PyTorch not available (optional dependency)"))
        if not GREAT_EXPECTATIONS_AVAILABLE and "test_data_validation" in nodeid:
            item.add_marker(
                pytest.mark.skip(reason="Great Expectations not available (optional dependency)")
            )
        if not FEAST_AVAILABLE and "test_feature_store" in nodeid:
            item.add_marker(pytest.mark.skip(reason="Feast not available (optional dependency)"))
        if not FAIRLEARN_AVAILABLE and "test_governance" in nodeid:
            item.add_marker(pytest.mark.skip(reason="Fairlearn not available (optional dependency)"))
        if not MLFLOW_AVAILABLE and "test_training" in nodeid:
            item.add_marker(pytest.mark.skip(reason="MLflow not available (optional dependency)"))


@pytest.fixture
def valid_raw_data() -> pd.DataFrame:
    """Valid upstream raw data matching GX expectation schema."""
    return pd.DataFrame(
        {
            "user_id": list(range(1, 151)),
            "event_timestamp": pd.to_datetime(["2024-01-01"] * 150),
            "feature_a": np.random.uniform(0, 1000, 150),
            "feature_b": np.random.uniform(-50, 50, 150),
            "feature_c": np.random.uniform(0, 1, 150),
            "label": np.random.choice([0, 1], 150),
        }
    )


@pytest.fixture
def poisoned_schema_data() -> pd.DataFrame:
    """Data with schema drift (missing columns, wrong types)."""
    return pd.DataFrame(
        {
            "user_id": ["not_an_int"] * 150,
            "event_timestamp": pd.to_datetime(["2024-01-01"] * 150),
            "feature_a": np.random.uniform(0, 1000, 150),
            "wrong_column": np.random.uniform(0, 1, 150),
        }
    )


@pytest.fixture
def poisoned_volume_data() -> pd.DataFrame:
    """Data with volume anomaly (too few rows)."""
    return pd.DataFrame(
        {
            "user_id": [1, 2],
            "event_timestamp": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "feature_a": [10.0, 20.0],
            "feature_b": [-1.0, 1.0],
            "feature_c": [0.5, 0.6],
            "label": [0, 1],
        }
    )


@pytest.fixture
def reference_monitoring_data() -> pd.DataFrame:
    """Reference training data for drift detection."""
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "feature_a": rng.normal(50, 10, 500),
            "feature_b": rng.normal(0, 5, 500),
            "feature_c": rng.uniform(0, 1, 500),
            "prediction_score": rng.uniform(0.3, 0.7, 500),
        }
    )


@pytest.fixture
def fairness_data() -> tuple[np.ndarray, np.ndarray, pd.Series]:
    """Balanced fairness evaluation dataset."""
    rng = np.random.default_rng(42)
    n = 200
    gender = pd.Series(rng.choice(["M", "F"], n))
    y_true = rng.choice([0, 1], n)
    y_pred = y_true.copy()
    y_pred[rng.choice(n, 5)] = 1 - y_pred[rng.choice(n, 5)]
    return y_true, y_pred, gender


@pytest.fixture
def biased_fairness_data() -> tuple[np.ndarray, np.ndarray, pd.Series]:
    """Biased dataset that should fail fairness gate."""
    n = 400
    gender = pd.Series(["M"] * (n // 2) + ["F"] * (n // 2))
    y_pred = np.array([1] * (n // 2) + [0] * (n // 2))
    y_true = np.random.choice([0, 1], n)
    return y_true, y_pred, gender


@pytest.fixture
def entity_df() -> pd.DataFrame:
    """Entity DataFrame for point-in-time feature retrieval."""
    return pd.DataFrame(
        {
            "user_id": [1, 2, 3, 4, 5],
            "event_timestamp": pd.to_datetime(
                ["2024-01-05", "2024-01-10", "2024-01-15", "2024-01-20", "2024-01-25"]
            ),
        }
    )
