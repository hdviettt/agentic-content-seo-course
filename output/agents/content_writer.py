"""
Content Writer -- researches topics and writes SEO articles.

Model: Claude Sonnet | Tools: DuckDuckGo + Airtable | Output: plain text
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools

from tools.airtable import save_article, list_all_articles

content_writer = Agent(
    name="Content Writer",
    role="Research topics and write SEO articles",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=[DuckDuckGoTools(), save_article, list_all_articles],
    instructions=[
        "You research topics and write comprehensive SEO articles.",
        "Use web search to research the topic thoroughly before writing.",
        "Write a well-structured Markdown article with:",
        "  - An H1 title",
        "  - 5-8 H2 section headings",
        "  - H3 subheadings where appropriate",
        "  - Bolded important keywords naturally within the text",
        "  - Bullet/numbered lists where helpful",
        "  - A compelling introduction and conclusion",
        "  - 1500-2500 words of engaging content",
        "After writing, call save_article with the topic, full article text, and target keywords.",
        "When asked to list articles, use list_all_articles.",
        "Never use emojis or icons.",
    ],
    markdown=True,
)
