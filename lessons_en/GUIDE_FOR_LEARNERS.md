# Learner's Guide

Welcome to the Agentic Content SEO course. This guide tells you everything you need to know before opening your first notebook.

## What you'll build

By the end of 20 lessons, you'll understand how an AI-powered SEO content pipeline works — from researching a topic to generating a complete article. You'll be able to run it, modify it, explain how each piece works, and use AI tools like Claude Code to extend it further.

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
| `ANTHROPIC_API_KEY` | Module 3+ (lesson 8 onward) | Pay-per-use. ~$0.50-2 per full article |
| `XAI_API_KEY` | Module 4+ (lesson 14 onward) | Pay-per-use. ~$0.50-1 per article |
| `FREEPIK_API_KEY` | Optional (image enrichment) | Free tier available |
| `DATA_FOR_SEO_API_KEY` | Optional (image enrichment) | Free trial available |

You do NOT need any API keys for Modules 1-2 (lessons 1-7).

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
jupyter notebook lessons_en/
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

### Module 2: Understanding AI (lessons 5-7)

No API keys needed. Conceptual lessons with Python exercises.

| Lesson | Topic | Time |
|--------|-------|------|
| 05 | How LLMs work (tokens, context, prediction) | 45 min |
| 06 | Prompts and context (system vs user prompts) | 45 min |
| 07 | Models and choices (speed/cost/quality tradeoffs) | 40 min |

After Module 2 you can: explain how LLMs work, write effective prompts, and understand why different models are chosen for different tasks.

### Module 3: Building Agents (lessons 8-12)

Needs `ANTHROPIC_API_KEY`. Each cell that calls an agent costs a small amount (~$0.01-0.05).

| Lesson | Topic | Time |
|--------|-------|------|
| 08 | Create your first agent | 30 min |
| 09 | Give agents tools (web search) | 30 min |
| 10 | Structured output (Pydantic) | 45 min |
| 11 | Chain agents into a pipeline | 30 min |
| 12 | Build a mini pipeline (bridge to production) | 50 min |

After Module 3 you can: create AI agents, give them tools, make them return structured data, chain them together, and build a working 3-agent pipeline with nested schemas.

### Module 4: The Real SEO Pipeline (lessons 13-15)

Needs `ANTHROPIC_API_KEY` + `XAI_API_KEY`. Running a full pipeline costs ~$1-3 in API calls.

| Lesson | Topic | Time |
|--------|-------|------|
| 13 | Research + Outline agents (real code) | 45 min |
| 14 | Writer + Image agents (real code) | 45 min |
| 15 | Full pipeline end-to-end | 30 min |

After Module 4 you can: run the full content pipeline and understand how each agent contributes.

### Module 5: The Complete Product (lessons 16-18)

Needs both API keys for creating articles. Status/history commands are free.

| Lesson | Topic | Time |
|--------|-------|------|
| 16 | Database and SQL basics | 45 min |
| 17 | Command line interface | 20 min |
| 18 | Chat interface (Agno Team) | 30 min |

After Module 5 you can: use the complete product via CLI or chat, and understand how all pieces connect.

### Module 6: AI-Assisted Development (lessons 19-20)

No API keys needed. Conceptual + guided walkthrough.

| Lesson | Topic | Time |
|--------|-------|------|
| 19 | Claude Code basics (installation, CLAUDE.md, workflow) | 45 min |
| 20 | Extending the product (adding a proofreading agent) | 50 min |

After Module 6 you can: use Claude Code to extend and modify the product, verify AI-generated code using your knowledge from all previous modules, and direct AI to build features for you.

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

### AI/LLM terms

