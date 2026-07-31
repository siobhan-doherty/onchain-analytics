{{ config(materialized = "table") }}

-- Enriched token transfers with Nansen wallet labels and token metrics
WITH base_transfers AS (
    SELECT
        t.block_time,
        t.tx_hash,
        t.evt_index,
        t.blockchain,
        t.token_address,
        t.token_symbol,
        t.from_address,
        t.to_address,
        t.amount,
        t.amount_usd,
        DATE_TRUNC('day', t.block_time) AS transfer_date
    FROM {{ ref("stg_token_transfers") }} t
),

-- Join with Nansen wallet labels for sender
sender_labels AS (
    SELECT
        b.*,
        l.label AS from_label,
        l.category AS from_category,
        l.is_smart_money AS from_is_smart_money,
        l.is_sanctioned AS from_is_sanctioned
    FROM base_transfers b
    LEFT JOIN {{ ref("stg_nansen_labels") }} l
        ON LOWER(b.from_address) = LOWER(l.address)
),

-- Join with Nansen wallet labels for recipient
recipient_labels AS (
    SELECT
        s.*,
        l.label AS to_label,
        l.category AS to_category,
        l.is_smart_money AS to_is_smart_money,
        l.is_sanctioned AS to_is_sanctioned
    FROM sender_labels s
    LEFT JOIN {{ ref("stg_nansen_labels") }} l
        ON LOWER(s.to_address) = LOWER(l.address)
),

-- Join with Nansen token metrics
enriched_transfers AS (
    SELECT
        r.*,
        tm.category AS token_category,
        tm.sub_category AS token_sub_category,
        tm.market_cap_usd,
        tm.price_usd AS token_price_usd,
        tm.volume_24h_usd AS token_volume_24h_usd,
        tm.holders_count AS token_holders_count,
        tm.is_verified AS token_is_verified,
        tm.risk_score AS token_risk_score
    FROM recipient_labels r
    LEFT JOIN {{ ref("stg_nansen_token_metrics") }} tm
        ON LOWER(r.token_address) = LOWER(tm.token_address)
)

SELECT
    *
FROM enriched_transfers
ORDER BY block_time DESC
