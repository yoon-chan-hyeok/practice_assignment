# 선택 시연: JSON과 HTML의 차이

필수 구현·채점 대상이 아닙니다. PPT 45·78쪽을 비교할 때 사용합니다.
수강생용/강사용 루트에서 `python -m pip install -r requirements-template.txt`를 실행합니다.
기존 서버를 끄고 이 Template_비교 폴더에서 `python -m uvicorn main:app --reload`로 실행합니다.
GET /api/knowledge는 JSON, GET /web/knowledge는 HTML입니다. 둘 다 이 폴더의 같은 data/knowledge.json을 읽습니다.
07_project와 동일 파일을 공유하는 것은 아니므로 프로젝트 데이터가 이 화면에 자동으로 나타나지 않습니다.
Jinja HTML 자동 이스케이프를 끄지 않습니다. CSS·JavaScript·채팅 UI를 새로 만들지 않습니다.
