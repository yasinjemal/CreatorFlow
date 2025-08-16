from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import mongo_client


analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.get("/overview")
@jwt_required()
def overview():
	db = mongo_client.get_db()
	content_count = db.content.count_documents({}) if "content" in db.list_collection_names() else 0
	brand_count = db.brands.count_documents({}) if "brands" in db.list_collection_names() else 0
	return jsonify({
		"content_count": content_count,
		"brand_count": brand_count,
		"engagement_pred": 0.0,
	})


@analytics_bp.get("/content/<content_id>")
@jwt_required()
def content_metrics(content_id: str):
	# Placeholder: would pull metrics by platform
	return jsonify({"content_id": content_id, "metrics": {"views": 0, "likes": 0, "comments": 0}})