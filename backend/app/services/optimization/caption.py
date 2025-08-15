from __future__ import annotations
from typing import Dict
from .hashtag import suggest_hashtags
from ..ai.gpt_client import GPTClient

PLATFORM_LIMITS: Dict[str, int] = {
    "instagram": 2200,
    "tiktok": 2200,
    "youtube": 5000,
    "linkedin": 3000,
    "twitter": 280,
    "facebook": 63206,
    "pinterest": 500,
}

PLATFORM_STYLE_HINTS: Dict[str, str] = {
    "instagram": "hook + value + CTA, line breaks, emojis OK",
    "tiktok": "short, punchy, challenge or question, emojis OK",
    "youtube": "value-driven, include keywords for SEO",
    "linkedin": "professional, structured with whitespace, no fluff",
    "twitter": "concise, 1 idea, avoid filler, add 1-2 hashtags",
    "facebook": "conversational, community-oriented",
    "pinterest": "descriptive, keyword-rich",
}


def generate_caption(topic: str, platform: str, brand_voice: str, cta: str) -> Dict[str, object]:
    ai = GPTClient(api_key=None)
    hint = PLATFORM_STYLE_HINTS.get(platform, "platform-optimized")
    limit = PLATFORM_LIMITS.get(platform, 2200)
    prompt = (
        f"You are a {brand_voice} social media strategist.\n"
        f"Platform: {platform}. Style: {hint}. Max length: {limit} chars.\n"
        f"Topic: {topic}. CTA: {cta}.\n"
        f"Write a caption tailored to the platform. Keep within the max length."
    )
    caption = ai.generate_text(prompt)
    caption = caption[:limit]
    hashtags = suggest_hashtags(topic, platform)
    return {"caption": caption, "hashtags": hashtags, "limit": limit}
