"""
Image search via DataForSEO -- toolkit for finding relevant images.

Used by the Image Finder agent to search for and insert images into articles.
"""

import json

import httpx
from agno.tools import Toolkit
from agno.utils.log import logger


class DataForSEOImageTools(Toolkit):
    """Image search via DataForSEO."""

    def __init__(self, login: str, password: str):
        self.auth = (login, password)
        self.base_url = "https://api.dataforseo.com/v3"
        super().__init__(name="image_tools", tools=[self.search_images])

    def search_images(self, query: str, max_results: int = 5) -> str:
        """Search for images using DataForSEO Image Search API.

        Args:
            query: The image search query.
            max_results: Maximum number of results to return (default 5).

        Returns:
            JSON list of image results with URLs and descriptions.
        """
        try:
            response = httpx.post(
                f"{self.base_url}/serp/google/images/live/advanced",
                auth=self.auth,
                json=[{
                    "keyword": query,
                    "location_code": 2840,
                    "language_code": "en",
                    "depth": max_results,
                }],
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

            results = []
            tasks = data.get("tasks", [])
            if tasks and tasks[0].get("result"):
                for item in tasks[0]["result"][0].get("items", []):
                    if item.get("type") != "images_search":
                        continue
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("source_url", ""),
                        "alt": item.get("alt", ""),
                        "source": item.get("subtitle", ""),
                    })
            return json.dumps(results[:max_results])
        except Exception as e:
            logger.warning(f"DataForSEO image search failed: {e}")
            return json.dumps({"error": str(e)})
