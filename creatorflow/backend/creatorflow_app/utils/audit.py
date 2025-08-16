from datetime import datetime
from ..extensions import mongo_client


def audit_log(event: str, actor_user_id: str | None, details: dict | None = None):
	db = mongo_client.get_db()
	db.audit.insert_one({
		"event": event,
		"actor_user_id": actor_user_id,
		"details": details or {},
		"created_at": datetime.utcnow(),
	})