from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import os, shutil

from app.database import get_db
from app.models import Reserve
from app.schemas import ReservationRequest, ReservationResponse
from app.services.in_image import extract_room_number
from app.services.out_image import extract_room_number_for_checkout

router = APIRouter()

# ------------------------
# [1] 예약 생성 API
# ------------------------
@router.post("/reserve")
def create_reservation(res_req: ReservationRequest, db: Session = Depends(get_db)):
    overlap = db.query(Reserve).filter(
        Reserve.class_id == res_req.class_id,
        Reserve.end_time > res_req.start_time,
        Reserve.start_time < res_req.end_time,
    ).first()

    if overlap:
        raise HTTPException(status_code=400, detail="이미 해당 시간에 예약이 존재합니다.")

    new_reservation = Reserve(
        user_id=res_req.user_id,
        class_id=res_req.class_id,
        start_time=res_req.start_time,
        end_time=res_req.end_time,
        status="예약"
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return {
        "message": "예약이 완료되었습니다.",
        "reservation_id": new_reservation.reservation_id
    }

# ------------------------
# [2] 마이페이지 예약 조회 API
# ------------------------
@router.get("/my-reservations/{user_id}", response_model=List[ReservationResponse])
def get_user_reservations(user_id: int, db: Session = Depends(get_db)):
    reservations = db.query(Reserve).filter(
        Reserve.user_id == user_id
    ).order_by(Reserve.start_time.desc()).all()

    results = []
    for r in reservations:
        use_deadline = r.start_time + timedelta(minutes=10)
        results.append(ReservationResponse(
            reservation_id=r.reservation_id,
            class_id=r.class_id,
            start_time=r.start_time,
            end_time=r.end_time,
            status=r.status,
            use_auth_deadline=use_deadline
        ))

    return results

# ------------------------
# [3] 사용 인증 (사진 업로드) API
# ------------------------
@router.post("/auth-use")
def auth_use_reservation(
    reservation_id: int = Form(...),
    user_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    reservation = db.query(Reserve).filter(
        Reserve.reservation_id == reservation_id,
        Reserve.user_id == user_id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="예약 내역을 찾을 수 없습니다.")

    if reservation.status != "예약":
        raise HTTPException(status_code=400, detail="이미 인증되었거나 인증 불가한 상태입니다.")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, image.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    extracted_number = extract_room_number(file_path)

    if extracted_number != str(reservation.class_id):
        raise HTTPException(status_code=400, detail=f"인식된 강의실 번호({extracted_number})가 예약된 강의실과 일치하지 않습니다.")

    reservation.status = "사용중"
    db.commit()

    return {
        "message": "사용 인증 완료되었습니다.",
        "recognized_room": extracted_number,
        "status": reservation.status
    }

# ------------------------
# [4] 퇴실 인증 (사진 업로드) API
# ------------------------
@router.post("/auth-out")
def auth_out_reservation(
    reservation_id: int = Form(...),
    user_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    reservation = db.query(Reserve).filter(
        Reserve.reservation_id == reservation_id,
        Reserve.user_id == user_id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="예약 정보를 찾을 수 없습니다.")

    if reservation.status != "사용중":
        raise HTTPException(status_code=400, detail="현재 상태에서는 퇴실 인증이 불가능합니다.")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, image.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    extracted_number = extract_room_number_for_checkout(file_path)

    if extracted_number != str(reservation.class_id):
        raise HTTPException(status_code=400, detail=f"인식된 강의실 번호({extracted_number})가 예약 강의실과 다릅니다.")

    reservation.status = "종료"
    db.commit()

    return {
        "message": "퇴실 인증 완료되었습니다.",
        "recognized_room": extracted_number,
        "status": reservation.status
    }

# ------------------------
# [5] 예약 취소 API (예약 상태만 가능)
# ------------------------
@router.post("/cancel-reservation")
def cancel_reservation(
    reservation_id: int = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    reservation = db.query(Reserve).filter(
        Reserve.reservation_id == reservation_id,
        Reserve.user_id == user_id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="예약 정보를 찾을 수 없습니다.")

    if reservation.status != "예약":
        raise HTTPException(status_code=400, detail="예약 상태가 아니므로 취소할 수 없습니다.")

    db.delete(reservation)
    db.commit()

    return {"message": "예약이 취소되었습니다."}
