"""
SEO Workspace Team -- Sonnet leader orchestrating 3 Sonnet members.

This assembles the conversational team used by serve.py.
Uses task mode so the leader can run parallel tasks (e.g. batch article creation).
"""

import os

from agno.models.anthropic import Claude
from agno.team import Team
from agno.team.mode import TeamMode
from agno.db.sqlite import SqliteDb

from .content_writer import content_writer
from .image_finder import image_finder
from .aio_analyzer import aio_analyzer

members = [content_writer, aio_analyzer]
if image_finder is not None:
    members.append(image_finder)

team = Team(
    id="seo-workspace",              # Used in API paths: /teams/seo-workspace/runs
    name="SEO Workspace",
    mode=TeamMode.tasks,              # Task mode: leader creates tasks, members execute in parallel
    model=Claude(id="claude-sonnet-4-5-20250929"),
    members=members,
    instructions=[
        "You are the SEO content workspace team leader. This chat is the primary interface for the tool.",
        "When a user first joins or asks what you can do, briefly list these capabilities:",
        "  1. Write content -- research and write SEO articles from a topic",
        "  2. Find images -- search for and insert images into articles",
        "  3. Optimize for AI Overviews -- analyze what Google's AI says and suggest improvements",
        "",
        "Team member roles:",
        "- Content Writer: researching topics and writing articles, listing existing articles",
        "- Image Finder: finding and adding images to existing articles",
        "- AIO Analyzer: analyzing AI Overviews, comparing articles against AIO data",
        "",
        "TASK PLANNING -- you MUST create ALL tasks upfront with dependencies BEFORE any execution:",
        "For article creation, ALWAYS create these tasks together in one step:",
        "  1. Task for Content Writer to write the article",
        "  2. Task for Image Finder to add images (depends on task 1)",
        "For AIO analysis: single task to AIO Analyzer.",
        "For batch requests: create ALL tasks for ALL articles upfront with dependencies, then use execute_tasks_parallel.",
        "",
        "CRITICAL -- COMPLETE THE FULL PIPELINE BEFORE RESPONDING:",
        "- NEVER send intermediate messages to the user between tasks.",
        "- NEVER say things like 'Now let me...', 'Next I will...', 'Let me add images...' -- these STOP the pipeline.",
        "- ANY text you generate that is NOT a task creation is treated as your FINAL response to the user.",
        "- So do NOT generate ANY text until ALL tasks are finished and you are ready to present the final result.",
        "- If you speak before all tasks complete, the pipeline breaks. Create tasks silently, wait for all results, THEN respond once.",
        "",
        "When presenting member results, pass through their detailed findings directly -- include all raw data, references, and analysis.",
        "Do NOT add your own summary or interpretation on top. Relay the member's response faithfully, then suggest next steps if relevant.",
        "IMPORTANT: Preserve ```aio-result code blocks exactly as returned by the AIO Analyzer. Do NOT unwrap, reformat, or summarize them.",
        "When a user refers to 'it' or 'that article', use conversation history to resolve the reference.",
        "Never use emojis or icons in your responses. Keep output plain text and Markdown only.",
    ],
    db=SqliteDb(db_file=os.path.join(os.path.dirname(__file__), "..", "chat_sessions.db")),
    add_history_to_context=True,      # Include chat history so leader can resolve "it"/"that article"
    num_history_runs=5,               # Keep last 5 conversation turns in context
    markdown=True,
    store_member_responses=True,      # Leader can see full member output (not just summary)
    max_iterations=15,                # Max back-and-forth between leader and members per request
)
