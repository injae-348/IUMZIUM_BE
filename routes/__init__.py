from flask import Blueprint
from .audioRoutes import audio_bp
from .rasaRoutes import rasa_bp
from .drinkRoutes import drink_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(audio_bp, url_prefix="/api/audio")
api_bp.register_blueprint(rasa_bp, url_prefix="/api/rasa")
api_bp.register_blueprint(drink_bp, url_prefix="/api/drink")