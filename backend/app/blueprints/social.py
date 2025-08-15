from flask import Blueprint, request, jsonify
from ..db import get_db
from ..utils.crypto import encrypt, decrypt
from flask import current_app, redirect
import urllib.parse
import requests

bp = Blueprint('social', __name__)

@bp.post("/oauth/store")
def store_oauth_token():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    platform = data.get("platform")
    access_token = data.get("access_token")
    if not (user_id and platform and access_token):
        return jsonify(error="Missing fields"), 400
    db = get_db()
    db.oauth_tokens.update_one(
        {"user_id": user_id, "platform": platform},
        {"$set": {"token": encrypt(access_token)}},
        upsert=True
    )
    return jsonify(ok=True)

@bp.get("/oauth/list")
def list_oauth():
    user_id = request.args.get("user_id")
    db = get_db()
    items = list(db.oauth_tokens.find({"user_id": user_id}, {"token":0}))
    for it in items:
        it["_id"] = str(it["_id"])
    return jsonify(items=items)

@bp.get('/linkedin/start')
def linkedin_start():
    client_id = current_app.config.get('LINKEDIN_CLIENT_ID')
    redirect_uri = current_app.config.get('LINKEDIN_REDIRECT_URI', 'http://localhost:8000/social/linkedin/callback')
    scope = 'w_member_social'
    # carry user_id through state so callback can store token for the right user
    state = request.args.get('user_id', 'creatorflow')
    url = 'https://www.linkedin.com/oauth/v2/authorization?' + urllib.parse.urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state,
    })
    return redirect(url)

@bp.get('/linkedin/callback')
def linkedin_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if not code:
        return jsonify(error='missing code'), 400
    client_id = current_app.config.get('LINKEDIN_CLIENT_ID')
    client_secret = current_app.config.get('LINKEDIN_CLIENT_SECRET')
    redirect_uri = current_app.config.get('LINKEDIN_REDIRECT_URI', 'http://localhost:8000/social/linkedin/callback')
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    resp = requests.post(token_url, data=data, timeout=30)
    try:
        payload = resp.json()
    except Exception:
        payload = {}
    # persist token if present
    access_token = payload.get('access_token')
    if access_token and state:
        db = get_db()
        db.oauth_tokens.update_one(
            {"user_id": state, "platform": "linkedin"},
            {"$set": {"token": encrypt(access_token)}},
            upsert=True
        )
    # After storing, redirect back to frontend with status
    if payload.get('access_token'):
        front = current_app.config.get('FRONTEND_BASE_URL', 'http://localhost:3000')
        return redirect(f"{front}/integrations?connected=linkedin&user_id={urllib.parse.quote(state or '')}")
    return jsonify(token_response=payload, stored=False)

@bp.get('/linkedin/me')
def linkedin_me():
    """Fetch current member and store person URN in profiles."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify(error='missing user_id'), 400
    db = get_db()
    tok = db.oauth_tokens.find_one({"user_id": user_id, "platform": "linkedin"})
    if not tok:
        return jsonify(error='not connected'), 400
    token = decrypt(tok.get('token',''))
    if not token:
        return jsonify(error='invalid token'), 400
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get('https://api.linkedin.com/v2/me', headers=headers, timeout=30)
    if not resp.ok:
        return jsonify(error='linkedin me failed', status=resp.status_code, data=resp.text), 502
    data = resp.json()
    lid = data.get('id')
    if not lid:
        return jsonify(error='no id'), 502
    urn = f"urn:li:person:{lid}"
    db.profiles.update_one({"user_id": user_id}, {"$set": {"linkedin_urn": urn}}, upsert=True)
    prof = db.profiles.find_one({"user_id": user_id}) or {}
    if prof.get('_id'):
        prof['_id'] = str(prof['_id'])
    return jsonify(urn=urn, profile=prof)

@bp.get('/profile')
def get_profile():
    user_id = request.args.get('user_id')
    db = get_db()
    prof = db.profiles.find_one({"user_id": user_id}) or {}
    if prof.get('_id'):
        prof['_id'] = str(prof['_id'])
    return jsonify(profile=prof)
