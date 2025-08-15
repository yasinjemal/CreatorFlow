from flask import Blueprint, request, jsonify
from ..db import get_db
from ..services.brand.consistency import analyze_tone
from werkzeug.utils import secure_filename
import os

bp = Blueprint('assets', __name__)

@bp.post("/brand")
def save_brand():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    profile = data.get("profile", {})
    db = get_db()
    db.brands.update_one({"user_id": user_id}, {"$set": profile}, upsert=True)
    return jsonify(ok=True)

@bp.get("/brand")
def get_brand():
    user_id = request.args.get("user_id")
    db = get_db()
    profile = db.brands.find_one({"user_id": user_id}) or {}
    if "_id" in profile:
        profile["_id"] = str(profile["_id"])
    return jsonify(profile=profile)

@bp.post("/brand/tone-check")
def brand_tone_check():
    data = request.get_json() or {}
    text = data.get("text", "")
    brand_voice = data.get("brand_voice", "confident, concise")
    analysis = analyze_tone(text, brand_voice)
    return jsonify(analysis=analysis)

@bp.post('/upload')
def upload_asset():
    f = request.files.get('file')
    if not f:
        return jsonify(error='No file'), 400
    name = secure_filename(f.filename)
    os.makedirs('/tmp/creatorflow', exist_ok=True)
    path = os.path.join('/tmp/creatorflow', name)
    f.save(path)
    return jsonify(ok=True, path=path)
