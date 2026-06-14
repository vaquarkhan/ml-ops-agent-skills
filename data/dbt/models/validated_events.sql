{{
    config(
        materialized='table',
        contract={'enforced': true}
    )
}}

SELECT
    CAST(user_id AS BIGINT) AS user_id,
    CAST(event_timestamp AS TIMESTAMP) AS event_timestamp,
    CAST(feature_a AS DOUBLE) AS feature_a,
    CAST(feature_b AS DOUBLE) AS feature_b,
    CAST(feature_c AS DOUBLE) AS feature_c,
    CAST(label AS INTEGER) AS label,
    CURRENT_TIMESTAMP AS ingested_at
FROM {{ source('raw', 'events') }}
