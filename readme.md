# Q_Rating Coding Standards

원활한 협업을 위해 코딩시 스타일을 통일하는 것이 중요합니다.



### coding styles

1. class 이름은 대문자로 시작하고, 파스칼 표기법(**P**ascal**C**ase)을 사용함.

   예시: BackgroundColor, TypeName, PowerPoint

2. 변수 이름은 소문자이며, 스네이크 표기법을 사용함

   예시: background_color, type_name

3. 변수가  A의 집합(리스트, 튜플 등)일 경우 복수형을 사용함

   예시 : questions = Questions.get.all
   
4. form 의 경우 뒤에 Form을 붙인다

   예시 : UserRegisterForm



### 용어 통일

- 회원가입 : register
- 로그인 : login
- 로그아웃 : logout



### Git Management

1. 깃 사용 순서
   1. git pull origin master
   2. 코딩 (기능 추가)
   3. git add .
   4. git commit -m "커밋메세지"
   5. git push origin master

2. 기능 추가1시마다 commit

   자리 떠날때마다 commit 이 아님!

3. create, update, implement 등의 무난한 단어를 즐겨 쓰자

   나중에 볼 때 편함



### 이거 수정하는 방법

1. 이건 markdown이라는 형식의 문서임

   문법은 여기서 배운다. https://gist.github.com/ihoneymon/652be052a0727ad59601

2. typora 라는 편집기를 설치하면 편함

   https://typora.io/

3. 자유롭게 개발 과정에서 추가해주세요!

