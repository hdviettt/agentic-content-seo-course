# Learner's Guide

Welcome to the Agentic Content SEO course. This guide tells you everything you need to know before opening your first notebook.

## What you'll build

By the end of 21 lessons, you'll understand how an AI-powered SEO content system works — from researching a topic to generating a complete article with images. You'll be able to run it, modify it, explain how each piece works, and use AI tools like Claude Code to extend it further.

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
| Node.js 18+ | Runs the frontend | `node --version` in terminal |
| Git (optional) | To track your changes | `git --version` |

### API keys

| Key | When needed | Cost |
|-----|------------|------|
| `ANTHROPIC_API_KEY` | Module 3+ (lesson 8 onward) | Pay-per-use. ~$0.50-2 per full article |
| `DATA_FOR_SEO_API_KEY` | Optional (web search, images, AIO) | Free trial available |

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
DATA_FOR_SEO_API_KEY=Basic your_base64_encoded_credentials_here
```

Ask your teacher for the API keys if you don't have them.

### Step 3: Install frontend dependencies

```bash
cd output/frontend
npm install
```

### Step 4: Verify your setup

Open Lesson 04 (`lessons_en/01-python-basics/04_setup_and_packages.ipynb`) and run the verification cell at the bottom. All 3 checks must pass.

### Step 5: Open Jupyter

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

### Module 3: Building Agents (lessons 8-13)

Needs `ANTHROPIC_API_KEY`. Each cell that calls an agent costs a small amount (~$0.01-0.05).

| Lesson | Topic | Time |
|--------|-------|------|
| 08 | Create your first agent | 30 min |
| 09 | Give agents tools (web search) | 30 min |
| 10 | Structured output (Pydantic) | 45 min |
| 11 | API calling (how agents talk to Claude) | 30 min |
| 12 | Chain agents into a pipeline | 30 min |
| 13 | Build a mini pipeline (bridge to production) | 50 min |

After Module 3 you can: create AI agents, give them tools, make them return structured data, chain them together, and build a working mini pipeline.

### Module 4: Building the Product (lessons 14-17)

Lesson 14 (Claude Code) needs no API keys. Lessons 15-17 need `ANTHROPIC_API_KEY`.

| Lesson | Topic | Time |
|--------|-------|------|
| 14 | Claude Code basics (installation, CLAUDE.md, workflow) | 45 min |
| 15 | The Content Writer agent | 45 min |
| 16 | Image Finder + AIO Analyzer agents | 45 min |
| 17 | Team & batch processing | 30 min |

After Module 4 you can: use Claude Code to navigate the codebase, understand each agent, and run batch article creation.

### Module 5: The Complete Product (lessons 18-21)

| Lesson | Topic | Time |
|--------|-------|------|
| 18 | Local file storage | 45 min |
| 19 | How everything connects | 20 min |
| 20 | Web interface (AgentOS + React) | 30 min |
| 21 | Extending the product | 50 min |

After Module 5 you can: use the complete product via the web interface, understand how all pieces connect, and use Claude Code to extend and modify the product.

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

### AI/LLM terms

- **LLM** — Large Language Model. The AI "brain" that predicts text. Claude and GPT are LLMs.
- **Token** — The unit LLMs process (~3/4 of a word). API costs are measured per token.
- **Context window** — Maximum input+output size an LLM can handle at once. Claude Sonnet has 200K tokens.
- **Knowledge cutoff** — The date training data ends. LLMs are "blind" after this date.
- **Temperature** — Controls creativity: 0 = focused/deterministic, 1 = creative/varied.
- **Hallucination** — When an LLM generates confident but incorrect information. Always fact-check.
- **Prompt** — Everything you send to an LLM. Better prompts = better output.
- **System prompt** — Persistent instructions that shape behavior (agent's `instructions`).

### Agent terms

- **Agent** — A program that uses an AI model to think and act. Has a name, model, instructions, and optionally tools.
- **Model** — The AI brain. We use Claude Sonnet for all agents (fast, good with tools, good writer).
- **Instructions** — Directives that shape how an agent behaves. Like a job description.
- **Tools** — Capabilities you give an agent (web search, image search, save articles). The agent decides when to use them.
- **Structured output / output_schema** — Forces an agent to return data in a specific format (not free-form text).
- **Team** — Multiple agents working together under a leader who delegates tasks.
- **AgentOS** — Agno's tool that wraps a Team into a web API automatically.

### Development terms

- **Claude Code** — Anthropic's CLI AI assistant that reads your codebase and makes changes.
- **CLAUDE.md** — Instructions file for Claude Code (like `instructions` for an agent).
- **Vibecoding** — Using AI tools like Claude Code to generate code by describing what you want.

### SEO terms (for non-SEO learners)

- **SEO** — Search Engine Optimization. Making web pages rank higher on Google.
- **Keywords** — Words/phrases people search for on Google. An article targets specific keywords.
- **AIO** — AI Overview. Google's AI-generated answer at the top of search results.
- **On-page SEO** — Optimizations made directly on the web page (titles, headings, content, images).

## How to run each cell

In Jupyter Notebook:
- **Shift + Enter** — Run the current cell and move to the next
- **Ctrl + Enter** — Run the current cell and stay on it
- **Cells run in order** — Always run from top to bottom. If you skip a cell, later cells may fail.

## Tips for success

1. **Run every cell**, even if you think you understand it. Seeing the output builds intuition.
2. **Read the error message** before asking for help. Python errors usually tell you exactly what went wrong.
3. **Experiment freely in Modules 1-2**. Change values, break things, see what happens. No API cost.
4. **Be careful with API costs in Modules 3-5**. Each `agent.run()` call costs money. Don't run cells in a loop.
5. **Don't memorize syntax**. Focus on understanding *what* each piece does.
6. **Module 2 is conceptual but essential**. It explains *why* the system works the way it does. Don't skip it.

## After completing all 21 lessons

You now understand the full system. Here's how the lesson code maps to the production files:

| Lesson | Builds toward | Production file |
|--------|---------------|-----------------|
| 05-07 | LLM understanding, prompts, model choices | (Informs all design decisions) |
| 08-09 | Agent creation, tools | `output/backend/agents/content_writer.py` |
| 10 | Pydantic schemas | Used across all agents |
| 11-13 | API calling, chaining, mini pipeline | `output/backend/agents/team.py` |
| 15 | Content Writer agent | `output/backend/agents/content_writer.py` |
| 17 | Team & batch processing | `output/backend/agents/team.py` |
| 18 | Local file storage | `output/backend/tools/storage.py` |
| 19 | How everything connects | All files in `output/backend/` |
| 20 | Web interface | `output/backend/serve.py`, `output/frontend/` |
| 21 | Extending the product | `CLAUDE.md` (the blueprint for Claude Code) |

To start using the product:

```bash
# Start the web app
python output/backend/serve.py        # Terminal 1: backend on port 7777
cd output/frontend && npm run dev     # Terminal 2: frontend on port 5173
```

Open `http://localhost:5173` in your browser.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'agno'` | Run `python -m pip install -r requirements.txt` |
| API key error / authentication failed | Check your `.env` file. Make sure there are no spaces around `=` and no quotes around the key value. |
| `python` command not found | Try `python3` instead, or check that Python is installed and on your PATH. |
| Jupyter won't start | Run `python -m pip install jupyter` then `jupyter notebook lessons_en/` |
| Cell runs forever (>2 minutes) | The agent might be waiting for an API call. Click the stop button (square icon) and try again. |
| `sys.path.insert` not working | Make sure you're running the notebook from the correct directory. Jupyter should be launched from the project root. |
