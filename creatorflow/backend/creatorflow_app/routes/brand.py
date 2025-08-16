from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import mongo_client
from ..utils.db import to_object_id


brand_bp = Blueprint("brand", __name__)


@brand_bp.post("")
@jwt_required()
def create_brand():
	data = request.get_json(force=True)
	db = mongo_client.get_db()
	user_id = get_jwt_identity()
	data["owner_user_id"] = user_id
	res = db.brands.insert_one(data)
	return jsonify({"id": str(res.inserted_id)})


@brand_bp.get("")
@jwt_required()
def list_brands():
	db = mongo_client.get_db()
	user_id = get_jwt_identity()
	items = list(db.brands.find({"owner_user_id": user_id}))
	for it in items:
		it["id"] = str(it.pop("_id"))
	return jsonify(items)


@brand_bp.get("/<brand_id>")
@jwt_required()
def get_brand(brand_id: str):
	db = mongo_client.get_db()
	b = db.brands.find_one({"_id": to_object_id(brand_id)})
	if not b:
		return jsonify({"error": "not found"}), 404
	b["id"] = str(b.pop("_id"))
	return jsonify(b)


@brand_bp.post("/<brand_id>/train")
@jwt_required()
def train_brand_voice(brand_id: str):
	# Placeholder for fine-tuning or vectorization of brand content samples
	return jsonify({"status": "queued"})