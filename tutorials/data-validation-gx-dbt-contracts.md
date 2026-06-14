# Data Validation with GX and dbt Contracts

## Goal

Halt poisoned data before Feast or training consumption.

## Steps

1. Review `data/dbt/models/schema.yml` contract.
2. Extend GX suite in `data/expectations/build_suite.py`.
3. Run `pytest tests/test_data_validation.py -v`.

Skill: `skills/data-validation-and-contract-testing/SKILL.md`
