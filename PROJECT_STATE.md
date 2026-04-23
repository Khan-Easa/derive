# Derivé — Project State

**Last updated:** 2026-04-23
**Current section:** Section 2 — SymPy feasibility spike (in progress)

---

## 1. Project Overview

Derivé is an educational web application that generates step-by-step 
mathematical derivations between two equations. The user provides a 
starting equation and a target equation, optionally specifies a method 
or context, and receives a rigorous, verified derivation transforming 
one into the other.

**Core differentiator:** Unlike Symbolab, MathGPT, or Wolfram Alpha 
which solve single equations, Derivé shows the *path* between two 
equations — with symbolic verification on each step.

**Target audience:** Physics undergraduates, early graduate students, 
and self-learners working through textbook derivations (Griffiths, 
Jackson, Sakurai, Goldstein level).

**Project goals:**
1. **Primary:** Portfolio piece for junior/mid-level AI engineering 
   job applications (target: end of 2026 / early 2027)
2. **Co-equal:** Just-in-time, project-driven learning of AI 
   engineering concepts
3. **Secondary:** If the product turns out well, make it 
   production-ready for real users

**Constraints:**
- Timeline: ~8 months, target completion end of December 2026
- Time commitment: 2–4 hours/day (~20 hrs/week)
- Budget: up to $100/month for APIs, models, databases
- Developer skill level: beginner-to-intermediate Python, learning 
  AI engineering from scratch through this project
- No manual verification of derivations (rusty on physics, relying 
  on automated verification instead)

---

## 2. Locked Decisions

### 2.1 Product Scope

**Domains for V1 (4 total):**
1. Classical mechanics — Newton's laws, Lagrangian/Hamiltonian 
   mechanics, oscillations, basic orbital mechanics
2. Electromagnetism — Maxwell's equations, wave equations, basic 
   electrostatics/magnetostatics, circuits
3. Calculus / Analysis — differentiation, integration techniques, 
   series, basic ODEs, vector calculus basics
4. Linear Algebra — matrix operations, eigenvalues/eigenvectors, 
   vector spaces, basic transformations

**Explicitly out of scope for V1:** General Relativity, Quantum Field 
Theory, tensor calculus, differential forms, advanced statistical 
mechanics, advanced quantum mechanics. These domains are where SymPy 
verification breaks down and are deferred.

**Corpus target:** ~300 verified derivations for V1.

**Student levels supported:** Beginner, Intermediate, Advanced (already 
implemented as a UI toggle in the frontend).

### 2.2 Architecture

**Three-tier architecture:**
- Frontend: React (JSX) with KaTeX — already built as a single-file 
  component; to be converted to a proper Vite + React project in Section 4
- **Design reference:** A Streamlit prototype (`app.py`) exists as an 
  earlier design iteration. It is not the production frontend — React 
  is. The Streamlit version is kept as a design reference only.
- Backend: Python 3.11+ with FastAPI — to be built
- Data layer: ChromaDB (vectors) + SQLite→PostgreSQL (relational)

**Pattern:** Agentic RAG with symbolic verification (not pure RAG).

**Deployment targets:**
- Frontend: Vercel (free tier)
- Backend: Railway (Hobby plan, containerized)
- PostgreSQL: Supabase (free tier)
- ChromaDB: Self-hosted alongside backend container
- Langfuse: Their cloud (free tier)

**Containerization:** Backend containerized via Docker in Month 7 
(polish phase). Frontend deploys as static build to Vercel, no 
container needed.

### 2.3 LLM Strategy

**Primary reasoning model:** DeepSeek R1 (~$20–30/month)  
**Fallback for hard derivations:** Claude Sonnet 4.6 (~$25–35/month)  
**LLM judge for evaluation:** Claude Opus 4.7 (~$15–25/month)  
**Embeddings:** sentence-transformers (local, free)

**Budget allocation target:** ~$75–90/month actual, ~$10/month buffer.

