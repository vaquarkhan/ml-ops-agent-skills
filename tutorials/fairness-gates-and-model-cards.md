# Fairness Gates and Model Cards

## Goal

Enforce demographic parity ≤ 0.05 before promotion.

## Steps

1. `GovernancePipeline.compute_fairness_metrics(...)`.
2. `enforce_fairness_gate(metrics)`.
3. `generate_model_card(...)` → markdown artifact.

Skill: `skills/responsible-ai-and-model-governance/SKILL.md`
