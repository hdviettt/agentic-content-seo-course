"""
Outline Agent -- takes research notes, produces a structured outline.

Model: Claude Sonnet | Tools: none | Output: ContentOutline schema
"""

from agno.agent import Agent
from agno.models.anthropic import Claude

from .schemas import ContentOutline

outline_agent = Agent(
    name="Outline Agent",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    output_schema=ContentOutline,
    instructions=[
        "You are an expert content strategist.",
        "Given research notes about a topic, create a structured content outline.",
        "Include 5-8 sections with clear H2 headings, optional H3 subheadings, "
        "key points, and relevant SEO keywords per section.",
        "The title should be SEO-optimized and compelling.",
        "The meta description must be under 160 characters.",
    ],
)
