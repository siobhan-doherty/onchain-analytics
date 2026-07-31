{{ config(materialized = "table") }}

SELECT
    date,
    category,
    blockchain,
    COUNT(DISTINCT protocol_id) AS protocol_count,
    SUM(revenue_usd) AS total_category_revenue_usd,
    SUM(tvl_usd) AS total_category_tvl_usd,
    SUM(volume_usd) AS total_category_volume_usd,
    SUM(fees_usd) AS total_category_fees_usd,
    MAX(unique_users) AS total_unique_users,
    MAX(tx_count) AS total_tx_count,
    MAX(last_updated) AS last_updated
FROM {{ ref("stg_token_terminal_protocols") }}
WHERE category IS NOT NULL
GROUP BY 1, 2, 3
ORDER BY date DESC, total_category_volume_usd DESC
