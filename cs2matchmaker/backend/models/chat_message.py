from ..extensions import database
from datetime import datetime, timezone  # timezone 추가

class ChatMessage(database.Model):
    __tablename__ = 'chat_messages'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    sender_id = database.Column(database.Integer, nullable=False)
    receiver_id = database.Column(database.Integer, nullable=False)
    content = database.Column(database.Text, nullable=False)
    # 권장 방식: timezone-aware UTC datetime
    timestamp = database.Column(
        database.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<ChatMessage {self.id} from {self.sender_id} to {self.receiver_id}>'

    # 직렬화 메서드
    def serialize(self):
        return {
            "id": self.id,
            "senderId": self.sender_id,
            "receiverId": self.receiver_id,
            "content": self.content,
            "date": self.timestamp.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        }
