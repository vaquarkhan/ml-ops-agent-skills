# Getting Started

Production-grade MLOps agent skills plus a runnable platform implementation.

## Quick Start

1. Clone this repository.
2. Load `skills/using-mlops-agent-skills/SKILL.md`.
3. Pick a preset from `presets/`.
4. Install into your project (optional):

```bash
./scripts/install.sh --tool all --target /path/to/project
```

Windows:

```powershell
pwsh scripts/install.ps1 --tool all --target C:\path\to\project
```

5. Bootstrap shortcuts:

```bash
./bootstrap.sh /path/to/project auto
pwsh .\bootstrap.ps1 C:\path\to\project auto
```

## Run the Platform

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest tests/ -v
python training/validate_k8s.py
```

## Install Surfaces

| Tool | Guide |
|------|-------|
| Cursor | [cursor-setup.md](cursor-setup.md) |
| VS Code / Cursor / Windsurf | [../vscode-extension/README.md](../vscode-extension/README.md) |
| JetBrains | [jetbrains-setup.md](jetbrains-setup.md) |
| Claude | [claude-setup.md](claude-setup.md) |
| Copilot | [copilot-setup.md](copilot-setup.md) |
| Codex / AGENTS.md | [AGENTS.md](../AGENTS.md) |

## Repository Layout

```
skills/           Workflow SKILL.md definitions
presets/          Platform operating profiles
docs/             Setup and onboarding guides
examples/         Runnable scaffolds and blueprints
references/       Checklists and decision guides
templates/        Contract and release templates
platform/         (root modules: data/, training/, serving/, ...)
scripts/          Install and validation helpers
vscode-extension/ VS Code family installer
jetbrains-plugin/ JetBrains installer scaffold
```

The runnable platform code lives at the repository root (`data/`, `feature_store/`, `training/`, etc.).
