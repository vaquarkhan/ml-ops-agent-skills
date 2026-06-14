#!/usr/bin/env python3
"""Install MLOps agent toolkit files into another project."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CORE_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    "skills-index.md",
    "registry/assets.json",
    "templates",
    "hooks",
    "skills",
    "presets",
    "starter-packs",
    "references",
    "examples",
    "tutorials",
    "docs/getting-started.md",
    "docs/cursor-setup.md",
    "docs/jetbrains-setup.md",
    "docs/claude-setup.md",
    "docs/copilot-setup.md",
    "bootstrap.sh",
    "bootstrap.ps1",
]

TOOL_PATHS = {
    "cursor": [".cursor/rules"],
    "claude": [".claude/commands", "AGENTS.md", "CLAUDE.md"],
    "copilot": [".github/copilot-instructions.md", "AGENTS.md"],
    "generic": CORE_PATHS,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install MLOps agent toolkit into a project.")
    parser.add_argument("--tool", required=True, help="Tool name, comma-separated, or: auto, all")
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def copy_path(relative_path: str, target_root: Path, force: bool) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        return
    if source.is_file():
        dest = target_root / relative_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and not force:
            print(f"Skipping: {dest}")
            return
        shutil.copy2(source, dest)
        print(f"Installed: {dest}")
        return
    dest_root = target_root / relative_path
    for src_file in source.rglob("*"):
        if src_file.is_file():
            rel = src_file.relative_to(source)
            dest = dest_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() and not force:
                continue
            shutil.copy2(src_file, dest)
            print(f"Installed: {dest}")


def main() -> int:
    args = parse_args()
    target = args.target.resolve()
    target.mkdir(parents=True, exist_ok=True)

    tools = args.tool.split(",") if args.tool not in ("all", "auto") else ["all"]
    paths: list[str] = list(CORE_PATHS)
    if "all" in tools or args.tool == "all":
        for tool_paths in TOOL_PATHS.values():
            paths.extend(tool_paths)
    else:
        for t in tools:
            paths.extend(TOOL_PATHS.get(t.strip(), []))

    seen: set[str] = set()
    for p in paths:
        if p not in seen:
            seen.add(p)
            copy_path(p, target, args.force)

    print("MLOps toolkit install complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
