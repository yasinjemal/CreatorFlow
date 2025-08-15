def suggest_hashtags(topic: str, platform: str) -> list[str]:
    base = topic.lower().replace(" ", "")
    common = ["#content", "#creator", "#trending"]
    platform_tags = {
        "instagram": ["#reels", "#instadaily"],
        "tiktok": ["#fyp", "#tiktok"],
        "youtube": ["#shorts", "#youtube"],
        "linkedin": ["#leadership", "#business"],
        "twitter": ["#X", "#growth"],
        "facebook": ["#facebook", "#community"],
        "pinterest": ["#pinterest", "#inspiration"]
    }
    return [f"#{base}", *platform_tags.get(platform, []), *common][:10]
