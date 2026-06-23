{{ config(materialized = "table") }}

SELECT
    DATE_TRUNC('day', created_at) AS registration_date,
    COUNT(*) AS domains_registered,
    COUNT(DISTINCT owner_address) AS unique_owners
FROM {{ ref("stg_graph_domains") }}
WHERE created_at IS NOT NULL
GROUP BY 1