- **LLM** — Large Language Model. The AI "brain" that predicts text. Claude, GPT, and Grok are all LLMs.
- **Token** — The unit LLMs process (~¾ of a word). API costs are measured per token.
- **Context window** — Maximum input+output size an LLM can handle at once. Claude Sonnet has 200K tokens.
- **Knowledge cutoff** — The date training data ends. LLMs are "blind" after this date.
- **Temperature** — Controls creativity: 0 = focused/deterministic, 1 = creative/varied.
- **Hallucination** — When an LLM generates confident but incorrect information. Always fact-check.
- **Embedding** — Text converted to numbers capturing meaning. Powers semantic search and similarity.
- **Prompt** — Everything you send to an LLM. Better prompts = better output.
- **System prompt** — Persistent instructions that shape behavior (agent's `instructions`).
- **Prompt engineering** — The skill of writing effective prompts. The new SEO skill.

### Agent terms

- **Agent** — A program that uses an AI model to think and act. Has a name, model, instructions, and optionally tools.
- **Model** — The AI brain. We use Claude Sonnet (fast, good with tools) and Grok-4 (good writer).
- **Instructions** — Directives that shape how an agent behaves. Like a job description.
- **Tools** — Capabilities you give an agent (web search, image search, API calls). The agent decides when to use them.
- **Structured output / output_schema** — Forces an agent to return data in a specific format (not free-form text).
- **Pipeline** — Multiple agents running in sequence, each passing output to the next.
- **Team** — Multiple agents working together under a leader who delegates tasks (used in the chat interface).

### Development terms

- **Claude Code** — Anthropic's CLI AI assistant that reads your codebase and makes changes.
- **CLAUDE.md** — Instructions file for Claude Code (like `instructions` for an agent).
- **MCP** — Model Context Protocol. Connects Claude Code to external documentation sources.

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
3. **Experiment freely in Modules 1-2**. Change values, break things, see what happens. No API cost.
4. **Be careful with API costs in Modules 3-5**. Each `agent.run()` call costs money. Don't run cells in a loop or re-run unnecessarily.
5. **Don't memorize syntax**. Focus on understanding *what* each piece does. You can always look up *how* to write it.
6. **Module 2 is conceptual but essential**. It explains *why* the pipeline works the way it does. Don't skip it.

## After completing all 20 lessons

You now understand the full system. Here's how the lesson code maps to the production files in `output/`:

| Lesson | Builds toward | Production file |
|--------|---------------|-----------------|
| 05-07 | LLM understanding, prompts, model choices | (Informs all design decisions) |
| 08-09 | Agent creation, tools | `output/agents/builders.py` |
| 10, 13 | Pydantic schemas | `output/agents/schemas.py` |
| 11-12, 13-15 | Agent chaining, pipeline | `output/pipeline.py` |
| 16 | Database layer | `output/db.py` |
| 17 | CLI interface | `output/cli.py` |
| 18 | Chat interface, workspace tools | `output/chat.py`, `output/workspace_tools.py` |
| 19-20 | AI-assisted development | `CLAUDE.md` (the blueprint for Claude Code) |

To start using the product:

```bash
# Create an article
python output/cli.py create "Your topic here"

# Check status
python output/cli.py status

# Or use the chat interface
python output/chat.py
```

To extend the product, use Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
cd your-project-folder
claude
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'agno'` | Run `python -m pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'ddgs'` | Run `python -m pip install ddgs` |
| API key error / authentication failed | Check your `.env` file. Make sure there are no spaces around `=` and no quotes around the key value. |
| `python` command not found | Try `python3` instead, or check that Python is installed and on your PATH. |
| Jupyter won't start | Run `python -m pip install jupyter` then `jupyter notebook lessons_en/` |
| Cell runs forever (>2 minutes) | The agent might be waiting for a web search. Click the stop button (square icon) and try again. DuckDuckGo sometimes rate-limits. |
| `Error: status -> error` when creating article | Check `python output/cli.py status --article <id>` to see the error message. Usually an API key issue. |
| `sys.path.insert` not working | Make sure you're running the notebook from the correct directory. Jupyter should be launched from the project root. |
