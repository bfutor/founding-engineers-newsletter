"""
RSS Feed scraper for various sources
"""
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import config
from .keywords import matched_keywords


class RSSScraper:
    """Scrape RSS feeds from various sources"""
    
    USER_AGENT = "FoundingEngineersNewsletter/1.0 (+https://github.com/bfutor/founding-engineers-newsletter)"

    def __init__(self):
        self.cutoff_date = datetime.now() - timedelta(days=config.DAYS_TO_COLLECT)

    def _fetch(self, feed_url: str):
        """Fetch a feed with a real User-Agent and parse it"""
        response = requests.get(feed_url, timeout=15, headers={"User-Agent": self.USER_AGENT})
        response.raise_for_status()
        return feedparser.parse(response.content)

    @staticmethod
    def _plain_text(html: str) -> str:
        """Strip markup and collapse whitespace in feed content"""
        if not html:
            return ""
        return ' '.join(BeautifulSoup(html, "html.parser").get_text(" ").split())

    def parse_feed(self, feed_url: str, source_name: str = None) -> List[Dict]:
        """Parse an RSS feed and return relevant items"""
        results = []
        
        try:
            feed = self._fetch(feed_url)

            if not feed.entries:
                print(f"RSS parsing error for {feed_url}: {getattr(feed, 'bozo_exception', 'no entries')}")
                return results

            for entry in feed.entries:
                # Parse date
                pub_date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else self.cutoff_date
                
                if pub_date < self.cutoff_date:
                    continue
                
                # Combine title and content for keyword matching
                parts = []
                if hasattr(entry, 'summary'):
                    parts.append(entry.summary)
                if hasattr(entry, 'content'):
                    parts.extend(c.value for c in entry.content)
                content_text = ' '.join(parts)
                
                full_text = f"{entry.title} {content_text}".lower()
                
                matched = matched_keywords(full_text)

                if matched:
                    item = {
                        "title": entry.title,
                        "url": entry.link,
                        "author": entry.get("author", ""),
                        "published": pub_date,
                        "source": source_name or feed_url,
                        "keywords_matched": matched,
                        "summary": self._plain_text(getattr(entry, 'summary', '') or content_text)
                    }
                    results.append(item)
                    
        except Exception as e:
            print(f"Error parsing feed {feed_url}: {e}")
            
        return results
    
    def scrape_all_feeds(self) -> List[Dict]:
        """Scrape all configured RSS feeds"""
        all_results = []
        
        # TechCrunch
        if config.SOURCES["techcrunch"]["enabled"]:
            print("Scraping TechCrunch...")
            results = self.parse_feed(
                config.SOURCES["techcrunch"]["rss_url"],
                "TechCrunch"
            )
            all_results.extend(results)
        
        # Substack
        if config.SOURCES["substack"]["enabled"]:
            print("Scraping Substack sources...")
            for feed_url in config.SOURCES["substack"]["sources"]:
                results = self.parse_feed(feed_url, "Substack")
                all_results.extend(results)
        
        # Medium
        if config.SOURCES["medium"]["enabled"] and "rss_urls" in config.SOURCES["medium"]:
            print("Scraping Medium...")
            for feed_url in config.SOURCES["medium"]["rss_urls"]:
                results = self.parse_feed(feed_url, "Medium")
                all_results.extend(results)
        
        return all_results
