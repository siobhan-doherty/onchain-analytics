import pytest
import requests
from unittest.mock import Mock, patch
from pathlib import Path
from fetch_dex_trades import fetch_from_dune, main


@pytest.fixture
def mock_headers():
    """Patch _headers to return valid headers without environment check."""
    with patch("fetch_dex_trades._headers") as mock:
        mock.return_value = {"x-dune-api-key": "test_key"}
        yield mock


def test_fetch_from_dune_success(mock_headers):
    """Simulate a successful Dune API response."""
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value = Mock(status_code = 200, json = lambda: {"execution_id": "123"})
        mock_get.side_effect = [
            Mock(status_code = 200, json = lambda: {"state": "QUERY_STATE_COMPLETED"}),
            Mock(status_code = 200, text = "block_time,amount_usd\n2025-01-01,1000")
        ]
        result = fetch_from_dune(123)
        assert "block_time" in result


def test_fetch_from_dune_failure(mock_headers):
    """Simulate a 401 Unauthorized error."""
    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(
            status_code = 401,
            raise_for_status = Mock(side_effect = requests.HTTPError("401 Unauthorized"))
        )
        with pytest.raises(requests.HTTPError):
            fetch_from_dune(123)


def test_main_fetch_failure_writes_fallback(mock_headers, tmp_path):
    """When the API fails, the fallback CSV should be written."""
    output_path = tmp_path / "raw_dex_trades.csv"
    with patch("fetch_dex_trades.fetch_from_dune") as mock_fetch:
        mock_fetch.side_effect = Exception("API Down")
        main(output_path = output_path)
        assert output_path.exists()
        content = output_path.read_text()
        # match actual fallback content, 2024-01-01
        assert "2024-01-01" in content


def test_main_fetch_success_writes_live_data(mock_headers, tmp_path):
    """When the API succeeds, the live CSV is written."""
    output_path = tmp_path / "raw_dex_trades.csv"
    with patch("fetch_dex_trades.fetch_from_dune") as mock_fetch:
        mock_fetch.return_value = "block_time,amount_usd\n2025-02-01,2000"
        main(output_path = output_path)
        assert output_path.exists()
        content = output_path.read_text()
        assert "2025-02-01" in content
