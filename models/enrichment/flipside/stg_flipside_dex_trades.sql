{{ config(materialized = "table") }}

SELECT
    TRY_CAST(trade_id AS TEXT) AS trade_id,
    TRY_CAST(tx_hash AS TEXT) AS tx_hash,
    TRY_CAST(block_number AS BIGINT) AS block_number,
    TRY_CAST(block_time AS TIMESTAMP) AS block_time,
    TRY_CAST(dex_name AS TEXT) AS dex_name,
    TRY_CAST(dex_version AS TEXT) AS dex_version,
    TRY_CAST(blockchain AS TEXT) AS blockchain,
    TRY_CAST(token_bought_address AS TEXT) AS token_bought_address,
    TRY_CAST(token_bought_symbol AS TEXT) AS token_bought_symbol,
    TRY_CAST(token_bought_amount AS DOUBLE) AS token_bought_amount,
    TRY_CAST(token_sold_address AS TEXT) AS token_sold_address,
    TRY_CAST(token_sold_symbol AS TEXT) AS token_sold_symbol,
    TRY_CAST(token_sold_amount AS DOUBLE) AS token_sold_amount,
    TRY_CAST(amount_usd AS DOUBLE) AS amount_usd,
    TRY_CAST(amount_eth AS DOUBLE) AS amount_eth,
    TRY_CAST(taker_address AS TEXT) AS taker_address,
    TRY_CAST(maker_address AS TEXT) AS maker_address,
    TRY_CAST(pool_address AS TEXT) AS pool_address,
    TRY_CAST(fee_tier AS TEXT) AS fee_tier,
    TRY_CAST(last_updated AS TIMESTAMP) AS last_updated
FROM {{ source("flipside", "raw_flipside_dex_trades") }}
WHERE tx_hash IS NOT NULL
    AND block_time IS NOT NULL
    AND amount_usd IS NOT NULL
