# Curriculum Issues — Full Audit (2026-02-24)

Analysis from the perspective of an SEO professional with zero coding experience.

## Critical — Will crash when students run it

- [ ] **L13 cell-11**: `from agents import ContentOutline, OutlineSection` — these classes don't exist anywhere in the codebase. Removed during flatten refactor (`fe0aed9`). Cell will throw `ImportError`.
- [ ] **L13 cell-4**: Markdown references `agents/schemas.py` — file doesn't exist.

**Fix**: Either remove the cell and reference, or create `output/backend/agents/schemas.py` with those classes and export from `__init__.py`.

---

## Structural — Wrong diagrams, filenames, ordering

### File structure diagrams wrong in L19, L20, L21

All show `output/chat.py`, `output/serve.py`. Actual structure is `output/backend/chat.py`, `output/backend/serve.py`. The `backend/` level is missing from every diagram. Code cells use the correct paths — only the visual diagrams are wrong.

### 6 notebook filenames don't match content

| File | Filename says | Actual lesson title |
|------|--------------|---------------------|
| `15_research_and_outline.ipynb` | Research and outline | The Content Writer |
| `16_writer_and_images.ipynb` | Writer and images | Image Finder and AIO Analyzer |
| `17_full_pipeline.ipynb` | Full pipeline | Team and Batch Processing |
| `18_database.ipynb` | Database | Storing Articles Locally |
| `19_command_line.ipynb` | Command line | How Everything Connects |
| `20_chat_interface.ipynb` | Chat interface | The Web Interface |

Same issue exists in Vietnamese counterparts (`lessons_vi/`).

### L18 (storage) placed after L15-L17 which already use storage

Students call `save_article()`, `list_all_articles()`, `get_article_content()` dozens of times in L15-L17 before L18 "introduces" them. Feels redundant. Either move L18 before L15 or reframe as "under the hood."

### L10 breaks the agent-building narrative

Module 3 arc: agents → tools → structured output → chaining → pipeline. L10 (raw HTTP/API calling) drops to a different abstraction level between L09 (agent+tools) and L11 (structured output). Both L12 and L13 summary tables skip L10 entirely.

**Options**: (a) Move L10 to end of Module 2 as a bonus, (b) rename as "Deep Dive: What Happens Inside Tools" and mark optional, (c) keep but add to summary tables and fix L09 "next lesson" teaser.

---

## High — Factual errors and wrong references

- [ ] **L06 cell-6**: References `output/backend/agents/researcher.py` — doesn't exist. Should reference `content_writer.py`.
- [ ] **L09 cell-10**: "Next lesson" says "structured output" — next is actually L10 (API Calling).
- [ ] **L20 exercise answer**: Says "3 custom routes" in serve.py — actually 4 (missed `POST /api/chat`).
- [ ] **L21 cell-11**: Says `frontend/package.json` — should be `output/frontend/package.json`.
- [ ] **L01 cell-11 vs cell-12**: Exercise instructions say `your_name`/`department`/`years` but code uses `company`/`employees`.

---

## Medium — Concepts used before they're taught

| Concept | First used | First explained |
|---------|-----------|----------------|
| `if` statements | L02 cell-7 | **Never** |
| `==` comparison | L02 exercise | **Never** |
| `enumerate()` | L02 cell-9 | **Never** |
| `sys.path.insert` | L09 cell-2 | L13 cell-10 (4 lessons later) |
| `json.loads()` | L15 cell-11 | L20 cell-9 (5 lessons later) |
| `try/except` | L04 cell-13 | L17 cell-2 (13 lessons later) |
| Classes (`Agent(...)`) | L08 cell-6 | L11 cell-4 (3 lessons later) |
| `.get()` dict method | L03 cell-7 | **Never** |
| `//` floor division | L03 cell-7 | **Never** |

### Other confusing moments

- [ ] **L02**: Nested structures section (cells 6-7) appears before for-loop explanation (cells 8-9). Should reorder.
- [ ] **L03**: `.title()` answer produces `"On-Page Seo Guide"` not `"SEO"` — Python gotcha never acknowledged.
- [ ] **L05**: Temperature demo uses list comprehensions and `**` — impenetrable for non-coders. Add "don't worry about the code, focus on the output" note.
- [ ] **L15**: Says "Let's build the same agent from scratch" but code differs from production version.
- [ ] **L15**: Shows `ContentOutline` schema then says "the Content Writer doesn't use this" — orphaned.
- [ ] **L17**: Batch processing described as deterministic parallel but it's LLM-dependent.
- [ ] **L20**: Shows entire serve.py source then says "you don't need to know FastAPI" — contradictory.

---

## Low — Polish

- [ ] **L04**: Only lesson with no exercise (breaks the pattern).
- [ ] **L04**: Module 2 preview says "Working with AI Agents" but M2 is conceptual theory.
- [ ] **L04**: fastapi/uvicorn described as "web interface" but they're transitive dependencies.
- [ ] **L07**: Embeddings section feels disconnected — explicitly says "we don't use this." Move to end as bonus.
- [ ] **L12**: Only one runnable chaining example (every other lesson has 2-3).
- [ ] **L18**: Never shows actual `storage.py` source code despite being the storage lesson.
- [ ] **L20**: No screenshots of the web interface.
- [ ] **L21**: `ProofreadResult` schema created but never used in the agent definition.
- [ ] **storage.py docstrings**: Say "timestamp string" for article IDs (they're slugs).

---

## What's good (keep these)

- **SEO relevance** throughout — every example uses real SEO data
- **L01 motivational framing** — n8n comparison, "you're not becoming a developer"
- **L05 hallucination warning** — directly relevant for content teams
- **L06 SEO-to-prompt-engineering table** — translates existing skills to new ones
- **L07 cost estimation** — concrete dollar figures for business justification
- **L08 "why agentic" intro** — best opening in Module 3
- **L19 request tracing** — best conceptual lesson, traces full system flow
- **L21 verification checklist** — references every module, strong capstone
- **Conditional tool patterns** — DataForSEO degradation shown consistently
- **Fill-in-the-blank exercises** — consistent pattern, appropriate difficulty

---

## Suggested fix order

1. **Critical** — L13 crash (10 min)
2. **Filenames** — rename 6 EN + 6 VI files
3. **File structure diagrams** — fix `backend/` in L19, L20, L21
4. **Factual errors** — L06, L09, L01, L20, L21
5. **Teach `if` statements** — add section to L02
6. **Structural reorder** — L18 placement, L10 framing
