"""
Hacker News scraper using Algolia API
"""
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import config


class HackerNewsScraper:
    """Scrape Hacker News using the Algolia search API"""
    
    def __init__(self):
        self.api_url = config.SOURCES["hacker_news"]["api_url"]
        self.min_date = (datetime.now() - timedelta(days=config.DAYS_TO_COLLECT)).timestamp()
        
    def search(self, query: str = None) -> List[Dict]:
        """Search HN for relevant posts from the last N days"""
        all_results = []
        
        # Search for each keyword
        keywords_to_search = [query] if query else config.KEYWORDS
        
        for keyword in keywords_to_search[:3]:  # Limit to avoid rate limits
            params = {
                "query": keyword,
                "tags": "story",
                "numericFilters": f"created_at_i>={int(self.min_date)}"
            }
            
            try:
                response = requests.get(self.api_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                for hit in data.get("hits", []):
                    item = {
                        "title": hit.get("title", ""),
                        "url": hit.get("url", ""),
                        "author": hit.get("author", ""),
                        "points": hit.get("points", 0),
                        "num_comments": hit.get("num_comments", 0),
                        "created_at": datetime.fromtimestamp(hit.get("created_at_i", 0)),
                        "source": "Hacker News",
                        "keywords_matched": [keyword]
                    }
                    
                    # Skip if no URL (self-posts often have no URL)
                    if item["url"]:
                        all_results.append(item)
                        
            except Exception as e:
                print(f"Error fetching from Hacker News for keyword '{keyword}': {e}")
                continue
                
        return all_results
    
    def get_trending(self) -> List[Dict]:
        """Get trending posts from HN (past 24 hours)"""
        params = {
            "tags": "story",
            "numericFilters": f"created_at_i>={int(self.min_date)}",
            "sort": "byPopularity"
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for hit in data.get("hits", [])[:20]:  # Top 20
                # Check if content matches our keywords
                title = hit.get("title", "").lower()
                if any(kw.lower() in title for kw in config.KEYWORDS):
                    item = {
                        "title": hit.get("title", ""),
                        "url": hit.get("url", ""),
                        "author": hit.get("author", ""),
                        "points": hit.get("points", 0),
                        "num_comments": hit.get("num_comments", 0),
                        "created_at": datetime.fromtimestamp(hit.get("created_at_i", 0)),
                        "source": "Hacker News",
                        "keywords_matched": [kw for kw in config.KEYWORDS if kw.lower() in title]
                    }
                    if item["url"]:
                        results.append(item)
                        
            return results
            
        except Exception as e:
            print(f"Error fetching trending from HN: {e}")
            return []
