---
name: data-validation-and-contract-testing
description: Validates upstream data with Great Expectations and dbt contracts. Use for ingestion pipelines, schema drift detection, volume anomalies, and halting bad data before feature store or training consumption.
---

# Data Validation and Contract Testing

## Overview

Enforce upstream data quality before any downstream ML consumption using Great Expectations expectation suites and dbt data contracts.

## When to Use

- building or modifying raw ingestion pipelines
- detecting schema drift or volume anomalies
- defining dbt contract YAML for downstream tables
- writing tests that halt on poisoned data streams

## Workflow

1. Define the raw schema contract in `data/dbt/models/schema.yml`.
2. Build or extend the GX suite in `data/expectations/build_suite.py`.
3. Wire validation into `data/ingestion_pipeline.py` — pipeline must halt on failure.
4. Add pytest cases for valid and poisoned streams in `tests/test_data_validation.py`.
5. Run `pytest tests/test_data_validation.py -v`.

## Implementation References

- Pipeline: `data/ingestion_pipeline.py`
- GX config: `data/great_expectations/great_expectations.yml`
- dbt contract: `data/dbt/models/schema.yml`

## Verification

- [ ] GX suite includes schema, null, range, and volume checks
- [ ] dbt contract enforced on validated models
- [ ] Poisoned data tests assert pipeline halt with `DataValidationError`
- [ ] No placeholder or TODO logic in validation paths
