from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from cs2matchmaker.backend.models.player import Member
from cs2matchmaker.backend.extensions import db
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
        "nickname": user.nickname,
        "premier_rating": user.premier_rating,
        # etc.
    }), 200
#유저정보를 갱신 API (단 해당 유저일 경우에만 사용할 수 있게하기) : 토큰 확인 후 본인일 경우에만 가능
@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403

    user = Member.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.premier_rating = data.get("premier_rating", user.premier_rating)
    user.fivewin_rating = data.get("5win_rating", user.fivewin_rating)
    user.faceit_rating = data.get("faceit_rating", user.faceit_rating)
    user.bestfive_rating = data.get("bestfive_rating", user.bestfive_rating)
    user.nickname = data.get("name", user.nickname)
    user.age = data.get("age", user.age)
    # 리스트는 JSON 문자열로 저장되어 있을 수 있으니 파싱
    if "map_selection" in data:
        user.available_maps = ",".join(data["map_selection"])
    if "mode_preference" in data:
        user.preferred_modes = ",".join(data["mode_preference"])

    user.updated_at = datetime.now(timezone.utc).date()
    db.session.commit()

    # map_selection, mode_preference 파싱 (DB에 JSON or CSV로 저장되었을 경우)
    map_selection = user.available_maps.split(",") if user.available_maps else []
    mode_preference = user.preferred_modes.split(",") if user.preferred_modes else []

    # 응답
    return jsonify({
        "id": user.id,
        "name": user.nickname,
        "date": user.updated_at.isoformat() + "T00:00:00.000Z",  # Date → ISO 포맷
        "premier_rating": user.premier_rating,
        "5win_rating": user.fivewin_rating,
        "faceit_rating": user.faceit_rating,
        "bestfive_rating": user.bestfive_rating,
        "map_selection": map_selection,
        "mode_preference": mode_preference,
        "age": user.age
    }), 200
    #return jsonify({"message": "Updated", "id": user.id}), 200
