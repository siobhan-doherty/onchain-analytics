{{ config(materialized = "table") }}

SELECT
    DATE_TRUNC('day', last_updated) AS snapshot_date,
    token_address,
    token_symbol,
    token_name,
    blockchain,
    AVG(price_usd) AS avg_price_usd,
    AVG(price_eth) AS avg_price_eth,
    AVG(market_cap_usd) AS avg_market_cap_usd,
    SUM(volume_24h_usd) AS total_daily_volume_usd,
    AVG(holders_count) AS avg_holders_count,
    AVG(total_supply) AS avg_total_supply,
    MAX(last_updated) AS last_updated
FROM {{ ref("stg_flipside_token_metrics") }}
GROUP BY 1, 2, 3, 4, 5
ORDER BY snapshot_date DESC, avg_market_cap_usd DESC
