"""News-search tool backed by Tavily."""
from __future__ import annotations

import os
from typing import Any

try:
    from tavily import TavilyClient
except ImportError:  # pragma: no cover - exercised only in incomplete environments
    TavilyClient = None


def search_financial_news(query: str, max_results: int = 5, api_key: str | None = None) -> list[dict[str, Any]]:
    """Search recent financial news and return title, URL, and summary fields."""
    if not query.strip():
        raise ValueError("A non-empty news query is required.")
    key = api_key or os.getenv("TAVILY_API_KEY")
    if not key or key == "YOUR_TAVILY_KEY_HERE":
        return [{"error": "TAVILY_API_KEY is not configured.", "query": query}]
    if TavilyClient is None:
        return [{"error": "tavily-python is not installed.", "query": query}]
    try:
        response = TavilyClient(api_key=key).search(query=query, max_results=max_results, topic="news")
        return [{"title": item.get("title"), "url": item.get("url"), "content": item.get("content"), "score": item.get("score")} for item in response.get("results", [])]
    except Exception as exc:
        return [{"error": str(exc), "query": query}]
