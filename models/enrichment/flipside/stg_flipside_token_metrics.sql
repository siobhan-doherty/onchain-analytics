{{ config(materialized = "table") }}

SELECT
    TRY_CAST(token_address AS TEXT) AS token_address,
    TRY_CAST(token_symbol AS TEXT) AS token_symbol,
    TRY_CAST(token_name AS TEXT) AS token_name,
    TRY_CAST(token_decimals AS BIGINT) AS token_decimals,
    TRY_CAST(blockchain AS TEXT) AS blockchain,
    TRY_CAST(price_usd AS DOUBLE) AS price_usd,
    TRY_CAST(price_eth AS DOUBLE) AS price_eth,
    TRY_CAST(market_cap_usd AS DOUBLE) AS market_cap_usd,
    TRY_CAST(volume_24h_usd AS DOUBLE) AS volume_24h_usd,
    TRY_CAST(volume_24h_eth AS DOUBLE) AS volume_24h_eth,
    TRY_CAST(holders_count AS BIGINT) AS holders_count,
    TRY_CAST(total_supply AS DOUBLE) AS total_supply,
    TRY_CAST(circulating_supply AS DOUBLE) AS circulating_supply,
    TRY_CAST(token_standard AS TEXT) AS token_standard,
    TRY_CAST(is_verified AS BOOLEAN) AS is_verified,
    TRY_CAST(category AS TEXT) AS category,
    TRY_CAST(last_updated AS TIMESTAMP) AS last_updated
FROM {{ source("flipside", "raw_flipside_token_metrics") }}
WHERE token_address IS NOT NULL
    AND token_symbol IS NOT NULL
