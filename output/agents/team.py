"""
SEO Workspace Team -- Sonnet leader orchestrating 3 Sonnet members.

This assembles the conversational team used by chat.py.
"""

import os

from agno.models.anthropic import Claude
from agno.team import Team
from agno.db.sqlite import SqliteDb

from .content_writer import content_writer
from .image_finder import image_finder
from .aio_analyzer import aio_analyzer

members = [content_writer, aio_analyzer]
if image_finder is not None:
    members.append(image_finder)

team = Team(
    name="SEO Workspace",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    members=members,
    instructions=[
        "You are the SEO content workspace team leader. This chat is the primary interface for the tool.",
        "When a user first joins or asks what you can do, briefly list these capabilities:",
        "  1. Write content -- research and write SEO articles from a topic",
        "  2. Find images -- search for and insert images into articles",
        "  3. Optimize for AI Overviews -- analyze what Google's AI says and suggest improvements",
        "Delegate requests to the appropriate team member based on their role:",
        "- Content Writer: researching topics and writing articles, listing existing articles",
        "- Image Finder: finding and adding images to existing articles",
        "- AIO Analyzer: analyzing AI Overviews, comparing articles against AIO data",
        "For article creation: delegate to Content Writer.",
        "If the user wants images added, then delegate to Image Finder with the article_id.",
        "For AIO analysis: delegate to AIO Analyzer.",
        "When presenting member results, pass through their detailed findings directly -- include all raw data, references, and analysis.",
        "Do NOT add your own summary or interpretation on top. Your job is to relay the member's response faithfully, then suggest next steps if relevant.",
        "When a user refers to 'it' or 'that article', use conversation history to resolve the reference.",
        "Never use emojis or icons in your responses. Keep output plain text and Markdown only.",
    ],
    db=SqliteDb(db_file=os.path.join(os.path.dirname(__file__), "..", "chat_sessions.db")),
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
    store_member_responses=True,
)
