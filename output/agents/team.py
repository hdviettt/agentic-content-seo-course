"""
SEO Workspace Team -- Opus leader orchestrating 3 Sonnet members.

This assembles the conversational team used by chat.py.
"""

import os

from agno.models.anthropic import Claude
from agno.team import Team
from agno.db.sqlite import SqliteDb

from .content_creator import content_creator
from .status_tracker import status_tracker
from .aio_analyst import aio_analyst

team = Team(
    name="SEO Workspace",
    model=Claude(id="claude-opus-4-6"),
    members=[content_creator, status_tracker, aio_analyst],
    instructions=[
        "You are the SEO content workspace team leader. This chat is the primary interface for the tool.",
        "When a user first joins or asks what you can do, briefly list these capabilities:",
        "  1. Create articles (single, batch, or from CSV file)",
        "  2. Check article status, details, content, and version history",
        "  3. Retry failed articles",
        "  4. Analyze Google AI Overviews for any keyword",
        "Delegate requests to the appropriate team member based on their role:",
        "- Content Creator: creating articles (single, batch, CSV import), retrying failed articles",
        "- Status Tracker: checking article status, details, content, or version history",
        "- AIO Analyst: analyzing AI Overviews, comparing articles against AIO data",
        "Synthesize member responses into clear, conversational replies.",
        "When a user refers to 'it' or 'that article', use conversation history to resolve the reference.",
        "If an article fails, proactively suggest using retry.",
    ],
    db=SqliteDb(db_file=os.path.join(os.path.dirname(__file__), "..", "chat_sessions.db")),
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
    store_member_responses=True,
)
