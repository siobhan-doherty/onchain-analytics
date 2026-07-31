import pytest
from unittest.mock import patch
from pathlib import Path
from fetch_token_terminal import write_protocols_csv, main


def test_write_protocols_csv(tmp_path):
    """Test writing protocols to CSV file."""
    protocols = [
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
            "last_updated": "2024-01-01T00:00:00Z"
        }
    ]
    output_path = tmp_path / "test_protocols.csv"
    write_protocols_csv(protocols, output_path)
    assert output_path.exists()
    content = output_path.read_text()
    assert "protocol_id" in content
    assert "uniswap" in content
    assert "DEX" in content


def test_main_success_writes_csv(tmp_path):
    """When fetch succeeds, the CSV should be written with mock data."""
    with patch("fetch_token_terminal.OUTPUT_PATH", tmp_path / "raw_token_terminal_protocols.csv"):
        main()
    assert (tmp_path / "raw_token_terminal_protocols.csv").exists()
    content = (tmp_path / "raw_token_terminal_protocols.csv").read_text()
    assert "protocol_id" in content
    assert "uniswap" in content


def test_headers_requires_api_key():
    """_headers function requires TOKEN_TERMINAL_API_KEY to be set."""
    import os
    from fetch_token_terminal import _headers
    original_key = os.environ.get("TOKEN_TERMINAL_API_KEY")
    try:
        if "TOKEN_TERMINAL_API_KEY" in os.environ:
            del os.environ["TOKEN_TERMINAL_API_KEY"]
        with pytest.raises(RuntimeError, match = "TOKEN_TERMINAL_API_KEY is not set"):
            _headers()
    finally:
        if original_key:
            os.environ["TOKEN_TERMINAL_API_KEY"] = original_key
