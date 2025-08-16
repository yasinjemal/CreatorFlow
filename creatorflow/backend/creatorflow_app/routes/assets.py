from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

assets_bp = Blueprint("assets", __name__)


@assets_bp.post("/upload")
@jwt_required()
def upload():
	# In production, use presigned S3 URLs and validate mime/types
	return jsonify({"status": "todo", "message": "use presigned upload"})