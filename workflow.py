import os
from datetime import datetime

from agno.workflow import Workflow, Step
from agno.workflow.step import StepInput, StepOutput

from agents.outline_agent import research_agent, outline_agent
from agents.writer_agent import writer_agent
from agents.image_agent import image_search_agent, image_assembler_agent


def run_outline(step_input: StepInput) -> StepOutput:
    """Step 1: Research the topic, then generate a structured outline."""
    research_response = research_agent.run(step_input.input)

    prompt = (
        f"Create a detailed SEO content outline for the topic: {step_input.input}\n\n"
        f"Use this research:\n\n{research_response.content}"
    )
    outline_response = outline_agent.run(prompt)

    outline = outline_response.content
    if hasattr(outline, "model_dump_json"):
        return StepOutput(content=outline.model_dump_json(indent=2))
    return StepOutput(content=str(outline))


def run_writer(step_input: StepInput) -> StepOutput:
    """Step 2: Write the full article from the outline."""
    prompt = f"Write a full SEO article based on this outline:\n\n{step_input.previous_step_content}"
    response = writer_agent.run(prompt)
    return StepOutput(content=response.content)


def run_images(step_input: StepInput) -> StepOutput:
    """Step 3: Enrich the article with images, then auto-export to output/."""
    article_markdown = step_input.previous_step_content

    image_results = ""
    if image_search_agent is not None:
        search_response = image_search_agent.run(
            f"Find relevant images for these article sections:\n\n{article_markdown}"
        )
        image_results = search_response.content

    prompt = (
        f"Here is the article:\n\n{article_markdown}\n\n"
        f"Here are the image search results:\n\n{image_results if image_results else 'No images available.'}"
    )
    response = image_assembler_agent.run(prompt)

    enriched = response.content
    final = enriched.markdown_content if hasattr(enriched, "markdown_content") else str(enriched)

    # Auto-export
    os.makedirs("output", exist_ok=True)
    topic = str(step_input.input or "article").lower().replace(" ", "-")[:50]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"output/{topic}-{timestamp}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final)
    print(f"\nExported to {filename}")

    return StepOutput(content=final)


workflow = Workflow(
    name="SEO Content Pipeline",
    steps=[
        Step(executor=run_outline, name="outline"),
        Step(executor=run_writer, name="write"),
        Step(executor=run_images, name="enrich"),
    ],
)
