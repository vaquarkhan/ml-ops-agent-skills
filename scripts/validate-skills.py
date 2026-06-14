#!/usr/bin/env python3
"""Validate MLOps agent skill markdown structure and IDE command surfaces."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MIN_SKILL_LINES = 80

REQUIRED_SKILL_SECTIONS = [
    "## Overview",
    "## When to Use",
    "## Workflow",
    "## Common Rationalizations",
    "## Red Flags",
    "## Verification",
]

LIFECYCLE_COMMANDS = ["spec", "plan", "build", "validate", "review", "retrain", "ship"]


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["missing opening YAML frontmatter delimiter"]
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, ["missing closing YAML frontmatter delimiter"]
    metadata: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, errors


def validate_skill_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    expected_name = path.parent.name
    metadata, fm_errors = parse_frontmatter(text)
    errors.extend(fm_errors)

    if metadata.get("name") != expected_name:
        errors.append(f"name frontmatter must match directory '{expected_name}'")
    elif not SKILL_NAME_PATTERN.fullmatch(expected_name):
        errors.append("name must be lowercase hyphen-separated")

    description = metadata.get("description", "")
    if not description:
        errors.append("missing description frontmatter")
    elif "use when" not in description.lower() and "use for" not in description.lower():
        errors.append("description should explain when to use the skill")
    elif len(description.split()) < 8:
        errors.append("description too short for progressive disclosure")

    for section in REQUIRED_SKILL_SECTIONS:
        if section not in text:
            errors.append(f"missing section '{section}'")

    line_count = len(text.splitlines())
    if line_count < MIN_SKILL_LINES:
        errors.append(f"skill too thin ({line_count} lines, minimum {MIN_SKILL_LINES})")

    return errors


def validate_command_surfaces() -> list[str]:
    errors: list[str] = []
    for command_dir in [ROOT / ".claude" / "commands", ROOT / ".gemini" / "commands"]:
        if not command_dir.exists():
            errors.append(f"missing command directory: {command_dir}")
            continue
        for name in LIFECYCLE_COMMANDS:
            if not (command_dir / f"{name}.md").exists():
                errors.append(f"missing command file: {command_dir / name}.md")
    kiro_dir = ROOT / ".kiro" / "steering"
    if not (kiro_dir / "mlops-agent-skills.md").exists():
        errors.append(f"missing Kiro steering file: {kiro_dir / 'mlops-agent-skills.md'}")
    return errors


def main() -> int:
    all_errors: list[str] = []
    skills = sorted(ROOT.glob("skills/*/SKILL.md"))
    for skill_file in skills:
        for error in validate_skill_file(skill_file):
            all_errors.append(f"{skill_file}: {error}")

    all_errors.extend(validate_command_surfaces())

    if all_errors:
        print("Validation failed:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(skills)} skills and lifecycle command surfaces.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
