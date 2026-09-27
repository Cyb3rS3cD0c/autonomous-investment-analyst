"""Market-data tools backed by Yahoo Finance."""
from __future__ import annotations

from typing import Any

try:  # keep deterministic/unit-test paths usable before optional providers install
    import yfinance as yf
except ImportError:  # pragma: no cover - exercised only in incomplete environments
    yf = None

from src.utils.logging import get_logger

logger = get_logger(__name__)


def _normalise_ticker(ticker: str) -> str:
    symbol = ticker.strip().upper()
    if not symbol:
        raise ValueError("A non-empty ticker symbol is required.")
    return symbol


def get_stock_price(ticker: str) -> dict[str, Any]:
    """Return the latest available price and basic market fields for ``ticker``."""
    symbol = _normalise_ticker(ticker)
    if yf is None:
        return {"ticker": symbol, "error": "yfinance is not installed.", "source": "Yahoo Finance"}
    try:
        history = yf.Ticker(symbol).history(period="5d", auto_adjust=False)
        if history.empty:
            return {"ticker": symbol, "error": "No price data was returned."}
        latest = history.iloc[-1]
        return {"ticker": symbol, "price": round(float(latest["Close"]), 2), "currency": "USD", "as_of": history.index[-1].isoformat(), "source": "Yahoo Finance"}
    except Exception as exc:
        logger.warning("Could not fetch price for %s: %s", symbol, exc)
        return {"ticker": symbol, "error": str(exc), "source": "Yahoo Finance"}


def get_stock_history(ticker: str, period: str = "3y") -> dict[str, Any]:
    """Return daily historical closes and a concise performance summary."""
    symbol = _normalise_ticker(ticker)
    if yf is None:
        return {"ticker": symbol, "period": period, "error": "yfinance is not installed.", "source": "Yahoo Finance"}
    try:
        history = yf.Ticker(symbol).history(period=period, auto_adjust=True)
        if history.empty:
            return {"ticker": symbol, "period": period, "error": "No historical data was returned."}
        closes = history["Close"]
        first, last = float(closes.iloc[0]), float(closes.iloc[-1])
        return {"ticker": symbol, "period": period, "start": history.index[0].date().isoformat(), "end": history.index[-1].date().isoformat(), "start_close": round(first, 2), "end_close": round(last, 2), "return_pct": round(((last / first) - 1) * 100, 2), "observations": len(history), "source": "Yahoo Finance"}
    except Exception as exc:
        logger.warning("Could not fetch history for %s: %s", symbol, exc)
        return {"ticker": symbol, "period": period, "error": str(exc), "source": "Yahoo Finance"}
