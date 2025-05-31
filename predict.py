from fastapi import APIRouter, Query, Depends
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app.point import get_points
from app.probability import ProbabilityManager, convert_point_to_trust_score

router = APIRouter()

@router.get("/predict/{user_id}")
def predict_probability(user_id: str, start_time: str = Query(...), db: Session = Depends(get_db)):
    start_dt = datetime.fromisoformat(start_time)
    elapsed_min = int((datetime.now() - start_dt).total_seconds() // 60)

    point_data = get_points(user_id, db)
    points = point_data["points"]
    trust_score = convert_point_to_trust_score(points)

    prob = ProbabilityManager().get_empty_probability(elapsed_min, trust_score)

    return {
        "user_id": user_id,
        "elapsed_time_min": elapsed_min,
        "points": points,
        "trust_score": round(trust_score, 2),
        "empty_probability": f"{prob}%"
    }