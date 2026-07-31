{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "tx_hash"},
            {"name": "not_null", "column": "amount_usd"},
            {"name": "not_null", "column": "block_time"}
        ]
    }
) }}

-- Final enriched fact table combining token transfers with Nansen and Token Terminal data
SELECT
    tx_hash,
    block_time,
    evt_index,
    blockchain,
    token_address,
    token_symbol,
    from_address,
    to_address,
    amount,
    amount_usd,
    transfer_date,
    -- Nansen wallet enrichment
    from_label,
    from_category,
    from_is_smart_money,
    from_is_sanctioned,
    to_label,
    to_category,
    to_is_smart_money,
    to_is_sanctioned,
    -- Nansen token enrichment
    token_category,
    token_sub_category,
    token_is_verified,
    token_risk_score,
    -- Calculated fields
    CASE 
        WHEN from_is_smart_money = TRUE THEN 'smart_money_outflow'
        WHEN to_is_smart_money = TRUE THEN 'smart_money_inflow'
        WHEN from_is_sanctioned = TRUE OR to_is_sanctioned = TRUE THEN 'sanctioned_related'
        ELSE 'regular'
    END AS transfer_classification,
    -- Flag transfers between labeled addresses
    CASE 
        WHEN from_label IS NOT NULL AND to_label IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS is_labeled_transfer,
    CURRENT_TIMESTAMP AS processed_at
FROM {{ ref("int_enriched_token_transfers") }}
ORDER BY block_time DESC
