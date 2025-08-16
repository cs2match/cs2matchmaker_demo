from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.player import Member
from ..extensions import database
from datetime import datetime, timezone

user_bp = Blueprint('user', __name__, url_prefix='/user')
# 프로필 (유저 ID에 따라 유저 정보를 가져오는 API)
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Member.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.nickname,
        "premier_rating": user.premier_rating,
        "fivewin_rating": user.fivewin_rating,
        "faceit_rating": user.faceit_rating,
        "bestfive_rating": user.bestfive_rating,
        "map_selection": user.available_maps.split(",") if user.available_maps else [],
        "mode_preference": user.preferred_modes.split(",") if user.preferred_modes else [],
        "age": user.age,
        "date": user.updated_at.isoformat() + "T00:00:00.000Z" if user.updated_at else None
    }), 200

#유저정보를 갱신 API (단 해당 유저일 경우에만 사용할 수 있게하기) : 토큰 확인 후 본인일 경우에만 가능
@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    # [A] JWT에서 유저 ID 추출 → 본인만 변경 가능
    current_user_id = get_jwt_identity()
    if str(current_user_id) != str(user_id):
        return jsonify({"error": "Unauthorized access"}), 403

    user = Member.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # [B] Content-Type 및 body 포맷 확인 → 422 방지
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty body"}), 400

    # [C] 각 필드 갱신
    user.premier_rating = data.get("premier_rating", user.premier_rating)
    user.fivewin_rating = data.get("fivewin_rating", user.fivewin_rating)
    user.faceit_rating = data.get("faceit_rating", user.faceit_rating)
    user.bestfive_rating = data.get("bestfive_rating", user.bestfive_rating)
    user.nickname = data.get("name", user.nickname)
    user.age = data.get("age", user.age)
    # 리스트는 JSON 문자열로 저장되어 있을 수 있으니 파싱
    if "map_selection" in data:
        ms = data["map_selection"]
        if isinstance(ms, list):
            user.available_maps = ",".join(str(x) for x in ms)
        elif ms is None:
            user.available_maps = ""
        else:
            user.available_maps = str(ms)
    if "mode_preference" in data:
        mp = data["mode_preference"]
        if isinstance(mp, list):
            user.preferred_modes = ",".join(str(x) for x in mp)
        elif mp is None:
            user.preferred_modes = ""
        else:
            user.preferred_modes = str(mp)

    user.updated_at = datetime.now(timezone.utc).date()
    database.session.commit()

    # 응답 JSON
    return jsonify({
        "id": user.id,
        "name": user.nickname,
        "date": user.updated_at.isoformat() + "T00:00:00.000Z",
        "premier_rating": user.premier_rating,
        "fivewin_rating": user.fivewin_rating,
        "faceit_rating": user.faceit_rating,
        "bestfive_rating": user.bestfive_rating,
        "map_selection": user.available_maps.split(",") if user.available_maps else [],
        "mode_preference": user.preferred_modes.split(",") if user.preferred_modes else [],
        "age": user.age
    }), 200
    #return jsonify({"message": "Updated", "id": user.id}), 200
