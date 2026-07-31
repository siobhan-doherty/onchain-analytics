import pytest
from unittest.mock import patch
from pathlib import Path
from fetch_nansen_token_metrics import write_metrics_csv, main


def test_write_metrics_csv(tmp_path):
    """Test writing token metrics to CSV file."""
    metrics = [
        {
            "token_address": "0x123",
            "token_symbol": "TEST",
            "token_name": "Test Token",
            "category": "Test",
            "sub_category": "Test",
            "market_cap_usd": 1000000.0,
            "price_usd": 1.0,
            "volume_24h_usd": 500000.0,
            "holders_count": 1000,
            "is_erc20": True,
            "is_erc721": False,
            "is_erc1155": False,
            "is_verified": True,
            "risk_score": 0.5,
            "last_updated": "2024-01-01T00:00:00Z"
        }
    ]
    output_path = tmp_path / "test_metrics.csv"
    write_metrics_csv(metrics, output_path)
    assert output_path.exists()
    content = output_path.read_text()
    assert "token_symbol" in content
    assert "TEST" in content


def test_main_success_writes_csv(tmp_path):
    """When fetch succeeds, the CSV should be written with mock data."""
    with patch("fetch_nansen_token_metrics.OUTPUT_PATH", tmp_path / "raw_nansen_token_metrics.csv"):
        main()
    assert (tmp_path / "raw_nansen_token_metrics.csv").exists()
    content = (tmp_path / "raw_nansen_token_metrics.csv").read_text()
    assert "token_symbol" in content
    assert "USDC" in content


def test_headers_requires_api_key():
    """_headers function requires NANSEN_API_KEY to be set."""
    import os
    from fetch_nansen_token_metrics import _headers
    original_key = os.environ.get("NANSEN_API_KEY")
    try:
        if "NANSEN_API_KEY" in os.environ:
            del os.environ["NANSEN_API_KEY"]
        with pytest.raises(RuntimeError, match = "NANSEN_API_KEY is not set"):
            _headers()
    finally:
        if original_key:
            os.environ["NANSEN_API_KEY"] = original_key
