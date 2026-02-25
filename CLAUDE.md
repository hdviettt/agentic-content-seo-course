# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
python output/start.py                                   # Start backend + frontend together (recommended)
python output/backend/serve.py                           # Start backend only (port 7777)
cd output/frontend && npm run dev                        # Start frontend only (port 5173)
python -m pip install -r requirements.txt                # Install Python dependencies (pip not on PATH)
cd output/frontend && npm install                        # Install frontend dependencies
jupyter notebook lessons_en/                             # Open teaching notebooks (English)
```

## Architecture

### Web interface (primary)

**`output/backend/serve.py`** — FastAPI backend via Agno's `AgentOS`. Wraps the team into a web server with 50+ auto-generated endpoints (SSE streaming, health check, Swagger docs at `/docs`). Custom routes for article CRUD (`/api/articles`). Run with `python output/backend/serve.py` (port 7777).

**`output/frontend/`** — React + Vite single-page app. Chat with SSE streaming, article sidebar, full article viewer with Markdown rendering. Proxies API calls to the backend via Vite dev server (port 5173). Key components: `Chat.jsx` (streaming chat), `ArticleList.jsx` (sidebar), `ArticleView.jsx` (article reader).

### Start script

**`output/start.py`** — Launches both backend and frontend in one command. Validates API key, auto-installs frontend deps if needed, spawns both processes, handles Ctrl+C. Usage: `python output/start.py`.

### Agent definitions (`output/backend/agents/`) — "who"

One agent per file. `__init__.py` re-exports everything so `from agents import content_writer` works.
- **`content_writer.py`**: Content Writer (Claude Sonnet + DataForSEO search + storage tools). Researches topics and writes SEO articles. Search is conditional on DataForSEO key.
- **`image_finder.py`**: Image Finder (Claude Sonnet + DataForSEO Images + storage tools). Finds and inserts images into articles. Optional — returns `None` if no DataForSEO key.
- **`aio_analyzer.py`**: AIO Analyzer (Claude Sonnet + AIO tool functions). Analyzes Google AI Overviews and suggests optimizations.
- **`team.py`**: Agno Team assembly (`id="seo-workspace"`, Sonnet leader + 3 Sonnet members, Image Finder conditional). Uses `TeamMode.tasks` for parallel batch processing.
- **All agents use Claude Sonnet** (Anthropic provider). No other API providers.

### Tool definitions (`output/backend/tools/`) — "what"

Tools are capabilities that agents use. Custom toolkits inherit `agno.tools.Toolkit`. Plain functions are passed directly as `tools=[...]`.
- **`storage.py`**: Local file storage for articles. Metadata in `content/articles.json`, content in `content/{id}.md`. Agent-facing tool functions: `save_article()`, `list_all_articles()`, `get_article_content()`, `update_article_content()`. Internal: `get_article()`, `list_articles()`.
- **`search.py`**: `DataForSEOSearchTools` toolkit for web search via DataForSEO SERP API. Used by Content Writer for topic research.
- **`aio.py`**: Google AI Overview analysis via DataForSEO. `AIOTools` toolkit, `get_dataforseo_credentials()`, and agent-facing tool functions: `analyze_keyword_aio()`, `optimize_for_aio()`.
- **`images.py`**: `DataForSEOImageTools` toolkit for image search via DataForSEO.
- **`__init__.py`**: Package marker.

### Storage layer (`output/backend/tools/storage.py`)

Local file storage. Article IDs are **keyword slugs** (e.g., `"on-page-seo-meta-tags"`). Articles stored as `.md` files in `content/`, metadata in `content/articles.json`. No external services, no env vars needed for storage. SQLite is only used for Agno chat memory (team session history).

### Teaching curriculum (`lessons_en/` and `lessons_vi/`)

22 Jupyter notebooks across 5 modules, available in English (`lessons_en/`) and Vietnamese (`lessons_vi/`). Modules 1-2 (Python basics + AI fundamentals) need no API keys. Module 3 builds agents (08-12, includes storage). Module 4 is AI-assisted development (13-18): paradigm shift, Claude Code usage, prompting/planning/learning, then building agents through Claude Code lens. Module 5 completes the product (19-22): architecture, web fundamentals, web interface, extending.

## Project structure

```
agentic-content-seo/
├── output/                        <- The finished product
|   ├── start.py                   Start backend + frontend together
|   ├── backend/                   <- Python backend (11 files)
|   |   ├── serve.py               Web backend entry point (AgentOS + article API)
|   |   ├── agents/                Agent definitions (who)
|   |   |   ├── __init__.py        Re-exports everything
|   |   |   ├── content_writer.py  Content Writer (DataForSEO search + storage tools)
|   |   |   ├── image_finder.py    Image Finder (DataForSEO Images + storage tools)
|   |   |   ├── aio_analyzer.py    AIO Analyzer (AIO analysis tools)
|   |   |   └── team.py            Agno Team assembly (Sonnet leader + 3 members)
|   |   └── tools/                 Tool definitions (what)
|   |       ├── __init__.py        Package marker
|   |       ├── storage.py         Local file storage (JSON metadata + .md files)
|   |       ├── search.py          DataForSEO web search toolkit
|   |       ├── aio.py             AIO analysis + credentials + agent-facing tools
|   |       └── images.py          DataForSEO image search toolkit
|   └── frontend/                  <- React + Vite web app
|       ├── package.json
|       ├── vite.config.js         Proxy /api, /teams, /health → backend
|       ├── index.html
|       └── src/
|           ├── main.jsx           React entry point
|           ├── App.jsx            Layout (sidebar + main area)
|           ├── api.js             API client (fetch + SSE streaming)
|           └── components/
|               ├── Chat.jsx       Chat with SSE streaming + Markdown
|               ├── ArticleList.jsx Sidebar article list (polling)
|               └── ArticleView.jsx Full article viewer (Markdown)
├── content/                       <- Generated articles (.md files + articles.json)
├── lessons_en/                    <- Teaching curriculum (22 English notebooks)
|   ├── 01-python-basics/          (01-04: no API keys needed)
|   ├── 02-understanding-ai/       (05-07: no API keys needed, LLM concepts)
|   ├── 03-building-agents/        (08-12: agents, tools, structured output, chaining, storage)
|   ├── 04-ai-assisted-development/ (13-18: Claude Code paradigm + usage + skills, then building agents)
|   └── 05-complete-product/       (19-22: architecture, web fundamentals, web interface, extending)
├── lessons_vi/                    <- Vietnamese translation (same 22 notebooks)
|   ├── 01-lap-trinh-co-ban/
|   ├── 02-hieu-ve-ai/
|   ├── 03-xay-dung-agent/
|   ├── 04-phat-trien-voi-ai/
|   └── 05-san-pham-hoan-chinh/
├── requirements.txt
├── README.md
├── CLAUDE.md
├── .env
└── .gitignore
```

## Key Framework Gotchas

- **All agents use Claude** (Anthropic provider). No other providers needed.
- **AgentOS**: `from agno.os import AgentOS` wraps Teams into FastAPI with SSE streaming. Accepts `base_app` for custom routes. Teams need `id` param for clean API paths (e.g., `/teams/seo-workspace/runs`).
- **`agno.workflow`** requires `fastapi` as a transitive dependency.
- **Agno Team**: Uses `TeamMode.tasks` for parallel batch processing with `execute_tasks_parallel`.
- **Image Finder is optional**: `build_image_finder()` returns `None` if no DataForSEO key is set. Team skips it gracefully.
- **Content Writer search is conditional**: If no DataForSEO key, the writer still works but without web search.
- **`get_dataforseo_credentials()`** lives in `tools/aio.py` (shared by search, AIO, and image toolkits).
- **Article IDs are keyword slugs** (e.g., `"on-page-seo-meta-tags"`), not integers or timestamps.

## Environment

- Python 3.14, Windows. Use `python -m pip` (pip not on PATH).
- APIs in `.env`: `ANTHROPIC_API_KEY` (required for all agents), `DATA_FOR_SEO_API_KEY` (required for web search, images, and AI Overview analysis).
- DataForSEO key format: `Basic <base64(login:password)>` — decoded by `tools.aio.get_dataforseo_credentials()`.
