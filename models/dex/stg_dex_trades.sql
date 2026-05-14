{{ config(materialized="view") }}

select
    cast(block_time as timestamp) as block_time,
    cast(blockchain as varchar) as blockchain,
    cast(project as varchar) as project,
    cast(version as varchar) as version,
    cast(token_bought_symbol as varchar) as token_bought_symbol,
    cast(token_sold_symbol as varchar) as token_sold_symbol,
    case
        when amount_usd is null then null
        when cast(amount_usd as varchar) = '<nil>' then null
        else cast(amount_usd as double)
    end as amount_usd,
    cast(taker as varchar) as taker,
    cast(maker as varchar) as maker
from {{ source("dune", "raw_dex_trades") }}
