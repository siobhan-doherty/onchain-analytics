{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "tx_hash"},
            {"name": "not_null", "column": "amount_usd"},
            {"name": "not_null", "column": "block_time"},
            {"name": "not_null", "column": "blockchain"},
            {"name": "not_null", "column": "token_symbol"},
            {"name": "not_null", "column": "from_address"},
            {"name": "not_null", "column": "to_address"}
        ]
    }
) }}

SELECT
    block_time,
    tx_hash,
    evt_index,
    blockchain,
    token_address,
    token_symbol,
    from_address,
    to_address,
    amount,
    amount_usd,
    DATE_TRUNC('day', block_time) AS transfer_date
FROM {{ ref("stg_token_transfers") }}
