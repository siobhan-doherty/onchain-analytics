{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "token_id"},
            {"name": "unique", "column": "token_id"},
            {"name": "not_null", "column": "token_symbol"},
            {"name": "not_null", "column": "token_address"}
        ]
    }
) }}

WITH token_stats AS (
    SELECT
        token_symbol,
        token_address,
        COUNT(*) AS transfer_count,
        SUM(amount) AS total_transferred,
        SUM(amount_usd) AS total_volume_usd,
        COUNT(DISTINCT from_address) AS unique_senders,
        COUNT(DISTINCT to_address) AS unique_recipients,
        MIN(block_time) AS first_transfer_time,
        MAX(block_time) AS last_transfer_time
    FROM {{ ref("stg_token_transfers") }}
    GROUP BY token_symbol, token_address
)
SELECT
    ROW_NUMBER() OVER (ORDER BY total_volume_usd DESC, transfer_count DESC) AS token_id,
    token_symbol,
    token_address,
    transfer_count,
    total_transferred,
    total_volume_usd,
    unique_senders,
    unique_recipients,
    first_transfer_time,
    last_transfer_time,
    DATE_TRUNC('day', COALESCE(first_transfer_time, CURRENT_TIMESTAMP)) AS first_transfer_date,
    DATE_TRUNC('day', COALESCE(last_transfer_time, CURRENT_TIMESTAMP)) AS last_transfer_date
FROM token_stats
