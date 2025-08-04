import os
import sys

import jwt
from flask import Flask
from flask_cors import CORS

from cs2matchmaker.backend.config import Config
from cs2matchmaker.backend.extensions import db, jwt
from cs2matchmaker.backend.routes.auth_routes import auth_bp
from cs2matchmaker.backend.routes.user_routes import user_bp
from cs2matchmaker.backend.routes.userlist_routes import userlist_bp

# 부모 디렉토리를 PYTHONPATH에 추가하여 import 경로 문제 방지
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 확장 기능 초기화
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # 블루프린트 등록
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(userlist_bp)

    # 기본 라우트 (서버 정상 여부 확인용)
    @app.route("/")
    def index():
        return "Flask + TiDB + SQLAlchemy 연결 OK!"

    return app

app = create_app()

if __name__ == '__main__':
    # 디버깅을 위한 환경 변수 출력
    print("Loading SSL CA file from:", os.getenv('DB_SSL_CA'))
    print("Full DB URI:", Config.SQLALCHEMY_DATABASE_URI)

    # 외부 접근 허용, 디버그 모드 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
