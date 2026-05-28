{{ config(materialized="table") }}

select
    block_time,
    blockchain,
    project,
    version,
    token_bought_symbol,
    token_sold_symbol,
    amount_usd,
    taker,
    maker
from {{ ref("stg_dex_trades") }}
where amount_usd is not null 
    and amount_usd > 0
