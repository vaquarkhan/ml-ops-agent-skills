"""Shared pytest fixtures for the MLOps platform test suite."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


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
