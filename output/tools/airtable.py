"""
Airtable database layer -- CRUD operations for the SEO content workspace.

Replaces SQLite as the primary data store. Article IDs are Airtable record IDs
(strings like "recABC123"). Requires AIRTABLE_PAT and AIRTABLE_BASE_ID in .env.

Setup:
    1. Get a Personal Access Token from airtable.com/create/tokens
    2. Set AIRTABLE_PAT in .env
    3. Run: python output/tools/airtable.py
    4. Add the printed AIRTABLE_BASE_ID to .env
"""

import json
import os
from datetime import datetime, timezone

import httpx
from agno.utils.log import logger


# ============================================================
# Connection helpers
# ============================================================

_api_instance = None


def _get_api():
    """Return a pyairtable Api instance, or None if not configured."""
    global _api_instance
    if _api_instance is not None:
        return _api_instance

    pat = os.getenv("AIRTABLE_PAT", "").strip()
    if not pat:
        return None

    from pyairtable import Api
    _api_instance = Api(pat)
    return _api_instance


def _get_table(table_name):
    """Return a pyairtable Table for the configured base, or None."""
    api = _get_api()
    if api is None:
        return None

    base_id = os.getenv("AIRTABLE_BASE_ID", "").strip()
    if not base_id:
        return None

    return api.table(base_id, table_name)


