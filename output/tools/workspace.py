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
    from tools.airtable import create_article as db_create_article, get_article
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


def retry_article(article_id: str) -> str:
    """Retry a failed article -- resets status to 'queued' and re-runs the full pipeline.

    Only works on articles with status 'error'. Use this when an article failed
    due to a temporary issue (network error, rate limit, etc.).

    Args:
        article_id: The article ID to retry. Must be in 'error' status.

    Returns:
        JSON with article_id, status, word_count, and output file path.
    """
    from tools.airtable import get_article, update_article_status
    from pipeline import run_content_pipeline

    article = get_article(article_id)
    if not article:
        return json.dumps({"error": f"Article {article_id} not found."})

    if article["status"] != "error":
        return json.dumps({
            "error": f"Article {article_id} is not in error status (current: {article['status']}). "
                     "Only articles with status 'error' can be retried."
        })

    # Reset status and clear error
    update_article_status(article_id, "queued", error_message=None)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        success = run_content_pipeline(article_id, article["topic"])

    article = get_article(article_id)
    return json.dumps({
        "article_id": article_id,
        "topic": article["topic"] if article else None,
        "status": article["status"] if article else ("review" if success else "error"),
        "word_count": article.get("word_count") if article else None,
        "output_file": article.get("output_file") if article else None,
        "pipeline_log": buf.getvalue(),
    })


def load_articles_from_csv(file_path: str, parallel: bool = False, max_workers: int = 3) -> str:
    """Load topics from a CSV file and run batch article creation.

    The CSV file should have columns: topic (required), keywords (optional, comma-separated).
    This is the same as batch article creation from the chat interface.

    Args:
        file_path: Path to the CSV file with topics.
        parallel:  If True, process articles at the same time instead of one by one.
        max_workers: How many articles to process at once when parallel is True. Default 3.

    Returns:
        JSON with batch_id and topic count.
    """
    from pipeline import run_batch, load_topics_from_csv

    topics = load_topics_from_csv(file_path)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        batch_id = run_batch(topics, parallel=parallel, max_workers=max_workers)

    return json.dumps({
        "batch_id": batch_id,
        "topic_count": len(topics),
        "parallel": parallel,
        "log": buf.getvalue(),
    })


def create_article_batch(topics_json: str, parallel: bool = False, max_workers: int = 3) -> str:
    """Create multiple articles in batch, optionally processing them in parallel.

    Args:
        topics_json: JSON array of objects, each with "topic" (required)
                     and optional "keywords" (comma-separated string).
                     Example: [{"topic": "Marathon training", "keywords": "marathon,running"}]
        parallel:    If True, process articles at the same time instead of
                     one by one. Faster but uses more API calls simultaneously.
        max_workers: How many articles to process at once when parallel is True.
                     Default 3.

    Returns:
        JSON with batch_id and per-topic results.
    """
    from pipeline import run_batch

    try:
        topics = json.loads(topics_json)
    except (json.JSONDecodeError, TypeError) as e:
        return json.dumps({"error": f"Invalid JSON: {e}"})
    # Normalize keywords from comma-separated strings to lists
    for t in topics:
        if "keywords" in t and isinstance(t["keywords"], str):
            t["keywords"] = [k.strip() for k in t["keywords"].split(",") if k.strip()]

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        batch_id = run_batch(topics, parallel=parallel, max_workers=max_workers)

    return json.dumps({
        "batch_id": batch_id,
        "topic_count": len(topics),
        "parallel": parallel,
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
    from tools.airtable import list_articles

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


def get_article_details(article_id: str) -> str:
    """Get full details for a specific article.

    Args:
        article_id: The article ID to look up.

    Returns:
        JSON with all article fields (excluding full markdown content).
    """
    from tools.airtable import get_article

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


def get_article_content(article_id: str) -> str:
    """Get the full Markdown content of an article.

    Args:
        article_id: The article ID to retrieve content for.

    Returns:
        The article's Markdown content, or an error message.
    """
    from tools.airtable import get_article

    article = get_article(article_id)
    if not article:
        return f"Article {article_id} not found."
    if not article.get("article_markdown"):
        return f"Article {article_id} has no content yet."
    return article["article_markdown"]


def get_version_history(article_id: str) -> str:
    """Get the version history for an article.

    Args:
        article_id: The article ID to get history for.

    Returns:
        JSON array of versions with version number, date, summary, and word count.
    """
    from tools.airtable import get_article_versions

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


# ============================================================
# AIO Analysis
# ============================================================


def analyze_keyword_aio(keyword: str, article_id: str = "") -> str:
    """Analyze what Google's AI Overview says about a keyword.

    Calls the DataForSEO SERP API to fetch the AI Overview for the keyword,
    then saves the result to Airtable if an article_id is provided.

    Args:
        keyword: The search term to analyze.
        article_id: Optional article ID to link the analysis to.

    Returns:
        JSON with the AI Overview content, references, and whether an AIO exists.
    """
    from tools.aio import get_ai_overview, save_aio_analysis

    result = get_ai_overview(keyword)
    if result is None:
        return json.dumps({"error": "DataForSEO not configured. Set DATA_FOR_SEO_API_KEY in .env."})

    # Save to Airtable if linked to an article
    if article_id:
        save_aio_analysis(article_id, keyword, result)

    return json.dumps(result)


def get_aio_history(article_id: str) -> str:
    """Get past AI Overview analyses for an article.

    Args:
        article_id: The article ID.

    Returns:
        JSON array of AIO analysis records sorted by date (newest first).
    """
    from tools.airtable import get_aio_analyses

    analyses = get_aio_analyses(article_id=article_id)
    if not analyses:
        return json.dumps({"message": f"No AIO analyses found for article {article_id}."})

    return json.dumps([
        {
            "keyword": a["keyword"],
            "has_aio": a["has_aio"],
            "aio_content": a["aio_content"][:500] if a["aio_content"] else "",
            "checked_date": a["checked_date"],
        }
        for a in analyses
    ])


def optimize_for_aio(article_id: str) -> str:
    """Compare an article against current AI Overviews for its keywords.

    Fetches fresh AIO data for each of the article's target keywords and
    returns a comparison showing what the AI Overview covers vs what the
    article covers, plus content gaps and cited sources.

    Args:
        article_id: The article ID to optimize.

    Returns:
        JSON with per-keyword AIO comparison data.
    """
    from tools.airtable import get_article
    from tools.aio import get_ai_overview, save_aio_analysis

    article = get_article(article_id)
    if not article:
        return json.dumps({"error": f"Article {article_id} not found."})

    # Parse keywords
    kw_raw = article.get("target_keywords")
    keywords = []
    if kw_raw:
        try:
            keywords = json.loads(kw_raw)
        except (json.JSONDecodeError, TypeError):
            pass

    if not keywords:
        return json.dumps({"error": "Article has no target keywords to analyze."})

    comparisons = []
    for kw in keywords:
        aio_data = get_ai_overview(kw)
        if aio_data is None:
            comparisons.append({
                "keyword": kw,
                "error": "DataForSEO not configured.",
            })
            continue

        # Save analysis to Airtable
        save_aio_analysis(article_id, kw, aio_data)

        comparisons.append({
            "keyword": kw,
            "has_aio": aio_data.get("has_aio", False),
            "aio_content": aio_data.get("content_markdown", ""),
            "aio_references": aio_data.get("references", []),
            "article_has_content": bool(article.get("article_markdown")),
            "article_word_count": article.get("word_count"),
        })

    return json.dumps({
        "article_id": article_id,
        "topic": article["topic"],
        "comparisons": comparisons,
    })
