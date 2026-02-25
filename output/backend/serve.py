"""
SEO Workspace — FastAPI backend via Agno AgentOS.

Serves the team at 50+ auto-generated endpoints (chat, sessions, health, docs)
plus custom routes for the article storage layer.

Usage:
    python output/backend/serve.py     (from project root)
"""

import json
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

load_dotenv()


def validate_api_keys():
    if not os.getenv("ANTHROPIC_API_KEY", "").strip():
        print("Missing required API key: ANTHROPIC_API_KEY")
        print("Add it to your .env file.")
        sys.exit(1)


validate_api_keys()

from agno.os import AgentOS
from agents.team import team
from tools.storage import get_article, list_articles, _load_metadata, _md_path, _lock, _save_metadata

# Custom FastAPI app with article routes
base_app = FastAPI(title="SEO Workspace", version="1.0.0")

base_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@base_app.get("/api/articles")
async def api_list_articles():
    """List all articles with metadata (no content)."""
    articles = list_articles()
    return [
        {
            "id": a["id"],
            "topic": a["topic"],
            "status": a["status"],
            "word_count": a["word_count"],
            "created_at": a["created_at"],
            "updated_at": a["updated_at"],
        }
        for a in articles
    ]


@base_app.get("/api/articles/{article_id}")
async def api_get_article(article_id: str):
    """Get a single article with full content."""
    article = get_article(article_id)
    if not article:
        return {"error": f"Article {article_id} not found."}
    return article


@base_app.delete("/api/articles/{article_id}")
async def api_delete_article(article_id: str):
    """Delete an article (metadata + .md file)."""
    with _lock:
        metadata = _load_metadata()
        if article_id not in metadata:
            return {"error": f"Article {article_id} not found."}
        del metadata[article_id]
        _save_metadata(metadata)

    md_file = _md_path(article_id)
    if os.path.exists(md_file):
        os.remove(md_file)

    return {"deleted": article_id}


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@base_app.post("/api/chat/stream")
async def api_chat_stream(req: ChatRequest):
    """Send a message to the team and stream the response via SSE.

    TeamMode.tasks does not support native SSE streaming, so we call
    team.arun() (non-streaming) and wrap the result in SSE events that
    the frontend can parse with the same ReadableStream logic.
    """

    async def generate():
        # Signal that we've started
        yield f"event: TeamRunStarted\ndata: {json.dumps({'event': 'TeamRunStarted'})}\n\n"

        try:
            response = await team.arun(req.message, session_id=req.session_id)

            # Extract the response content
            content = ""
            if hasattr(response, "messages") and response.messages:
                for msg in response.messages:
                    if getattr(msg, "role", None) == "assistant" and getattr(msg, "content", None):
                        content = msg.content
                        break
            if not content:
                content = response.content or ""

            # Send content as a single chunk
            yield f"event: TeamRunContent\ndata: {json.dumps({'event': 'TeamRunContent', 'content': content})}\n\n"

            # Signal completion
            yield f"event: TeamRunCompleted\ndata: {json.dumps({'event': 'TeamRunCompleted', 'content': content})}\n\n"

        except Exception as e:
            yield f"event: TeamRunError\ndata: {json.dumps({'event': 'TeamRunError', 'content': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# Wrap with AgentOS
agent_os = AgentOS(
    teams=[team],
    base_app=base_app,
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="serve:app", port=7777, reload=True)
