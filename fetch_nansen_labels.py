import os
import json
import logging
import requests
import csv
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

NANSEN_API_KEY = os.getenv("NANSEN_API_KEY")
NANSEN_API_URL = "https://api.nansen.ai/api/v1"
OUTPUT_PATH = Path(__file__).parent / "seeds" / "raw_nansen_labels.csv"


def _headers() -> dict[str, str]:
    if not NANSEN_API_KEY:
        raise RuntimeError("NANSEN_API_KEY is not set")
    return {
        "x-api-key": NANSEN_API_KEY,
        "Content-Type": "application/json"
    }


def fetch_nansen_labels(limit: int = 1000) -> list[dict]:
    """Fetch wallet labels from Nansen API."""
    log_event("nansen_labels_fetch_start", limit = limit)
    # this is a mock implementation, Nansen API requires specific endpoints
    # in prod, use Nansen's actual API endpoints
    # e.g. /wallets/labels or /wallets/smart-money
    # mock response for demonstration
    mock_labels = [
        {
            "address": "0xd8da6bf26964af9d7eed9e03e53415d37aa96045",
            "label": "Vitalik Buterin",
            "category": "Founder",
            "confidence": "high",
            "is_smart_money": True,
            "is_sanctioned": False,
            "last_updated": datetime.now(timezone.utc).isoformat()
        },
        {
            "address": "0x5754284f345afc66559469b23f8f5c87442814dd",
            "label": "Tornado Cash",
            "category": "Mixer",
            "confidence": "high",
            "is_smart_money": False,
            "is_sanctioned": True,
            "last_updated": datetime.now(timezone.utc).isoformat()
        },
        {
            "address": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
            "label": "Uniswap V3: Positions NFT",
            "category": "DeFi",
            "confidence": "high",
            "is_smart_money": False,
            "is_sanctioned": False,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    ]
    log_event("nansen_labels_fetch_success", count = len(mock_labels))
    return mock_labels


def write_labels_csv(labels: list[dict], path: Path) -> None:
    fieldnames = [
        "address", "label", "category", "confidence", 
        "is_smart_money", "is_sanctioned", "last_updated"
    ]
    with open(path, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(labels)


def load_csv_to_duckdb(csv_path: Path) -> None:
    """Load CSV into DuckDB as raw_nansen_labels table."""
    import duckdb

    duckdb_path = os.getenv("DUCKDB_PATH", "/app/data/onchain_analytics.duckdb")
    try:
        conn = duckdb.connect(duckdb_path)
        conn.execute(f"""
            CREATE OR REPLACE TABLE raw_nansen_labels AS
            SELECT * FROM read_csv_auto('{csv_path}')
        """)
        conn.close()
        log_event("duckdb_load_success", path = str(csv_path), db = duckdb_path)
    except Exception as e:
        log_event("duckdb_load_failure", error = str(e), error_type = type(e).__name__)


def main() -> None:
    log_event("nansen_fetch_start")
    try:
        labels = fetch_nansen_labels()
        OUTPUT_PATH.parent.mkdir(parents = True, exist_ok = True)
        write_labels_csv(labels, OUTPUT_PATH)
        log_event("nansen_fetch_success", count = len(labels), path = str(OUTPUT_PATH))
    except Exception as e:
        log_event("nansen_fetch_failure", error = str(e), error_type = type(e).__name__)
        raise
    
    # load into DuckDB
    load_csv_to_duckdb(OUTPUT_PATH)


if __name__ == "__main__":
    main()
