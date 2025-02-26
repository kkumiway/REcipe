# FastAPI 실행 파일

from fastapi import FastAPI
from routes import router

app = FastAPI()

# routes.py에서 정의한 API 엔드포인트 등록
app.include_router(router) # routes.py에서 만든 API가 FastAPI에서 작동

if __name__ == "__main__": # Python 내부적으로 예약된 특수 변수 -> __name/main__
    import uvicorn # FastAPI 서버 실행
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True) # reload=True : 코드 변경시 자동으로 서버 재시작
