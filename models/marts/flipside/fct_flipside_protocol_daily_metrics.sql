{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "date"},
            {"name": "not_null", "column": "protocol_id"},
            {"name": "not_null", "column": "daily_volume_usd"}
        ]
    }
) }}

SELECT
    date,
    protocol_id,
    protocol_name,
    protocol_slug,
    blockchain,
    category,
    daily_tvl_usd,
    daily_volume_usd,
    daily_revenue_usd,
    daily_fees_usd,
    daily_unique_users,
    daily_tx_count,
    daily_active_users,
    daily_new_users,
    last_updated
FROM {{ ref("int_flipside_daily_protocol_metrics") }}
ORDER BY date DESC, daily_volume_usd DESC
