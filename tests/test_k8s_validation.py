"""Tests for Volcano Kubernetes manifest validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from training.validate_k8s import VolcanoConfigValidator, ValidationResult, main


@pytest.fixture
def validator() -> VolcanoConfigValidator:
    return VolcanoConfigValidator()


class TestVolcanoConfigValidator:
    """Dry-run validation tests for K8s manifests."""

    def test_validate_queue_passes(self, validator: VolcanoConfigValidator) -> None:
        result = validator.validate_queue()
        assert result.valid is True
        assert result.manifest == "queue.yaml"

    def test_validate_podgroup_passes(self, validator: VolcanoConfigValidator) -> None:
        result = validator.validate_podgroup()
        assert result.valid is True
        assert result.manifest == "podgroup.yaml"

    def test_validate_training_job_passes(self, validator: VolcanoConfigValidator) -> None:
        result = validator.validate_training_job()
        assert result.valid is True

    def test_validate_all_returns_three_results(
        self, validator: VolcanoConfigValidator
    ) -> None:
        results = validator.validate_all()
        assert len(results) == 3
        assert all(isinstance(r, ValidationResult) for r in results)

    def test_podgroup_missing_fields_fails(self, validator: VolcanoConfigValidator) -> None:
        bad_manifest: dict[str, Any] = {"spec": {}}
        result = validator.validate_podgroup(bad_manifest)
        assert result.valid is False
        assert len(result.errors) > 0

    def test_podgroup_low_min_member_warns(self, validator: VolcanoConfigValidator) -> None:
        manifest: dict[str, Any] = {
            "spec": {
                "minMember": 1,
                "queue": "test-queue",
                "minResources": {"nvidia.com/gpu": "1"},
            }
        }
        result = validator.validate_podgroup(manifest)
        assert len(result.warnings) > 0

    def test_queue_missing_gpu_fails(self, validator: VolcanoConfigValidator) -> None:
        manifest: dict[str, Any] = {"spec": {"weight": 1, "capability": {"cpu": "4"}}}
        result = validator.validate_queue(manifest)
        assert result.valid is False

    def test_job_wrong_scheduler_fails(self, validator: VolcanoConfigValidator) -> None:
        manifest: dict[str, Any] = {
            "spec": {"schedulerName": "default-scheduler", "minAvailable": 4, "tasks": []}
        }
        result = validator.validate_training_job(manifest)
        assert result.valid is False

    def test_job_missing_gpu_fails(self, validator: VolcanoConfigValidator) -> None:
        manifest: dict[str, Any] = {
            "spec": {
                "schedulerName": "volcano",
                "minAvailable": 4,
                "tasks": [
                    {
                        "template": {
                            "spec": {
                                "containers": [
                                    {"name": "worker", "resources": {"requests": {"cpu": "1"}}}
                                ]
                            }
                        }
                    }
                ],
            }
        }
        result = validator.validate_training_job(manifest)
        assert result.valid is False

    def test_load_manifest_not_found(self, tmp_path: Path) -> None:
        v = VolcanoConfigValidator(manifest_dir=tmp_path)
        with pytest.raises(FileNotFoundError):
            v.load_manifest("nonexistent.yaml")

    def test_main_returns_zero_on_success(self, validator: VolcanoConfigValidator) -> None:
        assert main() == 0

    def test_queue_missing_required_fields(self, validator: VolcanoConfigValidator) -> None:
        result = validator.validate_queue({"spec": {}})
        assert result.valid is False

    def test_job_min_available_too_low(self, validator: VolcanoConfigValidator) -> None:
        manifest: dict[str, Any] = {
            "spec": {"schedulerName": "volcano", "minAvailable": 1, "tasks": []}
        }
        result = validator.validate_training_job(manifest)
        assert result.valid is False
