# Claude Setup

Use Claude with this repository via plugin bundle, commands, or copied skills.

## Recommended Setup

1. Clone the repository.
2. Install agent adapters:

```bash
scripts/install.sh --tool claude --target /path/to/project
```

3. Start sessions with `CLAUDE.md` and `skills/using-mlops-agent-skills/SKILL.md`.

## Included Surfaces

- `.claude/commands/` — slash command mappings (when installed)
- `.claude-plugin/` — plugin manifest (when present)
- `CLAUDE.md` — repository entry point
- `AGENTS.md` — generic agent routing

## Lifecycle Commands

Map user intent to:

| Command | Skill focus |
|---------|-------------|
| `/spec` | Contracts, schemas, SLAs |
| `/validate` | Tests, drift, fairness gates |
| `/ship` | Serving manifests, rollback |

See [AGENTS.md](../AGENTS.md) for full routing table.
