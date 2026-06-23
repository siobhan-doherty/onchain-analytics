{{ config(materialized = "table") }}

SELECT
    domain_id,
    name,
    owner_address,
    TRY_CAST(created_at AS TIMESTAMP) AS created_at,
    TRY_CAST(expiry_date AS TIMESTAMP) AS expiry_date
FROM {{ source("graph", "raw_graph_domains") }}
WHERE name IS NOT NULL
