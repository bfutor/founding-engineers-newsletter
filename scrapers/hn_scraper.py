"""
Hacker News scraper using Algolia API
"""
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import config
from .keywords import matched_keywords


class HackerNewsScraper:
    """Scrape Hacker News using the Algolia search API"""

    def __init__(self):
        self.api_url = config.SOURCES["hacker_news"]["api_url"]
        self.search_url = config.SOURCES["hacker_news"]["search_url"]
        self.min_date = (datetime.now() - timedelta(days=config.DAYS_TO_COLLECT)).timestamp()

    def _build_item(self, hit: Dict, keywords: List[str]) -> Dict:
        return {
            "title": hit.get("title", ""),
            "url": hit.get("url", ""),
            "author": hit.get("author", ""),
            "points": hit.get("points", 0),
            "num_comments": hit.get("num_comments", 0),
            "created_at": datetime.fromtimestamp(hit.get("created_at_i", 0)),
            "source": "Hacker News",
            "keywords_matched": keywords,
        }

    def search(self, query: str = None) -> List[Dict]:
        """Search HN for relevant posts from the last N days"""
        all_results = []

        keywords_to_search = [query] if query else config.KEYWORDS

        for keyword in keywords_to_search:
            params = {
                "query": keyword,
                "tags": "story",
                "numericFilters": f"created_at_i>={int(self.min_date)}",
                "hitsPerPage": 50,
            }

            try:
                response = requests.get(self.search_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                for hit in data.get("hits", []):
                    text = f"{hit.get('title', '')} {hit.get('story_text', '') or ''}"
                    # Algolia is typo tolerant, so confirm the keyword really appears
                    keywords = matched_keywords(text)
                    if not keywords:
                        continue

                    item = self._build_item(hit, keywords)

                    # Skip if no URL (self-posts often have no URL)
                    if item["url"]:
                        all_results.append(item)

            except Exception as e:
                print(f"Error fetching from Hacker News for keyword '{keyword}': {e}")
                continue

        return all_results

    def get_trending(self) -> List[Dict]:
        """Get popular recent posts from HN that match our keywords"""
        params = {
            "tags": "story",
            "numericFilters": f"created_at_i>={int(self.min_date)},points>=20",
            "hitsPerPage": 100,
        }

        try:
            response = requests.get(self.search_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for hit in data.get("hits", []):
                keywords = matched_keywords(hit.get("title", ""))
                if not keywords:
                    continue

                item = self._build_item(hit, keywords)
                if item["url"]:
                    results.append(item)

            return results

        except Exception as e:
            print(f"Error fetching trending from HN: {e}")
            return []
