"""
Content filtering, deduplication, and ranking
"""
from typing import List, Dict
from datetime import datetime
import hashlib
import config


class ContentFilter:
    """Filter, deduplicate, and rank content items"""
    
    def __init__(self):
        self.seen_urls = set()
        self.seen_titles = set()
    
    def _generate_hash(self, item: Dict) -> str:
        """Generate a unique hash for an item"""
        # Use URL + title for uniqueness
        key = f"{item.get('url', '')}{item.get('title', '')}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def deduplicate(self, items: List[Dict]) -> List[Dict]:
        """Remove duplicate items"""
        seen_hashes = set()
        unique_items = []
        
        for item in items:
            item_hash = self._generate_hash(item)
            
            if item_hash not in seen_hashes:
                seen_hashes.add(item_hash)
                unique_items.append(item)
        
        return unique_items
    
    def _calculate_score(self, item: Dict) -> float:
        """Calculate relevance score for an item"""
        score = 0.0
        
        # Base score from keywords matched
        keyword_count = len(item.get("keywords_matched", []))
        score += keyword_count * 10
        
        # Boost popular HN posts
        if item.get("source") == "Hacker News":
            score += item.get("points", 0) * 0.5
            score += item.get("num_comments", 0) * 0.2
        
        # Boost by recency (items from today get bonus)
        if "created_at" in item:
            days_old = (datetime.now() - item["created_at"]).days
            score += max(0, (7 - days_old) * 2)
        elif "published" in item:
            days_old = (datetime.now() - item["published"]).days
            score += max(0, (7 - days_old) * 2)
        
        return score
    
    def rank_and_filter(self, items: List[Dict]) -> List[Dict]:
        """Rank items by relevance and return top N"""
        # Deduplicate first
        unique_items = self.deduplicate(items)
        
        # Calculate scores
        for item in unique_items:
            item["score"] = self._calculate_score(item)
        
        # Sort by score (descending)
        sorted_items = sorted(unique_items, key=lambda x: x.get("score", 0), reverse=True)
        
        # Return top N items
        top_items = sorted_items[:config.MAX_ITEMS]
        
        # Apply minimum requirements
        if len(top_items) < config.MIN_ITEMS:
            # If we don't have enough, return what we have
            return top_items
        
        return top_items
    
    def cluster_by_theme(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        """Group items by theme/topic"""
        themes = {theme: [] for theme in config.THEMES}
        
        for item in items:
            title_lower = item.get("title", "").lower()
            content_lower = f"{title_lower} {item.get('summary', '').lower()}"
            
            # Assign to appropriate theme(s)
            assigned = False
            
            if any(kw in content_lower for kw in ["culture", "culture", "team", "collaboration", "values"]):
                themes["Engineering Culture"].append(item)
                assigned = True
            
            if any(kw in content_lower for kw in ["hire", "recruit", "interview", "team building", "onboarding"]):
                themes["Hiring & Team Building"].append(item)
                assigned = True
            
            if any(kw in content_lower for kw in ["stack", "architecture", "tech", "infrastructure", "system design"]):
                themes["Tech Stack & Architecture"].append(item)
                assigned = True
            
            if any(kw in content_lower for kw in ["founder", "co-founder", "startup", "early stage"]):
                themes["Founding Stories"].append(item)
                assigned = True
            
            if any(kw in content_lower for kw in ["lead", "management", "manager", "leadership"]):
                themes["Leadership & Management"].append(item)
                assigned = True
            
            if any(kw in content_lower for kw in ["product", "feature", "development", "build"]):
                themes["Product Development"].append(item)
                assigned = True
            
            if any(kw in content_lower for kw in ["scale", "scaling", "growth", "performance"]):
                themes["Scaling Challenges"].append(item)
                assigned = True
            
            # If no theme matched, add to "Founding Stories" as default
            if not assigned:
                themes["Founding Stories"].append(item)
        
        # Remove empty themes
        return {k: v for k, v in themes.items() if v}
