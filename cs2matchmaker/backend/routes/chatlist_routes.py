# /backend/routes/chatlist_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, func
from ..extensions import database
from ..models.chat_message import ChatMessage
from ..models.player import Member

chatlist_bp = Blueprint('chatlist', __name__, url_prefix='/chatlist')

# 채팅방 목록 API
@chatlist_bp.route('', methods=['POST'])
@jwt_required()
def chat_list():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    requested_user_id = data.get('id', current_user_id)

    if int(requested_user_id) != current_user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    # 상대방 ID, 마지막 메시지 시간 조회
    subquery = (
        database.session.query(
            func.IF(
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

    # User 테이블 조인해서 상대방 닉네임 가져오기
    results = (
        database.session.query(
            Member.id,
            Member.nickname,
            subquery.c.last_message_time
        )
        .join(subquery, Member.id == subquery.c.other_user_id)
        .order_by(subquery.c.last_message_time.desc())
        .all()
    )

    rooms = [
        {
            "id": r.id,
            "name": r.nickname,
            "date": r.last_message_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        for r in results
    ]

    return jsonify(rooms), 200
