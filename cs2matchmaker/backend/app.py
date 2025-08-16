#app.py
import os
import sys

# 부모 디렉토리를 PYTHONPATH에 추가하여 import 경로 문제 방지
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cs2matchmaker', 'backend'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from cs2matchmaker.backend import create_app
from cs2matchmaker.backend.config import Config

app = create_app()

if __name__ == '__main__':
    # 디버깅 환경 변수 출력
    print("Loading SSL CA file from:", os.getenv('DB_SSL_CA'))
    print("Full DB URI:", Config.SQLALCHEMY_DATABASE_URI)

    # 외부 접근 허용, 디버그 모드 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
