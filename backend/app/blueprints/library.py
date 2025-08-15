from flask import Blueprint, request, jsonify
from ..db import get_db
from ..utils.auth import require_auth
from bson import ObjectId

bp = Blueprint('library', __name__)

@bp.post('/item')
@require_auth
def create_item():
	data = request.get_json() or {}
	db = get_db()
	item = {
		"user_id": data.get("user_id"),
		"platform": data.get("platform", "instagram"),
		"topic": data.get("topic", ""),
		"caption": data.get("caption", ""),
		"hashtags": data.get("hashtags", []),
		"status": "draft",
		"versions": [
			{"caption": data.get("caption", ""), "created_at": request.date if hasattr(request, 'date') else None}
		],
	}
	res = db.content.insert_one(item)
	return jsonify(id=str(res.inserted_id))

@bp.get('/list')
@require_auth
def list_items():
	user_id = request.args.get("user_id")
	db = get_db()
	items = []
	for it in db.content.find({"user_id": user_id}).sort("_id", -1):
		it["_id"] = str(it["_id"])
		items.append(it)
	return jsonify(items=items)

@bp.post('/item/<id>/approve')
@require_auth
def approve_item(id: str):
	db = get_db()
	db.content.update_one({"_id": ObjectId(id)}, {"$set": {"status": "approved"}})
	return jsonify(ok=True)

@bp.post('/item/<id>/comment')
@require_auth
def comment_item(id: str):
	data = request.get_json() or {}
	comment = {"text": data.get("text", ""), "author": data.get("author", "" )}
	db = get_db()
	db.content.update_one({"_id": ObjectId(id)}, {"$push": {"comments": comment}})
	return jsonify(ok=True)


