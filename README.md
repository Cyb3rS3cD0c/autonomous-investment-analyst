# Autonomous Investment Analyst

An evidence-first financial research assistant built with LangGraph. It combines current market data, financial-news sentiment, and a private PDF knowledge base of company AI initiatives to produce structured research reports. It is an educational research tool, not personalized investment advice.

## Architecture

```text
User question → LangGraph agent → market / news / sentiment tools
                         └────→ private-PDF RAG retriever → cited answer
```

- `src/tools/`: Yahoo Finance prices and history, Tavily news, transparent sentiment scoring.
- `src/rag/`: PDF ingestion, chunking, OpenAI-compatible embeddings, persistent ChromaDB, and grounded Q&A.
- `src/agent/`: capability charters and an agent → tools → agent LangGraph workflow with `MemorySaver` memory.
- `tests/`: unit tests that mock external services.

## Setup

1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `config/config.example.json` to `config/config.json` (or set `OPENAI_API_KEY`, `OPENAI_API_BASE`, and `TAVILY_API_KEY` as environment variables).
4. Add research PDFs named `AMZN.pdf`, `MSFT.pdf`, `GOOGL.pdf`, `NVDA.pdf`, and `IBM.pdf` under `data/Companies-AI-Initiatives/`.
5. Build the private database with `build_vector_store()` from `src.rag.pipeline`.
6. Run `pytest`.

`config/config.json` is deliberately ignored by Git. Do not commit or publish API keys. The configured OpenAI-compatible base URL is `https://aibe.mygreatlearning.com/openai/v1`.

## Example

```python
from langchain_openai import ChatOpenAI
from src.agent.graphs import build_analyst_graph
from src.rag.pipeline import build_vector_store, create_retriever

retriever = create_retriever(build_vector_store())
llm = ChatOpenAI(model="gpt-4o-mini")
agent = build_analyst_graph(llm, retriever=retriever)
result = agent.invoke(
    {"messages": [("user", "Compare Microsoft and NVIDIA's AI initiatives.")]},
    config={"configurable": {"thread_id": "research-1"}},
)
print(result["messages"][-1].content)
```

The enhanced RAG charter asks for a thesis, evidence, risks, confidence, limitations, sources, and an **AI Research Activity** section. Live price and news results can be delayed, incomplete, or unavailable; verify all material claims against primary sources before making a decision.

## Notebook and HTML export

Open `notebooks/autonomous_financial_analyst.ipynb`, run all cells with credentials configured, and export it with:

```bash
jupyter nbconvert --to html notebooks/autonomous_financial_analyst.ipynb
```

The notebook keeps prompts and visible outputs in normal cells for straightforward HTML conversion.
