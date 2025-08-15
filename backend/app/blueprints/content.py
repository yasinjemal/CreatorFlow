from flask import Blueprint, request, jsonify
from ..db import get_db
from ..services.optimization.caption import generate_caption
from ..services.optimization.adaptation import adapt_caption_for_platform
from ..services.brand.consistency import analyze_tone
from ..services.optimization.trends import trending_topics
from ..services.optimization.hashtag import suggest_hashtags

bp = Blueprint('content', __name__)

@bp.post("/generate")
def generate():
    data = request.get_json() or {}
    topic = data.get("topic","")
    platform = data.get("platform","instagram")
    brand_voice = data.get("brand_voice","confident, concise")
    call_to_action = data.get("cta","Follow for more!")

    try:
        result = generate_caption(topic, platform, brand_voice, call_to_action)
        adapted = adapt_caption_for_platform(result["caption"], result["hashtags"], platform)
        tone = analyze_tone(adapted, brand_voice)
        return jsonify(platform=platform, caption=adapted, hashtags=result["hashtags"], tone=tone)
    except Exception as e:
        # Fallback when AI provider isn't configured
        caption = f"[Draft]\nPlatform: {platform}\nVoice: {brand_voice}\nTopic: {topic}\nCTA: {call_to_action}"
        tags = suggest_hashtags(topic, platform)
        adapted = adapt_caption_for_platform(caption, tags, platform)
        tone = analyze_tone(adapted, brand_voice)
        return jsonify(platform=platform, caption=adapted, hashtags=tags, tone=tone, fallback=True)

@bp.get("/hashtags")
def hashtags():
    topic = request.args.get("topic", "")
    platform = request.args.get("platform", "instagram")
    from ..services.optimization.hashtag import suggest_hashtags
    tags = suggest_hashtags(topic, platform)
    return jsonify(hashtags=tags)

@bp.get("/trending")
def trending():
    platform = request.args.get("platform", "instagram")
    return jsonify(topics=trending_topics(platform))