def _now():
    """Current UTC time in ISO 8601 format for Airtable dateTime fields."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def validate():
    """Check that Airtable env vars are set. Returns (ok, message)."""
    pat = os.getenv("AIRTABLE_PAT", "").strip()
    base_id = os.getenv("AIRTABLE_BASE_ID", "").strip()

    if not pat:
        return False, "AIRTABLE_PAT not set"
    if not base_id:
        return False, "AIRTABLE_BASE_ID not set (run: python output/tools/airtable.py)"
    return True, "Airtable configured"


# ============================================================
# Field mapping
# ============================================================

# Maps db.py-style kwargs to Airtable field names
_FIELD_MAP = {
    "outline_json": "Outline",
    "article_markdown": "Content",
    "output_file": "Output File",
    "word_count": "Word Count",
    "meta_description": "Meta Description",
    "error_message": "Error Message",
}


def _record_to_dict(record):
    """Convert an Airtable record to a flat dict matching the old db.py format."""
    f = record.get("fields", {})

    # Convert comma-separated keywords to JSON string (backward-compatible)
    kw_str = f.get("Target Keywords", "")
    if kw_str:
        kw_list = [k.strip() for k in kw_str.split(",") if k.strip()]
        target_keywords = json.dumps(kw_list)
    else:
        target_keywords = None

    return {
        "id": record["id"],
        "topic": f.get("Topic", ""),
        "target_keywords": target_keywords,
        "status": f.get("Status", "queued"),
        "outline_json": f.get("Outline"),
        "article_markdown": f.get("Content"),
        "output_file": f.get("Output File"),
        "word_count": f.get("Word Count"),
        "meta_description": f.get("Meta Description"),
        "error_message": f.get("Error Message"),
        "created_at": f.get("Created"),
        "updated_at": f.get("Updated"),
    }


# ============================================================
# Articles
# ============================================================


def create_article(topic, target_keywords=None):
    """Insert a new article in 'queued' status. Returns the record ID (string)."""
    table = _get_table("Articles")
    if table is None:
        raise RuntimeError(
            "Airtable not configured. Set AIRTABLE_PAT and AIRTABLE_BASE_ID in .env"
        )

    now = _now()
    fields = {"Topic": topic, "Status": "queued", "Created": now, "Updated": now}

    if target_keywords:
        if isinstance(target_keywords, list):
            fields["Target Keywords"] = ", ".join(target_keywords)
        else:
            fields["Target Keywords"] = str(target_keywords)

    record = table.create(fields)
    return record["id"]


def update_article_status(article_id, status, **fields):
    """Update an article's status and any additional fields.

    The **fields pattern lets callers pass any column as a keyword arg:
        update_article_status("recABC", "writing", article_markdown="...", word_count=2000)
    """
    table = _get_table("Articles")
    if table is None:
        return

    at_fields = {"Status": status, "Updated": _now()}

    for key, value in fields.items():
        at_field = _FIELD_MAP.get(key)
        if at_field:
            if at_field == "Content" and isinstance(value, str):
                at_fields[at_field] = value[:99000]  # Airtable 100k char limit
            else:
                at_fields[at_field] = value

    table.update(article_id, at_fields)


def get_article(article_id):
    """Fetch a single article by ID. Returns dict or None."""
    table = _get_table("Articles")
    if table is None:
        return None

    try:
        record = table.get(article_id)
        return _record_to_dict(record)
    except Exception:
        return None


def list_articles(status=None):
    """List articles, optionally filtered by status."""
    table = _get_table("Articles")
    if table is None:
        return []

    kwargs = {}
    if status:
        kwargs["formula"] = f"{{Status}} = '{status}'"

    records = table.all(**kwargs)
    return [_record_to_dict(r) for r in records]


# ============================================================
# AIO Analyses
# ============================================================


def save_aio_analysis(article_id, keyword, aio_content, references_json,
                      has_aio, location="United States", language="en"):
    """Insert an AIO analysis record. Returns the record ID."""
    table = _get_table("AIO Analyses")
    if table is None:
        return None

    fields = {
        "Keyword": keyword,
        "AIO Content": aio_content or "",
        "References": references_json or "[]",
        "Has AIO": bool(has_aio),
        "Location": location,
        "Language": language,
        "Checked Date": _now(),
        "Article ID": article_id,
    }
    if article_id:
        fields["Articles"] = [article_id]  # Linked record

    record = table.create(fields)
    return record["id"]


def get_aio_analyses(article_id=None, keyword=None):
    """Get AIO analysis records, optionally filtered by article and/or keyword."""
    table = _get_table("AIO Analyses")
    if table is None:
        return []

    formula_parts = []
    if article_id:
        formula_parts.append(f"{{Article ID}} = '{article_id}'")
    if keyword:
        formula_parts.append(f"{{Keyword}} = '{keyword}'")

    kwargs = {}
    if formula_parts:
        if len(formula_parts) == 1:
            kwargs["formula"] = formula_parts[0]
        else:
            kwargs["formula"] = "AND(" + ", ".join(formula_parts) + ")"

    records = table.all(**kwargs)
    records.sort(key=lambda r: r.get("fields", {}).get("Checked Date", ""), reverse=True)

    return [
        {
            "id": r["id"],
            "article_id": r["fields"].get("Article ID", ""),
            "keyword": r["fields"].get("Keyword", ""),
            "aio_content": r["fields"].get("AIO Content", ""),
            "references": r["fields"].get("References", "[]"),
            "has_aio": r["fields"].get("Has AIO", False),
            "location": r["fields"].get("Location", "United States"),
            "language": r["fields"].get("Language", "en"),
            "checked_date": r["fields"].get("Checked Date"),
        }
        for r in records
    ]


# ============================================================
# One-time setup -- creates Airtable tables
# ============================================================

_ARTICLES_FIELDS = [
    {"name": "Topic", "type": "singleLineText"},
    {"name": "Target Keywords", "type": "multilineText"},
    {"name": "Status", "type": "singleSelect", "options": {"choices": [
        {"name": "queued"}, {"name": "researching"},
        {"name": "outlining"}, {"name": "writing"},
        {"name": "enriching"}, {"name": "review"},
        {"name": "error"},
    ]}},
    {"name": "Outline", "type": "multilineText"},
    {"name": "Content", "type": "multilineText"},
    {"name": "Word Count", "type": "number", "options": {"precision": 0}},
    {"name": "Meta Description", "type": "singleLineText"},
    {"name": "Output File", "type": "singleLineText"},
    {"name": "Error Message", "type": "multilineText"},
    {"name": "Created", "type": "dateTime", "options": {
        "dateFormat": {"name": "iso"},
        "timeFormat": {"name": "24hour"},
        "timeZone": "utc",
    }},
    {"name": "Updated", "type": "dateTime", "options": {
        "dateFormat": {"name": "iso"},
        "timeFormat": {"name": "24hour"},
        "timeZone": "utc",
    }},
]

_AIO_ANALYSES_FIELDS = [
    {"name": "Keyword", "type": "singleLineText"},
    {"name": "AIO Content", "type": "multilineText"},
    {"name": "References", "type": "multilineText"},
    {"name": "Has AIO", "type": "checkbox", "options": {"color": "greenBright", "icon": "check"}},
    {"name": "Location", "type": "singleLineText"},
    {"name": "Language", "type": "singleLineText"},
    {"name": "Checked Date", "type": "dateTime", "options": {
        "dateFormat": {"name": "iso"},
        "timeFormat": {"name": "24hour"},
        "timeZone": "utc",
    }},
    {"name": "Article ID", "type": "singleLineText"},
]


def _list_bases(pat):
    """List Airtable bases accessible to this PAT."""
    resp = httpx.get(
        "https://api.airtable.com/v0/meta/bases",
        headers={"Authorization": f"Bearer {pat}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json().get("bases", [])


def setup():
    """One-time setup: create Articles and AIO Analyses tables.

    Run this once, then add the printed AIRTABLE_BASE_ID to your .env file.
    """
    pat = os.getenv("AIRTABLE_PAT", "").strip()
    if not pat:
        print("Error: AIRTABLE_PAT not set in .env")
        print("Get a Personal Access Token at: https://airtable.com/create/tokens")
        return None

    from pyairtable import Api
    api = Api(pat)

    # Step 1: Determine the base to use
    base_id = os.getenv("AIRTABLE_BASE_ID", "").strip()

    if not base_id:
        print("Finding an Airtable base...")
        try:
            bases = _list_bases(pat)
        except Exception as e:
            print(f"Error listing bases: {e}")
            return None

        if not bases:
            print("No bases found. Create a base at airtable.com first, then")
            print("add AIRTABLE_BASE_ID=appXXX to your .env file.")
            return None

        base_id = bases[0]["id"]
        print(f"Using base: {bases[0].get('name', base_id)} ({base_id})")
    else:
        print(f"Using configured base: {base_id}")

    base = api.base(base_id)

    # Step 2: Check existing tables
    print("Checking existing tables...")
    try:
        schema = base.schema()
        existing_tables = {t.name for t in schema.tables}
    except Exception as e:
        print(f"Error reading base schema: {e}")
        return None

    # Step 3: Create tables
    tables_to_create = {
        "Articles": (_ARTICLES_FIELDS, "SEO content articles"),
        "AIO Analyses": (_AIO_ANALYSES_FIELDS, "Google AI Overview analyses"),
    }

    for table_name, (fields, desc) in tables_to_create.items():
        if table_name not in existing_tables:
            print(f"Creating {table_name} table...")
            try:
                base.create_table(table_name, fields, description=desc)
            except Exception as e:
                print(f"Error creating {table_name} table: {e}")
                return None
        else:
            print(f"{table_name} table already exists.")

    # Step 4: Add linked record fields
    print("Adding linked record fields...")
    try:
        schema = base.schema()
        table_ids = {t.name: t.id for t in schema.tables}
        existing_fields = {}
        for t in schema.tables:
            existing_fields[t.name] = {f.name for f in t.fields}

        articles_table = api.table(base_id, table_ids["Articles"])

        # Articles -> AIO Analyses link
        if "AIO Analyses" not in existing_fields.get("Articles", set()):
            articles_table.create_field(
                name="AIO Analyses",
                field_type="multipleRecordLinks",
                options={"linkedTableId": table_ids["AIO Analyses"]},
            )
            print("Added Articles -> AIO Analyses link.")

    except Exception as e:
        print(f"Warning: Could not add linked fields: {e}")
        print("You can add them manually in Airtable if needed.")

    print(f"\nSetup complete! Add this to your .env file:\n")
    print(f"AIRTABLE_BASE_ID={base_id}")
    print()
    return base_id


# ============================================================
# Agent-facing tool functions (return JSON strings)
# ============================================================


def save_article(topic: str, article_markdown: str, keywords: str = "") -> str:
    """Save a new article to Airtable and write the .md file.

    Args:
        topic: The article topic.
        article_markdown: The full article content in Markdown.
        keywords: Optional comma-separated target keywords.

    Returns:
        JSON with article_id, filename, and word_count.
    """
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else None
    article_id = create_article(topic, target_keywords=kw_list)

    # Save to file
    content_dir = os.path.join(os.path.dirname(__file__), "..", "..", "content")
    os.makedirs(content_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filename = os.path.join(content_dir, f"{timestamp}.md")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(article_markdown)

    word_count = len(article_markdown.split())

    update_article_status(
        article_id, "review",
        article_markdown=article_markdown,
        output_file=filename,
        word_count=word_count,
    )

    return json.dumps({
        "article_id": article_id,
        "topic": topic,
        "filename": filename,
        "word_count": word_count,
        "status": "review",
    })


def list_all_articles(status_filter: str = "") -> str:
    """List all articles in the workspace, optionally filtered by status.

    Args:
        status_filter: Filter by status (queued, review, error). Leave empty for all.

    Returns:
        JSON array of article summaries.
    """
    articles = list_articles(status=status_filter or None)
    return json.dumps([
        {
            "id": a["id"],
            "topic": a["topic"],
            "status": a["status"],
            "word_count": a["word_count"],
            "created_at": a["created_at"],
            "updated_at": a["updated_at"],
        }
        for a in articles
    ])


def get_article_content(article_id: str) -> str:
    """Get an article's topic and full Markdown content.

    Args:
        article_id: The Airtable record ID of the article.

    Returns:
        JSON with article_id, topic, and article_markdown.
    """
    article = get_article(article_id)
    if not article:
        return json.dumps({"error": f"Article {article_id} not found."})

    return json.dumps({
        "article_id": article_id,
        "topic": article["topic"],
        "article_markdown": article.get("article_markdown", ""),
    })


def update_article_content(article_id: str, article_markdown: str) -> str:
    """Update an article's Markdown content in Airtable and overwrite the .md file.

    Args:
        article_id: The Airtable record ID of the article.
        article_markdown: The updated article Markdown.

    Returns:
        JSON with article_id and updated word_count.
    """
    article = get_article(article_id)
    if not article:
        return json.dumps({"error": f"Article {article_id} not found."})

    word_count = len(article_markdown.split())

    update_article_status(
        article_id, article["status"],
        article_markdown=article_markdown,
        word_count=word_count,
    )

    # Overwrite the .md file if it exists
    output_file = article.get("output_file")
    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(article_markdown)
        except OSError:
            pass  # File may not exist yet, that's OK

    return json.dumps({
        "article_id": article_id,
        "word_count": word_count,
    })


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    setup()
