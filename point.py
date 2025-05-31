from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter()

# 포인트정보 저장용 (DB에서 구현 계획이라면 Reserve처럼 모델을 만들고 연결)
user_points = {}

# 포인트 요청 목록
class PointRequest(BaseModel):
    user_id: str
    reason: str

# 포인트 적립
@router.post("/points/add")
def add_points(req: PointRequest, db: Session = Depends(get_db)):
    points_to_add = {
        "lecture_completed": 5,
        "cancel_before_15min": 5,
        "report_misuse": 10,
    }
    if req.reason not in points_to_add:
        raise HTTPException(status_code=400, detail="알 수 없는 적립 사유입니다.")
    if req.user_id not in user_points:
        user_points[req.user_id] = 100
    user_points[req.user_id] += points_to_add[req.reason]
    return {
        "user_id": req.user_id,
        "points": user_points[req.user_id],
        "message": f"{points_to_add[req.reason]}포인트 적립 완료"
    }

# 포인트 차감
@router.post("/points/deduct")
def deduct_points(req: PointRequest, db: Session = Depends(get_db)):
    points_to_deduct = {
        "no_checkout": 15,
        "no_auth_in_time": 10,
    }
    if req.reason not in points_to_deduct:
        raise HTTPException(status_code=400, detail="알 수 없는 차감 사유입니다.")
    if req.user_id not in user_points:
        user_points[req.user_id] = 100
    user_points[req.user_id] -= points_to_deduct[req.reason]
    if user_points[req.user_id] < 0:
        user_points[req.user_id] = 0
    return {
        "user_id": req.user_id,
        "points": user_points[req.user_id],
        "message": f"{points_to_deduct[req.reason]}포인트 차감 완료"
    }

# 포인트 조회
@router.get("/points/{user_id}")
def get_points(user_id: str, db: Session = Depends(get_db)):
    if user_id not in user_points:
        user_points[user_id] = 100
    return {
        "user_id": user_id,
        "points": user_points[user_id]
    }

# 포인트 이력 확인
@router.get("/history/{user_id}")
def get_point_history(user_id: str, db: Session = Depends(get_db)):
    history = db.query(models.Point).filter(models.Point.user_id == user_id).order_by(models.Point.time.desc()).all()
    if not history:
        return []

    result = []
    for row in history:
        point_value = row.plus if row.plus > 0 else -row.minus
        result.append({
            "type": "plus" if row.plus > 0 else "minus",
            "value": point_value,
            "description": get_reason_description(row.plus, row.minus),
            "timestamp": row.time.strftime("%Y-%m-%d %H:%M")
        })
    return result

def get_reason_description(plus: int, minus: int) -> str:
    if plus == 100: return "강의실 예약 시스템 첫 이용"
    elif plus == 10: return "부정 이용 신고 접수 완료"
    elif plus == 5: return "정상 이용 완료 / 예약 취소"
    elif minus == 15: return "예약 시간 종료 후 미퇴실"
    else: return "기타 포인트 기록"


