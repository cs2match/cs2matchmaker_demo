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
    # JWT에서 가져온 identity 값을 정수형으로 변환
    current_user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    # 요청 데이터의 id 역시 정수형으로 변환, 없으면 current_user_id 기본값 사용
    requested_user_id = int(data.get('id', current_user_id))

    # 타입이 통일되어 정확한 비교 가능
    if requested_user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    # 이하 쿼리 등 기존 코드 유지
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