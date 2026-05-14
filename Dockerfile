FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    dbt-duckdb \
    requests

WORKDIR /app
COPY . .

RUN dbt deps

CMD ["bash", "-lc", "python fetch_dex_trades.py && dbt build --profiles-dir /app"]
