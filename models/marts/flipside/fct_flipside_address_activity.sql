{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "activity_date"},
            {"name": "not_null", "column": "blockchain"},
            {"name": "not_null", "column": "unique_addresses"}
        ]
    }
) }}

SELECT
    activity_date,
    blockchain,
    unique_addresses,
    total_transactions,
    total_eth_spent,
    total_usd_spent,
    avg_active_days,
    contract_count,
    eoa_count,
    last_updated
FROM {{ ref("int_flipside_daily_address_activity") }}
ORDER BY activity_date DESC, unique_addresses DESC
