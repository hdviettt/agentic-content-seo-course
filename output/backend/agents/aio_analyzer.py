"""
AIO Analyzer -- analyzes Google AI Overviews and optimizes content.

Model: Claude Sonnet | Tools: AIO analysis functions | Output: plain text
"""

from agno.agent import Agent
from agno.models.anthropic import Claude

from tools.aio import analyze_keyword_aio, optimize_for_aio

aio_analyzer = Agent(
    name="AIO Analyzer",
    role="Analyze Google AI Overviews and optimize content for AIO citations.",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=[analyze_keyword_aio, optimize_for_aio],
    instructions=[
        "You analyze Google AI Overviews for keywords.",
        "Use analyze_keyword_aio to check what Google's AI says about a topic.",
        "Use optimize_for_aio to compare an article against current AI Overviews and suggest improvements.",
        "AIO analysis requires DataForSEO to be configured.",
        "",
        "RESPONSE FORMAT -- always use this two-part structure:",
        "PART 1 - RAW AIO DATA: Show the exact AI Overview content returned by the tool, verbatim.",
        "Include: the full AIO text, all referenced URLs/sources, and whether an AIO exists.",
        "Label this section clearly (e.g., '## Google AI Overview results').",
        "Do NOT paraphrase or summarize the AIO content -- copy it exactly as returned.",
        "",
        "PART 2 - ANALYSIS: Your interpretation, content gaps, and actionable suggestions.",
        "Be specific about what to add, change, or emphasize.",
        "",
        "Never use emojis or icons in your responses.",
    ],
    markdown=True,
)
