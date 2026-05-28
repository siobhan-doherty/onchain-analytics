SELECT
    tx_hash,
    evt_index,
    COUNT(*) AS duplicate_count
FROM {{ ref('fct_dex_trades') }}
GROUP BY tx_hash, evt_index
HAVING COUNT(*) > 1
