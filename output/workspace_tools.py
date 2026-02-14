"""
Workspace tools -- plain Python functions for the conversational team.

Each function wraps existing pipeline/DB logic and returns a string that
the team member agents interpret for conversational responses. These are
passed directly as tools=[...] to Agno agents.
"""

import io
import json
import contextlib


# ============================================================
# Content Creation
# ============================================================


def create_article(topic: str, keywords: str = "") -> str:
    """Create a new SEO article on the given topic. Runs the full content
    generation pipeline (research, outline, write, image enrichment).

    Args:
        topic: The article topic to write about.
        keywords: Optional comma-separated target keywords (e.g. "marathon training,running plan").

    Returns:
        JSON with article_id, status, word_count, and output file path.
    """
    from db import create_article as db_create_article, get_article
    from pipeline import run_content_pipeline

    kw_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else None
    article_id = db_create_article(topic, target_keywords=kw_list)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        success = run_content_pipeline(article_id, topic)

    article = get_article(article_id)
    return json.dumps({
        "article_id": article_id,
        "topic": topic,
        "status": article["status"] if article else ("review" if success else "error"),
        "word_count": article.get("word_count") if article else None,
        "output_file": article.get("output_file") if article else None,
        "pipeline_log": buf.getvalue(),
    })


def create_article_batch(topics_json: str) -> str:
    """Create multiple articles in batch.

    Args:
        topics_json: JSON array of objects, each with "topic" (required)
                     and optional "keywords" (comma-separated string).
                     Example: [{"topic": "Marathon training", "keywords": "marathon,running"}]

    Returns:
        JSON with batch_id and per-topic results.
    """
    from pipeline import run_batch

    topics = json.loads(topics_json)
    # Normalize keywords from comma-separated strings to lists
    for t in topics:
        if "keywords" in t and isinstance(t["keywords"], str):
            t["keywords"] = [k.strip() for k in t["keywords"].split(",") if k.strip()]

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        batch_id = run_batch(topics)

    return json.dumps({
        "batch_id": batch_id,
        "topic_count": len(topics),
        "log": buf.getvalue(),
    })


# ============================================================
# Status & Details
# ============================================================


def list_all_articles(status_filter: str = "", batch_id: str = "") -> str:
    """List all articles in the workspace, optionally filtered.

    Args:
        status_filter: Filter by status (queued, researching, outlining, writing,
                       enriching, review, error). Leave empty for all.
        batch_id: Filter by batch ID. Leave empty for all.

    Returns:
        JSON array of article summaries.
    """
    from db import list_articles

    articles = list_articles(
        status=status_filter or None,
        batch_id=batch_id or None,
    )
    return json.dumps([
        {
            "id": a["id"],
            "topic": a["topic"],
            "status": a["status"],
            "word_count": a["word_count"],
            "created_at": a["created_at"],
            "updated_at": a["updated_at"],
        }
        for a in articles
    ])


def get_article_details(article_id: int) -> str:
    """Get full details for a specific article.

    Args:
        article_id: The article ID to look up.

    Returns:
        JSON with all article fields (excluding full markdown content).
    """
    from db import get_article

    article = get_article(article_id)
    if not article:
        return json.dumps({"error": f"Article {article_id} not found."})

    return json.dumps({
        "id": article["id"],
        "topic": article["topic"],
        "status": article["status"],
        "word_count": article["word_count"],
        "target_keywords": json.loads(article["target_keywords"]) if article.get("target_keywords") else None,
        "meta_description": article.get("meta_description"),
        "output_file": article.get("output_file"),
        "batch_id": article.get("batch_id"),
        "error_message": article.get("error_message"),
        "created_at": article["created_at"],
        "updated_at": article["updated_at"],
    })


def get_article_content(article_id: int) -> str:
    """Get the full Markdown content of an article.

    Args:
        article_id: The article ID to retrieve content for.

    Returns:
        The article's Markdown content, or an error message.
    """
    from db import get_article

    article = get_article(article_id)
    if not article:
        return f"Article {article_id} not found."
    if not article.get("article_markdown"):
        return f"Article {article_id} has no content yet."
    return article["article_markdown"]


def get_version_history(article_id: int) -> str:
    """Get the version history for an article.

    Args:
        article_id: The article ID to get history for.

    Returns:
        JSON array of versions with version number, date, summary, and word count.
    """
    from db import get_article_versions

    versions = get_article_versions(article_id)
    if not versions:
        return json.dumps({"message": f"No versions found for article {article_id}."})

    return json.dumps([
        {
            "version": v["version_number"],
            "created_at": v["created_at"],
            "change_summary": v["change_summary"],
            "word_count": len(v["article_markdown"].split()) if v["article_markdown"] else 0,
        }
        for v in versions
    ])
