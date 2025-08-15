from __future__ import annotations
from functools import wraps
from typing import Callable
from flask import request, jsonify, g
from ..utils.jwt_utils import decode_token


def get_auth_user():
	"""Decode JWT from Authorization header 'Bearer <token>' and attach to g.user."""
	head = request.headers.get("Authorization", "")
	if head.lower().startswith("bearer "):
		token = head.split(" ", 1)[1]
		try:
			payload = decode_token(token)
			g.user = payload
			return payload
		except Exception:
			return None
	return None


def require_auth(fn: Callable):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		user = get_auth_user()
		if not user:
			return jsonify(error="unauthorized"), 401
		return fn(*args, **kwargs)
	return wrapper


def require_role(*roles: str):
	def decorator(fn: Callable):
		@wraps(fn)
		def wrapper(*args, **kwargs):
			user = get_auth_user()
			if not user:
				return jsonify(error="unauthorized"), 401
			if user.get("role") not in roles:
				return jsonify(error="forbidden"), 403
			return fn(*args, **kwargs)
		return wrapper
	return decorator
