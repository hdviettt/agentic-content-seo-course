"""
SERP rank tracker -- checks keyword positions via DataForSEO.

Queries the DataForSEO SERP API to find where a URL ranks for given
keywords. Results are saved to Airtable via tools.airtable.

Reuses credentials from agents.get_dataforseo_credentials().
"""

from datetime import date

import httpx
from agno.utils.log import logger

from agents.image import get_dataforseo_credentials


def check_keyword_position(keyword, target_url=None, location="United States"):
    """Check SERP position for a keyword via DataForSEO.

    Args:
        keyword: The search term to check.
        target_url: Optional URL to find in results. If provided, returns
                    the position of that specific URL. Otherwise returns top result.
        location: Search location (default: United States).

    Returns:
        Dict with {keyword, position, url, check_date} or None on failure.
    """
    creds = get_dataforseo_credentials()
    if creds is None:
        logger.warning("DataForSEO not configured -- cannot check rankings")
        return None

    login, password = creds

    try:
        response = httpx.post(
            "https://api.dataforseo.com/v3/serp/google/organic/live/regular",
            auth=(login, password),
            json=[{
                "keyword": keyword,
                "location_name": location,
                "language_code": "en",
                "depth": 100,
            }],
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        tasks = data.get("tasks", [])
        if not tasks or not tasks[0].get("result"):
            return None

        items = tasks[0]["result"][0].get("items", [])

        # If target_url specified, find its position
        if target_url:
            domain = _extract_domain(target_url)
            for item in items:
                item_url = item.get("url", "")
                if domain in item_url or target_url in item_url:
                    return {
                        "keyword": keyword,
                        "position": item.get("rank_absolute"),
                        "url": item_url,
                        "check_date": date.today().isoformat(),
                    }
            # Not found in top 100
            return {
                "keyword": keyword,
                "position": None,
                "url": None,
                "check_date": date.today().isoformat(),
            }

        # No target URL -- return top result
        if items:
            top = items[0]
            return {
                "keyword": keyword,
                "position": top.get("rank_absolute", 1),
                "url": top.get("url", ""),
                "check_date": date.today().isoformat(),
            }

        return None

    except Exception as e:
        logger.warning(f"DataForSEO SERP check failed for '{keyword}': {e}")
        return None


def _extract_domain(url):
    """Extract domain from a URL for fuzzy matching."""
    url = url.replace("https://", "").replace("http://", "")
    return url.split("/")[0].replace("www.", "")


def check_article_rankings(article_id, keywords=None, location="United States"):
    """Check SERP rankings for all keywords of an article.

    Args:
        article_id: The article to check rankings for (Airtable record ID).
        keywords: Optional list of keywords. If not provided, uses the
                  article's target_keywords from the database.
        location: Search location.

    Returns:
        List of ranking result dicts.
    """
    import json
    from tools.airtable import get_article, save_ranking

    article = get_article(article_id)
    if not article:
        return []

    # Determine keywords to check
    if not keywords:
        kw_raw = article.get("target_keywords")
        if kw_raw:
            try:
                keywords = json.loads(kw_raw)
            except (json.JSONDecodeError, TypeError):
                keywords = []
        else:
            keywords = []

    if not keywords:
        return []

    target_url = article.get("published_url")
    results = []

    for kw in keywords:
        result = check_keyword_position(kw, target_url=target_url, location=location)
        if result:
            # Save to Airtable
            ranking_id = save_ranking(
                article_id=article_id,
                keyword=result["keyword"],
                position=result["position"],
                url=result["url"],
                check_date=result["check_date"],
                location=location,
            )
            result["ranking_id"] = ranking_id
            results.append(result)

    return results
