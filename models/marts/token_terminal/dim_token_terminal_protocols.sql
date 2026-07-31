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
    MAX(revenue_usd) AS latest_revenue_usd,
    MAX(tvl_usd) AS latest_tvl_usd,
    MAX(volume_usd) AS latest_volume_usd,
    MAX(unique_users) AS latest_unique_users,
    MAX(last_updated) AS last_updated
FROM {{ ref("stg_token_terminal_protocols") }}
GROUP BY 1, 2, 3, 4, 5
ORDER BY latest_tvl_usd DESC
