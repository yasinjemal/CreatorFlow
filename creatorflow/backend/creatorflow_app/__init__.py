# CreatorFlow Flask App
from .app_types import *  # type: ignore  # placeholder if needed

import os
from flask import Flask, jsonify
from flask_cors import CORS
from .extensions import jwt, mongo_client, redis_client, rq_queue, scheduler, logger
from .settings import AppSettings
from .routes.auth import auth_bp
from .routes.brand import brand_bp
from .routes.content import content_bp
from .routes.schedule import schedule_bp
from .routes.analytics import analytics_bp
from .routes.social import social_bp
from .routes.assets import assets_bp


__all__ = ["create_app"]

def create_app() -> Flask:
	settings = AppSettings()
	app = Flask(__name__)
	app.config["SECRET_KEY"] = settings.secret_key
	app.config["JWT_SECRET_KEY"] = settings.jwt_secret
	app.config["JSON_SORT_KEYS"] = False

	CORS(app, resources={r"/*": {"origins": settings.cors_origins}}, supports_credentials=True, expose_headers=["Authorization"], allow_headers=["Authorization","Content-Type"])

	# Initialize extensions
	jwt.init_app(app)
	mongo_client.init_app(settings.mongo_uri)
	redis_client.init_app(settings.redis_url)
	rq_queue.init_app(redis_client.client)
	scheduler.init_app(app)
	logger.info("CreatorFlow app initialized")

	# Register blueprints
	app.register_blueprint(auth_bp, url_prefix="/auth")
	app.register_blueprint(brand_bp, url_prefix="/brand")
	app.register_blueprint(content_bp, url_prefix="/content")
	app.register_blueprint(schedule_bp, url_prefix="/schedule")
	app.register_blueprint(analytics_bp, url_prefix="/analytics")
	app.register_blueprint(social_bp, url_prefix="/social")
	app.register_blueprint(assets_bp, url_prefix="/assets")

	@app.get("/health")
	def health():
		return jsonify({"status": "ok"})

	return app