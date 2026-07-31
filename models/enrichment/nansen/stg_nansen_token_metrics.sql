{{ config(materialized = "table") }}

SELECT
    TRY_CAST(token_address AS TEXT) AS token_address,
    TRY_CAST(token_symbol AS TEXT) AS token_symbol,
    TRY_CAST(token_name AS TEXT) AS token_name,
    TRY_CAST(category AS TEXT) AS category,
    TRY_CAST(sub_category AS TEXT) AS sub_category,
    TRY_CAST(market_cap_usd AS DOUBLE) AS market_cap_usd,
    TRY_CAST(price_usd AS DOUBLE) AS price_usd,
    TRY_CAST(volume_24h_usd AS DOUBLE) AS volume_24h_usd,
    TRY_CAST(holders_count AS BIGINT) AS holders_count,
    TRY_CAST(is_erc20 AS BOOLEAN) AS is_erc20,
    TRY_CAST(is_erc721 AS BOOLEAN) AS is_erc721,
    TRY_CAST(is_erc1155 AS BOOLEAN) AS is_erc1155,
    TRY_CAST(is_verified AS BOOLEAN) AS is_verified,
    TRY_CAST(risk_score AS DOUBLE) AS risk_score,
    TRY_CAST(last_updated AS TIMESTAMP) AS last_updated
FROM {{ source("nansen", "raw_nansen_token_metrics") }}
WHERE token_address IS NOT NULL 
    AND token_symbol IS NOT NULL
