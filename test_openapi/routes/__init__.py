from flask import Blueprint
from .chatRoutes import chat_bp
from .audioRoutes import audio_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(chat_bp, url_prefix="/api/chat")
api_bp.register_blueprint(audio_bp, url_prefix="/api/audio")