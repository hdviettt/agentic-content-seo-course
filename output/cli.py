"""
CLI entry point -- all workspace commands in one place.

Usage:  python cli.py <command> [options]
Run:    python cli.py --help

Architecture: Each command is a thin handler that validates input,
calls the appropriate pipeline function, and formats output.
Heavy logic lives in pipeline.py, not here.
"""

import argparse
import json

from dotenv import load_dotenv

load_dotenv()

from db import (
    init_db,
    create_article,
    get_article,
    list_articles,
    get_article_versions,
)


# ============================================================
# Command Handlers -- one function per CLI command
# ============================================================


def cmd_create(args):
    """Create a single article and run the full generation pipeline."""
    keywords = None
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]

    article_id = create_article(args.topic, target_keywords=keywords)
    print(f"Article #{article_id} created: \"{args.topic}\"\n")

    # Lazy import -- only load agents when actually generating content.
    # This keeps commands like `status` instant (no model loading).
    from pipeline import run_content_pipeline

    run_content_pipeline(article_id, args.topic)


def cmd_create_batch(args):
    """Queue multiple topics and process them all sequentially."""
    from pipeline import run_batch, load_topics_from_csv

    if args.file:
        topics = load_topics_from_csv(args.file)
    elif args.topics:
        topics = [{"topic": t} for t in args.topics]
    else:
        print("Provide topics as arguments or use --file topics.csv")
        return

    run_batch(topics)


def cmd_status(args):
    """Show the article status table, or details for a single article."""
    if args.article:
        article = get_article(args.article)
        if not article:
            print(f"Article {args.article} not found.")
            return
        _print_article_detail(article)
        return

    articles = list_articles(status=args.filter, batch_id=args.batch)
    if not articles:
        print("No articles found.")
        return

    _print_articles_table(articles)


def cmd_history(args):
    """Show the version history for an article (v1, v2, v3...)."""
    article = get_article(args.article_id)
    if not article:
        print(f"Article {args.article_id} not found.")
        return

    versions = get_article_versions(article["id"])
    if not versions:
        print(f"No versions found for Article #{article['id']}.")
        return

    print(f"Article {article['id']} -- Version History\n")
    print(f"{'Ver':<5} | {'Date':<20} | {'Summary':<40} | Words")
    print(f"{'-' * 5}-|-{'-' * 20}-|-{'-' * 40}-|{'-' * 7}")
    for v in versions:
        wc = len(v["article_markdown"].split()) if v["article_markdown"] else 0
        summary = (v["change_summary"] or "")[:40]
        print(f"v{v['version_number']:<4} | {v['created_at']:<20} | {summary:<40} | {wc:,}")


def cmd_chat(args):
    """Launch the interactive conversational workspace."""
    from chat import main as chat_main
    chat_main()


# ============================================================
# Display Helpers
# ============================================================


def _print_articles_table(articles):
    """Print a formatted table of all articles."""
    print(f"{'ID':>4} | {'Topic':<40} | {'Status':<12} | {'Words':>7} | Updated")
    print(f"{'-' * 4}-|-{'-' * 40}-|-{'-' * 12}-|-{'-' * 7}-|{'-' * 20}")
    for a in articles:
        topic = (a["topic"][:38] + "..") if len(a["topic"]) > 40 else a["topic"]
        words = f"{a['word_count']:,}" if a["word_count"] else "-"
        updated = a["updated_at"] or a["created_at"]
        print(f"{a['id']:>4} | {topic:<40} | {a['status']:<12} | {words:>7} | {updated}")


def _print_article_detail(article):
    """Print detailed info for a single article."""
    print(f"Article #{article['id']}")
    print(f"  Topic:    {article['topic']}")
    print(f"  Status:   {article['status']}")
    print(f"  Words:    {article['word_count'] or '-'}")
    if article.get("target_keywords"):
        kw = json.loads(article["target_keywords"]) if isinstance(article["target_keywords"], str) else article["target_keywords"]
        print(f"  Keywords: {', '.join(kw)}")
    if article.get("output_file"):
        print(f"  File:     {article['output_file']}")
    if article.get("batch_id"):
        print(f"  Batch:    {article['batch_id']}")
    if article.get("error_message"):
        print(f"  Error:    {article['error_message']}")
    print(f"  Created:  {article['created_at']}")
    print(f"  Updated:  {article['updated_at']}")


# ============================================================
# Argument Parser -- maps CLI commands to handler functions
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="Agentic Content SEO Workspace",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Content Creation ---

    p = subparsers.add_parser("create", help="Generate a single SEO article")
    p.add_argument("topic", help="Article topic")
    p.add_argument("--keywords", help="Comma-separated target keywords")
    p.set_defaults(func=cmd_create)

    p = subparsers.add_parser("create-batch", help="Generate articles in batch")
    p.add_argument("topics", nargs="*", help="Topics as arguments")
    p.add_argument("--file", help="CSV file with topics (columns: topic, keywords)")
    p.set_defaults(func=cmd_create_batch)

    # --- Status ---

    p = subparsers.add_parser("status", help="View article status")
    p.add_argument("--article", type=int, help="Show details for a specific article")
    p.add_argument("--filter", help="Filter by status (queued, review, etc.)")
    p.add_argument("--batch", help="Filter by batch ID")
    p.set_defaults(func=cmd_status)

    # --- History ---

    p = subparsers.add_parser("history", help="View article version history")
    p.add_argument("article_id", type=int, help="Article ID")
    p.set_defaults(func=cmd_history)

    # --- Chat ---

    p = subparsers.add_parser("chat", help="Interactive conversational workspace")
    p.set_defaults(func=cmd_chat)

    # --- Run ---

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
