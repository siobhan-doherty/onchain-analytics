# Onchain Analytics

ELT pipeline for DEX trade data using Dune API, DuckDB, and dbt.

## What it does

- Fetches raw DEX trades from Dune Analytics API
- Loads and cleans data in DuckDB
- Transforms with dbt models (`fct_dex_trades`)

## Run

```bash
export DUNE_API_KEY=your_key
docker compose run --rm dbt python fetch_dex_trades.py
docker compose run --rm dbt dbt run
