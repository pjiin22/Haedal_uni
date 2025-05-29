from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse

from app import models
from app.database import engine

# 라우터 및 함수 import
from app.auth import router as auth_router, verify_student_login
from app.reservation import router as reservation_router
from app.house_select import router as house_router

# 테이블 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 및 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 라우터 등록
app.include_router(auth_router)
app.include_router(reservation_router)
app.include_router(house_router)

# 루트 리디렉션
@app.get("/")
def root():
    return RedirectResponse(url="/login")

# 로그인 페이지 렌더링
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 로그인 POST 처리
@app.post("/login")
def login(user_id: str = Form(...), name: str = Form(...), phone: str = Form(...)):
    if verify_student_login(user_id, name, phone):
        return JSONResponse(content={"success": True, "message": "로그인 성공"})
    else:
        return JSONResponse(content={"success": False, "message": "다시 시도하세요"})
