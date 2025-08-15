from flask import Blueprint, request, jsonify
from ..db import get_db
from ..services.optimization.timing import suggest_next_windows

bp = Blueprint('analytics', __name__)

@bp.post("/event")
def track_event():
    data = request.get_json() or {}
    db = get_db()
    db.events.insert_one({**data})
    return jsonify(ok=True)

@bp.get("/dashboard")
def dashboard():
    db = get_db()
    total = db.events.count_documents({})
    by_type = {}
    for doc in db.events.aggregate([{"$group":{"_id":"$type","n":{"$sum":1}}}]):
        by_type[doc["_id"]] = doc["n"]
    # Simple recommendation sample
    recs = {p: [dt.isoformat() for dt in suggest_next_windows(p)][:3] for p in [
        "instagram","tiktok","youtube","linkedin","twitter","facebook","pinterest"
    ]}
    return jsonify(total=total, by_type=by_type, recommendations={"best_times": recs})

@bp.post('/ab/create')
def ab_create():
    data = request.get_json() or {}
    db = get_db()
    test = {
        "name": data.get("name","ab-test"),
        "variants": data.get("variants", []),
        "metrics": {}
    }
    res = db.abtests.insert_one(test)
    return jsonify(id=str(res.inserted_id))

@bp.post('/ab/record')
def ab_record():
    data = request.get_json() or {}
    db = get_db()
    var = data.get("variant")
    inc = {f"metrics.{var}.engagement": data.get("engagement",1)}
    db.abtests.update_one({"_id": data.get("id")}, {"$inc": inc})
    return jsonify(ok=True)

@bp.get('/competitors')
def competitors():
    handles = (request.args.get('handles') or '').split(',')
    # Placeholder competitor benchmarking
    bench = {h: {"followers": 10000, "avg_engagement": 2.5} for h in handles if h}
    return jsonify(benchmark=bench)
