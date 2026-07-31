{{ config(materialized = "table") }}

SELECT
    TRY_CAST(address AS TEXT) AS address,
    TRY_CAST(label AS TEXT) AS label,
    TRY_CAST(category AS TEXT) AS category,
    TRY_CAST(confidence AS TEXT) AS confidence,
    TRY_CAST(is_smart_money AS BOOLEAN) AS is_smart_money,
    TRY_CAST(is_sanctioned AS BOOLEAN) AS is_sanctioned,
    TRY_CAST(last_updated AS TIMESTAMP) AS last_updated
FROM {{ source("nansen", "raw_nansen_labels") }}
WHERE address IS NOT NULL 
    AND label IS NOT NULL
