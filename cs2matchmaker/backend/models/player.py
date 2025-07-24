from cs2matchmaker.backend.extensions import db
from datetime import date


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    profile_image = db.Column(db.String(255))
    premier_rating = db.Column(db.Integer, default=0)
    bestfive_rating = db.Column(db.Integer, default=0)
    fivewin_rating = db.Column(db.Integer, default=0)
    faceit_rating = db.Column(db.Integer, default=0)
    age = db.Column(db.Integer, default=0)
    available_maps = db.Column(db.String(255))
    preferred_modes = db.Column(db.String(255))
    updated_at = db.Column(db.Date, default=lambda: date.today())
    joined_at = db.Column(db.Date, default=lambda: date.today())