### 2.4 Verification Architecture

Steps are categorized into 5 types, each with a distinct 
verification strategy:

- **Category A — Algebraic manipulation:** SymPy equivalence check
- **Category B — Calculus operations:** SymPy with variable hints
- **Category C — Named identity application:** Identity database 
  lookup + pattern match
- **Category D — Physical/contextual assumptions:** LLM judge 
  evaluation (not symbolic)
- **Category E — Notational/structural:** SymPy substitution check, 
  fallback to LLM judge

  **Role of the Method/Context field (user input):**

The third user input — "Method / Context" — is the primary mechanism 
for providing the LLM with:

1. **Method guidance:** Which technique to apply (e.g., "using Fourier 
   Transform", "via calculus of variations", "by vector identity"). 
   Shapes the derivation path the LLM takes.
2. **Physical or contextual assumptions:** Premises the user accepts 
   as given (e.g., "in free space, ∇·E = 0", "steady-state", 
   "small-angle approximation", "ideal gas"). Injected into the 
   prompt as premises for the derivation.

**Key design decision:** User-stated assumptions are treated as 
**premises, not conclusions.** The verifier does not judge whether 
an assumption is physically reasonable in the broader sense — that 
responsibility sits with the user. The system's verification job is 
narrower: given the stated premises, is each step a valid 
transformation?

**Implications:**

- Keeps Category D (physical/contextual assumptions) small and 
  tractable. The LLM judge only checks that stated assumptions are 
  applied correctly within the derivation — not that they are 
  appropriate for the problem in general.
- Mirrors how textbook derivations work: assumptions are stated, 
  then derivations proceed from them. The tool does not try to 
  second-guess the user's framing.
- Sets honest user expectations. The UI should make clear (in 
  Section 4 or polish phase) that the system verifies logical 
  consistency given premises, not premise validity itself.

**LLM output format:** Dual representation — each step includes 
both LaTeX (for display) and SymPy-compatible expressions (for 
verification). LLM generates both; SymPy parses the SymPy form 
rather than trying to parse LaTeX directly.

**Identity database:** ~50–100 curated mathematical identities for 
Category C verification. To be built in Month 3–4.

**LLM judge fallback:** Claude evaluates steps that fail automated 
verification. Used both as a backstop and as a quality check on 
difficult steps.

**Target verification coverage:**
- ~70–80% rigorously verified (SymPy or identity lookup)
- ~15–20% LLM-judged
- ~5–10% flagged as unverified to the user (presented honestly)

**Product decision:** Unverified steps are shown with a visible 
status indicator, not silently trusted. Honest flagging is a 
feature, not a bug.

**User-facing output format:** The frontend displays rendered mathematical 
notation via KaTeX. The backend sends LaTeX strings as part of the API 
response; KaTeX converts them to visual math before display. SymPy 
expressions are internal to the backend only — used for verification, 
never shown to the user. The user sees formatted equations, not raw 
LaTeX source.


### 2.5 Tech Stack

**Backend:**
- FastAPI — async web framework
- Pydantic — data validation, structured LLM outputs
- SQLAlchemy — ORM for relational DB
- ChromaDB — vector database (self-hosted, embedded library)
- sentence-transformers — local embeddings
- LiteLLM — unified multi-provider LLM interface
- SymPy — symbolic math for verification
- LangGraph — agent orchestration (ReAct pattern, tool use)
- Instructor — structured LLM outputs via Pydantic
- Langfuse — LLM observability
- tenacity — retry logic with exponential backoff
- httpx — async HTTP client

**Development tooling:**
- uv — Python package management
- ruff — linter and formatter
- mypy — static type checker
- pytest + pytest-asyncio — testing

**Frontend (already built, no major changes planned):**
- React with hooks
- KaTeX (loaded via CDN)
- EB Garamond + JetBrains Mono fonts

### 2.6 Phase Sequencing (8 months)

| Month | Focus |
|-------|-------|
| 1 | Foundations + SymPy feasibility spike + minimal end-to-end pipeline |
| 2 | Evaluation harness + test set (100 gold-standard derivations) |
| 3 | RAG pipeline + corpus v1 (~100 derivations) |
| 4 | Agentic tools via LangGraph (SymPy verifier, identity lookup, LaTeX validator, RAG-as-tool) |
| 5 | Corpus expansion (~300) + prompt engineering on starting→target framing |
| 6 | Multi-model routing + Langfuse integration + cost tracking |
| 7 | Production polish (error handling, graceful degradation, tests, CI/CD, Docker) |
| 8 | Buffer for slippage + README + cleanup |

### 2.7 Quality Commitments

- **Polish throughout, not at the end.** Error handling, logging, 
  tests, type hints, Pydantic validation are built in from day one.
- **Graceful degradation.** LLM timeouts, SymPy parse failures, 
  empty RAG results all have explicit handling paths.
- **Structured logging from the first endpoint.**
- **Type hints on every function.**
- **Pydantic validation on every API boundary.**
- **No hardcoded file paths or configuration values.**
- **Clear separation of concerns** (no oversized files).
- **Environment variables managed cleanly from the start.**

---

## 3. Section Plan

Build is structured as ~12 sections, completed sequentially. Each 
section has its own focused build chat(s), but all share context via 
this document.

| # | Section | Notes |
|---|---------|-------|
| 1 | Project setup and repository structure | Dev env, folder layout, tooling install |
| 2 | SymPy feasibility spike | Validate verification approach before committing architecture |
| 3 | Minimal backend skeleton | FastAPI + Pydantic + DeepSeek integration, one endpoint |
| 4 | Frontend-backend integration | Replace mock with real API; preserve cursor-stability logic |
| 5 | Evaluation harness + test set | 100 gold-standard derivations, automated checks, LLM judge |
| 6 | RAG pipeline | Embeddings, ChromaDB, retrieval |
| 7 | Corpus v1 | Scale to ~100 derivations, then ~300 |
| 8 | Verification tools | SymPy verifier, identity database, LaTeX validator |
| 9 | Agent loop | LangGraph, tool calling, ReAct pattern |
| 10 | Multi-model routing | DeepSeek primary, Claude Sonnet fallback |
| 11 | Observability | Langfuse integration, cost tracking, tracing |
| 12 | Polish and production-readiness | Error handling, deployment, Docker, README |

---

## 4. Current Status

**In progress:** Section 2 — SymPy feasibility spike (infrastructure phase complete).  
**Completed:** Planning phase, Section 1 (project setup and repository structure).  
**Next:** Author 3 test derivations, then set up DeepSeek, then run Experiment 1.

---

## 5. Section-by-Section Log

*(Entries will be added here as each section completes. Each entry 
captures: goal, what was built, key decisions made, deliverables, 
any deviations from the original plan.)*

### Section 1 — Project setup and repository structure
**Completed:** 2026-04-21

**Goal:** Establish the development environment, repository structure, 
and tooling baseline for the entire project.

**What was built:**
- WSL 2 + Ubuntu 24.04 environment on Windows 11
- Python 3.11.15 installed via uv (managed separately from system Python 3.12)
- Claude Code installed in WSL for implementation assistance
- Git repository initialized with `main` as default branch
- Monorepo folder structure with `frontend/`, `backend/`, `corpus/`, `docs/`
- Python src-layout at `backend/src/derive/` with module folders for 
  api, agents, llm, rag, database, verification, evaluation, observability
- Core configuration files: `pyproject.toml`, comprehensive `.gitignore`, 
  `.env.example` template, minimal `README.md`
- Development tooling installed and configured: pytest, pytest-asyncio, 
  ruff, mypy
- Strict mypy configuration (strict mode enabled)
- Ruff configured for Python 3.11, line length 100, with select lint 
  rule groups (E, W, F, I, B, C4, UP, N, SIM, RUF)
- pytest configured to use `asyncio_mode = "auto"` for FastAPI async tests
- uv lockfile (`uv.lock`) committed for reproducible builds

**Key decisions made:**
- **WSL over native Windows** — matches Linux production environment, 
  eliminates OS-specific friction with AI/ML libraries
- **uv as the Python toolchain** — replaces pip, venv, pyenv, poetry 
  with one fast tool; chosen for speed and modern standards
- **Python 3.11 (locked, not newer)** — best library compatibility 
  across our stack; `requires-python = ">=3.11,<3.12"` in pyproject.toml
- **Monorepo layout** — frontend and backend in single repository; 
  deployed separately (Vercel and Railway) from subdirectories
- **Src-layout** (`backend/src/derive/`) — prevents accidental imports 
  of local files, industry-standard for Python packages
- **`[dependency-groups]` over `[tool.uv].dev-dependencies`** — using 
  the newer PEP 735 standard, not uv's deprecated syntax
- **MIT license** — permissive, standard for open-source portfolio 
  projects
- **Mypy strict mode from day one** — easier than retrofitting strictness 
  later; teaches good typing habits as the project grows
- **Conventional Commits** — commit message format (feat:, fix:, chore:, 
  docs:, etc.) adopted as a project-wide convention

**Deliverables:**
- Working development environment runnable from WSL terminal
- `uv sync` restores full environment from committed state
- `uv run ruff check backend/src` — passes cleanly
- `uv run ruff format --check backend/src` — all files formatted
- `uv run mypy backend/src` — no type errors
- `uv run pytest backend/tests` — pytest launches, 0 tests collected
- Initial git commit on `main` branch, pushed to GitHub as 
  public/private repository at github.com/Khan-Easa/derive

**Deviations from plan:**
- Added Claude Code installation mid-section (originally not planned 
  for Section 1) — used for implementation assistance in later sections
- `uv init` auto-initialized git (newer uv behavior) — merged with our 
  plan rather than conflicting with it


---

### Section 2 — SymPy feasibility spike (in progress)
**Started:** 2026-04-22

**Goal:** Validate the verification architecture in Section 2.4 by 
testing its load-bearing assumptions before building production code 
on top of it.

**Progress so far — infrastructure phase:**
- Anthropic API account set up with $10 credit balance
- API key stored in `.env`, verified gitignored (line 67 of .gitignore)
- `anthropic==0.96.0` and `python-dotenv==1.2.2` added as dependencies
- `spike/` folder created at repo root for throwaway spike code
- `spike/verify_anthropic.py` confirms Anthropic API works end-to-end
- First successful API call completed against `claude-sonnet-4-6`

**Key decisions made:**
- **Spike scope — four experiments.** (1) LLM LaTeX-to-SymPy 
  translation quality, (2) SymPy equivalence reliability on 
  equivalent/non-equivalent expression pairs, (3) end-to-end step 
  generation and verification, (4) actual category (A/B/C/D/E) 
  distribution audit. Experiments 1 and 2 run first; 3 and 4 only 
  if 1 and 2 clear.
- **Success thresholds (preliminary, revisable).** Green/yellow/red 
  rubric per experiment: Experiment 1 at ≥90% parse / ≥80% semantic 
  match is green; Experiment 2 at ≥95% true-positive rate is green; 
  Experiment 3 at ≥70% full-derivation verification is green; 
  Experiment 4 at ≥60% A+B+C share is green.
- **Test set sourcing.** Derivations will be hand-authored from 
  canonical textbooks (Griffiths, Boas, Strang, Taylor) where the 
  ground truth is already established in print. Working around 
  physics rustiness by selecting mostly-algebraic-with-physics-
  layered-on derivations and cross-checking with Claude. Spike 
  test set is separate from and smaller than the eventual corpus.
- **Slice strategy.** Build 3 test derivations first, validate the 
  Experiment 1 pipeline on them, then scale to 15–20 only if the 
  pipeline works. Avoids authoring a large test set on a broken 
  measurement apparatus.
- **Models to compare.** DeepSeek (per original Section 2.3 plan) 
  against Claude Sonnet 4.6, run on the same test set. Divergence 
  between models is itself a meaningful finding for the primary-model 
  decision.
- **DeepSeek setup deferred.** Anthropic infrastructure validated 
  first; DeepSeek to be set up just before Experiment 1 runs. 
  Avoids dual-provider setup friction upfront.
- **Model selection open.** Original plan specified DeepSeek R1. 
  DeepSeek has since released R2 (newer reasoner) and V3.2 (unified 
  model). Exact DeepSeek model for the spike to be chosen at setup 
  time.

**Next up:**
- Author calc_taylor_001 (Taylor series of sin(x) around 0), 
  independently, using em_wave_001 and cm_shm_001 as templates
- DeepSeek API setup
- Write Experiment 1 script, run on 3-derivation sample
- Scale to 15-20 derivations if first pass is clean

**Findings so far — authoring Derivation 1 (Maxwell's → wave eq.):**

- **Product insight refined: Derivé fills *non-trivial* gaps.** The 
  core value is expanding the derivation steps textbook authors 
  skip — but not every transformation warrants a step. Trivial 
  normalizations (grad(0) → 0, Derivative(Derivative(E, t), t) → 
  Derivative(E, t, 2)) should be folded into adjacent non-trivial 
  steps, not listed separately. Authoring principle: each step 
  must represent a transformation a student could plausibly be 
  stuck on.

- **SymPy aggressively normalizes at parse time.** Any transformation 
  SymPy considers trivial will be pre-applied during sympify(). 
  Test case steps that represent only such transformations will 
  appear identical to their predecessor. Validator catches this by 
  detecting duplicate parsed forms.

- **Representation convention for vector calculus (Approach 3 — 
  hybrid):** vector fields (E, B) and vector operators (curl_E, 
  laplacian_E, etc.) are opaque SymPy Function(t) objects — 
  time-dependent so Derivative() works, but otherwise symbolic. 
  This makes Category A/B steps SymPy-verifiable while Category 
  C/D/E steps are marked sympy_verifiable=false and deferred to 
  identity lookup, LLM judge, or structural checks.

- **First test case category distribution:** A=3, C=1, D=2, E=2 
  out of 8 steps. A+B+C share = 50%, below the 60% green threshold. 
  Note: this derivation is vector-calculus-heavy; calculus and 
  linear algebra test cases expected to shift the balance. 
  Distribution verdict deferred until all 3 test cases authored.

- **SymPy normalization pattern confirmed across domains.** The same 
  auto-normalization behavior observed in em_wave_001 (grad(0) → 0, 
  nested derivatives collapsing) also appeared in cm_shm_001 with 
  fraction cancellation ((-m*g*l*θ)/(m*l²) → -g*θ/l). This is now 
  treated as a reliable pattern, not a one-off: test cases must 
  represent transformations SymPy cannot trivially normalize away.

- **Second test case category distribution:** A=1, D=1 out of 2 
  steps. Combined across em_wave_001 + cm_shm_001: A=4, C=1, D=3, 
  E=2 out of 10 total steps. A+B+C share = 50%. Still below 60% 
  green threshold; calc_taylor_001 expected to shift balance toward 
  B-heavy content.

---

## 6. Open Questions

Items flagged during planning but not yet resolved. These will be 
settled when their relevant section is reached.

- **Exact Pydantic schema for a derivation step.** Structure 
  agreed (dual LaTeX + SymPy representation, step type 
  classification) but concrete field names and types not yet 
  specified. Will be settled when we design the data model.
  
- **Identity database seed list and schema.** Scope agreed 
  (~50–100 entries across the 4 domains) but no concrete list or 
  structure yet. Will be settled in Section 8.

- **Feasibility spike specifics — partially resolved.** Four 
  experiments defined with preliminary success thresholds (logged 
  in Section 5, Section 2 entry). Remaining unknowns: exact 15–20 
  test derivations, final prompt template for Experiment 1, and 
  whether DeepSeek R1/R2/V3.2 is the right choice. Will be fully 
  closed when the spike concludes.

- **DeepSeek model for the spike.** Original plan (Section 2.3) 
  specified R1. R2 and V3.2 have since been released. Decision 
  deferred to DeepSeek setup session.

---

## 7. Tech Stack Quick Reference

*(Single-glance reference for any new chat.)*

**Languages:** Python 3.11+, JavaScript (React)  
**Backend framework:** FastAPI  
**Data validation:** Pydantic  
**LLM orchestration:** LangGraph  
**LLM interface:** LiteLLM  
**LLM output structuring:** Instructor  
**Vector DB:** ChromaDB (embedded, self-hosted)  
**Relational DB:** SQLite (dev) → PostgreSQL via Supabase (prod)  
**Embeddings:** sentence-transformers (local)  
**Symbolic math:** SymPy  
**Observability:** Langfuse  
**Package manager:** uv  
**Linter/formatter:** ruff  
**Type checker:** mypy  
**Testing:** pytest, pytest-asyncio  
**Deployment:** Vercel (frontend), Railway (backend), Supabase (DB)  
**Containerization:** Docker (backend only, Month 7)

**LLMs used:**
- DeepSeek (model TBD — R1/R2/V3.2 decision deferred to Section 2 spike) — primary reasoning
- Claude Sonnet 4.6 — fallback for hard derivations
- Claude Opus 4.7 — evaluation judge

---

## 8. Conventions

*(These may evolve; will be expanded as decisions come up during 
build sections.)*

**Naming:**
- Python: `snake_case` for variables/functions, `PascalCase` for classes
- API routes: lowercase with hyphens (e.g., `/derive`, `/user-history`)
- Database columns: `snake_case`
- Environment variables: `UPPER_SNAKE_CASE`
- React components: `PascalCase`
- Files: `snake_case.py` for Python, `camelCase.jsx` for React

**Git:**
- Conventional Commits format: `type: description`
  - Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `style`
- Small, focused commits
- Never commit `.env` or API keys
- Default branch: `main`

**Code quality:**
- Ruff for linting and formatting — run before every commit
- Mypy strict mode — type hints required on every function
- pytest with asyncio auto mode — async tests don't need decorators
- Line length: 100 characters
- Quote style: double quotes
- Indentation: 4 spaces (Python), 2 spaces (JSON/YAML/Markdown lists)

**Project layout:**
- Monorepo structure (`frontend/`, `backend/`, `corpus/`, `docs/`)
- Python src-layout (`backend/src/derive/` is the package root)
- One `__init__.py` per Python package folder
- Tests live in `backend/tests/`, mirroring the source structure

**Environment:**
- WSL 2 (Ubuntu 24.04) for development
- Python 3.11 (managed by uv, isolated from system Python)
- Linux filesystem (`~/projects/derive`) — never work from `/mnt/c/` or `/mnt/d/`

*(Additional conventions — folder structure, import style, logging 
format, etc. — will be added as they're decided during Section 1 
and beyond.)*

---

## 9. How to Use This Document

**In a new planning chat:** Paste the entire document at the start 
of your first message. Claude now has full project context.

**In a new build chat (Claude.ai):** Same — paste the document at 
the start. Add any section-specific context (like the current 
section's goals or your specific question) after.

**In Claude Code (local):** This file sits in the project root. 
Claude Code can read it directly when needed, either by being 
asked to or when working on files that reference it.

**Updating the document:** After each section completes, add a log 
entry in Section 5, update "Current Status" in Section 4, resolve 
any open questions in Section 6, and add any new conventions in 
Section 8. Commit the updated file with a message like 
`docs: update project state after section 3`.