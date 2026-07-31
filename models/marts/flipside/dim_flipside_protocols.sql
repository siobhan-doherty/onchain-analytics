{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "protocol_id"},
            {"name": "unique", "column": "protocol_id"}
        ]
    }
) }}

SELECT
    protocol_id,
    protocol_name,
    protocol_slug,
    blockchain,
    category,
    MAX(date) AS latest_date,
    MAX(daily_tvl_usd) AS latest_tvl_usd,
    MAX(daily_volume_usd) AS latest_volume_usd,
    MAX(daily_revenue_usd) AS latest_revenue_usd,
    MAX(daily_fees_usd) AS latest_fees_usd,
    MAX(daily_unique_users) AS latest_unique_users,
    MAX(last_updated) AS last_updated
FROM {{ ref("int_flipside_daily_protocol_metrics") }}
GROUP BY 1, 2, 3, 4, 5
ORDER BY latest_tvl_usd DESC
