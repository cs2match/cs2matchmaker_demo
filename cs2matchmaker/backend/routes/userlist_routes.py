
from flask import Blueprint, jsonify, request
from extensions import db
from models.player import Member
from sqlalchemy import or_

userlist_bp = Blueprint('userlist_bp', __name__, url_prefix="/userlist")

@userlist_bp.route("/", methods=["POST"])
def get_user_list():
    data = request.get_json()

    # 필터 파라미터 추출 (None 일 때는 무시)
    server = data.get("server")
    rating_min = data.get("rating_min")
    rating_max = data.get("rating_max")
    map_selection = data.get("map_selection")
    mode_preference = data.get("mode_preference")
    age = data.get("age")
    
# 쿼리 빌드
    query = db.session.query(Member)

#레이팅 필터
    if rating_min is not None and rating_max is not None:
        query = query.filter(Member.premier_rating.between(rating_min, rating_max))

    #맵 필터
    if map_selection:
        map_conditions = [Member.available_maps.like(f"%{m}%") for m in map_selection]
        query = query.filter(or_(*map_conditions))
    #모드 필터
    if mode_preference:

        mode_conditions = [Member.preferred_modes.like(f"%{m}%") for m in mode_preference]
        query = query.filter(or_(*mode_conditions))
    #나이 필터
    if age:
        query = query.filter(Member.age == age)
    #서버 필터    
    if server:
        query = query.filter(Member.server == server)
        
    users = query.all()
    
     return jsonify([as_user_dict(u) for u in users]), 200
     