"""
Web search via DataForSEO -- toolkit for researching topics.

Used by the Content Writer agent to research topics before writing articles.
"""

import json

import httpx
from agno.tools import Toolkit
from agno.utils.log import logger


class DataForSEOSearchTools(Toolkit):
    """Web search via DataForSEO SERP API."""

    def __init__(self, login: str, password: str):
        self.auth = (login, password)
        self.base_url = "https://api.dataforseo.com/v3"
        super().__init__(name="search_tools", tools=[self.web_search])

    def web_search(self, query: str, max_results: int = 10) -> str:
        """Search the web using Google via DataForSEO.

        Args:
            query: The search query.
            max_results: Maximum number of results to return (default 10).

        Returns:
            JSON list of search results with titles, URLs, and descriptions.
        """
        try:
            response = httpx.post(
                f"{self.base_url}/serp/google/organic/live/advanced",
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
                    if item.get("type") != "organic":
                        continue
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "description": item.get("description", ""),
                    })
            return json.dumps(results[:max_results])
        except Exception as e:
            logger.warning(f"DataForSEO web search failed: {e}")
            return json.dumps({"error": str(e)})
