**TinaAI**

An opinionated, modular AI agent stack by Tina Tsou — focused on practical, production‑minded building blocks for RAG, tools, and workflows. The repository currently includes a RAG prototype to bootstrap retrieval‑augmented answering.

**Why TinaAI**

Pragmatic first: minimal glue, maximum utility

Composable: small modules you can mix, match, or replace

Edge & developer friendly: designed with distributed/edge use cases and fast iteration in mind

Features (initial)

Retrieval‑Augmented Generation (RAG) starter

Pluggable data loaders and chunkers

Simple config for swapping models, stores, and prompts

As the project grows, this list will expand to include agents, tool use, evaluation harnesses, and deployment recipes.

**Quickstart**

**1. Clone**

git clone https://github.com/tinatsou/TinaAI.git
cd TinaAI

**2. Create env & install**
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt   # or pip install -e .

**3. Set secrets**

Create a .env (or export variables) for your model/provider keys:
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GROQ_API_KEY=...

(Use only what you need—missing providers are handled gracefully.)

**4. Run the RAG demo**

python RAG/app.py --docs ./data --query "What’s in these docs?"

Common flags:

--docs: folder or file path to index

--query: question to answer

--top_k: retrieved chunk count (default 5)

--model: override default LLM (e.g., gpt-4o-mini, claude-3-5-sonnet, etc.)

**Project structure (evolving)**

TinaAI/

├─ RAG/                 # RAG starter (ingest, index, retrieve, answer)

│  ├─ ingest.py

│  ├─ index.py

│  ├─ retriever.py

│  ├─ app.py

│  └─ ...

├─ data/                # (gitignored) sample documents

├─ requirements.txt

├─ README.md

└─ ...

**Configuration**

Most components read from environment variables and/or a config.yaml:

Embedding model: EMBEDDINGS_MODEL

LLM model: LLM_MODEL

Vector store: VECTOR_DB (e.g., faiss, chroma)

Chunking: CHUNK_SIZE, CHUNK_OVERLAP

**Data ingestion**

Add files to ./data (PDF, Markdown, text, HTML supported in the default loaders). Then:

python RAG/ingest.py --docs ./data

**Development**

Format: ruff / black

Type checks: mypy (optional)

Tests: pytest

pip install -r requirements-dev.txt
ruff check .
pytest -q

**Roadmap**

Agentic tool use (search, web, code, calculators)

Evaluations (faithfulness, answer quality, latency)

Multi‑store support (FAISS, Chroma, pgvector)

Packaging & CLI (tinaai ...)

Docker & lightweight edge deploys

**Contributing**

PRs and issues are welcome! Please:

Open an issue to discuss significant changes

Keep modules small and testable

Add/update docstrings and minimal tests

**License**

MIT — see LICENSE.

**Acknowledgements**

Inspired by the vibrant RAG and agent ecosystems. Built with ❤️ by Tina Tsou.
