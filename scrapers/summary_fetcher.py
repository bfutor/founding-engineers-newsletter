"""
Best-effort summaries for items that arrive without one (e.g. Hacker News links)
"""
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

USER_AGENT = "FoundingEngineersNewsletter/1.0 (+https://github.com/bfutor/founding-engineers-newsletter)"


def fetch_description(url: str, timeout: int = 8) -> str:
    """Return the page's meta description, or an empty string"""
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        if "html" not in response.headers.get("content-type", ""):
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        for attrs in ({"property": "og:description"}, {"name": "description"}):
            tag = soup.find("meta", attrs=attrs)
            if tag and tag.get("content"):
                return ' '.join(tag["content"].split())
    except Exception:
        pass

    return ""


def fill_missing_summaries(items: List[Dict]) -> List[Dict]:
    """Populate summaries for items that have none"""
    for item in items:
        if not item.get("summary") and item.get("url"):
            item["summary"] = fetch_description(item["url"])
    return items
