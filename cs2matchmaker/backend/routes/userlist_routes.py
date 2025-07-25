
from flask import Blueprint, request, jsonify
from cs2matchmaker.backend.extensions import db
from cs2matchmaker.backend.models.player import Member  # 혹은 환경에 맞는 모델 import
import datetime

userlist_bp = Blueprint('userlist', __name__, url_prefix='/')

def str_list_to_list(s):
    """DB에 콤마로 저장된 경우 파싱 편의 함수"""
    return s.split(',') if s else []

@userlist_bp.route('/userlist', methods=['POST'])
def get_user_list():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data"}), 400

    # 필터 파라미터 추출 (None 일 때는 무시)
    server = data.get('server')
    rating_min = data.get('rating_min', 0)
    rating_max = data.get('rating_max', 99999)
    map_selection = data.get('map_selection', [])
    mode_preference = data.get('mode_preference', [])
    age = data.get('age')

    # 쿼리 빌드
    query = Member.query

    if isinstance(age, int):
        query = query.filter(Member.age == age)
    query = query.filter(Member.premier_rating >= rating_min,
                         Member.premier_rating <= rating_max)
    # 맵/모드 필터: (단순 LIKE/IN, 실제 DB 스키마 따라 다르게 개선 가능)
    if map_selection:
        for map_name in map_selection:
            query = query.filter(Member.available_maps.contains(map_name))
    if mode_preference:
        for mode in mode_preference:
            query = query.filter(Member.preferred_modes.contains(mode))
    # 서버 필터용 컬럼이 존재하면 추가, 없으면 생략
    # if server and hasattr(Member, "server"):
    #     query = query.filter(Member.server == server)

    users = query.all()

    # 리스트 변환 및 가공 반환
    def as_user_dict(user):
        return {
            "id": user.id,
            "name": user.nickname,
            "date": user.updated_at.isoformat() + "T00:00:00.000Z" if user.updated_at else None,
            "premier_rating": user.premier_rating,
            "5win_rating": getattr(user, "fivewin_rating", None),   # 컬럼명에 유의
            "faceit_rating": user.faceit_rating,
            "bestfive_rating": user.bestfive_rating,
            "map_selection": str_list_to_list(user.available_maps),
            "mode_preference": str_list_to_list(user.preferred_modes),
            "age": user.age,
        }

    return jsonify([as_user_dict(u) for u in users]), 200
