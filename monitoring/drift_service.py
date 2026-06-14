"""Evidently-based data drift detection with PSI and Wasserstein metrics."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_PSI_THRESHOLD = float(os.getenv("PSI_DRIFT_THRESHOLD", "0.2"))


def _run_evidently_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
) -> dict[str, Any]:
    """
    Run Evidently DataDriftPreset report (lazy import to avoid startup failures).

    Args:
        reference_data: Reference training dataset.
        current_data: Current production dataset.

    Returns:
        Evidently report as dictionary.
    """
    from evidently.metric_preset import DataDriftPreset
    from evidently.report import Report

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    return report.as_dict()


@dataclass
class DriftReport:
    """Structured drift detection result."""

    drift_detected: bool
    psi_values: dict[str, float] = field(default_factory=dict)
    wasserstein_values: dict[str, float] = field(default_factory=dict)
    drifted_columns: list[str] = field(default_factory=list)
    psi_threshold: float = DEFAULT_PSI_THRESHOLD
    raw_report: dict[str, Any] = field(default_factory=dict)


class DriftDetectionService:
    """
    Continuous monitoring service comparing reference (training) data
    against current production inference data using Evidently AI.
    """

    NUMERIC_COLUMNS = ["feature_a", "feature_b", "feature_c", "prediction_score"]

    def __init__(self, psi_threshold: float = DEFAULT_PSI_THRESHOLD) -> None:
        self.psi_threshold = psi_threshold

    def detect_drift(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
    ) -> DriftReport:
        """
        Run Evidently DataDriftPreset and evaluate PSI/Wasserstein thresholds.

        Args:
            reference_data: Training/reference dataset.
            current_data: Current production inference dataset.

        Returns:
            DriftReport with drift_detected boolean and per-column metrics.
        """
        ref = reference_data.copy()
        cur = current_data.copy()

        for col in self.NUMERIC_COLUMNS:
            if col not in ref.columns:
                ref[col] = 0.0
            if col not in cur.columns:
                cur[col] = 0.0

        try:
            report_dict = _run_evidently_report(ref, cur)
        except Exception as exc:
            logger.warning("Evidently report unavailable (%s); using PSI fallback.", exc)
            report_dict = {
                "_reference_data": ref,
                "_current_data": cur,
                "metrics": [],
            }

        psi_values = self._extract_psi(report_dict, ref, cur)
        wasserstein_values = self._extract_wasserstein(ref, cur)
        drifted_columns = [
            col for col, psi in psi_values.items() if psi > self.psi_threshold
        ]

        drift_detected = len(drifted_columns) > 0

        if drift_detected:
            logger.warning(
                "Drift Detected: columns %s exceed PSI threshold %.2f",
                drifted_columns,
                self.psi_threshold,
            )
        else:
            logger.info("No drift detected. All PSI values below %.2f.", self.psi_threshold)

        return DriftReport(
            drift_detected=drift_detected,
            psi_values=psi_values,
            wasserstein_values=wasserstein_values,
            drifted_columns=drifted_columns,
            psi_threshold=self.psi_threshold,
            raw_report=report_dict,
        )

    def _extract_psi(
        self,
        report_dict: dict[str, Any],
        reference: pd.DataFrame | None = None,
        current: pd.DataFrame | None = None,
    ) -> dict[str, float]:
        """Extract Population Stability Index values from Evidently report."""
        psi_values: dict[str, float] = {}
        for metric in report_dict.get("metrics", []):
            metric_result = metric.get("result", {})
            if "drift_by_columns" in metric_result:
                for col, info in metric_result["drift_by_columns"].items():
                    drift_score = info.get("drift_score")
                    if drift_score is not None:
                        psi_values[col] = float(drift_score)
        if not psi_values:
            ref_data = reference if reference is not None else report_dict.get("_reference_data")
            cur_data = current if current is not None else report_dict.get("_current_data")
            psi_values = self._compute_psi_fallback(ref_data, cur_data)
        return psi_values

    def _compute_psi_fallback(
        self,
        reference: pd.DataFrame | None,
        current: pd.DataFrame | None,
    ) -> dict[str, float]:
        """Compute PSI manually when Evidently report lacks extracted values."""
        if reference is None or current is None:
            return {}
        psi_values: dict[str, float] = {}
        for col in self.NUMERIC_COLUMNS:
            if col in reference.columns and col in current.columns:
                psi_values[col] = compute_psi(
                    reference[col].dropna().values,
                    current[col].dropna().values,
                )
        return psi_values

    def _extract_wasserstein(
        self,
        reference: pd.DataFrame,
        current: pd.DataFrame,
    ) -> dict[str, float]:
        """Calculate Wasserstein distance for each numeric column."""
        from scipy.stats import wasserstein_distance

        distances: dict[str, float] = {}
        for col in self.NUMERIC_COLUMNS:
            if col in reference.columns and col in current.columns:
                ref_vals = reference[col].dropna().values
                cur_vals = current[col].dropna().values
                if len(ref_vals) > 0 and len(cur_vals) > 0:
                    distances[col] = float(wasserstein_distance(ref_vals, cur_vals))
        return distances


def compute_psi(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """
    Calculate Population Stability Index between two distributions.

    Args:
        reference: Reference (training) distribution samples.
        current: Current (production) distribution samples.
        bins: Number of histogram bins for discretization.

    Returns:
        PSI value (higher indicates greater distribution shift).
    """
    epsilon = 1e-6
    breakpoints = np.linspace(
        min(reference.min(), current.min()),
        max(reference.max(), current.max()),
        bins + 1,
    )
    ref_counts, _ = np.histogram(reference, bins=breakpoints)
    cur_counts, _ = np.histogram(current, bins=breakpoints)

    ref_pct = ref_counts / max(len(reference), 1) + epsilon
    cur_pct = cur_counts / max(len(current), 1) + epsilon

    ref_pct = ref_pct / ref_pct.sum()
    cur_pct = cur_pct / cur_pct.sum()

    psi = float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))
    return psi


def generate_synthetic_drifted_data(
    reference: pd.DataFrame,
    drift_magnitude: float = 3.0,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetically drifted production data for testing.

    Args:
        reference: Reference training DataFrame.
        drift_magnitude: Standard deviations to shift feature distributions.
        seed: Random seed for reproducibility.

    Returns:
        Drifted DataFrame simulating production distribution shift.
    """
    rng = np.random.default_rng(seed)
    drifted = reference.copy()
    for col in ["feature_a", "feature_b", "feature_c"]:
        if col in drifted.columns:
            std = drifted[col].std() or 1.0
            drifted[col] = drifted[col] + rng.normal(0, std * drift_magnitude, len(drifted))
    if "prediction_score" in drifted.columns:
        drifted["prediction_score"] = np.clip(
            drifted["prediction_score"] + rng.uniform(0.2, 0.5, len(drifted)),
            0,
            1,
        )
    return drifted
