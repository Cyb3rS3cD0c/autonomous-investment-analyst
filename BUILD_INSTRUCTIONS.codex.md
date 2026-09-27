Project: Autonomous Investment Analyst
Root Folder
Create the following root folder (if not already present):

Code
autonomous-investment-analyst/
Open this folder in VS Code before continuing.

1. Create Project Structure
Inside autonomous-investment-analyst/, create the following directories:

Code
config/
data/
data/Companies-AI-Initiatives/
notebooks/
src/
src/tools/
src/rag/
src/agent/
src/utils/
tests/
2. Create Configuration File
Create:

Code
config/config.json
Insert:

json
{
  "API_KEY": "YOUR_OPENAI_COMPATIBLE_API_KEY",
  "OPENAI_API_BASE": "https://aibe.mygreatlearning.com/openai/v1",
  "TAVILY_API_KEY": "YOUR_TAVILY_KEY_HERE"
}
Add config.json to .gitignore.

3. Create Requirements File
Create:

Code
requirements.txt
Insert:

Code
langchain==0.3.27
langchain-core==0.3.79
langchain-openai==0.3.11
langchain-community==0.3.31
langgraph==0.3.7
tavily-python
yfinance==0.2.66
chromadb==1.3.4
pypdf==6.2.0
tiktoken==0.12.0
4. Create Tool Modules
src/tools/financial_tools.py
Create stubs for:

get_stock_price()

get_stock_history()

src/tools/news_tools.py
Create stub for:

search_financial_news()

src/tools/sentiment_tools.py
Create stub for:

analyze_sentiment()

5. Create RAG Modules
src/rag/pipeline.py
Implement:

PDF loading

Chunking

Embeddings

ChromaDB vector store

Retriever creation

src/rag/query_tool.py
Implement:

query_private_database()

RAG prompt formatting

LLM invocation

6. Create Agent Modules
src/agent/charters.py
Create:

TRADITIONAL_CHARTER

BASIC_CHARTER

FULL_CHARTER

RAG_CHARTER

src/agent/graphs.py
Create:

LangGraph workflow builder

Agent node

Tool node

Routing logic

Memory integration

7. Create Utility Modules
src/utils/logging.py
Create:

Logging configuration

Helper functions

8. Create Notebook
Create:

Code
notebooks/autonomous_financial_analyst.ipynb
Codex should populate:

Part 1 (Tools + Agents)

Part 2 (RAG + Ranking)

All tests

HTML‑conversion‑ready formatting

9. Create Test Suite
tests/test_tools.py
Test:

stock tools

news tools

sentiment tools

tests/test_rag.py
Test:

PDF loading

chunking

embeddings

retrieval

tests/test_agents.py
Test:

traditional agent

basic agent

full agent

enhanced RAG agent

10. Create README.md
Create:

Code
README.md
Populate with the full project description, architecture, instructions, and your API key + base URL.

11. Populate Data Folder
Place the following PDFs into:

Code
data/Companies-AI-Initiatives/
AMZN.pdf

MSFT.pdf

GOOGL.pdf

NVDA.pdf

IBM.pdf

12. Begin Code Generation
After creating all folders and empty files, Codex should:

Fill in each module with working Python code.

Build the LangGraph agent.

Build the RAG pipeline.

Build the notebook.

Build the tests.
