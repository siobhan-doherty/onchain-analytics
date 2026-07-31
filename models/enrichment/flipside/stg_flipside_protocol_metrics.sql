{{ config(materialized = "table") }}

SELECT
    TRY_CAST(protocol_id AS TEXT) AS protocol_id,
    TRY_CAST(protocol_name AS TEXT) AS protocol_name,
    TRY_CAST(protocol_slug AS TEXT) AS protocol_slug,
    TRY_CAST(blockchain AS TEXT) AS blockchain,
    TRY_CAST(category AS TEXT) AS category,
    TRY_CAST(date AS DATE) AS date,
    TRY_CAST(tvl_usd AS DOUBLE) AS tvl_usd,
    TRY_CAST(volume_usd AS DOUBLE) AS volume_usd,
    TRY_CAST(revenue_usd AS DOUBLE) AS revenue_usd,
    TRY_CAST(fees_usd AS DOUBLE) AS fees_usd,
    TRY_CAST(unique_users AS BIGINT) AS unique_users,
    TRY_CAST(tx_count AS BIGINT) AS tx_count,
    TRY_CAST(active_users AS BIGINT) AS active_users,
    TRY_CAST(new_users AS BIGINT) AS new_users,
    TRY_CAST(last_updated AS TIMESTAMP) AS last_updated
FROM {{ source("flipside", "raw_flipside_protocol_metrics") }}
WHERE protocol_id IS NOT NULL
    AND date IS NOT NULL
