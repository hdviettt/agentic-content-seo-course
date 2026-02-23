"""
AIO (AI Overview) analysis -- checks what Google's AI says about a topic.

Queries the DataForSEO SERP API to extract Google AI Overview content for
keywords. Results can be saved to Airtable via tools.airtable.

Reuses credentials from agents.get_dataforseo_credentials().
"""

import json

import httpx
from agno.tools import Toolkit
from agno.utils.log import logger

from agents.image import get_dataforseo_credentials


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
# Standalone functions (used by workspace tools)
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


def save_aio_analysis(article_id, keyword, aio_data):
    """Save an AIO analysis result to Airtable.

    Args:
        article_id: The article this analysis is for.
        keyword: The keyword that was checked.
        aio_data: Dict from get_ai_overview() with has_aio, content_markdown, etc.

    Returns:
        JSON string with the record ID, or error message.
    """
    from tools.airtable import save_aio_analysis as db_save

    record_id = db_save(
        article_id=article_id,
        keyword=keyword,
        aio_content=aio_data.get("content_markdown", ""),
        references_json=json.dumps(aio_data.get("references", [])),
        has_aio=aio_data.get("has_aio", False),
    )
    return json.dumps({"record_id": record_id, "keyword": keyword})


def get_aio_analyses(article_id):
    """Get past AIO analyses for an article.

    Returns:
        List of analysis dicts from Airtable.
    """
    from tools.airtable import get_aio_analyses as db_get

    return db_get(article_id=article_id)
