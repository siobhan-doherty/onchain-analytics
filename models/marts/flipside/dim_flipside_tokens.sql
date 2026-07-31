{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "token_address"},
            {"name": "unique", "column": "token_address"}
        ]
    }
) }}

SELECT
    token_address,
    token_symbol,
    token_name,
    blockchain,
    avg_price_usd,
    avg_price_eth,
    avg_market_cap_usd,
    total_daily_volume_usd,
    avg_holders_count,
    avg_total_supply,
    token_standard,
    is_verified,
    category,
    MAX(snapshot_date) AS latest_snapshot_date,
    MAX(last_updated) AS last_updated
FROM {{ ref("int_flipside_daily_token_metrics") }}
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
ORDER BY avg_market_cap_usd DESC
