# Contributing to MLOps Agent Skills

Thank you for contributing. This repository combines **agent workflow skills** with a **runnable MLOps platform** — contributions should improve both.

## Before You Start

1. Read `skills/using-mlops-agent-skills/SKILL.md`
2. Check `skills-index.md` for existing coverage
3. Run validation locally:

```bash
python scripts/validate-skills.py
python scripts/validate-assets.py
pytest tests/ -v
```

## Skill Contributions

Every skill must:

- Live in `skills/<skill-name>/SKILL.md`
- Include YAML frontmatter with `name` and `description` (description must explain **when to use**)
- Include sections: Overview, When to Use, Workflow, Common Rationalizations, Red Flags, Verification
- Be **80+ lines** with decision frameworks and anti-patterns
- Map to runnable code or references where applicable

Run `python scripts/validate-skills.py` before opening a PR.

## Code Contributions

- Follow PEP 8 with type hints and docstrings
- No placeholder implementations (`pass`, `# TODO`, `...`)
- Add pytest coverage for new behavior
- Use skip guards for optional heavy dependencies (torch, feast, great_expectations, ezkl)
- Keep diffs focused — do not refactor unrelated code

## Pull Request Checklist

- [ ] `validate-skills.py` passes
- [ ] `validate-assets.py` passes
- [ ] `pytest` passes (or skipped tests documented)
- [ ] `CHANGELOG.md` updated under `[Unreleased]` or new version
- [ ] `VERSION` bumped if releasing
- [ ] No secrets or credentials in diff
- [ ] Reference provenance added for new domain checklists

## Commit Messages

Write clear, imperative commit messages focused on **why**:

```
Add drift detection starter pack for production monitoring workflows.
```

Do not include tool or vendor attribution lines in commit messages.

## Code of Conduct

Be respectful, specific, and grounded in real MLOps practice. Reject contributions that skip validation, governance, or reproducibility without documented justification.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
