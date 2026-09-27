"""Grounded private-document Q&A for the investment analyst."""
from __future__ import annotations

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.rag.pipeline import create_embeddings, create_retriever, load_config

RAG_PROMPT = """You are an investment research assistant. Answer using only the supplied private-document context. Cite each factual claim with its [source: page] label. If the context is insufficient, say so plainly.\n\nContext:\n{context}\n\nQuestion: {question}"""


def format_context(documents) -> str:
    """Format retrieved chunks with filename and page citations."""
    return "\n\n".join(
        f"[{str(doc.metadata.get('source', 'unknown')).replace('\\\\', '/').split('/')[-1]}: {doc.metadata.get('page', 0) + 1}]\n{doc.page_content}"
        for doc in documents
    )


def query_private_database(query: str, retriever, llm=None) -> dict[str, Any]:
    """Retrieve documents and use an LLM to answer only from their content."""
    if not query.strip():
        raise ValueError("A non-empty query is required.")
    documents = retriever.invoke(query)
    context = format_context(documents)
    if llm is None:
        from langchain_openai import ChatOpenAI
        settings = load_config()
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings["api_key"], base_url=settings["base_url"], temperature=0)
    response = llm.invoke([SystemMessage(content="Provide concise, evidence-grounded financial research."), HumanMessage(content=RAG_PROMPT.format(context=context, question=query))])
    return {"answer": response.content, "sources": [doc.metadata for doc in documents], "context": context}
