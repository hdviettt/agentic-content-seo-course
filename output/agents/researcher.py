"""
Research Agent -- searches the web, returns plain text research notes.

Model: Claude Sonnet | Tools: DuckDuckGo | Output: plain text
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools

research_agent = Agent(
    name="Research Agent",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "You are an expert SEO researcher.",
        "Research the given topic using web search.",
        "Identify primary and secondary keywords, analyze what top-ranking content covers, "
        "and find content gaps.",
        "Return your findings as clear, organized research notes.",
    ],
)
