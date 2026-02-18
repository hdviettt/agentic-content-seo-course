"""
Content Creator -- chat team member for article creation.

Creates single articles, batch generation, retry failed articles, and CSV import.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude

from tools.workspace import (
    create_article,
    create_article_batch,
    retry_article,
    load_articles_from_csv,
)

content_creator = Agent(
    name="Content Creator",
    role="Create new SEO articles, batch generation, retry failed articles, and CSV import.",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=[create_article, create_article_batch, retry_article, load_articles_from_csv],
    instructions=[
        "You create SEO articles using the workspace tools.",
        "When asked to create an article, use the create_article tool with the topic and optional keywords.",
        "When asked to create multiple articles, use create_article_batch with a JSON array of topics.",
        "For batch creation with many topics, set parallel=True for faster processing.",
        "When asked to retry a failed article, use retry_article with the article ID.",
        "When asked to load topics from a CSV file, use load_articles_from_csv with the file path.",
        "Report back the article ID, word count, and output file when done.",
        "Article creation takes time -- let the user know you're working on it.",
    ],
    markdown=True,
)
