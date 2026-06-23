import json
import logging
import csv
import requests
from pathlib import Path
from datetime import datetime, timezone

logging.basicConfig(level = logging.INFO, format = "%(message)s")
logger = logging.getLogger(__name__)


def log_event(event: str, **kwargs):
    logger.info(json.dumps({
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **kwargs
    }))

GRAPH_URL = "https://api.thegraph.com/subgraphs/name/ensdomains/ens"
OUTPUT_PATH = Path(__file__).parent / "seeds" / "raw_graph_domains.csv"


def fetch_ens_domains(limit: int = 100) -> list[dict]:
    """Fetch recent ENS domains from The Graph."""
    query = f"""
    {{
        domains(first: {limit}, orderBy: createdAt, orderDirection: desc) {{
            id
            name
            owner {{
                id
            }}
            createdAt
            expiryDate
        }}
    }}
    """
    response = requests.post(GRAPH_URL, json = {"query": query}, timeout = 30)
    response.raise_for_status()
    data = response.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]["domains"]


def write_domains_csv(domains: list[dict], path: Path) -> None:
    rows = []
    for d in domains:
        rows.append({
            "domain_id": d["id"],
            "name": d["name"],
            "owner_address": d["owner"]["id"] if d.get("owner") else None,
            "created_at": d.get("createdAt"),
            "expiry_date": d.get("expiryDate")
        })
    with open(path, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.DictWriter(f, fieldnames = rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    log_event("graph_fetch_start")
    try:
        domains = fetch_ens_domains(100)
        OUTPUT_PATH.parent.mkdir(parents = True, exist_ok = True)
        write_domains_csv(domains, OUTPUT_PATH)
        log_event("graph_fetch_success", count = len(domains), path = str(OUTPUT_PATH))
    except Exception as e:
        log_event("graph_fetch_failure", error = str(e), error_type = type(e).__name__)
        raise


if __name__ == "__main__":
    main()
