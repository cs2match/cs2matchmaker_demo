from cs2matchmaker.backend.extensions import db
from datetime import datetime

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ChatMessage {self.id} from {self.sender_id} to {self.receiver_id}>'
