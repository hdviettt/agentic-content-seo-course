"""
Content generation pipeline -- article creation and batch processing.

The core pipeline runs 4 agent steps sequentially with DB updates:
    1. Research   -- web search for topic info (Claude Sonnet + DuckDuckGo)
    2. Outline    -- structured outline from research (Claude Sonnet + output_schema)
    3. Write      -- full Markdown article from outline (Grok-4)
    4. Enrich     -- find and insert images (Claude Sonnet + image tools, optional)
"""

import csv
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from agents import research_agent, outline_agent, writer_agent, image_agent
from tools.airtable import update_article_status, save_article_version, create_article


# Lock for thread-safe printing during parallel batch processing.
# Without this, print output from multiple threads would mix mid-line.
_print_lock = threading.Lock()


def _thread_print(*args, **kwargs):
    """Thread-safe print -- acquires a lock so parallel output stays clean."""
    with _print_lock:
        print(*args, **kwargs)


def run_content_pipeline(article_id, topic, _print_fn=None):
    """Run the full content pipeline for a single article.

    Updates the article's status in the database at each step so you can
    always see where an article is in the pipeline.
    On error, the article stays at the failed step with an error message.

    Args:
        article_id: Airtable record ID for this article.
        topic: The article topic string.
        _print_fn: Optional custom print function. Used by parallel batch
                   processing to add article labels and thread-safe locking.
                   Defaults to the built-in print().

    Returns True on success, False on error.
    """
    if _print_fn is None:
        _print_fn = print

    pipeline_start = time.time()

    try:
        # ---- Step 1: Research ----
        _print_fn(f"  Researching: \"{topic}\"...")
        update_article_status(article_id, "researching")

        step_start = time.time()
        research_response = research_agent.run(
            f"Research this topic thoroughly for an SEO article: {topic}"
        )
        research_notes = research_response.content
        _print_fn(f"  Research done ({time.time() - step_start:.0f}s)")

        # ---- Step 2: Outline ----
        _print_fn(f"  Creating outline...")
        update_article_status(article_id, "outlining")

        step_start = time.time()
        outline_response = outline_agent.run(
            f"Create a structured content outline from these research notes:\n\n{research_notes}"
        )

        outline = outline_response.content
        outline_json = outline.model_dump_json(indent=2) if hasattr(outline, "model_dump_json") else str(outline)
        meta_desc = outline.meta_description if hasattr(outline, "meta_description") else None

        update_article_status(
            article_id, "outlining",
            outline_json=outline_json,
            meta_description=meta_desc,
        )
        _print_fn(f"  Outline done ({time.time() - step_start:.0f}s)")

        # ---- Step 3: Write ----
        _print_fn(f"  Writing article...")
        update_article_status(article_id, "writing")

        step_start = time.time()
        write_response = writer_agent.run(
            f"Write a full SEO article based on this outline:\n\n{outline_json}"
        )
        article_markdown = write_response.content

        update_article_status(article_id, "writing", article_markdown=article_markdown)
        _print_fn(f"  Writing done ({time.time() - step_start:.0f}s)")

        # ---- Step 4: Enrich with images ----
        if image_agent is not None:
            _print_fn(f"  Enriching with images...")
            update_article_status(article_id, "enriching")

            step_start = time.time()
            enrich_response = image_agent.run(
                f"Search for relevant images and insert them into this article:\n\n{article_markdown}"
            )
            enriched = enrich_response.content
            final_markdown = enriched.markdown_content if hasattr(enriched, "markdown_content") else str(enriched)
            _print_fn(f"  Images done ({time.time() - step_start:.0f}s)")
        else:
            _print_fn(f"  Skipping images (no image API keys configured)")
            final_markdown = article_markdown

        # ---- Export to file ----
        content_dir = os.path.join(os.path.dirname(__file__), "..", "content")
        os.makedirs(content_dir, exist_ok=True)
        slug = re.sub(r'[<>:"/\\|?*\']', '', topic.lower().replace(" ", "-"))[:50]
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        # Include article_id in filename to prevent collisions in parallel mode
        short_id = article_id[-6:] if len(article_id) > 6 else article_id
        filename = os.path.join(content_dir, f"{slug}-{short_id}-{timestamp}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_markdown)

        word_count = len(final_markdown.split())

        update_article_status(
            article_id, "review",
            article_markdown=final_markdown,
            output_file=filename,
            word_count=word_count,
        )

        save_article_version(article_id, final_markdown, "Initial generation")

        total_time = time.time() - pipeline_start
        _print_fn(f"  Done! ({word_count:,} words, {total_time:.0f}s total) -> {filename}")
        _print_fn(f"  Tip: Check your API dashboard for exact costs.")
        return True

    except Exception as e:
        _print_fn(f"  Error: {e}")
        update_article_status(article_id, "error", error_message=str(e))
        return False


# ============================================================
# Batch Processing
# ============================================================


def run_batch(topics, batch_id=None, parallel=False, max_workers=3):
    """Create and generate articles for a list of topics.

    Args:
        topics:      List of dicts, each with "topic" (required) and "keywords" (optional).
        batch_id:    Optional batch identifier. Auto-generated if not provided.
        parallel:    If True, process articles concurrently using threads.
                     Default False keeps the original one-at-a-time behavior.
        max_workers: How many articles to process at the same time when
                     parallel=True. Default 3 (conservative for API rate limits).

    Returns the batch_id (useful for later filtering by batch).
    """
    if batch_id is None:
        batch_id = f"batch-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    mode_label = f"parallel ({max_workers} workers)" if parallel else "sequential"
    print(f"Batch: {batch_id}")
    print(f"Topics: {len(topics)} ({mode_label})\n")

    # Phase 1: Create all article records upfront so they appear in status immediately
    article_ids = []
    for t in topics:
        aid = create_article(
            topic=t["topic"],
            target_keywords=t.get("keywords"),
            batch_id=batch_id,
        )
        article_ids.append(aid)

    # Phase 2: Process articles -- either one at a time or in parallel
    if parallel:
        succeeded, failed = _run_batch_parallel(article_ids, topics, max_workers)
    else:
        succeeded, failed = _run_batch_sequential(article_ids, topics)

    print(f"\nBatch complete: {succeeded} succeeded, {failed} failed")
    return batch_id


def _run_batch_sequential(article_ids, topics):
    """Process articles one at a time. This is the original behavior."""
    succeeded = 0
    failed = 0
    for i, (aid, t) in enumerate(zip(article_ids, topics), 1):
        print(f"[{i}/{len(topics)}] {t['topic']}")
        ok = run_content_pipeline(aid, t["topic"])
        if ok:
            succeeded += 1
        else:
            failed += 1
    return succeeded, failed


def _run_batch_parallel(article_ids, topics, max_workers):
    """Process articles concurrently using a thread pool.

    Each article gets its own thread. Output is prefixed with the article ID
    so you can trace which pipeline produced which log line.

    Think of it like a factory with multiple workers: each worker builds one
    article from start to finish, and we limit how many workers run at once.
    """
    succeeded = 0
    failed = 0
    total = len(topics)

    def _process_one(index, article_id, topic_entry):
        """Worker function -- runs one full pipeline in its own thread."""
        topic = topic_entry["topic"]
        short_id = article_id[-6:] if len(article_id) > 6 else article_id
        prefix = f"[{short_id}]"

        # Create a labeled print function so this article's output is traceable
        def labeled_print(*args, **kwargs):
            if args:
                _thread_print(f"{prefix} {args[0]}", *args[1:], **kwargs)
            else:
                _thread_print(**kwargs)

        labeled_print(f"({index}/{total}) Starting: \"{topic}\"")
        return run_content_pipeline(article_id, topic, _print_fn=labeled_print)

    # Submit all articles to the thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for i, (aid, t) in enumerate(zip(article_ids, topics), 1):
            future = executor.submit(_process_one, i, aid, t)
            futures[future] = t["topic"]

        # Collect results as they complete (not necessarily in order)
        for future in as_completed(futures):
            topic_name = futures[future]
            try:
                ok = future.result()
                if ok:
                    succeeded += 1
                else:
                    failed += 1
            except Exception as e:
                _thread_print(f"  Unexpected error for \"{topic_name}\": {e}")
                failed += 1

    return succeeded, failed


def load_topics_from_csv(filepath):
    """Load topics from a CSV file.

    Expected CSV format:
        topic,keywords
        How to train for a marathon,"marathon training,running plan"
        Best running shoes 2026,"running shoes,best shoes"

    The keywords column is optional. If present, keywords within it
    should be comma-separated (the whole field is quoted in the CSV).
    """
    topics = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            topic_entry = {"topic": row["topic"].strip()}
            if "keywords" in row and row["keywords"].strip():
                topic_entry["keywords"] = [k.strip() for k in row["keywords"].split(",")]
            topics.append(topic_entry)
    return topics
