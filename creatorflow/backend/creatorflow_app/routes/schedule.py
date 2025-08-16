from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import mongo_client
from datetime import datetime


schedule_bp = Blueprint("schedule", __name__)


@schedule_bp.post("")
@jwt_required()
def create_schedule():
	data = request.get_json(force=True)
	db = mongo_client.get_db()
	item = {
		"content_id": data["content_id"],
		"brand_id": data["brand_id"],
		"platforms": data.get("platforms", []),
		"post_at": datetime.fromisoformat(data["post_at"].replace("Z", "+00:00")),
		"status": "SCHEDULED",
	}
	res = db.schedules.insert_one(item)
	return jsonify({"id": str(res.inserted_id)})


@schedule_bp.get("")
@jwt_required()
def list_schedules():
	db = mongo_client.get_db()
	items = list(db.schedules.find().sort("post_at", 1))
	for it in items:
		it["id"] = str(it.pop("_id"))
		it["post_at"] = it["post_at"].isoformat() + "Z"
	return jsonify(items)