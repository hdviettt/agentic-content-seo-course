# Teacher's Guide

This guide helps you teach the Agentic Content SEO curriculum effectively. It covers preparation, pacing, per-lesson notes, and known pitfalls.

## Course overview

- **21 lessons** across 5 modules
- **Target audience**: Non-technical staff (marketing, SEO, content teams) with zero coding experience
- **Total time**: 12-14 hours of instruction, best delivered across 3 days
- **Goal**: Learners understand how the AI content system works, can run and read the code, and can use Claude Code to extend and modify it

## Before teaching

### Classroom setup

1. **Install Python 3.12+** on every machine
2. **Install Node.js 18+** for the frontend
3. **Pre-install all packages**: `python -m pip install -r requirements.txt` and `cd output/frontend && npm install`
4. **Distribute API keys** — create a shared `.env` file or give each student their own keys
5. **Test the web app** on at least one machine: run `python output/backend/serve.py` and `cd output/frontend && npm run dev`, then open `http://localhost:5173` and send a test prompt
6. **Open Jupyter** and verify notebooks load: `jupyter notebook lessons_en/`

### API cost planning

| Activity | Approximate cost per student |
|----------|------------------------------|
| Module 1 (lessons 1-4) | $0 (no API calls) |
| Module 2 (lessons 5-7) | $0 (no API calls) |
| Module 3 (lessons 8-13) | $0.75-1.50 (Sonnet calls, mini pipeline) |
| Module 4 (lessons 14-17) | $2-5 (Sonnet agents, full team) |
| Module 5 (lessons 18-21) | $0-3 (storage is free, creating articles costs) |
| **Total per student** | **$3-10** |

For a class of 10: budget $30-100 in API costs.

**Cost control tips:**
- Modules 1 and 2 are completely free — no API calls at all
- Lesson 14 (Claude Code) and 21 (Extending) are also free (no agent runs)
- In Module 3, have students run each demo cell only once (no re-runs)
- In lesson 17 (batch processing), the team run costs ~$1-3. Consider demoing once rather than having every student run
- Module 5 lessons 18-19 don't need to create new articles — storage queries are free

### What learners should already know

- How to open a terminal
- How to navigate folders on their computer
- Basic understanding of what SEO is (they work at an SEO agency, so this is given)
- **No programming knowledge required** — Module 1 covers everything from zero

## Suggested pacing

### Day 1: Foundation (4-5 hours)

| Block | Lessons | Duration | Notes |
|-------|---------|----------|-------|
| Morning 1 | 01-02 | 90 min | Python basics. Go slow. Let students experiment. |
| Morning 2 | 03-04 | 90 min | Functions + setup. End with setup verification. |
| Afternoon 1 | 05-06 | 90 min | How LLMs work + prompts. Conceptual but critical. |
| Afternoon 2 | 07 | 40 min | Models and choices. Ends Module 2 with cost exercise. |

**Checkpoint**: By end of Day 1, every student should understand tokens, prompts, and model tradeoffs, and have a working API key setup.

### Day 2: Building (4-5 hours)

| Block | Lessons | Duration | Notes |
|-------|---------|----------|-------|
| Morning 1 | 08-09 | 60 min | First agents. The "wow" moment when the agent responds. |
| Morning 2 | 10-11 | 75 min | Structured output + API calling. Conceptually harder. |
| Afternoon 1 | 12-13 | 80 min | Chaining + mini pipeline. Key bridge lesson. |
| Afternoon 2 | 14-15 | 90 min | Claude Code + Content Writer. Real production code. |

**Checkpoint**: By end of Day 2, every student should have run `agent.run()` successfully, seen a mini pipeline work, and understood the Content Writer agent.

### Day 3: Product + Capstone (4-5 hours)

| Block | Lessons | Duration | Notes |
|-------|---------|----------|-------|
| Morning 1 | 16-17 | 75 min | Image Finder + Team & batch processing. |
| Morning 2 | 18 | 45 min | Local storage. Hands-on save/list/get/update cycle. |
| Afternoon 1 | 19-20 | 60 min | How everything connects + web interface. Demo live. |
| Afternoon 2 | 21 | 60 min | Extending the product + vibecoding. |
| Wrap-up | — | 30 min | Full walkthrough of `output/` folder structure. Q&A. |

## Per-lesson teaching notes

### Lesson 01: Hello Python

- **Pace**: Very slow. This is many students' first code ever.
- **Key moment**: When `print("Hello!")` works. Give them time to feel it.
- **Common issue**: Students type `Print` (capital P) — Python is case-sensitive.

### Lesson 02: Lists and Dictionaries

- **Pace**: Medium. Lists are intuitive, dicts need more time.
- **Key moment**: The nested structure example. Pause here and draw it on a whiteboard.
- **Common issue**: Missing commas in dict literals cause `SyntaxError`.

### Lesson 03: Functions

