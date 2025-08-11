from .user_routes import user_bp
from .auth_routes import auth_bp
from .userlist_routes import userlist_bp
from .chat_routes import chat_bp
from .chatlist_routes import chatlist_bp

def register_blueprints(app):
    app.register_blueprint(user_bp)