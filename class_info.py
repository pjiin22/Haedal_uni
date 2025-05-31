from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Reserve

router = APIRouter()

@router.get("/classrooms/{class_id}/availability")
def get_classroom_availability(
    class_id: int,
    date: str = Query(..., description="예약 날짜 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    # 시간대: 9시 ~ 17시
    all_slots = list(range(9, 18))
    reserved_slots = set()

    # 해당 날짜의 예약 중인 시간대 조회
    reservations = db.query(Reserve).filter(
        Reserve.class_id == class_id,
        Reserve.start_time < 18,
        Reserve.end_time > 9
    ).all()

    for res in reservations:
        res_date = res.start_time.strftime("%Y-%m-%d")
        if res_date == date:
            reserved_range = range(res.start_time.hour, res.end_time.hour)
            reserved_slots.update(reserved_range)

    # 시간별 예약 가능 여부 표시
    return [
        {"hour": h, "status": "예약중" if h in reserved_slots else "예약가능"}
        for h in all_slots
    ]
