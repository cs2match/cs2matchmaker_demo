import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    db_name = os.getenv('DB_NAME')  # None이면 DB명 없이 접속
    if db_name:
        db_name_part = f"/{db_name}"
    else:
        db_name_part = ""  # DB명 없이 접속

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}{db_name_part}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if JWT_SECRET_KEY is None:
        raise ValueError("JWT_SECRET_KEY 환경변수가 필요합니다.")
