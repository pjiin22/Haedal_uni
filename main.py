from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from login import verify_student_login
from fastapi.middleware.cors import CORSMiddleware
from trust import TrustScoreManager  # trust.py에서 클래스 불러오기
from probability import ProbabilityManager


app = FastAPI()

# (선택) CORS 설정: JS 프론트엔드와 연동 시 필요
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

trust_manager = TrustScoreManager()  # 인스턴스 생성
probability_manager = ProbabilityManager()


# 루트 접속 시 메시지 반환
@app.get("/")
def root():
    return {"message": "FastAPI 신뢰도 API에 오신 걸 환영합니다!"}

@app.post("/login")
def login(num: str = Form(...), name: str = Form(...), phone: str = Form(...)):
    if verify_student_login(num, name, phone):
        return JSONResponse(content={"success": True, "message": "로그인 성공"})
    else:
        return JSONResponse(content={"success": False, "message": "다시 시도하세요"})

# 신뢰도 업데이트 요청 형식 정의
class TrustEvent(BaseModel):
    user_id: str
    event: str

# POST: 사용자 행동에 따른 신뢰도 업데이트
@app.post("/trust/update")
def update_trust(event: TrustEvent):
    new_score = trust_manager.update(event.user_id, event.event)
    return {"user_id": event.user_id, "new_score": new_score}

# GET: 사용자 신뢰도 조회
@app.get("/trust/{user_id}")
def get_trust(user_id: str):
    score = trust_manager.get_score(user_id)
    return {"user_id": user_id, "trust_score": score}

@app.get("/probability")
def get_probability(elapsed_time: int, trust_score: float):
    """
    경과 시간과 신뢰도를 받아 빈 강의실일 확률을 %로 반환하는 API
    예: /probability?elapsed_time=90&trust_score=0.8
    """
    prob = probability_manager.get_empty_probability(elapsed_time, trust_score)
    return {"elapsed_time": elapsed_time, "trust_score": trust_score, "empty_probability": f"{prob}%"}
