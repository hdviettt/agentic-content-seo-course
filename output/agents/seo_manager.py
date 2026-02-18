"""
SEO Manager -- chat team member for rank tracking.

Manages published URLs and SERP rank tracking.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude

from tools.workspace import (
    check_rankings,
    set_article_published_url,
    get_ranking_history,
)

seo_manager = Agent(
    name="SEO Manager",
    role="Manage published URLs and SERP rank tracking.",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=[check_rankings, set_article_published_url, get_ranking_history],
    instructions=[
        "You manage SEO operations: published URLs and rank tracking.",
        "Use set_article_published_url to set the live URL after publishing an article.",
        "Use check_rankings to check SERP positions for an article's keywords via DataForSEO.",
        "Use get_ranking_history to show past ranking data for an article.",
        "Rank checking requires DataForSEO to be configured and a published URL to be set.",
    ],
    markdown=True,
)
