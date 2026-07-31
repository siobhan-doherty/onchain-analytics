import pytest
import requests
from unittest.mock import Mock, patch
from pathlib import Path
from fetch_token_transfers import fetch_from_dune, main


@pytest.fixture
def mock_headers():
    """Patch _headers to return valid headers without environment check."""
    with patch("fetch_token_transfers._headers") as mock:
        mock.return_value = {"x-dune-api-key": "test_key"}
        yield mock


def test_fetch_from_dune_success(mock_headers):
    """Simulate a successful Dune API response for token transfers."""
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value = Mock(status_code = 200, json = lambda: {"execution_id": "123"})
        mock_get.side_effect = [
            Mock(status_code = 200, json = lambda: {"state": "QUERY_STATE_COMPLETED"}),
            Mock(status_code = 200, text = "block_time,tx_hash,evt_index,blockchain,token_address,token_symbol,from_address,to_address,amount,amount_usd\n2025-01-01,0xabc,1,ethereum,0x123,USDC,0xdef,0xghi,100.0,100.0")
        ]
        result = fetch_from_dune(3734834)
        assert "block_time" in result
        assert "0xabc" in result


def test_fetch_from_dune_failure(mock_headers):
    """Simulate a 401 Unauthorized error."""
    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(
            status_code = 401,
            raise_for_status = Mock(side_effect = requests.HTTPError("401 Unauthorized"))
        )
        with pytest.raises(requests.HTTPError):
            fetch_from_dune(3734834)


def test_main_fetch_failure_writes_fallback(mock_headers, tmp_path):
    """When the API fails, the fallback CSV should be written."""
    output_path = tmp_path / "raw_token_transfers.csv"
    with patch("fetch_token_transfers.fetch_from_dune") as mock_fetch:
        mock_fetch.side_effect = Exception("API Down")
        main(output_path = output_path)
        assert output_path.exists()
        content = output_path.read_text()
        # match actual fallback content from write_fallback_sample
        assert "2024-01-01" in content
        assert "USDC" in content


def test_main_fetch_success_writes_live_data(mock_headers, tmp_path):
    """When the API succeeds, the live CSV is written."""
    output_path = tmp_path / "raw_token_transfers.csv"
    with patch("fetch_token_transfers.fetch_from_dune") as mock_fetch:
        mock_fetch.return_value = "block_time,tx_hash,evt_index,blockchain,token_address,token_symbol,from_address,to_address,amount,amount_usd\n2025-02-01,0xabc,1,ethereum,0x123,ETH,0xdef,0xghi,0.5,1500.0"
        main(output_path = output_path)
        assert output_path.exists()
        content = output_path.read_text()
        assert "2025-02-01" in content
        assert "ETH" in content
