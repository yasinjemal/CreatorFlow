import os
from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from .db import get_db, close_db
from .queue import get_queue

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True)

    # db and queue on teardown
    app.teardown_appcontext(close_db)

    # Blueprints
    from .blueprints.auth import bp as auth_bp
    from .blueprints.content import bp as content_bp
    from .blueprints.schedule import bp as schedule_bp
    from .blueprints.analytics import bp as analytics_bp
    from .blueprints.social import bp as social_bp
    from .blueprints.assets import bp as assets_bp
    from .blueprints.library import bp as library_bp
    from .blueprints.workflow import bp as workflow_bp
    from .blueprints.campaigns import bp as campaigns_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(content_bp, url_prefix="/content")
    app.register_blueprint(schedule_bp, url_prefix="/schedule")
    app.register_blueprint(analytics_bp, url_prefix="/analytics")
    app.register_blueprint(social_bp, url_prefix="/social")
    app.register_blueprint(assets_bp, url_prefix="/assets")
    app.register_blueprint(library_bp, url_prefix="/library")
    app.register_blueprint(workflow_bp, url_prefix="/workflow")
    app.register_blueprint(campaigns_bp, url_prefix="/campaigns")

    @app.get("/health")
    def health():
        return jsonify(status="ok")
    return app
