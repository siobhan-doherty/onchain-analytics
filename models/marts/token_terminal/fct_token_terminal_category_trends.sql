{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "date"},
            {"name": "not_null", "column": "category"},
            {"name": "not_null", "column": "total_category_volume_usd"}
        ]
    }
) }}

SELECT
    date,
    category,
    blockchain,
    protocol_count,
    total_category_revenue_usd,
    total_category_tvl_usd,
    total_category_volume_usd,
    total_category_fees_usd,
    total_unique_users,
    total_tx_count,
    last_updated
FROM {{ ref("int_token_terminal_category_aggregates") }}
ORDER BY date DESC, total_category_volume_usd DESC
