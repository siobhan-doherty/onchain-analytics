{{ config(materialized="view") }}

SELECT
    DATE_TRUNC("day", block_time) AS trade_date,
    blockchain,
    project,
    COUNT(*) AS number_of_trades,
    SUM(amount_usd) AS total_volume_usd,
    COUNT(DISTINCT taker) AS unique_traders,
    AVG(amount_usd) AS avg_trade_size_usd
FROM {{ ref("stg_dex_trades") }}
GROUP BY 1, 2, 3
