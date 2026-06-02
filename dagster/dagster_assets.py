import os
from dagster import job, op, ScheduleDefinition, Definitions

@op
def run_fetch_data():
    os.system("python /app/fetch_dex_trades.py")

@op
def run_dbt_build():
    os.system("dbt build --profiles-dir /app")

@job
def daily_pipeline():
    run_fetch_data()
    run_dbt_build()

daily_schedule = ScheduleDefinition(
    name = "daily_dex_pipeline",
    cron_schedule = "0 6 * * *",
    job = daily_pipeline,
)

defs = Definitions(
    jobs = [daily_pipeline],
    schedules = [daily_schedule],
)
