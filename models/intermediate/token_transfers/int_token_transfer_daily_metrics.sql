{{ config(materialized = "table") }}

SELECT
    DATE_TRUNC('day', block_time) AS transfer_date,
    blockchain,
    token_symbol,
    token_address,
    COUNT(*) AS number_of_transfers,
    SUM(amount) AS total_amount,
    SUM(amount_usd) AS total_volume_usd,
    COUNT(DISTINCT from_address) AS unique_senders,
    COUNT(DISTINCT to_address) AS unique_recipients,
    AVG(amount_usd) AS avg_transfer_size_usd,
    MIN(amount_usd) AS min_transfer_size_usd,
    MAX(amount_usd) AS max_transfer_size_usd
FROM {{ ref("stg_token_transfers") }}
GROUP BY 1, 2, 3, 4
ORDER BY transfer_date DESC, total_volume_usd DESC
