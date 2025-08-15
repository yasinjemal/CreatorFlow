from __future__ import annotations
from typing import Dict

PLATFORM_RULES: Dict[str, Dict[str, int]] = {
    "instagram": {"max_hashtags": 30},
    "tiktok": {"max_hashtags": 10},
    "twitter": {"max_hashtags": 2},
    "linkedin": {"max_hashtags": 5},
}


def adapt_caption_for_platform(caption: str, hashtags: list[str], platform: str) -> str:
    rules = PLATFORM_RULES.get(platform, {"max_hashtags": 10})
    max_tags = rules["max_hashtags"]
    tag_str = " ".join(hashtags[:max_tags])
    if tag_str:
        return f"{caption}\n\n{tag_str}"
    return caption
