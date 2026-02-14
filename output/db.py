"""
Database layer -- SQLite connection, schema, and CRUD functions.

Creates a local workspace.db file on first import. All tables use
TEXT dates via SQLite's datetime() function since SQLite has no
native datetime type.

Why SQLite? It's built into Python (no install), stores everything
in a single file, and handles our sequential workload perfectly.
"""

import json
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "workspace.db")


def get_connection():
    """Open a connection to the workspace database.

    row_factory = sqlite3.Row lets us access columns by name (row["topic"])
    instead of by index (row[1]), making our code much more readable.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't already exist.

    Called automatically on import so the database is always ready.
    CREATE TABLE IF NOT EXISTS is idempotent -- safe to call every time.
    """
    conn = get_connection()
    conn.executescript("""

        -- Core article tracking. Status flows:
        -- queued -> researching -> outlining -> writing -> enriching -> review
        -- Any step can also -> error (with error_message set)
        CREATE TABLE IF NOT EXISTS articles (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            topic             TEXT NOT NULL,
            target_keywords   TEXT,                              -- JSON array of strings
            status            TEXT DEFAULT 'queued',
            outline_json      TEXT,                              -- structured outline from LLM
            article_markdown  TEXT,                              -- latest article content
            output_file       TEXT,                              -- path to exported .md file
            word_count        INTEGER,
            meta_description  TEXT,
            batch_id          TEXT,                              -- groups batch-created articles
            created_at        TEXT DEFAULT (datetime('now')),
            updated_at        TEXT DEFAULT (datetime('now')),
            error_message     TEXT
        );

        -- Every time article content changes, we snapshot it here.
        -- This gives us a full history: initial generation, each optimization, etc.
        CREATE TABLE IF NOT EXISTS article_versions (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id        INTEGER REFERENCES articles(id),
            version_number    INTEGER DEFAULT 1,
            article_markdown  TEXT NOT NULL,
            change_summary    TEXT,                              -- human-readable: "Initial generation"
            created_at        TEXT DEFAULT (datetime('now'))
        );

    """)
    conn.commit()
    conn.close()


# Auto-initialize on import -- the database is always ready to use
init_db()


# ============================================================
# Articles
# ============================================================


def create_article(topic, target_keywords=None, batch_id=None):
    """Insert a new article in 'queued' status. Returns the new article ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO articles (topic, target_keywords, batch_id) VALUES (?, ?, ?)",
        (topic, json.dumps(target_keywords) if target_keywords else None, batch_id),
    )
    conn.commit()
    article_id = cursor.lastrowid
    conn.close()
    return article_id


def update_article_status(article_id, status, **fields):
    """Update an article's status and any additional fields.

    The **fields pattern lets callers pass any column as a keyword arg:
        update_article_status(1, "writing", article_markdown="...", word_count=2000)

    This avoids needing a separate function for every field combination.
    """
    conn = get_connection()

    # Always update status and timestamp; append any extra fields
    sets = ["status = ?", "updated_at = datetime('now')"]
    values = [status]
    for key, value in fields.items():
        sets.append(f"{key} = ?")
        values.append(value)

    values.append(article_id)
    conn.execute(
        f"UPDATE articles SET {', '.join(sets)} WHERE id = ?",
        values,
    )
    conn.commit()
    conn.close()


def get_article(article_id):
    """Fetch a single article by ID. Returns dict or None."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_articles(status=None, batch_id=None):
    """List articles, optionally filtered by status and/or batch_id."""
    conn = get_connection()
    query = "SELECT * FROM articles"
    conditions = []
    values = []

    if status:
        conditions.append("status = ?")
        values.append(status)
    if batch_id:
        conditions.append("batch_id = ?")
        values.append(batch_id)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id"
    rows = conn.execute(query, values).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ============================================================
# Article Versions
# ============================================================


def save_article_version(article_id, markdown, change_summary):
    """Snapshot the current article content as a new version.

    Version numbers auto-increment per article: v1, v2, v3...
    The COALESCE handles the first version (when MAX returns NULL).
    """
    conn = get_connection()

    # Find the next version number for this article
    row = conn.execute(
        "SELECT COALESCE(MAX(version_number), 0) + 1 FROM article_versions WHERE article_id = ?",
        (article_id,),
    ).fetchone()
    version_number = row[0]

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO article_versions (article_id, version_number, article_markdown, change_summary) VALUES (?, ?, ?, ?)",
        (article_id, version_number, markdown, change_summary),
    )
    conn.commit()
    version_id = cursor.lastrowid
    conn.close()
    return version_id


def get_article_versions(article_id):
    """Get all versions of an article, ordered oldest-first."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM article_versions WHERE article_id = ? ORDER BY version_number",
        (article_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
