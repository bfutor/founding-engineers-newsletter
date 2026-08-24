"""
Keyword matching helpers
"""
import re
from typing import List

import config

_PATTERNS = {
    keyword: re.compile(r"\b" + re.escape(keyword.lower()).replace(r"\ ", r"[\s\-]+") + r"\b")
    for keyword in config.KEYWORDS
}


def matched_keywords(text: str) -> List[str]:
    """Return the configured keywords that appear in text as whole words"""
    lowered = text.lower()
    return [keyword for keyword, pattern in _PATTERNS.items() if pattern.search(lowered)]
