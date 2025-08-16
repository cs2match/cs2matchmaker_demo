from flask import Blueprint, request, jsonify
from cs2matchmaker.backend.extensions import database
from cs2matchmaker.backend.models.player import Member  # 모델 임포트 경로 확인 필요
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/user')

# 회원가입 API
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data"}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    map_selection = data.get('map_selection', [])
    age = data.get('age')

    if None in (name, email, password, age):
        return jsonify({"error": "Missing required fields"}), 400

    # 이메일 중복 체크
    if Member.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed_pw = generate_password_hash(password)
    member = Member(
        nickname=name,
        email=email,
        password=hashed_pw,
        available_maps=",".join(map_selection) if isinstance(map_selection, list) else "",
        age=age,
        joined_at=datetime.date.today()
    )
    database.session.add(member)
    database.session.commit()

    return jsonify({
        "id": member.id,
        "name": member.nickname,
        "map_selection": map_selection,
        "age": age
    }), 201

# 이메일 중복 확인 API
@auth_bp.route('/duplicate_check', methods=['POST'])
def duplicate_check():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email not provided"}), 400

    is_duplicated = Member.query.filter_by(email=email).first() is not None
    return jsonify({"isDuplicated": is_duplicated}), 200

# 로그인 API
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = Member.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"isSuccess": False}), 401

    #토큰 발행(1시간 유효)
    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))

    #로그인 성공 시 user_id도 함께 반환
    return jsonify({
        "isSuccess": True,
        "access_token": access_token,
        "user_id": user.id,
    }), 200