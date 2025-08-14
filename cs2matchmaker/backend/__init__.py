# /backend/__init__.py
from flask import Flask
from sqlalchemy import text

from .config import Config
from .extensions import database, jwt
from .routes.user_routes import user_bp
from .routes.auth_routes import auth_bp
from .routes.userlist_routes import userlist_bp
from .routes.chat_routes import chat_bp
from .routes.chatlist_routes import chatlist_bp

from flask_cors import CORS
from flask_sse import sse  # sse 통신 프로토콜

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 확장 기능 초기화
    database.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # SSE 블루프린트 등록
    app.register_blueprint(sse, url_prefix='/stream')  # SSE 사용 시 등록

    # 블루프린트 등록
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(userlist_bp)

    # 채팅 관련 블루프린트 등록
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(chatlist_bp, url_prefix='/chatlist')

    # 기본 라우트 (서버 정상 여부 확인용)
    @app.route("/")
    def index():
        return ("Flask + TiDB + SQLAlchemy 연결 OK!\n"
                "http연결 까지 성공하였습니다!")

    # DB 이름이 없거나 별도 지정 시 사용
    db_name = Config.SQLALCHEMY_DATABASE_URI.split('/')[-1].split('?')[0] if '/' in Config.SQLALCHEMY_DATABASE_URI else None

    with app.app_context():
        import cs2matchmaker.backend.models

        # 만약 db_name이 있다면 USE 명령어 실행 후 테이블 생성
        if db_name:
            database.session.execute(text(f"USE {db_name}"))
            database.session.commit()

        database.create_all()

    return app
