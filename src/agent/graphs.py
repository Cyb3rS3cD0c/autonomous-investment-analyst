"""LangGraph workflow with tool routing and conversation memory."""
from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from src.agent.charters import RAG_CHARTER
from src.rag.query_tool import query_private_database
from src.tools.financial_tools import get_stock_history, get_stock_price
from src.tools.news_tools import search_financial_news
from src.tools.sentiment_tools import analyze_sentiment


class AnalystState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_tools(retriever=None):
    """Create LangChain tool wrappers; the private-db tool is optional."""
    tools = [
        StructuredTool.from_function(get_stock_price),
        StructuredTool.from_function(get_stock_history),
        StructuredTool.from_function(search_financial_news),
        StructuredTool.from_function(analyze_sentiment),
    ]
    if retriever is not None:
        def private_database_query(query: str) -> dict[str, Any]:
            """Search the private company AI-initiatives PDF database."""
            return query_private_database(query, retriever=retriever)
        tools.append(StructuredTool.from_function(private_database_query, name="query_private_database"))
    return tools


def build_analyst_graph(llm, retriever=None, charter: str = RAG_CHARTER, memory: bool = True):
    """Compile a tool-calling analyst graph.

    Supply any compatible chat model, which keeps the graph simple to test and
    compatible with OpenAI-compatible endpoints.
    """
    tools = build_tools(retriever)
    tool_enabled_llm = llm.bind_tools(tools)

    def agent_node(state: AnalystState):
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=charter), *messages]
        return {"messages": [tool_enabled_llm.invoke(messages)]}

    def route_tools(state: AnalystState):
        last = state["messages"][-1]
        return "tools" if getattr(last, "tool_calls", None) else END

    workflow = StateGraph(AnalystState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", route_tools, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    return workflow.compile(checkpointer=MemorySaver() if memory else None)
