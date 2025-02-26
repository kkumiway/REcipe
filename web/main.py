# FastAPI 실행 파일
from fastapi import FastAPI
from routes import router

app = FastAPI()

# API 엔드포인트 등록
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
