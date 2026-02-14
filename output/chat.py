"""
Conversational SEO workspace -- natural-language interface via an Agno Team.

The team leader (Opus) delegates requests to specialized member agents
(Sonnet), each equipped with a focused subset of workspace tools.

Usage:
    python chat.py
    python cli.py chat
"""

from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team import Team
from agno.db.sqlite import SqliteDb

from db import init_db
from workspace_tools import (
    create_article,
    create_article_batch,
    list_all_articles,
    get_article_details,
    get_article_content,
    get_version_history,
)

# Ensure the workspace database exists
init_db()

# ============================================================
# Team Members -- each with a focused role and tool subset
# ============================================================

content_creator = Agent(
    name="Content Creator",
    role="Create new SEO articles and batch article generation.",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=[create_article, create_article_batch],
    instructions=[
        "You create SEO articles using the workspace tools.",
        "When asked to create an article, use the create_article tool with the topic and optional keywords.",
        "When asked to create multiple articles, use create_article_batch with a JSON array of topics.",
        "Report back the article ID, word count, and output file when done.",
        "Article creation takes time -- let the user know you're working on it.",
    ],
    markdown=True,
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
    ],
    markdown=True,
)

# ============================================================
# Team Leader -- orchestrates the members
# ============================================================

team = Team(
    name="SEO Workspace",
    model=Claude(id="claude-opus-4-6"),
    members=[content_creator, status_tracker],
    instructions=[
        "You are the SEO content workspace team leader.",
        "Delegate requests to the appropriate team member based on their role:",
        "- Content Creator: creating new articles (single or batch)",
        "- Status Tracker: checking article status, details, content, or version history",
        "Synthesize member responses into clear, conversational replies.",
        "When a user refers to 'it' or 'that article', use conversation history to resolve the reference.",
    ],
    db=SqliteDb(db_file="chat_sessions.db"),
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
    store_member_responses=True,
)


def main():
    team.cli_app(stream=True, markdown=True)


if __name__ == "__main__":
    main()
