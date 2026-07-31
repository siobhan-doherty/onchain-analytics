{{ config(materialized = "table") }}

SELECT
    DATE_TRUNC('day', block_time) AS trade_date,
    blockchain,
    dex_name,
    dex_version,
    COUNT(*) AS number_of_trades,
    SUM(amount_usd) AS total_volume_usd,
    SUM(amount_eth) AS total_volume_eth,
    COUNT(DISTINCT taker_address) AS unique_traders,
    COUNT(DISTINCT pool_address) AS unique_pools,
    AVG(amount_usd) AS avg_trade_size_usd,
    MAX(last_updated) AS last_updated
FROM {{ ref("stg_flipside_dex_trades") }}
GROUP BY 1, 2, 3, 4
ORDER BY trade_date DESC, total_volume_usd DESC
