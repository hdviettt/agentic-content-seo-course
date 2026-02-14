"""
Pydantic models -- shared data contracts between agents.

These models serve two purposes:
1. Structured output schemas -- when passed to an Agno agent via output_schema,
   the LLM returns validated JSON matching our exact structure.
2. Data transfer objects -- passed between pipeline steps as typed objects.
"""

from pydantic import BaseModel, Field


# ============================================================
# Content Pipeline -- used by outline, writer, and image agents
# ============================================================


class OutlineSection(BaseModel):
    """A single section in the article outline (maps to an H2)."""
    heading: str = Field(..., description="Section heading (H2)")
    subheadings: list[str] = Field(
        default_factory=list, description="Sub-section headings (H3)"
    )
    key_points: list[str] = Field(
        ..., description="Bullet points to cover in this section"
    )
    seo_keywords: list[str] = Field(
        default_factory=list, description="Target keywords for this section"
    )


class ContentOutline(BaseModel):
    """Full article outline -- the output_schema for the Research & Outline agent."""
    title: str = Field(..., description="SEO-optimized article title")
    meta_description: str = Field(
        ..., description="Meta description, max 160 chars"
    )
    target_keywords: list[str] = Field(
        ..., description="Primary SEO keywords for the article"
    )
    sections: list[OutlineSection] = Field(
        ..., description="Ordered list of content sections"
    )
    tone: str = Field(default="informative", description="Writing tone")


class ImageSuggestion(BaseModel):
    """Metadata for a single image found and inserted into the article."""
    section_heading: str = Field(
        ..., description="Which section this image belongs to"
    )
    search_query: str = Field(..., description="Query used to find the image")
    image_url: str = Field(..., description="URL of the image found")
    alt_text: str = Field(..., description="SEO-friendly alt text")
    source: str = Field(
        ..., description="'freepik' or 'dataforseo' or 'none'"
    )


class EnrichedContent(BaseModel):
    """Final article with images -- the output_schema for the Image Enrichment agent."""
    markdown_content: str = Field(
        ..., description="Full article in Markdown with images inserted"
    )
    images: list[ImageSuggestion] = Field(
        default_factory=list, description="Images that were inserted"
    )
