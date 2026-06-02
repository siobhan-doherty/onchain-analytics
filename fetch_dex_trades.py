import os
import time
import requests
from pathlib import Path

DUNE_API_KEY = os.getenv("DUNE_API_KEY")
DUNE_QUERY_ID = int(os.getenv("DUNE_QUERY_ID", "7494336"))
RAW_DEX_TRADES_CSV_PATH = Path(
    os.getenv("RAW_DEX_TRADES_CSV", "/app/data/raw_dex_trades.csv")
)


def _headers() -> dict[str, str]:
    if not DUNE_API_KEY:
        raise RuntimeError("DUNE_API_KEY is not set")
    return {"x-dune-api-key": DUNE_API_KEY}


def fetch_from_dune(query_id: int) -> str:
    execute_url = f"https://api.dune.com/api/v1/query/{query_id}/execute"
    execute_response = requests.post(execute_url, headers = _headers(), timeout = 30)
    execute_response.raise_for_status()
    execution_id = execute_response.json()["execution_id"]

    for _ in range(120):
        status_url = f"https://api.dune.com/api/v1/execution/{execution_id}/status"
        status_response = requests.get(status_url, headers = _headers(), timeout = 30)
        status_response.raise_for_status()
        state = status_response.json()["state"]

        if state == "QUERY_STATE_COMPLETED":
            break
        if state in {
            "QUERY_STATE_FAILED", 
            "QUERY_STATE_CANCELLED", 
            "QUERY_STATE_EXPIRED"
        }:
            raise RuntimeError(f"Dune execution ended with state={state}")
        
        time.sleep(2)
    else:
        raise TimeoutError("Timed out waiting for Dune query execution")

    results_url = f"https://api.dune.com/api/v1/execution/{execution_id}/results/csv"
    results_response = requests.get(results_url, headers = _headers(), timeout = 60)
    results_response.raise_for_status()
    return results_response.text


def write_fallback_sample(path: Path) -> None:
    sample = """block_time,blockchain,project,version,token_bought_symbol,token_sold_symbol,amount_usd,taker,maker
2025-01-01 00:00:00,ethereum,uniswap,v3,ETH,USDC,1000.0,0xabc,0xdef
2025-01-02 00:00:00,polygon,quickswap,v2,MATIC,USDC,500.0,0xghi,0xjkl
"""
    path.write_text(sample, encoding = "utf-8")


def main() -> None:
    RAW_DEX_TRADES_CSV_PATH.parent.mkdir(parents = True, exist_ok = True)

    try:
        csv_data = fetch_from_dune(DUNE_QUERY_ID)
        RAW_DEX_TRADES_CSV_PATH.write_text(csv_data, encoding = "utf-8")
        print(f"Wrote Dune CSV to {RAW_DEX_TRADES_CSV_PATH}")
    except Exception as e:
        print(f"Dune fetch failed: {e}")
        write_fallback_sample(RAW_DEX_TRADES_CSV_PATH)
        print(f"Wrote fallback sample CSV to {RAW_DEX_TRADES_CSV_PATH}")


if __name__ == "__main__":
    main()
