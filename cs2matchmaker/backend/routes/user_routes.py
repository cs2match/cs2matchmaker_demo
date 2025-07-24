from flask import Blueprint, jsonify, request
from cs2matchmaker.backend.models.player import Member
from cs2matchmaker.backend.extensions import db
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')

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

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Member.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.premier_rating = data.get("premier_rating", user.premier_rating)
    user.updated_at = datetime.utcnow().date()

    db.session.commit()

    return jsonify({"message": "Updated", "id": user.id}), 200
