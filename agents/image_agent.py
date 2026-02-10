import os

from agno.agent import Agent
from agno.models.xai import xAI

from schemas import EnrichedContent
from tools.freepik_tools import FreepikTools
from tools.dataforseo_tools import DataForSEOTools


def build_image_search_agent() -> Agent | None:
    """Build an image search agent if any image API keys are available.
    Returns None if no keys are configured."""
    image_tools = []

    freepik_key = os.getenv("FREEPIK_API_KEY")
    if freepik_key:
        image_tools.append(FreepikTools(api_key=freepik_key))

    dataforseo_login = os.getenv("DATAFORSEO_LOGIN")
    dataforseo_password = os.getenv("DATAFORSEO_PASSWORD")
    if dataforseo_login and dataforseo_password:
        image_tools.append(
            DataForSEOTools(login=dataforseo_login, password=dataforseo_password)
        )

    if not image_tools:
        return None

    return Agent(
        name="Image Searcher",
        model=xAI(id="grok-4-fast"),
        tools=image_tools,
        instructions=[
            "You are an image search specialist.",
            "Given article section headings, search for relevant high-quality images for 3-5 key sections.",
            "For each image found, output the section heading, the search query you used, the image URL, and a suggested SEO-friendly alt text.",
            "Format your output clearly so it can be parsed downstream.",
        ],
        markdown=True,
    )


# Assembler agent — no tools, structured output only.
# Grok does not support combining tools with json_schema, so this is separate.
image_assembler_agent = Agent(
    name="Image Assembler",
    model=xAI(id="grok-4"),
    output_schema=EnrichedContent,
    instructions=[
        "You are an image enrichment assembler for SEO content.",
        "You receive a Markdown article and image search results.",
        "Insert Markdown image syntax (![alt text](url)) into the article at the appropriate positions — directly after the relevant section heading.",
        "Return the full enriched Markdown and the list of images you inserted.",
        "If no image results are provided, return the article unchanged with an empty images list.",
    ],
)

image_search_agent = build_image_search_agent()
