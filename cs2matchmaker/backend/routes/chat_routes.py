from flask import Blueprint, request, jsonify, stream_with_context, Response, current_app
from flask_sse import sse
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import database
from ..models.chat_message import ChatMessage
from datetime import datetime, timezone
import json

chat_bp = Blueprint('chat', __name__)

ISO_UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def isoformat_utc(dt):
    if dt is None: return None
    return dt.astimezone(timezone.utc).strftime(ISO_UTC_FORMAT)

def validate_chat_users():
    try:
        user1 = request.args.get('user1', type=int)
        user2 = request.args.get('user2', type=int)
        current_user = int(get_jwt_identity())
        if not user1 or not user2:
            return None, None, None, ("user1 and user2 query parameters are required", 400)
        if current_user not in (user1, user2):
            return None, None, None, ("Unauthorized access", 403)
        return user1, user2, current_user, None
    except Exception as e:
        current_app.logger.exception(e)
        return None, None, None, ("Server error (validate users)", 500)

def make_chat_channel(user1, user2):
    """명확한 채널명: chat:user:{min_userid}:{max_userid}"""
    return f"chat:user:{min(user1, user2)}:{max(user1, user2)}"

def make_list_channel(user_id):
    """사용자별 채팅목록 채널명"""
    return f"chatlist:user:{user_id}"

# 채팅 발송 API
@chat_bp.route('', methods=['POST'])
@jwt_required()
def send_message():
    try:
        sender_id = int(get_jwt_identity())
        data = request.get_json()
        receiver_id = int(data.get('receiverId'))
        content = data.get('content')
        if not receiver_id or not content:
            return jsonify({'error': 'receiverId and content are required'}), 400

        now = datetime.now(timezone.utc)
        message = ChatMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            timestamp=now
        )
        database.session.add(message)
        database.session.commit()

        channel = make_chat_channel(sender_id, receiver_id)
        date_str = isoformat_utc(now)
        # 채팅방 pub/sub 전송
        try:
            sse.publish({
                'senderId': sender_id,
                'receiverId': receiver_id,
                'content': content,
                'date': date_str
            }, type='chat_message', channel=channel)
        except Exception as e:
            current_app.logger.error(f"SSE publish(chat message) error: {e}")

        # 채팅방 목록 갱신용 알림
        try:
            sse.publish({
                'room_id': channel,
                'last_message': content,
                'time': date_str
            }, type='chatlist_update', channel=make_list_channel(receiver_id))
        except Exception as e:
            current_app.logger.error(f"SSE publish(chatlist update) error: {e}")

        return jsonify({'status': 'success', 'date': date_str}), 201
    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({'error': 'Server Error'}), 500

# 채팅 내역 SSE 스트림 (페이징/포맷/예외처리 추가)
@chat_bp.route('/history')
@jwt_required()
def chat_history():
    user1, user2, current_user, error = validate_chat_users()
    if error: return error

    # 페이징 (기본 50개, 쿼리로 조정)
    try:
        limit = min(int(request.args.get('limit', 50)), 100)
        offset = int(request.args.get('offset', 0))
    except Exception:
        limit, offset = 50, 0

    try:
        messages = (
            ChatMessage.query.filter(
                ((ChatMessage.sender_id == user1) & (ChatMessage.receiver_id == user2)) |
                ((ChatMessage.sender_id == user2) & (ChatMessage.receiver_id == user1))
            )
            .order_by(ChatMessage.timestamp.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({'error': 'DB error'}), 500

    @stream_with_context
    def event_stream():
        try:
            for msg in reversed(messages):  # 최신순에서 다시 뒤집어 옛날→최신
                data = {
                    'senderId': msg.sender_id,
                    'receiverId': msg.receiver_id,
                    'content': msg.content,
                    'date': isoformat_utc(msg.timestamp)
                }
                yield f"data: {json.dumps(data)}\n\n"
        except GeneratorExit:
            pass  # 클라이언트 연결 종료시 오류 방지
        except Exception as e:
            current_app.logger.exception(e)
            yield f"data: {json.dumps({'error': 'Server-side exception'})}\n\n"
    return Response(event_stream(), mimetype='text/event-stream')

# 실시간 채팅 SSE 스트림 (서버 부하 관리)
@chat_bp.route('/stream')
@jwt_required()
def chat_stream():
    user1, user2, current_user, error = validate_chat_users()
    if error: return error

    channel = make_chat_channel(user1, user2)

    @stream_with_context
    def event_stream():
        # 서버 부하 완화: keepalive ping, 그리고 1 IP 1 커넥션 등(미구현), 클라이언트 측 제한 권장
        import time
        last_ping = time.time()
        try:
            for msg in sse.listen(channel=channel):
                yield f"data: {msg.data}\n\n"
                # 30초에 한 번씩 keepalive ping (브라우저 SSE timeout 방지)
                if time.time() - last_ping > 30:
                    yield "event: ping\ndata: {}\n\n"
                    last_ping = time.time()
        except GeneratorExit:
            pass
        except Exception as e:
            current_app.logger.exception(e)
            yield f"data: {json.dumps({'error': 'Stream server exception'})}\n\n"
    return Response(event_stream(), mimetype='text/event-stream')
