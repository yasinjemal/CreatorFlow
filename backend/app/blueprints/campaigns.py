from flask import Blueprint, request, jsonify
from ..db import get_db
from ..utils.auth import require_auth

bp = Blueprint('campaigns', __name__)

@bp.post('/campaign')
@require_auth
def create_campaign():
	data = request.get_json() or {}
	db = get_db()
	camp = {
		"name": data.get("name","Campaign"),
		"budget": data.get("budget",0),
		"spent": 0,
		"revenue": 0,
		"platforms": data.get("platforms", []),
	}
	res = db.campaigns.insert_one(camp)
	return jsonify(id=str(res.inserted_id))

@bp.post('/campaign/roi')
@require_auth
def update_roi():
	data = request.get_json() or {}
	db = get_db()
	db.campaigns.update_one({"_id": data.get("id")}, {"$inc": {"spent": data.get("spent",0), "revenue": data.get("revenue",0)}})
	return jsonify(ok=True)


