"""
RSS Feed scraper for various sources
"""
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import requests
import config


class RSSScraper:
    """Scrape RSS feeds from various sources"""
    
    def __init__(self):
        self.cutoff_date = datetime.now() - timedelta(days=config.DAYS_TO_COLLECT)
        
    def parse_feed(self, feed_url: str, source_name: str = None) -> List[Dict]:
        """Parse an RSS feed and return relevant items"""
        results = []
        
        try:
            feed = feedparser.parse(feed_url)
            
            if feed.bozo and feed.bozo_exception:
                print(f"RSS parsing error for {feed_url}: {feed.bozo_exception}")
                return results
                
            for entry in feed.entries:
                # Parse date
                pub_date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else self.cutoff_date
                
                if pub_date < self.cutoff_date:
                    continue
                
                # Combine title and content for keyword matching
                content_text = ""
                if hasattr(entry, 'summary'):
                    content_text = entry.summary
                elif hasattr(entry, 'content'):
                    content_text = ' '.join([c.value for c in entry.content])
                
                full_text = f"{entry.title} {content_text}".lower()
                
                # Check if keywords match
                matched_keywords = []
                for keyword in config.KEYWORDS:
                    if keyword.lower() in full_text:
                        matched_keywords.append(keyword)
                
                if matched_keywords:
                    item = {
                        "title": entry.title,
                        "url": entry.link,
                        "author": entry.get("author", ""),
                        "published": pub_date,
                        "source": source_name or feed_url,
                        "keywords_matched": matched_keywords,
                        "summary": entry.get("summary", "")
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
