{{ config(materialized="table") }}

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
