from flask import Blueprint, request, jsonify, stream_with_context, Response
from flask_sse import sse
from cs2matchmaker.backend.extensions import db
from cs2matchmaker.backend.models.chat_message import ChatMessage  # 모델 예시
chat_bp = Blueprint('chat', __name__)

# 채팅 발송 API - POST /chat
@chat_bp.route('', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = data.get('senderId')
    receiver_id = data.get('receiverId')
    content = data.get('content')

    # 메시지 DB 저장 (예시)
    message = ChatMessage(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(message)
    db.session.commit()

    # 새로운 메시지 SSE로 해당 채팅방에 푸시
    sse.publish({
        'senderId': sender_id,
        'receiverId': receiver_id,
        'content': content,
        'date': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }, type='chat_message', channel=f'chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}')

    return jsonify({'status': 'success'})

# 채팅방 목록 리스트 - POST /chatlist
@chat_bp.route('/list', methods=['POST'])
def chat_list():
    data = request.get_json()
    user_id = data.get('id')

    # 예시: DB에서 user_id가 참여하고 있는 채팅방 목록 조회 (구현 필요)
    rooms = [
        {'id': 2, 'name': '사용자2', 'date': '2024-08-04'},
        {'id': 3, 'name': '사용자3', 'date': '2024-08-03'},
        # ...
    ]

    return jsonify(rooms)

# 채팅 내역 SSE 스트림 - GET /stream/chat?user1=1&user2=2
@chat_bp.route('/history')
def chat_history():
    user1 = request.args.get('user1', type=int)
    user2 = request.args.get('user2', type=int)
    if not user1 or not user2:
        return "user1 and user2 query parameters are required", 400

    channel = f'chat_{min(user1, user2)}_{max(user1, user2)}'

    @stream_with_context
    def event_stream():
        # 첫 접속 시 기존 메시지들을 DB에서 조회해 먼저 전송 (구현 필요)
        messages = ChatMessage.query.filter(
            ((ChatMessage.sender_id == user1) & (ChatMessage.receiver_id == user2)) |
            ((ChatMessage.sender_id == user2) & (ChatMessage.receiver_id == user1))
        ).order_by(ChatMessage.timestamp).all()

        for msg in messages:
            yield f"data: { {
                'senderId': msg.sender_id,
                'receiverId': msg.receiver_id,
                'content': msg.content,
                'date': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            } }\n\n"

        # 이후 실시간으로 오는 메시지는 SSE 기본 플로우에 맡김

    return Response(event_stream(), mimetype='text/event-stream')