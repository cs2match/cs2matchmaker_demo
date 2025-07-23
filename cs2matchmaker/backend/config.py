# config.py
import os
from dotenv import load_dotenv
load_dotenv('.env')
load_dotenv('.env.database')

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        f"?ssl_ca={os.getenv('DB_SSL_CA')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT 환경변수 추가
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 초 단위, 기본 3600(1시간)
