from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

# -----------------------------
# 사용자 (학생)
# -----------------------------
class User(Base):
    __tablename__ = "users"
    user_id = Column(String(20), primary_key=True)
    name = Column(String(50))
    phone = Column(String(20))
    total_point = Column(Integer, default=0)

# -----------------------------
# 강의실
# -----------------------------
class Class(Base):
    __tablename__ = "class"
    
    class_id = Column(Integer, primary_key=True, index=True)
    house_id = Column(Integer, index=True)                         # 호관 번호
    lock = Column(String(50))                                      # 잠금 여부

# -----------------------------
# 시간표
# -----------------------------
class Timetable(Base):
    __tablename__ = "timetable"
    
    lecture_id = Column(Integer, primary_key=True)                 # 강의 ID
    class_id = Column(Integer, index=True)                         # 강의실 번호
    start_time = Column(Integer)                                   # 시작 시간
    end_time = Column(Integer)                                     # 종료 시간
    weekend = Column(Integer)                                      # 요일 (0=월~6=일)

# -----------------------------
# 예약 정보
# -----------------------------
class Reserve(Base):
    __tablename__ = "reserve"
    __table_args__ = {'extend_existing': True}

    reservation_id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String(50), default="예약")                   # 상태: 예약, 사용중, 종료 등


# -----------------------------
# 포인트
# -----------------------------
class Point(Base):
    __tablename__ = "point"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20))
    plus = Column(Integer, default=0)
    minus = Column(Integer, default=0)
    time = Column(DateTime)