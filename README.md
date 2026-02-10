# SEO Content Generator

An AI agent pipeline that researches a topic, writes an SEO-optimized article, and enriches it with images — all from a single terminal command.

Built with [Agno](https://github.com/agno-agi/agno) and powered by xAI's Grok models.

## How It Works

Three agents run sequentially as an Agno Workflow:

1. **Research & Outline** — Searches the web via DuckDuckGo, analyzes top-ranking content, and produces a structured outline with target keywords (`grok-4-fast` for research, `grok-4` for outline)
2. **Content Writer** — Expands the outline into a 1500–2500 word Markdown article with proper heading hierarchy and natural keyword placement (`grok-4`)
3. **Image Enrichment** — Finds relevant images via Freepik/DataForSEO APIs and inserts them into the article (`grok-4-fast` for search, `grok-4` for assembly). Skips gracefully if no image API keys are configured

The final article is auto-exported to `output/` as a `.md` file.

## Project Structure

```
├── main.py                 # CLI entry point
├── workflow.py             # Agno Workflow — 3 sequential steps
├── schemas.py              # Pydantic models (ContentOutline, EnrichedContent)
├── agents/
│   ├── outline_agent.py    # Research + Outline agents (split for Grok compatibility)
│   ├── writer_agent.py     # Content Writer agent
│   └── image_agent.py      # Image Search + Assembler agents
├── tools/
│   ├── freepik_tools.py    # Custom Toolkit: Freepik image search
│   └── dataforseo_tools.py # Custom Toolkit: DataForSEO image search
└── output/                 # Auto-exported markdown articles
```

## Setup

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file:

```env
# Required
XAI_API_KEY=your_xai_api_key

# Optional — images (pipeline works without these)
FREEPIK_API_KEY=your_freepik_api_key
DATAFORSEO_LOGIN=your_login
DATAFORSEO_PASSWORD=your_password
```

## Usage

```bash
python main.py
```

Enter a topic when prompted. The pipeline runs, streams output to the terminal with rich formatting, and saves the article to `output/`.

## Architecture Notes

Grok models do not support using tools and structured output (`json_schema` response format) in the same request. To work around this, agents that need both are split into two:

- **Research agent** (tools, free-form output) → **Outline agent** (no tools, structured output)
- **Image search agent** (tools, free-form output) → **Image assembler agent** (no tools, structured output)

This keeps each agent focused and avoids the API limitation.
