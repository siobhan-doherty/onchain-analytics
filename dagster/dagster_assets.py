import subprocess
from dagster import job, op, ScheduleDefinition, Definitions


@op
def run_fetch_data():
    result = subprocess.run(
        ["python", "/app/fetch_dex_trades.py"],
        capture_output = True,
        text = True
    )
    if result.returncode != 0:
        raise Exception(f"Data fetch failed: {result.stderr}")
    return result.stdout

@op
def run_dbt_build():
    result = subprocess.run(
        ["dbt", "build", "--profiles-dir", "/app"],
        capture_output = True,
        text = True
    )
    if result.returncode != 0:
        raise Exception(f"dbt build failed: {result.stderr}")
    return result.stdout

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
