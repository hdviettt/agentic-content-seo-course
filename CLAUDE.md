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

**`output/chat.py`** — Entry point only (~60 lines). Validates API keys + Airtable, imports team from `agents/team.py`, starts chat. The team (Opus 4.6 leader + 3 Sonnet members) is defined in `output/agents/team.py`. Members defined in individual files: `content_creator.py`, `status_tracker.py`, `seo_manager.py`. Members have focused tools from `tools/workspace.py` that wrap pipeline and Airtable calls. Content Creator also handles retry and CSV import. Chat history persisted in `chat_sessions.db` (SQLite, via Agno's `SqliteDb`). This is the **primary interface**.

### Content pipeline (`output/pipeline.py`)

Plain Python function that runs 4 sequential agent steps with Airtable status updates between each:

```
queued -> researching -> outlining -> writing -> enriching -> review -> published
          research_agent  outline_agent  writer_agent  image_agent   (manual)
          (Sonnet + DDG)  (Sonnet)       (Grok-4)      (Sonnet)
                              | Airtable updated at each step
```

On error at any step: `status -> error` with `error_message` saved. Batch processing (`run_batch()` in same file) supports both sequential (default) and parallel mode (`parallel=True` uses `ThreadPoolExecutor` to process multiple articles simultaneously). Articles saved to `content/`.

### Agent definitions (`output/agents/`)

One agent per file. `__init__.py` re-exports everything so `from agents import research_agent` works.
- **`schemas.py`**: `ContentOutline`, `EnrichedContent`, `OutlineSection`, `ImageSuggestion` (Pydantic models)
- **`researcher.py`**: Research Agent (Claude Sonnet + DuckDuckGo)
- **`outliner.py`**: Outline Agent (Claude Sonnet + `output_schema`)
- **`writer.py`**: Writer Agent (Grok-4, plain Markdown, no tools, no `output_schema`)
- **`image.py`**: Image Agent + `FreepikTools`, `DataForSEOTools`, `get_dataforseo_credentials()`, `build_image_agent()`
- **`content_creator.py`**: Chat team member (creates articles, retries, CSV import)
- **`status_tracker.py`**: Chat team member (queries articles, version history)
- **`seo_manager.py`**: Chat team member (rankings, published URLs)
- **`team.py`**: Agno Team assembly (Opus 4.6 leader + 3 Sonnet members)
- **Claude Sonnet** for research, outline, image, and chat member agents.
- **Grok-4** for writer agent only (cannot combine tools with structured output).
- **Opus 4.6** only for conversational team leader in `agents/team.py`.

### Database layer (`output/tools/airtable.py`)

Airtable is the primary data store. Article IDs are **strings** (Airtable record IDs like `"recABC123"`). No `init_db()` needed — just requires `AIRTABLE_PAT` and `AIRTABLE_BASE_ID` env vars. Functions: `create_article()`, `update_article_status()`, `get_article()`, `list_articles()`, `save_article_version()`, `get_article_versions()`, `save_ranking()`, `get_rankings()`, `set_published_url()`, `validate()`, `setup()`. Tables: **Articles**, **Versions** (linked to Articles), **Rankings** (linked to Articles). SQLite is only used for Agno chat memory in `chat.py`.

### Rank tracking (`output/tools/rankings.py`)

Uses DataForSEO SERP API to check keyword positions. `check_article_rankings()` queries each keyword, saves results to Airtable Rankings table. Requires `DATA_FOR_SEO_API_KEY` and a `published_url` set on the article.

### Tools pattern

Custom toolkits inherit `agno.tools.Toolkit`, pass function refs to `super().__init__(name=..., tools=[...])`. All tool functions return JSON strings. Workspace tools (`output/tools/workspace.py`) are plain Python functions passed directly as `tools=[...]` to team members.

### Teaching curriculum (`lessons_en/` and `lessons_vi/`)

20 Jupyter notebooks across 5 modules, available in English (`lessons_en/`) and Vietnamese (`lessons_vi/`). Modules 1-2 (Python basics + AI fundamentals) need no API keys. Module 3 builds agents. Module 4 starts with Claude Code (the bridge from notebooks to real files), then builds the pipeline. Module 5 completes the product and extends it. Lesson 18 is "How Everything Connects".

## Project structure

```
agentic-content-seo/
├── lessons_en/                 <- Teaching curriculum (20 English notebooks)
|   ├── 01-python-basics/       (01-04: no API keys needed)
|   ├── 02-understanding-ai/    (05-07: no API keys needed, LLM concepts)
|   ├── 03-building-agents/     (08-12: needs ANTHROPIC_API_KEY)
|   ├── 04-building-the-product/ (13-16: Claude Code, then pipeline agents)
|   └── 05-complete-product/    (17-20: Airtable, connections, chat, extending)
├── lessons_vi/                 <- Vietnamese translation (same 20 notebooks)
|   ├── 01-python-co-ban/
|   ├── 02-hieu-ve-ai/
|   ├── 03-xay-dung-agent/
|   ├── 04-xay-dung-san-pham/
|   └── 05-san-pham-hoan-chinh/
├── output/                     <- The finished product (16 Python files)
|   ├── chat.py                 <- Entry point (~60 lines, validation + start)
|   ├── pipeline.py             Content pipeline orchestrator
|   ├── agents/                 <- One agent per file
|   |   ├── __init__.py         Re-exports everything
|   |   ├── schemas.py          Pydantic models (ContentOutline, EnrichedContent, etc.)
|   |   ├── researcher.py       Research Agent (Claude Sonnet + DuckDuckGo)
|   |   ├── outliner.py         Outline Agent (Claude Sonnet + structured output)
|   |   ├── writer.py           Writer Agent (Grok-4, plain Markdown)
|   |   ├── image.py            Image Agent + FreepikTools + DataForSEOTools
|   |   ├── content_creator.py  Chat team member (creates articles)
|   |   ├── status_tracker.py   Chat team member (queries articles)
|   |   ├── seo_manager.py      Chat team member (rankings + URLs)
|   |   └── team.py             Agno Team assembly (Opus leader + 3 members)
|   └── tools/                  <- Toolkits, integrations, and utilities
|       ├── __init__.py         Package marker
|       ├── airtable.py         Airtable CRUD + one-time setup (primary data store)
|       ├── workspace.py        Chat team member tools
|       └── rankings.py         SERP rank checking via DataForSEO
├── content/                    <- Generated articles (.md files)
├── requirements.txt
├── README.md
├── CLAUDE.md
├── .env
└── .gitignore
```

## Key Framework Gotchas

- **Grok limitation**: Cannot combine `tools` and `output_schema` in one agent. Writer stays tool-free.
- **Claude can combine both**: No need for split agent pairs when using Claude/Anthropic provider.
- **xAI provider** requires `openai` pip package (transitive dep, already in requirements).
- **`DuckDuckGoTools`** requires `ddgs` package (not `duckduckgo-search`).
- **`agno.workflow`** requires `fastapi` as a transitive dependency.
- **Agno Team v2**: `mode` param is deprecated. Use `respond_directly=True` for routing, `delegate_to_all_members=True` for collaborate. `show_members_responses` -> `store_member_responses`.
- **Image agent is optional**: `build_image_agent()` returns `None` if no image API keys are set. Pipeline skips enrichment gracefully.
- **Airtable rate limits**: 5 requests/second. Parallel batch may need small delays for large batches.
- **Article IDs are strings**: Airtable record IDs (e.g., `"recABC123"`), not integers.

## Environment

- Python 3.14, Windows. Use `python -m pip` (pip not on PATH).
- APIs in `.env`: `ANTHROPIC_API_KEY` + `XAI_API_KEY` (required for pipeline), `FREEPIK_API_KEY` + `DATA_FOR_SEO_API_KEY` (optional, for images and rank tracking).
- Airtable in `.env`: `AIRTABLE_PAT` + `AIRTABLE_BASE_ID` (required for article storage). Run `python output/tools/airtable.py` to create the base tables.
- DataForSEO key format: `Basic <base64(login:password)>` — decoded by `agents.image.get_dataforseo_credentials()`.
