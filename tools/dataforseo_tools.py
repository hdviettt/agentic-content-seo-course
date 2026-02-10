import json

import httpx
from agno.tools import Toolkit
from agno.utils.log import logger


class DataForSEOTools(Toolkit):
    def __init__(self, login: str, password: str):
        self.auth = (login, password)
        self.base_url = "https://api.dataforseo.com/v3"
        super().__init__(name="dataforseo_tools", tools=[self.search_images])

    def search_images(self, query: str, max_results: int = 5) -> str:
        """Search for images using DataForSEO Image Search API. Returns JSON list of image results with URLs and descriptions."""
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
