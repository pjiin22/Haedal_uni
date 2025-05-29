from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Class  # class 테이블 모델

router = APIRouter()

@router.get("/houses")
def get_house_list(db: Session = Depends(get_db)):
    # 중복 제거된 건물번호(house_id) 목록 조회
    results = db.query(Class.house_id).distinct().all()
    houses = [{"house_id": h.house_id} for h in results]
    return {"houses": houses}

@router.get("/houses/{house_id}/classrooms")
def get_classrooms_by_house(house_id: int, db: Session = Depends(get_db)):
    classrooms = db.query(Class).filter(Class.house_id == house_id).all()
    return {
        "house_id": house_id,
        "classrooms": [
            {"class_id": c.class_id, "locked": c.lock} for c in classrooms
        ]
    }
