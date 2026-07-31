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
OUTPUT_PATH = Path(__file__).parent / "seeds" / "raw_nansen_token_metrics.csv"


def _headers() -> dict[str, str]:
    if not NANSEN_API_KEY:
        raise RuntimeError("NANSEN_API_KEY is not set")
    return {
        "x-api-key": NANSEN_API_KEY,
        "Content-Type": "application/json"
    }


def fetch_nansen_token_metrics(limit: int = 100) -> list[dict]:
    """Fetch token metrics from Nansen API."""
    log_event("nansen_token_metrics_fetch_start", limit = limit)
    # mock implementation, in prod. use actual Nansen API endpoints
    # e.g., /tokens/metrics or /tokens/list
    mock_metrics = [
        {
            "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            "token_symbol": "USDC",
            "token_name": "USD Coin",
            "category": "Stablecoin",
            "sub_category": "USD Stablecoin",
            "market_cap_usd": 28500000000.0,
            "price_usd": 1.0,
            "volume_24h_usd": 5200000000.0,
            "holders_count": 1500000,
            "is_erc20": True,
            "is_erc721": False,
            "is_erc1155": False,
            "is_verified": True,
            "risk_score": 0.1,
            "last_updated": datetime.now(timezone.utc).isoformat()
        },
        {
            "token_address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "token_symbol": "WETH",
            "token_name": "Wrapped Ether",
            "category": "Wrapped",
            "sub_category": "Ethereum",
            "market_cap_usd": 8500000000.0,
            "price_usd": 3200.0,
            "volume_24h_usd": 1200000000.0,
            "holders_count": 450000,
            "is_erc20": True,
            "is_erc721": False,
            "is_erc1155": False,
            "is_verified": True,
            "risk_score": 0.2,
            "last_updated": datetime.now(timezone.utc).isoformat()
        },
        {
            "token_address": "0x6b175474e89094c44da98b954eedeac495271d0f",
            "token_symbol": "DAI",
            "token_name": "DAI Stablecoin",
            "category": "Stablecoin",
            "sub_category": "Decentralized Stablecoin",
            "market_cap_usd": 5500000000.0,
            "price_usd": 1.0,
            "volume_24h_usd": 450000000.0,
            "holders_count": 380000,
            "is_erc20": True,
            "is_erc721": False,
            "is_erc1155": False,
            "is_verified": True,
            "risk_score": 0.3,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    log_event("nansen_token_metrics_fetch_success", count = len(mock_metrics))
    return mock_metrics


def write_metrics_csv(metrics: list[dict], path: Path) -> None:
    fieldnames = [
        "token_address", "token_symbol", "token_name", "category", 
        "sub_category", "market_cap_usd", "price_usd", "volume_24h_usd",
        "holders_count", "is_erc20", "is_erc721", "is_erc1155", 
        "is_verified", "risk_score", "last_updated"
    ]
    
    with open(path, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(metrics)


def load_csv_to_duckdb(csv_path: Path) -> None:
    """Load CSV into DuckDB as raw_nansen_token_metrics table."""
    import duckdb

    duckdb_path = os.getenv("DUCKDB_PATH", "/app/data/onchain_analytics.duckdb")
    try:
        conn = duckdb.connect(duckdb_path)
        conn.execute(f"""
            CREATE OR REPLACE TABLE raw_nansen_token_metrics AS
            SELECT * FROM read_csv_auto('{csv_path}')
        """)
        conn.close()
        log_event("duckdb_load_success", path = str(csv_path), db = duckdb_path)
    except Exception as e:
        log_event("duckdb_load_failure", error = str(e), error_type = type(e).__name__)


def main() -> None:
    log_event("nansen_token_metrics_fetch_start")
    try:
        metrics = fetch_nansen_token_metrics()
        OUTPUT_PATH.parent.mkdir(parents = True, exist_ok = True)
        write_metrics_csv(metrics, OUTPUT_PATH)
        log_event("nansen_token_metrics_fetch_success", count = len(metrics), path = str(OUTPUT_PATH))
    except Exception as e:
        log_event("nansen_token_metrics_fetch_failure", error = str(e), error_type = type(e).__name__)
        raise

    # load into DuckDB
    load_csv_to_duckdb(OUTPUT_PATH)


if __name__ == "__main__":
    main()
