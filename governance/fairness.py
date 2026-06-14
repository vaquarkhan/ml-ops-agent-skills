"""Fairlearn fairness evaluation, Model Card generation, and CI/CD gating."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from fairlearn.metrics import (
    MetricFrame,
    demographic_parity_difference,
    equalized_odds_difference,
)

logger = logging.getLogger(__name__)

DEFAULT_DP_THRESHOLD = float(os.getenv("FAIRNESS_DP_THRESHOLD", "0.05"))


class FairnessGateError(Exception):
    """Raised when fairness metrics exceed configured thresholds."""


@dataclass
class FairnessMetrics:
    """Computed fairness metrics across sensitive cohorts."""

    demographic_parity_difference: float
    equalized_odds_difference: float
    metric_frame: dict[str, Any] = field(default_factory=dict)
    sensitive_feature: str = "gender"
    passed: bool = False
    dp_threshold: float = DEFAULT_DP_THRESHOLD

    def evaluate_gate(self) -> None:
        """Determine pass/fail based on demographic parity threshold."""
        self.passed = abs(self.demographic_parity_difference) <= self.dp_threshold


@dataclass
class ModelCard:
    """Structured model card metadata."""

    model_name: str
    version: str
    description: str
    intended_use: str
    training_data_lineage: str
    fairness_metrics: FairnessMetrics
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    markdown_path: Path | None = None


class GovernancePipeline:
    """
    Automated governance pipeline computing Fairlearn metrics,
    generating Model Cards, and enforcing CI/CD fairness gates.
    """

    def __init__(self, dp_threshold: float = DEFAULT_DP_THRESHOLD) -> None:
        self.dp_threshold = dp_threshold

    def compute_fairness_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensitive_features: pd.Series,
        sensitive_feature_name: str = "gender",
    ) -> FairnessMetrics:
        """
        Calculate Demographic Parity and Equalized Odds using Fairlearn.

        Args:
            y_true: Ground truth labels.
            y_pred: Model predictions (binary).
            sensitive_features: Sensitive attribute per sample.
            sensitive_feature_name: Name of the sensitive feature column.

        Returns:
            FairnessMetrics with computed values and gate evaluation.
        """
        dp_diff = demographic_parity_difference(
            y_true, y_pred, sensitive_features=sensitive_features
        )
        eo_diff = equalized_odds_difference(
            y_true, y_pred, sensitive_features=sensitive_features
        )

        metric_frame = MetricFrame(
            metrics={"accuracy": lambda yt, yp: float(np.mean(yt == yp))},
            y_true=y_true,
            y_pred=y_pred,
            sensitive_features=sensitive_features,
        )

        metrics = FairnessMetrics(
            demographic_parity_difference=float(dp_diff),
            equalized_odds_difference=float(eo_diff),
            metric_frame={
                "by_group": metric_frame.by_group.to_dict(),
                "overall": float(metric_frame.overall.get("accuracy", 0.0)),
            },
            sensitive_feature=sensitive_feature_name,
            dp_threshold=self.dp_threshold,
        )
        metrics.evaluate_gate()

        logger.info(
            "Fairness metrics: DP diff=%.4f, EO diff=%.4f, passed=%s",
            metrics.demographic_parity_difference,
            metrics.equalized_odds_difference,
            metrics.passed,
        )
        return metrics

    def enforce_fairness_gate(self, metrics: FairnessMetrics) -> None:
        """
        CI/CD gate that fails the pipeline if DP difference exceeds threshold.

        Args:
            metrics: Computed fairness metrics.

        Raises:
            FairnessGateError: If demographic parity difference exceeds margin.
        """
        if not metrics.passed:
            raise FairnessGateError(
                f"Fairness gate FAILED: demographic parity difference "
                f"{metrics.demographic_parity_difference:.4f} exceeds threshold "
                f"{metrics.dp_threshold:.4f}."
            )
        logger.info("Fairness gate PASSED.")

    def generate_model_card(
        self,
        model_name: str,
        version: str,
        fairness_metrics: FairnessMetrics,
        training_data_lineage: str = "Feast feature store → GX validated upstream data",
        intended_use: str = "Binary user event classification for production inference.",
        output_dir: Path | None = None,
    ) -> ModelCard:
        """
        Generate a Model Card in markdown format summarizing governance metrics.

        Args:
            model_name: Registered model name.
            version: Model version identifier.
            fairness_metrics: Computed Fairlearn metrics.
            training_data_lineage: Description of training data provenance.
            intended_use: Documented intended use cases.
            output_dir: Directory to write the markdown file.

        Returns:
            ModelCard with generated markdown path.
        """
        output_dir = output_dir or Path("governance/model_cards")
        output_dir.mkdir(parents=True, exist_ok=True)

        card = ModelCard(
            model_name=model_name,
            version=version,
            description=f"Production classifier: {model_name} v{version}",
            intended_use=intended_use,
            training_data_lineage=training_data_lineage,
            fairness_metrics=fairness_metrics,
        )

        md_content = self._render_model_card_markdown(card)
        md_path = output_dir / f"{model_name}_v{version}_model_card.md"
        md_path.write_text(md_content, encoding="utf-8")
        card.markdown_path = md_path

        logger.info("Model card generated: %s", md_path)
        return card

    def _render_model_card_markdown(self, card: ModelCard) -> str:
        """Render Model Card content as markdown."""
        fm = card.fairness_metrics
        gate_status = "PASSED" if fm.passed else "FAILED"

        return f"""# Model Card: {card.model_name} v{card.version}

## Model Details
- **Description**: {card.description}
- **Generated At**: {card.generated_at}
- **Version**: {card.version}

## Intended Use
{card.intended_use}

## Training Data Lineage
{card.training_data_lineage}

## Fairness Metrics (Fairlearn)

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Demographic Parity Difference | {fm.demographic_parity_difference:.4f} | {fm.dp_threshold:.4f} | {gate_status} |
| Equalized Odds Difference | {fm.equalized_odds_difference:.4f} | N/A | — |

### Accuracy by {fm.sensitive_feature}
```
{fm.metric_frame.get('by_group', {})}
```

### Overall Accuracy
{fm.metric_frame.get('overall', 'N/A')}

## Governance Gate
Fairness CI/CD gate: **{gate_status}**

## Ethical Considerations
- Model predictions must not be used as sole basis for high-stakes decisions.
- Regular fairness audits are required when deployment cohorts shift.
- Sensitive feature `{fm.sensitive_feature}` is monitored for disparate impact.
"""
