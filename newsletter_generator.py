"""
Newsletter generation and formatting
"""
import json
from datetime import datetime
from typing import List, Dict
import config


class NewsletterGenerator:
    """Generate newsletters from curated content"""
    
    def __init__(self):
        self.date = datetime.now().strftime("%B %d, %Y")
        self.week_ending = datetime.now().strftime("%B %d, %Y")
    
    def generate_markdown(self, items: List[Dict]) -> str:
        """Generate a Markdown newsletter"""
        md = f"# {config.NEWSLETTER_TITLE}\n\n"
        md += f"**Week of {self.date}**\n\n"
        md += "---\n\n"
        md += f"*Curated content about founding engineers, startup engineering culture, and early-stage technical team building.*\n\n"
        md += "## This Week's Highlights\n\n"
        
        for idx, item in enumerate(items, 1):
            md += f"### {idx}. {item['title']}\n\n"
            md += f"**Source:** {item['source']}\n\n"
            
            if item.get('author'):
                md += f"**Author:** {item['author']}\n\n"
            
            # Show keywords matched
            if item.get('keywords_matched'):
                md += f"*Keywords: {', '.join(item['keywords_matched'][:3])}*\n\n"
            
            # Add summary if available
            if item.get('summary'):
                summary = item['summary'][:200]
                md += f"{summary}...\n\n"
            
            md += f"🔗 [Read More]({item['url']})\n\n"
            md += "---\n\n"
        
        md += f"\n\n*Generated automatically on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return md
    
    def generate_html(self, items: List[Dict]) -> str:
        """Generate an HTML newsletter"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{config.NEWSLETTER_TITLE}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #666; margin-top: 30px; }}
        h3 {{ color: #444; margin-top: 25px; }}
        .meta {{ color: #888; font-size: 0.9em; }}
        .keyword {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.85em; }}
        a {{ color: #4CAF50; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .summary {{ background: #f9f9f9; padding: 10px; border-left: 3px solid #4CAF50; margin: 10px 0; }}
        .date {{ color: #666; font-style: italic; }}
        hr {{ border: none; border-top: 1px solid #eee; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>{config.NEWSLETTER_TITLE}</h1>
    <p class="date"><strong>Week of {self.date}</strong></p>
    <p><em>Curated content about founding engineers, startup engineering culture, and early-stage technical team building.</em></p>
    
    <h2>This Week's Highlights</h2>
"""
        
        for idx, item in enumerate(items, 1):
            html += f"""
    <div style="margin-bottom: 40px;">
        <h3>{idx}. {item['title']}</h3>
        <p class="meta">
            <strong>Source:</strong> {item['source']}
"""
            
            if item.get('author'):
                html += f"<br><strong>Author:</strong> {item['author']}"
            
            html += "</p>"
            
            # Keywords
            if item.get('keywords_matched'):
                keywords_html = ' '.join([f'<span class="keyword">{kw}</span>' for kw in item['keywords_matched'][:3]])
                html += f"<p>{keywords_html}</p>"
            
            # Summary
            if item.get('summary'):
                summary = item['summary'][:300]
                html += f'<div class="summary"><p>{summary}...</p></div>'
            
            html += f'<p><a href="{item["url"]}">🔗 Read More</a></p>'
            html += "</div>"
        
        html += f"""
    <hr>
    <p class="date"><em>Generated automatically on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
</body>
</html>
"""
        
        return html
    
    def save_newsletter(self, items: List[Dict], clustered_items: Dict[str, List[Dict]] = None):
        """Save newsletter in multiple formats"""
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        
        # Save markdown
        md_content = self.generate_markdown(items)
        md_path = os.path.join(config.OUTPUT_DIR, config.NEWSLETTER_MD_FILE)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✅ Saved newsletter to {md_path}")
        
        # Save HTML
        html_content = self.generate_html(items)
        html_path = os.path.join(config.OUTPUT_DIR, config.NEWSLETTER_HTML_FILE)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Saved newsletter to {html_path}")
        
        # Save clustered version if available
        if clustered_items:
            clustered_md = self._generate_clustered_markdown(clustered_items)
            clustered_path = os.path.join(config.OUTPUT_DIR, "newsletter_clustered.md")
            with open(clustered_path, 'w', encoding='utf-8') as f:
                f.write(clustered_md)
            print(f"✅ Saved clustered newsletter to {clustered_path}")
    
    def _generate_clustered_markdown(self, clustered_items: Dict[str, List[Dict]]) -> str:
        """Generate a theme-clustered version of the newsletter"""
        md = f"# {config.NEWSLETTER_TITLE}\n\n"
        md += f"**Week of {self.date}**\n\n"
        md += "---\n\n"
        md += "*Organized by theme*\n\n"
        
        for theme, items in clustered_items.items():
            if items:
                md += f"## {theme}\n\n"
                for idx, item in enumerate(items, 1):
                    md += f"### {item['title']}\n\n"
                    md += f"**Source:** {item['source']}\n\n"
                    if item.get('author'):
                        md += f"**Author:** {item['author']}\n\n"
                    if item.get('summary'):
                        md += f"{item['summary'][:200]}...\n\n"
                    md += f"🔗 [Read More]({item['url']})\n\n"
                    md += "---\n\n"
        
        md += f"\n\n*Generated automatically on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return md
    
    def save_raw_data(self, all_items: List[Dict]):
        """Save raw scraped data to JSON"""
        import os
        
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        
        # Convert datetime objects to strings for JSON serialization
        json_items = []
        for item in all_items:
            json_item = item.copy()
            if "created_at" in json_item and hasattr(json_item["created_at"], 'isoformat'):
                json_item["created_at"] = json_item["created_at"].isoformat()
            if "published" in json_item and hasattr(json_item["published"], 'isoformat'):
                json_item["published"] = json_item["published"].isoformat()
            json_items.append(json_item)
        
        raw_path = os.path.join(config.OUTPUT_DIR, config.RAW_DATA_FILE)
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(json_items, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved raw data to {raw_path}")
        print(f"   Found {len(json_items)} total items")
