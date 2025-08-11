# extensions.py
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
jwt = JWTManager()