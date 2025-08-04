from flask import Flask

from cs2matchmaker.backend.config import Config
from cs2matchmaker.backend.extensions import db, jwt
from cs2matchmaker.backend.routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    # Config 클래스 전체 경로로 지정
    app.config.from_object(Config)

    # 확장 기능 초기화
    db.init_app(app)
    jwt.init_app(app)

    # 블루프린트 등록 (create_all 전이라면 URL 등록 먼저 해도 무방)
    app.register_blueprint(user_bp)

    # 앱 컨텍스트 내에서 테이블 생성, models 모듈 임포트는 아래처럼 패키지 전체 import 권장
    with app.app_context():
        import cs2matchmaker.backend.models
        db.create_all()

    return app
