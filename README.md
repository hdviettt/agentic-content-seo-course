# Agentic Content SEO

An AI-powered SEO content pipeline that researches topics, creates outlines, writes articles, and enriches them with images — all through a conversational chat interface.

Built with [Agno](https://github.com/agno-agi/agno), powered by Claude (Anthropic) and Grok (xAI).

This repo is also a **teaching project** — the `lessons_en/` folder contains 20 Jupyter notebooks across 5 modules that walk non-tech learners from Python basics to building and extending the full pipeline. A complete **Vietnamese translation** is available in `lessons_vi/`.

## Setup

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
# Then edit .env with your API keys
```

You need at minimum `ANTHROPIC_API_KEY`, `XAI_API_KEY`, and `AIRTABLE_PAT`. See `.env.example` for all options.

Set up Airtable (required for article storage):

```bash
python output/tools/airtable.py
# Add the printed AIRTABLE_BASE_ID to your .env
```

## Usage

```bash
python output/chat.py
```

Talk naturally: "Create an article about SEO on-page", "Show me all articles", "Retry article recABC123", "Load topics from topics.csv".

The chat interface is the primary way to use the product — an AI team that creates articles, tracks status, retries failures, and checks rankings, all through conversation.

## Teaching Curriculum (`lessons_en/`)

20 Jupyter notebooks (English) across 5 modules. Start with Module 1 (no API keys needed).

| Module | Topic | Notebooks |
|--------|-------|-----------|
| **01 - Python Basics** | Variables, lists, dicts, functions, packages | 01-04 |
| **02 - Understanding AI** | How LLMs work, prompts & context, model choices | 05-07 |
| **03 - Building Agents** | First agent, tools, structured output, chaining, mini pipeline | 08-12 |
| **04 - Building the Product** | Claude Code, research, outline, writer, images, full pipeline | 13-16 |
| **05 - Complete Product** | Airtable database, how everything connects, chat interface, extending | 17-20 |

```bash
python -m pip install jupyter
jupyter notebook lessons_en/
# Or for Vietnamese:
jupyter notebook lessons_vi/
```

## Project Structure

```
output/                     The finished product (16 Python files)
  chat.py                   Entry point (~60 lines, validation + start)
  pipeline.py               Content generation + batch processing
  agents/
    __init__.py             Re-exports everything
    schemas.py              Pydantic models (ContentOutline, EnrichedContent, etc.)
    researcher.py           Research Agent (Claude Sonnet + DuckDuckGo)
    outliner.py             Outline Agent (Claude Sonnet + structured output)
    writer.py               Writer Agent (Grok-4, plain Markdown)
    image.py                Image Agent + FreepikTools + DataForSEOTools
    content_creator.py      Chat team member (creates articles)
    status_tracker.py       Chat team member (queries articles)
    seo_manager.py          Chat team member (rankings + URLs)
    team.py                 Agno Team assembly (Opus leader + 3 members)
  tools/
    __init__.py             Package marker
    airtable.py             Airtable CRUD + one-time setup
    workspace.py            Team member tool functions
    rankings.py             SERP rank checking via DataForSEO

lessons_en/                 Teaching curriculum (20 English notebooks)
  01-python-basics/         Lessons 01-04 (no API keys needed)
  02-understanding-ai/      Lessons 05-07 (no API keys needed)
  03-building-agents/       Lessons 08-12 (needs ANTHROPIC_API_KEY)
  04-building-the-product/  Lessons 13-16 (Claude Code, builds the real pipeline)
  05-complete-product/      Lessons 17-20 (Airtable, connections, chat, extending)

lessons_vi/                 Vietnamese translation (same 20 notebooks)

content/                    Generated articles (.md files)
.env.example                Template for API keys
```

## Architecture

### Content Pipeline

```
Topic -> [Research Agent] -> [Outline Agent] -> [Writer Agent] -> [Image Agent] -> Article
           Claude+DDG        Claude+schema      Grok-4         Claude+tools
```

- **Research Agent** — searches the web via DuckDuckGo, returns research notes
- **Outline Agent** — creates a structured outline (Pydantic schema output)
- **Writer Agent** — writes full Markdown article from outline (Grok-4)
- **Image Agent** — finds and inserts images (optional, needs API keys)

### Model Choices

- **Claude Sonnet** for research, outline, and image agents — supports tools + structured output together
- **Grok-4** for the writer — great at long-form writing, but can't combine tools with structured output
- **Claude Opus** only for the conversational team leader in agents/team.py

### Database

Airtable is the primary data store. Articles track through: `queued -> researching -> outlining -> writing -> enriching -> review`. SQLite is used only for Agno chat memory (`chat_sessions.db`).
