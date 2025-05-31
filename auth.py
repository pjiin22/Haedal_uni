import mysql.connector
from fastapi import APIRouter, Form, Depends, HTTPException

router = APIRouter() 

def get_db_connection():
    """
    MySQL DB에 접속하는 함수
    """
    conn = mysql.connector.connect(
        host="localhost",           # 또는 db 서버 주소
        user="root",                # 사용자 계정
        password="@Imjiin61",   # 본인의 비밀번호
        database="haedal_uni"       # 사용할 데이터베이스
    )
    return conn

def verify_student_login(user_id: str, name: str, phone: str) -> bool:
    print("🔍 로그인 시도:", user_id, name, phone)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM users
        WHERE user_id = %s AND name = %s AND phone = %s
    """
    cursor.execute(query, (
    user_id.strip(), 
    name.strip(), 
    phone.strip()
))

    result = cursor.fetchone()

    print("✅ 결과:", result)

    cursor.close()
    conn.close()

    return result is not None