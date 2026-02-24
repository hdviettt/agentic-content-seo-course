"""
Conversational SEO workspace -- natural-language interface via an Agno Team.

The team leader (Sonnet) delegates requests to specialized member agents
(Sonnet), each equipped with a focused subset of workspace tools.

Usage:
    python output/chat.py     (from project root)
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()


def validate_api_keys():
    """Check that required API keys are set. Exit with a friendly message if not."""
    if not os.getenv("ANTHROPIC_API_KEY", "").strip():
        print("Missing required API key: ANTHROPIC_API_KEY\n")
        print("Add it to your .env file.")
        print("Get your key at: https://console.anthropic.com")
        sys.exit(1)


def main():
    validate_api_keys()

    from agents.team import team
    team.cli_app(stream=True, markdown=True)


if __name__ == "__main__":
    main()
