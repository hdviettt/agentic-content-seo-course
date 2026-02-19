# Teacher's Guide

This guide helps you teach the Agentic Content SEO curriculum effectively. It covers preparation, pacing, per-lesson notes, and known pitfalls.

## Course overview

- **20 lessons** across 5 modules
- **Target audience**: Non-technical staff (marketing, SEO, content teams) with zero coding experience
- **Total time**: 12-14 hours of instruction, best delivered across 3 days
- **Goal**: Learners understand how the AI content pipeline works, can run and read the code, and can use Claude Code to extend and modify it

## Before teaching

### Classroom setup

1. **Install Python 3.12+** on every machine
2. **Pre-install all packages**: `python -m pip install -r requirements.txt`
3. **Distribute API keys** — create a shared `.env` file or give each student their own keys
4. **Set up Airtable**: each student needs `AIRTABLE_PAT` in `.env`, then run `python output/tools/airtable.py` to create the tables
5. **Test the full pipeline** on at least one machine: run `python output/chat.py` and ask it to create a test article — this confirms all API keys and Airtable work
5. **Open Jupyter** and verify notebooks load: `jupyter notebook lessons_en/`

### API cost planning

| Activity | Approximate cost per student |
|----------|------------------------------|
| Module 1 (lessons 1-4) | $0 (no API calls) |
| Module 2 (lessons 5-7) | $0 (no API calls) |
| Module 3 (lessons 8-12) | $0.75-1.50 (Sonnet calls, mini pipeline) |
| Module 4 (lessons 13-15) | $2-5 (Sonnet + Grok, full pipeline) |
| Module 5 (lessons 16-18) | $0-3 (DB is free, creating articles costs) |
| **Total per student** | **$3-10** |

For a class of 10: budget $30-100 in API costs. Module 4 is the most expensive part because lesson 15 runs the full 4-agent pipeline.

**Cost control tips:**
- Modules 1 and 2 are completely free — no API calls at all. Lessons 13 (Claude Code) and 20 (Extending) are also free
- In Module 3, have students run each demo cell only once (no re-runs)
- In lesson 15, the writer agent cell takes 1-2 minutes and costs ~$0.50-1 per run. Consider running it as a live demo rather than having every student run it
- In lesson 15, the full pipeline run costs ~$1-3. You can demo this once and let students just read the output
- Module 5 lessons 17-18 don't need to create new articles — status and history queries are free

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
| Morning 2 | 10-11 | 75 min | Structured output + chaining. Conceptually harder. |
| Afternoon 1 | 12 | 50 min | Mini pipeline. Key bridge lesson. |
| Afternoon 2 | 13-14 | 90 min | Real agents. Compare to what they built in Module 3. |

**Checkpoint**: By end of Day 2, every student should have run `agent.run()` successfully, seen a 3-agent pipeline work, and understood nested schemas.

### Day 3: Product + Capstone (4-5 hours)

| Block | Lessons | Duration | Notes |
|-------|---------|----------|-------|
| Morning 1 | 15 | 45 min | Full pipeline. Can demo once instead of all students running. |
| Morning 2 | 16 | 60 min | Database. Hands-on Airtable API is safe and free. |
| Afternoon 1 | 17-18 | 60 min | How everything connects + chat. Demo live. Let students try the chat interface. |
| Afternoon 2 | 19-20 | 90 min | Claude Code basics + extending the product. |
| Wrap-up | — | 30 min | Full walkthrough of `output/` folder structure. Q&A. |

## Per-lesson teaching notes

### Lesson 01: Hello Python

- **Pace**: Very slow. This is many students' first code ever.
- **Key moment**: When `print("Hello!")` works. Give them time to feel it.
- **Common issue**: Students type `Print` (capital P) — Python is case-sensitive.
- **Exercise**: The mini exercise at the end is important. Walk around and help.
- **Demo tip**: Show that changing a variable and re-running the cell updates the output. This teaches the "code runs top to bottom" mental model.

### Lesson 02: Lists and Dictionaries

- **Pace**: Medium. Lists are intuitive, dicts need more time.
- **Key moment**: The nested structure example (article with sections). Pause here and draw it on a whiteboard.
- **Common issue**: Students confuse `list[0]` (first item) with `list[1]`. Reinforce zero-indexing.
- **Common issue**: Missing commas in dict literals cause `SyntaxError`. Show how to read the error.
- **No exercise in this lesson** — consider assigning verbally: "Create a dict representing your favorite article, with title, author, and a list of 3 keywords."

### Lesson 03: Functions

- **Pace**: Slow. Functions are the hardest concept in Module 1.
- **Key moment**: `format_seo_title()` — when students see that a function can be called with different inputs and produces different outputs.
- **Common issue**: Indentation errors. Explain that Python uses spaces (not tabs) and the code inside a function must be indented.
- **Common issue**: Forgetting `return` — the function runs but nothing comes back.
- **Exercise**: The exercise at the end is well-designed. Let students struggle for 5-10 minutes before showing a solution.

**Exercise solution** (for your reference):
```python
def create_seo_title(keyword):
    return f"{keyword.title()} - The Complete A-to-Z Guide [{2026}]"

print(create_seo_title("content marketing"))
print(create_seo_title("link building"))
print(create_seo_title("technical seo"))
```

### Lesson 04: Setup and Packages

- **Pace**: Fast for the concepts, slow for the actual setup.
- **Key moment**: When `os.getenv("ANTHROPIC_API_KEY")` returns their actual key (masked). This connects .env files to real code.
- **Critical**: End this lesson with a setup verification. Have every student run the verification commands from the Learner's Guide. Do not proceed to Module 2 until everyone has a working setup.
- **Security**: Emphasize never committing `.env` to git. Show them the `.gitignore` file.

### Lesson 05: How LLMs Work (NEW)

- **Pace**: Medium. Conceptual but engaging.
- **No API calls** — completely free. Students can experiment freely.
- **Key moments**: (1) Token estimation exercise — makes cost tangible. (2) Temperature demo — students see how randomness affects output.
- **Teach**: Hallucinations. This is critical for SEO teams generating content. Emphasize: "The pipeline puts articles in 'review' status, not 'published' — by design."
- **Connect**: When discussing knowledge cutoffs, preview Lesson 09: "This is exactly why we give the agent DuckDuckGo search."
- **Common question**: "Is this really how it works?" Answer: "This is simplified, but the core idea is correct — prediction, tokens, and context windows are real."

### Lesson 06: Prompts and Context (NEW)

- **Pace**: Medium-fast. Very practical.
- **No API calls** — students build prompts as Python strings.
- **Key moment**: The bad vs good prompt comparison. Make students articulate WHY the good prompt is better.
- **Teach**: The 4 components (Role, Task, Constraints, Examples). Write them on the board. Students will reference this pattern in every future lesson.
- **Exercise**: Students create their own prompt templates. Encourage templates for their actual work tasks (meta descriptions, title generation, etc.).
- **Connect to agents**: "When you see `instructions=[...]` in the next module, you now know these ARE the system prompts."

### Lesson 07: Models and Choices (NEW)

- **Pace**: Medium. The cost exercise is engaging.
- **No API calls** — conceptual with code exercises.
- **Key moment**: The architecture constraint visualization — when students see that Grok can't combine tools + output_schema, and that this single limitation shaped the entire pipeline architecture.
- **Teach**: Embeddings are introduced as a concept. Don't go deep — just plant the seed for future learning.
- **Exercise**: The model selection exercise is great for discussion. Let students debate answers before revealing the suggested ones.
- **Transition**: "You now understand WHY everything works the way it does. In Module 3, you'll BUILD it."

### Lesson 08: Your First Agent

- **Pace**: Medium. The code is simple but the concept is new.
- **Key moment**: The first `agent.run()` response. Students will be amazed that 5 lines of code create an AI that responds intelligently.
- **Demo tip**: Run the two different agents (bullet point vs simple explainer) side by side. This makes `instructions` tangible — same question, different behavior based on instructions.
- **Connect to Module 2**: "Remember the system prompt from Lesson 6? `instructions` IS the system prompt."
- **Common issue**: API key errors. If `load_dotenv()` doesn't find the `.env` file, the agent fails silently or with a cryptic auth error. Make sure students' notebooks can find the `.env` file (it should be in the project root, and Jupyter should be launched from the project root).
- **Exercise**: Create an agent with a custom role. Let students pick something related to their actual work — this makes it personal and memorable.

### Lesson 09: Agent with Tools

- **Pace**: Medium.
- **Key moment**: The comparison between agent with and without tools. Run both live and discuss the difference.
- **Connect to Module 2**: "In Lesson 5, we learned about knowledge cutoffs. Tools solve that problem."
- **Common issue**: DuckDuckGo rate-limiting. If too many students search simultaneously, some will get errors. Solution: stagger the runs or have half the class watch while the other half runs.
- **Cost**: Each `agent.run()` with DuckDuckGo costs ~$0.02-0.05 (Sonnet tokens + search).
- **Exercise**: Research their own company using the agent. Students verify if the results are accurate — teaches critical evaluation of AI output.

### Lesson 10: Structured Output

- **Pace**: SLOW. This is the hardest lesson in Module 3.
- **JSON intro**: The notebook includes a JSON explanation section. Reinforce it on the whiteboard if needed.
- **Key moment**: When `outline.title` returns just the title string, and `outline.sections[0]` returns just the first section. This is the "why structured output matters" realization.
- **Connect to Module 2**: "In Lesson 6, we talked about specifying output format in prompts. `output_schema` automates this and guarantees the format."
- **Common issue**: Students confuse `response.content` (the Pydantic object) with a string. Show that `type(response.content)` returns `ArticleOutline`, not `str`.
- **Exercise**: Modify the schema to add a new field. This teaches that schemas are not magic — you control what the agent returns.

### Lesson 11: Chaining Agents

- **Pace**: Medium. The concept is simple but powerful.
- **Key moment**: When students see that `research.content` (Agent 1's output) is passed directly into `writer.run()` (Agent 2's input). The f-string is the "glue."
- **Teach**: Pause at the pipeline diagram and connect it to what they'll build next.
- **Exercise**: Add a third agent (Editor) to the chain. This directly previews the mini pipeline in Lesson 12.

### Lesson 12: Building a Mini Pipeline (NEW)

- **Pace**: Medium-slow. This is the critical bridge lesson.
- **Key moment**: When students access `outline.sections[0].heading` and `outline.sections[0].key_points` — nested data access. This is the skill they need for Module 4.
- **Teach**: The progressive schema building (SimpleOutline → Section + DetailedOutline). Draw the nesting structure on the board.
- **Important**: The `sys.path.insert` pattern is introduced here. Explain briefly: "This tells Python where to find the production code files." Students will see it again in Module 4.
- **Cost**: ~$0.20-0.40 for all three agents. Takes 1-2 minutes.
- **Comparison table**: Spend time on the mini vs real pipeline comparison. This sets expectations for Module 4.

### Lesson 13: Claude Code Basics

- **Pace**: Medium. Conceptual but very practical. This is the bridge from notebooks to real files.
- **No API calls** — students read project files and write prompts as strings.
- **Key moment**: Reading the actual CLAUDE.md file. Students realize: "This is the system prompt for Claude Code, just like instructions is the system prompt for an agent."
- **Teach**: The 5-step workflow (Understand → Plan → Implement → Verify → Iterate). Connect to the pipeline pattern.
- **Exercise**: Students write Claude Code prompts for 3 scenarios. Grade them on specificity (file paths, clear problem, constraints).

### Lesson 14: Research and Outline Agents

- **Pace**: Medium-slow. This is the first "real product" code.
- **Important**: The bridge lesson (12) handles the gap from mini pipeline to production code. Lesson 14 opens by connecting to the mini pipeline pattern students already practiced.
- **Key moment**: The full `ContentOutline` schema with nested `OutlineSection`. Students should recognize the pattern from Lesson 12.
- **Cost**: Running this cell costs ~$0.10-0.20 (Sonnet for research + outline).
- **Takes time**: The test run cell takes 30-60 seconds. Warn students.

### Lesson 15: Writer and Image Agents

- **Pace**: Medium.
- **Key moment**: Explain WHY different models are used. Students already understand the tradeoffs from Lesson 7 — now they see it applied.
- **Grok limitation**: Students learned about this in Lesson 7. Reinforce: "Remember the capability table? This is why the writer uses Grok."
- **Cost**: The writer cell costs ~$0.50-1 per run (Grok for long article). Consider demoing once rather than having all students run.
- **Image agent**: Since most students won't have image API keys, lesson 14 just shows the concept. This is fine.

### Lesson 16: Full Pipeline

- **Pace**: Fast for the lesson itself. Slow for the "soak it in" discussion.
- **Critical teaching moment**: Show the pipeline diagram (queued → researching → ... → review) and connect it to everything they've learned.
- **Cost**: ~$1-3 per full pipeline run. **Strongly recommend demoing once** rather than having all students run.
- **After running**: Use the chat interface (`python output/chat.py`) to check the article status. Then open the generated `.md` file. This connects the notebook to the real product.
- **sys.path.insert**: Students already saw this in Lesson 12. Just note: "Same pattern as the mini pipeline."

### Lesson 17: Database (Airtable)

- **Pace**: Slow. Database concepts are new for most.
- **Safe to experiment**: Airtable has a visual UI so students can see their data immediately. Encourage experimentation.
- **Key moment**: When they create an article and see it appear in Airtable. Connect to: "This is what the chat interface does under the hood when you ask it to create or filter articles."
- **Teach**: The concept of record IDs (strings like "recABC123") and how Airtable fields map to Python dicts.
- **The second half** uses the real `tools/airtable.py` module. This creates actual records in their Airtable base.

### Lesson 18: How Everything Connects

- **Pace**: Fast. This is a short lesson.
- **Key message**: "The chat interface calls the same `pipeline.py` and `tools/airtable.py` you already understand. This lesson shows how all the pieces fit together."
- **Live demo**: Walk through the project structure and show how `chat.py` calls `tools/workspace.py` which calls `pipeline.py` which calls `tools/airtable.py`.
- **Don't create articles** in class unless you want to spend API money. Show the flow but explain the cost.

### Lesson 19: Chat Interface

- **Pace**: Medium.
- **Live demo**: Run `python output/chat.py` in a terminal. Type a message and let students watch the team delegation happen in real time.
- **Key teaching point**: The Team concept — leader delegates to specialized members. Connect to real-world management.
- **Hands-on**: Let students call `list_all_articles()` and `get_article_details()` directly in the notebook to understand what the team members actually do.

### Lesson 20: Extending the Product

- **Pace**: Medium-slow. This is the capstone.
- **No API calls** — students trace through what Claude Code would do.
- **Key moment**: The verification checklist. Students apply knowledge from ALL modules to verify the proofreading agent implementation. This is the "aha" moment — everything connects.
- **Teach**: Walk through the schema validation (Cell 7). Students see that the Pydantic schema works without running any agent — it's just Python.
- **Extension ideas table**: Let students discuss which ones interest them. Some may want to try with Claude Code after the course.
- **Ending**: Take time with the course recap. Let students reflect on the journey from `print("Hello")` to understanding a full AI pipeline.

## Checkpoints — verify students are on track

### After Module 1 (lesson 4)

Ask students to:
1. Create a variable, a list, and a dict
2. Write a function that takes an article topic and returns a formatted title
3. Show their API key status (masked) from lesson 4's verification cell

If a student can't do these, they need more time with Module 1 before proceeding.

### After Module 2 (lesson 7)

