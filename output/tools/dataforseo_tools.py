"""
DataForSEO image search toolkit + credential decoder.

Wraps the DataForSEO Google Images API to search for images by query.
Used by the Image Agent as an alternative to Freepik.

API docs: https://docs.dataforseo.com/v3/serp/google/images/
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


class DataForSEOTools(Toolkit):
    def __init__(self, login: str, password: str):
        self.auth = (login, password)
        self.base_url = "https://api.dataforseo.com/v3"
        super().__init__(name="dataforseo_tools", tools=[self.search_images])

    def search_images(self, query: str, max_results: int = 5) -> str:
        """Search for images using DataForSEO Image Search API.
        Returns JSON list of image results with URLs and descriptions."""
        try:
            response = httpx.post(
                f"{self.base_url}/serp/google/images/live",
                auth=self.auth,
                json=[{"keyword": query, "depth": max_results}],
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            results = []
            tasks = data.get("tasks", [])
            if tasks and tasks[0].get("result"):
                for item in tasks[0]["result"]:
                    for img in item.get("items", []):
                        results.append(
                            {
                                "title": img.get("title", ""),
                                "url": img.get("source_url", ""),
                                "source": img.get("source", ""),
                            }
                        )
            return json.dumps(results[:max_results])
        except Exception as e:
            logger.warning(f"DataForSEO search failed: {e}")
            return json.dumps({"error": str(e)})
