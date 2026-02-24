# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
python output/chat.py                                    # Start the chat workspace (primary interface)
python output/tools/airtable.py                          # One-time Airtable table creation
python -m pip install -r requirements.txt                # Install dependencies (pip not on PATH)
jupyter notebook lessons_en/                             # Open teaching notebooks (English)
```

## Architecture

### Chat interface

**`output/chat.py`** — Entry point (~50 lines). Validates Anthropic API key + Airtable, imports team from `agents/team.py`, starts chat via `team.cli_app()`. The team (Sonnet leader + 3 Sonnet members) is defined in `output/agents/team.py`. Members are defined in individual files: `content_writer.py`, `image_finder.py`, `aio_analyzer.py`. Each member has focused tools imported directly from `tools/`. Chat history persisted in `chat_sessions.db` (SQLite, via Agno's `SqliteDb`). This is the **primary interface**.

### Agent definitions (`output/agents/`) — "who"

One agent per file. `__init__.py` re-exports everything so `from agents import content_writer` works.
- **`content_writer.py`**: Content Writer (Claude Sonnet + DuckDuckGo + Airtable tools). Researches topics and writes SEO articles.
- **`image_finder.py`**: Image Finder (Claude Sonnet + DataForSEO Images + Airtable tools). Finds and inserts images into articles. Optional — returns `None` if no DataForSEO key.
- **`aio_analyzer.py`**: AIO Analyzer (Claude Sonnet + AIO tool functions). Analyzes Google AI Overviews and suggests optimizations.
- **`team.py`**: Agno Team assembly (Sonnet leader + 3 Sonnet members, Image Finder conditional)
- **All agents use Claude Sonnet** (Anthropic provider). No other API providers.

### Tool definitions (`output/tools/`) — "what"

Tools are capabilities that agents use. Custom toolkits inherit `agno.tools.Toolkit`. Plain functions are passed directly as `tools=[...]`.
- **`airtable.py`**: Airtable CRUD + one-time setup (primary data store). Agent-facing tool functions: `save_article()`, `list_all_articles()`, `get_article_content()`, `update_article_content()`. Internal CRUD: `create_article()`, `update_article_status()`, `get_article()`, `list_articles()`, `save_aio_analysis()`, `get_aio_analyses()`, `validate()`, `setup()`.
- **`aio.py`**: Google AI Overview analysis via DataForSEO. `AIOTools` toolkit, `get_dataforseo_credentials()`, and agent-facing tool functions: `analyze_keyword_aio()`, `optimize_for_aio()`.
- **`images.py`**: `DataForSEOImageTools` toolkit for image search via DataForSEO.
- **`__init__.py`**: Package marker.

### Database layer (`output/tools/airtable.py`)

Airtable is the primary data store. Article IDs are **strings** (Airtable record IDs like `"recABC123"`). No `init_db()` needed — just requires `AIRTABLE_PAT` and `AIRTABLE_BASE_ID` env vars. Tables: **Articles**, **AIO Analyses** (linked to Articles). SQLite is only used for Agno chat memory in `chat.py`.

### Teaching curriculum (`lessons_en/` and `lessons_vi/`)

21 Jupyter notebooks across 5 modules, available in English (`lessons_en/`) and Vietnamese (`lessons_vi/`). Modules 1-2 (Python basics + AI fundamentals) need no API keys. Module 3 builds agents (includes API calling lesson). Module 4 starts with Claude Code (the bridge from notebooks to real files), then builds the pipeline. Module 5 completes the product and extends it. Lesson 19 is "How Everything Connects".

## Project structure

```
agentic-content-seo/
├── lessons_en/                 <- Teaching curriculum (21 English notebooks)
|   ├── 01-python-basics/       (01-04: no API keys needed)
|   ├── 02-understanding-ai/    (05-07: no API keys needed, LLM concepts)
|   ├── 03-building-agents/     (08-13: needs ANTHROPIC_API_KEY)
|   ├── 04-building-the-product/ (14-17: Claude Code, then pipeline agents)
|   └── 05-complete-product/    (18-21: Airtable, connections, chat, extending)
├── lessons_vi/                 <- Vietnamese translation (same 21 notebooks)
|   ├── 01-lap-trinh-co-ban/
|   ├── 02-hieu-ve-ai/
|   ├── 03-xay-dung-agent/
|   ├── 04-xay-dung-san-pham/
|   └── 05-san-pham-hoan-chinh/
├── output/                     <- The finished product (10 Python files)
|   ├── chat.py                 <- Entry point (~50 lines, validation + start)
|   ├── agents/                 <- Agent definitions (who)
|   |   ├── __init__.py         Re-exports everything
|   |   ├── content_writer.py   Content Writer (DuckDuckGo + Airtable tools)
|   |   ├── image_finder.py     Image Finder (DataForSEO Images + Airtable tools)
|   |   ├── aio_analyzer.py     AIO Analyzer (AIO analysis tools)
|   |   └── team.py             Agno Team assembly (Sonnet leader + 3 members)
|   └── tools/                  <- Tool definitions (what)
|       ├── __init__.py         Package marker
|       ├── airtable.py         Airtable CRUD + agent-facing tool functions
|       ├── aio.py              AIO analysis + credentials + agent-facing tools
|       └── images.py           DataForSEO image search toolkit
├── content/                    <- Generated articles (.md files)
├── requirements.txt
├── README.md
├── CLAUDE.md
├── .env
└── .gitignore
```

## Key Framework Gotchas

- **All agents use Claude** (Anthropic provider). No other providers needed.
- **`DuckDuckGoTools`** requires `ddgs` package (not `duckduckgo-search`).
- **`agno.workflow`** requires `fastapi` as a transitive dependency.
- **Agno Team v2**: `mode` param is deprecated. Use `respond_directly=True` for routing, `delegate_to_all_members=True` for collaborate. `show_members_responses` -> `store_member_responses`.
- **Image Finder is optional**: `build_image_finder()` returns `None` if no DataForSEO key is set. Team skips it gracefully.
- **`get_dataforseo_credentials()`** lives in `tools/aio.py` (shared by both AIO and image search).
- **Article IDs are strings**: Airtable record IDs (e.g., `"recABC123"`), not integers.

## Environment

- Python 3.14, Windows. Use `python -m pip` (pip not on PATH).
- APIs in `.env`: `ANTHROPIC_API_KEY` (required for all agents), `DATA_FOR_SEO_API_KEY` (optional, for images and AI Overview analysis).
- Airtable in `.env`: `AIRTABLE_PAT` + `AIRTABLE_BASE_ID` (required for article storage). Run `python output/tools/airtable.py` to create the base tables.
- DataForSEO key format: `Basic <base64(login:password)>` — decoded by `tools.aio.get_dataforseo_credentials()`.
