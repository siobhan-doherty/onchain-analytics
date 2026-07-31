{{ config(materialized = "table") }}

SELECT
    DATE_TRUNC('day', last_updated) AS activity_date,
    blockchain,
    COUNT(DISTINCT address) AS unique_addresses,
    SUM(total_tx_count) AS total_transactions,
    SUM(total_eth_spent) AS total_eth_spent,
    SUM(total_usd_spent) AS total_usd_spent,
    AVG(active_days) AS avg_active_days,
    COUNT(DISTINCT CASE WHEN is_contract THEN address END) AS contract_count,
    COUNT(DISTINCT CASE WHEN is_eoa THEN address END) AS eoa_count,
    MAX(last_updated) AS last_updated
FROM {{ ref("stg_flipside_addresses") }}
GROUP BY 1, 2
ORDER BY activity_date DESC, unique_addresses DESC
