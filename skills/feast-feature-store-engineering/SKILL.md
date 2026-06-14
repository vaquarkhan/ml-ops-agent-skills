---
name: feast-feature-store-engineering
description: Implements Feast feature stores with offline Parquet and online Redis retrieval. Use for feature definitions, point-in-time correct training datasets, and eliminating training-serving skew.
---

# Feast Feature Store Engineering

## Overview

Define entities and feature views, materialize offline/online stores, and build point-in-time correct training datasets that prevent target leakage.

## When to Use

- creating or updating Feast feature definitions
- implementing historical feature retrieval for training
- verifying online feature freshness for inference
- debugging training-serving skew

## Workflow

1. Define entities and feature views in `feature_store/feature_repo/features.py`.
2. Configure offline/online stores in `feature_store/feature_repo/feature_store.yaml`.
3. Implement PIT retrieval in `feature_store/retrieval.py` using `get_historical_features`.
4. Generate sample data with `feature_store/feature_repo/generate_sample_data.py`.
5. Run integration tests in `tests/test_feature_store.py`.

## Verification

- [ ] At least one Entity and two FeatureViews (batch offline + online realtime)
- [ ] Point-in-time join validated — no future feature leakage
- [ ] Online retrieval tested with mocked Redis
- [ ] Feature freshness checks documented
