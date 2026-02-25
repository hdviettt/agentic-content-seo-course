# Agentic Content SEO

An AI-powered SEO content workspace that researches topics, writes articles, finds images, and analyzes Google AI Overviews — all through a conversational chat interface.

Built with [Agno](https://github.com/agno-agi/agno), powered by Claude (Anthropic).

This repo is also a **teaching project** — the `lessons_en/` folder contains 22 Jupyter notebooks across 5 modules that walk non-tech learners from Python basics to building and extending the full product. A complete **Vietnamese translation** is available in `lessons_vi/`.

## Setup

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
# Then edit .env with your API keys
```

You need at minimum `ANTHROPIC_API_KEY`. Add `DATA_FOR_SEO_API_KEY` for web search, image search, and AI Overview analysis.

## Usage

### Web interface (primary)

```bash
# Terminal 1 — Backend
python output/backend/serve.py

# Terminal 2 — Frontend
cd output/frontend && npm install && npm run dev
```

Open `http://localhost:5173` in your browser. Chat with the team, browse articles in the sidebar.

### CLI interface (alternative)

```bash
python output/backend/chat.py
```

Same team, terminal interface. Useful for development and testing.

### What you can do

Talk naturally: "Write an article about on-page SEO", "Add images to on-page-seo", "Analyze the AI Overview for 'technical SEO'", "Create 5 articles from these topics: ...".

The workspace has 3 capabilities:
1. **Write content** — research topics via web search and write SEO articles
2. **Find images** — search for and insert images into existing articles
3. **Optimize for AI Overviews** — analyze Google's AI responses and suggest improvements

## Teaching Curriculum (`lessons_en/`)

22 Jupyter notebooks (English) across 5 modules. Start with Module 1 (no API keys needed).

| Module | Topic | Notebooks |
|--------|-------|-----------|
| **01 - Python Basics** | Variables, lists, dicts, functions, packages | 01-04 |
| **02 - Understanding AI** | How LLMs work, prompts & context, model choices | 05-07 |
| **03 - Building Agents** | First agent, tools, structured output, chaining, storage | 08-12 |
| **04 - AI-Assisted Development** | Claude Code paradigm, usage, prompting/planning, building agents | 13-18 |
| **05 - Complete Product** | Architecture, web fundamentals, web interface, extending | 19-22 |

```bash
python -m pip install jupyter
jupyter notebook lessons_en/
# Or for Vietnamese:
jupyter notebook lessons_vi/
```

## Project Structure

```
output/                         The finished product
├── backend/                    Python backend (12 files)
│   ├── serve.py                Web backend (AgentOS + article API, port 7777)
│   ├── chat.py                 CLI entry point (~40 lines)
│   ├── agents/                 Agent definitions (who)
│   │   ├── __init__.py         Re-exports everything
│   │   ├── content_writer.py   Content Writer (DataForSEO search + storage)
│   │   ├── image_finder.py     Image Finder (DataForSEO Images + storage)
│   │   ├── aio_analyzer.py     AIO Analyzer (AIO analysis tools)
│   │   └── team.py             Agno Team (Sonnet leader + 3 Sonnet members)
│   └── tools/                  Tool definitions (what)
│       ├── __init__.py         Package marker
│       ├── storage.py          Local file storage (JSON metadata + .md files)
│       ├── search.py           DataForSEO web search toolkit
│       ├── aio.py              AIO analysis + credentials
│       └── images.py           DataForSEO image search toolkit
└── frontend/                   React + Vite web app
    ├── package.json
    ├── vite.config.js          Proxy /api, /teams, /health → backend
    └── src/
        ├── App.jsx             Layout (sidebar + main area)
        ├── api.js              API client (fetch + SSE streaming)
        └── components/
            ├── Chat.jsx        Chat with SSE streaming
            ├── ArticleList.jsx Sidebar article list
            └── ArticleView.jsx Full article viewer

lessons_en/                     Teaching curriculum (22 English notebooks)
├── 01-python-basics/           Lessons 01-04 (no API keys needed)
├── 02-understanding-ai/        Lessons 05-07 (no API keys needed)
├── 03-building-agents/         Lessons 08-12 (needs ANTHROPIC_API_KEY)
├── 04-ai-assisted-development/ Lessons 13-18 (Claude Code + building agents)
└── 05-complete-product/        Lessons 19-22 (architecture, web, extending)

lessons_vi/                     Vietnamese translation (same 22 notebooks)

content/                        Generated articles (.md files + articles.json)
```

## Architecture

All agents use **Claude Sonnet** (Anthropic). No other API providers.

```
User request → Team Leader (Sonnet) → delegates to the right member:

  [Content Writer]  — researches via DataForSEO web search, writes article, saves to disk
  [Image Finder]    — reads article, finds images via DataForSEO, inserts into article
  [AIO Analyzer]    — analyzes Google AI Overviews, suggests optimizations
```

- **Team Leader** reads your request and delegates to the right member
- **Content Writer** has web search + storage tools (search is optional — works without DataForSEO key)
- **Image Finder** is optional — `build_image_finder()` returns `None` if no DataForSEO key
- **AIO Analyzer** checks what Google's AI says about a keyword and how to optimize for it

### Storage

Local files. Articles stored as `.md` files in `content/`, metadata in `content/articles.json`. Article IDs are keyword slugs (e.g., `on-page-seo-meta-tags`). No external database — SQLite is only used for Agno chat memory.

## Environment

- Python 3.14, Windows. Use `python -m pip` (pip not on PATH).
- `ANTHROPIC_API_KEY` — required for all agents
- `DATA_FOR_SEO_API_KEY` — optional, enables web search, image search, and AIO analysis. Format: `Basic <base64(login:password)>`
