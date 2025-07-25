 # cs2matchmaker_demo
 - 회원(프로필,갱신 여부 포함), 채팅
   - 회원
     - ID : [PK] ```Integer```
     - 이메일 : ```String(255)```
     - 비밀번호 : ```String(20)```
     - 닉네임 : ```String(10)```
     - 프로필 사진 : (링크) ```String(255)```
     - 프리미어 레이팅 : ```Integer```
     - 베스트파이브 레이팅 : ```Integer```
     - 5윈 레이팅 : ```Integer```
     - faceit 레이팅 : ```Integer```
     - 나이 : (0 이면 비공개) ```Integer```
     - 가능한맵(14개) : ```String(10)``` 
       - Dust 2
       - inferno
       - Mirage
       - Overpass
       - Nuke
       - Vertigo
       - Anubis
       - Ancient
       - Train(collout)
       - Office
       - Italy
       - Jura
       - Grail
       - Agency
     - 선호 게임 모드 :```String(10)```
       - 프리미어
       - 경쟁
       - 캐주얼
       - 윙맨
       - 무기레이스
       - 데스매치
       - 커뮤니티 서버
       - 사설서버
     - 갱신일 Date
       - 처음가입 : null
       - ```updated_at = db.Column(db.Date, default=lambda: date.today())                                      joined_at = db.Column(db.Date, default=lambda: date.today())```
   -  채팅 (보류)
     - 메시지
       -  채팅 ID
       -  채팅 참여자1
       -  채팅 참여자2



## **api 명세**
- 메인화면
    - 필터에 따라 유저 리스트를 가져오는 API
        - POST /userlist
```
{ 
  server : cs2_premier
  rating_min : 1000,
  rating_max : 20000, 
  map_selection: [dust2 … ]
  mode_preference :   [community_server, premier, … ]
  age : 20
} 
```
```
[
{
  id : 1,
  name : player,
  date : 2011-10-05T14:48:00.000Z,
  premier_rating : 1000,
  5win_rating : 1000, 
  faceit_rating : 1000,
  bestfive_rating : 1000,
  map_selection: [dust2 … ]
  mode_preference :   [community_server, premier, … ]
  age : 20
},
…
]
```
---
- 프로필
  1. 유저 ID에 따라 유저 정보를 가져오는 API
      - GET /user/:id
  ```json5
  {
   id : 3,
   name : 'player',
   date : '2011-10-05T14:48:00.000Z',
   premier_rating : 1000,
   5win_rating : 1000, 
   faceit_rating : 1000,
   bestfive_rating : 1000,
   map_selection: ['dust2', … ]
   mode_preference :   ['community_server', 'premier', … ]
   age : 20
  }
  ```
  2. 유저정보를 갱신 API (단 해당 유저일 경우에만 사용할 수 있게하기) : 토큰 확인 후 본인일 경우에만 가능
     - PUT /user/:id
  ```json5
  {
   name : 'player',
   premier_rating : 1000,
   5win_rating : 1000, 
   faceit_rating : 1000,
   bestfive_rating : 1000,
   map_selection: ['dust2', … ]
   mode_preference :   ['community_server', 'premier', … ]
   age : 20
  }
  ```
  ```json5
  {
   id : 3,
   name : 'player',
   date : '2011-10-05T14:48:00.000Z',
   premier_rating : 1000,
   5win_rating : 1000, 
   faceit_rating : 1000,
   bestfive_rating : 1000,
   map_selection: ['dust2', … ]
   mode_preference :   ['community_server', 'premier', … ]
   age : 20
  }
  ```
  3. 업로드 API : 생각해보기
      - 파일을 올리면 깃허브/구글드라이브 API를 호출해서 받은 링크를 반환하기
---
  
- 채팅 : 임시, 차후에 결정하고 수정할 것, 로그인 후 가능
  1. 채팅 보내기 API
  2. 채팅 내역 가져오기 API
  3. 채팅방 목록 가져오기 API
---
- 회원
    - 회원가입 API
        - POST /user/register
  ```json5
  {
    name : 'player',
    email : 'hi@naver.com',
   password: 1234, 
   map_selection: ['dust2', … ]
   age : 20
  }
  ```
  ```json5
  {
    id : 1,
    name : 'player',
    map_selection: ['dust2', … ],
    age : 20,
  }
  ```
  - 이메일 중복 확인 API
      - POST user/duplicate_check
  ```json5
  {
    email : 'hi@naver.com',
  }
  ```
  ```json5
  {
   isDuplicated : true,
  }
  ```
  - 로그인 API : 권한에 따른 토큰 부여
    - POST user/login
  ```json5
  {
    email : 'hi@naver.com',
    password : 1234,
  }
  ```
  ```json5
  {
  isSuccess : true,
  }
  ```
---
## 파트 분배
**연준님** 
- 회원가입 
- 로그인
- 채팅 

**윤재님**
- 필터
- 유저 정보
- 유저 정보 갱신


### *fork 따보고(이해 안되는 부분) 수정할 부분있으면 연락주세요.*
