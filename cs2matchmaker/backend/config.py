import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # SSL CA 경로는 OS에 따라 구분자로 안전하게 변환
    ssl_ca_path = os.getenv('DB_SSL_CA', '')
    if ssl_ca_path:
        ssl_ca_path = os.path.normpath(ssl_ca_path)

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '4000')}/{os.getenv('DB_NAME')}"
        f"?ssl_ca={ssl_ca_path}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if JWT_SECRET_KEY is None:
        raise ValueError("JWT_SECRET_KEY 환경변수가 필요합니다.")
