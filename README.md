# Agentic Content SEO

An AI-powered SEO content pipeline that researches topics, creates outlines, writes articles, and enriches them with images — all from the command line or a conversational chat interface.

Built with [Agno](https://github.com/agno-agi/agno), powered by Claude (Anthropic) and Grok (xAI).

This repo is also a **teaching project** — the `lessons_en/` folder contains 20 Jupyter notebooks across 6 modules that walk non-tech learners from Python basics to building the full pipeline and extending it with AI-assisted development. A complete **Vietnamese translation** is available in `lessons_vi/`.

## Setup

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file:

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key
XAI_API_KEY=your_xai_api_key

# Optional — images (pipeline works without these)
FREEPIK_API_KEY=your_freepik_api_key
DATA_FOR_SEO_API_KEY=Basic <base64-encoded login:password>
```

## Usage

### Chat Interface (recommended)

```bash
python output/chat.py
```

Talk naturally: "Create an article about SEO on-page", "Show me all articles", "What's the status of article 3?"

### CLI

```bash
# Create articles
python output/cli.py create "How to train for a marathon"
python output/cli.py create "Best running shoes" --keywords "running shoes,best shoes 2026"
python output/cli.py create-batch "topic 1" "topic 2" "topic 3"
python output/cli.py create-batch --file topics.csv

# Check status
python output/cli.py status
python output/cli.py status --article 5
python output/cli.py status --filter review

# Version history
python output/cli.py history 3
```

## Teaching Curriculum (`lessons_en/`)

20 Jupyter notebooks (English) across 6 modules. Start with Module 1 (no API keys needed).

| Module | Topic | Notebooks |
|--------|-------|-----------|
| **01 - Python Basics** | Variables, lists, dicts, functions, packages | 01-04 |
| **02 - Understanding AI** | How LLMs work, prompts & context, model choices | 05-07 |
| **03 - Building Agents** | First agent, tools, structured output, chaining, mini pipeline | 08-12 |
| **04 - SEO Pipeline** | Research, outline, writer, images, full pipeline | 13-15 |
| **05 - Complete Product** | Database, CLI, chat interface | 16-18 |
| **06 - AI-Assisted Dev** | Claude Code basics, extending the product | 19-20 |

```bash
python -m pip install jupyter
jupyter notebook lessons_en/
# Or for Vietnamese:
jupyter notebook lessons_vi/
```

## Project Structure

```
lessons_en/                 Teaching curriculum (20 English notebooks)
  01-python-basics/
  02-understanding-ai/
  03-building-agents/
  04-seo-pipeline/
  05-complete-product/
  06-ai-assisted-dev/

lessons_vi/                 Giáo trình tiếng Việt (20 Vietnamese notebooks)
  01-python-co-ban/
  02-hieu-ve-ai/
  03-xay-dung-agent/
  04-seo-pipeline/
  05-san-pham-hoan-chinh/
  06-phat-trien-voi-ai/

output/                     The finished product (all Python code)
  agents/                   AI agents and their data models
    __init__.py             Re-exports agent instances and schemas
    builders.py             4 agent builder functions + instances
    schemas.py              Pydantic output schemas (data contracts)
  tools/                    External API toolkits (image search)
    __init__.py             Re-exports FreepikTools, DataForSEOTools
    freepik_tools.py        Freepik image search toolkit
    dataforseo_tools.py     DataForSEO image search toolkit
  pipeline.py               Content generation + batch processing
  db.py                     SQLite connection + CRUD functions
  chat.py                   Conversational team interface (Agno Team)
  cli.py                    CLI entry point
  workspace_tools.py        Team member tool functions

content/                    Generated articles (.md files)
```

## Architecture

### Content Pipeline

```
Topic → [Research Agent] → [Outline Agent] → [Writer Agent] → [Image Agent] → Article
           Claude+DDG        Claude+schema      Grok-4         Claude+tools
```

- **Research Agent** — searches the web via DuckDuckGo, returns research notes
- **Outline Agent** — creates a structured outline (Pydantic schema output)
- **Writer Agent** — writes full Markdown article from outline (Grok-4)
- **Image Agent** — finds and inserts images (optional, needs API keys)

### Model Choices

- **Claude Sonnet** for research, outline, and image agents — supports tools + structured output together
- **Grok-4** for the writer — great at long-form writing, but can't combine tools with structured output
- **Claude Opus** only for the conversational team leader in chat.py

### Database

SQLite (`output/workspace.db`), auto-created on first run. Articles track through: `queued → researching → outlining → writing → enriching → review`.
