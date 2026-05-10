FROM python:3.11-slim

# install git, required for dbt packages
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install dbt-core dbt-trino

WORKDIR /app
COPY . .
RUN dbt deps

CMD [ "dbt", "run"]
