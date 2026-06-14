# JetBrains Setup

Use the plugin scaffold in `jetbrains-plugin/` to install the MLOps skill pack into IntelliJ-platform IDEs.

Supported IDE families:

- IntelliJ IDEA
- PyCharm
- DataGrip
- WebStorm
- GoLand

## Recommended Flow

1. Build or run the plugin from `jetbrains-plugin/`
2. Open the target project in a JetBrains IDE
3. Use the **Tools** menu:
   - Install Full Toolkit
   - Install Core Pack
   - Install Agent Adapters
   - Install Starter Pack
   - Scaffold Runnable Example

## Manual Install from Disk

1. Download the `.zip` plugin from GitHub Releases (when published)
2. Open your IDE → **Settings** → **Plugins** → gear icon → **Install Plugin from Disk...**
3. Select the downloaded `.zip`
4. Restart the IDE

## What Gets Installed

- `AGENTS.md`
- `skills-index.md`
- `skills/` workflow definitions
- `presets/` platform profiles
- `references/` and `templates/`
- agent adapter files for supported tools

## Notes

- The plugin installs repository assets into the **current project**, not the IDE globally
- Complements `scripts/install.ps1` and the VS Code family extension

## Next Step

- [../tutorials/installing-vscode-and-jetbrains-plugins.md](../tutorials/installing-vscode-and-jetbrains-plugins.md)
- [../jetbrains-plugin/README.md](../jetbrains-plugin/README.md)
