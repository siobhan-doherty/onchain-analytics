{{ config(materialized = "table") }}

SELECT
    date,
    protocol_id,
    protocol_name,
    protocol_slug,
    blockchain,
    category,
    SUM(revenue_usd) AS daily_revenue_usd,
    SUM(tvl_usd) AS daily_tvl_usd,
    SUM(volume_usd) AS daily_volume_usd,
    SUM(fees_usd) AS daily_fees_usd,
    MAX(unique_users) AS daily_unique_users,
    MAX(tx_count) AS daily_tx_count,
    COUNT(*) AS record_count,
    MAX(last_updated) AS last_updated
FROM {{ ref("stg_token_terminal_protocols") }}
GROUP BY 1, 2, 3, 4, 5, 6
ORDER BY date DESC, daily_volume_usd DESC
