from ..extensions import database
from datetime import date


class Member(database.Model):
    __tablename__ = 'members'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    email = database.Column(database.String(255), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)
    nickname = database.Column(database.String(50), nullable=False)
    profile_image = database.Column(database.String(255))
    premier_rating = database.Column(database.Integer, default=0)
    bestfive_rating = database.Column(database.Integer, default=0)
    fivewin_rating = database.Column(database.Integer, default=0)
    faceit_rating = database.Column(database.Integer, default=0)
    age = database.Column(database.Integer, default=0)
    available_maps = database.Column(database.String(255))
    preferred_modes = database.Column(database.String(255))
    server = database.Column(database.String(255))  # <-- server 필드 추가
    updated_at = database.Column(database.Date, default=lambda: date.today())
    joined_at = database.Column(database.Date, default=lambda: date.today())
    
    def serialize(self):
        """객체를 직렬화하여 JSON 형태로 반환"""
        return {
            "id": self.id,
            "email": self.email,
            "nickname": self.nickname,
            "age": self.age,
            "premier_rating": self.premier_rating,
            "faceit_rating": self.faceit_rating,
            "available_maps": self.available_maps.split(",") if self.available_maps else [],
            "preferred_modes": self.preferred_modes.split(",") if self.preferred_modes else [],
            "server": self.server,
            "updated_at": self.updated_at.isoformat(),
            "joined_at": self.joined_at.isoformat()
        }