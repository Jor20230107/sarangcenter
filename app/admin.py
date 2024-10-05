from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# 패스워드 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 예시 관리자 계정
fake_admin_user = {
    "username": "admin",
    "password": pwd_context.hash("admin123")
}

# 로그인 처리
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_admin_user
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": "admin_token", "token_type": "bearer"}

# 관리자 대시보드
@router.get("/admin")
def admin_dashboard(token: str = Depends(oauth2_scheme)):
    if token != "admin_token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Welcome to the admin dashboard"}

# 페이지 수정
@router.post("/admin/edit")
def edit_page(page_name: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    # 페이지가 존재하는지 확인하고 업데이트
    page = db.query(PageContent).filter(PageContent.page_name == page_name).first()
    if page:
        page.content = content
    else:
        # 페이지가 없으면 새로 생성
        new_page = PageContent(page_name=page_name, content=content)
        db.add(new_page)
    db.commit()
    return {"message": f"Page {page_name} updated successfully!"}

# 이미지 업로드
@router.post("/admin/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"app/static/images/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}
