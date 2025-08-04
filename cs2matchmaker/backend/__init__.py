#init.py
from flask import Flask

from .config import Config
from .extensions import db, jwt
from .routes.user_routes import user_bp
from .routes.auth_routes import auth_bp
from .routes.userlist_routes import userlist_bp
from .routes.chat_routes import chat_bp

from flask_cors import CORS
from flask_sse import sse  #sse 통신 프로토콜

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 확장 기능 초기화
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # SSE 블루프린트 등록
    app.register_blueprint(sse, url_prefix='/stream')  # SSE 사용시 등록

    # 블루프린트 등록
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(userlist_bp)

    # 채팅 관련 블루프린트 등록
    app.register_blueprint(chat_bp, url_prefix='/chat')

    # 기본 라우트 (서버 정상 여부 확인용)
    @app.route("/")
    def index():
        return "Flask + TiDB + SQLAlchemy 연결 OK!"

    # 앱 컨텍스트 내에서 테이블 생성과 모델 임포트
    with app.app_context():
        import cs2matchmaker.backend.models
        db.create_all()

    return app
