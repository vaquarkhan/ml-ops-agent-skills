# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-14

### Added

- Apache-2.0 `LICENSE`, `VERSION`, `SECURITY.md`, `CONTRIBUTING.md`
- `scripts/validate-skills.py` and `scripts/validate-assets.py` with CI wiring
- `.pre-commit-config.yaml` and `.github/dependabot.yml`
- Multi-IDE adapters: `.claude/commands/`, `.gemini/commands/`, `.kiro/steering/`
- Deepened workflow skills (decision frameworks, anti-patterns, verification)
- Six additional starter packs and ten tutorials
- Reference provenance headers for domain trust
- `evals/run.py` benchmark harness for skill routing coverage
- Test skip guards for PyTorch, Feast, Great Expectations, and EZKL dependencies
- `requirements-minimal.txt` for lightweight local development

### Changed

- README banner optimized for GitHub rendering (`images/banner.jpg`)
- CI pipeline validates skills, assets, and runs lightweight test profile

## [1.0.0] - 2026-06-14

### Added

- Initial MLOps agent skills registry (9 workflow skills)
- Runnable platform: data validation, Feast, GPU training, MLflow, KServe, drift, zkML, governance
- Platform presets, install scripts, VS Code and JetBrains scaffolds
- pytest suite with ~95% coverage on core modules

[1.1.0]: https://github.com/vaquarkhan/ml-ops-agent-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/vaquarkhan/ml-ops-agent-skills/releases/tag/v1.0.0
