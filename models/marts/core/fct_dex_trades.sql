{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "tx_hash"},
            {"name": "not_null", "column": "amount_usd"},
            {"name": "not_null", "column": "evt_index"},
            {"name": "not_null", "column": "block_time"},
            {"name": "not_null", "column": "blockchain"},
            {"name": "not_null", "column": "project"}
        ]
    }
) }}

SELECT
    block_time,
    tx_hash,
    evt_index,
    blockchain,
    project,
    version,
    token_bought_symbol,
    token_sold_symbol,
    amount_usd,
    taker,
    maker
FROM {{ ref("stg_dex_trades") }}
