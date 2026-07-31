{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "token_id"},
            {"name": "unique", "column": "token_id"},
            {"name": "not_null", "column": "token_address"}
        ]
    }
) }}

-- Enriched token dimension with Nansen data
WITH token_stats AS (
    SELECT
        t.token_symbol,
        t.token_address,
        COUNT(*) AS transfer_count,
        SUM(t.amount) AS total_transferred,
        SUM(t.amount_usd) AS total_volume_usd,
        COUNT(DISTINCT t.from_address) AS unique_senders,
        COUNT(DISTINCT t.to_address) AS unique_recipients,
        MIN(t.block_time) AS first_transfer_time,
        MAX(t.block_time) AS last_transfer_time
    FROM {{ ref("stg_token_transfers") }} t
    GROUP BY t.token_symbol, t.token_address
),

enriched_tokens AS (
    SELECT
        ts.*,
        ntm.category AS nansen_category,
        ntm.sub_category AS nansen_sub_category,
        ntm.token_name AS nansen_token_name,
        ntm.market_cap_usd,
        ntm.price_usd,
        ntm.volume_24h_usd,
        ntm.holders_count,
        ntm.is_verified,
        ntm.risk_score
    FROM token_stats ts
    LEFT JOIN {{ ref("stg_nansen_token_metrics") }} ntm
        ON LOWER(ts.token_address) = LOWER(ntm.token_address)
)

SELECT
    ROW_NUMBER() OVER (ORDER BY COALESCE(total_volume_usd, 0) DESC, transfer_count DESC) AS token_id,
    token_symbol,
    token_address,
    nansen_token_name,
    nansen_category,
    nansen_sub_category,
    transfer_count,
    total_transferred,
    total_volume_usd,
    unique_senders,
    unique_recipients,
    first_transfer_time,
    last_transfer_time,
    market_cap_usd,
    price_usd,
    volume_24h_usd,
    holders_count,
    is_verified,
    risk_score,
    CASE 
        WHEN is_verified = TRUE THEN 'verified'
        WHEN risk_score > 7 THEN 'high_risk'
        WHEN risk_score > 3 THEN 'medium_risk'
        ELSE 'low_risk'
    END AS token_risk_category,
    DATE_TRUNC('day', COALESCE(first_transfer_time, CURRENT_TIMESTAMP)) AS first_transfer_date,
    DATE_TRUNC('day', COALESCE(last_transfer_time, CURRENT_TIMESTAMP)) AS last_transfer_date,
    CURRENT_TIMESTAMP AS processed_at
FROM enriched_tokens
