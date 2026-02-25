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
        "",
        "PART 1 - RAW AIO DATA: Output a fenced code block with language 'aio-result' containing valid JSON.",
        "The JSON object MUST have these fields:",
        '  - "keyword": the keyword analyzed (string)',
        '  - "has_aio": whether an AI Overview exists (boolean)',
        '  - "content": the full AI Overview text, verbatim as returned by the tool (string, empty if no AIO)',
        '  - "references": array of objects with "title", "url", "source" fields (empty array if none)',
        "",
        "Example:",
        "```aio-result",
        '{"keyword":"hidden gem netflix movies","has_aio":true,"content":"The exact AIO text here...","references":[{"title":"Source Title","url":"https://example.com","source":"example.com"}]}',
        "```",
        "",
        "CRITICAL: The JSON must be valid and the code block language must be exactly 'aio-result'.",
        "Do NOT paraphrase or summarize the AIO content -- copy it exactly as returned by the tool.",
        "",
        "PART 2 - ANALYSIS: After the aio-result block, write your interpretation under a '## Analysis' heading.",
        "Include: content gaps, key themes Google highlights, cited source patterns, and actionable suggestions.",
        "Be specific about what to add, change, or emphasize.",
        "",
        "Never use emojis or icons in your responses.",
    ],
    markdown=True,
)
