from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰")