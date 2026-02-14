# Teacher's Guide

This guide helps you teach the Agentic Content SEO curriculum effectively. It covers preparation, pacing, per-lesson notes, and known pitfalls.

## Course overview

- **14 lessons** across 4 modules
- **Target audience**: Non-technical staff (marketing, SEO, content teams) with zero coding experience
- **Total time**: 8-10 hours of instruction, best delivered across 2-3 days
- **Goal**: Learners understand how the AI content pipeline works and can run, read, and make basic modifications to the code

## Before teaching

### Classroom setup

1. **Install Python 3.12+** on every machine
2. **Pre-install all packages**: `python -m pip install -r requirements.txt`
3. **Distribute API keys** — create a shared `.env` file or give each student their own keys
4. **Test the full pipeline** on at least one machine: `python output/cli.py create "test article"` — this confirms all API keys work
5. **Open Jupyter** and verify notebooks load: `jupyter notebook lessons/`

### API cost planning

| Activity | Approximate cost per student |
|----------|------------------------------|
| Module 1 (lessons 1-4) | $0 (no API calls) |
| Module 2 (lessons 5-8) | $0.50-1.00 (Sonnet calls only) |
| Module 3 (lessons 9-11) | $2-5 (Sonnet + Grok, full pipeline) |
| Module 4 (lessons 12-14) | $0-3 (DB is free, creating articles costs) |
| **Total per student** | **$3-9** |

For a class of 10: budget $30-90 in API costs. Module 3 is the most expensive part because lesson 11 runs the full 4-agent pipeline.

**Cost control tips:**
- In Module 2, have students run each demo cell only once (no re-runs)
- In lesson 10, the writer agent cell takes 1-2 minutes and costs ~$0.50-1 per run. Consider running it as a live demo rather than having every student run it
- In lesson 11, the full pipeline run costs ~$1-3. You can demo this once and let students just read the output
- Module 4 lessons 13-14 don't need to create new articles — `status` and `history` commands are free

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
| Afternoon 1 | 05-06 | 60 min | First agents. The "wow" moment when the agent responds. |
| Afternoon 2 | 07-08 | 60 min | Structured output + chaining. Conceptually harder. |

**Checkpoint**: By end of Day 1, every student should have run `agent.run()` successfully and seen a 2-agent chain work.

### Day 2: The Real Thing (4-5 hours)

| Block | Lessons | Duration | Notes |
|-------|---------|----------|-------|
| Morning 1 | 09-10 | 90 min | Real agents. Compare to what they built in Module 2. |
| Morning 2 | 11 | 45 min | Full pipeline. Can demo once instead of all students running. |
| Afternoon 1 | 12 | 60 min | Database. Hands-on SQL in in-memory DB is safe and free. |
| Afternoon 2 | 13-14 | 60 min | CLI + chat. Demo both live. Let students try CLI commands. |
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

### Lesson 05: Your First Agent

- **Pace**: Medium. The code is simple but the concept is new.
- **Key moment**: The first `agent.run()` response. Students will be amazed that 5 lines of code create an AI that responds intelligently.
- **Demo tip**: Run the two different agents (bullet point vs simple explainer) side by side. This makes `instructions` tangible — same question, different behavior based on instructions.
- **Common issue**: API key errors. If `load_dotenv()` doesn't find the `.env` file, the agent fails silently or with a cryptic auth error. Make sure students' notebooks can find the `.env` file (it should be in the project root, and Jupyter should be launched from the project root).
- **Exercise**: Create an agent with a custom role. Let students pick something related to their actual work — this makes it personal and memorable.

### Lesson 06: Agent with Tools

- **Pace**: Medium.
- **Key moment**: The comparison between agent with and without tools. Run both live and discuss the difference.
- **Common issue**: DuckDuckGo rate-limiting. If too many students search simultaneously, some will get errors. Solution: stagger the runs or have half the class watch while the other half runs.
- **Cost**: Each `agent.run()` with DuckDuckGo costs ~$0.02-0.05 (Sonnet tokens + search).
- **Exercise**: Research their own company using the agent. Students verify if the results are accurate — teaches critical evaluation of AI output.

### Lesson 07: Structured Output

- **Pace**: SLOW. This is the hardest lesson in Module 2.
- **JSON intro**: The notebook now includes a JSON explanation section. Reinforce it on the whiteboard if needed.
- **Key moment**: When `outline.title` returns just the title string, and `outline.sections[0]` returns just the first section. This is the "why structured output matters" realization.
- **Common issue**: Students confuse `response.content` (the Pydantic object) with a string. Show that `type(response.content)` returns `ArticleOutline`, not `str`.
- **Exercise**: Modify the schema to add a new field. This teaches that schemas are not magic — you control what the agent returns.

### Lesson 08: Chaining Agents

- **Pace**: Medium. The concept is simple but powerful.
- **Key moment**: When students see that `research.content` (Agent 1's output) is passed directly into `writer.run()` (Agent 2's input). The f-string is the "glue."
- **Teach**: Pause at the pipeline diagram and connect it to what they'll build in Module 3.
- **Exercise**: Add a third agent (Editor) to the chain. This directly previews the pipeline pattern they'll see in Module 3.

### Lesson 09: Research and Outline Agents

- **Pace**: Medium-slow. This is the first "real product" code.
- **Important**: Explain that this lesson recreates the code from `output/agents/builders.py` and `output/agents/schemas.py`. Students are building the same thing the product uses.
- **Key moment**: The full `ContentOutline` schema with nested `OutlineSection`. Draw the structure on a whiteboard.
- **Cost**: Running this cell costs ~$0.10-0.20 (Sonnet for research + outline).
- **Takes time**: The test run cell takes 30-60 seconds. Warn students.

### Lesson 10: Writer and Image Agents

- **Pace**: Medium.
- **Key moment**: Explain WHY different models are used. The comparison table is excellent — make sure students understand this isn't random.
- **Grok limitation**: Spend time on why Grok can't combine tools + output_schema. This is a real-world constraint that affects architecture.
- **Cost**: The writer cell costs ~$0.50-1 per run (Grok for long article). Consider demoing once rather than having all students run.
- **Image agent**: Since most students won't have image API keys, lesson 10 just shows the concept. This is fine.

### Lesson 11: Full Pipeline

- **Pace**: Fast for the lesson itself. Slow for the "soak it in" discussion.
- **Critical teaching moment**: Show the pipeline diagram (queued → researching → ... → review) and connect it to everything they've learned.
- **Cost**: ~$1-3 per full pipeline run. **Strongly recommend demoing once** rather than having all students run.
- **After running**: Pull up `output/cli.py status` in a terminal to show the article in the database. Then open the generated `.md` file. This connects the notebook to the real product.
- **Prerequisite gap**: The `sys.path.insert(0, ...)` line is confusing. Briefly explain: "This tells Python where to find the production code files."

### Lesson 12: Database

- **Pace**: Slow. SQL is completely new for most.
- **Safe to experiment**: The in-memory database (`":memory:"`) disappears when the cell finishes. Students can't break anything. Encourage experimentation.
- **Key moment**: When they query with `WHERE status = ?` and see filtering work. Connect to: "This is what `cli.py status --filter review` does under the hood."
- **Teach**: The `?` placeholder for security (SQL injection). Even a brief mention plants the seed.
- **The second half** uses the real `db.py` module. This creates actual records in `workspace.db`. Explain the difference.

### Lesson 13: CLI

- **Pace**: Fast. This is a short lesson.
- **Live demo**: Open a terminal and run real commands. Let students follow along:
  - `python output/cli.py --help`
  - `python output/cli.py status`
  - `python output/cli.py status --article 1` (if an article exists from lesson 11)
