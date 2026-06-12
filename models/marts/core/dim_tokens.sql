{{ config(materialized="table")}}

WITH all_tokens AS (
    SELECT token_bought_symbol AS token_symbol FROM {{ ref('stg_dex_trades') }}
    UNION
    SELECT token_sold_symbol FROM {{ ref("stg_dex_trades") }}
)
SELECT
    ROW_NUMBER() OVER (ORDER BY token_symbol) AS token_id,
    token_symbol,
    COUNT(*) AS occurrence_count
FROM all_tokens
WHERE token_symbol IS NOT NULL
GROUP BY token_symbol
