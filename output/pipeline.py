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
from datetime import datetime

from agents import research_agent, outline_agent, writer_agent, image_agent
from db import update_article_status, save_article_version, create_article


def run_content_pipeline(article_id, topic):
    """Run the full content pipeline for a single article.

    Updates the article's status in the database at each step so you can
    always see where an article is in the pipeline via `cli.py status`.
    On error, the article stays at the failed step with an error message.

    Returns True on success, False on error.
    """
    try:
        # ---- Step 1: Research ----
        print(f"  Researching: \"{topic}\"...")
        update_article_status(article_id, "researching")

        research_response = research_agent.run(
            f"Research this topic thoroughly for an SEO article: {topic}"
        )
        research_notes = research_response.content

        # ---- Step 2: Outline ----
        print(f"  Creating outline...")
        update_article_status(article_id, "outlining")

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

        # ---- Step 3: Write ----
        print(f"  Writing article...")
        update_article_status(article_id, "writing")

        write_response = writer_agent.run(
            f"Write a full SEO article based on this outline:\n\n{outline_json}"
        )
        article_markdown = write_response.content

        update_article_status(article_id, "writing", article_markdown=article_markdown)

        # ---- Step 4: Enrich with images ----
        print(f"  Enriching with images...")
        update_article_status(article_id, "enriching")

        if image_agent is not None:
            enrich_response = image_agent.run(
                f"Search for relevant images and insert them into this article:\n\n{article_markdown}"
            )
            enriched = enrich_response.content
            final_markdown = enriched.markdown_content if hasattr(enriched, "markdown_content") else str(enriched)
        else:
            final_markdown = article_markdown

        # ---- Export to file ----
        content_dir = os.path.join(os.path.dirname(__file__), "..", "content")
        os.makedirs(content_dir, exist_ok=True)
        slug = topic.lower().replace(" ", "-")[:50]
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(content_dir, f"{slug}-{timestamp}.md")
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

        print(f"  Done! ({word_count:,} words) -> {filename}")
        return True

    except Exception as e:
        print(f"  Error: {e}")
        update_article_status(article_id, "error", error_message=str(e))
        return False


# ============================================================
# Batch Processing
# ============================================================


def run_batch(topics, batch_id=None):
    """Create and generate articles for a list of topics.

    Args:
        topics:   List of dicts, each with "topic" (required) and "keywords" (optional).
        batch_id: Optional batch identifier. Auto-generated if not provided.

    Returns the batch_id (useful for later filtering with `cli.py status --batch`).
    """
    if batch_id is None:
        batch_id = f"batch-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    print(f"Batch: {batch_id}")
    print(f"Topics: {len(topics)}\n")

    # Phase 1: Create all article records upfront so they appear in `status` immediately
    article_ids = []
    for t in topics:
        aid = create_article(
            topic=t["topic"],
            target_keywords=t.get("keywords"),
            batch_id=batch_id,
        )
        article_ids.append(aid)

    # Phase 2: Process each article through the full pipeline
    succeeded = 0
    failed = 0
    for i, (aid, t) in enumerate(zip(article_ids, topics), 1):
        print(f"[{i}/{len(topics)}] {t['topic']}")
        ok = run_content_pipeline(aid, t["topic"])
        if ok:
            succeeded += 1
        else:
            failed += 1

    print(f"\nBatch complete: {succeeded} succeeded, {failed} failed")
    return batch_id


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
