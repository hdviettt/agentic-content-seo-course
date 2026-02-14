# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
python output/chat.py                                    # Interactive conversational workspace (recommended)
python output/cli.py chat                                # Same, via CLI subcommand
python output/cli.py create "topic"                      # Generate a single SEO article
python output/cli.py create "topic" --keywords "kw1,kw2" # Generate with target keywords
python output/cli.py create-batch "t1" "t2"              # Batch create from arguments
python output/cli.py create-batch --file topics.csv      # Batch create from CSV (columns: topic,keywords)
python output/cli.py status                              # View all articles
python output/cli.py status --article <id>               # View article details
python output/cli.py status --filter <status>            # Filter by status
python output/cli.py history <id>                        # View article version history
python -m pip install -r requirements.txt                # Install dependencies (pip not on PATH)
jupyter notebook lessons/                                # Open teaching notebooks
```

## Architecture

### Two interfaces, same backend

- **`output/chat.py`** — Agno Team: Opus 4.6 leader + 2 Sonnet members (Content Creator, Status Tracker). Members have focused tools from `workspace_tools.py` that wrap pipeline and DB calls. Chat history persisted in `chat_sessions.db`.
- **`output/cli.py`** — Thin argparse CLI. Each command handler calls a pipeline or DB function directly. No business logic in the CLI layer.

### Content pipeline (`output/pipeline.py`)

Plain Python function that runs 4 sequential agent steps with DB status updates between each:

```
queued → researching → outlining → writing → enriching → review
          research_agent  outline_agent  writer_agent  image_agent
          (Sonnet + DDG)  (Sonnet)       (Grok-4)      (Sonnet + image tools)
```

On error at any step: `status → error` with `error_message` saved. Batch processing (`run_batch()` in same file) loops this per topic. Articles saved to `content/`.

### Agent model choices (`output/agents/builders.py`)

- **Claude Sonnet** for research, outline, and image agents — supports tools + `output_schema` together.
- **Grok-4** for writer agent only — plain Markdown output, no tools, no `output_schema` (Grok cannot combine tools with structured output).
- **Opus 4.6** only for conversational team leader in `output/chat.py`.

### Database layer (`output/db.py`)

SQLite (`workspace.db`), auto-created on import in the `output/` directory. No ORM — plain functions returning dicts. `update_article_status(id, status, **fields)` uses `**kwargs` for dynamic column updates.

### Tools pattern

Custom toolkits inherit `agno.tools.Toolkit`, pass function refs to `super().__init__(name=..., tools=[...])`. All tool functions return JSON strings. Workspace tools (`output/workspace_tools.py`) are plain Python functions passed directly as `tools=[...]` to team members.

### Teaching curriculum (`lessons/`)

14 Jupyter notebooks (English) across 4 modules. Module 1 (Python basics) needs no API keys. Modules 2-4 progressively build the product.

## Project structure

```
agentic-content-seo/
├── lessons/                    ← Teaching curriculum (14 English notebooks)
│   ├── 01-python-basics/       (01-04: no API keys needed)
│   ├── 02-ai-agents/           (05-08: needs ANTHROPIC_API_KEY)
│   ├── 03-seo-pipeline/        (09-11: builds the real pipeline)
│   └── 04-making-it-real/      (12-14: database, CLI, chat)
├── output/                     ← The finished product (all Python code)
│   ├── agents/                 ← AI agents and their data models
│   │   ├── __init__.py         Re-exports agent instances and schemas
│   │   ├── builders.py         4 agent builder functions + instances
│   │   └── schemas.py          Pydantic output schemas
│   ├── tools/                  ← External API toolkits (image search)
│   │   ├── __init__.py         Re-exports FreepikTools, DataForSEOTools
│   │   ├── freepik_tools.py    Freepik image search API
│   │   └── dataforseo_tools.py DataForSEO image search API
│   ├── pipeline.py             Content pipeline orchestrator
│   ├── db.py                   SQLite database layer
│   ├── workspace_tools.py      Chat team member tools
│   ├── cli.py                  CLI entry point
│   └── chat.py                 Chat entry point
├── content/                    ← Generated articles (.md files)
├── requirements.txt
├── README.md
├── CLAUDE.md
├── .env
└── .gitignore
```

No Python files at root. `__init__.py` only in `output/agents/` and `output/tools/` for re-exports.

## Key Framework Gotchas

- **Grok limitation**: Cannot combine `tools` and `output_schema` in one agent. Writer stays tool-free.
- **Claude can combine both**: No need for split agent pairs when using Claude/Anthropic provider.
- **xAI provider** requires `openai` pip package (transitive dep, already in requirements).
- **`DuckDuckGoTools`** requires `ddgs` package (not `duckduckgo-search`).
- **`agno.workflow`** requires `fastapi` as a transitive dependency.
- **Agno Team v2**: `mode` param is deprecated. Use `respond_directly=True` for routing, `delegate_to_all_members=True` for collaborate. `show_members_responses` → `store_member_responses`.
- **Image agent is optional**: `build_image_agent()` returns `None` if no image API keys are set. Pipeline skips enrichment gracefully.

## Environment

- Python 3.14, Windows. Use `python -m pip` (pip not on PATH).
- APIs in `.env`: `ANTHROPIC_API_KEY` + `XAI_API_KEY` (required), `FREEPIK_API_KEY` + `DATA_FOR_SEO_API_KEY` (optional, for images).
- DataForSEO key format: `Basic <base64(login:password)>` — decoded by `tools.dataforseo_tools.get_dataforseo_credentials()`.
