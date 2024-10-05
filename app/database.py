from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 파일 생성
SQLALCHEMY_DATABASE_URL = "sqlite:///./welfare_center.db"

# 데이터베이스 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 로컬 객체 생성 (데이터베이스와의 연결 관리)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 기본적인 모델 클래스 정의 (모든 ORM 모델은 이 클래스를 상속받음)
Base = declarative_base()

# 데이터베이스 테이블을 생성하기 위한 함수
def init_db():
    Base.metadata.create_all(bind=engine)

# 데이터베이스 세션 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()