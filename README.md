# Derivé

> Step-by-step mathematical derivations between two equations, with symbolic verification.

Derivé is an educational web application for physics and mathematics 
students. Unlike tools that solve individual equations (Symbolab, 
Wolfram Alpha, MathGPT), Derivé shows the **path between two 
equations** — the sequence of verified steps that transforms a 
starting expression into a target expression.

Each derivation step is verified using a combination of symbolic 
math (SymPy), curated mathematical identities, and LLM-based 
judgment. Unverified steps are flagged honestly rather than silently 
trusted.

## Status

🚧 **Early development.** Project scaffolding and architecture 
planning. Not yet functional. See `PROJECT_STATE.md` for the 
detailed project plan and current progress.

**Target V1 completion:** End of 2026.

## Scope (V1)

Derivé V1 focuses on four domains where symbolic verification is 
reliable:

- **Classical mechanics** — Newton's laws, Lagrangian/Hamiltonian 
  mechanics, oscillations
- **Electromagnetism** — Maxwell's equations, wave equations, 
  basic electrostatics/magnetostatics
- **Calculus & analysis** — differentiation, integration techniques, 
  basic ODEs
- **Linear algebra** — matrix operations, eigenvalues, vector spaces

Advanced domains (general relativity, quantum field theory, tensor 
calculus) are deliberately deferred to future versions.

## Architecture

- **Frontend:** React with KaTeX rendering (single-page app)
- **Backend:** Python 3.11 + FastAPI
- **Data:** ChromaDB (vectors) + SQLite (dev) / PostgreSQL (prod)
- **LLMs:** DeepSeek R1 (primary), Claude Sonnet (fallback), 
  Claude Opus (evaluation judge)
- **Observability:** Langfuse

## Tech stack

Python: FastAPI · Pydantic · SQLAlchemy · SymPy · LangGraph · 
Instructor · ChromaDB · sentence-transformers · LiteLLM · Langfuse

Frontend: React · KaTeX

Tooling: uv · ruff · mypy · pytest · Docker

## Getting started

**Prerequisites:**
- Python 3.11 (managed via [uv](https://github.com/astral-sh/uv))
- Node.js 18+ (for the frontend, when we get there)
- Git

**Backend setup:**

```bash
# Clone the repository
git clone https://github.com/Khan-Easa/derive.git
cd derive

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python 3.11 and project dependencies
uv python install 3.11
uv sync

# Copy the environment template and add your API keys
cp .env.example .env
# Edit .env with your real values
```

Additional setup instructions (running the backend, frontend, 
and tests) will be added as those components are built.

## Project layout
derive/
├── frontend/           # React app
├── backend/
│   ├── src/derive/     # Python package (API, agents, RAG, etc.)
│   └── tests/
├── corpus/             # Verified derivations dataset
├── docs/               # Architecture notes
├── PROJECT_STATE.md    # Detailed project plan and progress
└── pyproject.toml      # Python project configuration

## License

MIT — see `LICENSE` for details.

## Author

Khan Easa — building Derivé as a portfolio project while 
learning AI engineering.