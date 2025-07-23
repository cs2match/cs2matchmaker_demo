# yourapp/__init__.py
from flask import Flask
from extensions import db, jwt
from .routes.user_routes import user_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_bp)

    with app.app_context():
        from .models.member import Member
        db.create_all()

    return app
