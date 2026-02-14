# Learner's Guide

Welcome to the Agentic Content SEO course. This guide tells you everything you need to know before opening your first notebook.

## What you'll build

By the end of 14 lessons, you'll understand how an AI-powered SEO content pipeline works — from researching a topic to generating a complete article. You'll be able to run it, modify it, and explain how each piece works.

## What you need before starting

### Skills (no coding experience required)

- You can type in a terminal (copy-paste commands)
- You know what SEO is at a basic level (keywords, rankings, articles)
- You can open and navigate files on your computer

### Software

| Tool | Why | How to check |
|------|-----|------|
| Python 3.12+ | Runs all the code | `python --version` in terminal |
| Jupyter Notebook | Runs the lessons | Installed via requirements.txt |
| A code editor | To read production code later | VS Code recommended |
| Git (optional) | To track your changes | `git --version` |

### API keys

| Key | When needed | Cost |
|-----|------------|------|
| `ANTHROPIC_API_KEY` | Module 2+ (lesson 5 onward) | Pay-per-use. ~$0.50-2 per full article |
| `XAI_API_KEY` | Module 3+ (lesson 10 onward) | Pay-per-use. ~$0.50-1 per article |
| `FREEPIK_API_KEY` | Optional (image enrichment) | Free tier available |
| `DATA_FOR_SEO_API_KEY` | Optional (image enrichment) | Free trial available |

You do NOT need any API keys for Module 1 (lessons 1-4).

## Setup (do this once)

### Step 1: Install packages

Open your terminal in the project folder and run:

```bash
python -m pip install -r requirements.txt
```

### Step 2: Create your `.env` file

Create a file called `.env` in the project root (same folder as `README.md`):

```
ANTHROPIC_API_KEY=your_key_here
XAI_API_KEY=your_key_here
```

Ask your teacher for the API keys if you don't have them.

### Step 3: Verify your setup

Open a terminal and run:

```bash
python -c "import agno; print('agno OK')"
python -c "import anthropic; print('anthropic OK')"
python -c "from dotenv import load_dotenv; load_dotenv(); import os; key=os.getenv('ANTHROPIC_API_KEY',''); print('API key found' if len(key)>5 else 'WARNING: API key not found -- check your .env file')"
```

All three should print OK / "API key found". If not, ask your teacher before continuing.

### Step 4: Open Jupyter

```bash
jupyter notebook lessons/
```

Start with `01-python-basics/01_hello_python.ipynb`.

## Course structure

### Module 1: Python Basics (lessons 1-4)

No API keys needed. No internet needed. Safe to experiment freely.

| Lesson | Topic | Time |
|--------|-------|------|
| 01 | Variables, strings, f-strings | 30 min |
| 02 | Lists, dictionaries, loops | 45 min |
| 03 | Functions | 45 min |
| 04 | Packages, .env, setup | 30 min |

After Module 1 you can: read Python code, understand variables/lists/dicts/functions, and know how the project's packages fit together.

### Module 2: AI Agents (lessons 5-8)

Needs `ANTHROPIC_API_KEY`. Each cell that calls an agent costs a small amount (~$0.01-0.05).

| Lesson | Topic | Time |
|--------|-------|------|
| 05 | Create your first agent | 30 min |
| 06 | Give agents tools (web search) | 30 min |
| 07 | Structured output (Pydantic) | 45 min |
| 08 | Chain agents into a pipeline | 30 min |

After Module 2 you can: create AI agents, give them tools, make them return structured data, and chain them together.

### Module 3: The Real SEO Pipeline (lessons 9-11)

Needs `ANTHROPIC_API_KEY` + `XAI_API_KEY`. Running a full pipeline costs ~$1-3 in API calls.

| Lesson | Topic | Time |
|--------|-------|------|
| 09 | Research + Outline agents (real code) | 45 min |
| 10 | Writer + Image agents (real code) | 45 min |
| 11 | Full pipeline end-to-end | 30 min |

After Module 3 you can: run the full content pipeline and understand how each agent contributes.

### Module 4: The Complete Product (lessons 12-14)

Needs both API keys for creating articles. Status/history commands are free.

| Lesson | Topic | Time |
|--------|-------|------|
| 12 | Database and SQL basics | 45 min |
| 13 | Command line interface | 20 min |
| 14 | Chat interface (Agno Team) | 30 min |

After Module 4 you can: use the complete product via CLI or chat, and understand how all pieces connect.

## Key concepts glossary

These terms appear throughout the lessons. Refer back here when you encounter them.

### Python terms

