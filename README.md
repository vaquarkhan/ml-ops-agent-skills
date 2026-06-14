<p align="center">
  <img src="https://raw.githubusercontent.com/vaquarkhan/ml-ops-agent-skills/main/images/banner.jpg" alt="MLOps Agent Skills" width="900" />
</p>

# MLOps Agent Skills

Production-grade agent skills and a runnable MLOps platform for AI agents covering the full ML lifecycle: data validation, feature store, GPU training, model registry, LLM serving, monitoring, verifiable AI, and responsible AI governance.

> Pattern aligned with [data-engineering-agent-skills](https://github.com/vaquarkhan/data-engineering-agent-skills): skills registry, platform presets, VS Code/JetBrains installers, and multi-agent packaging.

## Agent Skills Registry Compatibility

- Every capability lives in a directory containing a `SKILL.md`
- Each `SKILL.md` starts with YAML frontmatter (`name`, `description`)
- Supporting materials live in `references/`, `templates/`, `examples/`, `hooks/`, and `scripts/`

## Quick Start

```bash
git clone https://github.com/vaquarkhan/ml-ops-agent-skills.git
cd ml-ops-agent-skills

# Install skills into another project
scripts/install.sh --tool all --target /path/to/project

# Windows
pwsh scripts/install.ps1 --tool all --target C:\path\to\project

# Run platform tests (lightweight local dev — no torch/feast/GX)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-minimal.txt
pytest tests/ -v

# Full platform suite (Linux CI or after installing optional deps)
pip install -r requirements.txt
pytest tests/ -v
```

Bootstrap shortcuts:

```bash
./bootstrap.sh /path/to/project auto
pwsh .\bootstrap.ps1 C:\path\to\project auto
```

## Start Here

1. Load `skills/using-mlops-agent-skills/SKILL.md`
2. Pick the closest platform preset from `presets/`
3. Use runnable platform code at repo root or an example from `examples/`

## Install Surfaces

| Tool | Guide | Install |
|------|-------|---------|
| **Cursor** | [docs/cursor-setup.md](docs/cursor-setup.md) | `scripts/install.sh --tool cursor` |
| **VS Code / Cursor / Windsurf** | [vscode-extension/README.md](vscode-extension/README.md) | VSIX or Command Palette |
| **JetBrains** | [docs/jetbrains-setup.md](docs/jetbrains-setup.md) | Marketplace or Plugin from Disk |
| **Claude** | [docs/claude-setup.md](docs/claude-setup.md) | `scripts/install.sh --tool claude` |
| **Copilot** | [docs/copilot-setup.md](docs/copilot-setup.md) | `scripts/install.sh --tool copilot` |
| **Generic AGENTS.md** | [AGENTS.md](AGENTS.md) | `scripts/install.sh --tool all` |

### VS Code / Cursor — Install from VSIX

1. Download `.vsix` from Releases
2. `Ctrl+Shift+P` → **Extensions: Install from VSIX...**
3. Reload editor
4. Command Palette → **MLOps Skills: Install Full Toolkit**

### JetBrains — Install from Disk

1. Download `.zip` from Releases
2. **Settings → Plugins → Install Plugin from Disk...**
3. Restart IDE
4. **Tools → MLOps Agent Skills**

See [tutorials/installing-vscode-and-jetbrains-plugins.md](tutorials/installing-vscode-and-jetbrains-plugins.md).

## Lifecycle Commands

| Command | Purpose |
|---------|---------|
| `/spec` | Model contract, feature schema, SLA, lineage |
| `/plan` | Atomic task breakdown |
| `/build` | Incremental implementation |
| `/validate` | Tests, drift, fairness gates |
| `/review` | Reliability, governance, cost |
| `/retrain` | Safe retraining and feature backfill |
| `/ship` | Deploy with rollback path |

## Skills Pack (9 workflows)

| Skill | Domain |
|-------|--------|
| [using-mlops-agent-skills](skills/using-mlops-agent-skills/SKILL.md) | Triage and routing |
| [data-validation-and-contract-testing](skills/data-validation-and-contract-testing/SKILL.md) | GX + dbt |
| [feast-feature-store-engineering](skills/feast-feature-store-engineering/SKILL.md) | Feast PIT joins |
| [distributed-gpu-training-and-scheduling](skills/distributed-gpu-training-and-scheduling/SKILL.md) | Volcano + K8s |
| [mlflow-model-registry-and-continuous-training](skills/mlflow-model-registry-and-continuous-training/SKILL.md) | MLflow UC |
| [llm-serving-and-inference-optimization](skills/llm-serving-and-inference-optimization/SKILL.md) | KServe + vLLM |
| [model-monitoring-and-drift-detection](skills/model-monitoring-and-drift-detection/SKILL.md) | Evidently PSI |
| [verifiable-ai-and-zkml](skills/verifiable-ai-and-zkml/SKILL.md) | EZKL proofs |
| [responsible-ai-and-model-governance](skills/responsible-ai-and-model-governance/SKILL.md) | Fairlearn |

Full catalog: [skills-index.md](skills-index.md)

## Platform Presets

- [kubernetes-gpu-mlops](presets/kubernetes-gpu-mlops.yaml) — K8s, Volcano, KServe, Feast
- [databricks-unity-catalog-mlops](presets/databricks-unity-catalog-mlops.yaml) — UC, MLflow
- [aws-sagemaker-mlops](presets/aws-sagemaker-mlops.yaml) — SageMaker, S3, GX
- [gcp-vertex-mlops](presets/gcp-vertex-mlops.yaml) — Vertex AI, BigQuery

## Runnable Platform Code

| Module | Path |
|--------|------|
| Data validation | `data/` |
| Feature store | `feature_store/` |
| Training + MLflow | `training/` |
| LLM serving | `serving/` |
| Drift monitoring | `monitoring/` |
| zkML | `zkml/` |
| Governance | `governance/` |
| Kubernetes | `k8s/` |
| Tests | `tests/` |

## Project Structure

```
ml-ops-agent-skills/
├── skills/              # Workflow SKILL.md definitions
├── presets/             # Platform operating profiles
├── references/          # Checklists
├── templates/           # Contracts and release gates
├── examples/            # Runnable + blueprint packs
├── docs/                # Cursor, JetBrains, Claude setup
├── tutorials/           # Long-form walkthroughs
├── vscode-extension/    # VS Code family installer
├── jetbrains-plugin/    # JetBrains installer scaffold
├── hooks/               # Pre-flight guards
├── scripts/             # install.sh, install.ps1
├── registry/            # assets.json index
├── data/                # Runnable: GX + dbt
├── feature_store/       # Runnable: Feast
├── training/            # Runnable: PyTorch + MLflow
├── serving/             # Runnable: KServe + load test
├── monitoring/          # Runnable: Evidently
├── zkml/                # Runnable: EZKL
└── governance/          # Runnable: Fairlearn
```

## Multi-Agent Packaging

- `.cursor/rules/` — Cursor project rules
- `.claude/commands/` — Claude Code lifecycle commands
- `.gemini/commands/` — Gemini CLI lifecycle commands
- `.kiro/steering/` — Kiro steering docs
- `.github/copilot-instructions.md` — GitHub Copilot
- `AGENTS.md` — Generic agent entry
- `CLAUDE.md` — Claude entry

## Governance and Quality

| Asset | Purpose |
|-------|---------|
| [LICENSE](LICENSE) | Apache-2.0 |
| [CHANGELOG](CHANGELOG.md) | Release history |
| [VERSION](VERSION) | Current semver |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guide |
| `scripts/validate-skills.py` | Skill structure CI gate |
| `scripts/validate-assets.py` | Registry path verification |
| `evals/run.py` | Skill routing benchmark (≥70%) |
| `.pre-commit-config.yaml` | Local lint hooks |
| `.github/dependabot.yml` | Dependency updates |

**Starter packs:** 7 · **Tutorials:** 10 · **Reference checklists:** 5 (with provenance)

## Documentation

- [docs/getting-started.md](docs/getting-started.md)
- [docs/cursor-setup.md](docs/cursor-setup.md)
- [docs/jetbrains-setup.md](docs/jetbrains-setup.md)
- [tutorials/installing-vscode-and-jetbrains-plugins.md](tutorials/installing-vscode-and-jetbrains-plugins.md)

## License

Apache-2.0 — see [LICENSE](LICENSE). Version **1.1.1** ([CHANGELOG](CHANGELOG.md)).

Inspired by [vaquarkhan/data-engineering-agent-skills](https://github.com/vaquarkhan/data-engineering-agent-skills).
