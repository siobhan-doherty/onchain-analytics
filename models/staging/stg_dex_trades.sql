{{ config(materialized="table") }}

SELECT
    TRY_CAST(block_time AS TIMESTAMP) AS block_time,
    tx_hash,
    evt_index,
    blockchain,
    project,
    version,
    token_bought_symbol,
    token_sold_symbol,
    TRY_CAST(amount_usd AS DOUBLE) amount_usd,
    taker,
    maker
FROM {{ source("dune", "raw_dex_trades") }}
WHERE TRY_CAST(amount_usd AS DOUBLE) > 0
