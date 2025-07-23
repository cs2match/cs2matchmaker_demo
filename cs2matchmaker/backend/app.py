#app.py
from flask import Flask
from config import Config
from extensions import db, jwt
from routes.user_routes import user_bp
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

    with app.app_context():
        from models.member import Member
        db.create_all()

    @app.route("/")
    def index():
        return "✅ Flask + TiDB + SQLAlchemy 연결 OK!"

    return app

# 실행
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
