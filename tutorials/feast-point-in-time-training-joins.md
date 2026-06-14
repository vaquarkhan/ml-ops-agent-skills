# Feast Point-in-Time Training Joins

## Goal

Build training datasets without target leakage.

## Steps

1. Define entity_df with `user_id` + `event_timestamp`.
2. Call `build_training_dataset(entity_df)` in `feature_store/retrieval.py`.
3. Verify `_validate_no_leakage` passes.

Skill: `skills/feast-feature-store-engineering/SKILL.md`
