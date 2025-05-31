from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta

from app.database import get_db
from app.models import Reserve

router = APIRouter()

# ✅ 사용자별 총 이용 시간 및 횟수 조회 API
@router.get("/usage-summary/{user_id}")
def get_usage_summary(user_id: int, db: Session = Depends(get_db)):
    # 종료된 예약만 집계
    completed_reservations = db.query(Reserve).filter(
        Reserve.user_id == user_id,
        Reserve.status == "종료"
    ).all()

    if not completed_reservations:
        return {
            "user_id": user_id,
            "total_sessions": 0,
            "total_usage_minutes": 0
        }

    total_sessions = len(completed_reservations)
    total_minutes = sum(
        int((res.end_time - res.start_time).total_seconds() // 60)
        for res in completed_reservations
    )

    return {
        "user_id": user_id,
        "total_sessions": total_sessions,
        "total_usage_minutes": total_minutes
    }
