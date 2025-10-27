"""
Claude-powered summarizer for newsletter content
"""
import os
from typing import Dict, List
import anthropic

class ClaudeSummarizer:
    """Use Claude AI to generate better summaries"""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.client = None
        
        if self.api_key and self.api_key != "your_api_key_here":
            try:
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"⚠️  Could not initialize Claude: {e}")
                self.client = None
        else:
            print("ℹ️  Claude API key not found. Using basic summaries.")
    
    def summarize(self, title: str, url: str, source: str, content: str = "") -> str:
        """Generate an AI-powered summary using Claude"""
        
        if not self.client:
            return ""
        
        try:
            prompt = f"""Please provide a concise 2-sentence summary of this article for a newsletter about founding engineers and startup technical teams:

Title: {title}
Source: {source}
URL: {url}

Provide just the summary without any additional commentary."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=200,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            summary = message.content[0].text if message.content else ""
            return summary.strip()
            
        except Exception as e:
            print(f"⚠️  Claude summarization failed: {e}")
            return ""
    
    def enhance_item(self, item: Dict) -> Dict:
        """Add an enhanced summary to an item"""
        if self.client and item.get("url"):
            enhanced_summary = self.summarize(
                title=item.get("title", ""),
                url=item.get("url", ""),
                source=item.get("source", ""),
                content=item.get("summary", "")
            )
            if enhanced_summary:
                item["ai_summary"] = enhanced_summary
                item["summary"] = enhanced_summary  # Replace with AI summary
        return item
