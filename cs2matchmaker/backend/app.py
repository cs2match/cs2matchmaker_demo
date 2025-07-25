#app.py
import os

import jwt
from flask import Flask
from config import Config

from cs2matchmaker.backend import db, jwt

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.userlist_routes import userlist_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 애플리케이션 초기화
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # 블루프린트 등록
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def index():
        return "✅ Flask + TiDB + SQLAlchemy 연결 OK!"
    return app

# 실행
if __name__ == '__main__':
    print("Loading SSL CA file from:", os.getenv('DB_SSL_CA')) #임시 테스트 확인용
    print("Full DB URI:", Config.SQLALCHEMY_DATABASE_URI) #임시 테스트 확인용

    app = create_app()
    app.run(debug=True)
