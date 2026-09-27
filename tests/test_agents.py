from unittest.mock import MagicMock

from langchain_core.messages import AIMessage

from src.agent.charters import BASIC_CHARTER, FULL_CHARTER, RAG_CHARTER, TRADITIONAL_CHARTER
from src.agent.graphs import build_analyst_graph, build_tools


def test_agent_charters_progressively_add_capability():
    assert len(TRADITIONAL_CHARTER) < len(BASIC_CHARTER) < len(FULL_CHARTER) < len(RAG_CHARTER)


def test_basic_and_full_tools_are_available():
    names = {tool.name for tool in build_tools()}
    assert {"get_stock_price", "get_stock_history", "search_financial_news", "analyze_sentiment"} <= names


def test_enhanced_rag_agent_adds_private_database_tool():
    names = {tool.name for tool in build_tools(retriever=MagicMock())}
    assert "query_private_database" in names


def test_traditional_style_graph_invokes_model_without_tools():
    llm = MagicMock()
    llm.bind_tools.return_value.invoke.return_value = AIMessage(content="Research report")
    graph = build_analyst_graph(llm, charter=TRADITIONAL_CHARTER, memory=False)
    output = graph.invoke({"messages": [("user", "Summarize IBM")]})
    assert output["messages"][-1].content == "Research report"
