# GitHub Copilot Setup

Install Copilot instructions from this repository.

## Install

```bash
scripts/install.sh --tool copilot --target /path/to/project
```

This copies `.github/copilot-instructions.md` and core entry files.

## Usage

Copilot reads `.github/copilot-instructions.md` in the target project. Ensure it references:

1. `skills/using-mlops-agent-skills/SKILL.md`
2. The active platform preset
3. Task-specific skills for the current change

See [AGENTS.md](../AGENTS.md) for lifecycle commands and guardrails.
