{{ config(materialized = "table") }}

SELECT
    TRY_CAST(tx_hash AS TEXT) AS tx_hash,
    TRY_CAST(block_number AS BIGINT) AS block_number,
    TRY_CAST(block_time AS TIMESTAMP) AS block_time,
    TRY_CAST(from_address AS TEXT) AS from_address,
    TRY_CAST(to_address AS TEXT) AS to_address,
    TRY_CAST(value_eth AS DOUBLE) AS value_eth,
    TRY_CAST(value_usd AS DOUBLE) AS value_usd,
    TRY_CAST(gas_used AS BIGINT) AS gas_used,
    TRY_CAST(gas_price AS DOUBLE) AS gas_price,
    TRY_CAST(gas_fee_usd AS DOUBLE) AS gas_fee_usd,
    TRY_CAST(blockchain AS TEXT) AS blockchain,
    TRY_CAST(tx_status AS TEXT) AS tx_status,
    TRY_CAST(input_data AS TEXT) AS input_data,
    TRY_CAST(method_id AS TEXT) AS method_id,
    TRY_CAST(contract_address AS TEXT) AS contract_address,
    TRY_CAST(last_updated AS TIMESTAMP) AS last_updated
FROM {{ source("flipside", "raw_flipside_transactions") }}
WHERE tx_hash IS NOT NULL
    AND block_time IS NOT NULL
