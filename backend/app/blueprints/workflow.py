from flask import Blueprint, request, jsonify
from ..db import get_db
from ..utils.auth import require_auth, require_role
from bson import ObjectId

bp = Blueprint('workflow', __name__)

@bp.post('/team')
@require_role('admin')
def create_team():
	data = request.get_json() or {}
	db = get_db()
	team = {"name": data.get("name", "Team"), "members": data.get("members", [])}
	res = db.teams.insert_one(team)
	return jsonify(id=str(res.inserted_id))

@bp.post('/team/invite')
@require_role('admin','manager')
def invite():
	data = request.get_json() or {}
	db = get_db()
	db.invitations.insert_one({"email": data.get("email"), "team_id": data.get("team_id"), "role": data.get("role","editor")})
	return jsonify(ok=True)

@bp.get('/team/members')
@require_auth
def members():
	team_id = request.args.get('team_id')
	db = get_db()
	try:
		obj_id = ObjectId(team_id)
	except Exception:
		return jsonify(members=[])
	team = db.teams.find_one({"_id": obj_id})
	if not team:
		return jsonify(members=[])
	return jsonify(members=team.get('members', []))


