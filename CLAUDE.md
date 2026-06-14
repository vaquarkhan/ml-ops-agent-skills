# Claude Entry Point

This repository uses the same agent skill layout as [data-engineering-agent-skills](https://github.com/vaquarkhan/data-engineering-agent-skills).

## Start Here

1. Read `skills/using-mlops-agent-skills/SKILL.md`
2. Load the matching preset from `presets/`
3. Load task-specific skills only when needed
4. Use lifecycle commands: `/spec`, `/plan`, `/build`, `/validate`, `/review`, `/retrain`, `/ship`

## Slash Commands

Map these to Claude commands in `.claude/commands/` when installed:

| Command | Purpose |
|---------|---------|
| `/spec` | Define contracts, schemas, SLAs |
| `/plan` | Task breakdown |
| `/build` | Implement changes |
| `/validate` | Run tests, drift, fairness gates |
| `/review` | Reliability and governance review |
| `/retrain` | Safe retraining workflow |
| `/ship` | Deploy with rollback path |

See `AGENTS.md` for full routing and guardrails.
