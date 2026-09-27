from unittest.mock import MagicMock

from langchain_core.documents import Document

from src.rag.pipeline import chunk_documents, create_retriever
from src.rag.query_tool import format_context, query_private_database


def test_chunking_preserves_documents():
    chunks = chunk_documents([Document(page_content="AI investment " * 300, metadata={"source": "IBM.pdf", "page": 0})], chunk_size=100, chunk_overlap=10)
    assert len(chunks) > 1
    assert chunks[0].metadata["source"] == "IBM.pdf"


def test_context_includes_citation():
    assert "[NVDA.pdf: 2]" in format_context([Document(page_content="GPU research", metadata={"source": "C:/data/NVDA.pdf", "page": 1})])


def test_retriever_creation():
    store = MagicMock()
    create_retriever(store, k=3)
    store.as_retriever.assert_called_once_with(search_kwargs={"k": 3})


def test_query_private_database():
    retriever, llm = MagicMock(), MagicMock()
    retriever.invoke.return_value = [Document(page_content="AI projects", metadata={"source": "IBM.pdf", "page": 0})]
    llm.invoke.return_value = MagicMock(content="Grounded answer [IBM.pdf: 1]")
    result = query_private_database("What AI projects exist?", retriever, llm)
    assert result["answer"].startswith("Grounded")
