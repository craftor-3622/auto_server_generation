import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.sqlite3"  # SQLite

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB 및 테이블 생성 함수
def init_db():
    from models import User  # Base를 상속한 모델 import 필수
    # ✅ 파일 존재 여부 확인 (SQLite인 경우만 적용)
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
        db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
        if not os.path.exists(db_path):
            Base.metadata.create_all(bind=engine)
    else:
        # PostgreSQL 등은 항상 실행
        Base.metadata.create_all(bind=engine)


# 의존성 주입용 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
