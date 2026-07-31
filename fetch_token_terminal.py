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

TOKEN_TERMINAL_API_KEY = os.getenv("TOKEN_TERMINAL_API_KEY")
TOKEN_TERMINAL_API_URL = "https://api.tokenterminal.com/v1"
OUTPUT_PATH = Path(__file__).parent / "seeds" / "raw_token_terminal_protocols.csv"


def _headers() -> dict[str, str]:
    if not TOKEN_TERMINAL_API_KEY:
        raise RuntimeError("TOKEN_TERMINAL_API_KEY is not set")
    return {
        "Authorization": f"Bearer {TOKEN_TERMINAL_API_KEY}",
        "Content-Type": "application/json"
    }


def fetch_token_terminal_protocols(limit: int = 100) -> list[dict]:
    """Fetch protocol metrics from Token Terminal API."""
    log_event("token_terminal_fetch_start", limit = limit)
    # mock implementation, in prod. use actual Token Terminal API
    # e.g., /protocols or /metrics
    mock_protocols = [
        {
            "protocol_id": "uniswap",
            "protocol_name": "Uniswap",
            "protocol_slug": "uniswap",
            "blockchain": "ethereum",
            "category": "DEX",
            "date": "2024-01-01",
            "revenue_usd": 1500000.0,
            "tvl_usd": 3500000000.0,
            "volume_usd": 850000000.0,
            "unique_users": 125000,
            "tx_count": 450000,
            "fees_usd": 450000.0,
            "last_updated": datetime.now(timezone.utc).isoformat()
        },
        {
            "protocol_id": "aave",
            "protocol_name": "Aave",
            "protocol_slug": "aave",
            "blockchain": "ethereum",
            "category": "Lending",
            "date": "2024-01-01",
            "revenue_usd": 850000.0,
            "tvl_usd": 2800000000.0,
            "volume_usd": 320000000.0,
            "unique_users": 85000,
            "tx_count": 120000,
            "fees_usd": 250000.0,
            "last_updated": datetime.now(timezone.utc).isoformat()
        },
        {
            "protocol_id": "maker",
            "protocol_name": "Maker",
            "protocol_slug": "maker",
            "blockchain": "ethereum",
            "category": "Lending",
            "date": "2024-01-01",
            "revenue_usd": 650000.0,
            "tvl_usd": 1800000000.0,
            "volume_usd": 150000000.0,
            "unique_users": 45000,
            "tx_count": 65000,
            "fees_usd": 180000.0,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    ]
    log_event("token_terminal_fetch_success", count = len(mock_protocols))
    return mock_protocols


def write_protocols_csv(protocols: list[dict], path: Path) -> None:
    fieldnames = [
        "protocol_id", "protocol_name", "protocol_slug", "blockchain",
        "category", "date", "revenue_usd", "tvl_usd", "volume_usd",
        "unique_users", "tx_count", "fees_usd", "last_updated"
    ]
    with open(path, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(protocols)


def load_csv_to_duckdb(csv_path: Path) -> None:
    """Load CSV into DuckDB as raw_token_terminal_protocols table."""
    import duckdb

    duckdb_path = os.getenv("DUCKDB_PATH", "/app/data/onchain_analytics.duckdb")
    try:
        conn = duckdb.connect(duckdb_path)
        conn.execute(f"""
            CREATE OR REPLACE TABLE raw_token_terminal_protocols AS
            SELECT * FROM read_csv_auto('{csv_path}')
        """)
        conn.close()
        log_event("duckdb_load_success", path = str(csv_path), db = duckdb_path)
    except Exception as e:
        log_event("duckdb_load_failure", error = str(e), error_type = type(e).__name__)


def main() -> None:
    log_event("token_terminal_fetch_start")
    try:
        protocols = fetch_token_terminal_protocols()
        OUTPUT_PATH.parent.mkdir(parents = True, exist_ok = True)
        write_protocols_csv(protocols, OUTPUT_PATH)
        log_event("token_terminal_fetch_success", count = len(protocols), path = str(OUTPUT_PATH))
    except Exception as e:
        log_event("token_terminal_fetch_failure", error = str(e), error_type = type(e).__name__)
        raise
    
    # load into DuckDB
    load_csv_to_duckdb(OUTPUT_PATH)


if __name__ == "__main__":
    main()
