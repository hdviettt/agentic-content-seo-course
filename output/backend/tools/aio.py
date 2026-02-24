"""
AIO (AI Overview) analysis -- checks what Google's AI says about a topic.

Queries the DataForSEO SERP API to extract Google AI Overview content for
keywords.

Also houses get_dataforseo_credentials() since both AIO and image search
use DataForSEO.
"""

import base64
import json
import os

import httpx
from agno.tools import Toolkit
from agno.utils.log import logger


def get_dataforseo_credentials() -> tuple[str, str] | None:
    """Decode DATA_FOR_SEO_API_KEY into a (login, password) tuple.

    The env var format is:  Basic <base64(login:password)>
    Returns None if the env var is missing or malformed.
    """
    raw = os.getenv("DATA_FOR_SEO_API_KEY", "").strip()
    if not raw:
        return None

    # Strip the "Basic " prefix if present
    if raw.startswith("Basic "):
        raw = raw[len("Basic "):]

    try:
        decoded = base64.b64decode(raw).decode("utf-8")
    except Exception:
        return None

    if ":" not in decoded:
        return None

    login, password = decoded.split(":", 1)
    return (login, password)


class AIOTools(Toolkit):
    """Toolkit for retrieving Google AI Overviews via DataForSEO."""

    def __init__(self, login: str, password: str):
        self.auth = (login, password)
        super().__init__(name="aio_tools", tools=[self.get_ai_overview])

    def get_ai_overview(self, keyword: str, location_code: int = 2840,
                        language_code: str = "en") -> str:
        """Get Google's AI Overview for a keyword.

        Queries the DataForSEO SERP API with AI Overview loading enabled.
        Returns JSON with the AI Overview content, or indicates no AIO exists.

        Args:
            keyword: The search term to check.
            location_code: DataForSEO location code (default 2840 = United States).
            language_code: Language code (default "en").

        Returns:
            JSON string with keyword, has_aio, and (if present) content and references.
        """
        try:
            response = httpx.post(
                "https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
                auth=self.auth,
                json=[{
                    "keyword": keyword,
                    "location_code": location_code,
                    "language_code": language_code,
                    "load_async_ai_overview": True,
                }],
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

            tasks = data.get("tasks", [])
            if not tasks or not tasks[0].get("result"):
                return json.dumps({"keyword": keyword, "has_aio": False})

            items = tasks[0]["result"][0].get("items", [])

            # Find the AI Overview item
            aio_item = None
            for item in items:
                if item.get("type") == "ai_overview":
                    aio_item = item
                    break

            if not aio_item:
                return json.dumps({"keyword": keyword, "has_aio": False})

            # Extract content and references from the AI Overview
            sections = []
            references = []

            for element in aio_item.get("items") or []:
                if element.get("text"):
                    sections.append(element["text"])
                for ref in element.get("references") or []:
                    references.append({
                        "title": ref.get("title", ""),
                        "url": ref.get("url", ""),
                        "source": ref.get("source", ""),
                    })

            content_markdown = "\n\n".join(sections) if sections else ""

            return json.dumps({
                "keyword": keyword,
                "has_aio": True,
                "content_markdown": content_markdown,
                "sections": sections,
                "references": references,
            })

        except Exception as e:
            logger.warning(f"DataForSEO AIO check failed for '{keyword}': {e}")
            return json.dumps({"keyword": keyword, "has_aio": False, "error": str(e)})


# ============================================================
# Standalone functions (used internally)
# ============================================================


def get_ai_overview(keyword, location_code=2840, language_code="en"):
    """Get Google's AI Overview for a keyword (standalone function).

    Returns a parsed dict (not JSON string). Returns None if DataForSEO
    is not configured.
    """
    creds = get_dataforseo_credentials()
    if creds is None:
        logger.warning("DataForSEO not configured -- cannot check AI Overviews")
        return None

    toolkit = AIOTools(login=creds[0], password=creds[1])
    result_json = toolkit.get_ai_overview(keyword, location_code, language_code)
    return json.loads(result_json)


# ============================================================
# Agent-facing tool functions (return JSON strings)
# ============================================================


def analyze_keyword_aio(keyword: str, article_id: str = "") -> str:
    """Analyze what Google's AI Overview says about a keyword.

    Calls the DataForSEO SERP API to fetch the AI Overview for the keyword.

    Args:
        keyword: The search term to analyze.
        article_id: Optional article ID (for context, not used for storage).

    Returns:
        JSON with the AI Overview content, references, and whether an AIO exists.
    """
    result = get_ai_overview(keyword)
    if result is None:
        return json.dumps({"error": "DataForSEO not configured. Set DATA_FOR_SEO_API_KEY in .env."})

    return json.dumps(result)


def optimize_for_aio(article_id: str) -> str:
    """Compare an article against current AI Overviews for its keywords.

    Fetches fresh AIO data for each of the article's target keywords and
    returns a comparison showing what the AI Overview covers vs what the
    article covers, plus content gaps and cited sources.

    Args:
        article_id: The article ID to optimize.

    Returns:
        JSON with per-keyword AIO comparison data and the article's markdown.
    """
    from tools.storage import get_article

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

        comparisons.append({
            "keyword": kw,
            "has_aio": aio_data.get("has_aio", False),
            "aio_content": aio_data.get("content_markdown", ""),
            "aio_references": aio_data.get("references", []),
            "article_has_content": bool(article.get("article_markdown")),
            "article_word_count": article.get("word_count"),
        })

    # Extract section headings -- agent doesn't need the full article to analyze gaps
    markdown = article.get("article_markdown", "")
    headings = [line.strip()[3:].strip() for line in markdown.split("\n") if line.strip().startswith("## ")]

    return json.dumps({
        "article_id": article_id,
        "topic": article["topic"],
        "article_sections": headings,
        "article_word_count": article.get("word_count"),
        "comparisons": comparisons,
    })
