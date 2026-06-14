const vscode = require("vscode");
const { execSync } = require("child_process");
const path = require("path");

function getRepoRoot() {
  const ext = vscode.extensions.getExtension("mlops-platform.mlops-agent-skills");
  if (ext) return path.resolve(ext.extensionPath, "..");
  return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || process.cwd();
}

function runInstall(tool, target) {
  const root = getRepoRoot();
  const script = path.join(root, "scripts", "install_toolkit.py");
  execSync(`python "${script}" --tool ${tool} --target "${target}"`, {
    cwd: root,
    stdio: "inherit",
  });
}

function activate(context) {
  const target = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!target) return;

  context.subscriptions.push(
    vscode.commands.registerCommand("mlopsSkills.installFull", () => {
      runInstall("all", target);
      vscode.window.showInformationMessage("MLOps Full Toolkit installed.");
    }),
    vscode.commands.registerCommand("mlopsSkills.installCore", () => {
      runInstall("generic", target);
      vscode.window.showInformationMessage("MLOps Core Pack installed.");
    }),
    vscode.commands.registerCommand("mlopsSkills.installAdapters", () => {
      runInstall("cursor,claude,copilot", target);
      vscode.window.showInformationMessage("MLOps Agent Adapters installed.");
    }),
    vscode.commands.registerCommand("mlopsSkills.installStarter", () => {
      runInstall("generic", target);
      vscode.window.showInformationMessage("Starter pack files installed.");
    }),
    vscode.commands.registerCommand("mlopsSkills.scaffoldExample", () => {
      runInstall("generic", target);
      vscode.window.showInformationMessage("Example scaffold installed.");
    })
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