Ask students to:
1. Explain in their own words: what is a token, what is a context window, what is a knowledge cutoff?
2. Write a prompt with all 4 components (Role, Task, Constraints, Examples) for an SEO task
3. Explain why the writer agent uses Grok instead of Claude (model capability constraint)

If a student can't explain tokens and prompts, revisit Lessons 5-6 before moving to Module 3.

### After Module 3 (lesson 12)

Ask students to:
1. Explain in their own words: what is an agent, what are tools, what is structured output?
2. Access nested data from a schema: "How would you get the heading of the first section from an outline?"
3. Explain the difference between `list[str]` and `list[Section]`

### After Module 4 (lesson 16)

Ask students to:
1. Draw the pipeline on paper: 4 agents, what each does, what data passes between them
2. Explain why the writer uses Grok instead of Claude (connecting Lesson 7 to Lesson 15)
3. Describe what happens in the database at each pipeline step

### After Module 5 (lesson 20)

Ask students to:
1. Use the chat interface to check article status and explain the output
2. Explain how the chat interface delegates tasks to specialized team members
3. Name 3 files in `output/` and describe what each does

## Curriculum notes

The following topics are covered in the notebooks. Reinforce them verbally where useful:

- **Tokens and context windows** — Lesson 05 explains these concepts. Reference them when discussing API costs.
- **Prompt engineering** — Lesson 06 covers this thoroughly. Reference the 4-component pattern (Role, Task, Constraints, Examples) whenever reviewing agent instructions.
- **Model tradeoffs** — Lesson 07 builds the decision framework. Reference it in Lessons 14-15 when students see the real model choices.
- **JSON** — Lesson 10 includes a JSON intro section. Draw on a whiteboard to reinforce.
- **Markdown** — Lesson 15 includes a Markdown intro section. Show a `.md` file and its rendered output side by side.
- **Error handling (try/except)** — Lesson 16 includes a full explanation. Walk through it on screen.
- **Nested schemas bridge** — Lesson 12 introduces nested schemas before the production code in Lesson 14. This eliminates the old complexity cliff.
- **Production code bridge** — Lesson 19 includes a "Reading the Production Code" section mapping lessons to `output/` files.
- **Setup verification** — Lesson 04 ends with a 4-check verification cell. Do not proceed until all students pass.
- **Cost warnings** — Lessons 08, 12, 14, 15, 16 include cost notes before expensive cells.

## Adapting the course

### For a shorter workshop (half day, ~4 hours)

Skip Module 1 if students have any programming background. Start at lesson 5.

Focus on: lessons 5, 6 (quick), 7, 8, 10, 11, 12 (quick), 15 (demo).

Skip: lessons 1-4, 9, 13, 14, 16, 17, 18, 19, 20.

### For a 2-day workshop (~8-10 hours)

Combine Modules 1-2 on Day 1 (skip exercises, demo-only). Combine Modules 3-5 on Day 2 (demo pipeline and database). Demo Claude Code from Lesson 13 in the wrap-up.

### For experienced developers

Skip Modules 1-2 entirely. Start at Module 3. Add time for code review — walk through the actual `output/` files in detail. Module 5's Lesson 20 is still valuable.

### For non-SEO teams

Replace SEO-specific terminology with their domain. The pipeline structure (research → outline → write → enrich) applies to any content generation workflow.

## Post-course: next steps for learners

After completing the course, learners can:

1. **Customize agent instructions** — Edit `output/agents/writer.py` to change writing style, or any agent file in `output/agents/` to adjust behavior
2. **Add target keywords** — Provide keywords when creating articles via the chat interface
3. **Run batch generation** — Create a `topics.csv` and process multiple articles via the chat interface
4. **Monitor output quality** — Use the chat interface to check status and review generated articles in `content/`

For learners who want to go deeper (using Claude Code):
1. Add a new tool to an agent (e.g., Google Search Console API)
2. Modify the pipeline to add a proofreading step
3. Change the writer model or try different models for different agents
4. Add translation to generate multilingual content
5. Build a web dashboard for the workspace
