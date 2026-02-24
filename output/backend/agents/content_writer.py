"""
Content Writer -- researches topics and writes SEO articles.

Model: Claude Sonnet | Tools: DataForSEO search + local storage | Output: plain text
"""

from agno.agent import Agent
from agno.models.anthropic import Claude

from tools.aio import get_dataforseo_credentials
from tools.search import DataForSEOSearchTools
from tools.storage import save_article, list_all_articles

_tools = [save_article, list_all_articles]
_creds = get_dataforseo_credentials()
if _creds:
    _tools.insert(0, DataForSEOSearchTools(login=_creds[0], password=_creds[1]))

content_writer = Agent(
    name="Content Writer",
    role="Research topics and write SEO articles",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=_tools,
    instructions=[
        "You research topics and write comprehensive SEO articles.",
        "RESEARCH: Do 1-2 web searches max per article -- one broad search for the main topic, optionally one more for a specific angle. Do NOT over-research.",
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
