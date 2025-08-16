from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import mongo_client
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/signup")
def signup():
	data = request.get_json(force=True)
	email = data.get("email", "").strip().lower()
	password = data.get("password", "")
	name = data.get("name", "")
	if not email or not password:
		return jsonify({"error": "email and password required"}), 400
	db = mongo_client.get_db()
	if db.users.find_one({"email": email}):
		return jsonify({"error": "email already exists"}), 409
	db.users.insert_one({
		"email": email,
		"password_hash": generate_password_hash(password),
		"name": name,
		"roles": ["owner"],
	})
	return jsonify({"status": "ok"})


@auth_bp.post("/login")
def login():
	data = request.get_json(force=True)
	email = data.get("email", "").strip().lower()
	password = data.get("password", "")
	db = mongo_client.get_db()
	user = db.users.find_one({"email": email})
	if not user or not check_password_hash(user.get("password_hash", ""), password):
		return jsonify({"error": "invalid credentials"}), 401
	token = create_access_token(identity=str(user["_id"]), additional_claims={"email": email}, expires_delta=timedelta(hours=12))
	return jsonify({"access_token": token})


@auth_bp.get("/me")
@jwt_required()
def me():
	user_id = get_jwt_identity()
	return jsonify({"user_id": user_id})