- **Don't run `create`** in class unless you want to spend API money. Show the command but explain the cost.
- **Key message**: "The CLI calls the same `pipeline.py` and `db.py` you already understand. It's just a different way to trigger them."

### Lesson 14: Chat Interface

- **Pace**: Medium.
- **Live demo**: Run `python output/chat.py` in a terminal. Type a message and let students watch the team delegation happen in real time.
- **Key teaching point**: The Team concept — leader delegates to specialized members. Connect to real-world management.
- **Hands-on**: Let students call `list_all_articles()` and `get_article_details()` directly in the notebook to understand what the team members actually do.
- **End of course**: Use the congratulations section as a springboard for discussion. Ask: "What would you add or change?"

## Curriculum notes

The following topics are now covered in the notebooks themselves. Reinforce them verbally where useful:

- **JSON** — Lesson 07 now includes a JSON intro section. Draw on a whiteboard to reinforce.
- **Markdown** — Lesson 10 now includes a Markdown intro section. Show a `.md` file and its rendered output side by side.
- **Error handling (try/except)** — Lesson 11 now includes a full explanation. Walk through it on screen.
- **Module 2→3 bridge** — Lesson 09 now opens with a "What's Different" section that sets expectations for the complexity jump. Reinforce verbally.
- **Production code bridge** — Lesson 14 now includes a "Reading the Production Code" section mapping lessons to `output/` files.
- **Setup verification** — Lesson 04 now ends with a 4-check verification cell. Do not proceed until all students pass.
- **Cost warnings** — Lessons 05, 09, 10, 11 now include cost notes before expensive cells.

## Checkpoints — verify students are on track

### After Module 1 (lesson 4)

Ask students to:
1. Create a variable, a list, and a dict
2. Write a function that takes an article topic and returns a formatted title
3. Show their API key status (masked) from lesson 4's verification cell

If a student can't do these, they need more time with Module 1 before proceeding.

### After Module 2 (lesson 8)

Ask students to:
1. Explain in their own words: what is an agent, what are tools, what is structured output?
2. Predict what happens if you remove `tools=[DuckDuckGoTools()]` from the research agent
3. Explain why the research agent's output needs to be passed as a string to the writer agent

### After Module 3 (lesson 11)

Ask students to:
1. Draw the pipeline on paper: 4 agents, what each does, what data passes between them
2. Explain why the writer uses Grok instead of Claude
3. Describe what happens in the database at each pipeline step

### After Module 4 (lesson 14)

Ask students to:
1. Run `python output/cli.py status` and explain the output
2. Explain the difference between the CLI and chat interface
3. Name 3 files in `output/` and describe what each does

## Adapting the course

### For a shorter workshop (half day, ~4 hours)

Skip Module 1 if students have any programming background. Start at lesson 5.

Focus on: lessons 5, 6, 7 (quick), 8, 9 (demo), 11 (demo), 13 (quick demo).

Skip: lessons 1-4, 10 (image agent), 12 (database), 14 (chat).

### For experienced developers

Skip Modules 1-2 entirely. Start at Module 3. Add time for code review — walk through the actual `output/` files in detail.

### For non-SEO teams

Replace SEO-specific terminology with their domain. The pipeline structure (research → outline → write → enrich) applies to any content generation workflow.

## Post-course: next steps for learners

After completing the course, learners can:

1. **Customize agent instructions** — Edit `output/agents/builders.py` to change writing style, tone, or SEO approach
2. **Add target keywords** — Use `--keywords` flag to steer article content
3. **Run batch generation** — Create a `topics.csv` and process multiple articles
4. **Monitor output quality** — Use `cli.py status` and review generated articles in `content/`

For learners who want to go deeper:
1. Add a new tool to an agent (e.g., Google Search Console API)
2. Modify the pipeline to add a proofreading step
3. Change the writer model or try different models for different agents
