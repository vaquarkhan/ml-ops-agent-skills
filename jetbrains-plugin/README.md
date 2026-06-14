# MLOps Agent Skills — JetBrains Plugin

Install MLOps agent skills into the current project from IntelliJ-platform IDEs.

## Supported IDEs

- IntelliJ IDEA
- PyCharm
- DataGrip
- WebStorm
- GoLand

## Menu Actions (planned)

- **Tools → MLOps Agent Skills → Install Full Toolkit**
- **Tools → MLOps Agent Skills → Install Core Pack**
- **Tools → MLOps Agent Skills → Install Agent Adapters**

## Manual Install

1. Download plugin `.zip` from GitHub Releases
2. **Settings → Plugins → Install Plugin from Disk...**
3. Restart IDE

## Script Alternative

```powershell
pwsh scripts/install.ps1 --tool all --target C:\path\to\project
```

## Plugin Source

Kotlin plugin scaffold — implement `InstallToolkitAction` calling `scripts/install_toolkit.py`.

See [../docs/jetbrains-setup.md](../docs/jetbrains-setup.md).
