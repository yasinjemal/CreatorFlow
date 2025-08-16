from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import mongo_client
from ..services.ai import ContentGenerator
from ..services.hashtags import HashtagService
from ..services.optimization import OptimizationService
from ..utils.db import to_object_id


content_bp = Blueprint("content", __name__)

generator = ContentGenerator()
hashtags_service = HashtagService(generator)
optimizer = OptimizationService()


@content_bp.post("/generate/caption")
@jwt_required()
def generate_caption():
	data = request.get_json(force=True)
	platform = data["platform"]
	topic = data.get("topic", "")
	brand_id = data["brand_id"]
	db = mongo_client.get_db()
	brand = db.brands.find_one({"_id": to_object_id(brand_id)})
	if not brand:
		return jsonify({"error": "brand not found"}), 404
	cap = generator.generate_caption(platform, topic, brand)
	cap = optimizer.adapt_caption(platform, cap)
	return jsonify({"caption": cap})


@content_bp.post("/generate/hashtags")
@jwt_required()
def generate_hashtags():
	data = request.get_json(force=True)
	platform = data["platform"]
	topic = data.get("topic", "")
	brand_id = data["brand_id"]
	count = int(data.get("count", 10))
	db = mongo_client.get_db()
	brand = db.brands.find_one({"_id": to_object_id(brand_id)})
	if not brand:
		return jsonify({"error": "brand not found"}), 404
	tags = hashtags_service.suggest(platform, topic, brand, count)
	return jsonify({"hashtags": tags})


@content_bp.post("/generate/script")
@jwt_required()
def generate_script():
	data = request.get_json(force=True)
	platform = data["platform"]
	topic = data.get("topic", "")
	duration = int(data.get("duration_seconds", 30))
	brand_id = data["brand_id"]
	db = mongo_client.get_db()
	brand = db.brands.find_one({"_id": to_object_id(brand_id)})
	if not brand:
		return jsonify({"error": "brand not found"}), 404
	script = generator.generate_script(platform, topic, duration, brand)
	return jsonify({"script": script})


@content_bp.post("/optimize/post-time")
@jwt_required()
def optimize_post_time():
	data = request.get_json(force=True)
	platform = data["platform"]
	rec = optimizer.recommend_post_time(platform)
	return jsonify({"recommended_post_time": rec.isoformat() + "Z"})