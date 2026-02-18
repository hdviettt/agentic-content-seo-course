"""
Status Tracker -- chat team member for querying articles.

Checks article status, details, content, and version history.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude

from tools.workspace import (
    list_all_articles,
    get_article_details,
    get_article_content,
    get_version_history,
)

status_tracker = Agent(
    name="Status Tracker",
    role="Query article status, details, content, and version history.",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=[list_all_articles, get_article_details, get_article_content, get_version_history],
    instructions=[
        "You help users check on their articles and content.",
        "Use list_all_articles to show all articles or filter by status.",
        "Use get_article_details for specific article info.",
        "Use get_article_content to retrieve the full Markdown text of an article.",
        "Use get_version_history to show how an article has changed over time.",
        "Format results in a clear, readable way.",
        "Article IDs are Airtable record IDs (strings like 'recABC123').",
    ],
    markdown=True,
)
