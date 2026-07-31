import pytest
from unittest.mock import patch
from pathlib import Path
from fetch_nansen_labels import write_labels_csv, main


def test_write_labels_csv(tmp_path):
    """Test writing labels to CSV file."""
    labels = [
        {
            "address": "0x123",
            "label": "Test Wallet",
            "category": "Test",
            "confidence": "high",
            "is_smart_money": True,
            "is_sanctioned": False,
            "last_updated": "2024-01-01T00:00:00Z"
        }
    ]
    output_path = tmp_path / "test_labels.csv"
    write_labels_csv(labels, output_path)
    assert output_path.exists()
    content = output_path.read_text()
    assert "address" in content
    assert "0x123" in content
    assert "Test Wallet" in content


def test_main_success_writes_csv(tmp_path):
    """When fetch succeeds, the CSV should be written with mock data."""
    with patch("fetch_nansen_labels.OUTPUT_PATH", tmp_path / "raw_nansen_labels.csv"):
        main()
    assert (tmp_path / "raw_nansen_labels.csv").exists()
    content = (tmp_path / "raw_nansen_labels.csv").read_text()
    assert "address" in content
    assert "Vitalik Buterin" in content


def test_headers_requires_api_key():
    """_headers function requires NANSEN_API_KEY to be set."""
    import os
    from fetch_nansen_labels import _headers
    original_key = os.environ.get("NANSEN_API_KEY")
    try:
        if "NANSEN_API_KEY" in os.environ:
            del os.environ["NANSEN_API_KEY"]
        with pytest.raises(RuntimeError, match = "NANSEN_API_KEY is not set"):
            _headers()
    finally:
        if original_key:
            os.environ["NANSEN_API_KEY"] = original_key
