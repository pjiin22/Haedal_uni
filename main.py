from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse

from app import models
from app.database import engine

from app.auth import router as auth_router, verify_student_login
from app.reservation import router as reservation_router
from app.house_select import router as house_router
from app.class_info import router as class_info_router
from app.class_list import router as class_list_router
from app.point import router as point_router
from app.predict import router as predict_router


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)
app.include_router(reservation_router)
app.include_router(house_router)
app.include_router(class_info_router)
app.include_router(class_list_router)
app.include_router(point_router, prefix="/points", tags=["Points"])  
app.include_router(predict_router)



@app.get("/")
def root():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(user_id: str = Form(...), name: str = Form(...), phone: str = Form(...)):
    if verify_student_login(user_id, name, phone):
        return JSONResponse(content={"success": True, "message": "로그인 성공"})
    else:
        return JSONResponse(content={"success": False, "message": "다시 시도하세요"})

@app.get("/mainmenu.html", response_class=HTMLResponse)
def mainmenu_page(request: Request):
    return templates.TemplateResponse("mainmenu.html", {"request": request})

@app.get("/classroom-search1.html", response_class=HTMLResponse)
def classroom_search1_page(request: Request):
    return templates.TemplateResponse("classroom-search1.html", {"request": request})

@app.get("/classroom-search2.html", response_class=HTMLResponse)
def classroom_search2_page(request: Request):
    return templates.TemplateResponse("classroom-search2.html", {"request": request})

@app.get("/classroom-page1.html", response_class=HTMLResponse)
def classroom_page1_page(request: Request):
    return templates.TemplateResponse("classroom-page1.html", {"request": request})

@app.get("/classroom-page2.html", response_class=HTMLResponse)
def classroom_page2_page(request: Request):
    return templates.TemplateResponse("classroom-page2.html", {"request": request})

@app.get("/usage-history.html", response_class=HTMLResponse)
def usage_history_page(request: Request):
    return templates.TemplateResponse("usage-history.html", {"request": request})

@app.get("/point.html", response_class=HTMLResponse)
def point_page(request: Request):
    return templates.TemplateResponse("point.html", {"request": request})


@app.get("/mypage.html", response_class=HTMLResponse)
def point_page(request: Request):
    return templates.TemplateResponse("mypage.html", {"request": request})