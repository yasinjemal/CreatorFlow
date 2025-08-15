from flask import Blueprint, request, jsonify
from ..queue import get_queue
from ..db import get_db
from ..services.social.base import ADAPTERS
from ..utils.crypto import decrypt
from rq.job import Job

bp = Blueprint('schedule', __name__)

def publish_job(payload):
    # Minimal mock implementation: try to use stored OAuth token and echo publish
    platform = payload.get("platform")
    user_id = payload.get("user_id")
    if not platform or not user_id:
        return {"ok": False, "error": "platform and user_id required"}
    from pymongo import MongoClient
    import os
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/creatorflow"))
    db = client.get_default_database()
    tok_doc = db.oauth_tokens.find_one({"user_id": user_id, "platform": platform})
    token = decrypt(tok_doc["token"]) if tok_doc else ""
    adapter = ADAPTERS.get(platform)
    if not adapter:
        return {"ok": False, "error": f"No adapter for {platform}"}
    try:
        res = adapter.publish(token, payload)
        return {"ok": True, "status":"scheduled", "result": res}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@bp.post("/publish")
def publish():
    payload = request.get_json() or {}
    q = get_queue()
    job = q.enqueue(publish_job, payload, job_timeout=600)
    return jsonify(job_id=job.id, status="queued")

@bp.get('/status/<job_id>')
def status(job_id: str):
    q = get_queue()
    try:
        job = Job.fetch(job_id, connection=q.connection)
    except Exception:
        return jsonify(error="job not found"), 404
    return jsonify(
        id=job.id,
        status=job.get_status(),
        enqueued_at=str(getattr(job, 'enqueued_at', '')),
        started_at=str(getattr(job, 'started_at', '')),
        ended_at=str(getattr(job, 'ended_at', '')),
        result=job.result if job.is_finished else None,
        error=getattr(job, 'exc_info', None)
    )
