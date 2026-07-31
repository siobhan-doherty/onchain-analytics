{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "trade_date"},
            {"name": "not_null", "column": "dex_name"},
            {"name": "not_null", "column": "total_volume_usd"}
        ]
    }
) }}

SELECT
    trade_date,
    blockchain,
    dex_name,
    dex_version,
    number_of_trades,
    total_volume_usd,
    total_volume_eth,
    unique_traders,
    unique_pools,
    avg_trade_size_usd,
    last_updated
FROM {{ ref("int_flipside_daily_dex_volume") }}
ORDER BY trade_date DESC, total_volume_usd DESC
