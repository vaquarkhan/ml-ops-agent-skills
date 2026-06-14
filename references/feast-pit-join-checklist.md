# Feast Point-in-Time Join Checklist

> **Provenance:** Feast project documentation (point-in-time joins); ML feature store best practices (Tecton, Databricks); internal MLOps platform patterns v1.1.

- [ ] Entity DataFrame has `user_id` and `event_timestamp`
- [ ] Feature views use correct `timestamp_field` and `created_timestamp_column`
- [ ] Offline batch features do not leak future labels
- [ ] Online features materialized to Redis with TTL configured
- [ ] Historical retrieval uses `get_historical_features`, not latest snapshot
- [ ] Training dataset validated for join mismatches
- [ ] Feature column null rates documented and handled
