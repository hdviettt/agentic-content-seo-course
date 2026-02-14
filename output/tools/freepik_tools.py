"""
Freepik image search toolkit.

Wraps the Freepik REST API to search for stock photos by query.
Used by the Image Agent to find relevant images for articles.

API docs: https://docs.freepik.com/
"""

import json

import httpx
from agno.tools import Toolkit
from agno.utils.log import logger


class FreepikTools(Toolkit):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.freepik.com/v1"
        super().__init__(name="freepik_tools", tools=[self.search_images])

    def search_images(self, query: str, max_results: int = 5) -> str:
        """Search Freepik for stock images matching a query.
        Returns JSON list of image results with URLs and descriptions."""
        try:
            response = httpx.get(
                f"{self.base_url}/resources",
                headers={"x-freepik-api-key": self.api_key},
                params={
                    "term": query,
                    "limit": max_results,
                    "filters[content_type][photo]": 1,
                },
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("data", []):
                results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("image", {}).get("source", {}).get("url", ""),
                        "thumbnail": item.get("image", {}).get("source", {}).get("url", ""),
                    }
                )
            return json.dumps(results[:max_results])
        except Exception as e:
            logger.warning(f"Freepik search failed: {e}")
            return json.dumps({"error": str(e)})
