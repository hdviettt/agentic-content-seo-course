from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.duckduckgo import DuckDuckGoTools

from schemas import ContentOutline

# Phase 1: Research agent — uses web search tools, returns free-form text.
# Grok does not support combining tools with json_schema response format,
# so research and structured outline generation are split into two agents.
research_agent = Agent(
    name="Topic Researcher",
    model=xAI(id="grok-4-fast"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "You are an expert SEO researcher.",
        "Research the given topic using web search.",
        "Analyze what top-ranking content covers for this topic.",
        "Identify primary and secondary target keywords.",
        "Summarize your findings: key themes, common headings used by competitors, target keywords, and content gaps.",
        "Be thorough — your research will be used to build a content outline.",
    ],
    markdown=True,
)

# Phase 2: Outline agent — no tools, structured output only.
outline_agent = Agent(
    name="Outline Designer",
    model=xAI(id="grok-4"),
    output_schema=ContentOutline,
    instructions=[
        "You are an expert SEO content strategist.",
        "Based on the research provided, produce a structured content outline.",
        "Include 5-8 sections with clear H2 headings, optional H3 subheadings, key points to cover, and relevant SEO keywords per section.",
        "The title should be SEO-optimized and compelling.",
        "The meta description must be under 160 characters.",
        "Focus on search intent and comprehensive topic coverage.",
    ],
)
