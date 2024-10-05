from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.admin import router as admin_router
from app.database import SessionLocal, init_db, get_db
from app.models import PageContent

app = FastAPI()

# Static files 설정 (CSS, 이미지)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates 설정
templates = Jinja2Templates(directory="app/templates")

# 데이터베이스 초기화
init_db()



# 메인 페이지 라우팅 (DB에서 페이지 내용 가져오기)
@app.get("/")
def read_main_page(request: Request, db: Session = Depends(get_db)):
    # 데이터베이스에서 센터 소개 페이지 내용 가져오기
    # page_content = db.query(PageContent).filter(PageContent.page_name == "index").first()
    return templates.TemplateResponse("index.html", {"request": request
                                                    #  , "content": page_content.content if page_content else "소개 내용이 없습니다."
                                                     })

# 기타 페이지 라우팅
@app.get("/activities")
def read_activities_page(request: Request, db: Session = Depends(get_db)):
    # 활동 페이지 내용 가져오기
    page_content = db.query(PageContent).filter(PageContent.page_name == "activities").first()
    return templates.TemplateResponse("activities.html", {"request": request, "content": page_content.content if page_content else "활동 내용이 없습니다."})

@app.get("/directions")
def read_directions_page(request: Request, db: Session = Depends(get_db)):
    # 오시는 길 페이지 내용 가져오기
    page_content = db.query(PageContent).filter(PageContent.page_name == "directions").first()
    return templates.TemplateResponse("directions.html", {"request": request, "content": page_content.content if page_content else "오시는 길 내용이 없습니다."})

# Admin 라우터 추가 (admin.py에서 가져온 라우터)
app.include_router(admin_router)
