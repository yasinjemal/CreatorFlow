from flask import Blueprint, request, jsonify
from ..db import get_db
from ..utils.jwt_utils import create_token
import bcrypt

bp = Blueprint('auth', __name__)

@bp.post("/register")
def register():
    data = request.get_json() or {}
    email = data.get("email","").lower().strip()
    password = data.get("password","")
    name = data.get("name","")
    if not email or not password:
        return jsonify(error="email and password required"), 400
    db = get_db()
    if db.users.find_one({"email": email}):
        return jsonify(error="email exists"), 409
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = {"email": email, "password": hashed, "name": name, "role":"user"}
    res = db.users.insert_one(user)
    token = create_token(str(res.inserted_id), email, "user")
    return jsonify(token=token, user={"email": email, "name": name})

@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email","").lower().strip()
    password = data.get("password","")
    db = get_db()
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify(error="invalid credentials"), 401
    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify(error="invalid credentials"), 401
    token = create_token(str(user["_id"]), user["email"], user.get("role","user"))
    return jsonify(token=token, user={"email": user["email"], "name": user.get("name","")})
