from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import logging

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # SQLite 데이터베이스 경로 설정
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app,db)

    logging.basicConfig(level=logging.INFO)

    from routes import api_bp
    app.register_blueprint(api_bp)

    CORS(app, resources={r"/*":{"origins":"*"}})

    return app