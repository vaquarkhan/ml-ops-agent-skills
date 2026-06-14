"""Integration tests for Feast feature store point-in-time retrieval."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from feature_store.retrieval import (
    FeatureRetrievalError,
    build_training_dataset,
    get_online_features,
    _build_feature_refs,
    _validate_no_leakage,
)


@pytest.fixture
def mock_feature_store() -> MagicMock:
    """Mock Feast FeatureStore with historical and online retrieval."""
    store = MagicMock()

    batch_view = MagicMock()
    batch_view.schema = [
        MagicMock(name="feature_a"),
        MagicMock(name="feature_b"),
        MagicMock(name="label"),
    ]
    for field in batch_view.schema:
        field.name = field._mock_name

    realtime_view = MagicMock()
    realtime_view.schema = [
        MagicMock(name="feature_c"),
        MagicMock(name="session_count"),
        MagicMock(name="last_active_minutes"),
    ]
    for field in realtime_view.schema:
        field.name = field._mock_name

    def get_view(name: str) -> MagicMock:
        views = {
            "user_batch_features": batch_view,
            "user_realtime_features": realtime_view,
        }
        return views[name]

    store.get_feature_view.side_effect = get_view

    historical_result = MagicMock()
    historical_result.to_df.return_value = pd.DataFrame(
        {
            "user_id": [1, 2, 3],
            "event_timestamp": pd.to_datetime(["2024-01-05", "2024-01-10", "2024-01-15"]),
            "feature_a": [10.0, 20.0, 30.0],
            "feature_b": [-1.0, 0.0, 1.0],
            "feature_c": [0.5, 0.6, 0.7],
            "session_count": [3, 5, 2],
            "label": [0, 1, 0],
        }
    )
    store.get_historical_features.return_value = historical_result

    online_result = MagicMock()
    online_result.to_df.return_value = pd.DataFrame(
        {
            "user_id": [1, 2],
            "feature_c": [0.8, 0.9],
            "session_count": [7, 4],
            "last_active_minutes": [10, 20],
        }
    )
    store.get_online_features.return_value = online_result

    return store


class TestFeatureRetrieval:
    """Tests for point-in-time feature retrieval."""

    def test_build_training_dataset_success(
        self, entity_df: pd.DataFrame, mock_feature_store: MagicMock
    ) -> None:
        result = build_training_dataset(entity_df.iloc[:3], mock_feature_store)
        assert len(result) == 3
        assert "feature_a" in result.columns
        assert "label" in result.columns
        mock_feature_store.get_historical_features.assert_called_once()

    def test_missing_entity_columns_raises(self, mock_feature_store: MagicMock) -> None:
        bad_df = pd.DataFrame({"user_id": [1]})
        with pytest.raises(FeatureRetrievalError, match="missing required columns"):
            build_training_dataset(bad_df, mock_feature_store)

    def test_historical_retrieval_failure_raises(
        self, entity_df: pd.DataFrame, mock_feature_store: MagicMock
    ) -> None:
        mock_feature_store.get_historical_features.side_effect = RuntimeError("Feast error")
        with pytest.raises(FeatureRetrievalError, match="Historical feature retrieval failed"):
            build_training_dataset(entity_df.iloc[:3], mock_feature_store)

    def test_empty_training_dataset_raises(self, mock_feature_store: MagicMock) -> None:
        entity_df = pd.DataFrame(
            {"user_id": [1], "event_timestamp": pd.to_datetime(["2024-01-01"])}
        )
        empty_result = MagicMock()
        empty_result.to_df.return_value = pd.DataFrame()
        mock_feature_store.get_historical_features.return_value = empty_result

        with pytest.raises(FeatureRetrievalError, match="empty"):
            build_training_dataset(entity_df, mock_feature_store)

    def test_get_online_features(
        self, mock_feature_store: MagicMock
    ) -> None:
        result = get_online_features([1, 2], mock_feature_store)
        assert len(result) == 2
        mock_feature_store.get_online_features.assert_called_once()

    def test_build_feature_refs(self, mock_feature_store: MagicMock) -> None:
        refs = _build_feature_refs(
            mock_feature_store, ["user_batch_features", "user_realtime_features"]
        )
        assert "user_batch_features:feature_a" in refs
        assert "user_realtime_features:feature_c" in refs

    def test_validate_no_leakage_passes(self, entity_df: pd.DataFrame) -> None:
        training_df = entity_df.iloc[:3].copy()
        training_df["feature_a"] = [1.0, 2.0, 3.0]
        _validate_no_leakage(entity_df.iloc[:3], training_df)

    def test_validate_no_leakage_mismatch_raises(self, entity_df: pd.DataFrame) -> None:
        training_df = entity_df.iloc[:3].copy()
        training_df.loc[0, "event_timestamp"] = pd.Timestamp("2025-01-01")
        with pytest.raises(FeatureRetrievalError, match="Point-in-time join mismatch"):
            _validate_no_leakage(entity_df.iloc[:3], training_df)

    @patch("feature_store.retrieval.FeatureStore")
    def test_get_feature_store_default_path(self, mock_fs_class: MagicMock) -> None:
        get_online_features([1], feature_store=mock_fs_class.return_value)
        mock_fs_class.return_value.get_online_features.assert_called()

    def test_default_feature_views(self, entity_df: pd.DataFrame, mock_feature_store: MagicMock) -> None:
        build_training_dataset(entity_df.iloc[:3], mock_feature_store, feature_view_names=None)
        assert mock_feature_store.get_feature_view.call_count >= 2
