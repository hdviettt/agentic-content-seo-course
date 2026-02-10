from agno.agent import Agent
from agno.models.xai import xAI

writer_agent = Agent(
    name="Content Writer",
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
        "Do NOT output anything other than the article Markdown itself — no preamble or explanation.",
    ],
    markdown=True,
)
