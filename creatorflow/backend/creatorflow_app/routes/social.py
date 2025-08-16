from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..social import PROVIDERS


social_bp = Blueprint("social", __name__)


@social_bp.post("/publish")
@jwt_required()
def publish():
	data = request.get_json(force=True)
	platform = data["platform"]
	credentials = data.get("credentials", {})
	payload = data.get("payload", {})
	provider = PROVIDERS.get(platform)
	if not provider:
		return jsonify({"error": "unsupported platform"}), 400
	res = provider.publish(credentials, payload)
	return jsonify(res)