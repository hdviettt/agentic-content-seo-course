"""
Research Agent -- searches the web, returns plain text research notes.

Model: Claude Sonnet | Tools: DuckDuckGo (+ AIOTools if configured) | Output: plain text
"""

import os

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools


def build_research_agent() -> Agent:
    """Build the research agent, optionally adding AIO tools if DataForSEO is configured."""
    tools = [DuckDuckGoTools()]
    extra_instructions = []

    if os.getenv("DATA_FOR_SEO_API_KEY", "").strip():
        from .image import get_dataforseo_credentials
        from tools.aio import AIOTools

        creds = get_dataforseo_credentials()
        if creds:
            tools.append(AIOTools(login=creds[0], password=creds[1]))
            extra_instructions.append(
                "You have AIO tools available. Check what Google's AI Overview says about "
                "the topic and incorporate those insights into your research notes."
            )

    return Agent(
        name="Research Agent",
        model=Claude(id="claude-sonnet-4-5-20250929"),
        tools=tools,
        instructions=[
            "You are an expert SEO researcher.",
            "Research the given topic using web search.",
            "Identify primary and secondary keywords, analyze what top-ranking content covers, "
            "and find content gaps.",
            "Return your findings as clear, organized research notes.",
            *extra_instructions,
        ],
    )


research_agent = build_research_agent()
