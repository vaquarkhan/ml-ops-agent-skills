# Cursor Setup

Use this repository in Cursor by referencing skills and supporting docs as project rules.

## Recommended Setup

1. Clone the repository locally.
2. Choose whether you want:
   - a subset of skills copied into `.cursor/rules/`, or
   - this repository referenced as the source for shared rule content
3. Start with:
   - `skills/using-mlops-agent-skills/SKILL.md`
   - the stack preset under `presets/`
   - task-specific skills such as `feast-feature-store-engineering` or `llm-serving-and-inference-optimization`

## One-Line Install

```bash
scripts/install.sh --tool cursor --target /path/to/project
```

Windows:

```powershell
pwsh scripts/install.ps1 --tool cursor --target C:\path\to\project
```

## Suggested Project Rule Flow

1. Load `using-mlops-agent-skills`.
2. Load the relevant preset such as `kubernetes-gpu-mlops` or `databricks-unity-catalog-mlops`.
3. Load workflow-specific skills only when the task needs them.
4. Load checklist references for review or release readiness.

## Tips

- Avoid loading every skill at once.
- Keep project-specific policies in your own repo; use this repository for reusable workflow logic.
- Prefer referencing templates and examples when starting new ML products.
- Run hooks from `hooks/` for risky work (schema change, release, retrain).

## VS Code Extension (Cursor Compatible)

Cursor supports the VS Code extension family. Install from:

- Command Palette → `Extensions: Install from VSIX...` (see Releases)
- Or run `MLOps Skills: Install Full Toolkit` after installing the extension

See [../vscode-extension/README.md](../vscode-extension/README.md) and [../tutorials/installing-vscode-and-jetbrains-plugins.md](../tutorials/installing-vscode-and-jetbrains-plugins.md).
