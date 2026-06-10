import subprocess
import duckdb
from dagster import (
    job, op, ScheduleDefinition, Definitions, sensor, RunRequest, 
    SkipReason, SensorEvaluationContext
)
from datetime import datetime


@sensor(job = daily_pipeline, minimum_interval_seconds = 3600)  # runs every hour
def data_freshness_sensor(context: SensorEvaluationContext):
    conn = duckdb.connect("/app/data/dex_analytics.duckdb")
    result = conn.execute(
        "SELECT MAX(trade_date) FROM int_dex_daily_volume"
    ).fetchone()
    conn.close()
    last_update = result[0]
    if last_update is None:
        context.log.warning("No data in int_dex_daily_volume – run the pipeline now.")
        return SkipReason("No data")
    hours_since = (datetime.now() - last_update).total_seconds() / 3600
    if hours_since > 24:
        context.log.warning(
            f"Data is stale ({hours_since:.1f} hours). Consider running the pipeline."
        )
        return SkipReason(f"Stale data, last update {last_update}")
    context.log.info(f"Data fresh, last update {last_update}")
    return SkipReason("Data fresh, no action needed")

@op
def check_freshness():
    conn = duckdb.connect("/app/data/dex_analytics.duckdb")
    result = conn.execute(
        "SELECT MAX(trade_date) FROM int_dex_daily_volume"
    ).fetchone()
    conn.close()
    last_update = result[0]
    if last_update is None:
        raise Exception("No data in int_dex_daily_volume")
    hours_since = (datetime.now() - last_update).total_seconds() / 3600
    if hours_since > 24:
        raise Exception(f"Data is stale: last update was {hours_since:.1f} hours ago")
    return f"Fresh data: last update {last_update}"

@op
def run_fetch_data():
    result = subprocess.run(
        ["python", "/app/fetch_dex_trades.py"], capture_output = True, text = True
    )
    if result.returncode != 0:
        raise Exception(f"Data fetch failed: {result.stderr}")
    return result.stdout

@op
def run_dbt_build():
    result = subprocess.run(
        ["dbt", "build", "--profiles-dir", "/app"], capture_output = True, text = True
    )
    if result.returncode != 0:
        raise Exception(f"dbt build failed: {result.stderr}")
    return result.stdout

@job
def daily_pipeline():
    run_fetch_data()
    run_dbt_build()
    check_freshness()

@job
def test_freshness():
    check_freshness()

daily_schedule = ScheduleDefinition(
    name = "daily_dex_pipeline",
    cron_schedule = "0 6 * * *",
    job = daily_pipeline,
)

defs = Definitions(
    jobs = [daily_pipeline, test_freshness],
    schedules = [daily_schedule],
    sensors = [data_freshness_sensor],
)
