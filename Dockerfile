FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# copy requirements first for better caching
COPY requirements.txt .

# install all Python deps from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade dagster dagster-dbt dagster-webserver

WORKDIR /app
COPY . .

RUN dbt deps

CMD ["bash", "-c", "python fetch_dex_trades.py && dbt build --profiles-dir /app"]
