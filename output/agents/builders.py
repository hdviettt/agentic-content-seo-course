"""
Pipeline agents -- the AI workers that produce content.

Four agents, each with a single job:
  1. research_agent  -- searches the web, returns research notes
  2. outline_agent   -- takes research, produces a structured outline
  3. writer_agent    -- takes outline, writes the full article
  4. image_agent     -- takes article, finds and inserts images (optional)
"""

import os

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.xai import xAI
from agno.tools.duckduckgo import DuckDuckGoTools

from agents.schemas import ContentOutline, EnrichedContent
from tools import FreepikTools, DataForSEOTools
from tools.dataforseo_tools import get_dataforseo_credentials


# 1. Research Agent -- searches the web, returns plain text research notes
#    Model: Claude Sonnet | Tools: DuckDuckGo | Output: plain text
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


# 2. Outline Agent -- takes research notes, produces a structured outline
#    Model: Claude Sonnet | Tools: none | Output: ContentOutline schema
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


# 3. Writer Agent -- takes an outline, writes the full Markdown article
#    Model: Grok-4 | Tools: none | Output: plain Markdown
writer_agent = Agent(
    name="Writer Agent",
    model=xAI(id="grok-4"),
    instructions=[
        "You are an expert SEO content writer.",
        "Write a comprehensive, SEO-optimized article following the provided outline exactly.",
        "Use proper Markdown formatting: H1 for the title, H2 for section headings, H3 for subheadings.",
        "Bold important keywords naturally within the text.",
        "Use bullet lists and numbered lists where appropriate.",
        "Write in the tone specified by the outline.",
        "Naturally incorporate the target keywords throughout the article without keyword stuffing.",
        "Aim for 1500-2500 words of high-quality, engaging content.",
        "Include a compelling introduction and a strong conclusion with a call to action.",
        "Do NOT output anything other than the article Markdown itself -- no preamble or explanation.",
    ],
    markdown=True,
)


# 4. Image Agent -- takes an article, finds images and inserts them (optional)
#    Model: Claude Sonnet | Tools: image search | Output: EnrichedContent schema
#    Returns None if no image API keys are configured.

def build_image_agent() -> Agent | None:
    """Build an image agent if any image API keys are available.
    Returns None if no keys are configured (images will be skipped)."""
    image_tools = []

    freepik_key = os.getenv("FREEPIK_API_KEY")
    if freepik_key:
        image_tools.append(FreepikTools(api_key=freepik_key))

    creds = get_dataforseo_credentials()
    if creds:
        image_tools.append(DataForSEOTools(login=creds[0], password=creds[1]))

    if not image_tools:
        return None

    return Agent(
        name="Image Agent",
        model=Claude(id="claude-sonnet-4-5-20250929"),
        tools=image_tools,
        output_schema=EnrichedContent,
        instructions=[
            "You are an image search and content enrichment specialist.",
            "Given a Markdown article, search for relevant high-quality images for 3-5 key sections.",
            "Insert Markdown image syntax (![alt text](url)) into the article at the appropriate "
            "positions -- directly after the relevant section heading.",
            "Return the full enriched Markdown and the list of images you inserted.",
            "For each image, include the section heading, search query used, image URL, "
            "SEO-friendly alt text, and source (freepik or dataforseo).",
            "If no suitable images are found, return the article unchanged with an empty images list.",
        ],
    )


image_agent = build_image_agent()
