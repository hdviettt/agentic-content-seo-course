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


def validate_airtable():
    """Check that Airtable is configured. Exit with setup instructions if not."""
    from tools.airtable import validate

    ok, message = validate()
    if not ok:
        print(f"Airtable not configured: {message}\n")
        print("Airtable is required for article storage. Setup steps:")
        print("  1. Create an account at airtable.com")
        print("  2. Get a Personal Access Token at airtable.com/create/tokens")
        print("  3. Add AIRTABLE_PAT=your_token to .env")
        print("  4. Run: python output/tools/airtable.py")
        print("  5. Add the printed AIRTABLE_BASE_ID to .env")
        sys.exit(1)


def main():
    validate_api_keys()
    validate_airtable()

    from agents.team import team
    team.cli_app(stream=True, markdown=True)


if __name__ == "__main__":
    main()
