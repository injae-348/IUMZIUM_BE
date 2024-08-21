from flask import Blueprint
from .audioRoutes import audio_bp
from .rasaRoutes import rasa_bp
from .drinkRoutes import drink_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(audio_bp, url_prefix="/api/audio")
api_bp.register_blueprint(drink_bp, url_prefix="/api/drink")
api_bp.register_blueprint(rasa_bp, url_prefix="/api/rasa")


# 클로바 api 만 호출
# POST /api/audio/

# 클로바 api + rasa 호출
# POST /api/audio/rasa/

# 음료 카테고리
# GET /api/drink/?category=

# rasa 호출
# POST /api/rasa/test