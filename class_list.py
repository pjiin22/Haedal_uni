from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Class, Timetable, Reserve  # 필요 테이블들

router = APIRouter()

@router.get("/classrooms/{house_id}")
def get_classrooms_by_house(house_id: int, db: Session = Depends(get_db)):
    now = datetime.now().hour  # 시간 기준만 본다고 가정 (분/요일 추가 가능)

    # 1. 해당 호관 강의실들 조회
    classrooms = db.query(Class).filter(Class.house_id == house_id).all()
    results = []

    for room in classrooms:
        locked = False

        # 2. 수동 잠금 여부
        if room.lock == "Y":
            locked = True
        else:
            # 3. timetable 또는 reserve 기준 자동 잠금 체크 (시작시간 <= now <= 종료시간)
            reserved = db.query(Reserve).filter(
                Reserve.class_id == room.class_id,
                Reserve.start_time <= now,
                Reserve.end_time >= now
            ).first()

            in_lecture = db.query(Timetable).filter(
                Timetable.class_id == room.class_id,
                Timetable.start_time <= now,
                Timetable.end_time >= now
            ).first()

            if reserved or in_lecture:
                locked = True

        results.append({
            "class_id": room.class_id,
            "locked": locked
        })

    return {"house_id": house_id, "classrooms": results}
