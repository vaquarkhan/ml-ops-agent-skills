# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue for exploitable vulnerabilities.
2. Email the maintainer via GitHub private vulnerability reporting, or open a
   **Security Advisory** on the repository.
3. Include: affected module, reproduction steps, impact assessment, and suggested fix if available.

We aim to acknowledge reports within **72 hours** and provide a remediation plan within **14 days** for confirmed issues.

## Scope

In scope:

- Python platform code (`data/`, `training/`, `serving/`, `monitoring/`, `zkml/`, `governance/`)
- Install scripts and CI workflows
- VS Code / JetBrains extension scaffolds
- Credential handling in examples and templates

Out of scope:

- Third-party services (Databricks, AWS, GCP) misconfiguration in user environments
- Custom forks that modify security-sensitive defaults

## Secure Development

- Never commit secrets (`.env`, keys, tokens) — see `.gitignore`
- Run `pre-commit` hooks before pushing
- Dependabot monitors GitHub Actions and pip dependencies
- Fairness and drift CI gates block unsafe model promotion paths

## Hardening Checklist for Deployments

- [ ] Rotate MLflow and Unity Catalog credentials regularly
- [ ] Restrict K8s GPU job RBAC to training namespaces
- [ ] Enable network policies on inference endpoints
- [ ] Audit Model Cards before production promotion
- [ ] Verify zkML proof keys are not exposed in public artifacts
