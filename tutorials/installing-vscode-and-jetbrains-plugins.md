# Installing VS Code and JetBrains Plugins

Walkthrough for installing MLOps Agent Skills into VS Code family editors and JetBrains IDEs.

## VS Code Family (VS Code, Cursor, Windsurf, VSCodium)

### From Marketplace (when published)

1. Open Extensions panel (`Ctrl+Shift+X`)
2. Search **MLOps Agent Skills**
3. Click Install
4. Reload the editor

### From VSIX (manual)

1. Download `.vsix` from GitHub Releases
2. `Ctrl+Shift+P` → **Extensions: Install from VSIX...**
3. Select the downloaded file
4. Reload when prompted
5. `Ctrl+Shift+P` → search **MLOps Skills:** for commands

### Commands

- **MLOps Skills: Install Full Toolkit**
- **MLOps Skills: Install Core Pack**
- **MLOps Skills: Install Agent Adapters**
- **MLOps Skills: Install Starter Pack**
- **MLOps Skills: Scaffold Runnable Example**

## JetBrains (IntelliJ, PyCharm, DataGrip)

### From Marketplace (when published)

1. **Settings** → **Plugins** → **Marketplace**
2. Search **MLOps Agent Skills**
3. Install and restart

### From Disk

1. Download `.zip` from Releases
2. **Settings** → **Plugins** → gear → **Install Plugin from Disk...**
3. Restart IDE
4. **Tools** → **MLOps Agent Skills** menu

## Script Install (all tools)

```bash
scripts/install.sh --tool all --target /path/to/project
pwsh scripts/install.ps1 --tool all --target C:\path\to\project
```

## Verify

After install, confirm these exist in your project:

- `AGENTS.md`
- `skills-index.md`
- `skills/using-mlops-agent-skills/SKILL.md`

Run platform tests:

```bash
pip install -r requirements.txt
pytest tests/ -v
```
