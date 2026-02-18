"""
Image Agent -- finds and inserts images into articles (optional).

Model: Claude Sonnet | Tools: Freepik, DataForSEO | Output: EnrichedContent schema

Also contains the image toolkit classes and credential helper.
Returns None if no image API keys are configured.
"""

import base64
import json
import os

import httpx
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import Toolkit
from agno.utils.log import logger

from .schemas import EnrichedContent


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


def build_image_agent() -> Agent | None:
    """Build an image agent if any image API keys are available.
    Returns None if no keys are configured (images will be skipped)."""
    image_tools = []

    freepik_key = os.getenv("FREEPIK_API_KEY")
    if freepik_key:
        image_tools.append(FreepikTools(api_key=freepik_key))

    creds = get_dataforseo_credentials()
    if creds:
        image_tools.append(DataForSEOTools(login=creds[0], password=creds[1]))

    if not image_tools:
        return None

    return Agent(
        name="Image Agent",
        model=Claude(id="claude-sonnet-4-5-20250929"),
        tools=image_tools,
        output_schema=EnrichedContent,
        instructions=[
            "You are an image search and content enrichment specialist.",
            "Given a Markdown article, search for relevant high-quality images for 3-5 key sections.",
            "Insert Markdown image syntax (![alt text](url)) into the article at the appropriate "
            "positions -- directly after the relevant section heading.",
            "Return the full enriched Markdown and the list of images you inserted.",
            "For each image, include the section heading, search query used, image URL, "
            "SEO-friendly alt text, and source (freepik or dataforseo).",
            "If no suitable images are found, return the article unchanged with an empty images list.",
        ],
    )


image_agent = build_image_agent()
