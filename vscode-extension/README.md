# MLOps Agent Skills for VS Code Family

Install the MLOps agent skill pack into the current workspace.

Compatible editors:

- VS Code
- Cursor
- Windsurf
- VSCodium

## Commands

- **MLOps Skills: Install Full Toolkit**
- **MLOps Skills: Install Core Pack**
- **MLOps Skills: Install Agent Adapters**
- **MLOps Skills: Install Starter Pack**
- **MLOps Skills: Scaffold Runnable Example**

## Manual VSIX Install

1. Download `.vsix` from GitHub Releases
2. `Ctrl+Shift+P` → **Extensions: Install from VSIX...**
3. Reload editor
4. Run commands from Command Palette

## Script Alternative

```bash
scripts/install.sh --tool all --target .
pwsh scripts/install.ps1 --tool all --target .
```

## What It Installs

- `AGENTS.md`, `CLAUDE.md`, `skills-index.md`
- `skills/`, `presets/`, `references/`, `templates/`
- `.cursor/rules/` agent adapters
- `examples/`, `starter-packs/`

## Local Development

1. Open `vscode-extension/` in VS Code
2. Press `F5` to launch Extension Development Host
3. Run install commands in a test workspace

See [../tutorials/installing-vscode-and-jetbrains-plugins.md](../tutorials/installing-vscode-and-jetbrains-plugins.md).
