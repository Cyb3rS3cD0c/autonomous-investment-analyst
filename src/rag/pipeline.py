"""Build and load the private PDF vector database."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "Companies-AI-Initiatives"
DEFAULT_PERSIST_DIR = PROJECT_ROOT / "chroma_db"


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load local ignored configuration, allowing environment overrides."""
    path = config_path or PROJECT_ROOT / "config" / "config.json"
    values = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    return {
        "api_key": os.getenv("OPENAI_API_KEY", values.get("API_KEY")),
        "base_url": os.getenv("OPENAI_API_BASE", values.get("OPENAI_API_BASE")),
    }


def load_pdfs(data_dir: str | Path = DEFAULT_DATA_DIR):
    """Load every PDF in the company research directory."""
    directory = Path(data_dir)
    if not directory.exists():
        raise FileNotFoundError(f"PDF directory does not exist: {directory}")
    from langchain_community.document_loaders import PyPDFDirectoryLoader
    documents = PyPDFDirectoryLoader(str(directory), glob="**/*.pdf").load()
    if not documents:
        raise ValueError(f"No PDFs found in {directory}")
    return documents


def chunk_documents(documents, chunk_size: int = 1_000, chunk_overlap: int = 150):
    """Split documents into citation-preserving chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)


def create_embeddings(**overrides):
    """Create OpenAI-compatible embeddings from local configuration."""
    from langchain_openai import OpenAIEmbeddings
    settings = load_config()
    return OpenAIEmbeddings(api_key=overrides.get("api_key", settings["api_key"]), base_url=overrides.get("base_url", settings["base_url"]))


def build_vector_store(documents=None, data_dir: str | Path = DEFAULT_DATA_DIR, persist_directory: str | Path = DEFAULT_PERSIST_DIR, embeddings=None):
    """Chunk PDFs and write a persistent ChromaDB collection."""
    source_documents = documents if documents is not None else load_pdfs(data_dir)
    chunks = chunk_documents(source_documents)
    if not chunks:
        raise ValueError("No text chunks were generated from the PDFs.")
    from langchain_community.vectorstores import Chroma
    return Chroma.from_documents(chunks, embeddings or create_embeddings(), persist_directory=str(persist_directory), collection_name="company_ai_initiatives")


def create_retriever(vector_store, k: int = 4):
    """Expose a standard LangChain retriever for the private database."""
    return vector_store.as_retriever(search_kwargs={"k": k})
