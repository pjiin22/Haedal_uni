from pydantic import BaseModel
from datetime import datetime

class UserLogin(BaseModel):
    user_id: str
    name: str
    password: str



class ReservationRequest(BaseModel):
    user_id: int
    class_id: int
    start_time: datetime
    end_time: datetime


class ReservationResponse(BaseModel):
    reservation_id: int
    class_id: int
    start_time: datetime
    end_time: datetime
    status: str
    use_auth_deadline: datetime
