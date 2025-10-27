"""
Configuration file for the Founding Engineers Newsletter Agent
"""
import os
from datetime import timedelta

# Time window for content (last N days)
DAYS_TO_COLLECT = 7

# Keywords to search for
KEYWORDS = [
    "founding engineer",
    "founding engineers",
    "early engineer",
    "startup engineering",
    "engineering co-founder",
    "tech co-founder",
    "first engineer hire",
    "startup tech team",
    "early-stage engineering",
    "engineering leadership",
    "startup culture",
    "technical founder",
    "CTO",
    "VP Engineering"
]

# Sources to scrape
SOURCES = {
    "hacker_news": {
        "enabled": True,
        "url": "https://news.ycombinator.com",
        "api_url": "https://hn.algolia.com/api/v1/search_by_date"
    },
    "techcrunch": {
        "enabled": True,
        "rss_url": "https://techcrunch.com/feed/"
    },
    "substack": {
        "enabled": True,
        "sources": [
            "https://lethain.com/rss/",
            "https://blog.pragmaticengineer.com/feed"
        ]
    },
    "medium": {
        "enabled": True,
        "rss_urls": [
            "https://medium.com/feed/tag/startup",
            "https://medium.com/feed/tag/engineering"
        ]
    }
}

# OpenAI API configuration (optional, for advanced summarization)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4-turbo-preview"

# Newsletter configuration
NEWSLETTER_TITLE = "Founding Engineers Weekly Digest"
MAX_ITEMS = 10
MIN_ITEMS = 5

# Theme clusters
THEMES = [
    "Engineering Culture",
    "Hiring & Team Building",
    "Tech Stack & Architecture",
    "Founding Stories",
    "Leadership & Management",
    "Product Development",
    "Scaling Challenges"
]

# Output settings
OUTPUT_DIR = "./output"
RAW_DATA_FILE = "raw_sources.json"
NEWSLETTER_MD_FILE = "newsletter.md"
NEWSLETTER_HTML_FILE = "newsletter.html"
