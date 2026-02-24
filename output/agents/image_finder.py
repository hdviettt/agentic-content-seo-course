"""
Image Finder -- finds and inserts images into articles (optional).

Model: Claude Sonnet | Tools: DataForSEO Images + Airtable | Output: plain text

Returns None if no DataForSEO API key is configured.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude

from tools.aio import get_dataforseo_credentials
from tools.images import DataForSEOImageTools
from tools.airtable import get_article_content, update_article_content


def build_image_finder() -> Agent | None:
    """Build the image finder agent if DataForSEO credentials are available.
    Returns None if not configured (images will be skipped)."""
    creds = get_dataforseo_credentials()
    if not creds:
        return None

    return Agent(
        name="Image Finder",
        role="Find and insert images into articles",
        model=Claude(id="claude-sonnet-4-5-20250929"),
        tools=[DataForSEOImageTools(creds[0], creds[1]), get_article_content, update_article_content],
        instructions=[
            "You find relevant images and insert them into articles.",
            "Use get_article_content to read the article.",
            "Search for 3-5 relevant images for the article's sections.",
            "Insert images as ![alt text](url) after relevant ## headings.",
            "Use update_article_content to save the updated article.",
            "Do not change the article text -- only add image lines.",
            "Never use emojis or icons.",
        ],
        markdown=True,
    )


image_finder = build_image_finder()
