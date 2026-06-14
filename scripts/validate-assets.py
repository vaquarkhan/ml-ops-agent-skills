#!/usr/bin/env python3
"""Validate registry/assets.json paths and preset file existence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    registry_path = ROOT / "registry" / "assets.json"
    if not registry_path.exists():
        print(f"Missing registry: {registry_path}")
        return 1

    data = json.loads(registry_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    for skill in data.get("skills", []):
        path = ROOT / skill["path"]
        if not path.exists():
            errors.append(f"skill path missing: {skill['path']}")
        if skill.get("name") != path.parent.name:
            errors.append(f"skill name mismatch: {skill.get('name')} vs {path.parent.name}")

    for preset in data.get("presets", []):
        if not (ROOT / preset).exists():
            errors.append(f"preset missing: {preset}")

    for pack in data.get("starter_packs", []):
        if not (ROOT / pack).exists():
            errors.append(f"starter pack missing: {pack}")

    for example in data.get("examples", []):
        if not (ROOT / example).exists():
            errors.append(f"example missing: {example}")

    for module in data.get("platform_modules", []):
        if not (ROOT / module).is_dir():
            errors.append(f"platform module missing: {module}")

    version_file = ROOT / "VERSION"
    if version_file.exists():
        version = version_file.read_text(encoding="utf-8").strip()
        if data.get("version") != version:
            errors.append(f"registry version {data.get('version')} != VERSION file {version}")

    if errors:
        print("Asset validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print(
        f"Validated registry: {len(data.get('skills', []))} skills, "
        f"{len(data.get('presets', []))} presets, "
        f"{len(data.get('starter_packs', []))} starter packs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
