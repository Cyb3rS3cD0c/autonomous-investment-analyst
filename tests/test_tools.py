from unittest.mock import MagicMock, patch

from src.tools.financial_tools import get_stock_history, get_stock_price
from src.tools.news_tools import search_financial_news
from src.tools.sentiment_tools import analyze_sentiment


@patch("src.tools.financial_tools.yf.Ticker")
def test_stock_price(mock_ticker):
    frame = MagicMock()
    frame.empty = False
    frame.index = [MagicMock(isoformat=lambda: "2026-01-01T00:00:00")]
    latest = {"Close": 123.456}
    frame.iloc.__getitem__.return_value = latest
    mock_ticker.return_value.history.return_value = frame
    assert get_stock_price("msft")["price"] == 123.46


@patch("src.tools.financial_tools.yf.Ticker")
def test_stock_history(mock_ticker):
    frame = MagicMock()
    frame.empty = False
    frame.index = [MagicMock(date=lambda: MagicMock(isoformat=lambda: "2023-01-01")), MagicMock(date=lambda: MagicMock(isoformat=lambda: "2026-01-01"))]
    closes = MagicMock()
    closes.iloc.__getitem__.side_effect = [100.0, 150.0]
    frame.__getitem__.return_value = closes
    frame.__len__.return_value = 2
    mock_ticker.return_value.history.return_value = frame
    assert get_stock_history("MSFT")["return_pct"] == 50.0


def test_news_without_key_is_actionable():
    result = search_financial_news("Microsoft earnings", api_key="YOUR_TAVILY_KEY_HERE")
    assert "error" in result[0]


def test_sentiment_baseline():
    assert analyze_sentiment("Record profit and strong growth") ["sentiment"] == "positive"
