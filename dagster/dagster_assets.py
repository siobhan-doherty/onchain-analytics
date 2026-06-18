import os
import subprocess
import duckdb
from dagster import (
    job,
    op,
    ScheduleDefinition,
    Definitions,
    sensor,
    SkipReason,
    SensorEvaluationContext,
)
from datetime import datetime
from pathlib import Path

DUCKDB_PATH = os.getenv("DUCKDB_PATH", "/app/data/dex_analytics.duckdb")


# ops
@op
def check_freshness():
    conn = duckdb.connect(DUCKDB_PATH)
    result = conn.execute("SELECT MAX(trade_date) FROM int_dex_daily_volume").fetchone()
    conn.close()
    last_update = result[0]
    if last_update is None:
        raise Exception("No data in int_dex_daily_volume")
    hours_since = (datetime.now() - last_update).total_seconds() / 3600
    if hours_since > 168:  # 7 days
        raise Exception(f"Data is stale: last update was {hours_since:.1f} hours ago")
    return f"Fresh data: last update {last_update}"


@op
def run_fetch_data():
    # run existing Python script to write CSV
    result = subprocess.run(
        ["python", "/app/fetch_dex_trades.py"], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"Data fetch failed: {result.stderr}")

    # load CSV into DuckDB, overwrites raw_dex_trades
    csv_path = "/app/data/raw_dex_trades.csv"
    if not Path(csv_path).exists():
        raise Exception(f"CSV file {csv_path} not found after fetch")
    conn = duckdb.connect(DUCKDB_PATH)
    conn.execute(f"""
        CREATE OR REPLACE TABLE raw_dex_trades AS
        SELECT * FROM read_csv_auto('{csv_path}')
    """)
    conn.close()
    return f"Fetched and loaded CSV, row count: {result.stdout}"


@op
def run_dbt_build():
    result = subprocess.run(
        ["dbt", "build", "--profiles-dir", "/app"], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt build failed: {result.stderr}")
    return result.stdout


# jobs
@job
def daily_pipeline():
    run_fetch_data()
    run_dbt_build()
    check_freshness()


@job
def test_freshness():
    check_freshness()


# schedule
daily_schedule = ScheduleDefinition(
    name="daily_dex_pipeline",
    cron_schedule="0 6 * * *",
    job=daily_pipeline,
)


# sensor
@sensor(job=daily_pipeline, minimum_interval_seconds=3600)
def data_freshness_sensor(context: SensorEvaluationContext):
    conn = duckdb.connect(DUCKDB_PATH)
    result = conn.execute("SELECT MAX(trade_date) FROM int_dex_daily_volume").fetchone()
    conn.close()
    if result is not None:
        last_update = result[0]
    else:
        last_update = None

    if last_update is None:
        context.log.warning("No data in int_dex_daily_volume – run the pipeline now.")
        return SkipReason("No data")
    hours_since = (datetime.now() - last_update).total_seconds() / 3600
    if hours_since > 168:
        context.log.warning(
            f"Data is stale ({hours_since:.1f} hours). Consider running the pipeline."
        )
        return SkipReason(f"Stale data, last update {last_update}")
    context.log.info(f"Data fresh, last update {last_update}")
    return SkipReason("Data fresh, no action needed")


# definitions
defs = Definitions(
    jobs=[daily_pipeline, test_freshness],
    schedules=[daily_schedule],
    sensors=[data_freshness_sensor],
)
