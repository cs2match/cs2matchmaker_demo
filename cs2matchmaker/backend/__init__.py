# yourapp/__init__.py

from flask import Flask
from .extensions import db, jwt  # extensions.py에서 직접 인스턴스를 import
from .routes.user_routes import user_bp
from .config import Config   # 상대 경로로 불러오는 방식 권장

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 실제로 확장 기능 init
    db.init_app(app)
    jwt.init_app(app)

    # 블루프린트 등록
    app.register_blueprint(user_bp)

    # DB 테이블 생성 (앱 실행 시 단 1회만 실행됨)
    with app.app_context():
        from .models.member import Member  # 지연 import (순환참조 방지)
        db.create_all()

    return app
