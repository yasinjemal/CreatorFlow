from __future__ import annotations
from typing import Dict, List

TRENDING_TOPICS: Dict[str, List[str]] = {
    "instagram": ["behind the scenes", "day in the life", "creator tips"],
    "tiktok": ["capcut templates", "ai filters", "before and after"],
    "youtube": ["how to", "top 10", "react"],
    "linkedin": ["ai in business", "leadership", "remote work"],
    "twitter": ["productivity", "launch", "buildinpublic"],
    "facebook": ["local events", "community", "family"],
    "pinterest": ["home office", "meal prep", "minimalism"],
}


def trending_topics(platform: str) -> List[str]:
    return TRENDING_TOPICS.get(platform, ["creator economy", "content strategy"])[:10]
