{{ config(materialized = "table") }}

SELECT
    TRY_CAST(address AS TEXT) AS address,
    TRY_CAST(address_type AS TEXT) AS address_type,
    TRY_CAST(is_contract AS BOOLEAN) AS is_contract,
    TRY_CAST(is_eoa AS BOOLEAN) AS is_eoa,
    TRY_CAST(contract_creator AS TEXT) AS contract_creator,
    TRY_CAST(created_at AS TIMESTAMP) AS created_at,
    TRY_CAST(first_tx_date AS DATE) AS first_tx_date,
    TRY_CAST(last_tx_date AS DATE) AS last_tx_date,
    TRY_CAST(total_tx_count AS BIGINT) AS total_tx_count,
    TRY_CAST(total_eth_spent AS DOUBLE) AS total_eth_spent,
    TRY_CAST(total_usd_spent AS DOUBLE) AS total_usd_spent,
    TRY_CAST(active_days AS BIGINT) AS active_days,
    TRY_CAST(blockchain AS TEXT) AS blockchain,
    TRY_CAST(label AS TEXT) AS label,
    TRY_CAST(category AS TEXT) AS category,
    TRY_CAST(last_updated AS TIMESTAMP) AS last_updated
FROM {{ source("flipside", "raw_flipside_addresses") }}
WHERE address IS NOT NULL
