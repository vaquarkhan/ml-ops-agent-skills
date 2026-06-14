"""Optional dependency detection for pytest skip guards."""

from __future__ import annotations

import importlib.util


def _can_import(module: str) -> bool:
    if importlib.util.find_spec(module) is None:
        return False
    try:
        importlib.import_module(module)
        return True
    except (ImportError, OSError):
        return False


TORCH_AVAILABLE = _can_import("torch")
FEAST_AVAILABLE = _can_import("feast")
GREAT_EXPECTATIONS_AVAILABLE = _can_import("great_expectations")
EVIDENTLY_AVAILABLE = _can_import("evidently")
MLFLOW_AVAILABLE = _can_import("mlflow")
ONNX_AVAILABLE = _can_import("onnx")

# EZKL is CLI-based; treat as optional unless CLI present
EZKL_AVAILABLE = False
try:
    import shutil

    EZKL_AVAILABLE = shutil.which("ezkl") is not None
except Exception:
    EZKL_AVAILABLE = False
