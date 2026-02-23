"""
AIO Analyst -- chat team member for Google AI Overview analysis.

Analyzes what Google's AI says about topics and helps optimize content
to be cited in AI Overviews.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude

from tools.workspace import (
    analyze_keyword_aio,
    get_aio_history,
    optimize_for_aio,
)

aio_analyst = Agent(
    name="AIO Analyst",
    role="Analyze Google AI Overviews and optimize content for AIO citations.",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=[analyze_keyword_aio, get_aio_history, optimize_for_aio],
    instructions=[
        "You analyze Google AI Overviews for keywords.",
        "Use analyze_keyword_aio to check what Google's AI says about a topic.",
        "Use get_aio_history to see past analyses for an article's keywords.",
        "Use optimize_for_aio to compare an article against current AI Overviews and suggest improvements.",
        "AIO analysis requires DataForSEO to be configured.",
    ],
    markdown=True,
)
