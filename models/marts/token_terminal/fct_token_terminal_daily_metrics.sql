{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "trade_date"},
            {"name": "not_null", "column": "protocol_id"},
            {"name": "not_null", "column": "daily_volume_usd"}
        ]
    }
) }}

SELECT
    date AS trade_date,
    protocol_id,
    protocol_name,
    protocol_slug,
    blockchain,
    category,
    daily_revenue_usd,
    daily_tvl_usd,
    daily_volume_usd,
    daily_fees_usd,
    daily_unique_users,
    daily_tx_count,
    record_count,
    last_updated
FROM {{ ref("int_token_terminal_daily_protocol_metrics") }}
ORDER BY trade_date DESC, daily_volume_usd DESC
