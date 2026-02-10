from pydantic import BaseModel, Field


class OutlineSection(BaseModel):
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
    markdown_content: str = Field(
        ..., description="Full article in Markdown with images inserted"
    )
    images: list[ImageSuggestion] = Field(
        default_factory=list, description="Images that were inserted"
    )
