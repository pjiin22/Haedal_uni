from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# ⭐ 신뢰도 관리 클래스 정의
class TrustScoreManager:
    def __init__(self):
        self.user_scores = {}

    def _init_user(self, user_id):
        if user_id not in self.user_scores:
            self.user_scores[user_id] = 36.5

    def update(self, user_id: str, event: str):
        self._init_user(user_id)
        changes = {
            "on_time_check_in": 0.1,
            "check_in": 0.05,
            "check_out": 0.25,
            "report_empty_room": 0.5,
            "no_show": -0.3,
            "no_check_out": -0.1,
        }
        delta = changes.get(event)
        if delta is None:
            raise ValueError(f"알 수 없는 이벤트: {event}")
        new_score = self.user_scores[user_id] + delta
        self.user_scores[user_id] = max(0.0, min(100.0, new_score))
        return round(self.user_scores[user_id], 2)

    def get_score(self, user_id: str):
        self._init_user(user_id)
        return round(self.user_scores[user_id], 2)

# ✅ 인스턴스 생성
trust_manager = TrustScoreManager()

# ✅ 요청 모델
class TrustEvent(BaseModel):
    event: str  # "check_in", "check_out", "no_show" 등

# ✅ 신뢰도 조회
@router.get("/trust/{user_id}")
def get_trust_score(user_id: str):
    score = trust_manager.get_score(user_id)
    return {"user_id": user_id, "trust_score": score}

# ✅ 신뢰도 갱신 (PATCH)
@router.patch("/trust/{user_id}")
def update_trust_score(user_id: str, event_data: TrustEvent):
    try:
        updated_score = trust_manager.update(user_id, event_data.event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "user_id": user_id,
        "updated_event": event_data.event,
        "trust_score": updated_score
    }
