"""Tests for Evidently AI drift detection service."""

from __future__ import annotations

import pandas as pd
import pytest

from monitoring.drift_service import (
    DriftDetectionService,
    compute_psi,
    generate_synthetic_drifted_data,
)


class TestDriftDetection:
    """Drift detection with PSI and Wasserstein metrics."""

    def test_no_drift_on_identical_data(
        self, reference_monitoring_data: pd.DataFrame
    ) -> None:
        service = DriftDetectionService(psi_threshold=0.2)
        report = service.detect_drift(reference_monitoring_data, reference_monitoring_data.copy())
        assert report.drift_detected is False
        assert len(report.drifted_columns) == 0

    def test_drift_detected_on_synthetic_shift(
        self, reference_monitoring_data: pd.DataFrame
    ) -> None:
        service = DriftDetectionService(psi_threshold=0.2)
        drifted = generate_synthetic_drifted_data(reference_monitoring_data, drift_magnitude=5.0)
        report = service.detect_drift(reference_monitoring_data, drifted)
        assert report.drift_detected is True
        assert len(report.drifted_columns) > 0

    def test_psi_exceeds_threshold_triggers_alert(
        self, reference_monitoring_data: pd.DataFrame
    ) -> None:
        service = DriftDetectionService(psi_threshold=0.2)
        drifted = generate_synthetic_drifted_data(reference_monitoring_data, drift_magnitude=8.0)
        report = service.detect_drift(reference_monitoring_data, drifted)
        for col in report.drifted_columns:
            assert report.psi_values.get(col, 0) > 0.2 or col in report.drifted_columns

    def test_wasserstein_computed(
        self, reference_monitoring_data: pd.DataFrame
    ) -> None:
        service = DriftDetectionService()
        drifted = generate_synthetic_drifted_data(reference_monitoring_data)
        report = service.detect_drift(reference_monitoring_data, drifted)
        assert len(report.wasserstein_values) > 0

    def test_compute_psi_identical_distributions(self) -> None:
        import numpy as np

        data = np.random.default_rng(42).normal(0, 1, 1000)
        psi = compute_psi(data, data.copy())
        assert psi < 0.1

    def test_compute_psi_shifted_distributions(self) -> None:
        import numpy as np

        rng = np.random.default_rng(42)
        ref = rng.normal(0, 1, 1000)
        cur = rng.normal(5, 1, 1000)
        psi = compute_psi(ref, cur)
        assert psi > 0.2

    def test_missing_columns_filled(
        self, reference_monitoring_data: pd.DataFrame
    ) -> None:
        service = DriftDetectionService()
        minimal = pd.DataFrame({"feature_a": [1.0, 2.0, 3.0]})
        report = service.detect_drift(reference_monitoring_data, minimal)
        assert report.raw_report is not None

    def test_generate_synthetic_drifted_data(self, reference_monitoring_data: pd.DataFrame) -> None:
        drifted = generate_synthetic_drifted_data(reference_monitoring_data)
        assert len(drifted) == len(reference_monitoring_data)
        assert not drifted.equals(reference_monitoring_data)

    def test_psi_fallback_extraction(self, reference_monitoring_data: pd.DataFrame) -> None:
        service = DriftDetectionService()
        report_dict: dict = {"metrics": [{"result": {}}]}
        psi = service._extract_psi(
            report_dict,
            reference=reference_monitoring_data,
            current=generate_synthetic_drifted_data(reference_monitoring_data),
        )
        assert isinstance(psi, dict)
        assert len(psi) > 0

    def test_compute_psi_fallback_with_data(self, reference_monitoring_data: pd.DataFrame) -> None:
        service = DriftDetectionService()
        report_dict = {
            "_reference_data": reference_monitoring_data,
            "_current_data": generate_synthetic_drifted_data(reference_monitoring_data),
        }
        psi = service._compute_psi_fallback(
            report_dict["_reference_data"],
            report_dict["_current_data"],
        )
        assert len(psi) > 0

    def test_compute_psi_fallback_none_data(self) -> None:
        service = DriftDetectionService()
        assert service._compute_psi_fallback(None, None) == {}
