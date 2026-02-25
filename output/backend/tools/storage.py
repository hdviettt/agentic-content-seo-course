"""
Local file storage -- article metadata in JSON, content in .md files.

Articles are stored in the content/ directory:
  - content/articles.json  -- metadata (topic, keywords, status, word count)
  - content/{id}.md        -- full article Markdown

Article IDs are keyword slugs like "on-page-seo-meta-tags".
"""

import json
import os
import re
import threading
from datetime import datetime, timezone


_CONTENT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "content")
)
_METADATA_FILE = os.path.join(_CONTENT_DIR, "articles.json")
_lock = threading.Lock()


# ============================================================
# Internal helpers
# ============================================================


def _load_metadata() -> dict:
    """Read articles.json. Returns {} if file doesn't exist."""
    try:
        with open(_METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_metadata(data: dict):
    """Write articles.json directly (caller must hold _lock)."""
    os.makedirs(_CONTENT_DIR, exist_ok=True)
    with open(_METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _now() -> str:
    """Current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:50]


def _generate_id(keywords: str = "", topic: str = "") -> str:
    """Generate article ID from keywords or topic as a slug."""
    source = keywords or topic
    if not source:
        source = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    base = _slugify(source)
    if not base:
        base = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    path = os.path.join(_CONTENT_DIR, f"{base}.md")
    if not os.path.exists(path):
        return base
    # Handle collision
    for i in range(2, 100):
        candidate = f"{base}-{i}"
        if not os.path.exists(os.path.join(_CONTENT_DIR, f"{candidate}.md")):
            return candidate
    return base


def _md_path(article_id: str) -> str:
    """Path to the .md file for an article."""
    return os.path.join(_CONTENT_DIR, f"{article_id}.md")


# ============================================================
# Internal CRUD (used by aio.py)
# ============================================================


def get_article(article_id: str) -> dict | None:
    """Fetch a single article by ID. Returns dict or None."""
    metadata = _load_metadata()
    entry = metadata.get(article_id)
    if not entry:
        return None

    # Read content from .md file
    md_file = _md_path(article_id)
    try:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    keywords = entry.get("keywords", [])
    return {
        "id": article_id,
        "topic": entry.get("topic", ""),
        "target_keywords": json.dumps(keywords) if keywords else None,
        "status": entry.get("status", "review"),
        "article_markdown": content,
        "output_file": md_file,
        "word_count": entry.get("word_count"),
        "created_at": entry.get("created_at"),
        "updated_at": entry.get("updated_at"),
    }


def list_articles(status: str = None) -> list[dict]:
    """List articles, optionally filtered by status."""
    metadata = _load_metadata()
    results = []
    for article_id, entry in metadata.items():
        if status and entry.get("status") != status:
            continue
        keywords = entry.get("keywords", [])
        results.append({
            "id": article_id,
            "topic": entry.get("topic", ""),
            "target_keywords": json.dumps(keywords) if keywords else None,
            "status": entry.get("status", "review"),
            "article_markdown": None,  # Don't load content for listings
            "output_file": _md_path(article_id),
            "word_count": entry.get("word_count"),
            "created_at": entry.get("created_at"),
            "updated_at": entry.get("updated_at"),
        })
    return results


# ============================================================
# Agent-facing tool functions (return JSON strings)
# ============================================================


def save_article(topic: str, article_markdown: str, keywords: str = "") -> str:
    """Save a new article to disk.

    Args:
        topic: The article topic.
        article_markdown: The full article content in Markdown.
        keywords: Optional comma-separated target keywords.

    Returns:
        JSON with article_id, filename, and word_count.
    """
    word_count = len(article_markdown.split())
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []
    now = _now()

    with _lock:
        article_id = _generate_id(keywords=keywords, topic=topic)
        os.makedirs(_CONTENT_DIR, exist_ok=True)

        # Write .md file
        md_file = _md_path(article_id)
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(article_markdown)

        # Update metadata
        metadata = _load_metadata()
        metadata[article_id] = {
            "topic": topic,
            "keywords": kw_list,
            "status": "review",
            "word_count": word_count,
            "created_at": now,
            "updated_at": now,
        }
        _save_metadata(metadata)

    return json.dumps({
        "article_id": article_id,
        "topic": topic,
        "filename": md_file,
        "word_count": word_count,
        "status": "review",
    })


def list_all_articles(status_filter: str = "") -> str:
    """List all articles, optionally filtered by status.

    Args:
        status_filter: Filter by status (e.g. "review"). Leave empty for all.

    Returns:
        JSON array of article summaries.
    """
    articles = list_articles(status=status_filter or None)
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


def get_article_content(article_id: str) -> str:
    """Get an article's topic and full Markdown content.

    Args:
        article_id: The article ID (keyword slug, e.g. "on-page-seo-meta-tags").

    Returns:
        JSON with article_id, topic, and article_markdown.
    """
    article = get_article(article_id)
    if not article:
        return json.dumps({"error": f"Article {article_id} not found."})

    return json.dumps({
        "article_id": article_id,
        "topic": article["topic"],
        "article_markdown": article.get("article_markdown", ""),
    })


def update_article_content(article_id: str, article_markdown: str) -> str:
    """Update an article's Markdown content.

    Args:
        article_id: The article ID (keyword slug, e.g. "on-page-seo-meta-tags").
        article_markdown: The updated article Markdown.

    Returns:
        JSON with article_id and updated word_count.
    """
    word_count = len(article_markdown.split())

    with _lock:
        metadata = _load_metadata()
        if article_id not in metadata:
            return json.dumps({"error": f"Article {article_id} not found."})

        # Write .md file
        md_file = _md_path(article_id)
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(article_markdown)

        # Update metadata
        metadata[article_id]["word_count"] = word_count
        metadata[article_id]["updated_at"] = _now()
        _save_metadata(metadata)

    return json.dumps({
        "article_id": article_id,
        "word_count": word_count,
    })
