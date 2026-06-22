{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "trade_date"},
            {"name": "not_null", "column": "total_volume_usd"},
            {"name": "not_null", "column": "unique_traders"}
        ]
    }
) }}

SELECT
    trade_date,
    blockchain,
    project,
    number_of_trades,
    total_volume_usd,
    unique_traders,
    avg_trade_size_usd
FROM {{ ref("int_dex_daily_volume") }}
ORDER BY trade_date DESC, total_volume_usd DESC
