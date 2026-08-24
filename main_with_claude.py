"""
Main orchestrator with Claude AI integration for enhanced summaries
"""
import os
import sys
from datetime import datetime
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Import our modules
import config
from scrapers import HackerNewsScraper, RSSScraper, ContentFilter, fill_missing_summaries
from scrapers.claude_summarizer import ClaudeSummarizer
from newsletter_generator import NewsletterGenerator


def main():
    """Main execution flow with Claude integration"""
    print("🚀 Starting Founding Engineers Newsletter Agent with Claude AI...\n")
    print(f"📅 Collecting content from the last {config.DAYS_TO_COLLECT} days")
    print(f"📝 Keywords: {', '.join(config.KEYWORDS[:5])}...\n")
    
    all_items = []
    
    # Scrape Hacker News
    if config.SOURCES["hacker_news"]["enabled"]:
        print("🔍 Scraping Hacker News...")
        hn_scraper = HackerNewsScraper()
        hn_items = hn_scraper.get_trending() + hn_scraper.search()
        all_items.extend(hn_items)
        print(f"   Found {len(hn_items)} items\n")
    
    # Scrape RSS feeds
    if any([config.SOURCES.get(src, {}).get("enabled", False) for src in ["techcrunch", "substack", "medium"]]):
        print("🔍 Scraping RSS feeds...")
        rss_scraper = RSSScraper()
        rss_items = rss_scraper.scrape_all_feeds()
        all_items.extend(rss_items)
        print(f"   Found {len(rss_items)} items\n")
    
    print(f"📊 Total items collected: {len(all_items)}\n")
    
    if not all_items:
        print("⚠️  No items found. Please check your sources or date range.")
        sys.exit(1)
    
    # Filter and rank content
    print("�� Filtering and ranking content...")
    content_filter = ContentFilter()
    filtered_items = content_filter.rank_and_filter(all_items)
    
    print(f"✅ Selected {len(filtered_items)} items for newsletter\n")
    
    # Enhanced summarization with Claude
    print("🤖 Enhancing summaries with Claude AI...")
    claude = ClaudeSummarizer()
    
    for item in filtered_items:
        claude.enhance_item(item)
    
    print(f"✅ Enhanced summaries generated\n")

    fill_missing_summaries(filtered_items)
    
    # Cluster by theme
    print("📑 Clustering by theme...")
    clustered_items = content_filter.cluster_by_theme(filtered_items)
    
    for theme, items in clustered_items.items():
        print(f"   {theme}: {len(items)} items")
    print()
    
    # Generate newsletter
    print("📧 Generating newsletter...")
    generator = NewsletterGenerator()
    generator.save_newsletter(filtered_items, clustered_items)
    generator.save_raw_data(all_items)
    
    print("\n�� Newsletter generation complete!")
    print(f"📁 Check the {config.OUTPUT_DIR}/ directory for outputs:")
    print(f"   - {config.NEWSLETTER_MD_FILE} (Markdown)")
    print(f"   - {config.NEWSLETTER_HTML_FILE} (HTML)")
    print(f"   - newsletter_clustered.md (Theme-clustered)")
    print(f"   - {config.RAW_DATA_FILE} (Raw data)")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
