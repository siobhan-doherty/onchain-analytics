{{ config(materialized = "table") }}

SELECT 
    TRY_CAST(block_time AS TIMESTAMP) AS block_time, 
    tx_hash,
    evt_index,
    blockchain,
    token_address,
    token_symbol,
    from_address,
    to_address,
    TRY_CAST(amount AS DOUBLE) AS amount,
    TRY_CAST(amount_usd AS DOUBLE) AS amount_usd
FROM {{ source("token_transfers", "raw_token_transfers") }}
WHERE TRY_CAST(amount_usd AS DOUBLE) > 0
    AND token_symbol IS NOT NULL
    AND tx_hash IS NOT NULL
