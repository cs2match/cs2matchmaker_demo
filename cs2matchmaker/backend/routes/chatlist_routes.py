import json
from flask import Blueprint, request, jsonify, stream_with_context, Response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, func
from ..extensions import database
from ..models.chat_message import ChatMessage
from ..models.player import Member
from flask_sse import sse

chatlist_bp = Blueprint('chatlist', __name__, url_prefix='/chatlist')

ISO_UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

@chatlist_bp.route('', methods=['POST'])
@jwt_required()
def chat_list():
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        requested_user_id = int(data.get('id', current_user_id))
        if requested_user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # 페이징 처리 (body에, 없으면 기본값)
        limit = min(int(data.get('limit', 50)), 100)
        offset = int(data.get('offset', 0))

        subquery = (
            database.session.query(
                func.if_(
                    ChatMessage.sender_id == current_user_id,
                    ChatMessage.receiver_id,
                    ChatMessage.sender_id
                ).label('other_user_id'),
                func.max(ChatMessage.timestamp).label('last_message_time')
            )
            .filter(
                or_(
                    ChatMessage.sender_id == current_user_id,
                    ChatMessage.receiver_id == current_user_id
                )
            )
            .group_by('other_user_id')
            .subquery()
        )

        results = (
            database.session.query(
                Member.id,
                Member.nickname,
                subquery.c.last_message_time
            )
            .join(subquery, Member.id == subquery.c.other_user_id)
            .order_by(subquery.c.last_message_time.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        rooms = [
            {
                "id": r.id,
                "name": r.nickname,
                "date": r.last_message_time.astimezone().strftime(ISO_UTC_FORMAT)
                if r.last_message_time else None
            }
            for r in results
        ]

        return jsonify(rooms), 200

    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({'error': 'Server error'}), 500

@chatlist_bp.route('/stream')
@jwt_required()
def chatlist_stream():
    current_user_id = int(get_jwt_identity())
    channel = f'chatlist:user:{current_user_id}'  # 일관성 있는 사용자별 채널명

    @stream_with_context
    def event_stream():
        import time
        last_ping = time.time()
        try:
            for msg in sse.listen(channel=channel):
                yield f"data: {msg.data}\n\n"
                # 30초마다 keepalive ping (client side SSE 연결 유지)
                if time.time() - last_ping > 30:
                    yield "event: ping\ndata: {}\n\n"
                    last_ping = time.time()
        except GeneratorExit:
            pass
        except Exception as e:
            current_app.logger.exception(e)
            yield f"data: {json.dumps({'error': 'SSE stream error'})}\n\n"
    return Response(event_stream(), mimetype='text/event-stream')
