from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify
from ..extensions import mongo_client


def require_roles(required: list[str]):
	def decorator(fn):
		@wraps(fn)
		@jwt_required()
		def wrapper(*args, **kwargs):
			user_id = get_jwt_identity()
			db = mongo_client.get_db()
			user = db.users.find_one({"_id": __import__('bson').ObjectId(user_id)})
			roles = set(user.get("roles", [])) if user else set()
			if not roles.intersection(set(required)):
				return jsonify({"error": "forbidden"}), 403
			return fn(*args, **kwargs)
		return wrapper
	return decorator