- **Pace**: Slow. Functions are the hardest concept in Module 1.
- **Common issue**: Indentation errors and forgetting `return`.

### Lesson 04: Setup and Packages

- **Critical**: End this lesson with setup verification. Have every student run the verification cell. Do not proceed to Module 2 until everyone passes all 3 checks.
- **Security**: Emphasize never committing `.env` to git.

### Lesson 05-07: Understanding AI (Module 2)

- **No API calls** — completely free. Students can experiment freely.
- **Key moments**: Token estimation exercise (makes cost tangible), temperature demo, model tradeoffs.
- **Teach**: Hallucinations — critical for SEO teams generating content.

### Lesson 08: Your First Agent

- **Key moment**: The first `agent.run()` response. Students will be amazed that 5 lines create an AI agent.
- **Common issue**: API key errors if `load_dotenv()` can't find `.env`.

### Lesson 09: Agent with Tools

- **Key moment**: Agent with vs without tools comparison. Run both live.
- **Connect to Module 2**: "In Lesson 5, we learned about knowledge cutoffs. Tools solve that problem."
- **Cost**: Each `agent.run()` with DataForSEO costs ~$0.02-0.05.

### Lesson 10: Structured Output

- **Pace**: SLOW. This is the hardest lesson in Module 3.
- **Key moment**: When `outline.title` returns just the title string. This is the "why structured output matters" realization.

### Lesson 11: API Calling

- **Teaches**: How agents talk to Claude under the hood (HTTP requests, JSON payloads).

### Lesson 12-13: Chaining + Mini Pipeline

- **Key bridge**: These lessons connect simple agents to the production code pattern.
- **The `sys.path.insert` pattern** is introduced here. Explain: "This tells Python where to find the production code files."

### Lesson 14: Claude Code Basics

- **No API calls** — students read project files and write prompts as strings.
- **Key moment**: Reading the actual CLAUDE.md file. "This is the system prompt for Claude Code."

### Lesson 15: The Content Writer

- **First "real product" code**. Students see the actual Content Writer agent from `output/backend/agents/content_writer.py`.
- **Teaches**: DataForSEO search + storage tools working together in one agent.

### Lesson 16: Image Finder and AIO Analyzer

- **Two agents in one lesson** — the Image Finder (optional, needs DataForSEO) and the AIO Analyzer (Google AI Overview analysis).
- **Key patterns**: Factory function (`build_image_finder()` returns `None` if no API key), read-modify-write pattern (read article → insert images → save).
- **Graceful degradation**: Image Finder is optional. No DataForSEO key = team skips it. No errors.
- **Cost**: $0 if no DataForSEO key (just reading production code). ~$0.10 if running the AIO analyzer.

### Lesson 17: Team & Batch Processing

- **Key moment**: Batch article creation — multiple articles in parallel.
- **Cost**: ~$1-3 per batch run. Consider demoing once.

### Lesson 18: Local File Storage

- **Safe to experiment**: Creating/reading/updating articles in `content/` is free.
- **Key moment**: When students see their article appear as a `.md` file.

### Lesson 19: How Everything Connects

- **Short lesson** — trace how a request flows through the system.
- **Live demo**: Walk through the project structure.

### Lesson 20: Web Interface

- **Live demo**: Run the web app (two terminals) and let students see streaming responses.
- **Teaches vibecoding**: How Claude Code generated `serve.py` from the team definition.

### Lesson 21: Extending the Product

- **Capstone lesson**. Students design a new agent (Proofreader) and trace through all the steps.
- **No API calls** — students plan and verify without running agents.
- **Vibecoding section**: How Claude Code built the React frontend.

## Checkpoints

### After Module 1 (lesson 4)
Ask students to: create a variable, a list, and a dict; write a function; show their API key status from lesson 4's verification cell.

### After Module 2 (lesson 7)
Ask students to: explain tokens, context windows, knowledge cutoffs; write a prompt with Role/Task/Constraints/Examples.

### After Module 3 (lesson 13)
Ask students to: explain agents, tools, structured output; access nested data from a schema; describe the mini pipeline flow.

### After Module 4 (lesson 17)
Ask students to: explain what the Content Writer does; describe how the Team delegates; explain batch processing.

### After Module 5 (lesson 21)
Ask students to: use the web interface; explain how all pieces connect; name 3 files in `output/backend/` and describe what each does.

## Post-course: next steps for learners

After completing the course, learners can:

1. **Customize agent instructions** — Edit `output/backend/agents/content_writer.py` to change writing style
2. **Add target keywords** — Provide keywords when creating articles via the web interface
3. **Run batch generation** — Ask the team to create multiple articles at once
4. **Monitor output quality** — Review generated articles in `content/`

For learners who want to go deeper (using Claude Code):
1. Add a new tool to an agent (e.g., Google Search Console API)
2. Add a proofreading agent to the team
3. Add translation to generate multilingual content
4. Extend the frontend with new features
