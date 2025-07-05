from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, threads, users
from database import init_db

app = FastAPI()

# ✅ DB 및 테이블 자동 생성
init_db()

# 개발 용도 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(threads.router)