- **Variable** — A named container for data. `name = "Viet"` creates a variable called `name`.
- **String** — Text data, always in quotes: `"hello"`.
- **List** — An ordered collection: `["a", "b", "c"]`. Access items by position: `list[0]`.
- **Dictionary (dict)** — Key-value pairs: `{"name": "Viet", "age": 20}`. Access by key: `dict["name"]`.
- **Function** — Reusable code block. `def greet(name):` defines one, `greet("Viet")` calls it.
- **Import** — Bring external code into your file: `from agno.agent import Agent`.
- **Package** — Pre-written code you install and import (e.g., `agno`, `anthropic`).

### Data format terms

- **JSON** — A text format for structured data. Looks like Python dicts and lists:
  ```json
  {"title": "SEO Guide", "keywords": ["seo", "ranking"]}
  ```
  Used when agents exchange data. You'll see `.model_dump_json()` which converts Python objects to JSON text.

- **Markdown** — A text format for formatted documents. Our articles are written in Markdown:
  ```markdown
  # Main Title        (H1 heading)
  ## Section           (H2 heading)
  **bold text**        (bold)
  - bullet point       (list item)
  ![alt](url)          (image)
  ```
  Files ending in `.md` are Markdown files. The `content/` folder contains generated articles in Markdown.

- **CSV** — Comma-separated values. A simple spreadsheet format:
  ```
  topic,keywords
  SEO Guide 2026,"seo,ranking"
  ```
  Used for batch article creation.

### AI/Agent terms

- **Agent** — A program that uses an AI model to think and act. Has a name, model, instructions, and optionally tools.
- **Model** — The AI brain. We use Claude Sonnet (fast, good with tools) and Grok-4 (good writer).
- **Instructions** — Directives that shape how an agent behaves. Like a job description.
- **Tools** — Capabilities you give an agent (web search, image search, API calls). The agent decides when to use them.
- **Structured output / output_schema** — Forces an agent to return data in a specific format (not free-form text).
- **Pipeline** — Multiple agents running in sequence, each passing output to the next.
- **Team** — Multiple agents working together under a leader who delegates tasks (used in the chat interface).

### SEO terms (for non-SEO learners)

- **SEO** — Search Engine Optimization. Making web pages rank higher on Google.
- **Keywords** — Words/phrases people search for on Google. An article targets specific keywords.
- **Meta description** — The 1-2 sentence summary shown in Google search results (max 160 characters).
- **On-page SEO** — Optimizations made directly on the web page (titles, headings, content, images).
- **Backlinks** — Links from other websites to yours. A key ranking factor.

## How to run each cell

In Jupyter Notebook:
- **Shift + Enter** — Run the current cell and move to the next
- **Ctrl + Enter** — Run the current cell and stay on it
- **Cells run in order** — Always run from top to bottom. If you skip a cell, later cells may fail.

## Tips for success

1. **Run every cell**, even if you think you understand it. Seeing the output builds intuition.
2. **Read the error message** before asking for help. Python errors usually tell you exactly what went wrong (wrong variable name, missing package, etc.).
3. **Experiment freely in Module 1**. Change values, break things, see what happens. No API cost.
4. **Be careful with API costs in Modules 2-4**. Each `agent.run()` call costs money. Don't run cells in a loop or re-run unnecessarily.
5. **Don't memorize syntax**. Focus on understanding *what* each piece does. You can always look up *how* to write it.

## After completing all 14 lessons

You now understand the full system. Here's how the lesson code maps to the production files in `output/`:

| Lesson | Builds toward | Production file |
|--------|---------------|-----------------|
| 05-06 | Agent creation, tools | `output/agents/builders.py` |
| 07 | Pydantic schemas | `output/agents/schemas.py` |
| 08-11 | Agent chaining, pipeline | `output/pipeline.py` |
| 12 | Database layer | `output/db.py` |
| 13 | CLI interface | `output/cli.py` |
| 14 | Chat interface, workspace tools | `output/chat.py`, `output/workspace_tools.py` |

To start using the product:

```bash
# Create an article
python output/cli.py create "Your topic here"

# Check status
python output/cli.py status

# Or use the chat interface
python output/chat.py
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'agno'` | Run `python -m pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'ddgs'` | Run `python -m pip install ddgs` |
| API key error / authentication failed | Check your `.env` file. Make sure there are no spaces around `=` and no quotes around the key value. |
| `python` command not found | Try `python3` instead, or check that Python is installed and on your PATH. |
| Jupyter won't start | Run `python -m pip install jupyter` then `jupyter notebook lessons/` |
| Cell runs forever (>2 minutes) | The agent might be waiting for a web search. Click the stop button (square icon) and try again. DuckDuckGo sometimes rate-limits. |
| `Error: status -> error` when creating article | Check `python output/cli.py status --article <id>` to see the error message. Usually an API key issue. |
