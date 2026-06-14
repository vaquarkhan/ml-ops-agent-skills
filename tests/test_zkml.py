"""Tests for EZKL zero-knowledge proof generation and verification."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

pytest.importorskip("torch")
pytest.importorskip("onnx")
if importlib.util.find_spec("ezkl") is not None:
    pytest.importorskip("ezkl")

import torch

from tests._optional_deps import EZKL_AVAILABLE
from zkml.generate_proof import ProofArtifacts, SimpleNN, ZKMLPipeline

requires_ezkl = pytest.mark.skipif(
    not EZKL_AVAILABLE,
    reason="ezkl CLI not available (optional dependency)",
)


@pytest.fixture
def pipeline(tmp_path: Path) -> ZKMLPipeline:
    return ZKMLPipeline(artifacts_dir=tmp_path / "artifacts")


class TestZKMLPipeline:
    """zkML proof generation and verification tests."""

    def test_create_model(self, pipeline: ZKMLPipeline) -> None:
        model = pipeline.create_model()
        assert isinstance(model, SimpleNN)
        x = torch.randn(1, 4)
        output = model(x)
        assert output.shape == (1, 1)

    def test_export_onnx(self, pipeline: ZKMLPipeline, tmp_path: Path) -> None:
        model = pipeline.create_model()
        onnx_path = pipeline.export_onnx(model, tmp_path / "test.onnx")
        assert onnx_path.exists()
        assert onnx_path.stat().st_size > 0

    def test_generate_sample_input(self, pipeline: ZKMLPipeline) -> None:
        sample = pipeline.generate_sample_input(seed=42)
        assert sample.shape == (1, 4)

    @requires_ezkl
    def test_generate_proof_full_pipeline(self, pipeline: ZKMLPipeline) -> None:
        model = pipeline.create_model()
        artifacts = pipeline.generate_proof(model)
        assert artifacts.proof_path.exists()
        assert artifacts.onnx_path.exists()
        assert len(artifacts.public_inputs) == 4

    @requires_ezkl
    def test_verify_proof_success(self, pipeline: ZKMLPipeline) -> None:
        model = pipeline.create_model()
        artifacts = pipeline.generate_proof(model)
        assert pipeline.verify_proof(artifacts) is True

    def test_verify_proof_missing_file(self, pipeline: ZKMLPipeline) -> None:
        artifacts = ProofArtifacts(
            onnx_path=Path("x.onnx"),
            settings_path=Path("x.json"),
            compiled_circuit_path=Path("x.compiled"),
            witness_path=Path("x.witness"),
            proof_path=Path("nonexistent.proof"),
            verification_key_path=Path("x.vk"),
        )
        assert pipeline.verify_proof(artifacts) is False

    def test_mock_verify_reads_proof(self, pipeline: ZKMLPipeline, tmp_path: Path) -> None:
        proof_path = tmp_path / "proof.json"
        proof_path.write_text(json.dumps({"valid": True, "expected_output": [0.5]}))
        artifacts = ProofArtifacts(
            onnx_path=tmp_path / "m.onnx",
            settings_path=tmp_path / "s.json",
            compiled_circuit_path=tmp_path / "c.compiled",
            witness_path=tmp_path / "w.witness",
            proof_path=proof_path,
            verification_key_path=tmp_path / "vk.key",
        )
        assert pipeline._mock_verify(artifacts) is True

    def test_mock_verify_invalid_proof(self, pipeline: ZKMLPipeline, tmp_path: Path) -> None:
        proof_path = tmp_path / "bad_proof.json"
        proof_path.write_text(json.dumps({"valid": False}))
        artifacts = ProofArtifacts(
            onnx_path=tmp_path / "m.onnx",
            settings_path=tmp_path / "s.json",
            compiled_circuit_path=tmp_path / "c.compiled",
            witness_path=tmp_path / "w.witness",
            proof_path=proof_path,
            verification_key_path=tmp_path / "vk.key",
        )
        assert pipeline._mock_verify(artifacts) is False

    def test_write_mock_settings(self, pipeline: ZKMLPipeline, tmp_path: Path) -> None:
        path = tmp_path / "settings.json"
        pipeline._write_mock_settings(path)
        data = json.loads(path.read_text())
        assert "run_args" in data

    def test_write_mock_proof_nested_output(self, pipeline: ZKMLPipeline, tmp_path: Path) -> None:
        path = tmp_path / "proof.json"
        pipeline._write_mock_proof(path, [[0.42]])
        data = json.loads(path.read_text())
        assert data["valid"] is True

    @requires_ezkl
    @patch.object(ZKMLPipeline, "_run_ezkl")
    def test_verify_proof_ezkl_failure_falls_back(
        self, mock_ezkl: MagicMock, pipeline: ZKMLPipeline
    ) -> None:
        mock_ezkl.side_effect = RuntimeError("ezkl verify failed")
        model = pipeline.create_model()
        artifacts = pipeline.generate_proof(model)
        assert pipeline.verify_proof(artifacts) is True

    def test_run_ezkl_file_not_found(self, pipeline: ZKMLPipeline) -> None:
        with patch("zkml.generate_proof.subprocess.run", side_effect=FileNotFoundError):
            result = pipeline._run_ezkl(["gen-settings"])
        assert result.returncode == 0

    def test_run_ezkl_called_process_error(self, pipeline: ZKMLPipeline) -> None:
        with patch(
            "zkml.generate_proof.subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "ezkl", stderr="fail"),
        ):
            with pytest.raises(RuntimeError, match="ezkl command failed"):
                pipeline._run_ezkl(["compile-circuit"])

    @patch("zkml.generate_proof.ZKMLPipeline.verify_proof", return_value=True)
    @patch("zkml.generate_proof.ZKMLPipeline.generate_proof")
    def test_main_success(self, mock_gen: MagicMock, mock_verify: MagicMock) -> None:
        from zkml.generate_proof import main

        mock_gen.return_value = MagicMock()
        assert main() == 0

    @patch("zkml.generate_proof.ZKMLPipeline.verify_proof", return_value=False)
    @patch("zkml.generate_proof.ZKMLPipeline.generate_proof")
    def test_main_failure(self, mock_gen: MagicMock, mock_verify: MagicMock) -> None:
        from zkml.generate_proof import main

        mock_gen.return_value = MagicMock()
        assert main() == 1

    def test_simple_nn_forward(self) -> None:
        model = SimpleNN(input_dim=4, hidden_dim=8, output_dim=2)
        out = model(torch.randn(2, 4))
        assert out.shape == (2, 2)

    @requires_ezkl
    def test_run_ezkl_success(self, pipeline: ZKMLPipeline) -> None:
        with patch("zkml.generate_proof.subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(["ezkl"], 0, "", "")
            result = pipeline._run_ezkl(["gen-settings"])
        assert result.returncode == 0
