# /backend/routes/chat_routes.py
from flask import Blueprint, request, jsonify, stream_with_context, Response
from flask_sse import sse
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import database
from ..models.chat_message import ChatMessage
from datetime import datetime, timezone  # timezone import

chat_bp = Blueprint('chat', __name__)

# 채팅 발송 API - POST /chat
@chat_bp.route('', methods=['POST'])
@jwt_required()
def send_message():
    sender_id = get_jwt_identity()
    data = request.get_json()
    receiver_id = data.get('receiverId')
    content = data.get('content')

    if not receiver_id or not content:
        return jsonify({'error': 'receiverId and content are required'}), 400

    # 메시지 DB 저장 (timezone-aware UTC datetime 사용)
    message = ChatMessage(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        timestamp=datetime.now(timezone.utc)
    )
    database.session.add(message)
    database.session.commit()

    channel = f'chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}'

    sse.publish({
        'senderId': sender_id,
        'receiverId': receiver_id,
        'content': content,
        'date': message.timestamp.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    }, type='chat_message', channel=channel)

    return jsonify({'status': 'success'}), 201


# 채팅 내역 SSE 스트림
@chat_bp.route('/history')
@jwt_required()
def chat_history():
    user1 = request.args.get('user1', type=int)
    user2 = request.args.get('user2', type=int)
    current_user = get_jwt_identity()

    if not user1 or not user2:
        return "user1 and user2 query parameters are required", 400

    if current_user not in (user1, user2):
        return "Unauthorized access", 403

    @stream_with_context
    def event_stream():
        # 기존 메시지 전송
        messages = ChatMessage.query.filter(
            ((ChatMessage.sender_id == user1) & (ChatMessage.receiver_id == user2)) |
            ((ChatMessage.sender_id == user2) & (ChatMessage.receiver_id == user1))
        ).order_by(ChatMessage.timestamp).all()

        for msg in messages:
            yield f"data: { { 
                'senderId': msg.sender_id, 
                'receiverId': msg.receiver_id,
                'content': msg.content,
                'date': msg.timestamp.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            } }\n\n"

    return Response(event_stream(), mimetype='text/event-stream')
