# 코드 스타일
#### 1. 하위 폴더에 존재하는 파일을 import할 때는 상대경로로 작성해주시고
```python
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
```
#### 상위 폴더에 존재하는 파일은 무조건 절대경로로 작성바랍니다.
```python
from cs2matchmaker.backend.models.player import Member
from cs2matchmaker.backend.extensions import db
```
# 커밋 사용시
|    타입    |            목적/설명             |
|:--------:|:----------------------------:|
|   feat   |        새로운 기능 추가 (feature)   |
|   fix    |       버그 수정 (bug fix)        |
|   docs   |     문서 수정 (README, 주석 등)     |
|  style   | 코드 포맷팅, 세미콜론, 띄어쓰기 등 (기능 무관) |
| refactor |      코드 리팩토링 (기능 변화 없음)      |
|   test   |      테스트(코드/케이스) 추가·수정       |
|  chore   |    빌드, 패키지, 환경설정 등 기타 잡일     |
|    ci    |     성능 개선(optimization)      |
|   perf   |    CI(지속적 통합) 설정/스크립트 변경     |

